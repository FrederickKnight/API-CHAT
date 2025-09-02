import uuid

from app.models import (
    BaseCreatedModel
)

from sqlalchemy.orm import (
    Session,
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
        Message,
        UserZoe
    )

from sqlalchemy.dialects.postgresql import ENUM
from app.schemas import TypeRoomEnum

type_room_enum = ENUM(*[tp.value for tp in TypeRoomEnum],name="type_room",create_type=True)

class Room(BaseCreatedModel):
    uuid:Mapped[Optional[str]] = mapped_column(default=None,unique=True)

    name:Mapped[str]
    type_room:Mapped[TypeRoomEnum] = mapped_column(type_room_enum,default=TypeRoomEnum.PRIVATE.value)

    users:Mapped[list["RoomUser"]] = relationship("RoomUser",back_populates="room",cascade="all, delete-orphan")
    
    messages:Mapped[list["Message"]] = relationship("Message",back_populates="room",cascade="all, delete-orphan")
    
@event.listens_for(Room, "before_insert")
def generate_uuid(mapper, connection, target:Room):

    session = Session(bind = connection)

    while True:
        generated_uuid = str(uuid.uuid4())

        exist = session.query(Room).filter_by(uuid = generated_uuid).first()

        if not exist:
            target.uuid = generated_uuid
            break

class RoomUser(BaseCreatedModel):
    id_room:Mapped[int] = mapped_column(ForeignKey("room.id"))
    room:Mapped["Room"] = relationship("Room",back_populates="users")

    id_user:Mapped[int] = mapped_column(ForeignKey("user.id"))
    user:Mapped["User"] = relationship("User",back_populates="rooms")

    id_zoe:Mapped[int] = mapped_column(ForeignKey("user_zoe.id"))
    zoe:Mapped["UserZoe"] = relationship("UserZoe",back_populates="room")