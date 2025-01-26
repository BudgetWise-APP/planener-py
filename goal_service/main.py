from bson import ObjectId
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer

from common.get_current_user import get_current_user
from goal_service.schemas import GoalSchema

from .services import GoalService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

goals_router = APIRouter()


@goals_router.get("/goals", tags=["Goals"])
async def get_goals(user_id: str = Depends(get_current_user("userId"))):
    try:
        goals = await GoalService.get_goals(user_id)
        return {"goals": goals}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@goals_router.post("/goals/create", tags=["Goals"])
async def create_goal(
    goal: GoalSchema, 
    user_id: str = Depends(get_current_user("userId"))
   ):
    try:
        goal.user_id = ObjectId(user_id)
        await GoalService.create_goal(goal)
        return {"message": "Goal created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@goals_router.get("/goals/{goal_id}", tags=["Goals"])
async def get_goal_by_id(
    goal_id: str, 
    user_id: str = Depends(get_current_user("userId"))
    ):
    try:
        goal = await GoalService.get_goal_by_id(goal_id, user_id)
        return {"goal": goal}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@goals_router.put("/goals/{goal_id}", tags=["Goals"])
async def update_goal(
    goal_id: str, 
    goal: GoalSchema, 
    user_id: str = Depends(get_current_user("userId"))
    ):
    try:
        await GoalService.update_goal(goal_id, goal, user_id)
        return {"message": "Goal updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@goals_router.delete("/goals/{goal_id}", tags=["Goals"])
async def delete_goal(goal_id: str, user_id: str = Depends(get_current_user("userId"))):
    try:
        await GoalService.delete_goal(goal_id, user_id)
        return {"message": "Goal deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@goals_router.get("/goals/favorite", tags=["Goals"])
async def get_favorite_goals(user_id: str = Depends(get_current_user("userId"))):
    try:
        goal = await GoalService.get_favorite_goals(user_id)
        return {"goal": goal}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))