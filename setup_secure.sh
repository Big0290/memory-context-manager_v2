#!/bin/bash

echo "🔒 Setting up secure environment variables..."
echo "============================================="

# Check if .env already exists
if [ -f ".env" ]; then
    echo "⚠️  .env file already exists!"
    echo "   Please edit it manually with your actual values."
    exit 1
fi

# Copy template
if [ -f "env.template" ]; then
    cp env.template .env
    echo "✅ Created .env from template"
else
    echo "❌ env.template not found!"
    exit 1
fi

echo ""
echo "🔑 IMPORTANT: Edit .env file with your actual values:"
echo "   1. Google Custom Search API Key"
echo "   2. Google Custom Search Engine ID"
echo "   3. WebUI Secret Key"
echo "   4. Optional: Bing Search API Key"
echo ""
echo "📝 Edit command:"
echo "   nano .env"
echo ""
echo "🚀 After editing, start the system with:"
echo "   docker-compose up -d"
echo ""
echo "🔒 Your system will now be secure!"
