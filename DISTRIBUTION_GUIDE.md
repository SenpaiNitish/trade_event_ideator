# Stock News Analyzer - Distribution Guide

## How to Download and Package the Complete Application

### Method 1: Download Everything (Recommended)

I've created a complete package for you. Run this to create a distributable version:

```bash
cd stock-analyzer
./package.sh
```

This creates:
- `stock-news-analyzer-YYYYMMDD.tar.gz` - Complete package archive
- `stock-news-analyzer-YYYYMMDD.zip` - Windows-friendly zip file
- `stock-news-analyzer-YYYYMMDD/` - Directory with all files

### Method 2: Manual File Collection

If you prefer to collect files manually:

**Essential Files:**
```
stock-analyzer/
├── backend/                # FastAPI backend code
├── frontend/              # React frontend code
├── run_production.py      # Main application runner
├── requirements.txt       # Python dependencies
├── docker-compose.yml     # Docker deployment
├── Dockerfile            # Container configuration
├── README.md             # Setup instructions
└── *.md files            # Documentation
```

## How to Share with Others

### Option 1: Send Package File
1. Create package: `./package.sh`
2. Send the `.tar.gz` or `.zip` file
3. Recipient extracts and runs: `./start.sh`

### Option 2: Git Repository
```bash
# Initialize git repository
git init
git add .
git commit -m "Stock News Analyzer - Complete Application"

# Push to GitHub/GitLab
git remote add origin <your-repository-url>
git push -u origin main
```

### Option 3: Docker Hub
```bash
# Build and push Docker image
docker build -t your-username/stock-analyzer .
docker push your-username/stock-analyzer

# Others can then run:
# docker run -p 8000:8000 -p 8080:8080 your-username/stock-analyzer
```

## Running the Application Locally

### Quick Start (Any Platform)
```bash
# Extract the package
tar -xzf stock-news-analyzer-*.tar.gz
cd stock-news-analyzer-*/

# Run with Docker (if available)
docker-compose up --build

# OR run manually
./start.sh
```

### Manual Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Run demo mode
python run_production.py --mode demo

# Access at: http://localhost:8080/demo.html
```

### Production Setup with Real AI
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh
ollama serve &
ollama pull mistral

# Run production mode
python run_production.py --mode production
```

## System Requirements

### Minimum Requirements
- Python 3.8+
- 2GB RAM
- 1GB disk space
- Internet connection (for web scraping in production mode)

### With Docker
- Docker 20.10+
- Docker Compose 2.0+
- 2GB RAM
- 1GB disk space

### For Production Mode
- All above requirements
- Ollama with Mistral model
- Additional 4GB RAM for AI processing

## Access Points

Once running, access:
- **Web Dashboard**: http://localhost:8080/demo.html
- **API Endpoint**: http://localhost:8000/signals
- **Health Check**: http://localhost:8000/health
- **API Documentation**: http://localhost:8000/docs

## File Structure for Distribution

```
stock-news-analyzer/
├── README.md              # Setup and usage instructions
├── start.sh              # One-click startup script
├── requirements.txt      # Python dependencies
├── docker-compose.yml    # Docker deployment
├── Dockerfile           # Container configuration
├── run_production.py    # Application runner
├── backend/             # FastAPI backend
│   ├── demo_main.py     # Demo mode server
│   ├── production_main.py # Production server
│   └── main.py          # Original backend
├── frontend/            # React frontend
│   ├── src/            # Source code
│   ├── package.json    # Node dependencies
│   └── build files     # Configuration
├── logs/               # Application logs
└── documentation/      # Guides and docs
```

The package is completely self-contained and ready for distribution.