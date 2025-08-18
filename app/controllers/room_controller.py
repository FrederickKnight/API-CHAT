from .base_controller import BaseController

from app.models import(
    Room,
    RoomUser
)

from app.schemas import (
    RoomSchema,
    RoomUserSchema
)

class RoomController(BaseController):
    def __init__(self):
        super().__init__(
            model=Room,
            schema=RoomSchema
        )

class RoomUserController(BaseController):
    def __init__(self):
        super().__init__(
            model=RoomUser,
            schema=RoomUserSchema
        )