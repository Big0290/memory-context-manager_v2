#!/usr/bin/env python3
"""
Test Local MCP Server stdio Communication
"""

import sys
import asyncio
import logging
import subprocess
import time

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_local_mcp_stdio():
    """Test if local MCP server can communicate via stdio"""
    try:
        logger.info("🧪 Testing local MCP server stdio communication...")
        
        # Start the local MCP server
        logger.info("🚀 Starting local MCP server...")
        
        # Start the server process
        process = subprocess.Popen(
            ["python", "main.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        # Wait a bit for server to start
        time.sleep(2)
        
        # Check if process is still running
        if process.poll() is None:
            logger.info("✅ Local MCP server started successfully")
            
            # Try to send a simple MCP message
            try:
                # Send a simple test message
                test_message = "test\n"
                process.stdin.write(test_message)
                process.stdin.flush()
                
                # Wait for response
                time.sleep(1)
                
                # Check if we got any output
                if process.stdout.readable():
                    output = process.stdout.read()
                    logger.info(f"📤 Server output: {output[:100]}...")
                
                return True
                
            except Exception as e:
                logger.error(f"❌ Communication test failed: {str(e)}")
                return False
            finally:
                # Clean up
                process.terminate()
                process.wait()
        else:
            logger.error("❌ Local MCP server failed to start")
            # Check stderr for errors
            stderr_output = process.stderr.read()
            logger.error(f"Stderr: {stderr_output}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_local_mcp_stdio()
    sys.exit(0 if success else 1)
