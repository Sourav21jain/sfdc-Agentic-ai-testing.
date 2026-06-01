#!/bin/bash

# Quick Test Script
# Tests individual components without running the full agent

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "========================================="
echo "Quick Component Testing"
echo "========================================="
echo ""

# Activate virtual environment
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Run ./run_agent.sh first."
    exit 1
fi

source venv/bin/activate

# Test 1: Mock Insights Service
echo "1️⃣  Testing Mock Insights Service..."
python -m src.insights_service
echo ""

# Test 2: SFDC Client Authentication
echo "2️⃣  Testing SFDC Client..."
if [ ! -f "config/.env" ]; then
    echo "⚠️  config/.env not found. Skipping SFDC tests."
else
    python -m src.sfdc_client
fi
echo ""

# Test 3: Comment Generator
echo "3️⃣  Testing Comment Generator..."
python -m src.comment_generator
echo ""

echo "========================================="
echo "✅ Quick tests completed!"
echo "========================================="
echo ""
echo "To run the full agent: ./run_agent.sh"
