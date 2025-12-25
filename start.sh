#!/bin/bash
# Quick start script for Smart Trash AIOT

echo "================================"
echo "Smart Trash AIOT - Quick Start"
echo "================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Create necessary directories
echo "Creating directories..."
mkdir -p models logs data

# Run the system
echo ""
echo "Starting Smart Trash AIOT system..."
echo "Press Ctrl+C to stop"
echo ""
cd src
python main.py
