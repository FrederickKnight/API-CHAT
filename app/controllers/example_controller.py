from .base_controller import BaseController

from app.models import(
    Example
)

from app.schemas import (
    ExampleSchema
)

class ExampleController(BaseController):
    def __init__(self):

        example_defaults = {
            "name" : None,
            "quantity" : None,
            "user_id" : None
        }

        super().__init__(
            model=Example,
            schema=ExampleSchema,
            defaults=example_defaults
        )