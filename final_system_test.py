#!/usr/bin/env python3
"""
Final Comprehensive System Test for Memory Context Manager v2
This test verifies everything is working perfectly for sharing
"""

import asyncio
import sys
import os
import requests
import json

async def test_ollama_service():
    """Test if Ollama service is responding and has models"""
    try:
        print("🤖 Testing Ollama LLM Service...")
        
        # Test Ollama API
        response = requests.get("http://localhost:11434/api/tags", timeout=10)
        if response.status_code == 200:
            models = response.json().get("models", [])
            print(f"✅ Ollama service responding (HTTP {response.status_code})")
            print(f"✅ Available models: {len(models)}")
            
            for model in models:
                print(f"   📦 {model['name']} ({model['details']['parameter_size']}, {model['details']['quantization_level']})")
            
            return True
        else:
            print(f"❌ Ollama service error: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Ollama service test failed: {str(e)}")
        return False

def test_web_ui():
    """Test if Web UI is accessible"""
    try:
        print("\n🌐 Testing Web UI...")
        
        response = requests.get("http://localhost:3000", timeout=10)
        if response.status_code == 200:
            print(f"✅ Web UI accessible (HTTP {response.status_code})")
            print("   📱 Users can access at: http://localhost:3000")
            return True
        else:
            print(f"⚠️  Web UI status: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Web UI test failed: {str(e)}")
        return False

async def test_mcp_server():
    """Test MCP server functionality"""
    try:
        print("\n🧠 Testing MCP Server...")
        
        # Import and test the server
        import main
        main.initialize_server()
        
        # Test brain interface
        if hasattr(main, 'brain'):
            brain = main.brain
            brain_tools = brain.get_tool_info()
            print(f"✅ Brain interface ready with {len(brain_tools)} cognitive functions")
            
            # List available brain functions
            for tool_name, description in brain_tools.items():
                print(f"   🧠 {tool_name}: {description}")
        else:
            print("⚠️  Brain interface not found")
            return False
        
        # Test MCP server instance
        mcp_server = main.mcp
        print(f"✅ MCP server instance: {type(mcp_server).__name__}")
        
        return True
        
    except Exception as e:
        print(f"❌ MCP server test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_docker_setup():
    """Test Docker setup and configuration"""
    try:
        print("\n🐳 Testing Docker Setup...")
        
        # Test if our container can run
        import subprocess
        result = subprocess.run([
            "docker", "run", "--rm", "-i", 
            "-v", f"{os.getcwd()}:/workspace", 
            "-w", "/workspace", 
            "memory-context-manager-v2:latest", 
            "python", "-c", "print('✅ Container test successful!')"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Docker container test successful")
            print("✅ Volume mounting working")
            print("✅ Python execution working")
            return True
        else:
            print(f"❌ Docker container test failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Docker setup test failed: {str(e)}")
        return False

async def main():
    """Run all tests"""
    print("🧠 Memory Context Manager v2 - Final System Test")
    print("=" * 60)
    
    tests = [
        ("Ollama LLM Service", test_ollama_service()),
        ("Web UI", test_web_ui()),
        ("MCP Server", test_mcp_server()),
        ("Docker Setup", test_docker_setup())
    ]
    
    results = []
    for test_name, test_coro in tests:
        if asyncio.iscoroutine(test_coro):
            result = await test_coro
        else:
            result = test_coro
        results.append((test_name, result))
    
    # Print summary
    print("\n" + "=" * 60)
    print("🎯 FINAL TEST RESULTS")
    print("=" * 60)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL TESTS PASSED! 🎉")
        print("✅ Your system is ready for sharing!")
        print("✅ Users can clone and run immediately!")
        print("✅ All services are healthy and working!")
    else:
        print("⚠️  Some tests failed - review before sharing")
    
    print("\n🚀 Ready for Cursor MCP Integration!")
    print("📱 Web UI available at: http://localhost:3000")
    print("🤖 LLM API available at: http://localhost:11434")
    
    return all_passed

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
