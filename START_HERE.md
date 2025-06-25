# How to Use Your Stock News Analyzer

## The Application is Currently Running

### Quick Access
**Open this URL in your browser:** http://localhost:8080/demo.html

### What You'll See
- Trading signal cards showing Buy/Sell/Hold recommendations
- Company names like TCS, Reliance, HDFC Bank
- Confidence scores from 50-100%
- AI reasoning for each recommendation
- Color coding: Green (Buy), Red (Sell), Gray (Hold)

### How to Use
1. Click "Refresh Signals" to generate new analysis
2. Use filter buttons to show only Buy, Sell, or Hold signals
3. Look for high confidence signals (above 80%)
4. Read the AI reasoning to understand each recommendation

### API Testing (Optional)
```bash
# Get trading signals
curl http://localhost:8000/signals

# Check system health
curl http://localhost:8000/health
```

### To Restart Later
```bash
cd stock-analyzer
python run_production.py --mode demo
```

### Features Available
- Real-time signal generation with AI analysis
- Confidence scoring and sentiment analysis
- Event classification (earnings, contracts, operations)
- Auto-refresh every 5 minutes
- Mobile-responsive design

The application generates realistic trading recommendations based on stock news analysis.