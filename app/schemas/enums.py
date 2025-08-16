from enum import Enum

    
class AuthLevelEnum(Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    WORKER = "worker"
