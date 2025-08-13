#!/bin/bash
# Script to restart Docker Compose with search engine integration

echo "🐳 Restarting Docker Compose with Search Engine Integration"
echo "=========================================================="

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Pull latest images (optional)
echo "📥 Pulling latest images..."
docker-compose pull

# Start containers with new configuration
echo "🚀 Starting containers with search engine configuration..."
docker-compose up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be healthy..."
sleep 30

# Check container status
echo "📊 Container Status:"
docker-compose ps

# Check logs for search engine initialization
echo "📋 Checking search engine initialization logs..."
docker-compose logs memory_mcp_server | grep -E "(Google|Bing|Search|API)" | tail -10

echo ""
echo "✅ Docker Compose restarted with search engine integration!"
echo ""
echo "🔍 To test the integration:"
echo "   1. Check container logs: docker-compose logs memory_mcp_server"
echo "   2. Run the test script: python test_docker_search_integration.py"
echo "   3. Monitor API usage in Google Cloud Console"
echo ""
echo "🚀 Your AI system should now be able to search the web!"
