from app.models import (
    BaseSession
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from sqlalchemy import (
    ForeignKey
)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models import (
        User
    )

class Session(BaseSession):
    id_user:Mapped[int] = mapped_column(ForeignKey("user.id"),unique=True)
    user:Mapped["User"] = relationship("User",back_populates="user_session")