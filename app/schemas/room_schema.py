from pydantic import BaseModel, Field, PrivateAttr, model_validator, field_validator
from .enums import TypeRoomEnum

class RoomSchema(BaseModel):
    name:str
    type_room:str = Field(default=TypeRoomEnum.PRIVATE.value)


class RoomUserSchema(BaseModel):
    id_room:int
    id_user:int