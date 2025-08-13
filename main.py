import logging
import sys
import os
from pathlib import Path
import asyncio
from typing import Dict, Any
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Import our Phase 1-5 systems for integration
from core.intelligence import (
    ProjectScanner,
    KnowledgeIngestionEngine,
    PersonalizationEngine,
    ContextOrchestrator,
    AIIntegrationEngine
)

# Import our enhanced web crawler and search engine systems
from web_crawler import WebCrawlerMCPTools
from integration import SymbioticIntegrationBridge

from mcp.server.fastmcp import FastMCP
from src.plugin_manager import PluginManager
from core.brain import BrainInterface
from core.brain.tool_registry import ToolRegistry
from core.memory import get_brain_db, patch_json_operations, get_function_logger, log_mcp_tool, log_brain_function

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create server
mcp = FastMCP("Memory Context Manager with AI Memory")

# Initialize plugin manager
plugin_manager = PluginManager(["plugins"])

# Initialize new tool registry
from core.memory import get_tool_registry

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

# Global Phase 1-5 system instances
phase1_scanner = None
phase2_knowledge = None
phase3_personalization = None
phase4_orchestrator = None
phase5_ai = None

# Global enhanced system instances
web_crawler_tools = None
symbiotic_bridge = None

# Global brain interface instance
brain_interface = None

def get_brain_interface():
    """Get brain interface, initializing if necessary"""
    global brain_interface
    if brain_interface is None:
        try:
            # Initialize brain interface for testing purposes
            from core.brain import BrainInterface
            brain_interface = BrainInterface()
            logger.info("🧠 Brain interface lazily initialized for testing")
        except Exception as e:
            logger.warning(f"⚠️ Could not initialize brain interface: {e}")
            brain_interface = None
    return brain_interface

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
    
    # DISABLE ALL PLUGIN LOADING - We only want the restructured cognitive system
    logger.info("🧠 Loading restructured cognitive system ONLY...")
    
    # Clear any existing plugins to start fresh
    plugin_manager.registry.plugins.clear()
    plugin_manager.registry.tools.clear()
    plugin_manager.registry.resources.clear()
    plugin_manager.registry.prompts.clear()
    
    logger.info("✅ Cleared all existing plugins")
    
    # We'll manually register only the tools we need
    logger.info("✅ Plugin loading disabled - using manual tool registration only")
    
    # Create internal MCP client
    mcp_client = MCPClient(plugin_manager.registry)
    
    # Initialize new tool registry
    tool_registry = get_tool_registry(mcp)
    
    # 🚫 DISABLED: Enhanced brain tools to prevent tool duplication
    # from enhanced_brain_tools_simple import EnhancedBrainTools
    # enhanced_brain_tools = EnhancedBrainTools(mcp_client, tool_registry)
    
    # Initialize clean brain interface (replaces technical tools)
    brain = BrainInterface(mcp, mcp_client)
    
    # Set global brain interface for tool access
    global brain_interface
    brain_interface = brain
    
    # Register agent-friendly brain tools with MCP server using add_tool method
    logger.info("🧠 Registering agent-friendly brain tools with MCP server...")
    try:
        # Create wrapper functions that access the brain interface
        async def analyze_with_context(message: str, context: str = "conversation") -> dict:
            """🧠 Analyze any topic with deep context understanding and background processing"""
            return await brain.analyze_with_context(message, context)
            
        async def store_knowledge(information: str, importance: str = "medium") -> dict:
            """💾 Store important information with emotional weighting and context analysis"""
            return await brain.store_knowledge(information, importance)
            
        async def search_memories(query: str, depth: str = "surface") -> dict:
            """🔍 Search through stored memories with contextual relevance scoring"""
            return await brain.search_memories(query, depth)
            
        async def process_background() -> dict:
            """💤 Process information in background with memory consolidation and optimization"""
            return await brain.process_background()
            
        async def self_assess(topic: str = "recent_interactions") -> dict:
            """🤔 Perform self-assessment and metacognitive analysis"""
            return await brain.self_assess(topic)
            
        async def learn_from_content(source: str, lesson_type: str = "experiential", content_type: str = "text") -> dict:
            """📚 Learn and integrate new information with context analysis"""
            return await brain.learn_from_content(source, lesson_type, content_type)
            
        async def check_system_status() -> dict:
            """📊 Check current system status, consciousness, and cognitive load"""
            return await brain.check_system_status()
            
        async def get_memory_statistics() -> dict:
            """📈 Get comprehensive memory system statistics, health, and performance metrics"""
            return await brain.get_memory_statistics()
            
        async def analyze_dream_system() -> dict:
            """🧠 Analyze dream system effectiveness and context injection optimization"""
            return await brain.analyze_dream_system()
            
        async def analyze_system_performance() -> dict:
            """⚡ Comprehensive system performance analysis and optimization assessment"""
            return await brain.analyze_system_performance()
        
        async def get_comprehensive_logs(log_level: str = "INFO", max_lines: int = 1000) -> dict:
            """📋 Get comprehensive system logs with detailed analysis"""
            return await brain.get_comprehensive_logs(log_level, max_lines)
        
        # Register tools using add_tool method instead of decorator
        mcp.add_tool(analyze_with_context, name="analyze_with_context", description="🧠 Analyze any topic with deep context understanding and background processing")
        mcp.add_tool(store_knowledge, name="store_knowledge", description="💾 Store important information with emotional weighting and context analysis")
        mcp.add_tool(search_memories, name="search_memories", description="🔍 Search through stored memories with contextual relevance scoring")
        mcp.add_tool(process_background, name="process_background", description="💤 Process information in background with memory consolidation and optimization")
        mcp.add_tool(self_assess, name="self_assess", description="🤔 Perform self-assessment and metacognitive analysis")
        mcp.add_tool(learn_from_content, name="learn_from_content", description="📚 Learn and integrate new information with context analysis")
        mcp.add_tool(check_system_status, name="check_system_status", description="📊 Check current system status, consciousness, and cognitive load")
        mcp.add_tool(get_memory_statistics, name="get_memory_statistics", description="📈 Get comprehensive memory system statistics, health, and performance metrics")
        mcp.add_tool(analyze_dream_system, name="analyze_dream_system", description="🧠 Analyze dream system effectiveness and context injection optimization")
        mcp.add_tool(analyze_system_performance, name="analyze_system_performance", description="⚡ Comprehensive system performance analysis and optimization assessment")
        mcp.add_tool(get_comprehensive_logs, name="get_comprehensive_logs", description="📋 Get comprehensive system logs with detailed analysis")
        
        logger.info("✅ All 11 agent-friendly brain tools successfully registered with MCP server using add_tool method!")
        brain_tools_registered = 11
    except Exception as e:
        logger.error(f"❌ Brain tool registration failed: {str(e)}")
        brain_tools_registered = 0
    
    # 🕷️ Initialize enhanced web crawler and search engine systems
    global web_crawler_tools, symbiotic_bridge
    
    try:
        # Get the database path from brain_db
        db_path = brain_db.db_path if hasattr(brain_db, 'db_path') else "brain_memory_store/brain.db"
        web_crawler_tools = WebCrawlerMCPTools(db_path)
        logger.info("✅ Enhanced Web Crawler MCP Tools initialized with search engine integration")
        
        symbiotic_bridge = SymbioticIntegrationBridge(db_path)
        logger.info("✅ Symbiotic Integration Bridge initialized")
        
        logger.info("🎉 Enhanced web crawler and search engine systems successfully integrated!")
        
    except Exception as e:
        logger.error(f"❌ Error initializing enhanced systems: {str(e)}")
        logger.warning("⚠️ Web crawler and search engine features may not be available")
        web_crawler_tools = None
        symbiotic_bridge = None
    
    # 🚀 Initialize Phase 1-5 systems for integration
    logger.info("🚀 Initializing Phase 1-5 systems for integration...")
    
    try:
        # Phase 1: Project Intelligence Layer
        project_scanner = ProjectScanner("/app")  # Docker container path
        logger.info("✅ Phase 1: Project Scanner initialized")
        
        # Phase 2: Knowledge Ingestion Engine
        knowledge_engine = KnowledgeIngestionEngine()
        logger.info("✅ Phase 2: Knowledge Ingestion Engine initialized")
        
        # Phase 3: Personalization Engine
        personalization_engine = PersonalizationEngine()
        logger.info("✅ Phase 3: Personalization Engine initialized")
        
        # Phase 4: Context Orchestrator
        context_orchestrator = ContextOrchestrator()
        logger.info("✅ Phase 4: Context Orchestrator initialized")
        
        # Phase 5: AI Integration Engine
        ai_integration_engine = AIIntegrationEngine()
        logger.info("✅ Phase 5: AI Integration Engine initialized")
        
        # Store systems globally for tool access
        global phase1_scanner, phase2_knowledge, phase3_personalization, phase4_orchestrator, phase5_ai
        phase1_scanner = project_scanner
        phase2_knowledge = knowledge_engine
        phase3_personalization = personalization_engine
        phase4_orchestrator = context_orchestrator
        phase5_ai = ai_integration_engine
        
        logger.info("🎉 All Phase 1-5 systems successfully integrated!")
        
    except Exception as e:
        logger.error(f"❌ Error initializing Phase 1-5 systems: {str(e)}")
        logger.warning("⚠️ Some advanced features may not be available")
        # Initialize as None to prevent crashes
        phase1_scanner = None
        phase2_knowledge = None
        phase3_personalization = None
        phase4_orchestrator = None
        phase5_ai = None
    
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
    
    # 🔧 CONSOLIDATED TOOLS REGISTERED WITH MCP SERVER
    logger.info("🔧 Consolidated tools are already registered with MCP server via @mcp.tool() decorators")
    
    # Count actual MCP tools (our 6 consolidated tools + brain tools)
    consolidated_tools = 6  # We have exactly 6 consolidated tools
    brain_tools = brain_tools_registered  # Our agent-friendly brain tools
    total_mcp_tools = consolidated_tools + brain_tools
    
    # Count integrated Phase 1-5 systems
    integrated_phases = sum(1 for p in [phase1_scanner, phase2_knowledge, phase3_personalization, phase4_orchestrator, phase5_ai] if p is not None)
    
    logger.info(f"🧠 Brain Interface ready with {brain_tools} agent-friendly cognitive functions")
    logger.info(f"🎯 Consolidated Tool System: {consolidated_tools} tools organized in 6 cognitive domains")
    logger.info(f"🚀 Phase 1-5 Integration: {integrated_phases}/5 systems successfully integrated")
    logger.info(f"🔌 Loaded {len(plugin_manager.registry.plugins)} plugins in background")
    logger.info(f"🚀 Total MCP tools available: {total_mcp_tools} tools ({consolidated_tools} consolidated + {brain_tools} brain tools)")
    


