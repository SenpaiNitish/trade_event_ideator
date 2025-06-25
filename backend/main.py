from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import aiohttp
import json
import re
from typing import List, Dict, Any
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Stock News Analyzer", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
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
            async with aiohttp.ClientSession(headers=headers) as session:
                url = "https://www.moneycontrol.com/news/business/stocks/"
                async with session.get(url) as response:
                    if response.status == 200:
                        html = await response.text()
                        
                        # Use BeautifulSoup for better parsing
                        from bs4 import BeautifulSoup
                        soup = BeautifulSoup(html, 'html.parser')
                        
                        # Look for common headline patterns
                        headlines = []
                        
                        # Try multiple selectors for headlines
                        selectors = [
                            'h2 a',
                            'h3 a', 
                            '.news_title a',
                            '.title a',
                            'a[href*="/news/"]'
                        ]
                        
                        for selector in selectors:
                            elements = soup.select(selector)
                            for element in elements:
                                text = element.get_text(strip=True)
                                if text and len(text) > 20 and any(keyword in text.lower() for keyword in ['stock', 'share', 'company', 'profit', 'revenue', 'quarter']):
                                    headlines.append(text)
                                    if len(headlines) >= 10:
                                        break
                            if len(headlines) >= 10:
                                break
                        
                        return list(set(headlines))[:10]  # Remove duplicates and limit
                    else:
                        logger.error(f"Failed to fetch MoneyControl: {response.status}")
                        return []
        except Exception as e:
            logger.error(f"Error scraping MoneyControl: {e}")
            return []
    
    async def scrape_zerodha_pulse(self) -> List[str]:
        """Scrape headlines from Zerodha Pulse"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            async with aiohttp.ClientSession(headers=headers) as session:
                url = "https://pulse.zerodha.com/"
                async with session.get(url) as response:
                    if response.status == 200:
                        html = await response.text()
                        
                        from bs4 import BeautifulSoup
                        soup = BeautifulSoup(html, 'html.parser')
                        
                        headlines = []
                        
                        # Look for post titles and headlines
                        selectors = [
                            '.post-title',
                            '.title',
                            'h1', 'h2', 'h3',
                            'a[href*="/post/"]'
                        ]
                        
                        for selector in selectors:
                            elements = soup.select(selector)
                            for element in elements:
                                text = element.get_text(strip=True)
                                if text and len(text) > 15:
                                    headlines.append(text)
                                    if len(headlines) >= 10:
                                        break
                            if len(headlines) >= 10:
                                break
                        
                        return list(set(headlines))[:10]
                    else:
                        logger.error(f"Failed to fetch Zerodha Pulse: {response.status}")
                        return []
        except Exception as e:
            logger.error(f"Error scraping Zerodha Pulse: {e}")
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
            "stream": False
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.ollama_url, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        response_text = result.get("response", "")
                        
                        # Try to extract JSON from the response
                        try:
                            # Find JSON in the response
                            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                            if json_match:
                                analysis = json.loads(json_match.group())
                                analysis["headline"] = headline
                                analysis["timestamp"] = datetime.now().isoformat()
                                return analysis
                            else:
                                logger.error(f"No JSON found in Ollama response: {response_text}")
                                return None
                        except json.JSONDecodeError as e:
                            logger.error(f"Failed to parse JSON from Ollama: {e}")
                            logger.error(f"Raw response: {response_text}")
                            return None
                    else:
                        logger.error(f"Ollama request failed: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"Error calling Ollama: {e}")
            return None
    
    async def process_headlines(self) -> List[Dict[str, Any]]:
        """Process all headlines and return filtered signals"""
        # Scrape headlines from both sources
        mc_headlines = await self.scrape_moneycontrol()
        zp_headlines = await self.scrape_zerodha_pulse()
        
        all_headlines = mc_headlines + zp_headlines
        logger.info(f"Scraped {len(all_headlines)} headlines total")
        
        # Process each headline with Ollama
        tasks = [self.analyze_with_ollama(headline) for headline in all_headlines]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter and clean results
        valid_signals = []
        for result in results:
            if isinstance(result, dict) and result.get("confidence", 0) >= 50:
                valid_signals.append(result)
        
        logger.info(f"Generated {len(valid_signals)} valid signals")
        return valid_signals

processor = NewsProcessor()

@app.get("/")
async def root():
    return {"message": "Stock News Analyzer API", "status": "running"}

@app.get("/signals")
async def get_signals():
    """Trigger scraping and return trade signals"""
    try:
        signals = await processor.process_headlines()
        
        # Update in-memory storage
        global signals_storage
        signals_storage = signals
        
        return {
            "signals": signals,
            "count": len(signals),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error processing signals: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/signals/cached")
async def get_cached_signals():
    """Return cached signals without triggering new scraping"""
    return {
        "signals": signals_storage,
        "count": len(signals_storage),
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)