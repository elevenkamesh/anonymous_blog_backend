from fastapi import Depends, HTTPException , status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from app.database import users_collection
from bson import ObjectId
from datetime import datetime, timedelta
import jwt 

security = HTTPBearer()

SECRET_KEY = "your-secret-key"  # move to config

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user_id",
            )
        user = users_collection.find_one({"_id": ObjectId(user_id)})

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or invalid token",
            )
            
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ✅ Token creator
def create_access_token(data: dict, expires_delta: Optional[int] = 60):
    """
    expires_delta: expiry time in minutes (default 60 min)
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt