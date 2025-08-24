from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import request
from app.controllers import RoomController, RoomUserController, MessageController, AuthUserController

from app import socketio

user_controller = AuthUserController()

@socketio.on("connect")
def handle_connect():
    print("Cliente conectado")

@socketio.on("join")
def handle_join(data):
    room = data["room"]
    join_room(room)

    user = data["user"]

    message = {
        "user": {
            "id":user["id"],
            "username":user["username"]

        }, 
        "msg": f"{user['username']} se unió"
    }

    print(message)
    emit("message", message, to=room)

@socketio.on("send_room_message")
def handle_message(data):
    room = data["room"]
    msg = data["msg"]
    user = data["user"]

    message = {
        "user": user,
        "msg":msg
    }
    print(msg)

    emit("message",message,to=room)