from fastapi import FastAPI
from 
app = FastAPI(title="Social Media API", version="1.0.0")

app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(post_router, prefix="/posts", tags=["Posts"])
app.include_router(comment_router, prefix="/comments", tags=["Comments"])
app.include_router(like_router, prefix="/likes", tags=["Likes"])    