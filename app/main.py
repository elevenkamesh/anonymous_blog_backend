from fastapi import FastAPI
from app.routes.like_router import like_router
from app.routes.comment_router import comment_router
from app.routes.post_router import post_router
from app.routes.user_router import user_router

app = FastAPI(title="Anonymous Blog Media API", version="1.0.0")
@app.get("/")
async def root():
    return {"message": "Welcome to the Social Media API"}
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(post_router, prefix="/posts", tags=["Posts"])
app.include_router(comment_router, prefix="/comments", tags=["Comments"])
app.include_router(like_router, prefix="/likes", tags=["Likes"])    