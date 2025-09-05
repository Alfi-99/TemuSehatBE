#!/bin/bash
# start.sh

# Load environment variables
export $(cat .env | xargs)

# Jalankan ADK API Server
adk api_server --host 0.0.0.0 --port $PORT
