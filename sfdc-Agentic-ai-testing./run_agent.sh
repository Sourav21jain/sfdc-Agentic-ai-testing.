#!/bin/bash

# SFDC OpenShift Insights Agent Launcher
# Usage: ./run_agent.sh

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "========================================="
echo "SFDC OpenShift Insights Agent"
echo "========================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Check for .env file
if [ ! -f "config/.env" ]; then
    echo "⚠️  Warning: config/.env not found"
    echo "Please copy config/.env.example to config/.env and configure your credentials"
    exit 1
fi

# Create logs directory
mkdir -p logs

# Run the agent
echo "Starting agent..."
echo ""
python -m src.agent
