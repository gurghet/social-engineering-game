#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for required commands
if ! command_exists python; then
    echo -e "${RED}Error: Python is not installed${NC}"
    exit 1
fi

if ! command_exists npm; then
    echo -e "${RED}Error: npm is not installed${NC}"
    exit 1
fi

# Check for .env file
if [ ! -f .env ]; then
    echo -e "${RED}Error: .env file not found${NC}"
    echo "Please create a .env file with the following variables:"
    echo "OPENAI_API_KEY_JANET=your_api_key_here"
    echo "JANET_SEG_BOT_TOKEN=your_telegram_bot_token"
    echo "JANET_SEG_BOT_CHAT_ID=your_telegram_chat_id"
    exit 1
fi

# Function to run backend
run_backend() {
    echo -e "${BLUE}Starting backend server...${NC}"
    cd server
    pip install -r requirements.txt
    python server.py &
    cd ..
}

# Function to run frontend
run_frontend() {
    echo -e "${BLUE}Starting frontend development server...${NC}"
    cd frontend
    npm install
    npm run dev &
    cd ..
}

# Function to cleanup processes on exit
cleanup() {
    echo -e "${BLUE}Cleaning up processes...${NC}"
    pkill -f "python server.py"
    pkill -f "npm run dev"
    exit 0
}

# Set up cleanup trap
trap cleanup EXIT

# Main execution
echo -e "${GREEN}Starting Social Engineering Game in development mode...${NC}"

# Start backend
run_backend

# Wait a bit for backend to initialize
sleep 2

# Start frontend
run_frontend

# Print access information
echo -e "${GREEN}Services started:${NC}"
echo -e "Backend: ${BLUE}http://localhost:23925${NC}"
echo -e "Frontend: ${BLUE}http://localhost:5173${NC}"

# Keep script running and show logs
echo -e "${GREEN}Press Ctrl+C to stop all services${NC}"
wait
