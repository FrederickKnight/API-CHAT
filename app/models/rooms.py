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
        Message
    )

from sqlalchemy.dialects.postgresql import ENUM
from app.schemas import TypeRoomEnum

type_room_enum = ENUM(*[tp.value for tp in TypeRoomEnum],name="type_room",create_type=True)

class Room(BaseCreatedModel):
    name:Mapped[str]
    type_room:Mapped[TypeRoomEnum] = mapped_column(type_room_enum,default=TypeRoomEnum.PRIVATE.value)

    users:Mapped[list["RoomUser"]] = relationship("RoomUser",back_populates="room",cascade="all, delete-orphan")
    
    messages:Mapped[list["Message"]] = relationship("Message",back_populates="room",cascade="all, delete-orphan")

class RoomUser(BaseCreatedModel):
    id_room:Mapped[int] = mapped_column(ForeignKey("room.id"))
    room:Mapped["Room"] = relationship("Room",back_populates="users",cascade="all, delete-orphan")

    id_user:Mapped[int] = mapped_column(ForeignKey("user.id"))
    user:Mapped["User"] = relationship("User",back_populates="rooms",cascade="all, delete-orphan")