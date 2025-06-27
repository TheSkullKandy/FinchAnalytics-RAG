#!/bin/bash
echo "=== Debug Start Script ==="
echo "Current directory: $(pwd)"
echo "Listing files:"
ls -la
echo "=== Backend directory ==="
cd backend
echo "Backend directory: $(pwd)"
echo "Listing backend files:"
ls -la
echo "=== Python path ==="
which python
echo "=== Installed packages ==="
pip list | grep -E "(fastapi|uvicorn|pandas|numpy)"
echo "=== Starting server ==="
python -m uvicorn main:app --host 0.0.0.0 --port $PORT 