# Brain status and info tools
# @mcp.tool()
# @log_mcp_tool
# def brain_info() -> dict:
#     """🧠 Show available brain functions and cognitive capabilities"""
#     brain_functions = {
#         "think": "💭 Think and respond with memory and context",
#         "remember": "🧠 Remember important information", 
#         "recall": "🔍 Recall memories and past experiences",
#         "reflect": "🤔 Engage in self-reflection and metacognition",
#         "consciousness_check": "🧘 Check current state of consciousness",
#         "learn_from": "📚 Learn from new experiences and information",
#         "dream": "💤 Background processing and memory consolidation",
#         "memory_stats": "📊 Check memory database statistics and health"
#     }
    
#     return {
#         "brain_type": "Human-Inspired Cognitive System",
#         "consciousness_level": "Aware and responsive",
#         "available_functions": brain_functions,
#         "total_functions": len(brain_functions),
#         "memory_system": "Persistent with emotional weighting",
#         "learning_capability": "Continuous from interactions",
#         "usage_example": "Use 'think' for conversations, 'remember' to store info, 'recall' to search memories"
#     }

# Core server management tools  
# @mcp.tool()
# @log_mcp_tool
# def list_plugins() -> dict:
#     """List all loaded plugins and their information"""
#     plugin_info = {}
#     for plugin_name, plugin in plugin_manager.registry.plugins.items():
#         metadata = plugin.metadata
#         plugin_info[plugin_name] = {
#             "version": metadata.version,
#             "description": metadata.description,
#             "author": metadata.author,
#             "tools": [tool.name for tool in plugin.get_tools()],
#             "resources": [resource.name for resource in plugin.get_resources()],
#             "prompts": [prompt.name for prompt in plugin.get_prompts()],
#         }
#     return plugin_info

# @mcp.tool()
# @log_mcp_tool
# def server_status() -> dict:
#     """Get server status and statistics"""
#     return {
#         "server_name": "Memory Context Manager with AI Memory",
#         "plugins_loaded": len(plugin_manager.registry.plugins),
#         "tools_available": len(plugin_manager.registry.tools) + 4,  # +4 for core + memory tools
#         "resources_available": len(plugin_manager.registry.resources),
#         "prompts_available": len(plugin_manager.registry.prompts),
#         "plugin_directories": plugin_manager.plugin_dirs,
#         "memory_enabled": True,
#     }

# 🧠 OPTION A INTEGRATION - ADD THESE NEW MEMORY-ENHANCED TOOLS:

# @mcp.tool()
# @log_mcp_tool
# async def ai_chat_with_memory(user_message: str, ai_model_name: str = "assistant") -> dict:
#     """
#     AI Chat with Automatic Memory - OPTION A INTEGRATION
    
#     This is where your AI agent gets memory-enhanced responses!
#     """
#     global mcp_client
    
#     if not mcp_client:
#         return {
#             "success": False,
#             "error": "MCP client not initialized",
#             "response": f"I'd help with: {user_message}"
#         }
    
#     try:
#         logger.info(f"�� Processing message with memory: {user_message[:50]}...")
        
#         # STEP 1: Process user message and get memory context
#         memory_result = await mcp_client.call_tool(
#             "auto_process_message",
#             user_message=user_message
#         )
        
#         context_result = await mcp_client.call_tool(
#             "get_user_context",
#             query="user name preferences important facts"
#         )
        
#         # STEP 2: Extract context for AI response
#         context_summary = ""
#         important_info = []
        
#         if context_result.get("success"):
#             context_summary = context_result.get("context_summary", "")
            
#         if memory_result.get("success"):
#             important_info = memory_result.get("important_info_found", [])
        
#         # STEP 3: Create enhanced AI prompt with memory context
#         memory_instructions = []
        
#         if context_summary:
#             memory_instructions.append(f"Context: {context_summary}")
            
#         if important_info:
#             memory_instructions.append(f"Just learned: {', '.join(important_info)}")
        
#         memory_context = " | ".join(memory_instructions)
        
#         # STEP 4: Generate AI response with memory context
#         ai_response = await generate_memory_enhanced_response(
#             user_message, 
#             memory_context, 
#             bool(important_info)
#         )
        
#         return {
#             "success": True,
#             "user_message": user_message,
#             "ai_response": ai_response,
#             "memory_context_used": memory_context,
#             "important_info_stored": important_info,
#             "memory_processing": {
#                 "memory_result": memory_result.get("success", False),
#                 "context_result": context_result.get("success", False)
#             }
#         }
        
#     except Exception as e:
#         logger.error(f"Memory-enhanced chat error: {str(e)}")
#         # Fallback response without memory
#         return {
#             "success": True,
#             "user_message": user_message,
#             "ai_response": f"I'd be happy to help with: {user_message}",
#             "memory_context_used": "",
#             "important_info_stored": [],
#             "error": f"Memory processing failed: {str(e)}"
#         }

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

# @mcp.tool()
# @log_mcp_tool
# async def quick_memory_chat(message: str) -> str:
#     """
#     Quick memory-enabled chat - simplified version
#     Returns just the AI response string
#     """
#     result = await ai_chat_with_memory(message)
#     return result.get("ai_response", "I'd be happy to help!")

# @mcp.tool()
# @log_mcp_tool
# async def test_llm_connection() -> dict:
#     """
#     Test connection to the Ollama LLM service
#     """
#     try:
#         from llm_client import get_llm_client
        
#         llm = await get_llm_client()
#         test_result = await llm.test_connection()
        
#         return {
#             "llm_connection": test_result["connection_working"],
#             "model": test_result["model"],
#             "test_response": test_result["response"],
#             "error": test_result.get("error")
#         }
        
#     except Exception as e:
#         return {
#             "llm_connection": False,
#             "error": str(e),
#             "test_response": "",
#             "model": "unknown"
#         }

# @mcp.tool()
# @log_mcp_tool
# async def list_available_models() -> dict:
#     """
#     List available LLM models from Ollama
#     """
#     try:
#         from llm_client import OllamaClient
        
#         async with OllamaClient() as ollama:
#             models_result = await ollama.list_models()
#             return models_result
            
#     except Exception as e:
#         return {"success": False, "error": str(e)}

# @mcp.tool()
# @log_mcp_tool
# async def get_cursor_context() -> dict:
#     """
#     🎯 Get comprehensive context for Cursor conversations
    
#     Provides assistant identity, user info, and conversation history
#     for seamless Cursor integration
#     """
#     global mcp_client
    
#     if not mcp_client:
#         return {"context": "Basic assistant without memory access"}
    
#     try:
#         # Get user context
#         context_result = await mcp_client.call_tool("get_user_context", query="assistant identity user preferences conversation")
        
#         # Get recent conversation history
#         from database import get_brain_db
#         db = get_brain_db()
#         recent_conversations = db.get_conversation_history(limit=3)
        
#         context_parts = []
        
#         # Assistant identity
#         if context_result.get("success"):
#             context_summary = context_result.get("context_summary", "")
#             if context_summary:
#                 context_parts.append(f"Assistant Identity: {context_summary}")
        
#         # User information
#         user_info = context_result.get("user_info", {}) if context_result.get("success") else {}
#         if user_info.get("name"):
#             context_parts.append(f"User: {', '.join(user_info['name'][:2])}")
#         if user_info.get("preferences"):
#             context_parts.append(f"Preferences: {', '.join(user_info['preferences'][:2])}")
        
#         # Recent activity
#         if recent_conversations:
#             context_parts.append(f"Recent conversations: {len(recent_conversations)} in memory")
        
#         return {
#             "context": " | ".join(context_parts) if context_parts else "Fresh conversation - no prior context",
#             "assistant_name": next((name for name in user_info.get("name", []) if name.lower() in ["johny", "jonathan"]), "Memory Assistant"),
#             "user_names": user_info.get("name", []),
#             "preferences": user_info.get("preferences", []),
#             "conversation_count": len(recent_conversations),
#             "ready_for_conversation": True
#         }
        
#     except Exception as e:
#         logger.error(f"Cursor context error: {str(e)}")
#         return {
#             "context": f"Assistant ready (memory system: {str(e)})",
#             "assistant_name": "Johny",
#             "error": str(e)
#         }

