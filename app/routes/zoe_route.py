from flask import Blueprint,request

from app.controllers import ZoeController

from .base_route import BaseRoute

zoe_controller = ZoeController()
zoe_bp = Blueprint("zoe",__name__)

class ZoeRoute(BaseRoute):
    def __init__(self):
        super().__init__(zoe_bp,zoe_controller)

    @zoe_bp.route("/user/<int:id>/welcome-message",methods=["GET"],strict_slashes=False)
    def route_get_welcome_message(id):
        return zoe_controller.controller_welcome_message(
            id = id,
            request = request
        )