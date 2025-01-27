from bson import ObjectId
from fastapi import HTTPException
from common.config import KAFKA_TOPIC_INTEGRATIONS
from common.kafka_producer import send_message
from common.mongo_client import db


class GoalService:
    @staticmethod
    async def get_goals(user_id: str):
        goals = await db.goals.find(
            {"user_id": ObjectId(user_id)}, {"user_id": 0}
        ).to_list(None)
        send_message(
            key="update_goals",
            value={"user_id": user_id},
            topic=KAFKA_TOPIC_INTEGRATIONS,
        )

        for goal in goals:
            goal["_id"] = str(goal["_id"])
        return goals

    @staticmethod
    async def create_goal(goal):
        is_platform_used = db.goals.find_one({"platform": goal.platform})
        if is_platform_used:
            raise HTTPException(
                status_code=400, detail="Goal with this platform already exists"
            )
        await db.goals.insert_one(goal.model_dump(by_alias=True))

    @staticmethod
    async def get_goal_by_id(goal_id: str, user_id: str):
        goal = await db.goals.find_one(
            {"_id": ObjectId(goal_id), "user_id": ObjectId(user_id)}, {"user_id": 0}
        )
        if goal is None:
            raise HTTPException(status_code=404, detail="Goal not found")

        send_message(
            key="update_goals",
            value={"user_id": user_id},
            topic=KAFKA_TOPIC_INTEGRATIONS,
        )
        goal["_id"] = str(goal["_id"])
        return goal

    @staticmethod
    async def update_goal(goal_id: str, goal, user_id: str):
        is_platform_used = db.goals.find_one({"platform": goal.platform})
        if is_platform_used:
            raise HTTPException(
                status_code=400, detail="Goal with this platform already exists"
            )
        await db.goals.find_one_and_update(
            {"_id": ObjectId(goal_id), "user_id": ObjectId(user_id)},
            {"$set": goal.model_dump(by_alias=True)},
        )
        return {"message": "Goal updated successfully"}

    @staticmethod
    async def delete_goal(goal_id: str, user_id: str):
        await db.goals.find_one_and_delete(
            {"_id": ObjectId(goal_id), "user_id": ObjectId(user_id)}
        )
        return {"message": "Goal deleted successfully"}

    @staticmethod
    async def get_favorite_goals(user_id: str):
        goals = await db.goals.find(
            {"user_id": ObjectId(user_id), "isFavorite": True}
        ).to_list(None)
        send_message(
            key="update_goals",
            value={"user_id": user_id},
            topic=KAFKA_TOPIC_INTEGRATIONS,
        )
        for goal in goals:
            goal["_id"] = str(goal["_id"])
        return goals