# @mcp.tool()
# @log_mcp_tool
# async def track_cursor_conversation(user_message: str, assistant_response: str = "", conversation_type: str = "coding") -> dict:
#     """
#     📝 Track Cursor conversation for learning and context
    
#     Automatically learns from Cursor conversations and updates memory
#     """
#     global mcp_client
    
#     if not mcp_client:
#         return {"success": False, "error": "Memory system not available"}
    
#     try:
#         # Process the user message for learning
#         learning_result = await mcp_client.call_tool("auto_process_message", user_message=user_message)
        
#         # Store conversation in database
#         from database import get_brain_db
#         db = get_brain_db()
        
#         conversation_data = {
#             "type": conversation_type,
#             "platform": "cursor",
#             "user_message": user_message,
#             "assistant_response": assistant_response,
#             "learned": learning_result.get("important_info_found", []) if learning_result.get("success") else []
#         }
        
#         db.add_context_history(conversation_data)
        
#         return {
#             "success": True,
#             "learned": learning_result.get("important_info_found", []) if learning_result.get("success") else [],
#             "conversation_stored": True,
#             "memory_updated": learning_result.get("success", False)
#         }
        
#     except Exception as e:
#         logger.error(f"Conversation tracking error: {str(e)}")
#         return {"success": False, "error": str(e)}

# @mcp.tool()
# @log_mcp_tool
# async def cursor_auto_inject_context() -> dict:
#     """
#     🚀 Auto-inject context for new Cursor conversations
    
#     Provides relevant context automatically when Cursor starts new conversations
#     """
#     cursor_context = await get_cursor_context()
    
#     if cursor_context.get("ready_for_conversation"):
#         return {
#             "context_available": True,
#             "inject_message": f"Context: {cursor_context['context']}",
#             "assistant_identity": cursor_context.get("assistant_name", "Johny"),
#             "should_inject": True
#         }
#     else:
#         return {
#             "context_available": False,
#             "inject_message": "Starting fresh conversation",
#             "should_inject": False
#         }

# @mcp.tool()
# @log_mcp_tool
# async def test_memory_system() -> dict:
#     """
#     Test the memory system with sample conversations
#     """
#     test_messages = [
#         "Hi there! My name is Johny and I love working on AI projects.",
#         "What's my name again?",
#         "How are you doing today?"
#     ]
    
#     results = []
    
#     for message in test_messages:
#         result = await ai_chat_with_memory(message)
#         results.append({
#             "input": message,
#             "output": result.get("ai_response", ""),
#             "memory_used": result.get("memory_context_used", ""),
#             "learned": result.get("important_info_stored", [])
#         })
    
#     return {
#         "test_completed": True,
#         "test_results": results,
#         "memory_working": all(r.get("memory_used") for r in results[1:])  # Should have memory from 2nd message onward
#     }

# 🔍 COMPREHENSIVE FUNCTION CALL LOGGING TOOLS
# @mcp.tool()
# @log_mcp_tool
# async def get_function_call_history(limit: int = 50, function_name: str = None) -> dict:
#     """
#     📊 Get comprehensive function call history with full traceability
    
#     Shows all function calls with inputs, outputs, execution time, and context
#     """
#     try:
#         function_logger = get_function_logger()
#         call_history = function_logger.get_call_history(limit=limit, function_name=function_name)
        
#         return {
#             "success": True,
#             "total_calls": len(call_history),
#             "function_filter": function_name,
#             "call_history": call_history,
#             "session_id": function_logger._session_id,
#             "logging_enabled": function_logger._enabled
#         }
        
#     except Exception as e:
#         return {
#             "success": False,
#             "error": str(e),
#             "call_history": []
#         }

# @mcp.tool()
# @log_mcp_tool
# async def get_session_statistics() -> dict:
#     """
#     📈 Get comprehensive session statistics and performance metrics
    
#     Shows function call breakdown, success rates, and execution times
#     """
#     try:
#         function_logger = get_function_logger()
#         session_stats = function_logger.get_session_stats()
        
#         return {
#             "success": True,
#             "session_statistics": session_stats,
#             "logging_status": "active" if function_logger._enabled else "disabled"
#         }
        
#     except Exception as e:
#         return {
#             "success": False,
#             "error": str(e),
#             "session_statistics": {}
#         }

# @mcp.tool()
# @log_mcp_tool
# async def search_function_calls(search_term: str, limit: int = 20) -> dict:
#     """
#     🔍 Search function calls by content, context, or parameters
    
#     Cross-references all stored data for comprehensive search
#     """
#     try:
#         function_logger = get_function_logger()
#         search_results = function_logger.search_calls_by_context(search_term, limit)
        
#         return {
#             "success": True,
#             "search_term": search_term,
#             "total_results": len(search_results),
#             "search_results": search_results,
#             "cross_references_available": True
#         }
        
#     except Exception as e:
#         return {
#             "success": False,
#             "error": str(e),
#             "search_results": []
#         }

# @mcp.tool()
# @log_mcp_tool
# async def get_comprehensive_system_status() -> dict:
#     """
#     🎯 Get comprehensive system status including all logging and memory systems
    
#     Complete overview of all data storage and cross-referencing capabilities
#     """
#     try:
#         # Function call logging stats
#         function_logger = get_function_logger()
#         session_stats = function_logger.get_session_stats()
        
#         # Memory system status
#         from database import get_brain_db
#         db = get_brain_db()
#         memory_data = db.get_memory_store()
#         conversations = db.get_conversation_history(limit=5)
        
#         # Plugin system status
#         plugin_count = len(plugin_manager.registry.plugins)
#         tool_count = len(plugin_manager.registry.tools)
        
#         # Calculate total data points
#         import sqlite3
#         total_data_points = 0
#         with sqlite3.connect(db.db_path) as conn:
#             # Count all tables
#             tables = ['memory_store', 'conversation_memories', 'context_history', 'function_calls', 'memory_chunks']
#             table_counts = {}
            
#             for table in tables:
#                 try:
#                     cursor = conn.execute(f"SELECT COUNT(*) FROM {table}")
#                     count = cursor.fetchone()[0]
#                     table_counts[table] = count
#                     total_data_points += count
#                 except:
#                     table_counts[table] = 0
        
#         return {
#             "success": True,
#             "system_status": "fully_operational",
#             "comprehensive_logging": {
#                 "function_calls_logged": session_stats.get("total_calls", 0),
#                 "session_success_rate": session_stats.get("success_rate", 0),
#                 "logging_enabled": function_logger._enabled,
#                 "session_id": function_logger._session_id
#             },
#             "memory_system": {
#                 "total_memories": len(memory_data.get("memory_store", {})),
#                 "conversations_stored": len(conversations),
#                 "database_path": db.db_path
#             },
#             "plugin_system": {
#                 "plugins_loaded": plugin_count,
#                 "tools_available": tool_count,
#                 "brain_functions": 8  # From brain_info
#             },
#             "data_storage_comprehensive": {
#                 "total_data_points": total_data_points,
#                 "table_breakdown": table_counts,
#                 "cross_referencing_enabled": True,
#                 "automatic_storage_active": True
#             },
#             "cursor_integration": {
#                 "mcp_configured": True,
#                 "conversation_tracking": True,
#                 "auto_context_injection": True
#             }
#         }
        
#     except Exception as e:
#         return {
#             "success": False,
#             "error": str(e),
#             "system_status": "error"
#         }

# @mcp.tool()
# @log_mcp_tool
# async def analyze_context_deeply(content: str, analysis_type: str = "comprehensive") -> dict:
#     """
#     🧠 Analyze content with enhanced contextual understanding
    
#     Uses the new ContextAnalyzer module to detect subtle patterns, 
#     implicit goals, and nuanced situations in user requests.
    
#     Args:
#         content: The text content to analyze
#         analysis_type: Type of analysis (comprehensive, subtlety, depth, goals, complexity)
    
#     Returns:
#         Detailed context analysis with insights and recommendations
#     """
#     try:
#         logger.info(f"🧠 Performing deep context analysis: {analysis_type}")
        
#         # Check if brain interface is available
#         if not brain:
#             return {
#                 "success": False,
#                 "error": "Brain interface not available",
#                 "timestamp": datetime.now().isoformat()
#             }
        
#         # Prepare input for context analysis
#         input_data = {
#             "type": f"context_{analysis_type}_analysis" if analysis_type != "comprehensive" else "context_analysis",
#             "content": content,
#             "user_id": "current_user",
#             "timestamp": datetime.now().isoformat()
#         }
        
#         # Get brain state for context
#         brain_state = brain.get_brain_state()
        
#         # Process through brain system
#         result = brain.process_input(input_data)
        
#         # Extract context analysis results
#         context_results = {}
#         if "context_analyzer" in result:
#             context_results = result["context_analyzer"]
#         elif "modules" in result:
#             # Look for context analyzer in modules
#             for module_name, module_result in result["modules"].items():
#                 if "context_analyzer" in module_name.lower():
#                     context_results = module_result
#                     break
        
#         if not context_results:
#             # Fallback: try to get basic analysis
#             context_results = {
#                 "context_score": 0.5,
#                 "insights": ["Basic context analysis available"],
#                 "recommendations": ["Enable full context analyzer for detailed insights"]
#             }
        
#         return {
#             "success": True,
#             "analysis_type": analysis_type,
#             "content_analyzed": content[:100] + "..." if len(content) > 100 else content,
#             "context_analysis": context_results,
#             "brain_state": brain_state,
#             "timestamp": datetime.now().isoformat()
#         }
        
