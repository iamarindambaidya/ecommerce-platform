from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pymongo
import os

app = FastAPI()

# MongoDB connection
mongo_uri = os.getenv("DB_URI", "mongodb://localhost:27017/")
client = pymongo.MongoClient(mongo_uri)
db = client["user_db"]
collection = db["users"]

class User(BaseModel):
    username: str
    password: str

@app.post("/register")
async def register_user(user: User):
    existing = collection.find_one({"username": user.username})
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    collection.insert_one({"username": user.username, "password": user.password})
    return {"message": "User registered"}