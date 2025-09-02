from flask import Blueprint

from app.controllers import ZoeController

from .base_route import BaseRoute

class ZoeRoute(BaseRoute):
    def __init__(self):
        zoe_bp = Blueprint("zoe",__name__)

        super().__init__(zoe_bp,ZoeController())