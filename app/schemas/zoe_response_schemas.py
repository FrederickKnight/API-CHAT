from pydantic import BaseModel, Field, PrivateAttr, model_validator, field_validator
from .enums import ExampleMoodsEnum

class ZoeMessageSchema(BaseModel):
    role:str
    content:str
    moods:list[ExampleMoodsEnum]

class ZoeMessagesSummary(BaseModel):
    content:str
    average_mood:ExampleMoodsEnum

class ZoeContentSchema(BaseModel):
    recent_messages:list[ZoeMessageSchema]
    summary:ZoeMessagesSummary
    last_message:str
    relation_score:float
    instruction:str

class ZoeResponseSchema(BaseModel):
    content:str
    moods:list[ExampleMoodsEnum]

class AIContentMoodsSchema(BaseModel):
    instruction:str
    message:str

class ZoeResponseWelcomeMessageSchema(BaseModel):
    instruction:str
    relation_score:float