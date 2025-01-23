from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer
from common.mongo_client import db
from .schemas import BudgetSchema
from .services import get_userid_from_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

budget_router = APIRouter()


@budget_router.get("/budgets")
async def get_budgets(token: str = Depends(oauth2_scheme)):
    try:
        user_id = get_userid_from_jwt(token)
        budgets = db.budgets.find({"userId": user_id}).to_list(length=None)

        return budgets
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@budget_router.post("/budget/create")
async def create_budget(budget: BudgetSchema, token: str = Depends(oauth2_scheme)):
    try:
        user_id = get_userid_from_jwt(token)
        budget.userId = user_id
        db.budgets.insert_one(budget.model_dump(by_alias=True))
        return {"message": "Budget created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@budget_router.get("/budgets/{budget_id}")
async def get_budget_by_id(budget_id: str, token: str = Depends(oauth2_scheme)):
    try:
        user_id = get_userid_from_jwt(token)
        budget = db.budgets.find_one({"_id": budget_id, "userId": user_id})
        if budget is None:
            raise HTTPException(status_code=404, detail="Budget not found")
        return budget
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@budget_router.put("/budget/update/{budget_id}")
async def update_budget(
    budget_id: str, budget: BudgetSchema, token: str = Depends(oauth2_scheme)
):
    try:
        user_id = get_userid_from_jwt(token)
        db.budgets.find_one_and_update(
            {"_id": budget_id, "userId": user_id},
            {"$set": budget.model_dump(by_alias=True)},
        )
        return {"message": "Budget updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@budget_router.delete("/budget/delete/{budget_id}")
async def delete_budget(budget_id: str, token: str = Depends(oauth2_scheme)):
    try:
        user_id = get_userid_from_jwt(token)
        db.budgets.find_one_and_delete({"_id": budget_id, "userId": user_id})
        return {"message": "Budget deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
