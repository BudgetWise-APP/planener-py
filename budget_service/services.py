from fastapi import HTTPException
from budget_service.schemas import BudgetSchema
from bson import ObjectId
from common.mongo_client import db

class BudgetService:
    @staticmethod
    async def get_budgets(user_id: str):
        budgets = await db.budgets.find({"user_id": ObjectId(user_id)}, {"user_id": 0}).to_list(
            None
        )
        for budget in budgets:
            budget["_id"] = str(budget["_id"])
        return budgets

    @staticmethod
    async def create_budget(budget: BudgetSchema):
        await db.budgets.insert_one(budget.model_dump(by_alias=True))

    @staticmethod
    async def get_budget_by_id(budget_id: str, user_id: str):
        budget = await db.budgets.find_one(
            {"_id": ObjectId(budget_id), "user_id": ObjectId(user_id)}, {"user_id": 0}
        )
        if budget is None:
            raise HTTPException(status_code=404, detail="Budget not found")
        budget["_id"] = str(budget["_id"])
        return budget

    @staticmethod
    async def update_budget(budget_id: str, budget: BudgetSchema, user_id: str):
        await db.budgets.find_one_and_update(
            {"_id": ObjectId(budget_id), "user_id": ObjectId(user_id)},
            {"$set": budget.model_dump(by_alias=True)},
        )
        return {"message": "Budget updated successfully"}

    @staticmethod
    async def delete_budget(budget_id: str, user_id: str):
        await db.budgets.find_one_and_delete(
            {"_id": ObjectId(budget_id), "user_id": ObjectId(user_id)}
        )
        return {"message": "Budget deleted successfully"}
