from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import aiohttp
import json
import re
from typing import List, Dict, Any
from datetime import datetime
import logging
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Stock News Analyzer", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for signals
signals_storage: List[Dict[str, Any]] = []

class NewsProcessor:
    def __init__(self):
        self.ollama_url = "http://localhost:11434/api/generate"
        
    async def scrape_moneycontrol(self) -> List[str]:
        """Scrape headlines from MoneyControl"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            async with aiohttp.ClientSession(headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as session:
                url = "https://www.moneycontrol.com/news/business/stocks/"
                async with session.get(url) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        
                        headlines = []
                        selectors = [
                            'h2 a', 'h3 a', '.news_title a', '.title a',
                            'a[href*="/news/"]', '.headline a'
                        ]
                        
                        for selector in selectors:
                            elements = soup.select(selector)
                            for element in elements:
                                text = element.get_text(strip=True)
                                if (text and len(text) > 20 and 
                                    any(keyword in text.lower() for keyword in 
                                        ['stock', 'share', 'company', 'profit', 'revenue', 'quarter', 'earnings'])):
                                    headlines.append(text)
                                    if len(headlines) >= 15:
                                        break
                            if len(headlines) >= 15:
                                break
                        
                        logger.info(f"Scraped {len(headlines)} headlines from MoneyControl")
                        return list(set(headlines))[:10]
                    else:
                        logger.error(f"MoneyControl returned status: {response.status}")
                        return []
        except Exception as e:
            logger.error(f"Error scraping MoneyControl: {e}")
            return []
    
    async def scrape_financial_express(self) -> List[str]:
        """Scrape headlines from Financial Express as alternative"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            async with aiohttp.ClientSession(headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as session:
                url = "https://www.financialexpress.com/market/"
                async with session.get(url) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        
                        headlines = []
                        selectors = ['h2 a', 'h3 a', '.story-title a', '.title a']
                        
                        for selector in selectors:
                            elements = soup.select(selector)
                            for element in elements:
                                text = element.get_text(strip=True)
                                if text and len(text) > 20:
                                    headlines.append(text)
                                    if len(headlines) >= 10:
                                        break
                            if len(headlines) >= 10:
                                break
                        
                        logger.info(f"Scraped {len(headlines)} headlines from Financial Express")
                        return list(set(headlines))[:10]
                    return []
        except Exception as e:
            logger.error(f"Error scraping Financial Express: {e}")
            return []
    
    async def analyze_with_ollama(self, headline: str) -> Dict[str, Any]:
        """Send headline to Ollama for analysis"""
        prompt = f"""Given the following stock news headline, return a JSON object with:
{{
  "stock": "<company name>",
  "event": "<event type>",
  "sentiment": "positive/negative/neutral",
  "signal": "buy/sell/hold",
  "confidence": <score 0-100>,
  "reason": "<short explanation>"
}}
Return only JSON. Do not include commentary.
Headline: {headline}"""

        payload = {
            "model": "mistral",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,
                "top_p": 0.9
            }
        }
        
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
                async with session.post(self.ollama_url, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        response_text = result.get("response", "")
                        
                        # Extract JSON from response
                        try:
                            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                            if json_match:
                                analysis = json.loads(json_match.group())
                                
                                # Validate required fields
                                required_fields = ["stock", "event", "sentiment", "signal", "confidence", "reason"]
                                if all(field in analysis for field in required_fields):
                                    analysis["headline"] = headline
                                    analysis["timestamp"] = datetime.now().isoformat()
                                    analysis["source"] = "ollama"
                                    return analysis
                                else:
                                    logger.error(f"Missing required fields in analysis: {analysis}")
                                    return None
                            else:
                                logger.error(f"No JSON found in Ollama response: {response_text}")
                                return None
                        except json.JSONDecodeError as e:
                            logger.error(f"Failed to parse JSON from Ollama: {e}")
                            return None
                    else:
                        logger.error(f"Ollama request failed: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"Error calling Ollama: {e}")
            return None
    
    async def process_headlines(self) -> List[Dict[str, Any]]:
        """Process all headlines and return filtered signals"""
        # Try multiple sources
        mc_headlines = await self.scrape_moneycontrol()
        fe_headlines = await self.scrape_financial_express()
        
        all_headlines = mc_headlines + fe_headlines
        # Remove duplicates
        unique_headlines = list(set(all_headlines))
        
        logger.info(f"Processing {len(unique_headlines)} unique headlines")
        
        # Process headlines with Ollama
        tasks = [self.analyze_with_ollama(headline) for headline in unique_headlines[:15]]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter valid signals
        valid_signals = []
        for result in results:
            if isinstance(result, dict) and result.get("confidence", 0) >= 50:
                valid_signals.append(result)
            elif isinstance(result, Exception):
                logger.error(f"Analysis failed: {result}")
        
        logger.info(f"Generated {len(valid_signals)} valid signals from {len(unique_headlines)} headlines")
        return valid_signals

processor = NewsProcessor()

@app.get("/")
async def root():
    return {
        "message": "Stock News Analyzer API", 
        "status": "running",
        "endpoints": ["/signals", "/signals/cached", "/health"],
        "ollama_status": "checking..."
    }

@app.get("/health")
async def health_check():
    """Comprehensive health check"""
    try:
        # Check Ollama connectivity
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get("http://localhost:11434/api/tags", timeout=aiohttp.ClientTimeout(total=5)) as response:
                    ollama_status = "connected" if response.status == 200 else "disconnected"
            except:
                ollama_status = "disconnected"
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "ollama": ollama_status,
            "cached_signals": len(signals_storage)
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@app.get("/signals")
async def get_signals():
    """Trigger scraping and return trade signals"""
    try:
        signals = await processor.process_headlines()
        
        # Update cache
        global signals_storage
        signals_storage = signals
        
        return {
            "signals": signals,
            "count": len(signals),
            "timestamp": datetime.now().isoformat(),
            "mode": "production"
        }
    except Exception as e:
        logger.error(f"Error processing signals: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/signals/cached")
async def get_cached_signals():
    """Return cached signals without new processing"""
    return {
        "signals": signals_storage,
        "count": len(signals_storage),
        "timestamp": datetime.now().isoformat(),
        "mode": "cached"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)