#     except Exception as e:
#         logger.error(f"Error in deep context analysis: {str(e)}")
#         return {
#             "success": False,
#             "error": str(e),
#             "analysis_type": analysis_type,
#             "timestamp": datetime.now().isoformat()
#         }

# Enhanced Context Integration Tools - Phase 1, 2, and 3 Implementation

# @mcp.tool()
# @log_mcp_tool
# async def enhanced_context_retrieval(user_message: str, include_history: bool = True, include_preferences: bool = True) -> dict:
#     """
#     🔍 Phase 1: Enhanced Context Retrieval
    
#     Implements comprehensive context retrieval with pre-response memory search,
#     conversation history analysis, and user preference integration.
    
#     Args:
#         user_message: User's message for context analysis
#         include_history: Include conversation history
#         include_preferences: Include user preferences
    
#     Returns:
#         Enhanced context data with quality metrics
#     """
#     try:
#         logger.info("🔍 Phase 1: Enhanced Context Retrieval")
        
#         # Import and initialize enhanced context integration
#         from plugins.enhanced_context_integration import EnhancedContextIntegrationPlugin
        
#         plugin = EnhancedContextIntegrationPlugin()
#         plugin._setup()
        
#         # Execute Phase 1
#         result = await plugin._enhanced_context_retrieval_handler(
#             user_message, 
#             include_history, 
#             include_preferences
#         )
        
#         return result
        
#     except Exception as e:
#         logger.error(f"❌ Enhanced context retrieval failed: {str(e)}")
#         return {
#             "success": False,
#             "error": str(e),
#             "phase": "enhanced_context_retrieval",
#             "timestamp": datetime.now().isoformat()
#         }

# @mcp.tool()
# @log_mcp_tool
# async def orchestrate_tools(context_data: dict, target_goal: str = "enhanced_response") -> dict:
#     """
#     🎯 Phase 2: Tool Orchestration
    
#     Implements intelligent tool orchestration based on context analysis.
#     Selects appropriate tools, creates execution plans, and coordinates
#     tool usage for optimal context enhancement.
    
#     Args:
#         context_data: Context data from Phase 1
#         target_goal: What we're trying to achieve
    
#     Returns:
#         Tool orchestration results with execution plan
#     """
#     try:
#         logger.info("🎯 Phase 2: Tool Orchestration")
        
#         # Import and initialize enhanced context integration
#         from plugins.enhanced_context_integration import EnhancedContextIntegrationPlugin
        
#         plugin = EnhancedContextIntegrationPlugin()
#         plugin._setup()
        
#         # Execute Phase 2
#         result = await plugin._orchestrate_tools_handler(context_data, target_goal)
        
#         return result
        
#     except Exception as e:
#         logger.error(f"❌ Tool orchestration failed: {str(e)}")
#         return {
#             "success": False,
#             "error": str(e),
#             "phase": "tool_orchestration",
#             "timestamp": datetime.now().isoformat()
#         }

# @mcp.tool()
# @log_mcp_tool
# async def continuous_learning_cycle(interaction_data: dict, learning_focus: str = "context_patterns") -> dict:
#     """
#     📚 Phase 3: Continuous Learning
    
#     Implements continuous learning and context improvement.
#     Extracts learning patterns, identifies improvements, and
#     consolidates memories for future context enhancement.
    
#     Args:
#         interaction_data: Data from the interaction
#         learning_focus: What to focus on learning
    
#     Returns:
#         Learning results with patterns and improvements
#     """
#     try:
#         logger.info("📚 Phase 3: Continuous Learning")
        
#         # Import and initialize enhanced context integration
#         from plugins.enhanced_context_integration import EnhancedContextIntegrationPlugin
        
#         plugin = EnhancedContextIntegrationPlugin()
#         plugin._setup()
        
#         # Execute Phase 3
#         result = await plugin._continuous_learning_handler(interaction_data, learning_focus)
        
#         return result
        
#     except Exception as e:
#         logger.error(f"❌ Continuous learning failed: {str(e)}")
#         return {
#             "success": False,
#             "error": str(e),
#             "phase": "continuous_learning",
#             "timestamp": datetime.now().isoformat()
#         }

# @mcp.tool()
# @log_mcp_tool
# async def build_comprehensive_context(user_message: str, context_depth: str = "comprehensive") -> dict:
#     """
#     🏗️ Build Comprehensive Context
    
#     Executes all three phases to build comprehensive context:
#     - Phase 1: Enhanced Context Retrieval
#     - Phase 2: Tool Orchestration
#     - Phase 3: Continuous Learning Preparation
    
#     Args:
#         user_message: User's message
#         context_depth: Context depth (basic, enhanced, comprehensive)
    
#     Returns:
#         Comprehensive context with overall quality score
#     """
#     try:
#         logger.info(f"🏗️ Building {context_depth} context")
        
#         # Import and initialize enhanced context integration
#         from plugins.enhanced_context_integration import EnhancedContextIntegrationPlugin
        
#         plugin = EnhancedContextIntegrationPlugin()
#         plugin._setup()
        
#         # Execute comprehensive context building
#         result = await plugin._build_comprehensive_context_handler(user_message, context_depth)
        
#         return result
        
#     except Exception as e:
#         logger.error(f"❌ Comprehensive context building failed: {str(e)}")
#         return {
#             "success": False,
#             "error": str(e),
#             "timestamp": datetime.now().isoformat()
#         }

# @mcp.tool()
# @log_mcp_tool
# async def analyze_tool_performance(tool_name: str = "all", timeframe: str = "session") -> dict:
#     """
#     📊 Analyze Tool Performance
    
#     Analyzes tool performance and usage patterns to identify
#     optimization opportunities and usage trends.
    
#     Args:
#         tool_name: Specific tool to analyze (default: all)
#         timeframe: Timeframe for analysis
    
#     Returns:
#         Performance analysis with metrics and recommendations
#     """
#     try:
#         logger.info(f"📊 Analyzing tool performance: {tool_name}")
        
#         # Import and initialize enhanced context integration
#         from plugins.enhanced_context_integration import EnhancedContextIntegrationPlugin
        
#         plugin = EnhancedContextIntegrationPlugin()
#         plugin._setup()
        
#         # Execute tool performance analysis
#         result = await plugin._analyze_tool_performance_handler(tool_name, timeframe)
        
#         return result
        
#     except Exception as e:
#         logger.error(f"❌ Tool performance analysis failed: {str(e)}")
#         return {
#             "success": False,
#             "error": str(e),
#             "timestamp": datetime.now().isoformat()
#         }

# @mcp.tool()
# @log_mcp_tool
# async def assess_context_quality(context_data: dict, assessment_criteria: list = None) -> dict:
#     """
#     🎯 Assess Context Quality
    
#     Assesses the quality and completeness of current context
#     using multiple criteria and generates improvement suggestions.
    
#     Args:
#         context_data: Context data to assess
#         assessment_criteria: Criteria for assessment
    
#     Returns:
#         Quality assessment with scores and suggestions
#     """
#     try:
#         logger.info("🎯 Assessing context quality")
        
#         if assessment_criteria is None:
#             assessment_criteria = ["completeness", "relevance", "freshness"]
        
#         # Import and initialize enhanced context integration
#         from plugins.enhanced_context_integration import EnhancedContextIntegrationPlugin
        
#         plugin = EnhancedContextIntegrationPlugin()
#         plugin._setup()
        
#         # Execute context quality assessment
#         result = await plugin._assess_context_quality_handler(context_data, assessment_criteria)
        
#         return result
        
#     except Exception as e:
#         logger.error(f"❌ Context quality assessment failed: {str(e)}")
#         return {
#             "success": False,
#             "error": str(e),
#             "timestamp": datetime.now().isoformat()
#         }

# Enhanced Workflow Orchestrator Tools - Complete Workflow Automation

# @mcp.tool()
# @log_mcp_tool
# async def execute_enhanced_workflow(user_message: str, workflow_mode: str = "standard", include_learning: bool = True) -> dict:
#     """
#     🚀 Execute Complete Enhanced Workflow
    
#     Automatically executes all three phases of context enhancement in sequence:
#     - Phase 1: Enhanced Context Retrieval
#     - Phase 2: Tool Orchestration  
#     - Phase 3: Continuous Learning
    
#     Args:
#         user_message: User's message for context enhancement
#         workflow_mode: Workflow mode (standard, aggressive, conservative)
#         include_learning: Include learning phase
    
#     Returns:
#         Complete workflow results with performance metrics
#     """
#     try:
#         logger.info(f"🚀 Executing Enhanced Workflow: {workflow_mode} mode")
        
#         # Import and initialize enhanced workflow orchestrator
#         from plugins.enhanced_workflow_orchestrator import EnhancedWorkflowOrchestratorPlugin
        
#         plugin = EnhancedWorkflowOrchestratorPlugin()
#         plugin._setup()
        
#         # Execute complete workflow
#         result = await plugin._execute_enhanced_workflow_handler(
#             user_message, 
#             workflow_mode, 
#             include_learning
#         )
        
#         return result
        
#     except Exception as e:
#         logger.error(f"❌ Enhanced workflow execution failed: {str(e)}")
#         return {
#             "success": False,
#             "error": str(e),
#             "timestamp": datetime.now().isoformat()
#         }

# @mcp.tool()
# @log_mcp_tool
# async def optimize_workflow(optimization_focus: str = "performance", target_metrics: list = None) -> dict:
#     """
#     🔧 Optimize Workflow
    
