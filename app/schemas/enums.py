from enum import Enum
    
class AuthLevelEnum(Enum):
    ADMIN = "admin"
    USER = "user"

class TypeRoomEnum(Enum):
    PRIVATE = "private"
    GROUP = "group"