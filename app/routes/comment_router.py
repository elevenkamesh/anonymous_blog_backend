from fastapi import FastAPI , APIRouter , Depends
from database import comments_collection
from datetime import datetime
from bson import ObjectId
from lib.auth import get_current_user
from fastapi.responses import JSONResponse
comment_router = APIRouter()

@comment_router.post("/", summary="Add a comment to a post")
async def add_comment(comment: dict , current_user: dict = Depends(get_current_user)):
    comment_doc = {
        "post_id": comment["post_id"],
        "user_id": str(current_user["_id"]),  # store user id
        "content": comment["content"],
        "created_at": datetime.utcnow()
    }
    result = await comments_collection.insert_one(comment_doc)
    return JSONResponse(status_code=201 ,
            content={
                "comment_id": str(result.inserted_id) , 
                "status" : True ,
                "message" : "Comment added successfully"
                })