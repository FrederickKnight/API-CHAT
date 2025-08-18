from app.models import BaseModel
from flask import Response
from pydantic import BaseModel, Field, PrivateAttr, model_validator, field_validator
from typing import Self
import re


class JsonResponse(BaseModel):
    response:dict | list
    type:str
    pagination_data:dict = Field(default_factory=dict)

    _size:int = PrivateAttr(default=0)

    @field_validator("response",mode="before")
    @classmethod
    def validate_response(cls,response) -> dict | list:

        if isinstance(response,dict) or isinstance(response,list):
            return response
        
        if isinstance(response,Response):
            return response.get_json()
        
        return response
        
    @model_validator(mode="after")
    def validate_json(self) -> Self:
        self._size = len([self.response]) if isinstance(self.response,Response) else len(self.response)

        return self
    
    def get_response(self):
        return {
            "response":["Base Response"],
            "metadata":{
                "type":"schema",
                "size":self._size,
                "api_version":"v0",
                "type_response":"list" if isinstance(self.response,list) else "dict",
                "pagination":{
                    "page":self.pagination_data.get("page",0),
                    "pages":self.pagination_data.get("pages",0),
                    "limit":self.pagination_data.get("limit",0),
                    "total":self.pagination_data.get("total",0)
                }
            }
        }

class JsonResponseV1(JsonResponse):
    def get_response(self):
        schema = {
            "response":self.response,
            "metadata":{
                "type":self.type,
                "size":self._size,
                "api_version":"v1",
                "type_response":"list" if isinstance(self.response,list) else "dict",
                "pagination":{
                    "page":self.pagination_data.get("page",0),
                    "pages":self.pagination_data.get("pages",0),
                    "limit":self.pagination_data.get("limit",0),
                    "total":self.pagination_data.get("total",0)
                }
            }
        }

        if not isinstance(self.response,list):
            schema["metadata"]["response_id"] = self.response.get("id",None)
            
        return schema
    
version_list:dict[str,JsonResponse] = {
    "v1": JsonResponseV1,
}

def get_version(version:str = None) ->JsonResponse:
    if not version:
        return JsonResponseV1
    
    re_version = re.search(r'templatename\.v(\d+)', version.lower())
    _version = f"v{re_version.group(1)}" if re_version else "v1"
    
    return version_list.get(_version,None)