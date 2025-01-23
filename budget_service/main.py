from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer

from budget_service.schemas import BudgetSchema

from .services import BudgetService, get_userid_from_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

budget_router = APIRouter()


@budget_router.get("/budgets")
async def get_budgets(token: str = Depends(oauth2_scheme)):
    try:
        user_id = get_userid_from_jwt(token)
        budgets = await BudgetService.get_budgets(user_id)
        return {"budgets": budgets}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@budget_router.post("/budget/create")
async def create_budget(budget: BudgetSchema, token: str = Depends(oauth2_scheme)):
    try:
        user_id = get_userid_from_jwt(token)
        budget.user_id = user_id
        await BudgetService.create_budget(budget)
        return {"message": "Budget created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@budget_router.get("/budgets/{budget_id}")
async def get_budget_by_id(budget_id: str, token: str = Depends(oauth2_scheme)):
    try:
        user_id = get_userid_from_jwt(token)
        budget = await BudgetService.get_budget_by_id(budget_id, user_id)
        return {"budget": budget}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@budget_router.put("/budget/update/{budget_id}")
async def update_budget(
    budget_id: str, budget: BudgetSchema, token: str = Depends(oauth2_scheme)
):
    try:
        user_id = get_userid_from_jwt(token)
        await BudgetService.update_budget(budget_id, budget, user_id)
        return {"message": "Budget updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@budget_router.delete("/budget/delete/{budget_id}")
async def delete_budget(budget_id: str, token: str = Depends(oauth2_scheme)):
    try:
        user_id = get_userid_from_jwt(token)
        await BudgetService.delete_budget(budget_id, user_id)
        return {"message": "Budget deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
