#!/usr/bin/env python3
"""
Production runner for Stock News Analyzer
Handles both demo mode and production mode with Ollama
"""

import subprocess
import time
import sys
import os
import requests
import argparse

def check_ollama():
    """Check if Ollama is running and has Mistral model"""
    try:
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            has_mistral = any('mistral' in model.get('name', '') for model in models)
            return True, has_mistral
        return False, False
    except:
        return False, False

def start_ollama():
    """Start Ollama service"""
    print("Starting Ollama service...")
    try:
        process = subprocess.Popen(['ollama', 'serve'], 
                                 stdout=subprocess.DEVNULL, 
                                 stderr=subprocess.DEVNULL)
        time.sleep(5)
        
        # Check if it started successfully
        running, has_model = check_ollama()
        if running:
            print("Ollama service started successfully!")
            if not has_model:
                print("Installing Mistral model...")
                subprocess.run(['ollama', 'pull', 'mistral'], check=True)
                print("Mistral model installed!")
            return process
        else:
            print("Failed to start Ollama service")
            return None
    except Exception as e:
        print(f"Error starting Ollama: {e}")
        return None

def start_backend(mode='demo'):
    """Start the backend server"""
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    
    if mode == 'production':
        script = 'production_main.py'
    else:
        script = 'demo_main.py'
    
    print(f"Starting backend in {mode} mode...")
    process = subprocess.Popen([sys.executable, script], cwd=backend_dir)
    
    # Wait for backend to start
    time.sleep(3)
    
    # Test backend
    try:
        response = requests.get('http://localhost:8000/', timeout=5)
        if response.status_code == 200:
            print(f"Backend started successfully in {mode} mode!")
            return process
        else:
            print(f"Backend responded with status: {response.status_code}")
            return None
    except:
        print("Failed to connect to backend")
        return None

def start_frontend():
    """Start the frontend demo server"""
    print("Starting demo web server...")
    process = subprocess.Popen([
        sys.executable, '-m', 'http.server', '8080'
    ], cwd=os.path.dirname(__file__))
    time.sleep(2)
    return process

def main():
    parser = argparse.ArgumentParser(description='Stock News Analyzer Runner')
    parser.add_argument('--mode', choices=['demo', 'production'], default='demo',
                       help='Run mode: demo (simulated) or production (with Ollama)')
    parser.add_argument('--no-ollama', action='store_true',
                       help='Skip Ollama setup (demo mode only)')
    
    args = parser.parse_args()
    
    processes = []
    
    try:
        if args.mode == 'production' and not args.no_ollama:
            # Check and start Ollama
            running, has_model = check_ollama()
            if not running:
                ollama_process = start_ollama()
                if ollama_process:
                    processes.append(ollama_process)
                else:
                    print("Failed to start Ollama. Falling back to demo mode.")
                    args.mode = 'demo'
        
        # Start backend
        backend_process = start_backend(args.mode)
        if backend_process:
            processes.append(backend_process)
        else:
            print("Failed to start backend")
            return 1
        
        # Start frontend
        frontend_process = start_frontend()
        if frontend_process:
            processes.append(frontend_process)
        
        print(f"\n{'='*60}")
        print(f"Stock News Analyzer is running in {args.mode.upper()} mode!")
        print(f"{'='*60}")
        print(f"Backend API: http://localhost:8000")
        print(f"Demo UI: http://localhost:8080/demo.html")
        print(f"Health Check: http://localhost:8000/health")
        
        if args.mode == 'production':
            print(f"Ollama API: http://localhost:11434")
            print(f"Using real web scraping and AI analysis")
        else:
            print(f"Using simulated data for demonstration")
        
        print(f"\nAPI Endpoints:")
        print(f"  GET /signals - Get trading signals")
        print(f"  GET /signals/cached - Get cached signals")
        print(f"  GET /health - Health check")
        print(f"\nPress Ctrl+C to stop all services")
        print(f"{'='*60}")
        
        # Keep running until interrupted
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nShutting down all services...")
        for process in processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except:
                process.kill()
        print("All services stopped.")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())