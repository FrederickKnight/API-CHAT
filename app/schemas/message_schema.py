from pydantic import BaseModel, Field, PrivateAttr, model_validator, field_validator

class MessageSchema(BaseModel):
    id:int = None
    content:str

    id_room:int
    id_user:int = None
    id_zoe:int = None

    @model_validator(mode="after")
    def validate_users(self):
        if self.id_user and self.id_zoe:
            raise ValueError("the sender must be just one, cant be user and zoe.")
        if not self.id_user and not self.id_zoe:
            raise ValueError("the sender ust be one, cant be None for user or zoe.")