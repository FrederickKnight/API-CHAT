from flask import Blueprint

from app.controllers import ExampleController

from .base_route import BaseRoute

class ExampleRoute(BaseRoute):
    def __init__(self):
        example_bp = Blueprint("example",__name__)

        super().__init__(example_bp,ExampleController())