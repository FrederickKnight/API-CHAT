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

from .zoe import (
    handle_zoe_response
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

    room = get_room(
        id = data["room"]
    )

    join_room(room.uuid)
    user = data["user"]

    message = {
        "user": {
            "id":0,
            "username":"System"

        },
        "content": f"{user['username']} se unió"
    }

    emit("user_room_online", message, to=room.uuid)

@socketio.on("send_room_message")
def handle_message(data):
    id_room = data["room"]
    content = data["content"]
    user = data["user"]

    room = get_room(
        id = id_room
    )

    message = {
        "user": user,
        "content":content
    }

    emit("message",message,to=room.uuid)

    add_message(
        id_room = id_room,
        id_user = user["id"],
        content = content
    )


@socketio.on("send_zoe_message")
def handle_zoe_message(data):
    id_room = data["room"]
    content = data["content"]
    user = data["user"]

    room = get_room(
        id = id_room
    )

    # Message from user to register
    message = {
        "user": user,
        "content":content
    }

    emit("message",message,to=room.uuid)

    add_message(
        id_room = id_room,
        id_user = user["id"],
        content = content
    )

    # Message from zoe
    zoe_response = handle_zoe_response(
        id_room = id_room,
        message = content
    )

    room_user = get_room_user(
        id_room = id_room
    )

    add_message(
        id_room = id_room,
        id_zoe = room_user.id_zoe,
        content = zoe_response.content
    )

    zoe_message = {
        "zoe" : {
            "id":room_user.zoe.id,
            "name":room_user.zoe.name,
            "nickname":room_user.zoe.nickname,
            "user_nickname":room_user.zoe.user_nickname
        },
        "content" : zoe_response.content
    }

    emit("message",zoe_message,to=room.uuid)


def add_message(id_room:int,content:str,id_user:int = None,id_zoe:int = None):

    if id_user and not id_zoe:
        message = MessageSchema(
            id_room = id_room,
            id_user = id_user,
            content = content
        )

    elif id_zoe and not id_user:
        message = MessageSchema(
            id_room = id_room,
            id_zoe = id_zoe,
            content = content
        )

    try:
        session.add(Message(**message.model_dump(exclude="id")))
        session.commit()

    except Exception as e:
        session.rollback()
        raise e


def get_room(id:int) -> Room:
    _room = session.query(Room).filter_by(id = id).first()
    if not _room:
        raise ValueError("Not a valid room")
    
    return _room

def get_room_user(id_room:int) -> RoomUser:
    _roomuser = session.query(RoomUser).filter_by(id_room = id_room).first()
    if not _roomuser:
        raise ValueError("Not a valid room")
    
    return _roomuser

def check_if_user_room(id_user:int,id_room:int):
    user = session.query(User).filter_by(id = id_user).first()
    if not user:
        raise ValueError("User is not valid")
    
    room = session.query(Room).filter_by(id = id_room).first()
    if not room:
        raise ValueError("Room is not valid")
    
    return True if session.query(RoomUser).filter_by(id_room = id_room).filter_by(id_user = id_user).first() else False