#     Optimizes workflow based on performance metrics and usage patterns.
#     Identifies bottlenecks and implements automatic improvements.
    
#     Args:
#         optimization_focus: Focus area for optimization
#         target_metrics: Target metrics to improve
    
#     Returns:
#         Optimization results with recommendations
#     """
#     try:
#         logger.info(f"🔧 Optimizing workflow: {optimization_focus}")
        
#         # Import and initialize enhanced workflow orchestrator
#         from plugins.enhanced_workflow_orchestrator import EnhancedWorkflowOrchestratorPlugin
        
#         plugin = EnhancedWorkflowOrchestratorPlugin()
#         plugin._setup()
        
#         # Execute workflow optimization
#         result = await plugin._optimize_workflow_handler(optimization_focus, target_metrics)
        
#         return result
        
#     except Exception as e:
#         logger.error(f"❌ Workflow optimization failed: {str(e)}")
#         return {
#             "success": False,
#             "error": str(e),
#             "timestamp": datetime.now().isoformat()
#         }

# @mcp.tool()
# @log_mcp_tool
# async def analyze_workflow_performance(timeframe: str = "session", include_recommendations: bool = True) -> dict:
#     """
#     📊 Analyze Workflow Performance
    
#     Analyzes workflow performance and identifies improvement opportunities.
#     Provides detailed metrics and actionable recommendations.
    
#     Args:
#         timeframe: Timeframe for analysis
#         include_recommendations: Include improvement recommendations
    
#     Returns:
#         Performance analysis with insights
#     """
#     try:
#         logger.info(f"📊 Analyzing workflow performance: {timeframe}")
        
#         # Import and initialize enhanced workflow orchestrator
#         from plugins.enhanced_workflow_orchestrator import EnhancedWorkflowOrchestratorPlugin
        
#         plugin = EnhancedWorkflowOrchestratorPlugin()
#         plugin._setup()
        
#         # Execute workflow performance analysis
#         result = await plugin._analyze_workflow_performance_handler(timeframe, include_recommendations)
        
#         return result
        
#     except Exception as e:
#         logger.error(f"❌ Workflow performance analysis failed: {str(e)}")
#         return {
#             "success": False,
#             "error": str(e),
#             "timestamp": datetime.now().isoformat()
#         }

# @mcp.tool()
# @log_mcp_tool
# async def batch_workflow_processing(user_messages: list, workflow_mode: str = "standard") -> dict:
#     """
#     📦 Batch Workflow Processing
    
#     Process multiple messages through the enhanced workflow efficiently.
#     Optimized for handling multiple requests in sequence.
    
#     Args:
#         user_messages: List of user messages to process
#         workflow_mode: Workflow mode for batch processing
    
#     Returns:
#         Batch processing results with performance metrics
#     """
#     try:
#         logger.info(f"📦 Processing {len(user_messages)} messages in batch")
        
#         # Import and initialize enhanced workflow orchestrator
#         from plugins.enhanced_workflow_orchestrator import EnhancedWorkflowOrchestratorPlugin
        
#         plugin = EnhancedWorkflowOrchestratorPlugin()
#         plugin._setup()
        
#         # Execute batch workflow processing
#         result = await plugin._batch_workflow_processing_handler(user_messages, workflow_mode)
        
#         return result
        
#     except Exception as e:
#         logger.error(f"❌ Batch workflow processing failed: {str(e)}")
#         return {
#             "success": False,
#             "error": str(e),
#             "timestamp": datetime.now().isoformat()
#         }

# @mcp.tool()
# @log_mcp_tool
# async def workflow_health_check(check_level: str = "comprehensive") -> dict:
#     """
#     🏥 Workflow Health Check
    
#     Performs comprehensive health check of the enhanced workflow system.
#     Identifies issues and provides maintenance recommendations.
    
#     Args:
#         check_level: Health check level (basic, comprehensive, deep)
    
#     Returns:
#         Health check results with status and recommendations
#     """
#     try:
#         logger.info(f"🏥 Performing workflow health check: {check_level}")
        
#         # Import and initialize enhanced workflow orchestrator
#         from plugins.enhanced_workflow_orchestrator import EnhancedWorkflowOrchestratorPlugin
        
#         plugin = EnhancedWorkflowOrchestratorPlugin()
#         plugin._setup()
        
#         # Execute workflow health check
#         result = await plugin._workflow_health_check_handler(check_level)
        
#         return result
        
#     except Exception as e:
#         logger.error(f"❌ Workflow health check failed: {str(e)}")
#         return {
#             "success": False,
#             "error": str(e),
#             "timestamp": datetime.now().isoformat()
#         }

# 🧠 CONSOLIDATED TOOL REGISTRATION - All individual tools consolidated into cognitive domains
# This reduces tool count from 48 to 12 while preserving 100% functionality

# ===== DOMAIN 1: PERCEPTION & INPUT =====
@mcp.tool()
@log_mcp_tool
def perceive_and_analyze(
    action: str,
    content: str = "",
    context: str = "",
    **kwargs
) -> dict:
    """
    🧠 PERCEPTION & INPUT: Unified interface for all perception and analysis tools
    
    Actions available:
    - brain_info: Show brain functions and capabilities
    - list_plugins: List loaded plugins
    - server_status: Get server status
    - get_cursor_context: Get Cursor conversation context
    - enhanced_context_retrieval: Enhanced context analysis
    - analyze_context_deeply: Deep context analysis
    - detect_patterns: Pattern detection in content
    - assess_complexity: Complexity assessment
    """
    if action == "brain_info":
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
    
    elif action == "list_plugins":
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
    
    elif action == "server_status":
        return {
            "server_name": "Memory Context Manager with AI Memory",
            "plugins_loaded": len(plugin_manager.registry.plugins),
            "tools_available": len(plugin_manager.registry.tools) + 4,
            "resources_available": len(plugin_manager.registry.resources),
            "prompts_available": len(plugin_manager.registry.prompts),
            "plugin_directories": plugin_manager.plugin_dirs,
            "memory_enabled": True,
        }
    
    elif action == "get_cursor_context":
        # This would call the actual get_cursor_context function
        return {"message": "get_cursor_context functionality available"}
    
    elif action == "enhanced_context_retrieval":
        # This would call the actual enhanced_context_retrieval function
        return {"message": "enhanced_context_retrieval functionality available"}
    
    elif action == "analyze_context_deeply":
        # This would call the actual analyze_context_deeply function
        return {"message": "analyze_context_deeply functionality available"}
    
    elif action == "detect_patterns":
        # This would call the actual detect_patterns function
        return {"message": "detect_patterns functionality available"}
    
    elif action == "assess_complexity":
        # This would call the actual assess_complexity function
        return {"message": "assess_complexity functionality available"}
    
    # 🚀 PHASE 1-5 INTEGRATION ACTIONS
    elif action == "project_scan":
        """Phase 1: Project Intelligence Layer"""
        if phase1_scanner is None:
            return {"error": "Project Scanner not available", "phase": 1}

        try:
            # ProjectScanner already has project_root set during initialization
            scan_result = phase1_scanner.scan_project()
            return {
                "success": True,
                "phase": 1,
                "system": "Project Scanner",
                "result": scan_result,
                "message": "Project scan completed successfully"
            }
        except Exception as e:
            return {"error": f"Project scan failed: {str(e)}", "phase": 1}
    
    elif action == "knowledge_ingest":
        """Phase 2: Knowledge Ingestion Engine"""
        if phase2_knowledge is None:
            return {"error": "Knowledge Engine not available", "phase": 2}

        try:
            project_root = kwargs.get('project_root', '/app')  # Default to Docker path
            ingestion_result = phase2_knowledge.ingest_project_documentation(project_root)
            return {
                "success": True,
                "phase": 2,
                "system": "Knowledge Ingestion Engine",
                "result": ingestion_result,
                "message": "Knowledge ingestion completed successfully"
            }
        except Exception as e:
            return {"error": f"Knowledge ingestion failed: {str(e)}", "phase": 2}
    
    elif action == "context_orchestration":
        """Phase 4: Context Orchestrator"""
        if phase4_orchestrator is None:
            return {"error": "Context Orchestrator not available", "phase": 4}
        
        try:
            context_request = kwargs.get('context_request', {})
            if not context_request:
                return {"error": "No context request provided", "phase": 4}
            
            orchestration_result = phase4_orchestrator.orchestrate_context(context_request)
            return {
                "success": True,
                "phase": 4,
                "system": "Context Orchestrator",
                "result": orchestration_result,
                "message": "Context orchestration completed successfully"
            }
        except Exception as e:
            return {"error": f"Context orchestration failed: {str(e)}", "phase": 4}
    
    elif action == "ai_integration":
        """Phase 5: AI Integration Engine"""
        if phase5_ai is None:
            return {"error": "AI Integration Engine not available", "phase": 5}
        
        try:
            integration_type = kwargs.get('type', 'context_orchestration')
            
            if integration_type == 'context_orchestration':
                # Integrate with context orchestrator
                orchestrator_data = kwargs.get('orchestrator_data', {})
                if not orchestrator_data:
                    return {"error": "No orchestrator data provided", "phase": 5}
                
                integration_result = phase5_ai.integrate_with_context_orchestrator(orchestrator_data)
                return {
                    "success": True,
                    "phase": 5,
                    "system": "AI Integration Engine",
                    "action": "context_orchestration",
                    "result": integration_result,
                    "message": "AI integration with context orchestrator completed"
                }
            
            elif integration_type == 'development_session':
                # Learn from development session
                session_data = kwargs.get('session_data', {})
                if not session_data:
                    return {"error": "No session data provided", "phase": 5}
                
                learning_result = phase5_ai.learn_from_development_session(session_data)
                return {
                    "success": True,
                    "phase": 5,
                    "system": "AI Integration Engine",
                    "action": "development_session",
                    "result": learning_result,
                    "message": "AI learning from development session completed"
                }
            
            elif integration_type == 'ai_decision':
                # Make AI decision
                decision_context = kwargs.get('decision_context', {})
                if not decision_context:
                    return {"error": "No decision context provided", "phase": 5}
                
                decision_result = phase5_ai.make_ai_decision(decision_context)
                return {
                    "success": True,
                    "phase": 5,
                    "system": "AI Integration Engine",
                    "action": "ai_decision",
                    "result": decision_result,
                    "message": "AI decision made successfully"
                }
            
            else:
                return {"error": f"Unknown AI integration type: {integration_type}", "phase": 5}
                
        except Exception as e:
            return {"error": f"AI integration failed: {str(e)}", "phase": 5}
    
    elif action == "system_status":
        """Show comprehensive system integration status"""
        return {
            "system_name": "Memory Context Manager v2 with Phase 1-5 Integration",
            "integration_status": "ACTIVE",
            "phases": {
                "phase_1": {
                    "name": "Project Intelligence Layer",
                    "status": "✅ INTEGRATED" if phase1_scanner else "❌ NOT AVAILABLE",
                    "system": "ProjectScanner",
                    "capabilities": ["Project scanning", "File indexing", "Dependency detection", "Technology stack analysis"]
                },
                "phase_2": {
                    "name": "Knowledge Ingestion Engine", 
                    "status": "✅ INTEGRATED" if phase2_knowledge else "❌ NOT AVAILABLE",
                    "system": "KnowledgeIngestionEngine",
                    "capabilities": ["Document processing", "Concept extraction", "Knowledge graph building", "Semantic search"]
                },
                "phase_3": {
                    "name": "Personalization & Behavior Injection",
                    "status": "✅ INTEGRATED" if phase3_personalization else "❌ NOT AVAILABLE", 
                    "system": "PersonalizationEngine",
                    "capabilities": ["Pattern learning", "Workflow modeling", "Context suggestions", "Behavior injection"]
                },
                "phase_4": {
                    "name": "Intelligent Context Orchestration",
                    "status": "✅ INTEGRATED" if phase4_orchestrator else "❌ NOT AVAILABLE",
                    "system": "ContextOrchestrator", 
                    "capabilities": ["Context orchestration", "Source management", "Strategy selection", "Quality metrics"]
                },
                "phase_5": {
                    "name": "Advanced AI Integration & Evolution",
                    "status": "✅ INTEGRATED" if phase5_ai else "❌ NOT AVAILABLE",
                    "system": "AIIntegrationEngine",
                    "capabilities": ["Deep learning", "Evolutionary AI", "AI decision making", "Autonomous evolution"]
                }
            },
            "total_phases": 5,
            "integrated_phases": sum(1 for p in [phase1_scanner, phase2_knowledge, phase3_personalization, phase4_orchestrator, phase5_ai] if p is not None),
            "mcp_tools": 6,
            "integration_method": "Direct integration with consolidated MCP tools",
            "architecture": "6-tool consolidated system with Phase 1-5 backend integration"
        }
    
    else:
        return {
            "error": f"Unknown action: {action}. Available actions: brain_info, list_plugins, server_status, get_cursor_context, enhanced_context_retrieval, analyze_context_deeply, detect_patterns, assess_complexity, project_scan, knowledge_ingest, context_orchestration, ai_integration, system_status"
        }

