from .base_auth_controller import BaseAuthController

from app.models import (
    User,
    Session
)

from app.schemas import (
    UserSchema,
    SessionSchema
)

class AuthUserController(BaseAuthController):
    def __init__(self):
        
        super().__init__(
            user_model=User,
            user_schema=UserSchema,
            session_model=Session,
            session_schema=SessionSchema,
        )