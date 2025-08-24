from database import posts_collection 
from fastapi import APIRouter, HTTPException, Depends
from lib.auth import get_current_user
from datetime import datetime
from typing import List
from pydantic import BaseModel
from bson import ObjectId
from fastapi.responses import JSONResponse
post_router = APIRouter()

@post_router.post("/", summary="Create a new post")
async def create_post(post: dict, current_user: dict = Depends(get_current_user)):
    post_doc = {
        "title": post["title"],
        "content": post["content"],
        "author_id": str(current_user["_id"]),  # store user id
        "created_at": datetime.utcnow()
    }
    result = await posts_collection.insert_one(post_doc)
    return {"post_id": str(result.inserted_id) , "status" : True , "message" : "Post created successfully" , "data" : post_doc}

@post_router.get("/", summary="Get all posts")
async def get_posts():
    pipeline = [
        {"$sort": {"created_at": -1}},

    # Join with users
        {
        "$lookup": {
            "from": "users",
            "localField": "author_id",
            "foreignField": "_id",
            "as": "author"
            }
        },
        {"$unwind": "$author"},

        # Join with comments
        {
        "$lookup": {
            "from": "comments",
            "localField": "_id",
            "foreignField": "post_id",
            "as": "comments"
            }
        },
        # if you don’t want empty comments removed, don’t unwind
        # {"$unwind": "$comments"},

        # Join with likes
        {
        "$lookup": {
            "from": "likes",
            "localField": "_id",
            "foreignField": "post_id",
            "as": "likes"
        }
        },

    # Add like_count field
        {
        "$addFields": {
            "like_count": {"$size": "$likes"}
        }
        },

        # Optional: remove raw likes array if you only need count
        {
        "$project": {
            "likes": 0,
            "author.password": 0   # avoid leaking password
        }
        }
    ]
    cursor = posts_collection.aggregate(pipeline)
    posts = []
    async for post in cursor:
        post["_id"] = str(post["_id"])
        post["author"]["_id"] = str(post["author"]["_id"])
        posts.append(post)

    if not posts:
        return  JSONResponse(status_code=404, content={
            "message" : "No posts found yet",
            "status" : False
            })

    return JSONResponse(status_code=200, content={
        "data": posts,
        "status": True,
        "message": "Posts fetched successfully"
    })


@post_router.get("/{author_id}", summary="Get a post by ID")
async def get_author_post(author_id: str):  
    pipeline = [
        {"$match": {"author_id": author_id}},
        {"$sort": {"created_at": -1}},

    # Join with users
        {
        "$lookup": {
            "from": "users",
            "localField": "author_id",
            "foreignField": "_id",
            "as": "author"
            }
        },
        {"$unwind": "$author"},

        # Join with comments
        {
        "$lookup": {
            "from": "comments",
            "localField": "_id",
            "foreignField": "post_id",
            "as": "comments"
            }
        },
        # if you don’t want empty comments removed, don’t unwind
        # {"$unwind": "$comments"},

        # Join with likes
        {
        "$lookup": {
            "from": "likes",
            "localField": "_id",
            "foreignField": "post_id",
            "as": "likes"
        }
        },

    # Add like_count field
        {
        "$addFields": {
            "like_count": {"$size": "$likes"}
        }
        },

        # Optional: remove raw likes array if you only need count
        {
        "$project": {
            "likes": 0,
            "author.password": 0   # avoid leaking password
        }
        }
    ]
    cursor = posts_collection.aggregate(pipeline)
    posts = []
    async for post in cursor:
        post["_id"] = str(post["_id"])
        post["author"]["_id"] = str(post["author"]["_id"])
        posts.append(post)

    if not posts:
        return  JSONResponse(status_code=404, content={
            "message" : "No posts found for this author",
            "status" : False
            })

    return JSONResponse(status_code=200, content={
        "data": posts,
        "status": True,
        "message": "Posts fetched successfully"
    })