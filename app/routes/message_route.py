from flask import Blueprint

from app.controllers import MessageController

from .base_route import BaseRoute

class MessageRoute(BaseRoute):
    def __init__(self):
        message_bp = Blueprint("message",__name__)

        super().__init__(message_bp,MessageController())