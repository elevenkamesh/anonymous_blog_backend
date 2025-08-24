from fastapi import FastAPI , Depends , APIRouter
from app.database import users_collection
from bson import ObjectId
from app.lib.auth import get_current_user , create_access_token
from pydantic import BaseModel
from typing import List
from app.lib.utils import hash_password , verify_password
from datetime import datetime
user_router = APIRouter()

@user_router.post("/register", summary="Create a new user")
async def create_user(user: dict):
    user_doc = {
        "username": user["username"],
        "email": user["email"],
        "password": hash_password(user["password"]),  # In production, hash the password!
        "created_at": datetime.utcnow()
    }
    isExist = await users_collection.find_one({"username": user["username"]})
    if isExist:
        return {"status" : False , "message" : "User already exists"}
    
    result = await users_collection.insert_one(user_doc)
    return {"user_id": str(result.inserted_id) , "status" : True , "message" : "User created successfully"}

@user_router.post("/login", summary="User login")
async def login(user: dict):
    user_in_db = await users_collection.find_one({"username": user["username"]})
    if not user_in_db:
        return {"status" : False , "message" : "Invalid username or password"}
    
    if not verify_password(user["password"], user_in_db["password"]):
        return {"status" : False , "message" : "Invalid username or password"}
    
    token = create_access_token(data={"user_id": str(user_in_db["_id"])})
    return {"access_token": token , "token_type": "bearer" , "status" : True , "message" : "Login successful"}