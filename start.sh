#!/bin/bash
echo "Starting Stock News Analyzer..."

# Check if Docker is available
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    echo "Using Docker deployment..."
    docker-compose up --build
else
    echo "Using manual deployment..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        echo "Error: Python 3 is required"
        exit 1
    fi
    
    # Install dependencies
    pip install -r requirements.txt
    
    # Run application
    python3 run_production.py --mode demo
fi
