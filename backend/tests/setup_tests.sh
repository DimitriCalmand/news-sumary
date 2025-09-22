#!/bin/bash
# Setup script for News Summary Backend tests
# This script sets up the test environment

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}🔧 Setting up News Summary Backend Test Environment${NC}"
echo -e "${BLUE}====================================================${NC}"

# Check if we're in the right directory
if [ ! -f "$BACKEND_DIR/requirements.txt" ]; then
    echo -e "${RED}❌ Error: Not in the correct directory${NC}"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$SCRIPT_DIR/venv" ]; then
    echo -e "${YELLOW}📦 Creating virtual environment...${NC}"
    python -m venv "$SCRIPT_DIR/venv"
fi

# Activate virtual environment
echo -e "${GREEN}✅ Activating virtual environment...${NC}"
source "$SCRIPT_DIR/venv/bin/activate" 2>/dev/null || source "$SCRIPT_DIR/venv/Scripts/activate" 2>/dev/null || {
    echo -e "${RED}❌ Failed to activate virtual environment${NC}"
    exit 1
}

# Install main dependencies
echo -e "${YELLOW}📥 Installing main dependencies...${NC}"
pip install -r "$BACKEND_DIR/requirements.txt"

# Install test dependencies
echo -e "${YELLOW}📥 Installing test dependencies...${NC}"
pip install -r "$SCRIPT_DIR/requirements-test.txt"

echo -e "${GREEN}✅ Setup complete!${NC}"
echo
echo -e "${BLUE}🚀 To run tests:${NC}"
echo -e "  cd $SCRIPT_DIR"
echo -e "  source venv/bin/activate  # On Windows: venv\\Scripts\\activate"
echo -e "  ./run_tests.sh"
echo
echo -e "${BLUE}📊 To run with coverage:${NC}"
echo -e "  ./run_tests.sh --coverage"