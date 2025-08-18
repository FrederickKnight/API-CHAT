from enum import Enum

    
class AuthLevelEnum(Enum):
    ADMIN = "admin"
    USER = "user"
    WORKER = "worker"

class TypeRoomEnum(Enum):
    PRIVATE = "private"
    GROUP = "group"