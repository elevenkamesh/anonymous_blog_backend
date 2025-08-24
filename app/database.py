from  motor.motor_asyncio import AsyncIOMotorClient

# MongoDB connection URI
db_url = "mongodb://localhost:27017"
client = AsyncIOMotorClient(db_url)

# Database name
database_name = "social_media_app"
db = client[database_name]

# Collections
users_collection = db["users"]
posts_collection = db["posts"]
comments_collection = db["comments"]
likes_collection = db["likes"]


