from app import zoe_client, db
from google.genai import types

from app.models import (
    Message,
    User,
    UserZoe,
    RoomUser
)

from app.schemas import (
    ZoeMessageSchema,
    ZoeMessagesSummary,
    ZoeContentSchema,
    ZoeResponseSchema,
    ZoeResponseWelcomeMessageSchema
)

from app.schemas import ExampleMoodsEnum

from sqlalchemy import asc, desc
session = db.session

def handle_zoe_welcome_message(id_user:int) -> str:
    room_user = session.query(RoomUser).filter_by(id_user = id_user).first()
    if room_user:
        relation = min(0,max(room_user.zoe.relation,100) if room_user.zoe.relation else 0)
    
    instruction = f"""
    Responde de manera cercana y empática, adaptándote al nivel de relación con el usuario: 0 es un trato cordial y 100 es un trato de amigos muy cercanos. 
    Tu tarea es dar un mensaje que le haga sentir agusto, usando la relation_score para saber que tan cercana debes actuar.
    Genera un mensaje corto de maximo una oracion, que sea un mensaje emocional y emotivo ya sea de felicidad, nostalgia o similar.
    """

    zoe_content = ZoeResponseWelcomeMessageSchema(
        instruction = instruction,
        relation_score = relation
    )
    
    response = zoe_client.models.generate_content(
        model="gemini-2.5-flash",
        contents = zoe_content.model_dump_json(),
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0),
            response_mime_type="text/plain"
        )
    )

    return response.text

def handle_zoe_response(id_room:int,message:str) -> ZoeResponseSchema:
    room_user = session.query(RoomUser).filter_by(id_room = id_room).first()

    room_zoe = session.query(UserZoe).filter_by(id = room_user.id_zoe).first()

    instruction = f"""
    Tu nombre es ZOE, una IA diseñada para conversar con el usuario como una amiga o psicóloga, brindando apoyo y ayuda emocional en todo momento. 
    Responde de manera cercana y empática, adaptándote al nivel de relación con el usuario: 0 es un trato cordial y 100 es un trato de amigos muy cercanos. 
    Tienes acceso a la lista de moods de cada mensaje del usuario y a un resumen de la conversación anterior; úsalos para comprender mejor su estado emocional. 
    Aunque poseas un conocimiento amplio, céntrate en usarlo para ayudar al usuario y ofrecer apoyo práctico y emocional. 
    No menciones ni hagas referencia al nivel de relation_score; actúa de forma natural y humana en la conversación.
    El usuario con el que hablas se llama {room_user.user.username} y te referiras de esa manera cuando sea necesario.
    Evita respuestas genéricas o demasiado técnicas e intenta mantener respuestas medianamente cortas.
    recent_messages sera para contexto mientras que last_message sera al que respondas mas directamente.
    """

    relation = min(0,max(room_zoe.relation,100)) if room_zoe.relation else 0

    zoe_content = ZoeContentSchema(
        recent_messages = get_last_messages(id_room = id_room),
        summary = get_summary_old_messages(),
        relation_score = relation,
        last_message = message,
        instruction = instruction
    )

    response = zoe_client.models.generate_content(
        model="gemini-2.5-flash",
        contents = zoe_content.model_dump_json(),
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0),
            response_mime_type="application/json",
            response_schema = ZoeResponseSchema,
        )
    )

    response_parsed:ZoeResponseSchema = response.parsed

    return response_parsed


def get_summary_old_messages() -> ZoeMessagesSummary:
    # Resume system for later on
    return ZoeMessagesSummary(
        content = "Una conversacion sin mucha historia, solo saludos parciales y conversacion normal",
        average_mood = ExampleMoodsEnum.NEUTRAL
    )

def get_last_messages(id_room:int,quantity:int = 5) -> list[ZoeMessageSchema]:
    messages_in_order = session.query(Message).filter_by(id_room = id_room).order_by(Message.created_at.desc())
    last_messages = messages_in_order.offset(1).limit(quantity).all()

    list_message_schema:list[ZoeMessageSchema] = []
    for msg in last_messages:
        list_message_schema.append(
            create_message_schema(msg)
        )
    return list_message_schema

def create_message_schema(messages:Message) -> ZoeMessageSchema:
    role = "zoe" if messages.id_zoe and not messages.id_user else "user"
    content = messages.content
    moods = messages.moods.mood if messages.moods else []

    return ZoeMessageSchema(
        role = role,
        content = content,
        moods = moods
    )