#!/bin/bash

# 🧠 Memory Context Manager v2 - Easy Setup Script
# This script makes it super easy to get your brain-enhanced AI running!

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}🔧 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_header() {
    echo -e "${BLUE}"
    echo "🧠 Memory Context Manager v2 - Easy Setup"
    echo "=========================================="
    echo -e "${NC}"
}

# Check if Docker is installed and running
check_docker() {
    print_status "Checking Docker installation..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed!"
        echo "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop"
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        print_error "Docker is not running!"
        echo "Please start Docker Desktop and try again."
        exit 1
    fi
    
    print_success "Docker is ready!"
}

# Check if required files exist
check_files() {
    print_status "Checking required files..."
    
    required_files=(
        "docker-compose-shareable.yml"
        "Dockerfile.shareable"
        "main.py"
        "pyproject.toml"
    )
    
    for file in "${required_files[@]}"; do
        if [[ ! -f "$file" ]]; then
            print_error "Missing required file: $file"
            exit 1
        fi
    done
    
    print_success "All required files found!"
}

# Build and start services
start_services() {
    print_status "Building and starting services..."
    
    # Stop any existing containers
    docker-compose -f docker-compose-shareable.yml down 2>/dev/null || true
    
    # Build the containers
    print_status "Building containers (this may take a few minutes)..."
    docker-compose -f docker-compose-shareable.yml build
    
    # Start services
    print_status "Starting services..."
    docker-compose -f docker-compose-shareable.yml up -d
    
    print_success "Services started successfully!"
}

# Wait for services to be ready
wait_for_services() {
    print_status "Waiting for services to be ready..."
    
    # Wait for Ollama
    print_status "Waiting for Ollama service..."
    max_attempts=30
    for i in $(seq 1 $max_attempts); do
        if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
            print_success "Ollama service is ready!"
            break
        fi
        
        if [[ $i -eq $max_attempts ]]; then
            print_error "Ollama service failed to start"
            exit 1
        fi
        
        echo "   Attempt $i/$max_attempts... (waiting 10 seconds)"
        sleep 10
    done
    
    # Wait for model setup to complete
    print_status "Waiting for AI models to download..."
    echo "📥 This may take 10-20 minutes depending on your internet connection..."
    
    max_attempts=120  # Wait up to 2 hours
    for i in $(seq 1 $max_attempts); do
        if docker-compose -f docker-compose-shareable.yml ps model_setup | grep -q "exited (0)"; then
            print_success "AI models downloaded successfully!"
            break
        fi
        
        if docker-compose -f docker-compose-shareable.yml ps model_setup | grep -q "exited ("; then
            print_error "Model download failed"
            exit 1
        fi
        
        if [[ $i -eq $max_attempts ]]; then
            print_warning "Model download taking longer than expected, continuing anyway..."
            break
        fi
        
        echo "   Still downloading models... ($i/$max_attempts - waiting 1 minute)"
        sleep 60
    done
}

# Test the installation
test_installation() {
    print_status "Testing installation..."
    
    # Test Ollama
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        print_success "Ollama is responding"
    else
        print_error "Ollama is not responding"
    fi
    
    # Test Web UI
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        print_success "Web UI is accessible"
    else
        print_warning "Web UI is not accessible (this is optional)"
    fi
    
    # Test MCP server container
    if docker-compose -f docker-compose-shareable.yml ps memory_mcp_server | grep -q "Up"; then
        print_success "MCP server container is running"
    else
        print_error "MCP server container is not running"
    fi
}

# Show usage information
show_usage() {
    echo ""
    echo -e "${GREEN}🎉 SETUP COMPLETE! 🎉${NC}"
    echo ""
    echo "📋 Your services are running:"
    echo "   🤖 Ollama LLM:        http://localhost:11434"
    echo "   🌐 Web UI:            http://localhost:3000"
    echo "   🧠 MCP Server:        Container 'memory_mcp_server_shared'"
    echo ""
    echo "🔧 Useful commands:"
    echo "   View logs:            docker-compose -f docker-compose-shareable.yml logs -f"
    echo "   Stop services:        docker-compose -f docker-compose-shareable.yml down"
    echo "   Restart services:     docker-compose -f docker-compose-shareable.yml up -d"
    echo "   Shell into MCP:       docker-compose -f docker-compose-shareable.yml exec memory_mcp_server_shared bash"
    echo ""
    echo "🧠 Test your memory system:"
    echo "   1. Connect to your MCP server"
    echo "   2. Run: test_memory_system"
    echo "   3. Run: ai_chat_with_memory --user_message 'Hi, I'm testing the memory system!'"
    echo ""
    echo "🌐 Access Web UI at: http://localhost:3000"
    echo "   - Chat directly with the LLM"
    echo "   - Test different models"
    echo "   - Monitor performance"
    echo ""
    echo "🔍 Check service status: docker-compose -f docker-compose-shareable.yml ps"
    echo ""
    echo -e "${BLUE}🎯 Next steps:${NC}"
    echo "1. Your memory-enhanced AI is ready!"
    echo "2. Connect to your MCP server and test the memory features"
    echo "3. Use ai_chat_with_memory to chat with memory-enhanced AI"
    echo "4. Visit http://localhost:3000 for direct LLM interaction"
}

# Main function
main() {
    print_header
    
    check_docker
    check_files
    start_services
    wait_for_services
    test_installation
    show_usage
}

# Run main function
main "$@"
