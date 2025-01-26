from bson import ObjectId
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer

from budget_service.schemas import BudgetSchema
from common.get_current_user import get_current_user

from .services import BudgetService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

budget_router = APIRouter()


@budget_router.get("/budgets", tags=["Budgets"])
async def get_budgets(user_id: str = Depends(get_current_user("userId"))):
    try:
        budgets = await BudgetService.get_budgets(user_id)
        return {"budgets": budgets}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@budget_router.post("/budget/create", tags=["Budgets"])
async def create_budget(
    budget: BudgetSchema,
    user_id: str = Depends(get_current_user("userId"))
    ):
    try:
        budget.user_id = ObjectId(user_id)
        await BudgetService.create_budget(budget)
        return {"message": "Budget created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@budget_router.get("/budgets/{budget_id}", tags=["Budgets"])
async def get_budget_by_id(
    budget_id: str, 
    user_id: str = Depends(get_current_user("userId"))
    ):
    try:
        budget = await BudgetService.get_budget_by_id(budget_id, user_id)
        return {"budget": budget}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@budget_router.put("/budget/update/{budget_id}", tags=["Budgets"])
async def update_budget(
    budget_id: str,
    budget: BudgetSchema,
    user_id: str = Depends(get_current_user("userId"))
):
    try:
        await BudgetService.update_budget(budget_id, budget, user_id)
        return {"message": "Budget updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@budget_router.delete("/budget/delete/{budget_id}", tags=["Budgets"])
async def delete_budget(
    budget_id: str,
    user_id: str = Depends(get_current_user("userId"))
    ):
    try:
        await BudgetService.delete_budget(budget_id, user_id)
        return {"message": "Budget deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
