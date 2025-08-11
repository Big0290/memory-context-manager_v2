#!/usr/bin/env python3
"""
Clean Tool Registry System
Prevents tool conflicts and organizes tools logically
"""

import logging
from typing import Dict, Any, List, Optional
from mcp.server.fastmcp import FastMCP

logger = logging.getLogger(__name__)

class ToolRegistry:
    """Clean tool registry that prevents conflicts and organizes tools logically"""
    
    def __init__(self, mcp_server: FastMCP):
        self.mcp = mcp_server
        self.registered_tools = {}
        self.tool_categories = {
            "cognitive": [],
            "memory": [],
            "analysis": [],
            "cursor": [],
            "system": [],
            "context": []
        }
    
    def register_tool(self, name: str, handler, category: str, description: str, **kwargs):
        """Register a tool with conflict prevention"""
        
        if name in self.registered_tools:
            logger.warning(f"Tool '{name}' already registered. Skipping duplicate.")
            return False
        
        # Register with MCP server
        tool_decorator = self.mcp.tool()
        decorated_handler = tool_decorator(handler)
        
        # Store tool info
        self.registered_tools[name] = {
            "handler": decorated_handler,
            "category": category,
            "description": description,
            "kwargs": kwargs
        }
        
        # Add to category
        if category in self.tool_categories:
            self.tool_categories[category].append(name)
        
        logger.info(f"✅ Registered tool: {name} (category: {category})")
        return True
    
    def get_tool_info(self) -> Dict[str, Any]:
        """Get comprehensive tool information"""
        return {
            "total_tools": len(self.registered_tools),
            "categories": self.tool_categories,
            "tools": {
                name: {
                    "category": info["category"],
                    "description": info["description"]
                }
                for name, info in self.registered_tools.items()
            }
        }
    
    def list_tools_by_category(self, category: str) -> List[str]:
        """List tools in a specific category"""
        return self.tool_categories.get(category, [])
    
    def get_tool_description(self, name: str) -> Optional[str]:
        """Get description of a specific tool"""
        tool_info = self.registered_tools.get(name)
        return tool_info["description"] if tool_info else None
    
    def get_all_tools(self) -> Dict[str, Any]:
        """Get all registered tools with their handlers and info"""
        return self.registered_tools

# Global tool registry instance
tool_registry = None

def get_tool_registry(mcp_server: FastMCP) -> ToolRegistry:
    """Get or create the global tool registry"""
    global tool_registry
    if tool_registry is None:
        tool_registry = ToolRegistry(mcp_server)
    return tool_registry
