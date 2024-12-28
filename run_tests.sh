#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Setting up test environment...${NC}"

# Function to run a command and check its exit status
run_test() {
    echo "🔄 Running $1..."
    if $2; then
        echo -e "${GREEN}✓ $1 passed${NC}"
        return 0
    else
        echo -e "${RED}✗ $1 failed${NC}"
        return 1
    fi
}

# Initialize error counter
errors=0

# Setup Python virtual environment
cd server
if [ ! -d "python-virtual-env" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv python-virtual-env
fi

# Activate virtual environment
source python-virtual-env/bin/activate

# Install Python dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies..."
    pip install -r requirements.txt --quiet
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to install Python dependencies${NC}"
        exit 1
    fi
else
    echo -e "${RED}Warning: requirements.txt not found${NC}"
fi

# Build and start Docker containers
cd ..
echo "Building and starting Docker containers..."
docker compose -f docker-compose.ci.yml up --build -d

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 10

# Run server tests
echo -e "\n=== Server Tests ==="
cd server
run_test "Server Tests" "python3 -m pytest -v" || ((errors++))
cd ..

# Run E2E tests if they exist
if [ -d "e2e" ]; then
    echo -e "\n=== E2E Tests ==="
    cd e2e
    if [ -f "package.json" ]; then
        # Install dependencies if needed
        if [ ! -d "node_modules" ]; then
            echo "Installing E2E test dependencies..."
            npm install
        fi
        run_test "E2E Tests" "npx playwright test" || ((errors++))
    else
        echo "E2E tests directory exists but no package.json found. Skipping..."
    fi
    cd ..
fi

# Clean up
echo -e "\n=== Cleanup ==="
echo "Stopping Docker containers..."
docker compose -f docker-compose.ci.yml down

# Deactivate Python virtual environment
deactivate

echo
if [ $errors -eq 0 ]; then
    echo -e "${GREEN}All tests passed! 🎉${NC}"
    exit 0
else
    echo -e "${RED}$errors test suite(s) failed${NC}"
    exit 1
fi
