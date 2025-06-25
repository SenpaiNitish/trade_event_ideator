# Stock News Analyzer - User Guide

## How to Use Your Application

### Step 1: Start the Application
```bash
cd stock-analyzer
python run_production.py --mode demo
```

### Step 2: Access the Web Interface
Open your browser and go to: **http://localhost:8080/demo.html**

### Step 3: Use the Dashboard
- Click "Refresh Signals" to generate new trading analysis
- View trading recommendations as colored cards:
  - Green = Buy signal
  - Red = Sell signal  
  - Gray = Hold signal
- Each card shows:
  - Company name
  - Signal type with confidence percentage
  - AI reasoning
  - Original headline

### Step 4: Filter and Analyze
- Use filter buttons to show only Buy, Sell, or Hold signals
- Look for high confidence signals (above 80%)
- Read the AI reasoning to understand why each signal was generated

### API Usage (For Developers)
```bash
# Get new trading signals
curl http://localhost:8000/signals

# Check system health
curl http://localhost:8000/health

# Get cached signals (faster)
curl http://localhost:8000/signals/cached
```

### Features Available
- Real-time signal generation
- Confidence scoring (50-100%)
- Event classification (earnings, contracts, operations)
- Sentiment analysis (positive, negative, neutral)
- Auto-refresh every 5 minutes
- Mobile-responsive design

### To Stop the Application
Press Ctrl+C in the terminal where it's running

### Troubleshooting
- If the dashboard doesn't load, ensure both services are running on ports 8000 and 8080
- If no signals appear, click "Refresh Signals" and wait a few seconds
- Check the terminal for any error messages

The application is ready for immediate use with realistic stock analysis and trading signals.