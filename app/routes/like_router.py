from fastapi import APIRouter
from database import likes_collection
router = APIRouter()

@router.post("/{id}", summary="Like a post")
async def like_post(id: str, current_user: dict = Depends(get_current_user)):
    isExist = await likes_collection.find_one({"post_id": id, "user_id": str(current_user["_id"])})
    if isExist:
        result = await likes_collection.delete_one({"_id": isExist["_id"]})
        { "message": "unliked", "like_id": str(isExist["_id"]) }
        
    like_doc = {
        "post_id": id,
        "user_id": str(current_user["_id"]),  # store user id
        "created_at": datetime.utcnow()
    }
    result = await likes_collection.insert_one(like_doc)
    return {"message": "Post liked", "like_id": str(result.inserted_id)}