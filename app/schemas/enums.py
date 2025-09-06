from enum import Enum
    
class AuthLevelEnum(Enum):
    ADMIN = "admin"
    USER = "user"

class TypeRoomEnum(Enum):
    PRIVATE = "private"
    GROUP = "group"

class ExampleMoodsEnum(Enum):
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    FRUSTRATED = "frustrated"
    ANXIOUS = "anxious"
    HOPEFUL = "hopeful"
    GRATEFUL = "grateful"
    LONELY = "lonely"
    CURIOUS = "curious"
    CONFUSED = "confused"
    EXCITED = "excited"
    AFFECTIONATE = "affectionate"
    ENCOURAGING = "encouraging"
    WORRIED = "worried"
    NEUTRAL = "neutral"