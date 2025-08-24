from pydantic iomport BaseModel
from datetime import datetime
from typing import Optional

class Post(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    title: str
    content: str
    image_url: Optional[str] = None
    user_id: str
    created_at:  datetime = Field(default_factory=datetime.utcnow)
    updated_at:  datetime = Field(default_factory=datetime.utcnow)
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

class User(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    username: str
    email: Optional[EmailStr] = None
    password: str
    created_at:  datetime = Field(default_factory=datetime.utcnow)
    updated_at:  datetime = Field(default_factory=datetime.utcnow)
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

class Comment(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    post_id: str
    user_id: str
    content: str
    created_at:  datetime = Field(default_factory=datetime.utcnow)
    updated_at:  datetime = Field(default_factory=datetime.utcnow)
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

class Like(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    post_id: str
    user_id: str
    created_at:  datetime = Field(default_factory=datetime.utcnow)
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

        