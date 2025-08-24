from app.models import (
    BaseCreatedModel
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from sqlalchemy import (
    ForeignKey,
)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models import (
        User,
        Room
    )

class Message(BaseCreatedModel):
    content:Mapped[str]

    id_room:Mapped[int] = mapped_column(ForeignKey("room.id"))
    room:Mapped["Room"] = relationship("Room",back_populates="messages")

    id_user:Mapped[int] = mapped_column(ForeignKey("user.id"))
    user:Mapped["User"] = relationship("User",back_populates="messages")