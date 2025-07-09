#!/bin/bash
# Install MongoDB client (mongosh) if not present
if ! command -v mongosh &> /dev/null; then
    sudo apt update
    sudo apt install -y gnupg
    curl -fsSL https://www.mongodb.org/static/pgp/server-8.0.asc | sudo gpg --dearmor -o /usr/share/keyrings/mongodb-server-8.0.gpg
    echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-8.0.gpg ] https://repo.mongodb.org/apt/ubuntu noble/mongodb-org/8.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-8.0.list
    sudo apt update
    sudo apt install -y mongodb-org-shell mongodb-org-tools
fi
# Start MongoDB container if not running
if ! docker ps | grep -q mongodb; then
    docker rm -f mongodb || true
    docker run -d --name mongodb -p 27017:27017 mongo:latest
fi
echo "MongoDB running at localhost:27017"