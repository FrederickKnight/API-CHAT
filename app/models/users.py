from app.models import (
    BaseUser,
    BaseCreatedModel
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from app.models import (
        Session,
        RoomUser,
        Message,
        MessageWelcome
    )

from sqlalchemy.dialects.postgresql import ENUM
from app.schemas import AuthLevelEnum
from sqlalchemy import (
    ForeignKey,
    event
)

auth_level_enum = ENUM(*[level.value for level in AuthLevelEnum], name="auth_level_type",create_type=True)

class User(BaseUser):
    auth_level:Mapped[AuthLevelEnum] = mapped_column(auth_level_enum,default=AuthLevelEnum.USER.value)

    user_session:Mapped["Session"] = relationship("Session",back_populates="user",uselist=False)

    rooms:Mapped[list["RoomUser"]] = relationship("RoomUser",back_populates="user",cascade="all, delete-orphan")

    messages:Mapped[list["Message"]] = relationship("Message",back_populates="user",cascade="all, delete-orphan")
    
    welcome_message:Mapped["MessageWelcome"] = relationship("MessageWelcome",back_populates="user")

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

class UserZoe(BaseCreatedModel):
    name:Mapped[str] = mapped_column(default="ZOE")
    nickname:Mapped[Optional[str]]

    user_nickname:Mapped[Optional[str]]
    relation:Mapped[Optional[float]] = mapped_column(default=0.0)

    room:Mapped["RoomUser"] = relationship("RoomUser",back_populates="zoe")

    messages:Mapped[list["Message"]] = relationship("Message",back_populates="zoe",cascade="all, delete-orphan")

@event.listens_for(UserZoe,"after_update")
@event.listens_for(UserZoe,"after_insert")
def validate_relation_number(mapper, connection, target: "UserZoe"):

    if not isinstance(target.relation,float):
        raise TypeError("relation must be a valid float number")
    
    target.relation = min(0,max(target.relation,100))