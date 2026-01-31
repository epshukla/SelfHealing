#!/bin/bash
echo "Starting Backend..."
python main.py &
BACKEND_PID=$!

echo "Starting Frontend..."
cd ui/dashboard
npm run dev -- --port 5173 &
FRONTEND_PID=$!

echo "Systems running. Press Ctrl+C to stop."
wait $BACKEND_PID $FRONTEND_PID
