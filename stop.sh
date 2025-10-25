#!/bin/bash

# SenpaiAI Stop Script
echo "🛑 Stopping SenpaiAI services..."

# Stop and remove containers
docker-compose down

# Optional: Remove volumes (uncomment if you want to reset data)
# echo "🗑️  Removing volumes..."
# docker-compose down -v

echo "✅ SenpaiAI services stopped!"
echo "💡 To start again: ./start.sh"

