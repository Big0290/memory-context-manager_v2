#!/usr/bin/env python3
"""
Test MCP Server stdio Communication
"""

import sys
import json
import asyncio
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_mcp_stdio():
    """Test MCP server stdio communication"""
    try:
        logger.info("🧪 Testing MCP server stdio communication...")
        
        # Import main module
        import main
        
        logger.info("✅ Main module imported successfully")
        
        # Initialize server
        main.initialize_server()
        logger.info("✅ Server initialized")
        
        # Check tools
        tools_list = await main.mcp.list_tools()
        logger.info(f"✅ Found {len(tools_list)} tools")
        
        # Test a simple tool call
        logger.info("🧪 Testing brain_info tool...")
        
        # Find the brain_info tool
        brain_info_tool = None
        for tool in tools_list:
            if hasattr(tool, 'name') and tool.name == 'brain_info':
                brain_info_tool = tool
                break
        
        if brain_info_tool:
            logger.info("✅ Found brain_info tool")
            
            # Inspect the tool object
            logger.info(f"🔍 Tool object type: {type(brain_info_tool)}")
            logger.info(f"🔍 Tool object attributes: {dir(brain_info_tool)}")
            
            # Try different ways to call it
            try:
                # Try direct call
                if callable(brain_info_tool):
                    result = await brain_info_tool()
                    logger.info(f"✅ brain_info direct call result: {result}")
                    return True
                else:
                    logger.info("❌ Tool is not callable")
                    return False
                    
            except Exception as e:
                logger.error(f"❌ brain_info call failed: {str(e)}")
                return False
        else:
            logger.error("❌ brain_info tool not found")
            return False
            
    except Exception as e:
        logger.error(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main entry point"""
    success = asyncio.run(test_mcp_stdio())
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
