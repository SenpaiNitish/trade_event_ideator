#!/bin/bash

echo "Setting up Ollama for Stock News Analyzer..."

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "Installing Ollama..."
    curl -fsSL https://ollama.ai/install.sh | sh
else
    echo "Ollama is already installed"
fi

# Start Ollama service
echo "Starting Ollama service..."
ollama serve &
OLLAMA_PID=$!

# Wait for service to start
sleep 5

# Pull Mistral model
echo "Pulling Mistral model..."
ollama pull mistral

echo "Setup complete!"
echo "Ollama is running on http://localhost:11434"
echo "PID: $OLLAMA_PID"

# Keep service running
wait $OLLAMA_PID