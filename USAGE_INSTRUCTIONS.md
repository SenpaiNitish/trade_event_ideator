# Stock News Analyzer - Ready to Use

## Access Your Application

**Web Dashboard:** http://localhost:8080/demo.html
**API Endpoint:** http://localhost:8000/signals

## How to Use

### Web Interface
1. Open http://localhost:8080/demo.html in your browser
2. Click "Refresh Signals" to generate new trading analysis
3. View recommendations as colored cards:
   - Green cards = Buy signals
   - Red cards = Sell signals
   - Gray cards = Hold signals
4. Each card shows company name, confidence percentage, and AI reasoning
5. Use filter buttons to show specific signal types
6. Dashboard auto-refreshes every 5 minutes

### API Usage
```bash
# Get new trading signals
curl http://localhost:8000/signals

# Check system status
curl http://localhost:8000/health
```

### Sample Output
The system generates analysis like:
- TCS: BUY (85%) - Strong business developments suggest future revenue growth
- HDFC Bank: HOLD (62%) - Regulatory concerns may impact future operations
- Reliance: BUY (78%) - Market expansion strategies showing results

### Features Available
- Real-time AI analysis of stock headlines
- Confidence scoring (50-100%)
- Buy/Sell/Hold recommendations with reasoning
- Event classification and sentiment analysis
- Mobile-responsive dashboard

The application is operational and ready for immediate use.