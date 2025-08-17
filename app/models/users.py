from app.models import (
    BaseModel,
    BaseUser
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models import (
        Session,
    )

from sqlalchemy.dialects.postgresql import ENUM
from app.schemas.enums import AuthLevelEnum

auth_level_enum = ENUM(*[level.value for level in AuthLevelEnum], name="auth_level_type",create_type=True)

class User(BaseUser):
    auth_level:Mapped[AuthLevelEnum] = mapped_column(auth_level_enum,default=AuthLevelEnum.WORKER.value)

    user_session:Mapped["Session"] = relationship("Session",back_populates="user",uselist=False)

    def check_auth_level(self,levels):
        if self.auth_level.lower() == AuthLevelEnum.ADMIN:
            return True
        
        auth_level = self.auth_level.lower()

        if isinstance(levels,list):
            levels_lower = [level.lower() if isinstance(level, str) else level for level in levels]
            return auth_level in levels_lower
        elif isinstance(levels,str):
            return auth_level == levels.lower()
        
        return False