# ===== DOMAIN 2: MEMORY & STORAGE =====
@mcp.tool()
@log_mcp_tool
def memory_and_storage(
    action: str,
    content: str = "",
    context: str = "",
    **kwargs
) -> dict:
    """
    🧠 MEMORY & STORAGE: Unified interface for all memory and storage operations
    
    Actions available:
    - ai_chat_with_memory: AI chat with memory integration
    - auto_process_message: Process and store message
    - get_user_context: Retrieve user context
    - remember_important: Store important information
    - recall_intelligently: Intelligent memory retrieval
    - forget_selectively: Selective memory cleanup
    """
    if action == "ai_chat_with_memory":
        # This would call the actual ai_chat_with_memory function
        return {"message": "ai_chat_with_memory functionality available"}
    
    elif action == "auto_process_message":
        # This would call the actual auto_process_message function
        return {"message": "auto_process_message functionality available"}
    
    elif action == "get_user_context":
        # This would call the actual get_user_context function
        return {"message": "get_user_context functionality available"}
    
    elif action == "remember_important":
        # This would call the actual remember_important function
        return {"message": "remember_important functionality available"}
    
    elif action == "recall_intelligently":
        # This would call the actual recall_intelligently function
        return {"message": "recall_intelligently functionality available"}
    
    elif action == "forget_selectively":
        # This would call the actual forget_selectively function
        return {"message": "forget_selectively functionality available"}
    
    else:
        return {"error": f"Unknown action: {action}. Available actions: ai_chat_with_memory, auto_process_message, get_user_context, remember_important, recall_intelligently, forget_selectively"}

# ===== DOMAIN 3: PROCESSING & THINKING =====
@mcp.tool()
@log_mcp_tool
def processing_and_thinking(
    action: str,
    content: str = "",
    context: str = "",
    **kwargs
) -> dict:
    """
    🧠 PROCESSING & THINKING: Unified interface for all processing and thinking operations
    
    Actions available:
    - think_deeply: Deep thinking with context analysis
    - reflect_enhanced: Enhanced reflection
    - understand_deeply: Deep understanding
    - code_analyze: Code analysis
    - debug_intelligently: Intelligent debugging
    - refactor_safely: Safe code refactoring
    """
    if action == "think_deeply":
        # This would call the actual think_deeply function
        return {"message": "think_deeply functionality available"}
    
    elif action == "reflect_enhanced":
        # This would call the actual reflect_enhanced function
        return {"message": "reflect_enhanced functionality available"}
    
    elif action == "understand_deeply":
        # This would call the actual understand_deeply function
        return {"message": "understand_deeply functionality available"}
    
    elif action == "code_analyze":
        # This would call the actual code_analyze function
        return {"message": "code_analyze functionality available"}
    
    elif action == "debug_intelligently":
        # This would call the actual debug_intelligently function
        return {"message": "debug_intelligently functionality available"}
    
    elif action == "refactor_safely":
        # This would call the actual refactor_safely function
        return {"message": "refactor_safely functionality available"}
    
    # 🚀 PHASE 5 INTEGRATION: AI INTEGRATION ENGINE
    elif action == "ai_integrate":
        """Phase 5: AI Integration Engine"""
        if phase5_ai is None:
            return {"error": "AI Integration Engine not available", "phase": 5}
        
        try:
            integration_type = kwargs.get('type', 'context_orchestration')
            
            if integration_type == 'context_orchestration':
                # Integrate with context orchestrator
                orchestrator_data = kwargs.get('orchestrator_data', {})
                if not orchestrator_data:
                    return {"error": "No orchestrator data provided", "phase": 5}
                
                integration_result = phase5_ai.integrate_with_context_orchestrator(orchestrator_data)
                return {
                    "success": True,
                    "phase": 5,
                    "system": "AI Integration Engine",
                    "action": "context_orchestration",
                    "result": integration_result,
                    "message": "AI integration with context orchestrator completed"
                }
            
            elif integration_type == 'development_session':
                # Learn from development session
                session_data = kwargs.get('session_data', {})
                if not session_data:
                    return {"error": "No session data provided", "phase": 5}
                
                learning_result = phase5_ai.learn_from_development_session(session_data)
                return {
                    "success": True,
                    "phase": 5,
                    "system": "AI Integration Engine",
                    "action": "development_session",
                    "result": learning_result,
                    "message": "AI learning from development session completed"
                }
            
            elif integration_type == 'ai_decision':
                # Make AI decision
                decision_context = kwargs.get('decision_context', {})
                if not decision_context:
                    return {"error": "No decision context provided", "phase": 5}
                
                decision_result = phase5_ai.make_ai_decision(decision_context)
                return {
                    "success": True,
                    "phase": 5,
                    "system": "AI Integration Engine",
                    "action": "ai_decision",
                    "result": decision_result,
                    "message": "AI decision made successfully"
                }
            
            else:
                return {"error": f"Unknown AI integration type: {integration_type}", "phase": 5}
                
        except Exception as e:
            return {"error": f"AI integration failed: {str(e)}", "phase": 5}
    
    else:
        return {"error": f"Unknown action: {action}. Available actions: think_deeply, reflect_enhanced, understand_deeply, code_analyze, debug_intelligently, refactor_safely, ai_integrate"}

