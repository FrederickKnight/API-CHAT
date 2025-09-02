from flask_socketio import SocketIO, emit, join_room, leave_room

from app import socketio,db

from app.models import (
    Room,
    RoomUser,
    Message,
    User
)

from app.schemas import(
    MessageSchema
)

session = db.session

@socketio.on("connect")
def handle_connect():
    print("Cliente conectado")

@socketio.on("disconnect")
def handle_connect():
    print("Cliente desconectado")

@socketio.on("join")
def handle_join(data):
    if not check_if_user_room(
            id_user = data["user"]["id"],
            id_room = data["room"]
        ):
        raise ValueError("User is not in that chat room")

    room_uuid = get_room_uuid(
        id = data["room"]
    )

    join_room(room_uuid)
    user = data["user"]

    message = {
        "user": {
            "id":0,
            "username":"System"

        },
        "content": f"{user['username']} se unió"
    }

    emit("user_room_online", message, to=room_uuid)

@socketio.on("send_room_message")
def handle_message(data):
    room = data["room"]
    content = data["content"]
    user = data["user"]

    room_uuid = get_room_uuid(
        id = room
    )

    message = {
        "user": user,
        "content":content
    }

    add_message(
        id_room = room,
        id_user = user["id"],
        content = content
    )

    emit("message",message,to=room_uuid)

def add_message(id_room:int,id_user:int,content:str):
    message = MessageSchema(
        id_room = id_room,
        id_user = id_user,
        content = content
    )

    try:
        session.add(Message(**message.model_dump(exclude="id")))
        session.commit()

    except Exception as e:
        session.rollback()
        raise e


def get_room_uuid(id:int) -> str:
    _room = session.query(Room).filter_by(id = id).first()
    if not _room:
        raise ValueError("Not a valid room")
    
    return _room.uuid

def check_if_user_room(id_user:int,id_room:int):
    user = session.query(User).filter_by(id = id_user).first()
    if not user:
        raise ValueError("User is not valid")
    
    room = session.query(Room).filter_by(id = id_room).first()
    if not room:
        raise ValueError("Room is not valid")
    
    return True if session.query(RoomUser).filter_by(id_room = id_room).filter_by(id_user = id_user).first() else False