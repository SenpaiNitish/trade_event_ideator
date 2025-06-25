# Docker Deployment Guide - Stock News Analyzer

## Quick Docker Setup

### 1. Build and Run with Docker Compose (Recommended)
```bash
# From the stock-analyzer directory
docker-compose up --build
```

This automatically:
- Builds the Docker image
- Starts all services
- Maps ports 8000 (API) and 8080 (Web UI)
- Sets up health checks
- Creates log volumes

### 2. Manual Docker Build
```bash
# Build the image
docker build -t stock-analyzer .

# Run the container
docker run -d \
  --name stock-analyzer \
  -p 8000:8000 \
  -p 8080:8080 \
  -v $(pwd)/logs:/app/logs \
  stock-analyzer
```

### 3. Docker Hub Distribution
```bash
# Tag for Docker Hub
docker tag stock-analyzer your-username/stock-analyzer:latest

# Push to Docker Hub
docker push your-username/stock-analyzer:latest

# Others can then run:
docker run -p 8000:8000 -p 8080:8080 your-username/stock-analyzer
```

## Production Docker Setup

### With Ollama Integration
```bash
# Create docker-compose.prod.yml
version: '3.8'
services:
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    restart: unless-stopped
    
  stock-analyzer:
    build: .
    ports:
      - "8000:8000"
      - "8080:8080"
    environment:
      - PYTHONUNBUFFERED=1
      - OLLAMA_URL=http://ollama:11434
    depends_on:
      - ollama
    restart: unless-stopped

volumes:
  ollama_data:

# Run production setup
docker-compose -f docker-compose.prod.yml up --build
```

## Docker Configuration Details

### Dockerfile Explanation
```dockerfile
FROM python:3.11-slim        # Lightweight Python base
WORKDIR /app                 # Set working directory
COPY requirements.txt .      # Copy dependencies first (caching)
RUN pip install ...         # Install Python packages
COPY . .                    # Copy application code
EXPOSE 8000 8080            # Expose API and web ports
HEALTHCHECK ...             # Container health monitoring
CMD ["python", "run_production.py", "--mode", "demo"]
```

### Environment Variables
```bash
# Set in docker-compose.yml or docker run
PYTHONUNBUFFERED=1          # Immediate stdout/stderr
OLLAMA_URL=http://localhost:11434  # Ollama API endpoint
MODE=demo                   # Application mode (demo/production)
```

### Volume Mapping
```yaml
volumes:
  - ./logs:/app/logs         # Persistent logs
  - ./data:/app/data         # Data persistence (if needed)
```

### Health Checks
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

## Sharing Docker Images

### Method 1: Docker Hub
```bash
# Build and tag
docker build -t your-username/stock-analyzer:v1.0 .

# Push to registry
docker push your-username/stock-analyzer:v1.0

# Share instructions:
# docker run -p 8000:8000 -p 8080:8080 your-username/stock-analyzer:v1.0
```

### Method 2: Save/Load Image
```bash
# Save image to file
docker save stock-analyzer > stock-analyzer.tar

# Load on another machine
docker load < stock-analyzer.tar
docker run -p 8000:8000 -p 8080:8080 stock-analyzer
```

### Method 3: Export Container
```bash
# Export running container
docker export container-name > stock-analyzer-export.tar

# Import and run
docker import stock-analyzer-export.tar stock-analyzer:imported
```

## Deployment Environments

### Development
```bash
docker-compose up --build
# Auto-restart on code changes
```

### Staging
```bash
docker-compose -f docker-compose.staging.yml up -d
# Background deployment with monitoring
```

### Production
```bash
docker-compose -f docker-compose.prod.yml up -d
# With Ollama, monitoring, and persistence
```

## Monitoring and Logs

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f stock-analyzer

# Container logs
docker logs -f container-name
```

### Health Monitoring
```bash
# Check container health
docker ps

# Inspect health status
docker inspect --format='{{.State.Health.Status}}' container-name
```

## Troubleshooting

### Common Issues
1. **Port conflicts**: Change ports in docker-compose.yml
2. **Permission issues**: Add user mapping in Docker
3. **Memory limits**: Increase Docker memory allocation
4. **Network issues**: Check Docker network configuration

### Debug Commands
```bash
# Enter container shell
docker exec -it container-name bash

# Check running processes
docker exec container-name ps aux

# View resource usage
docker stats container-name
```

The Docker setup provides a complete, portable deployment solution for the Stock News Analyzer.