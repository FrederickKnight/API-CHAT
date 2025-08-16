from pydantic import BaseModel, Field, PrivateAttr, model_validator, field_validator
from .enums import AuthLevelEnum

username_len = 3

class UserSchema(BaseModel):
    username:str
    password:str
    is_active:bool = Field(default=True)
    auth_level:str = Field(default=AuthLevelEnum.WORKER.value)

    @field_validator("username",mode="before")
    @classmethod
    def validate_username(cls,username):

        if not isinstance(username,str):
            raise TypeError(f"Expected string, got {type(username).__name__}")
        
        if not len(username) > username_len:
            raise ValueError(f"Username must be more than {username_len} chars")

        return username
    
    @field_validator("password",mode="before")
    @classmethod
    def validate_password(cls,password):

        if not isinstance(password,str):
            raise TypeError(f"Expected string, got {type(password).__name__}")
        
        # More validations like password contains numbers and chars or etc, later on
        
        return password