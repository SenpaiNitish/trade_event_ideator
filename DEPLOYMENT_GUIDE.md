# Stock News Analyzer - Deployment Guide

## Complete Full-Stack Application

This application provides AI-powered stock news analysis with trading signals. It includes:

### Backend Features
- **FastAPI** REST API with async processing
- **Web scraping** from MoneyControl and Financial Express
- **AI analysis** via Ollama + Mistral model (production) or simulation (demo)
- **CORS support** for frontend integration
- **Health checks** and error handling
- **Confidence filtering** (minimum 50%)

### Frontend Features
- **React dashboard** with TypeScript
- **Real-time updates** every 5 minutes
- **Signal filtering** by buy/sell/hold
- **Confidence visualization** with progress bars
- **Responsive design** with Tailwind CSS
- **Error handling** and loading states

## Quick Start

### Demo Mode (Recommended)
```bash
cd stock-analyzer
python run_production.py --mode demo
```

**Access Points:**
- API: http://localhost:8000
- Demo UI: http://localhost:8080/demo.html
- Health Check: http://localhost:8000/health

### Production Mode (Real AI)
```bash
# Install Ollama first
curl -fsSL https://ollama.ai/install.sh | sh
ollama serve &
ollama pull mistral

# Run with real scraping + AI
python run_production.py --mode production
```

## API Endpoints

### Core Endpoints
- `GET /` - Service status and info
- `GET /health` - Comprehensive health check
- `GET /signals` - Generate new trading signals (scrapes + analyzes)
- `GET /signals/cached` - Return cached signals without processing

### Response Format
```json
{
  "signals": [
    {
      "stock": "Reliance",
      "event": "Earnings Report",
      "sentiment": "positive",
      "signal": "buy",
      "confidence": 85,
      "reason": "Strong quarterly results indicate growth",
      "headline": "Reliance reports 15% jump in profits...",
      "timestamp": "2025-06-25T15:04:30.123456"
    }
  ],
  "count": 10,
  "timestamp": "2025-06-25T15:04:30.123456",
  "mode": "demo"
}
```

## Architecture

### Tech Stack
- **Backend**: Python 3.11, FastAPI, aiohttp, BeautifulSoup
- **AI/LLM**: Ollama with Mistral model
- **Frontend**: React 18, TypeScript, Tailwind CSS, Axios
- **Deployment**: Docker, Docker Compose support

### Data Flow
1. **Scraping**: Fetch headlines from news sources
2. **Analysis**: Send to Ollama for AI processing
3. **Filtering**: Remove low-confidence signals (<50%)
4. **Storage**: Cache in memory for quick access
5. **Frontend**: Display with real-time updates

## Configuration

### Environment Variables
```bash
export OLLAMA_URL="http://localhost:11434/api/generate"
export MIN_CONFIDENCE=50
export MAX_SIGNALS=20
export SCRAPING_TIMEOUT=10
export API_TIMEOUT=30
```

### Production Settings
- **Rate limiting**: Respectful scraping with delays
- **Error handling**: Graceful fallbacks and retries
- **Logging**: Structured logging for monitoring
- **Health checks**: Docker-compatible health endpoints

## Monitoring

### Health Check Response
```json
{
  "status": "healthy",
  "timestamp": "2025-06-25T15:04:30.123456",
  "ollama": "connected",
  "cached_signals": 10
}
```

### Key Metrics
- Signal generation rate
- Confidence score distribution
- Scraping success rate
- API response times
- Ollama connectivity status

## Security Considerations

### Production Deployment
- **CORS**: Configure allowed origins
- **Rate limiting**: Implement request throttling
- **Input validation**: Sanitize scraped content
- **API keys**: Secure external service credentials
- **Network security**: Use HTTPS in production

### Data Privacy
- No personal data collection
- Public news sources only
- Temporary in-memory storage
- No user tracking or analytics

## Troubleshooting

### Common Issues

**Backend won't start:**
```bash
# Check Python dependencies
pip install -r requirements.txt

# Verify port availability
lsof -i :8000
```

**No signals generated:**
- Check internet connection for scraping
- Verify Ollama is running (production mode)
- Check logs for scraping errors

**Frontend errors:**
- Ensure backend is running on port 8000
- Check browser console for CORS issues
- Verify API endpoints are accessible

**Ollama issues (production mode):**
```bash
# Check Ollama status
curl http://localhost:11434/api/tags

# Restart Ollama
ollama serve

# Reinstall Mistral model
ollama pull mistral
```

## Performance Optimization

### Backend
- Async processing for concurrent scraping
- Connection pooling for HTTP requests
- Response caching to reduce load
- Timeout configuration for reliability

### Frontend
- Lazy loading for large signal lists
- Debounced API calls
- Error boundaries for stability
- Progressive loading states

## Future Enhancements

### Planned Features
- Database persistence (PostgreSQL)
- User authentication and portfolios
- Email/SMS notifications for high-confidence signals
- Historical signal tracking and backtesting
- Additional news sources and languages
- Advanced filtering and search capabilities

### Scaling Considerations
- Horizontal scaling with load balancers
- Redis for distributed caching
- Message queues for background processing
- CDN for static asset delivery
- Database clustering for high availability