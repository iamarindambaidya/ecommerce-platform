#!/bin/bash
# Start MongoDB
if ! docker ps | grep -q mongodb; then
    docker rm -f mongodb || true
    docker run -d --name mongodb -p 27017:27017 mongo:latest
fi
# Test Product Service API
curl -X POST http://localhost:8000/products -H "Content-Type: application/json" -d '{"id":"1","name":"Laptop","price":999.99,"stock":10}'
curl http://localhost:8000/products