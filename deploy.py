#!/usr/bin/env python3
"""
Production deployment script for Stock News Analyzer
Handles both demo and production modes with proper error handling
"""

import subprocess
import sys
import os
import json
import time
import requests
from pathlib import Path

def check_system_requirements():
    """Check if system has required dependencies"""
    print("Checking system requirements...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("Error: Python 3.8+ required")
        return False
    
    # Check if pip packages are installed
    try:
        import fastapi, uvicorn, aiohttp, requests
        from bs4 import BeautifulSoup
        print("✓ All Python dependencies available")
    except ImportError as e:
        print(f"✗ Missing Python package: {e}")
        return False
    
    return True

def setup_environment():
    """Set up the environment for production"""
    print("Setting up environment...")
    
    # Create logs directory
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Create data directory for future database storage
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    print("✓ Environment setup complete")

def test_backend_api():
    """Test the backend API endpoints"""
    print("Testing backend API...")
    
    base_url = "http://localhost:8000"
    
    try:
        # Test health endpoint
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print(f"✓ Backend healthy - {health_data.get('status', 'unknown')}")
        else:
            print(f"✗ Health check failed: {response.status_code}")
            return False
        
        # Test signals endpoint (this will take longer)
        print("Testing signals generation...")
        response = requests.get(f"{base_url}/signals", timeout=60)
        if response.status_code == 200:
            signals_data = response.json()
            count = signals_data.get('count', 0)
            mode = signals_data.get('mode', 'unknown')
            print(f"✓ Generated {count} signals in {mode} mode")
            
            # Show sample signals
            for i, signal in enumerate(signals_data.get('signals', [])[:3]):
                print(f"  {i+1}. {signal['stock']}: {signal['signal']} ({signal['confidence']}%)")
            
            return True
        else:
            print(f"✗ Signals endpoint failed: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"✗ API test failed: {e}")
        return False

def create_production_config():
    """Create production configuration"""
    config = {
        "app": {
            "name": "Stock News Analyzer",
            "version": "1.0.0",
            "mode": "production"
        },
        "api": {
            "host": "0.0.0.0",
            "port": 8000,
            "timeout": 60
        },
        "scraping": {
            "sources": [
                "https://www.moneycontrol.com/news/business/stocks/",
                "https://www.financialexpress.com/market/"
            ],
            "max_headlines": 15,
            "timeout": 10
        },
        "ollama": {
            "url": "http://localhost:11434/api/generate",
            "model": "mistral",
            "timeout": 30
        },
        "filtering": {
            "min_confidence": 50,
            "max_signals": 20
        }
    }
    
    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("✓ Production configuration created")

def main():
    """Main deployment function"""
    print("=" * 60)
    print("Stock News Analyzer - Production Deployment")
    print("=" * 60)
    
    # Check requirements
    if not check_system_requirements():
        sys.exit(1)
    
    # Setup environment
    setup_environment()
    
    # Create production config
    create_production_config()
    
    # Start the application
    print("\nStarting Stock News Analyzer...")
    
    try:
        # Use the existing runner
        subprocess.run([sys.executable, "run_production.py", "--mode", "demo"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to start application: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nShutdown requested by user")
        sys.exit(0)

if __name__ == "__main__":
    main()