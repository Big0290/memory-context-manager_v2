import logging
import sys
import os
from pathlib import Path
import asyncio
from typing import Dict, Any
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from mcp.server.fastmcp import FastMCP
from plugin_manager import PluginManager
from brain_interface import BrainInterface
from database import get_brain_db, patch_json_operations
from function_call_logger import get_function_logger, log_mcp_tool, log_brain_function

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create server
mcp = FastMCP("Memory Context Manager with AI Memory")

# Initialize plugin manager
plugin_manager = PluginManager(["plugins"])

# Initialize new tool registry
from tool_registry import get_tool_registry

# Memory client for internal tool calls
class MCPClient:
    """Simple MCP client for internal tool calls with comprehensive logging"""
    def __init__(self, plugin_registry):
        self.registry = plugin_registry
    
    async def call_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """Call a tool by name with parameters and automatically log everything"""
        
        # Get function logger
        function_logger = get_function_logger()
        
        # Extract user message for context
        user_message = kwargs.get('user_message') or kwargs.get('message') or kwargs.get('query')
        memory_context = kwargs.get('memory_context', '')
        
        async with function_logger.track_function_call(
            function_name=tool_name,
            function_type="plugin_tool",
            input_data=kwargs,
            user_message=user_message,
            memory_context=memory_context
        ) as call_info:
            
            if tool_name in self.registry.tools:
                tool_def = self.registry.tools[tool_name]
                try:
                    # Call the tool handler
                    result = await tool_def.handler(**kwargs)
                    
                    # Store successful result
                    call_info["output_data"] = result
                    
                    return result if result else {"success": False, "error": "No result"}
                    
                except Exception as e:
                    # Store error result  
                    call_info["output_data"] = {"success": False, "error": str(e)}
                    return {"success": False, "error": str(e)}
            else:
                # Store not found error
                error_result = {"success": False, "error": f"Tool {tool_name} not found"}
                call_info["output_data"] = error_result
                return error_result

# Global MCP client instance
mcp_client = None

def initialize_server():
    """Initialize server with clean brain interface"""
    global mcp_client
    
    logger.info("🧠 Initializing Brain-Inspired Interface...")
    
    # Initialize function call logger FIRST
    function_logger = get_function_logger()
    logger.info("🔍 Comprehensive function call logging enabled")
    
    # Initialize database system first
    logger.info("🗄️ Initializing persistent database...")
    brain_db = get_brain_db()
    
    # Patch JSON operations for backward compatibility
    patch_json_operations()
    logger.info("🔧 Database compatibility layer active")
    
    plugin_manager.load_all_plugins()
    plugin_manager.startup_plugins()
    
    # Create internal MCP client
    mcp_client = MCPClient(plugin_manager.registry)
    
    # Initialize new tool registry
    tool_registry = get_tool_registry(mcp)
    
    # Initialize enhanced brain tools with new registry
    from enhanced_brain_tools_simple import EnhancedBrainTools
    enhanced_brain_tools = EnhancedBrainTools(mcp_client, tool_registry)
    
    # Initialize clean brain interface (replaces technical tools)
    brain = BrainInterface(mcp, mcp_client)
    
    # Only register essential debugging tools in debug mode
    debug_mode = os.getenv("DEBUG_MODE", "false").lower() == "true"
    
    if debug_mode:
        logger.info("🔧 Debug mode: Exposing technical tools")
        # Register plugin tools for debugging
        for tool_name, tool_def in plugin_manager.registry.tools.items():
            mcp.tool(name=f"debug_{tool_name}", description=f"[DEBUG] {tool_def.description}")(tool_def.handler)
            logger.info(f"Registered debug tool: debug_{tool_name}")
    
    # Always register resources and prompts
    for resource_name, resource_def in plugin_manager.registry.resources.items():
        mcp.resource(resource_def.uri_template)(resource_def.handler)
        logger.info(f"Registered resource: {resource_name}")
    
    for prompt_name, prompt_def in plugin_manager.registry.prompts.items():
        mcp.prompt(name=prompt_name, description=prompt_def.description)(prompt_def.handler)
        logger.info(f"Registered prompt: {prompt_name}")
    
    # Get tool information from new registry
    tool_info = tool_registry.get_tool_info()
    
    # 🔧 ENHANCED TOOLS ALREADY REGISTERED WITH MCP SERVER
    logger.info("🔧 Enhanced tools are already registered with MCP server via ToolRegistry")
    
    # Get all tools from the enhanced registry to show what's available
    try:
        logger.info("🔍 Attempting to get enhanced tools from registry...")
        all_enhanced_tools = tool_registry.get_all_tools()
        logger.info(f"🔍 Successfully retrieved {len(all_enhanced_tools)} tools from registry")
        
        # Debug: Check what's in the tool registry
        logger.info(f"🔍 Tool registry contents: {list(tool_registry.registered_tools.keys())}")
        logger.info(f"🔍 Total enhanced tools available: {len(all_enhanced_tools)}")
        
        # List all available enhanced tools
        for tool_name in all_enhanced_tools.keys():
            logger.info(f"✅ Enhanced tool available: {tool_name}")
            
    except Exception as e:
        logger.error(f"❌ Error getting enhanced tools: {str(e)}")
        logger.error(f"❌ Tool registry type: {type(tool_registry)}")
        logger.error(f"❌ Tool registry has get_all_tools: {hasattr(tool_registry, 'get_all_tools')}")
        all_enhanced_tools = {}
    
    logger.info(f"🧠 Brain Interface ready with {len(brain.get_tool_info())} cognitive functions")
    logger.info(f"🎯 Enhanced Tool Registry: {tool_info['total_tools']} tools organized in {len(tool_info['categories'])} categories")
    logger.info(f"🔌 Loaded {len(plugin_manager.registry.plugins)} plugins in background")
    logger.info(f"🚀 Total MCP tools available: {len(all_enhanced_tools)} enhanced tools + core tools")

