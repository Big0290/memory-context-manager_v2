#!/usr/bin/env python3
"""
Test MCP Server Protocol Startup
"""

import sys
import asyncio
import logging
import signal
import time

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def signal_handler(signum, frame):
    """Handle interrupt signals"""
    logger.info("🛑 Received interrupt signal, shutting down...")
    sys.exit(0)

async def test_mcp_protocol():
    """Test if MCP server can start stdio protocol"""
    try:
        logger.info("🧪 Testing MCP server protocol startup...")
        
        # Import main module
        import main
        
        logger.info("✅ Main module imported successfully")
        
        # Initialize server
        main.initialize_server()
        logger.info("✅ Server initialized")
        
        # Check tools
        tools_list = await main.mcp.list_tools()
        logger.info(f"✅ Found {len(tools_list)} tools")
        
        # Test if we can start the MCP server (without blocking)
        logger.info("🚀 Testing MCP server startup...")
        
        # Create a task to start the server
        server_task = asyncio.create_task(start_server_safely(main.mcp))
        
        # Wait a bit to see if it starts
        await asyncio.sleep(2)
        
        if not server_task.done():
            logger.info("✅ MCP server started successfully (non-blocking)")
            server_task.cancel()
            return True
        else:
            logger.error("❌ MCP server task completed unexpectedly")
            return False
            
    except Exception as e:
        logger.error(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def start_server_safely(mcp_server):
    """Start MCP server safely"""
    try:
        await mcp_server.run("stdio")
    except Exception as e:
        logger.error(f"Server error: {str(e)}")

def main():
    """Main entry point"""
    # Set up signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    success = asyncio.run(test_mcp_protocol())
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
