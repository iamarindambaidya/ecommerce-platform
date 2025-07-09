from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import pymongo
import os
import requests

app = FastAPI()

# MongoDB connection
mongo_uri = os.getenv("DB_URI", "mongodb://localhost:27017/")
client = pymongo.MongoClient(mongo_uri)
db = client["order_db"]
collection = db["orders"]

# Service URLs (local testing)
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://localhost:8001/products")

class Order(BaseModel):
    id: str
    user_id: str
    product_id: str
    quantity: int
    total_price: Optional[float] = None  # Make total_price optional

@app.post("/orders/", response_model=Order)
async def create_order(order: Order):
    # Verify product exists
    product_response = requests.get(f"{PRODUCT_SERVICE_URL}/{order.product_id}")
    if product_response.status_code != 200:
        raise HTTPException(status_code=404, detail="Product not found")
    product = product_response.json()
    if product["stock"] < order.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    # Calculate total price
    order.total_price = product["price"] * order.quantity
    collection.insert_one(order.dict())
    return order

@app.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: str):
    order = collection.find_one({"id": order_id}, {"_id": 0})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order