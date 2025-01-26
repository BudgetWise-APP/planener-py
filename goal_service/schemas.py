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
    id: Optional[PyObjectId] = Field(default=None, alias='_id')
    user_id: PyObjectId
    title: str
    description: Optional[str] = None
    goal: int
    currentStatus: int
    isFavorite: bool = False
    done: bool = False
    trackBy: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
