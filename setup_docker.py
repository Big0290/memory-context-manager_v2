#!/usr/bin/env python3
"""
Docker Setup Script for Memory-Enhanced MCP Server with LLM
"""

import subprocess
import sys
import time
import requests
from pathlib import Path

def run_command(cmd, description):
    """Run a shell command with error handling"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed")
            return True
        else:
            print(f"❌ {description} failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} error: {str(e)}")
        return False

def check_docker():
    """Check if Docker is installed and running"""
    print("🐳 Checking Docker...")
    
    # Check if docker is installed
    docker_installed = run_command("docker --version", "Checking Docker installation")
    if not docker_installed:
        print("❌ Docker is not installed. Please install Docker Desktop first.")
        return False
    
    # Check if docker is running
    docker_running = run_command("docker ps", "Checking Docker daemon")
    if not docker_running:
        print("❌ Docker daemon is not running. Please start Docker Desktop.")
        return False
    
    return True

def check_dependencies():
    """Check if required Python packages are available"""
    print("📦 Checking dependencies...")
    
    required_files = [
        "pyproject.toml",
        "docker-compose.yml", 
        "Dockerfile",
        "main.py",
        "llm_client.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files present")
    return True

def build_and_start():
    """Build and start the Docker services"""
    print("\n🚀 Building and starting services...")
    
    # Stop any existing containers
    run_command("docker-compose down", "Stopping existing containers")
    
    # Build and start services
    build_success = run_command("docker-compose build", "Building containers")
    if not build_success:
        return False
    
    start_success = run_command("docker-compose up -d", "Starting services")
    if not start_success:
        return False
    
    return True

def wait_for_services():
    """Wait for services to be ready"""
    print("\n⏳ Waiting for services to be ready...")
    
    # Wait for Ollama service
    print("🤖 Waiting for Ollama service...")
    max_attempts = 30
    
    for attempt in range(max_attempts):
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                print("✅ Ollama service is ready")
                break
        except:
            pass
        
        if attempt == max_attempts - 1:
            print("❌ Ollama service failed to start")
            return False
        
        time.sleep(10)
        print(f"   Attempt {attempt + 1}/{max_attempts}...")
    
    return True

def setup_models():
    """Setup LLM models"""
    print("\n📥 Setting up LLM models...")
    
    # The model setup service should handle this automatically
    print("🤖 Models will be downloaded automatically by the model_setup service")
    print("   This may take 10-20 minutes depending on your internet connection...")
    
    # Wait for model setup to complete
    for i in range(60):  # Wait up to 60 minutes
        try:
            result = subprocess.run(
                "docker-compose ps model_setup", 
                shell=True, capture_output=True, text=True
            )
            
            if "exited (0)" in result.stdout:
                print("✅ Models downloaded successfully")
                return True
            elif "exited (" in result.stdout:
                print("❌ Model download failed")
                return False
                
        except:
            pass
        
        time.sleep(60)  # Wait 1 minute between checks
        print(f"   Still downloading models... ({i+1}/60 minutes)")
    
    print("⚠️  Model download taking longer than expected")
    return True  # Continue anyway

def test_installation():
    """Test the installation"""
    print("\n🧪 Testing installation...")
    
    # Test if services are responding
    services_to_test = [
        ("Ollama", "http://localhost:11434/api/tags"),
        ("Web UI", "http://localhost:3000"),
    ]
    
    for service_name, url in services_to_test:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code in [200, 404]:  # 404 is ok for some services
                print(f"✅ {service_name} is responding")
            else:
                print(f"⚠️  {service_name} responded with status {response.status_code}")
        except Exception as e:
            print(f"❌ {service_name} is not responding: {str(e)}")

def show_usage_info():
    """Show usage information"""
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETE!")
    print("="*60)
    print()
    print("📋 Your services are running:")
    print("   🤖 Ollama LLM:        http://localhost:11434")
    print("   🌐 Web UI:            http://localhost:3000")
    print("   🧠 MCP Server:        Container 'memory_mcp_server'")
    print()
    print("🔧 Useful commands:")
    print("   View logs:            docker-compose logs -f")
    print("   Stop services:        docker-compose down") 
    print("   Restart services:     docker-compose up -d")
    print("   Shell into MCP:       docker-compose exec memory_mcp_server bash")
    print()
    print("🧠 Test your memory system:")
    print("   1. Connect to your MCP server")
    print("   2. Run: test_memory_system")
    print("   3. Run: ai_chat_with_memory --user_message 'Hi, I'm Johny!'")
    print("   4. Run: ai_chat_with_memory --user_message 'What's my name?'")
    print()
    print("🌐 Access Web UI at: http://localhost:3000")
    print("   - Chat directly with the LLM")
    print("   - Test different models")
    print("   - Monitor performance")
    print()
    print("🔍 Check service status: docker-compose ps")

def main():
    """Main setup function"""
    print("🧠 Memory-Enhanced MCP Server Docker Setup")
    print("="*50)
    
    # Check prerequisites
    if not check_docker():
        sys.exit(1)
    
    if not check_dependencies():
        sys.exit(1)
    
    # Build and start
    if not build_and_start():
        print("❌ Failed to build and start services")
        sys.exit(1)
    
    # Wait for services
    if not wait_for_services():
        print("❌ Services failed to start properly")
        sys.exit(1)
    
    # Setup models
    setup_models()
    
    # Test installation
    test_installation()
    
    # Show usage info
    show_usage_info()
    
    print("\n🎯 Next steps:")
    print("1. Your memory-enhanced AI is ready!")
    print("2. Connect to your MCP server and test the memory features")
    print("3. Use ai_chat_with_memory to chat with memory-enhanced AI")
    print("4. Visit http://localhost:3000 for direct LLM interaction")

if __name__ == "__main__":
    main()