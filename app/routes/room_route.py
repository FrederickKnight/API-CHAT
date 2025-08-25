from flask import Blueprint

from app.controllers import RoomController, RoomUserController

from .base_route import BaseRoute

class RoomRoute(BaseRoute):
    def __init__(self):
        room_bp = Blueprint("room",__name__)

        super().__init__(room_bp,RoomController())

class RoomUserRoute(BaseRoute):
    def __init__(self):
        room_user_bp = Blueprint("room_user",__name__)

        super().__init__(room_user_bp,RoomUserController())