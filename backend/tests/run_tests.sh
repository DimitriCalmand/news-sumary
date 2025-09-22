#!/bin/bash
# Test runner script for News Summary Backend
# Usage: ./run_tests.sh [options]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$(dirname "$SCRIPT_DIR")"
PROJECT_ROOT="$(dirname "$BACKEND_DIR")"

echo -e "${BLUE}🚀 News Summary Backend Test Runner${NC}"
echo -e "${BLUE}=====================================${NC}"

# Check if we're in the right directory
if [ ! -f "$BACKEND_DIR/requirements.txt" ]; then
    echo -e "${RED}❌ Error: requirements.txt not found in $BACKEND_DIR${NC}"
    echo -e "${YELLOW}Please run this script from the backend/tests directory${NC}"
    exit 1
fi

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo -e "${YELLOW}⚠️  pytest not found. Installing test dependencies...${NC}"

    # Install test dependencies
    if command -v pip &> /dev/null; then
        pip install -r "$SCRIPT_DIR/requirements-test.txt"
    elif command -v pip3 &> /dev/null; then
        pip3 install -r "$SCRIPT_DIR/requirements-test.txt"
    else
        echo -e "${RED}❌ Error: pip not found. Please install pip first.${NC}"
        exit 1
    fi
fi

# Change to backend directory for proper imports
cd "$BACKEND_DIR"

echo -e "${GREEN}✅ Running unit and API tests from $BACKEND_DIR${NC}"
echo -e "${YELLOW}📊 Test Results:${NC}"
echo

# Run the tests with coverage (excluding integration tests by default)
if [ "$1" = "--coverage" ] || [ "$1" = "-c" ]; then
    echo -e "${BLUE}📈 Running tests with coverage...${NC}"
    python3 -m pytest tests/ -v --tb=short --cov=src --cov-report=term-missing -m "not integration"
else
    # Run tests normally (excluding integration tests)
    python3 -m pytest tests/ -v --tb=short -m "not integration" "$@"
fi

TEST_EXIT_CODE=$?

echo
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ All unit and API tests passed!${NC}"
    echo
    echo -e "${BLUE}💡 To run integration tests:${NC}"
    echo -e "  1. Start the backend server: cd backend && python3 main.py"
    echo -e "  2. Run: SKIP_INTEGRATION_TESTS=false ./run_all_tests.sh --integration"
else
    echo -e "${RED}❌ Some tests failed. Exit code: $TEST_EXIT_CODE${NC}"
fi

exit $TEST_EXIT_CODE