#!/bin/bash
# Stock News Analyzer - Complete Package Creation Script

echo "Creating complete package for Stock News Analyzer..."

# Create package directory
PACKAGE_NAME="stock-news-analyzer-$(date +%Y%m%d)"
mkdir -p "$PACKAGE_NAME"

# Copy all application files
cp -r backend/ "$PACKAGE_NAME/"
cp -r frontend/ "$PACKAGE_NAME/"
cp *.py "$PACKAGE_NAME/"
cp *.md "$PACKAGE_NAME/"
cp *.txt "$PACKAGE_NAME/"
cp *.html "$PACKAGE_NAME/"
cp *.yml "$PACKAGE_NAME/"
cp Dockerfile "$PACKAGE_NAME/"
cp *.sh "$PACKAGE_NAME/"

# Create package-specific files
cat > "$PACKAGE_NAME/README.md" << 'EOF'
# Stock News Analyzer - Complete Package

## Overview
AI-powered stock news analysis with trading signals. Includes both demo mode and production mode with real web scraping and Ollama integration.

## Quick Start

### Option 1: Docker (Recommended)
```bash
docker-compose up --build
```
Access: http://localhost:8080/demo.html

### Option 2: Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run demo mode
python run_production.py --mode demo
```

### Option 3: Production with Ollama
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh
ollama serve &
ollama pull mistral

# Run production mode
python run_production.py --mode production
```

## Features
- Real-time stock news analysis
- Buy/sell/hold signals with confidence scores
- Web dashboard with auto-refresh
- RESTful API endpoints
- Docker deployment ready

## Access Points
- Web Interface: http://localhost:8080/demo.html
- API Endpoint: http://localhost:8000/signals
- Health Check: http://localhost:8000/health

## Architecture
- Backend: FastAPI + Python with web scraping
- Frontend: React + TypeScript with Tailwind CSS
- AI: Ollama + Mistral model integration
- Deployment: Docker with health checks
EOF

# Create simplified Docker Compose
cat > "$PACKAGE_NAME/docker-compose.yml" << 'EOF'
version: '3.8'

services:
  stock-analyzer:
    build: .
    ports:
      - "8000:8000"
      - "8080:8080"
    environment:
      - PYTHONUNBUFFERED=1
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
EOF

# Create optimized Dockerfile
cat > "$PACKAGE_NAME/Dockerfile" << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories
RUN mkdir -p logs

# Expose ports
EXPOSE 8000 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["python", "run_production.py", "--mode", "demo"]
EOF

# Create startup script
cat > "$PACKAGE_NAME/start.sh" << 'EOF'
#!/bin/bash
echo "Starting Stock News Analyzer..."

# Check if Docker is available
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    echo "Using Docker deployment..."
    docker-compose up --build
else
    echo "Using manual deployment..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        echo "Error: Python 3 is required"
        exit 1
    fi
    
    # Install dependencies
    pip install -r requirements.txt
    
    # Run application
    python3 run_production.py --mode demo
fi
EOF

chmod +x "$PACKAGE_NAME/start.sh"

# Create .gitignore
cat > "$PACKAGE_NAME/.gitignore" << 'EOF'
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.env
.venv
node_modules/
dist/
build/
logs/
*.log
.DS_Store
.vscode/
.idea/
EOF

# Create package info
cat > "$PACKAGE_NAME/PACKAGE_INFO.txt" << EOF
Stock News Analyzer - Complete Package
Generated: $(date)
Version: 1.0.0

Contents:
- Complete source code (backend + frontend)
- Docker deployment configuration
- Manual setup instructions
- All dependencies and requirements
- Documentation and guides

Quick Start:
1. Extract this package
2. Run: ./start.sh
3. Access: http://localhost:8080/demo.html

For more details, see README.md
EOF

# Create archive
tar -czf "${PACKAGE_NAME}.tar.gz" "$PACKAGE_NAME"
zip -r "${PACKAGE_NAME}.zip" "$PACKAGE_NAME"

echo "Package created successfully:"
echo "  - Directory: $PACKAGE_NAME/"
echo "  - Archive: ${PACKAGE_NAME}.tar.gz"
echo "  - Zip file: ${PACKAGE_NAME}.zip"
echo ""
echo "Distribution options:"
echo "  1. Send the .tar.gz or .zip file"
echo "  2. Share the entire directory"
echo "  3. Push to Git repository"
echo "  4. Deploy with Docker"