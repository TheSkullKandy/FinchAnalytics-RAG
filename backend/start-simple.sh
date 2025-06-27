#!/bin/bash

echo "🚀 Starting LLM Stock Analyst API (Simplified Version)..."

# Check if we're in the backend directory
if [ ! -f "main-simple.py" ]; then
    echo "❌ Error: main-simple.py not found. Please run this script from the backend directory."
    exit 1
fi

# Set environment variables
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
export PORT="${PORT:-8000}"

echo "📋 Environment:"
echo "   PYTHONPATH: $PYTHONPATH"
echo "   PORT: $PORT"
echo "   Python version: $(python --version)"

# Install dependencies if requirements-simple.txt exists
if [ -f "requirements-simple.txt" ]; then
    echo "📦 Installing dependencies..."
    pip install -r requirements-simple.txt
fi

# Start the application
echo "🌟 Starting FastAPI application..."
python main-simple.py 