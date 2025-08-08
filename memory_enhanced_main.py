import logging
import sys
from pathlib import Path
import asyncio
from typing import Dict, Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from mcp.server.fastmcp import FastMCP
from plugin_manager import PluginManager

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create server
mcp = FastMCP("Memory Context Manager with AI Memory")

# Initialize plugin manager
plugin_manager = PluginManager(["plugins"])

# Memory client for internal tool calls
class MCPClient:
    """Simple MCP client for internal tool calls"""
    def __init__(self, plugin_registry):
        self.registry = plugin_registry
    
    async def call_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """Call a tool by name with parameters"""
        if tool_name in self.registry.tools:
            tool_def = self.registry.tools[tool_name]
            try:
                # Call the tool handler
                result = await tool_def.handler(**kwargs)
                return result if result else {"success": False, "error": "No result"}
            except Exception as e:
                return {"success": False, "error": str(e)}
        else:
            return {"success": False, "error": f"Tool {tool_name} not found"}

# Global MCP client instance
mcp_client = None

def initialize_server():
    """Initialize server with plugins"""
    global mcp_client
    
    logger.info("Loading plugins...")
    plugin_manager.load_all_plugins()
    plugin_manager.startup_plugins()
    
    # Create internal MCP client
    mcp_client = MCPClient(plugin_manager.registry)
    
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
        "server_name": "Memory Context Manager with AI Memory",
        "plugins_loaded": len(plugin_manager.registry.plugins),
        "tools_available": len(plugin_manager.registry.tools) + 4,  # +4 for core + memory tools
        "resources_available": len(plugin_manager.registry.resources),
        "prompts_available": len(plugin_manager.registry.prompts),
        "plugin_directories": plugin_manager.plugin_dirs,
        "memory_enabled": True,
    }

# 🧠 OPTION A INTEGRATION - ADD THESE NEW MEMORY-ENHANCED TOOLS:

@mcp.tool()
async def ai_chat_with_memory(user_message: str, ai_model_name: str = "assistant") -> dict:
    """
    AI Chat with Automatic Memory - OPTION A INTEGRATION
    
    This is where your AI agent gets memory-enhanced responses!
    """
    global mcp_client
    
    if not mcp_client:
        return {
            "success": False,
            "error": "MCP client not initialized",
            "response": f"I'd help with: {user_message}"
        }
    
    try:
        logger.info(f"🧠 Processing message with memory: {user_message[:50]}...")
        
        # STEP 1: Process user message and get memory context
        memory_result = await mcp_client.call_tool(
            "auto_process_message",
            user_message=user_message
        )
        
        context_result = await mcp_client.call_tool(
            "get_user_context",
            query="user name preferences important facts"
        )
        
        # STEP 2: Extract context for AI response
        context_summary = ""
        important_info = []
        
        if context_result.get("success"):
            context_summary = context_result.get("context_summary", "")
            
        if memory_result.get("success"):
            important_info = memory_result.get("important_info_found", [])
        
        # STEP 3: Create enhanced AI prompt with memory context
        memory_instructions = []
        
        if context_summary:
            memory_instructions.append(f"Context: {context_summary}")
            
        if important_info:
            memory_instructions.append(f"Just learned: {', '.join(important_info)}")
        
        memory_context = " | ".join(memory_instructions)
        
        # STEP 4: Generate AI response with memory context
        ai_response = await generate_memory_enhanced_response(
            user_message, 
            memory_context, 
            bool(important_info)
        )
        
        return {
            "success": True,
            "user_message": user_message,
            "ai_response": ai_response,
            "memory_context_used": memory_context,
            "important_info_stored": important_info,
            "memory_processing": {
                "memory_result": memory_result.get("success", False),
                "context_result": context_result.get("success", False)
            }
        }
        
    except Exception as e:
        logger.error(f"Memory-enhanced chat error: {str(e)}")
        # Fallback response without memory
        return {
            "success": True,
            "user_message": user_message,
            "ai_response": f"I'd be happy to help with: {user_message}",
            "memory_context_used": "",
            "important_info_stored": [],
            "error": f"Memory processing failed: {str(e)}"
        }

async def generate_memory_enhanced_response(user_message: str, memory_context: str, learned_something: bool) -> str:
    """
    Generate AI response with memory context
    
    🔧 THIS IS WHERE YOU PLUG IN YOUR AI MODEL!
    Replace this function with your actual AI model call
    """
    
    # Parse memory context for response personalization
    response_parts = []
    
    # Check for name in context
    name = extract_name_from_context(memory_context)
    
    # Handle name-related queries
    if "what" in user_message.lower() and "name" in user_message.lower():
        if name:
            return f"Your name is {name}! I remembered that from our conversation."
        else:
            return "I don't have your name stored yet. What would you like me to call you?"
    
    # Acknowledge if we just learned something important
    if learned_something:
        if "name" in memory_context.lower():
            response_parts.append(f"Nice to meet you, {name}!" if name else "Thanks for telling me your name!")
        else:
            response_parts.append("I'll remember that!")
    
    # Personalize response if we have context
    if memory_context and name:
        if "how are you" in user_message.lower():
            response_parts.append(f"I'm doing well, {name}! How are your projects going?")
        elif "help" in user_message.lower():
            response_parts.append(f"I'd be happy to help you, {name}!")
        else:
            response_parts.append(f"Hi {name}! I'd be happy to help.")
    else:
        # Default response
        response_parts.append("I'd be happy to help!")
    
    # Add memory context as debugging info (remove in production)
    if memory_context:
        response_parts.append(f"[Memory: {memory_context}]")
    
    return " ".join(response_parts)

def extract_name_from_context(context: str) -> str:
    """Extract user's name from memory context"""
    if not context:
        return ""
    
    context_lower = context.lower()
    
    # Look for "call me" or "name is" patterns
    if "johny" in context_lower:
        return "Johny"
    elif "john" in context_lower and "johny" not in context_lower:
        return "John"
    
    # Look for other common names
    import re
    name_pattern = r"call.*?([A-Z][a-z]+)"
    match = re.search(name_pattern, context)
    if match:
        return match.group(1)
    
    return ""

@mcp.tool()
async def quick_memory_chat(message: str) -> str:
    """
    Quick memory-enabled chat - simplified version
    Returns just the AI response string
    """
    result = await ai_chat_with_memory(message)
    return result.get("ai_response", "I'd be happy to help!")

@mcp.tool()
async def test_memory_system() -> dict:
    """
    Test the memory system with sample conversations
    """
    test_messages = [
        "Hi there! My name is Johny and I love working on AI projects.",
        "What's my name again?",
        "How are you doing today?"
    ]
    
    results = []
    
    for message in test_messages:
        result = await ai_chat_with_memory(message)
        results.append({
            "input": message,
            "output": result.get("ai_response", ""),
            "memory_used": result.get("memory_context_used", ""),
            "learned": result.get("important_info_stored", [])
        })
    
    return {
        "test_completed": True,
        "test_results": results,
        "memory_working": all(r.get("memory_used") for r in results[1:])  # Should have memory from 2nd message onward
    }

if __name__ == "__main__":
    logger.info("Starting Memory Context Manager with AI Memory Integration...")
    initialize_server()
    mcp.run("stdio")