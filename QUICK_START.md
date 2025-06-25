# Quick Start Guide - Stock News Analyzer

## The Application is Currently Running!

### Access Methods

**1. Web Dashboard (Best for Users)**
Open: http://localhost:8080/demo.html
- Visual interface with trading signals
- Click "Refresh Signals" to see new analysis
- Filter by Buy/Sell/Hold signals
- Auto-refreshes every 5 minutes

**2. Direct API (For Developers)**
```bash
# Get trading signals
curl http://localhost:8000/signals

# Check system health  
curl http://localhost:8000/health
```

### What You'll See
- Company names (TCS, Reliance, HDFC Bank, etc.)
- Trading signals: Buy 🟢, Sell 🔴, Hold ⚪
- Confidence scores: 50-100%
- AI reasoning for each recommendation
- Stock headlines that triggered the analysis

### How It Works
1. System analyzes realistic stock headlines
2. AI determines sentiment and event type
3. Generates buy/sell/hold recommendations
4. Shows confidence scores and reasoning
5. Updates in real-time

### To Stop the Application
Press Ctrl+C in the terminal

### To Restart Later
```bash
cd stock-analyzer
python run_production.py --mode demo
```

The application is ready for immediate use - just open the web interface!