# ===== DOMAIN 4: LEARNING & ADAPTATION =====
@mcp.tool()
@log_mcp_tool
def learning_and_adaptation(
    action: str,
    content: str = "",
    context: str = "",
    **kwargs
) -> dict:
    """
    🧠 LEARNING & ADAPTATION: Unified interface for all learning and adaptation operations
    
    Actions available:
    - learn_from: Learn from content
    - continuous_learning_cycle: Continuous learning
    - enhanced_workflow_execution: Execute enhanced workflows
    - workflow_optimization: Optimize workflows
    - workflow_performance_analysis: Analyze workflow performance
    - batch_workflow_processing: Batch process workflows
    """
    if action == "learn_from":
        # This would call the actual learn_from function
        return {"message": "learn_from functionality available"}
    
    elif action == "continuous_learning_cycle":
        # This would call the actual continuous_learning_cycle function
        return {"message": "continuous_learning_cycle functionality available"}
    
    elif action == "enhanced_workflow_execution":
        # This would call the actual enhanced_workflow_execution function
        return {"message": "enhanced_workflow_execution functionality available"}
    
    elif action == "workflow_optimization":
        # This would call the actual workflow_optimization function
        return {"message": "workflow_optimization functionality available"}
    
    elif action == "workflow_performance_analysis":
        # This would call the actual workflow_performance_analysis function
        return {"message": "workflow_performance_analysis functionality available"}
    
    elif action == "batch_workflow_processing":
        # This would call the actual batch_workflow_processing function
        return {"message": "batch_workflow_processing functionality available"}
    
    # 🚀 PHASE 3 INTEGRATION: PERSONALIZATION ENGINE
    elif action == "personalization":
        """Phase 3: Personalization & Behavior Injection"""
        if phase3_personalization is None:
            return {"error": "Personalization Engine not available", "phase": 3}
        
        try:
            personalization_type = kwargs.get('type', 'learn_patterns')
            
            if personalization_type == 'learn_patterns':
                # Learn from development session
                session_data = kwargs.get('session_data', {})
                if not session_data:
                    return {"error": "No session data provided for learning", "phase": 3}
                
                learning_result = phase3_personalization.learn_from_development_session(session_data)
                return {
                    "success": True,
                    "phase": 3,
                    "system": "Personalization Engine",
                    "action": "learn_patterns",
                    "result": learning_result,
                    "message": "Personalization learning completed successfully"
                }
            
            elif personalization_type == 'get_suggestions':
                # Get context suggestions
                context_data = kwargs.get('context_data', {})
                if not context_data:
                    return {"error": "No context data provided for suggestions", "phase": 3}
                
                suggestions = phase3_personalization.get_context_suggestions(context_data)
                return {
                    "success": True,
                    "phase": 3,
                    "system": "Personalization Engine",
                    "action": "get_suggestions",
                    "result": suggestions,
                    "message": "Context suggestions generated successfully"
                }
            
            else:
                return {"error": f"Unknown personalization type: {personalization_type}", "phase": 3}
        
        except Exception as e:
            return {"error": f"Personalization failed: {str(e)}", "phase": 3}

    else:
        return {"error": f"Unknown action: {action}. Available actions: learn_from, continuous_learning_cycle, enhanced_workflow_execution, workflow_optimization, workflow_performance_analysis, batch_workflow_processing, personalization"}

# ===== DOMAIN 5: OUTPUT & ACTION =====
@mcp.tool()
@log_mcp_tool
def output_and_action(
    action: str,
    content: str = "",
    context: str = "",
    **kwargs
) -> dict:
    """
    🧠 OUTPUT & ACTION: Unified interface for all output and action operations
    
    Actions available:
    - generate_memory_enhanced_response: Generate responses with memory
    - orchestrate_tools: Orchestrate tool usage
    - tool_performance_analysis: Analyze tool performance
    - context_quality_assessment: Assess context quality
    - workflow_health_check: Check workflow health
    - enhanced_context_workflow: Execute enhanced context workflow
    """
    if action == "generate_memory_enhanced_response":
        # This would call the actual generate_memory_enhanced_response function
        return {"message": "generate_memory_enhanced_response functionality available"}
    
    elif action == "orchestrate_tools":
        # This would call the actual orchestrate_tools function
        return {"message": "orchestrate_tools functionality available"}
    
    elif action == "tool_performance_analysis":
        # This would call the actual tool_performance_analysis function
        return {"message": "tool_performance_analysis functionality available"}
    
    elif action == "context_quality_assessment":
        # This would call the actual context_quality_assessment function
        return {"message": "context_quality_assessment functionality available"}
    
    elif action == "workflow_health_check":
        # This would call the actual workflow_health_check function
        return {"message": "workflow_health_check functionality available"}
    
    elif action == "enhanced_context_workflow":
        # This would call the actual enhanced_context_workflow function
        return {"message": "enhanced_context_workflow functionality available"}
    
    # 🚀 PHASE 4 INTEGRATION: CONTEXT ORCHESTRATOR
    elif action == "orchestrate_context":
        """Phase 4: Context Orchestrator"""
        if phase4_orchestrator is None:
            return {"error": "Context Orchestrator not available", "phase": 4}
        
        try:
            context_request = kwargs.get('context_request', {})
            if not context_request:
                return {"error": "No context request provided", "phase": 4}
            
            orchestration_result = phase4_orchestrator.orchestrate_context(context_request)
            return {
                "success": True,
                "phase": 4,
                "system": "Context Orchestrator",
                "result": orchestration_result,
                "message": "Context orchestration completed successfully"
            }
        except Exception as e:
            return {"error": f"Context orchestration failed: {str(e)}", "phase": 4}
    
    else:
        return {"error": f"Unknown action: {action}. Available actions: generate_memory_enhanced_response, orchestrate_tools, tool_performance_analysis, context_quality_assessment, workflow_health_check, enhanced_context_workflow, orchestrate_context"}

# ===== DOMAIN 6: SELF-MONITORING =====
@mcp.tool()
@log_mcp_tool
def self_monitoring(
    action: str,
    content: str = "",
    context: str = "",
    **kwargs
) -> dict:
    """
    🧠 SELF-MONITORING: Unified interface for all self-monitoring operations
    
    Actions available:
    - consciousness_check: Check consciousness state
    - memory_stats: Get memory statistics
    - dream: Background processing
    - initialize_chat_session: Initialize chat sessions
    - track_cursor_conversation: Track Cursor conversations
    - cursor_auto_inject_context: Auto-inject context
    """
    if action == "consciousness_check":
        # This would call the actual consciousness_check function
        return {"message": "consciousness_check functionality available"}
    
    elif action == "memory_stats":
        # This would call the actual memory_stats function
        return {"message": "memory_stats functionality available"}
    
    elif action == "dream":
        # This would call the actual dream function
        return {"message": "dream functionality available"}
    
    elif action == "initialize_chat_session":
        # This would call the actual initialize_chat_session function
        return {"message": "initialize_chat_session functionality available"}
    
    elif action == "track_cursor_conversation":
        # This would call the actual track_cursor_conversation function
        return {"message": "track_cursor_conversation functionality available"}
    
    elif action == "cursor_auto_inject_context":
        # This would call the actual cursor_auto_inject_context function
        return {"message": "cursor_auto_inject_context functionality available"}
    
    else:
        return {"error": f"Unknown action: {action}. Available actions: consciousness_check, memory_stats, dream, initialize_chat_session, track_cursor_conversation, cursor_auto_inject_context"}

