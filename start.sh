#!/bin/bash

echo "🚀 Starting AI Drive Assistant Backend on Render..."

uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
