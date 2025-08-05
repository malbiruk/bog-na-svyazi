#!/bin/bash

# Deployment script for bog-na-svyazi on home server

set -e

echo "🚀 Starting deployment of bog-na-svyazi..."

# Build and start the container
echo "📦 Building Docker image..."
docker-compose build

echo "🔄 Stopping old container (if exists)..."
docker-compose down

echo "▶️  Starting new container..."
docker-compose up -d

echo "✅ Deployment complete!"
echo "🌐 Application is running at http://localhost:8090"
echo ""
echo "📊 View logs: docker-compose logs -f"
echo "🛑 Stop: docker-compose down"