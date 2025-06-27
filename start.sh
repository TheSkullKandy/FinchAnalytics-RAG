#!/bin/bash

# LLM Stock Analyst Startup Script

echo "🚀 Starting LLM Stock Analyst..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please copy .env.example to .env and configure your API keys."
    exit 1
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Function to cleanup background processes
cleanup() {
    echo "🛑 Shutting down services..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start backend
echo "🔧 Starting FastAPI backend..."
cd backend
python -m uvicorn main:app --host $BACKEND_HOST --port $BACKEND_PORT --reload &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Start frontend
echo "🎨 Starting Streamlit frontend..."
cd frontend
streamlit run app.py --server.port $FRONTEND_PORT --server.headless true &
FRONTEND_PID=$!
cd ..

echo "✅ Services started successfully!"
echo "📊 Frontend: http://localhost:$FRONTEND_PORT"
echo "📚 API Docs: http://localhost:$BACKEND_PORT/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for background processes
wait 