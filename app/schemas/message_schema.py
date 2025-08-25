from pydantic import BaseModel, Field, PrivateAttr, model_validator, field_validator

class MessageSchema(BaseModel):
    id:int = None
    content:str

    id_room:int
    id_user:int