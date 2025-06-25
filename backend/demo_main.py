from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import random
from typing import List, Dict, Any
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Stock News Analyzer Demo", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample headlines with realistic stock news
SAMPLE_HEADLINES = [
    "Reliance Industries reports 15% jump in quarterly profits driven by retail expansion",
    "TCS announces major cloud computing deal worth $2.5 billion with European client",
    "HDFC Bank faces regulatory scrutiny over digital lending practices",
    "Infosys stock surges after raising full-year revenue guidance",
    "Adani Group stocks tumble amid fresh concerns over debt levels",
    "ITC shares gain on strong cigarette volume growth in Q3",
    "Bajaj Finance reports higher bad loan provisions, stock falls",
    "Wipro wins multi-year IT services contract from Fortune 500 company",
    "Maruti Suzuki cuts production due to semiconductor shortage",
    "SBI reports record quarterly profits, announces dividend increase",
    "Bharti Airtel subscriber base grows, ARPU shows improvement",
    "Coal India production drops 8% in December, shares decline",
    "Tata Motors electric vehicle sales cross 50,000 units milestone",
    "ONGC discovers new oil reserves in Krishna Godavari basin",
    "Asian Paints faces margin pressure from raw material cost inflation"
]

# Sample analysis results
def generate_sample_signal(headline: str) -> Dict[str, Any]:
    """Generate realistic sample analysis for a headline"""
    
    # Extract company name from headline
    companies = ["Reliance", "TCS", "HDFC Bank", "Infosys", "Adani", "ITC", 
                "Bajaj Finance", "Wipro", "Maruti Suzuki", "SBI", "Bharti Airtel", 
                "Coal India", "Tata Motors", "ONGC", "Asian Paints"]
    
    stock = next((comp for comp in companies if comp.lower() in headline.lower()), "Unknown")
    
    # Generate realistic sentiment and signals based on headline keywords
    positive_keywords = ["jump", "surges", "gains", "growth", "profits", "wins", "discovers", "milestone"]
    negative_keywords = ["falls", "tumble", "drops", "decline", "shortage", "scrutiny", "concerns"]
    
    if any(word in headline.lower() for word in positive_keywords):
        sentiment = "positive"
        signal = "buy" if random.random() > 0.3 else "hold"
        confidence = random.randint(65, 90)
    elif any(word in headline.lower() for word in negative_keywords):
        sentiment = "negative" 
        signal = "sell" if random.random() > 0.4 else "hold"
        confidence = random.randint(55, 80)
    else:
        sentiment = "neutral"
        signal = "hold"
        confidence = random.randint(50, 70)
    
    # Generate event type
    if "profit" in headline.lower() or "revenue" in headline.lower():
        event = "Earnings Report"
    elif "deal" in headline.lower() or "contract" in headline.lower():
        event = "Business Contract"
    elif "production" in headline.lower() or "sales" in headline.lower():
        event = "Operational Update"
    else:
        event = "Corporate News"
    
    # Generate reason
    reasons = {
        "buy": [
            "Strong financial performance indicates growth potential",
            "Positive business development suggests future revenue growth",
            "Market expansion strategy showing results",
            "Strong operational metrics support bullish outlook"
        ],
        "sell": [
            "Regulatory concerns may impact future operations",
            "Operational challenges could affect profitability",
            "Market headwinds pose risks to performance",
            "Financial metrics show concerning trends"
        ],
        "hold": [
            "Mixed signals suggest wait-and-see approach",
            "Current valuation appears fair given fundamentals",
            "Need more data to confirm trend direction",
            "Balanced risk-reward profile warrants holding"
        ]
    }
    
    return {
        "stock": stock,
        "event": event,
        "sentiment": sentiment,
        "signal": signal,
        "confidence": confidence,
        "reason": random.choice(reasons[signal]),
        "headline": headline,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/")
async def root():
    return {"message": "Stock News Analyzer Demo API", "status": "running", "mode": "demo"}

@app.get("/signals")
async def get_signals():
    """Generate demo signals from sample headlines"""
    try:
        # Generate signals from sample headlines
        signals = []
        selected_headlines = random.sample(SAMPLE_HEADLINES, k=random.randint(8, 12))
        
        for headline in selected_headlines:
            signal = generate_sample_signal(headline)
            # Only include signals with confidence >= 50
            if signal["confidence"] >= 50:
                signals.append(signal)
        
        logger.info(f"Generated {len(signals)} demo signals")
        
        return {
            "signals": signals,
            "count": len(signals),
            "timestamp": datetime.now().isoformat(),
            "mode": "demo"
        }
    except Exception as e:
        logger.error(f"Error generating demo signals: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/signals/cached")
async def get_cached_signals():
    """Return empty cache for demo"""
    return {
        "signals": [],
        "count": 0,
        "timestamp": datetime.now().isoformat(),
        "mode": "demo"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)