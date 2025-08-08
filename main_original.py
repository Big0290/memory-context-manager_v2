import logging
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from mcp.server.fastmcp import FastMCP
from plugin_manager import PluginManager

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create server
mcp = FastMCP("Memory Context Manager")

# Initialize plugin manager
plugin_manager = PluginManager(["plugins"])

def initialize_server():
    """Initialize server with plugins"""
    logger.info("Loading plugins...")
    plugin_manager.load_all_plugins()
    plugin_manager.startup_plugins()
    
    # Register plugin tools
    for tool_name, tool_def in plugin_manager.registry.tools.items():
        mcp.tool(name=tool_name, description=tool_def.description)(tool_def.handler)
        logger.info(f"Registered tool: {tool_name}")
    
    # Register plugin resources  
    for resource_name, resource_def in plugin_manager.registry.resources.items():
        mcp.resource(resource_def.uri_template)(resource_def.handler)
        logger.info(f"Registered resource: {resource_name}")
    
    # Register plugin prompts
    for prompt_name, prompt_def in plugin_manager.registry.prompts.items():
        mcp.prompt(name=prompt_name, description=prompt_def.description)(prompt_def.handler)
        logger.info(f"Registered prompt: {prompt_name}")
    
    logger.info(f"Server initialized with {len(plugin_manager.registry.plugins)} plugins")

# Core server management tools
@mcp.tool()
def list_plugins() -> dict:
    """List all loaded plugins and their information"""
    plugin_info = {}
    for plugin_name, plugin in plugin_manager.registry.plugins.items():
        metadata = plugin.metadata
        plugin_info[plugin_name] = {
            "version": metadata.version,
            "description": metadata.description,
            "author": metadata.author,
            "tools": [tool.name for tool in plugin.get_tools()],
            "resources": [resource.name for resource in plugin.get_resources()],
            "prompts": [prompt.name for prompt in plugin.get_prompts()],
        }
    return plugin_info

@mcp.tool()
def server_status() -> dict:
    """Get server status and statistics"""
    return {
        "server_name": "Memory Context Manager",
        "plugins_loaded": len(plugin_manager.registry.plugins),
        "tools_available": len(plugin_manager.registry.tools) + 2,  # +2 for core tools
        "resources_available": len(plugin_manager.registry.resources),
        "prompts_available": len(plugin_manager.registry.prompts),
        "plugin_directories": plugin_manager.plugin_dirs,
    }

if __name__ == "__main__":
    logger.info("Starting Memory Context Manager...")
    initialize_server()
    mcp.run("stdio")
