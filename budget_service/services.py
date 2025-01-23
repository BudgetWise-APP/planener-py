from fastapi import HTTPException
from budget_service.schemas import BudgetSchema
from common.config import JWT_SECRET, ALGORITHM
from jose import jwt, JWTError
from bson import ObjectId
from common.mongo_client import db


def get_userid_from_jwt(token: str):
    try:
        print(token)
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        print(payload)
        userId: str = payload.get("userId")
        if userId is None:
            raise HTTPException(status_code=401, detail="UserID not found in token")
        return ObjectId(userId)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


class BudgetService:
    @staticmethod
    async def get_budgets(user_id: ObjectId):
        budgets = await db.budgets.find({"user_id": user_id}, {"user_id": 0}).to_list(
            None
        )
        for budget in budgets:
            budget["_id"] = str(budget["_id"])
        return budgets

    @staticmethod
    async def create_budget(budget: BudgetSchema):
        await db.budgets.insert_one(budget.model_dump(by_alias=True))

    @staticmethod
    async def get_budget_by_id(budget_id: str, user_id: ObjectId):
        budget = await db.budgets.find_one(
            {"_id": ObjectId(budget_id), "user_id": user_id}, {"user_id": 0}
        )
        if budget is None:
            raise HTTPException(status_code=404, detail="Budget not found")
        budget["_id"] = str(budget["_id"])
        return budget

    @staticmethod
    async def update_budget(budget_id: str, budget: BudgetSchema, user_id: ObjectId):
        await db.budgets.find_one_and_update(
            {"_id": ObjectId(budget_id), "user_id": user_id},
            {"$set": budget.model_dump(by_alias=True)},
        )
        return {"message": "Budget updated successfully"}

    @staticmethod
    async def delete_budget(budget_id: str, user_id: ObjectId):
        await db.budgets.find_one_and_delete(
            {"_id": ObjectId(budget_id), "user_id": user_id}
        )
        return {"message": "Budget deleted successfully"}
