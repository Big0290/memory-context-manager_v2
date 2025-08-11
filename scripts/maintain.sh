#!/bin/bash

# Memory Context Manager v2 - Project Maintenance Script
# This script runs the Python maintenance script to keep the project organized

echo "🔧 Memory Context Manager v2 - Project Maintenance"
echo "=================================================="

# Check if Python 3 is available
if command -v python3 &> /dev/null; then
    echo "🐍 Using Python 3"
    python3 scripts/maintain_project.py
elif command -v python &> /dev/null; then
    echo "🐍 Using Python"
    python scripts/maintain_project.py
else
    echo "❌ Python not found. Please install Python 3.x"
    exit 1
fi

echo ""
echo "💡 Tip: Add this to your crontab for automatic weekly maintenance:"
echo "   0 9 * * 1 cd $(pwd) && ./scripts/maintain.sh"
