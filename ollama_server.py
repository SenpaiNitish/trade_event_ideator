#!/usr/bin/env python3
"""
Local Ollama API simulation for production testing
Mimics the real Ollama API with intelligent analysis
"""

from fastapi import FastAPI
import json
import re
import random
from datetime import datetime
from typing import Dict, Any

app = FastAPI(title="Ollama API Simulation", version="1.0.0")

class IntelligentAnalyzer:
    """Intelligent stock news analyzer that mimics Ollama/Mistral responses"""
    
    def __init__(self):
        self.stock_keywords = {
            'reliance': ['reliance', 'ril'],
            'tcs': ['tcs', 'tata consultancy'],
            'hdfc': ['hdfc', 'housing development'],
            'infosys': ['infosys', 'infy'],
            'adani': ['adani'],
            'itc': ['itc'],
            'bajaj': ['bajaj'],
            'wipro': ['wipro'],
            'maruti': ['maruti', 'suzuki'],
            'sbi': ['sbi', 'state bank'],
            'bharti': ['bharti', 'airtel'],
            'coal india': ['coal india', 'cil'],
            'tata motors': ['tata motors'],
            'ongc': ['ongc', 'oil and natural'],
            'asian paints': ['asian paints']
        }
        
        self.sentiment_indicators = {
            'positive': ['surge', 'jump', 'gain', 'profit', 'growth', 'revenue', 'expansion', 'strong', 'increase', 'rise', 'boost', 'success'],
            'negative': ['fall', 'drop', 'decline', 'loss', 'concern', 'scrutiny', 'issue', 'problem', 'decrease', 'tumble', 'pressure', 'shortage'],
            'neutral': ['announce', 'report', 'update', 'plan', 'expect', 'forecast', 'outlook', 'guidance']
        }
    
    def extract_company(self, headline: str) -> str:
        """Extract company name from headline"""
        headline_lower = headline.lower()
        for company, keywords in self.stock_keywords.items():
            if any(keyword in headline_lower for keyword in keywords):
                return company.title()
        
        # Extract potential company names (capitalized words)
        words = headline.split()
        for word in words:
            if word[0].isupper() and len(word) > 3:
                return word
        
        return "Unknown Company"
    
    def analyze_sentiment(self, headline: str) -> str:
        """Analyze sentiment based on keywords"""
        headline_lower = headline.lower()
        
        positive_score = sum(1 for word in self.sentiment_indicators['positive'] if word in headline_lower)
        negative_score = sum(1 for word in self.sentiment_indicators['negative'] if word in headline_lower)
        
        if positive_score > negative_score:
            return "positive"
        elif negative_score > positive_score:
            return "negative"
        else:
            return "neutral"
    
    def determine_event_type(self, headline: str) -> str:
        """Determine event type from headline"""
        headline_lower = headline.lower()
        
        if any(word in headline_lower for word in ['profit', 'revenue', 'earnings', 'quarter']):
            return "Earnings Report"
        elif any(word in headline_lower for word in ['deal', 'contract', 'agreement', 'partnership']):
            return "Business Contract"
        elif any(word in headline_lower for word in ['production', 'sales', 'volume', 'output']):
            return "Operational Update"
        elif any(word in headline_lower for word in ['regulation', 'government', 'policy']):
            return "Regulatory News"
        elif any(word in headline_lower for word in ['expansion', 'launch', 'new']):
            return "Business Expansion"
        else:
            return "Corporate News"
    
    def generate_signal(self, sentiment: str, headline: str) -> tuple:
        """Generate trading signal and confidence"""
        headline_lower = headline.lower()
        
        # Base confidence on sentiment strength
        if sentiment == "positive":
            # Look for strong positive indicators
            strong_positive = ['surge', 'jump', 'strong', 'record', 'best']
            if any(word in headline_lower for word in strong_positive):
                signal = "buy"
                confidence = random.randint(75, 95)
            else:
                signal = "buy" if random.random() > 0.3 else "hold"
                confidence = random.randint(60, 80)
        
        elif sentiment == "negative":
            # Look for strong negative indicators
            strong_negative = ['tumble', 'crash', 'concern', 'problem', 'scrutiny']
            if any(word in headline_lower for word in strong_negative):
                signal = "sell"
                confidence = random.randint(70, 90)
            else:
                signal = "sell" if random.random() > 0.4 else "hold"
                confidence = random.randint(55, 75)
        
        else:  # neutral
            signal = "hold"
            confidence = random.randint(50, 70)
        
        return signal, confidence
    
    def generate_reason(self, signal: str, sentiment: str, event: str) -> str:
        """Generate reasoning for the signal"""
        reasons = {
            "buy": {
                "positive": [
                    "Strong financial performance indicates growth potential",
                    "Positive business developments suggest future revenue growth", 
                    "Market expansion strategies showing promising results",
                    "Operational improvements support bullish outlook"
                ],
                "neutral": [
                    "Stable fundamentals with potential upside opportunities",
                    "Market position remains strong despite mixed signals"
                ]
            },
            "sell": {
                "negative": [
                    "Regulatory concerns may impact future operations",
                    "Operational challenges could affect profitability",
                    "Market headwinds pose significant risks",
                    "Financial metrics show concerning trends"
                ],
                "neutral": [
                    "Risk-reward ratio not favorable at current levels",
                    "Better opportunities available elsewhere"
                ]
            },
            "hold": {
                "positive": [
                    "Current valuation appears fair given positive developments",
                    "Wait for better entry point despite good news"
                ],
                "negative": [
                    "Impact assessment needed before making moves",
                    "Temporary setback, long-term outlook unclear"
                ],
                "neutral": [
                    "Mixed signals suggest wait-and-see approach",
                    "Need more data to confirm trend direction",
                    "Balanced risk-reward profile warrants holding"
                ]
            }
        }
        
        return random.choice(reasons[signal].get(sentiment, reasons[signal]["neutral"]))
    
    def analyze_headline(self, headline: str) -> Dict[str, Any]:
        """Complete analysis of a headline"""
        stock = self.extract_company(headline)
        sentiment = self.analyze_sentiment(headline)
        event = self.determine_event_type(headline)
        signal, confidence = self.generate_signal(sentiment, headline)
        reason = self.generate_reason(signal, sentiment, event)
        
        return {
            "stock": stock,
            "event": event,
            "sentiment": sentiment,
            "signal": signal,
            "confidence": confidence,
            "reason": reason
        }

