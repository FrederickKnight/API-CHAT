from .base_controller import BaseController

from app.models import (
    Message
)

from app.schemas import (
    MessageSchema
)

class MessageController(BaseController):
    def __init__(self):
        super().__init__(
            model=Message,
            schema=MessageSchema
        )