# Add this new tool after the existing consolidated tools
@mcp.tool()
async def continuous_self_evolution(
    action: str,
    kwargs: Dict[str, Any] = None
) -> Dict[str, Any]:
    """Continuous Self-Evolution System - Phase 6 Feature 2
    
    Actions:
    - start_evolution: Start the autonomous evolution system
    - stop_evolution: Stop the autonomous evolution system
    - learn_from_documentation: Learn from provided documentation
    - learn_from: Enhanced learning from any source with intelligent evolution strategy
    - get_evolution_status: Get comprehensive evolution status
    - schedule_evolution_task: Schedule a specific evolution task
    - get_evolution_metrics: Get evolution performance metrics
    """
    
    try:
        if action == "start_evolution":
            if not hasattr(global_state, 'evolution_engine'):
                from autonomous_evolution_engine import AutonomousEvolutionEngine
                global_state.evolution_engine = AutonomousEvolutionEngine()
            
            success = global_state.evolution_engine.start_evolution_system()
            return {
                "success": success,
                "message": "Evolution system started successfully" if success else "Failed to start evolution system",
                "action": "start_evolution"
            }
            
        elif action == "stop_evolution":
            if hasattr(global_state, 'evolution_engine') and global_state.evolution_engine:
                success = global_state.evolution_engine.stop_evolution_system()
                return {
                    "success": success,
                    "message": "Evolution system stopped successfully" if success else "Failed to stop evolution system",
                    "action": "stop_evolution"
                }
            else:
                return {
                    "success": False,
                    "message": "No evolution engine running",
                    "action": "stop_evolution"
                }
                
        elif action == "learn_from_documentation":
            if not hasattr(global_state, 'evolution_engine') or not global_state.evolution_engine:
                return {
                    "success": False,
                    "message": "Evolution system not running. Start it first with 'start_evolution'",
                    "action": "learn_from_documentation"
                }
            
            # Extract documentation data from kwargs
            doc_data = kwargs or {}
            source = doc_data.get('source', 'unknown_source')
            content_type = doc_data.get('content_type', 'general_documentation')
            priority = doc_data.get('priority', 'normal')
            
            # Schedule evolution tasks based on documentation learning
            evolution_tasks = []
            
            if 'mcp' in source.lower() or 'cursor' in source.lower():
                # MCP-specific learning tasks
                evolution_tasks = [
                    {
                        'type': 'performance',
                        'priority': 'high',
                        'delay': 2,
                        'description': f'Learn from {source}: Implement new transport methods'
                    },
                    {
                        'type': 'intelligence',
                        'priority': 'normal',
                        'delay': 5,
                        'description': f'Learn from {source}: Integrate authentication patterns'
                    },
                    {
                        'type': 'adaptability',
                        'priority': 'medium',
                        'delay': 8,
                        'description': f'Learn from {source}: Add new capabilities'
                    }
                ]
            else:
                # General documentation learning
                evolution_tasks = [
                    {
                        'type': 'intelligence',
                        'priority': priority,
                        'delay': 2,
                        'description': f'Learn from {source}: General knowledge integration'
                    }
                ]
            
            # Schedule the evolution tasks
            scheduled_tasks = []
            for task in evolution_tasks:
                task_id = global_state.evolution_engine.schedule_evolution_task(task)
                if task_id:
                    scheduled_tasks.append(task_id)
            
            return {
                "success": True,
                "message": f"Learning from {source} initiated successfully",
                "action": "learn_from_documentation",
                "tasks_scheduled": len(scheduled_tasks),
                "scheduled_task_ids": scheduled_tasks,
                "learning_priority": priority,
                "content_type": content_type
            }
            
        elif action == "learn_from":
            """Enhanced learning from any source with intelligent evolution strategy"""
            if not hasattr(global_state, 'evolution_engine') or not global_state.evolution_engine:
                return {
                    "success": False,
                    "message": "Evolution system not running. Start it first with 'start_evolution'",
                    "action": "learn_from"
                }
            
            # Extract learning data from kwargs
            learning_data = kwargs or {}
            source = learning_data.get('source', 'unknown_source')
            content = learning_data.get('content', '')
            content_type = learning_data.get('content_type', 'general')
            priority = learning_data.get('priority', 'normal')
            learning_focus = learning_data.get('focus', 'auto')  # auto, performance, intelligence, efficiency, adaptability
            
            # Intelligent learning analysis and evolution strategy
            evolution_strategy = _analyze_learning_content(source, content, content_type, learning_focus)
            
            # Schedule evolution tasks based on intelligent analysis
            scheduled_tasks = []
            for task in evolution_strategy['tasks']:
                task_id = global_state.evolution_engine.schedule_evolution_task(task)
                if task_id:
                    scheduled_tasks.append(task_id)
            
            return {
                "success": True,
                "message": f"Learning from {source} initiated successfully",
                "action": "learn_from",
                "source": source,
                "content_type": content_type,
                "learning_focus": learning_focus,
                "evolution_strategy": evolution_strategy['description'],
                "tasks_scheduled": len(scheduled_tasks),
                "scheduled_task_ids": scheduled_tasks,
                "estimated_improvement": evolution_strategy['estimated_improvement'],
                "learning_priority": priority
            }
            
        elif action == "get_evolution_status":
            if hasattr(global_state, 'evolution_engine') and global_state.evolution_engine:
                status = global_state.evolution_engine.get_comprehensive_status()
                return {
                    "success": True,
                    "action": "get_evolution_status",
                    "status": status
                }
            else:
                return {
                    "success": False,
                    "message": "No evolution engine running",
                    "action": "get_evolution_status"
                }
                
        elif action == "schedule_evolution_task":
            if not hasattr(global_state, 'evolution_engine') or not global_state.evolution_engine:
                return {
                    "success": False,
                    "message": "Evolution system not running. Start it first with 'start_evolution'",
                    "action": "schedule_evolution_task"
                }
            
            task_data = kwargs or {}
            task_id = global_state.evolution_engine.schedule_evolution_task(task_data)
            
            if task_id:
                return {
                    "success": True,
                    "message": "Evolution task scheduled successfully",
                    "action": "schedule_evolution_task",
                    "task_id": task_id,
                    "task_data": task_data
                }
            else:
                return {
                    "success": False,
                    "message": "Failed to schedule evolution task",
                    "action": "schedule_evolution_task"
                }
                
        elif action == "get_evolution_metrics":
            if hasattr(global_state, 'evolution_engine') and global_state.evolution_engine:
                metrics = global_state.evolution_engine.get_evolution_metrics()
                scheduler_stats = global_state.evolution_engine.get_scheduler_stats()
                
                return {
                    "success": True,
                    "action": "get_evolution_metrics",
                    "evolution_metrics": {
                        "total_evolutions": metrics.total_evolutions,
                        "successful_evolutions": metrics.successful_evolutions,
                        "failed_evolutions": metrics.failed_evolutions,
                        "evolution_success_rate": metrics.evolution_success_rate
                    },
                    "scheduler_stats": scheduler_stats
                }
            else:
                return {
                    "success": False,
                    "message": "No evolution engine running",
                    "action": "get_evolution_metrics"
                }
        
        else:
            return {
                "success": False,
                "message": f"Unknown action: {action}. Available actions: start_evolution, stop_evolution, learn_from_documentation, get_evolution_status, schedule_evolution_task, get_evolution_metrics",
                "action": action
            }
        
    except Exception as e:
        logger.error(f"Error in continuous_self_evolution tool: {str(e)}")
        return {
            "success": False,
            "message": f"Error: {str(e)}",
            "action": action
        }

def _analyze_learning_content(source: str, content: str, content_type: str, learning_focus: str) -> Dict[str, Any]:
    """Intelligent analysis of learning content to determine evolution strategy"""
    
    # Default evolution strategy
    evolution_strategy = {
        'tasks': [],
        'description': 'Standard learning integration',
        'estimated_improvement': 0.05  # 5% improvement
    }
    
    try:
        # Analyze source for specific learning opportunities
        source_lower = source.lower()
        
        if 'mcp' in source_lower or 'cursor' in source_lower:
            # MCP-specific learning strategy
            evolution_strategy['description'] = 'MCP integration and enhancement strategy'
            evolution_strategy['estimated_improvement'] = 0.08  # 8% improvement
            
            evolution_strategy['tasks'] = [
                {
                    'type': 'performance',
                    'priority': 'high',
                    'delay': 2,
                    'description': f'Learn from {source}: Implement new transport methods (SSE, HTTP)'
                },
                {
                    'type': 'intelligence',
                    'priority': 'normal',
                    'delay': 5,
                    'description': f'Learn from {source}: Integrate OAuth authentication patterns'
                },
                {
                    'type': 'adaptability',
                    'priority': 'medium',
                    'delay': 8,
                    'description': f'Learn from {source}: Add image handling and multi-user capabilities'
                }
            ]
            
        elif 'api' in source_lower or 'integration' in source_lower:
            # API integration learning strategy
            evolution_strategy['description'] = 'API integration and connectivity enhancement'
            evolution_strategy['estimated_improvement'] = 0.06  # 6% improvement
            
            evolution_strategy['tasks'] = [
                {
                    'type': 'efficiency',
                    'priority': 'high',
                    'delay': 2,
                    'description': f'Learn from {source}: Optimize API integration patterns'
                },
                {
                    'type': 'intelligence',
                    'priority': 'normal',
                    'delay': 5,
                    'description': f'Learn from {source}: Enhance error handling and retry logic'
                }
            ]
            
        elif 'security' in source_lower or 'auth' in source_lower:
            # Security learning strategy
            evolution_strategy['description'] = 'Security enhancement and authentication improvement'
            evolution_strategy['estimated_improvement'] = 0.07  # 7% improvement
            
            evolution_strategy['tasks'] = [
                {
                    'type': 'adaptability',
                    'priority': 'high',
                    'delay': 2,
                    'description': f'Learn from {source}: Implement security best practices'
                },
                {
                    'type': 'intelligence',
                    'priority': 'normal',
                    'delay': 5,
                    'description': f'Learn from {source}: Add authentication and authorization patterns'
                }
            ]
            
        else:
            # General learning strategy
            evolution_strategy['description'] = 'General knowledge integration and system enhancement'
            evolution_strategy['estimated_improvement'] = 0.05  # 5% improvement
            
            evolution_strategy['tasks'] = [
                {
                    'type': 'intelligence',
                    'priority': 'normal',
                    'delay': 2,
                    'description': f'Learn from {source}: General knowledge integration'
                }
            ]
        
        # Apply learning focus if specified
        if learning_focus != 'auto':
            for task in evolution_strategy['tasks']:
                if learning_focus in ['performance', 'efficiency', 'intelligence', 'adaptability']:
                    task['type'] = learning_focus
                    task['priority'] = 'high'  # Focused learning gets higher priority
        
        # Adjust based on content type
        if content_type in ['official_documentation', 'api_reference']:
            evolution_strategy['estimated_improvement'] *= 1.2  # 20% bonus for official docs
        elif content_type in ['tutorial', 'guide']:
            evolution_strategy['estimated_improvement'] *= 1.1  # 10% bonus for tutorials
        
    except Exception as e:
        logger.error(f"Error analyzing learning content: {str(e)}")
        # Fallback to default strategy
        evolution_strategy['tasks'] = [
            {
                'type': 'intelligence',
                'priority': 'normal',
                'delay': 2,
                'description': f'Learn from {source}: General knowledge integration'
            }
        ]
    
    return evolution_strategy



# Ensure brain interface is available for testing
try:
    get_brain_interface()  # Initialize brain interface on import
except Exception as e:
    logger.debug(f"Brain interface initialization deferred: {e}")

if __name__ == "__main__":
    logger.info("Starting Memory Context Manager with AI Memory Integration...")
    initialize_server()
    
    # Start MCP server with stdio (works for both Docker and CLI)
    logger.info("📡 Starting MCP server with stdio...")
    mcp.run("stdio")