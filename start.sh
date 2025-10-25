#!/bin/bash

# SenpaiAI Startup Script
echo "🎌 Starting SenpaiAI - Japanese Learning Assistant..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if Ollama is running (optional)
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✅ Ollama is running - using free local LLM"
else
    echo "⚠️  Ollama not detected - will use OpenAI API (requires API key)"
fi

# Check if .env files exist
if [ ! -f "backend/.env" ]; then
    echo "⚠️  Backend .env file not found. Creating from template..."
    cp backend/env.example backend/.env
    echo "📝 Please edit backend/.env and configure your LLM provider"
fi

if [ ! -f "frontend/.env" ]; then
    echo "⚠️  Frontend .env file not found. Creating from template..."
    cp frontend/env.example frontend/.env
fi

# Start services
echo "🚀 Starting all services with Docker Compose..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 15

# Check if services are running
echo "🔍 Checking service status..."
docker-compose ps

echo ""
echo "✅ SenpaiAI is starting up!"
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo "🤖 Ollama API: http://localhost:11434"
echo ""
echo "💡 To view logs: docker-compose logs -f"
echo "🛑 To stop: docker-compose down"
echo ""
echo "🎌 Happy learning Japanese with SenpaiAI!"
