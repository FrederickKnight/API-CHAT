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
    event
)

from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from app.models import (
        User,
        UserZoe,
        Room
    )

class Message(BaseCreatedModel):
    content:Mapped[str]

    id_room:Mapped[int] = mapped_column(ForeignKey("room.id"))
    room:Mapped["Room"] = relationship("Room",back_populates="messages")

    id_user:Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"))
    user:Mapped[Optional["User"]] = relationship("User",back_populates="messages")

    id_zoe:Mapped[Optional[int]] = mapped_column(ForeignKey("user_zoe.id"))
    zoe:Mapped[Optional["UserZoe"]] = relationship("UserZoe",back_populates="messages")


@event.listens_for(Message,"before_update")
@event.listens_for(Message,"before_insert")
def validate_message_emitter(mapper, connection, target: "Message"):
    if target.id_user and target.id_zoe:
        raise ValueError("the sender must be just one, cant be user and zoe.")
    if not target.id_user and not target.id_zoe:
        raise ValueError("the sender ust be one, cant be None for user or zoe.")