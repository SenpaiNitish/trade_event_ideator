# Stock News Analyzer - Complete Package

## Overview
AI-powered trade idea geneartor using ollama. A vibe coding project built with minimal hardcoding and smart modular components. This tool seamlessly switches between demo mode and production mode, delivering AI-backed market insights.

In production mode, it scrapes real-time news and event headlines from trusted sources like Moneycontrol and Zerodha Pulse. These updates are passed to an Ollama-powered AI model, which analyzes sentiment and relevance. The AI then provides concise trade ideas or alerts, directly viewable on a clean, responsive frontend.

Whether you’re a trader looking for AI-generated trade calls or a developer exploring real-world integrations with Ollama and scraping tools, this project delivers a sharp and scalable experience.
## Quick Start

### Option 1: Docker (Recommended)
```bash
# run this in your powershell
git clone https://github.com/SenpaiNitish/trade_ideator2.git 
cd trade_ideator2
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
