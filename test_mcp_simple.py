#!/usr/bin/env python3
"""
Simple MCP Server Test - Verify server can start and expose tools
"""

import sys
import os
import asyncio
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_mcp_server():
    """Test if MCP server can start and expose tools"""
    try:
        logger.info("🧪 Testing MCP server startup...")
        
        # Import main module
        import main
        
        logger.info("✅ Main module imported successfully")
        
        # Check if MCP server is initialized
        if hasattr(main, 'mcp'):
            logger.info("✅ MCP server object exists")
            
            # Check tools before initialization
            tools_before = getattr(main.mcp, '_tools', {})
            logger.info(f"📋 Tools before init: {len(tools_before)}")
            
            # Call initialize_server to register tools
            logger.info("🔧 Calling initialize_server()...")
            main.initialize_server()
            
            # Check tools after initialization - try different attributes
            tools_after = getattr(main.mcp, '_tools', {})
            logger.info(f"📋 Tools after init (_tools): {len(tools_after)}")
            
            # Check other possible tool storage locations
            if hasattr(main.mcp, 'tools'):
                tools_alt = main.mcp.tools
                logger.info(f"📋 Tools (tools attribute): {len(tools_alt) if tools_alt else 0}")
            
            if hasattr(main.mcp, 'handlers'):
                handlers = main.mcp.handlers
                logger.info(f"📋 Handlers: {len(handlers) if handlers else 0}")
            
            # Check if brain interface was created
            if hasattr(main, 'brain'):
                logger.info("🧠 Brain interface exists")
                brain_tools = main.brain.get_tool_info()
                logger.info(f"🧠 Brain reports {len(brain_tools)} tools")
            else:
                logger.info("❌ Brain interface not found")
            
            # Try to list tools using the list_tools method (async)
            logger.info("🔍 Calling list_tools() method...")
            try:
                tools_list = await main.mcp.list_tools()
                logger.info(f"📋 list_tools() returned: {len(tools_list)} tools")
                
                if tools_list:
                    # Show first few tools
                    logger.info("📋 First 5 tools:")
                    for i, tool in enumerate(tools_list[:5]):
                        if hasattr(tool, 'name'):
                            logger.info(f"  {i+1}. {tool.name}")
                        elif isinstance(tool, dict) and 'name' in tool:
                            logger.info(f"  {i+1}. {tool['name']}")
                        else:
                            logger.info(f"  {i+1}. {str(tool)[:50]}...")
                    
                    # Check if we have brain tools
                    brain_tool_names = ['think', 'remember', 'recall', 'reflect', 'consciousness_check']
                    found_brain_tools = []
                    for tool in tools_list:
                        tool_name = getattr(tool, 'name', None) or (tool.get('name') if isinstance(tool, dict) else None)
                        if tool_name in brain_tool_names:
                            found_brain_tools.append(tool_name)
                    
                    logger.info(f"🧠 Found brain tools: {found_brain_tools}")
                    
                    return True
                else:
                    logger.warning("⚠️ list_tools() returned empty")
                    return False
            except Exception as e:
                logger.error(f"❌ list_tools() failed: {str(e)}")
                return False
            
        else:
            logger.error("❌ MCP server object not found")
            return False
            
    except Exception as e:
        logger.error(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main entry point"""
    success = asyncio.run(test_mcp_server())
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
