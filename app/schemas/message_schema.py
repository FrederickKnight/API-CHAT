from pydantic import BaseModel, Field, PrivateAttr, model_validator, field_validator

class MessageSchema(BaseModel):
    content:str

    id_room:int
    id_user:int