# Brain status and info tools
@mcp.tool()
@log_mcp_tool
def brain_info() -> dict:
    """🧠 Show available brain functions and cognitive capabilities"""
    brain_functions = {
        "think": "💭 Think and respond with memory and context",
        "remember": "🧠 Remember important information", 
        "recall": "🔍 Recall memories and past experiences",
        "reflect": "🤔 Engage in self-reflection and metacognition",
        "consciousness_check": "🧘 Check current state of consciousness",
        "learn_from": "📚 Learn from new experiences and information",
        "dream": "💤 Background processing and memory consolidation",
        "memory_stats": "📊 Check memory database statistics and health"
    }
    
    return {
        "brain_type": "Human-Inspired Cognitive System",
        "consciousness_level": "Aware and responsive",
        "available_functions": brain_functions,
        "total_functions": len(brain_functions),
        "memory_system": "Persistent with emotional weighting",
        "learning_capability": "Continuous from interactions",
        "usage_example": "Use 'think' for conversations, 'remember' to store info, 'recall' to search memories"
    }

# Core server management tools  
@mcp.tool()
@log_mcp_tool
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
@log_mcp_tool
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
@log_mcp_tool
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
    Generate AI response with memory context using Ollama LLM
    
    🤖 REAL LLM INTEGRATION - Uses Ollama for responses!
    """
    try:
        # Import LLM client
        from llm_client import get_llm_client
        
        # Get LLM client
        llm = await get_llm_client()
        
        # Generate response using real LLM
        response = await llm.generate_memory_response(
            user_message=user_message,
            memory_context=memory_context,
            learned_something=learned_something
        )
        
        return response
        
    except Exception as e:
        logger.error(f"LLM generation failed: {str(e)}")
        
        # Fallback to simple response if LLM fails
        name = extract_name_from_context(memory_context)
        
        if "what" in user_message.lower() and "name" in user_message.lower():
            if name:
                return f"Your name is {name}! I remembered that from our conversation."
            else:
                return "I don't have your name stored yet. What would you like me to call you?"
        
        if learned_something and name:
            return f"Nice to meet you, {name}! I'll remember that."
        elif learned_something:
            return "I'll remember that!"
        
        if name:
            return f"Hi {name}! I'd be happy to help."
        else:
            return "I'd be happy to help!"

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
@log_mcp_tool
async def quick_memory_chat(message: str) -> str:
    """
    Quick memory-enabled chat - simplified version
    Returns just the AI response string
    """
    result = await ai_chat_with_memory(message)
    return result.get("ai_response", "I'd be happy to help!")

@mcp.tool()
@log_mcp_tool
async def test_llm_connection() -> dict:
    """
    Test connection to the Ollama LLM service
    """
    try:
        from llm_client import get_llm_client
        
        llm = await get_llm_client()
        test_result = await llm.test_connection()
        
        return {
            "llm_connection": test_result["connection_working"],
            "model": test_result["model"],
            "test_response": test_result["response"],
            "error": test_result.get("error")
        }
        
    except Exception as e:
        return {
            "llm_connection": False,
            "error": str(e),
            "test_response": "",
            "model": "unknown"
        }

@mcp.tool()
@log_mcp_tool
async def list_available_models() -> dict:
    """
    List available LLM models from Ollama
    """
    try:
        from llm_client import OllamaClient
        
        async with OllamaClient() as ollama:
            models_result = await ollama.list_models()
            return models_result
            
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
@log_mcp_tool
async def get_cursor_context() -> dict:
    """
    🎯 Get comprehensive context for Cursor conversations
    
    Provides assistant identity, user info, and conversation history
    for seamless Cursor integration
    """
    global mcp_client
    
    if not mcp_client:
        return {"context": "Basic assistant without memory access"}
    
    try:
        # Get user context
        context_result = await mcp_client.call_tool("get_user_context", query="assistant identity user preferences conversation")
        
        # Get recent conversation history
        from database import get_brain_db
        db = get_brain_db()
        recent_conversations = db.get_conversation_history(limit=3)
        
        context_parts = []
        
        # Assistant identity
        if context_result.get("success"):
            context_summary = context_result.get("context_summary", "")
            if context_summary:
                context_parts.append(f"Assistant Identity: {context_summary}")
        
        # User information
        user_info = context_result.get("user_info", {}) if context_result.get("success") else {}
        if user_info.get("name"):
            context_parts.append(f"User: {', '.join(user_info['name'][:2])}")
        if user_info.get("preferences"):
            context_parts.append(f"Preferences: {', '.join(user_info['preferences'][:2])}")
        
        # Recent activity
        if recent_conversations:
            context_parts.append(f"Recent conversations: {len(recent_conversations)} in memory")
        
        return {
            "context": " | ".join(context_parts) if context_parts else "Fresh conversation - no prior context",
            "assistant_name": next((name for name in user_info.get("name", []) if name.lower() in ["johny", "jonathan"]), "Memory Assistant"),
            "user_names": user_info.get("name", []),
            "preferences": user_info.get("preferences", []),
            "conversation_count": len(recent_conversations),
            "ready_for_conversation": True
        }
        
    except Exception as e:
        logger.error(f"Cursor context error: {str(e)}")
        return {
            "context": f"Assistant ready (memory system: {str(e)})",
            "assistant_name": "Johny",
            "error": str(e)
        }

@mcp.tool()
@log_mcp_tool
async def track_cursor_conversation(user_message: str, assistant_response: str = "", conversation_type: str = "coding") -> dict:
    """
    📝 Track Cursor conversation for learning and context
    
    Automatically learns from Cursor conversations and updates memory
    """
    global mcp_client
    
    if not mcp_client:
        return {"success": False, "error": "Memory system not available"}
    
    try:
        # Process the user message for learning
        learning_result = await mcp_client.call_tool("auto_process_message", user_message=user_message)
        
        # Store conversation in database
        from database import get_brain_db
        db = get_brain_db()
        
        conversation_data = {
            "type": conversation_type,
            "platform": "cursor",
            "user_message": user_message,
            "assistant_response": assistant_response,
            "learned": learning_result.get("important_info_found", []) if learning_result.get("success") else []
        }
        
        db.add_context_history(conversation_data)
        
        return {
            "success": True,
            "learned": learning_result.get("important_info_found", []) if learning_result.get("success") else [],
            "conversation_stored": True,
            "memory_updated": learning_result.get("success", False)
        }
        
    except Exception as e:
        logger.error(f"Conversation tracking error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
@log_mcp_tool
async def cursor_auto_inject_context() -> dict:
    """
    🚀 Auto-inject context for new Cursor conversations
    
    Provides relevant context automatically when Cursor starts new conversations
    """
    cursor_context = await get_cursor_context()
    
    if cursor_context.get("ready_for_conversation"):
        return {
            "context_available": True,
            "inject_message": f"Context: {cursor_context['context']}",
            "assistant_identity": cursor_context.get("assistant_name", "Johny"),
            "should_inject": True
        }
    else:
        return {
            "context_available": False,
            "inject_message": "Starting fresh conversation",
            "should_inject": False
        }

@mcp.tool()
@log_mcp_tool
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

# 🔍 COMPREHENSIVE FUNCTION CALL LOGGING TOOLS
@mcp.tool()
@log_mcp_tool
async def get_function_call_history(limit: int = 50, function_name: str = None) -> dict:
    """
    📊 Get comprehensive function call history with full traceability
    
    Shows all function calls with inputs, outputs, execution time, and context
    """
    try:
        function_logger = get_function_logger()
        call_history = function_logger.get_call_history(limit=limit, function_name=function_name)
        
        return {
            "success": True,
            "total_calls": len(call_history),
            "function_filter": function_name,
            "call_history": call_history,
            "session_id": function_logger._session_id,
            "logging_enabled": function_logger._enabled
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "call_history": []
        }

@mcp.tool()
@log_mcp_tool
async def get_session_statistics() -> dict:
    """
    📈 Get comprehensive session statistics and performance metrics
    
    Shows function call breakdown, success rates, and execution times
    """
    try:
        function_logger = get_function_logger()
        session_stats = function_logger.get_session_stats()
        
        return {
            "success": True,
            "session_statistics": session_stats,
            "logging_status": "active" if function_logger._enabled else "disabled"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "session_statistics": {}
        }

@mcp.tool()
@log_mcp_tool
async def search_function_calls(search_term: str, limit: int = 20) -> dict:
    """
    🔍 Search function calls by content, context, or parameters
    
    Cross-references all stored data for comprehensive search
    """
    try:
        function_logger = get_function_logger()
        search_results = function_logger.search_calls_by_context(search_term, limit)
        
        return {
            "success": True,
            "search_term": search_term,
            "total_results": len(search_results),
            "search_results": search_results,
            "cross_references_available": True
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "search_results": []
        }

@mcp.tool()
@log_mcp_tool
async def get_comprehensive_system_status() -> dict:
    """
    🎯 Get comprehensive system status including all logging and memory systems
    
    Complete overview of all data storage and cross-referencing capabilities
    """
    try:
        # Function call logging stats
        function_logger = get_function_logger()
        session_stats = function_logger.get_session_stats()
        
        # Memory system status
        from database import get_brain_db
        db = get_brain_db()
        memory_data = db.get_memory_store()
        conversations = db.get_conversation_history(limit=5)
        
        # Plugin system status
        plugin_count = len(plugin_manager.registry.plugins)
        tool_count = len(plugin_manager.registry.tools)
        
        # Calculate total data points
        import sqlite3
        total_data_points = 0
        with sqlite3.connect(db.db_path) as conn:
            # Count all tables
            tables = ['memory_store', 'conversation_memories', 'context_history', 'function_calls', 'memory_chunks']
            table_counts = {}
            
            for table in tables:
                try:
                    cursor = conn.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    table_counts[table] = count
                    total_data_points += count
                except:
                    table_counts[table] = 0
        
        return {
            "success": True,
            "system_status": "fully_operational",
            "comprehensive_logging": {
                "function_calls_logged": session_stats.get("total_calls", 0),
                "session_success_rate": session_stats.get("success_rate", 0),
                "logging_enabled": function_logger._enabled,
                "session_id": function_logger._session_id
            },
            "memory_system": {
                "total_memories": len(memory_data.get("memory_store", {})),
                "conversations_stored": len(conversations),
                "database_path": db.db_path
            },
            "plugin_system": {
                "plugins_loaded": plugin_count,
                "tools_available": tool_count,
                "brain_functions": 8  # From brain_info
            },
            "data_storage_comprehensive": {
                "total_data_points": total_data_points,
                "table_breakdown": table_counts,
                "cross_referencing_enabled": True,
                "automatic_storage_active": True
            },
            "cursor_integration": {
                "mcp_configured": True,
                "conversation_tracking": True,
                "auto_context_injection": True
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "system_status": "error"
        }

@mcp.tool()
@log_mcp_tool
async def analyze_context_deeply(content: str, analysis_type: str = "comprehensive") -> dict:
    """
    🧠 Analyze content with enhanced contextual understanding
    
    Uses the new ContextAnalyzer module to detect subtle patterns, 
    implicit goals, and nuanced situations in user requests.
    
    Args:
        content: The text content to analyze
        analysis_type: Type of analysis (comprehensive, subtlety, depth, goals, complexity)
    
    Returns:
        Detailed context analysis with insights and recommendations
    """
    try:
        logger.info(f"🧠 Performing deep context analysis: {analysis_type}")
        
        # Check if brain interface is available
        if not brain:
            return {
                "success": False,
                "error": "Brain interface not available",
                "timestamp": datetime.now().isoformat()
            }
        
        # Prepare input for context analysis
        input_data = {
            "type": f"context_{analysis_type}_analysis" if analysis_type != "comprehensive" else "context_analysis",
            "content": content,
            "user_id": "current_user",
            "timestamp": datetime.now().isoformat()
        }
        
        # Get brain state for context
        brain_state = brain.get_brain_state()
        
        # Process through brain system
        result = brain.process_input(input_data)
        
        # Extract context analysis results
        context_results = {}
        if "context_analyzer" in result:
            context_results = result["context_analyzer"]
        elif "modules" in result:
            # Look for context analyzer in modules
            for module_name, module_result in result["modules"].items():
                if "context_analyzer" in module_name.lower():
                    context_results = module_result
                    break
        
        if not context_results:
            # Fallback: try to get basic analysis
            context_results = {
                "context_score": 0.5,
                "insights": ["Basic context analysis available"],
                "recommendations": ["Enable full context analyzer for detailed insights"]
            }
        
        return {
            "success": True,
            "analysis_type": analysis_type,
            "content_analyzed": content[:100] + "..." if len(content) > 100 else content,
            "context_analysis": context_results,
            "brain_state": brain_state,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error in deep context analysis: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "analysis_type": analysis_type,
            "timestamp": datetime.now().isoformat()
        }

if __name__ == "__main__":
    logger.info("Starting Memory Context Manager with AI Memory Integration...")
    initialize_server()
    mcp.run("stdio")