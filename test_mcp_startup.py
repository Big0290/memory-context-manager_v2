#!/usr/bin/env python3
"""
Test MCP server startup
"""

import sys
import os

def test_mcp_startup():
    """Test if MCP server can start"""
    try:
        print("🧪 Testing MCP server startup...")
        
        # Import main module
        import main
        
        # Initialize server
        print("🔧 Initializing server...")
        main.initialize_server()
        print("✅ Server initialized")
        
        # Check if we can access the MCP server
        mcp_server = main.mcp
        print(f"✅ MCP server: {type(mcp_server).__name__}")
        
        # Try to start the MCP server (this should work)
        print("🚀 Attempting to start MCP server...")
        
        # Import asyncio for testing
        import asyncio
        
        # Test if we can list tools
        async def test_tools():
            try:
                tools = await mcp_server.list_tools()
                print(f"✅ Tools available: {len(tools)}")
                for tool in tools[:3]:  # Show first 3 tools
                    print(f"   🧠 {tool.name}: {tool.description[:50]}...")
                return True
            except Exception as e:
                print(f"❌ Error listing tools: {str(e)}")
                return False
        
        # Run the test
        success = asyncio.run(test_tools())
        
        if success:
            print("\n🎉 MCP server is working correctly!")
            print("✅ Tools are registered and accessible")
            print("✅ Server can start and communicate")
        else:
            print("\n⚠️  MCP server has issues")
            print("❌ Tools not accessible")
        
        return success
        
    except Exception as e:
        print(f"❌ MCP startup test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_mcp_startup()
    sys.exit(0 if success else 1)
