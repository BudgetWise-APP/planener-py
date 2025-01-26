from pydantic import BaseModel, Field
from typing import Optional, List
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


class BudgetItemSchema(BaseModel):
    icon: Optional[str] = None
    title: str
    amount: str
    description: Optional[str] = None


class BudgetItemsSchema(BaseModel):
    essentialNeeds: List[BudgetItemSchema] = []
    personalWants: List[BudgetItemSchema] = []
    savings: List[BudgetItemSchema] = []


class BudgetSchema(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias='_id')
    user_id: Optional[PyObjectId] = Field(default = None)
    title: str
    income: str
    currency: str
    budgetType: Optional[str] = None
    items: BudgetItemsSchema = BudgetItemsSchema()

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
