#!/bin/bash
# Complete test runner for News Summary Backend
# Runs all test suites

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}🧪 News Summary Backend - Complete Test Suite${NC}"
echo -e "${BLUE}================================================${NC}"

# Check if we're in the right directory
if [ ! -f "$BACKEND_DIR/requirements.txt" ]; then
    echo -e "${RED}❌ Error: requirements.txt not found${NC}"
    exit 1
fi

cd "$BACKEND_DIR"

echo -e "${YELLOW}📋 Test Suites Available:${NC}"
echo -e "  1. Unit Tests (test_models.py) - Test individual components"
echo -e "  2. API Tests (test_api.py) - Test API endpoints with mocks"
echo -e "  3. Integration Tests (test_integration.py) - Test against real server"
echo -e "  4. All Tests - Run complete test suite"
echo

# Parse arguments
RUN_COVERAGE=false
RUN_INTEGRATION=false
TEST_TYPE="all"

while [[ $# -gt 0 ]]; do
    case $1 in
        --coverage|-c)
            RUN_COVERAGE=true
            shift
            ;;
        --integration|-i)
            RUN_INTEGRATION=true
            shift
            ;;
        --unit|-u)
            TEST_TYPE="unit"
            shift
            ;;
        --api|-a)
            TEST_TYPE="api"
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [options]"
            echo
            echo "Options:"
            echo "  -u, --unit         Run only unit tests"
            echo "  -a, --api          Run only API tests"
            echo "  -i, --integration  Run only integration tests"
            echo "  -c, --coverage     Run with coverage report"
            echo "  -h, --help         Show this help"
            echo
            echo "Examples:"
            echo "  $0                    # Run all tests"
            echo "  $0 --coverage        # Run all tests with coverage"
            echo "  $0 --unit            # Run only unit tests"
            echo "  $0 --api --coverage  # Run API tests with coverage"
            exit 0
            ;;
        *)
            echo -e "${RED}❌ Unknown option: $1${NC}"
            echo -e "${YELLOW}Use --help for usage information${NC}"
            exit 1
            ;;
    esac
done

# Check if pytest is available
if ! command -v pytest &> /dev/null; then
    echo -e "${RED}❌ pytest not found. Installing test dependencies...${NC}"
    pip install -r "$SCRIPT_DIR/requirements-test.txt" 2>/dev/null || {
        echo -e "${RED}❌ Failed to install test dependencies${NC}"
        exit 1
    }
fi

# Build pytest command
PYTEST_CMD="python3 -m pytest"

if [ "$RUN_COVERAGE" = true ]; then
    PYTEST_CMD="$PYTEST_CMD --cov=src --cov-report=term-missing --cov-report=html:htmlcov"
fi

PYTEST_CMD="$PYTEST_CMD -v --tb=short"

# Determine which tests to run
case $TEST_TYPE in
    "unit")
        echo -e "${GREEN}🏃 Running Unit Tests...${NC}"
        TEST_FILES="tests/test_models.py"
        ;;
    "api")
        echo -e "${GREEN}🏃 Running API Tests...${NC}"
        TEST_FILES="tests/test_api.py"
        ;;
    "integration")
        echo -e "${GREEN}🏃 Running Integration Tests...${NC}"
        TEST_FILES="tests/test_integration.py"
        PYTEST_CMD="$PYTEST_CMD -m integration"
        ;;
    "all")
        echo -e "${GREEN}🏃 Running All Tests...${NC}"
        TEST_FILES="tests/"
        if [ "$RUN_INTEGRATION" = true ]; then
            PYTEST_CMD="$PYTEST_CMD -m \"not slow\""
        fi
        ;;
esac

echo -e "${BLUE}Command: $PYTEST_CMD $TEST_FILES${NC}"
echo

# Run the tests
eval "$PYTEST_CMD $TEST_FILES"
TEST_EXIT_CODE=$?

echo
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ All tests passed!${NC}"

    if [ "$RUN_COVERAGE" = true ]; then
        echo -e "${BLUE}📊 Coverage report saved to: htmlcov/index.html${NC}"
    fi
else
    echo -e "${RED}❌ Some tests failed (exit code: $TEST_EXIT_CODE)${NC}"
fi

# Additional information for integration tests
if [ "$TEST_TYPE" = "integration" ] && [ $TEST_EXIT_CODE -ne 0 ]; then
    echo
    echo -e "${YELLOW}💡 Integration test tips:${NC}"
    echo -e "  - Make sure the backend server is running on http://localhost:5000"
    echo -e "  - Check that test data exists in the data directory"
    echo -e "  - Verify database connections if applicable"
fi

exit $TEST_EXIT_CODE