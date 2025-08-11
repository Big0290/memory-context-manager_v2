# 🧠 Memory Context Manager v2 - Easy Setup Guide

Welcome to the **Memory Context Manager v2** - a revolutionary AI system that gives AI persistent memory, emotional intelligence, and human-like learning capabilities! This guide will get you up and running in minutes.

## 🚀 What You're Getting

- **🧠 Brain-Inspired AI**: AI that thinks and learns like a human brain
- **💾 Persistent Memory**: Remembers conversations and learns from interactions
- **😊 Emotional Intelligence**: Understands context and importance
- **🔄 Self-Learning**: Continuously improves through experience
- **🔌 MCP Integration**: Seamlessly works with Cursor IDE and other MCP clients

## 📋 Prerequisites

- **Docker Desktop** installed and running
- **Git** for cloning the repository
- **Cursor IDE** (recommended) or any MCP client

## 🎯 Quick Start (3 Steps!)

### Step 1: Clone & Setup
```bash
# Clone the repository
git clone https://github.com/Big0290/memory-context-manager_v2.git
cd memory-context-manager_v2

# Make setup script executable (Mac/Linux)
chmod +x setup_shared.sh

# Run the setup script
./setup_shared.sh
```

**Windows Users**: Run `setup_shared.bat` instead!

### Step 2: Wait for Setup
The setup script will:
- ✅ Check Docker installation
- 🐳 Build and start all services
- 🤖 Download AI models (10-20 minutes)
- 🧪 Test everything works
- 🎉 Show you what's ready!

### Step 3: Connect to Cursor
1. Copy this configuration into your Cursor MCP settings:
```json
{
  "mcpServers": {
    "memory-context-manager-v2": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-v",
        "${workspaceFolder}:/workspace",
        "-w",
        "/workspace",
        "memory-context-manager-v2:latest"
      ],
      "env": {
        "PYTHONPATH": "/workspace",
        "MCP_LOG_LEVEL": "INFO",
        "OLLAMA_BASE_URL": "http://host.docker.internal:11434"
      }
    }
  }
}
```

2. Restart Cursor
3. Your brain-enhanced AI is ready! 🎉

## 🔧 Manual Setup (Alternative)

If you prefer manual setup or the script doesn't work:

### 1. Build the Docker Image
```bash
docker build -f Dockerfile.shareable -t memory-context-manager-v2:latest .
```

### 2. Start Services
```bash
docker-compose -f docker-compose-shareable.yml up -d
```

### 3. Wait for Models
```bash
# Check if models are ready
docker-compose -f docker-compose-shareable.yml ps model_setup

# View logs
docker-compose -f docker-compose-shareable.yml logs -f
```

## 🧠 Testing Your AI

Once everything is running, test your memory-enhanced AI:

### Test 1: Basic Memory
```
@memory-context-manager-v2 test_memory_system
```

### Test 2: Chat with Memory
```
@memory-context-manager-v2 ai_chat_with_memory --user_message "Hi! My name is Alice and I love coding in Python."
```

### Test 3: Test Memory Recall
```
@memory-context-manager-v2 ai_chat_with_memory --user_message "What's my name and what do I love?"
```

### Test 4: Brain Functions
```
@memory-context-manager-v2 brain_info
```

## 🌐 Web Interface

Access the web interface at **http://localhost:3000** to:
- Chat directly with the LLM
- Test different AI models
- Monitor system performance
- Debug any issues

## 🔍 Troubleshooting

### Common Issues

#### 1. "Cannot start server" Error
**Solution**: Make sure Docker is running and the image is built
```bash
docker ps
docker images | grep memory-context-manager-v2
```

#### 2. Models Not Downloading
**Solution**: Check the model setup service
```bash
docker-compose -f docker-compose-shareable.yml logs model_setup
```

#### 3. Port Conflicts
**Solution**: Check what's using the ports
```bash
# Check port 11434 (Ollama)
lsof -i :11434

# Check port 3000 (Web UI)
lsof -i :3000
```

#### 4. Permission Issues
**Solution**: Make sure setup script is executable
```bash
chmod +x setup_shared.sh
```

### Getting Help

1. **Check logs**: `docker-compose -f docker-compose-shareable.yml logs -f`
2. **Check status**: `docker-compose -f docker-compose-shareable.yml ps`
3. **Restart services**: `docker-compose -f docker-compose-shareable.yml restart`
4. **Full reset**: `docker-compose -f docker-compose-shareable.yml down && ./setup_shared.sh`

## 🎯 What You Can Do Now

### Available AI Functions
- **💭 Think**: Process information with memory context
- **🧠 Remember**: Store important information
- **🔍 Recall**: Search through memories
- **🤔 Reflect**: Learn from experiences
- **🧘 Consciousness Check**: Monitor AI state
- **📚 Learn From**: Process new experiences
- **💤 Dream**: Background memory consolidation

### Use Cases
- **Code Context Memory**: Remember project preferences and patterns
- **Learning Assistant**: AI that learns your coding style
- **Project History**: Maintain context across development sessions
- **Personal AI**: AI that remembers you and your preferences

## 🔧 Advanced Configuration

### Environment Variables
You can customize the AI behavior:

```bash
# In docker-compose-shareable.yml
environment:
  - OLLAMA_MODEL=phi3:mini          # AI model to use
  - DEBUG_MODE=false                 # Enable debug logging
  - MCP_LOG_LEVEL=INFO              # Logging level
  - MEMORY_STORAGE_DIR=/app/brain_memory_store
```

### Custom Models
Want to use different AI models? Edit the `model_setup` service:

```yaml
command: >
  sh -c "
    ollama pull llama3.1:8b &&
    ollama pull phi3:mini &&
    ollama pull codellama:7b
  "
```

## 📊 System Requirements

- **RAM**: Minimum 4GB, Recommended 8GB+
- **Storage**: 2GB+ for AI models
- **CPU**: Multi-core recommended
- **OS**: Windows 10+, macOS 10.15+, Linux (Ubuntu 18.04+)

## 🚀 Performance Tips

1. **Use SSD storage** for faster model loading
2. **Allocate more RAM** to Docker if available
3. **Close other applications** during initial model download
4. **Use wired internet** for faster model downloads

## 🔄 Updates & Maintenance

### Update the System
```bash
git pull origin main
docker-compose -f docker-compose-shareable.yml down
./setup_shared.sh
```

### Backup Your Memories
```bash
# Backup memory data
cp -r brain_memory_store/ my_memories_backup/
```

### Clean Up
```bash
# Remove old containers and images
docker system prune -a

# Remove volumes (WARNING: This deletes all memories!)
docker volume rm memory-context-manager_v2_brain_database_shared
```

## 🎉 Congratulations!

You now have a **brain-enhanced AI system** that:
- ✅ Remembers everything you tell it
- ✅ Learns from your interactions
- ✅ Understands context and importance
- ✅ Works seamlessly with Cursor IDE
- ✅ Runs reliably in Docker containers

## 🤝 Support & Community

- **Issues**: [GitHub Issues](https://github.com/Big0290/memory-context-manager_v2/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Big0290/memory-context-manager_v2/discussions)
- **Star the repo** if you find it useful! ⭐

---

**Built with 🧠 for intelligent AI assistance**

*This system represents a paradigm shift in AI capabilities - from stateless to stateful, from technical to human-like, from static to continuously learning.*
