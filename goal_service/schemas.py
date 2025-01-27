from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return ObjectId(v)
    

class GoalSchema(BaseModel):
    user_id: Optional[PyObjectId] = Field(default = None, alias='user_id')
    title: str
    description: Optional[str] = None
    goal: float
    currentStatus: float
    isFavorite: bool = False
    done: bool = False
    trackBy: str = ""

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
