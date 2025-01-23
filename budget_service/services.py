from fastapi import HTTPException
from common.config import JWT_SECRET, ALGORITHM
from jose import jwt, JWTError


def get_userid_from_jwt(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        userId: str = payload.get("userId")
        if userId is None:
            raise HTTPException(status_code=401, detail="UserID not found in token")
        return userId
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
