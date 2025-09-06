from app.models import (
    BaseCreatedModel,
    BaseModel
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from sqlalchemy import (
    ForeignKey,
    event,
    insert
)

from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from app.models import (
        User,
        UserZoe,
        Room
    )

from sqlalchemy.engine import Connection
from sqlalchemy.dialects.postgresql import (
     ENUM,
     ARRAY
)

from app.schemas import (
    ExampleMoodsEnum,
    AIContentMoodsSchema
)

from app import (
    zoe_client
)
from google.genai import types
import json


class Message(BaseCreatedModel):
    content:Mapped[str]

    id_room:Mapped[int] = mapped_column(ForeignKey("room.id"))
    room:Mapped["Room"] = relationship("Room",back_populates="messages")

    id_user:Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"))
    user:Mapped[Optional["User"]] = relationship("User",back_populates="messages")

    id_zoe:Mapped[Optional[int]] = mapped_column(ForeignKey("user_zoe.id"))
    zoe:Mapped[Optional["UserZoe"]] = relationship("UserZoe",back_populates="messages")

    moods:Mapped[Optional["MessageMood"]] = relationship("MessageMood",back_populates="message",cascade="all, delete-orphan",uselist=False)


@event.listens_for(Message,"before_update")
@event.listens_for(Message,"before_insert")
def validate_message_emitter(mapper, connection, target: "Message"):
    if target.id_user and target.id_zoe:
        raise ValueError("the sender must be just one, cant be user and zoe.")
    if not target.id_user and not target.id_zoe:
        raise ValueError("the sender ust be one, cant be None for user or zoe.")
    
@event.listens_for(Message,"after_insert")
def moods_for_message(mapper, connection:Connection, target: "Message"):

    # detectar de quien es

    # generar mood list

    _instruction = """
    Determina tres y solo tres moods que expliquen lo mejor posible el mood del mensaje
    """

    _content = AIContentMoodsSchema(
        instruction=_instruction,
        message=target.content
    )

    ai_response = zoe_client.models.generate_content(
        model= "gemini-2.5-flash",
        contents= _content.model_dump_json(),
        config= types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0),
            response_mime_type="application/json",
            response_schema= list[ExampleMoodsEnum]
        )
    )

    try:
        moods_from_ai = json.loads(ai_response.text)
    except json.JSONDecodeError:
        moods_from_ai = []

    valid_moods = [mood for mood in moods_from_ai if mood in [ex.value for ex in ExampleMoodsEnum]]
    
    connection.execute(
        insert(MessageMood).values(
            id_message = target.id,
            mood = valid_moods
        )
    )

moods_conversation = ENUM(*[mood.value for mood in ExampleMoodsEnum], name="moods_conversation",create_type=True)

class MessageMood(BaseModel):
    id_message:Mapped[int] = mapped_column(ForeignKey("message.id"))
    message:Mapped["Message"] = relationship("Message",back_populates="moods")

    mood:Mapped[list[ExampleMoodsEnum]] = mapped_column(ARRAY(moods_conversation),default=list)