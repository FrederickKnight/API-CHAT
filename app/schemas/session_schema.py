from pydantic import BaseModel, Field, PrivateAttr, model_validator, field_validator
from app.utils import create_timestampt

class SessionSchema(BaseModel):
    id_user:int
    session:str
    expires_at:int = Field(default_factory=create_timestampt)

    @field_validator("expires_at",mode="before")
    @classmethod
    def validate_expires_at(cls,expires_at):

        if not isinstance(expires_at,int):
            raise TypeError(f"Expected a timestamp as integer, not {type(expires_at).__name__}")

        return expires_at