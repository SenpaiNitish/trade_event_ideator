# Stock News Analyzer - Complete Package

## Overview
AI-powered stock news analysis with trading signals. Includes both demo mode and production mode with real web scraping and Ollama integration.

## Quick Start

### Option 1: Docker (Recommended)
```bash
docker-compose up --build
```
Access: http://localhost:8080/demo.html

### Option 2: Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run demo mode
python run_production.py --mode demo
```

### Option 3: Production with Ollama
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh
ollama serve &
ollama pull mistral

# Run production mode
python run_production.py --mode production
```

## Features
- Real-time stock news analysis
- Buy/sell/hold signals with confidence scores
- Web dashboard with auto-refresh
- RESTful API endpoints
- Docker deployment ready

## Access Points
- Web Interface: http://localhost:8080/demo.html
- API Endpoint: http://localhost:8000/signals
- Health Check: http://localhost:8000/health

## Architecture
- Backend: FastAPI + Python with web scraping
- Frontend: React + TypeScript with Tailwind CSS
- AI: Ollama + Mistral model integration
- Deployment: Docker with health checks
