from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import pymongo
import os

app = FastAPI()

# MongoDB connection
mongo_uri = os.getenv("DB_URI", "mongodb://localhost:27017/")
client = pymongo.MongoClient(mongo_uri)
db = client["product_db"]
collection = db["products"]

class Product(BaseModel):
    id: str
    name: str
    price: float
    stock: int

@app.post("/products/", response_model=Product)
async def create_product(product: Product):
    existing = collection.find_one({"id": product.id})
    if existing:
        raise HTTPException(status_code=400, detail="Product ID already exists")
    collection.insert_one(product.dict())
    return product

@app.get("/products/", response_model=List[Product])
async def get_products():
    products = list(collection.find({}, {"_id": 0}))
    return products

@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    product = collection.find_one({"id": product_id}, {"_id": 0})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product