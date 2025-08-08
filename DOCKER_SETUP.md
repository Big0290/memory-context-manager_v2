# 🧠🤖 Memory-Enhanced MCP Server with Local LLM

Complete Docker setup for deploying a local LLM (Ollama) integrated with your memory-enhanced MCP server.

## 🎯 What This Gives You

- **🤖 Local LLM**: Ollama running Llama 3.1 8B model
- **🧠 Memory System**: Persistent memory with emotional weighting
- **💬 Memory-Enhanced AI**: AI that remembers "Johny" and everything else
- **🌐 Web UI**: Direct chat interface with the LLM
- **🔧 MCP Tools**: All your existing tools + memory-enhanced chat

## 🚀 Quick Start

### 1. Prerequisites
```bash
# Install Docker Desktop
# Make sure Docker is running

# Verify Docker
docker --version
docker ps
```

### 2. One-Command Setup
```bash
python setup_docker.py
```

This will:
- ✅ Build all containers
- ✅ Download Llama 3.1 8B model (~4.7GB)
- ✅ Start all services
- ✅ Test everything

### 3. Manual Setup (Alternative)
```bash
# Build and start services
docker-compose up -d

# Wait for models to download (10-20 minutes)
docker-compose logs -f model_setup

# Check status
docker-compose ps
```

## 📦 What Gets Deployed

### Services
- **🤖 Ollama LLM**: `localhost:11434`
  - Llama 3.1 8B model
  - API endpoint for LLM requests
  - GPU support (if available)

- **🧠 MCP Server**: Container `memory_mcp_server`
  - Your memory-enhanced MCP server
  - Brain plugin system
  - Auto-memory integration
  - LLM integration

- **🌐 Web UI**: `localhost:3000`
  - Direct chat with LLM
  - Model management
  - Performance monitoring

### Storage
- **🗄️ Persistent Memory**: `./brain_memory_store/`
  - JSON-based brain storage
  - Survives container restarts
  - Shared with host

- **📦 Model Storage**: Docker volume
  - LLM models storage
  - Survives container restarts

## 🧪 Testing Your Setup

### 1. Test LLM Connection
```bash
# Connect to your MCP server, then run:
test_llm_connection
```

### 2. Test Memory System
```bash
test_memory_system
```

### 3. Test Memory-Enhanced Chat
```bash
# Introduce yourself
ai_chat_with_memory --user_message "Hi there! My name is Johny and I love AI projects"

# Ask if it remembers
ai_chat_with_memory --user_message "What's my name?"

# Test personalized response
ai_chat_with_memory --user_message "How are you doing today?"
```

### 4. Test Web UI
Visit `http://localhost:3000` and chat directly with the LLM.

## 🛠️ Management Commands

### Service Control
```bash
# View all services
docker-compose ps

# View logs
docker-compose logs -f
docker-compose logs -f memory_mcp_server
docker-compose logs -f ollama

# Restart services
docker-compose restart

# Stop services
docker-compose down

# Stop and remove everything
docker-compose down -v
```

### LLM Management
```bash
# List available models
list_available_models

# Shell into Ollama container
docker-compose exec ollama bash

# Pull new models manually
docker-compose exec ollama ollama pull llama3.1:70b
```

### MCP Server Management
```bash
# Shell into MCP server
docker-compose exec memory_mcp_server bash

# View memory files
ls -la brain_memory_store/

# Test memory directly
python -c "
import asyncio
from llm_client import test_llm_integration
asyncio.run(test_llm_integration())
"
```

## 🔧 Configuration

### Environment Variables
Edit `docker-compose.yml` to customize:

```yaml
environment:
  - OLLAMA_BASE_URL=http://ollama:11434
  - OLLAMA_MODEL=llama3.1:8b        # Change model
  - MEMORY_STORAGE_DIR=/app/brain_memory_store
  - DEBUG_MODE=false                # Enable debug mode
```

### Models
Available models (edit in `docker-compose.yml` model_setup service):
- `llama3.1:8b` (4.7GB) - Default, good balance
- `llama3.1:70b` (40GB) - Better quality, needs more RAM
- `phi3:mini` (2.3GB) - Faster, smaller
- `codellama:7b` (3.8GB) - Code-focused

### Resource Requirements
- **Minimum**: 8GB RAM, 10GB disk
- **Recommended**: 16GB RAM, 20GB disk  
- **GPU**: Optional but recommended (CUDA/Metal)

## 🎯 Usage Examples

### Memory-Enhanced Conversations
```bash
# Session 1
ai_chat_with_memory --user_message "Hi! I'm Johny, a software developer working on AI memory systems"

# Session 2 (later)
ai_chat_with_memory --user_message "How's my AI memory project going?"
# AI will remember you're Johny and your project!
```

### Direct LLM Chat (Web UI)
1. Go to `http://localhost:3000`
2. Chat directly with Llama 3.1
3. Test different prompts
4. Monitor performance

### MCP Integration
Your existing MCP tools now have access to:
- `ai_chat_with_memory` - Full memory-enhanced chat
- `quick_memory_chat` - Simple chat interface
- `auto_process_message` - Process messages automatically
- `get_user_context` - Get user information
- `brain_remember` - Store facts
- `brain_recall` - Search memories

## 🔍 Troubleshooting

### Common Issues

**Ollama won't start**
```bash
# Check Docker resources
docker system df
docker system prune

# Check logs
docker-compose logs ollama
```

**Models won't download**
```bash
# Check internet connection and disk space
docker-compose logs model_setup

# Manual download
docker-compose exec ollama ollama pull llama3.1:8b
```

**Memory not working**
```bash
# Check brain storage
ls -la brain_memory_store/

# Test memory system
test_memory_system

# Check MCP logs
docker-compose logs memory_mcp_server
```

**Out of memory**
```bash
# Use smaller model
# Edit docker-compose.yml: OLLAMA_MODEL=phi3:mini

# Restart with new model
docker-compose down
docker-compose up -d
```

### Performance Tuning

**GPU Support**
```yaml
# Uncomment in docker-compose.yml
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          count: all
          capabilities: [gpu]
```

**Model Selection**
- Fast responses: `phi3:mini`
- Balanced: `llama3.1:8b` 
- Best quality: `llama3.1:70b`

## 🎉 Success!

Your memory-enhanced AI system is now running with:
- ✅ Local LLM (no API keys needed)
- ✅ Persistent memory system
- ✅ Emotional weighting and learning
- ✅ Web interface for testing
- ✅ Complete MCP integration

**Test it now:**
1. `ai_chat_with_memory --user_message "Hi, I'm Johny"`
2. `ai_chat_with_memory --user_message "What's my name?"`
3. Watch it remember you perfectly! 🧠✨