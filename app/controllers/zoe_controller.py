from .base_controller import BaseController

from app.models import (
    UserZoe
)

from app.schemas import (
    UserZoeSchema
)

class ZoeController(BaseController):
    def __init__(self):
        super().__init__(
            model=UserZoe,
            schema=UserZoeSchema
        )