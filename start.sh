#!/bin/bash

echo "🟢 Setting PYTHONPATH..."
export PYTHONPATH="$PYTHONPATH:/opt/render/project/src/drive-ai-agent"

echo "🔧 Starting API server..."
uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
