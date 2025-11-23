#!/bin/bash

# Ollama Setup Script for SenpaiAI
echo "🎌 Setting up Ollama for SenpaiAI..."

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama is not installed. Please install Ollama first:"
    echo "   Visit: https://ollama.ai/download"
    exit 1
fi

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "🚀 Starting Ollama service..."
    ollama serve &
    sleep 5
fi

echo "📥 Pulling required models..."

# Pull Gemma 2B model (lightweight, good for Japanese)
echo "Pulling Gemma 2B model..."
ollama pull gemma:2b

# Pull Gemma 7B model (better quality, requires more resources)
echo "Pulling Gemma 7B model..."
ollama pull gemma:7b

# Pull embedding model
echo "Pulling embedding model..."
ollama pull nomic-embed-text

# Pull other useful models
echo "Pulling additional models..."
ollama pull llama2:7b
ollama pull mistral:7b

echo ""
echo "✅ Ollama setup completed!"
echo ""
echo "Available models:"
ollama list
echo ""
echo "💡 Recommended models for SenpaiAI:"
echo "   - gemma:2b (fast, lightweight)"
echo "   - gemma:7b (better quality)"
echo "   - nomic-embed-text (for embeddings)"
echo ""
echo "🎌 SenpaiAI is ready to use with Ollama!"