analyzer = IntelligentAnalyzer()

@app.get("/api/tags")
async def get_models():
    """Simulate Ollama models endpoint"""
    return {
        "models": [
            {
                "name": "mistral:latest",
                "model": "mistral",
                "modified_at": "2024-01-01T00:00:00Z",
                "size": 4109395648
            }
        ]
    }

@app.post("/api/generate")
async def generate_response(request: dict):
    """Simulate Ollama generate endpoint with intelligent analysis"""
    
    model = request.get("model", "mistral")
    prompt = request.get("prompt", "")
    
    # Extract headline from prompt
    headline_match = re.search(r'Headline:\s*(.+?)(?:\n|$)', prompt)
    if not headline_match:
        return {"response": '{"error": "No headline found in prompt"}'}
    
    headline = headline_match.group(1).strip()
    
    try:
        # Perform intelligent analysis
        analysis = analyzer.analyze_headline(headline)
        
        # Format as JSON response
        response_json = json.dumps(analysis, indent=2)
        
        return {
            "model": model,
            "created_at": datetime.now().isoformat() + "Z",
            "response": response_json,
            "done": True
        }
        
    except Exception as e:
        return {
            "model": model,
            "created_at": datetime.now().isoformat() + "Z", 
            "response": f'{{"error": "Analysis failed: {str(e)}"}}',
            "done": True
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=11434)