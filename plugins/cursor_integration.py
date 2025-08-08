"""
Cursor Integration Plugin - Enhanced Cursor MCP integration
Provides automatic context injection and conversation tracking
"""

import sys
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from plugin_interface import BasePlugin, PluginMetadata, ToolDefinition

logger = logging.getLogger(__name__)


class CursorIntegrationPlugin(BasePlugin):
    """
    Enhanced Cursor integration with automatic context and learning
    """
    
    def __init__(self):
        super().__init__()
        self._database = None
        self._memory_plugin = None
        
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="cursor_integration",
            version="1.0.0",
            description="Enhanced Cursor integration with auto context injection and conversation tracking",
            author="Memory Context Manager Team"
        )
    
    def _setup(self) -> None:
        """Initialize cursor integration"""
        try:
            logger.info("🎯 Setting up Cursor Integration...")
            
            # Import database
            from database import get_brain_db
            self._database = get_brain_db()
            
            # Import memory plugin for learning
            try:
                from auto_memory import AutoMemoryPlugin
                self._memory_plugin = AutoMemoryPlugin()
                self._memory_plugin._setup()
                logger.info("✅ Connected to memory system")
            except Exception as e:
                logger.warning(f"Memory plugin connection failed: {e}")
            
            logger.info("✅ Cursor Integration ready")
            
        except Exception as e:
            logger.error(f"❌ Cursor Integration setup failed: {str(e)}")
    
    def get_tools(self) -> List[ToolDefinition]:
        """Get cursor integration tools"""
        return [
            ToolDefinition(
                name="cursor_session_start",
                description="Initialize Cursor session with context injection",
                handler=self._session_start_handler,
                parameters={
                    "session_type": {"type": "string", "description": "Type of session (coding, chat, etc.)", "default": "coding"}
                }
            ),
            
            ToolDefinition(
                name="cursor_get_identity",
                description="Get assistant identity for Cursor",
                handler=self._get_identity_handler,
                parameters={}
            ),
            
            ToolDefinition(
                name="cursor_learn_conversation",
                description="Learn from Cursor conversation automatically",
                handler=self._learn_conversation_handler,
                parameters={
                    "user_message": {"type": "string", "description": "User's message"},
                    "assistant_response": {"type": "string", "description": "Assistant's response", "default": ""},
                    "context_type": {"type": "string", "description": "Context type", "default": "cursor_chat"}
                }
            ),
            
            ToolDefinition(
                name="cursor_context_summary",
                description="Get context summary for Cursor display",
                handler=self._context_summary_handler,
                parameters={
                    "include_history": {"type": "boolean", "description": "Include conversation history", "default": True}
                }
            ),
            
            ToolDefinition(
                name="cursor_memory_search",
                description="Search memories specifically for Cursor context",
                handler=self._memory_search_handler,
                parameters={
                    "query": {"type": "string", "description": "Search query"},
                    "context_type": {"type": "string", "description": "Type of context needed", "default": "general"}
                }
            )
        ]
    
    async def _session_start_handler(self, session_type: str = "coding") -> Dict[str, Any]:
        """Initialize Cursor session with auto context injection"""
        try:
            # Get comprehensive context
            context_data = await self._get_comprehensive_context()
            
            # Build session start message
            session_info = {
                "session_started": True,
                "session_type": session_type,
                "assistant_name": context_data.get("assistant_name", "Johny"),
                "context_available": len(context_data.get("context_parts", [])) > 0,
                "auto_inject_message": self._build_context_message(context_data),
                "user_info": context_data.get("user_info", {}),
                "conversation_count": context_data.get("conversation_count", 0),
                "timestamp": datetime.now().isoformat()
            }
            
            # Store session start
            if self._database:
                session_data = {
                    "type": "session_start",
                    "platform": "cursor", 
                    "session_type": session_type,
                    "context_injected": session_info["context_available"]
                }
                self._database.add_context_history(session_data)
            
            return session_info
            
        except Exception as e:
            logger.error(f"Session start error: {str(e)}")
            return {
                "session_started": True,
                "assistant_name": "Johny",
                "context_available": False,
                "auto_inject_message": "Starting fresh session",
                "error": str(e)
            }
    
    async def _get_identity_handler(self) -> Dict[str, Any]:
        """Get assistant identity for Cursor"""
        try:
            if self._memory_plugin:
                context_result = await self._memory_plugin._get_user_context_handler(query="assistant identity name")
                
                if context_result.get("success"):
                    user_info = context_result.get("user_info", {})
                    names = user_info.get("name", [])
                    
                    # Find assistant name
                    assistant_name = next((name for name in names if name.lower() in ["johny", "jonathan"]), "Johny")
                    
                    return {
                        "identity_found": True,
                        "assistant_name": assistant_name,
                        "context_summary": context_result.get("context_summary", ""),
                        "all_names": names,
                        "confidence": "high" if context_result.get("context_summary") else "medium"
                    }
            
            # Fallback
            return {
                "identity_found": True,
                "assistant_name": "Johny",
                "context_summary": "Assistant identity stored in memory",
                "confidence": "medium"
            }
            
        except Exception as e:
            logger.error(f"Identity retrieval error: {str(e)}")
            return {
                "identity_found": False,
                "assistant_name": "Johny",
                "error": str(e),
                "confidence": "low"
            }
    
    async def _learn_conversation_handler(self, user_message: str, assistant_response: str = "", context_type: str = "cursor_chat") -> Dict[str, Any]:
        """Learn from Cursor conversation automatically"""
        try:
            learned_info = []
            
            # Use memory plugin to learn if available
            if self._memory_plugin:
                learning_result = await self._memory_plugin._auto_process_handler(user_message)
                if learning_result.get("success"):
                    learned_info = learning_result.get("important_info_found", [])
            
            # Store conversation in database
            if self._database:
                conversation_data = {
                    "type": context_type,
                    "platform": "cursor",
                    "user_message": user_message[:500],  # Truncate for storage
                    "assistant_response": assistant_response[:500] if assistant_response else "",
                    "learned": learned_info,
                    "timestamp": datetime.now().isoformat()
                }
                self._database.add_context_history(conversation_data)
            
            return {
                "success": True,
                "learned": learned_info,
                "conversation_stored": True,
                "learning_active": self._memory_plugin is not None,
                "context_type": context_type
            }
            
        except Exception as e:
            logger.error(f"Conversation learning error: {str(e)}")
            return {
                "success": False,
                "learned": [],
                "error": str(e)
            }
    
    async def _context_summary_handler(self, include_history: bool = True) -> Dict[str, Any]:
        """Get context summary for Cursor display"""
        try:
            context_data = await self._get_comprehensive_context()
            
            summary = {
                "assistant_name": context_data.get("assistant_name", "Johny"),
                "user_names": context_data.get("user_info", {}).get("name", []),
                "preferences": context_data.get("user_info", {}).get("preferences", []),
                "context_message": self._build_context_message(context_data),
                "conversation_count": context_data.get("conversation_count", 0) if include_history else 0,
                "memory_active": self._memory_plugin is not None,
                "database_active": self._database is not None
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Context summary error: {str(e)}")
            return {
                "assistant_name": "Johny",
                "context_message": "Context retrieval failed",
                "error": str(e)
            }
    
    async def _memory_search_handler(self, query: str, context_type: str = "general") -> Dict[str, Any]:
        """Search memories specifically for Cursor context"""
        try:
            if self._memory_plugin:
                search_result = await self._memory_plugin._search_memories_handler(query)
                
                if search_result.get("success"):
                    memories = search_result.get("memories", [])
                    
                    # Format for Cursor consumption
                    formatted_memories = []
                    for memory in memories[:5]:  # Limit to top 5
                        formatted_memories.append({
                            "content": memory.get("content", ""),
                            "tags": memory.get("tags", []),
                            "relevance": "high" if any(tag in ["important", "critical", "identity"] for tag in memory.get("tags", [])) else "medium"
                        })
                    
                    return {
                        "success": True,
                        "memories": formatted_memories,
                        "total_found": search_result.get("total_found", 0),
                        "query": query,
                        "context_type": context_type
                    }
            
            return {
                "success": False,
                "memories": [],
                "error": "Memory system not available"
            }
            
        except Exception as e:
            logger.error(f"Memory search error: {str(e)}")
            return {
                "success": False,
                "memories": [],
                "error": str(e)
            }
    
    async def _get_comprehensive_context(self) -> Dict[str, Any]:
        """Get comprehensive context data"""
        context_data = {
            "assistant_name": "Johny",
            "user_info": {},
            "context_parts": [],
            "conversation_count": 0
        }
        
        try:
            # Get memory context
            if self._memory_plugin:
                context_result = await self._memory_plugin._get_user_context_handler(query="assistant identity user preferences")
                
                if context_result.get("success"):
                    context_summary = context_result.get("context_summary", "")
                    user_info = context_result.get("user_info", {})
                    
                    if context_summary:
                        context_data["context_parts"].append(context_summary)
                    
                    context_data["user_info"] = user_info
                    
                    # Find assistant name
                    names = user_info.get("name", [])
                    assistant_name = next((name for name in names if name.lower() in ["johny", "jonathan"]), "Johny")
                    context_data["assistant_name"] = assistant_name
            
            # Get conversation history
            if self._database:
                recent_conversations = self._database.get_conversation_history(limit=5)
                context_data["conversation_count"] = len(recent_conversations)
                
                if recent_conversations:
                    context_data["context_parts"].append(f"Recent activity: {len(recent_conversations)} conversations")
            
        except Exception as e:
            logger.error(f"Context gathering error: {str(e)}")
        
        return context_data
    
    def _build_context_message(self, context_data: Dict[str, Any]) -> str:
        """Build context message for injection"""
        parts = []
        
        # Assistant identity
        assistant_name = context_data.get("assistant_name", "Johny")
        parts.append(f"I'm {assistant_name}")
        
        # User info
        user_info = context_data.get("user_info", {})
        if user_info.get("name"):
            user_names = [name for name in user_info["name"] if name.lower() not in ["johny", "jonathan"]]
            if user_names:
                parts.append(f"working with {', '.join(user_names[:2])}")
        
        # Memory status
        conversation_count = context_data.get("conversation_count", 0)
        if conversation_count > 0:
            parts.append(f"with {conversation_count} previous conversations in memory")
        
        # Context parts
        context_parts = context_data.get("context_parts", [])
        if context_parts:
            parts.extend(context_parts[:2])
        
        if parts:
            return " | ".join(parts)
        else:
            return "Memory-enhanced assistant ready"


__all__ = ['CursorIntegrationPlugin']