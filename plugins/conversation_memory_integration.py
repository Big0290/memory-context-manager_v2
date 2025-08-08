"""
Conversation Memory Integration Plugin
Automatically stores and retrieves memories during conversations to provide persistent context
"""

import sys
import re
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
from datetime import datetime
import logging

# Add the plugin package to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from plugin_interface import BasePlugin, PluginMetadata, ToolDefinition

logger = logging.getLogger(__name__)


class ConversationMemoryIntegration(BasePlugin):
    """
    Plugin that automatically handles conversation memory storage and retrieval
    """
    
    def __init__(self):
        super().__init__()
        self._brain_integration = None
        self._conversation_history = []
        self._last_user_message = ""
        self._memory_keywords = set()
        
        # Patterns for important information to remember
        self._important_patterns = [
            # Name patterns
            r"(?:my name is|i'm|i am|call me|i go by)\s+([a-zA-Z]+)",
            r"(?:you can call me|please call me)\s+([a-zA-Z]+)",
            
            # Preference patterns  
            r"i (?:like|love|prefer|enjoy|hate|dislike)\s+(.+)",
            r"i (?:always|usually|never|often)\s+(.+)",
            
            # Personal info patterns
            r"i (?:work at|work for|am at|study at)\s+(.+)",
            r"i live in\s+(.+)",
            r"i'm (?:a|an)\s+(.+)",
            
            # Project/task patterns
            r"(?:i'm working on|working on|building|creating|developing)\s+(.+)",
            r"(?:my project|this project|our project)\s+(.+)",
            
            # Important facts
            r"(?:remember that|keep in mind|important:|note:)\s+(.+)",
            r"(?:don't forget|make sure)\s+(.+)",
        ]
        
        # Keywords that indicate important information
        self._importance_keywords = {
            'critical', 'important', 'remember', 'always', 'never', 
            'prefer', 'like', 'love', 'hate', 'dislike', 'name', 
            'called', 'project', 'working', 'building', 'creating'
        }
    
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="conversation_memory",
            version="1.0.0",
            description="Automatically stores and retrieves conversation memories for persistent context",
            author="Memory Integration Team",
            dependencies=["cognitive_brain"]
        )
    
    def _setup(self) -> None:
        """Initialize the conversation memory integration"""
        try:
            logger.info("🧠 Setting up Conversation Memory Integration...")
            
            # Import brain integration
            sys.path.insert(0, str(Path(__file__).parent))
            from cognitive_brain_plugin.integration.brain_plugin_integration import BrainPluginIntegration
            
            # Initialize brain integration  
            self._brain_integration = BrainPluginIntegration("brain_memory_store")
            
            # Initialize brain system if not already done
            if not self._brain_integration.brain.modules:
                success = self._brain_integration.brain.initialize()
                if not success:
                    raise Exception("Failed to initialize brain system")
            
            logger.info("✅ Conversation Memory Integration ready")
            
        except Exception as e:
            logger.error(f"❌ Failed to setup Conversation Memory Integration: {str(e)}")
            raise
    
    def get_tools(self) -> List[ToolDefinition]:
        """Get conversation memory tools"""
        tools = []
        
        # Automatic conversation processing
        tools.append(ToolDefinition(
            name="process_conversation",
            description="Process a conversation turn, automatically storing important info and retrieving relevant context",
            handler=self._process_conversation_handler,
            parameters={
                "user_message": {"type": "string", "description": "The user's message"},
                "ai_response": {"type": "string", "description": "The AI's response (optional, for learning)", "required": False}
            }
        ))
        
        # Get conversation context
        tools.append(ToolDefinition(
            name="get_conversation_context",
            description="Get relevant memories and context for the current conversation",
            handler=self._get_conversation_context_handler,
            parameters={
                "query": {"type": "string", "description": "Current conversation topic or query"},
                "max_memories": {"type": "integer", "description": "Maximum memories to retrieve", "default": 5}
            }
        ))
        
        # Memory search for conversations
        tools.append(ToolDefinition(
            name="search_conversation_memories",
            description="Search through stored conversation memories",
            handler=self._search_conversation_memories_handler,
            parameters={
                "query": {"type": "string", "description": "Search query"},
                "limit": {"type": "integer", "description": "Maximum results", "default": 10}
            }
        ))
        
        # Get user profile from memories
        tools.append(ToolDefinition(
            name="get_user_profile",
            description="Get accumulated user profile information from conversation memories",
            handler=self._get_user_profile_handler,
            parameters={}
        ))
        
        # Store important fact manually
        tools.append(ToolDefinition(
            name="remember_important_fact",
            description="Manually store an important fact about the user or conversation",
            handler=self._remember_important_fact_handler,
            parameters={
                "fact": {"type": "string", "description": "The important fact to remember"},
                "category": {"type": "string", "description": "Category (personal, preference, project, etc.)", "default": "general"}
            }
        ))
        
        return tools
    
    # Tool Handlers
    async def _process_conversation_handler(self, user_message: str, ai_response: str = None) -> Dict[str, Any]:
        """Process a conversation turn automatically"""
        try:
            self._last_user_message = user_message
            
            # 1. Extract important information from user message
            important_info = self._extract_important_info(user_message)
            stored_memories = []
            
            # 2. Store important information
            for info in important_info:
                memory_result = await self._brain_integration.store_memory(
                    content=info['content'],
                    tags=info['tags'],
                    emotional_weight=info['weight']
                )
                stored_memories.append({
                    "content": info['content'][:50] + "...",
                    "stored": memory_result.get('success', False)
                })
            
            # 3. Get relevant context for response
            context_memories = await self._get_relevant_context(user_message)
            
            # 4. Store the conversation turn
            conversation_memory = f"User: {user_message}"
            if ai_response:
                conversation_memory += f" | AI: {ai_response}"
                
            await self._brain_integration.store_memory(
                content=conversation_memory,
                tags=['conversation', 'dialogue'],
                emotional_weight='routine'
            )
            
            return {
                "success": True,
                "important_info_found": len(important_info),
                "memories_stored": stored_memories,
                "context_provided": len(context_memories),
                "relevant_context": context_memories,
                "analysis": {
                    "has_important_info": len(important_info) > 0,
                    "conversation_stored": True
                }
            }
            
        except Exception as e:
            logger.error(f"Conversation processing error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def _get_conversation_context_handler(self, query: str, max_memories: int = 5) -> Dict[str, Any]:
        """Get relevant conversation context"""
        try:
            context_memories = await self._get_relevant_context(query, max_memories)
            user_profile = await self._build_user_profile()
            
            return {
                "success": True,
                "relevant_memories": context_memories,
                "user_profile": user_profile,
                "context_summary": self._create_context_summary(context_memories, user_profile)
            }
            
        except Exception as e:
            logger.error(f"Context retrieval error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def _search_conversation_memories_handler(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Search conversation memories"""
        try:
            search_result = await self._brain_integration.recall_memories(query, limit)
            
            return {
                "success": True,
                "query": query,
                "memories_found": search_result.get('memories', []),
                "total_found": len(search_result.get('memories', []))
            }
            
        except Exception as e:
            logger.error(f"Memory search error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def _get_user_profile_handler(self) -> Dict[str, Any]:
        """Get user profile from memories"""
        try:
            user_profile = await self._build_user_profile()
            
            return {
                "success": True,
                "user_profile": user_profile,
                "profile_completeness": self._assess_profile_completeness(user_profile)
            }
            
        except Exception as e:
            logger.error(f"User profile error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def _remember_important_fact_handler(self, fact: str, category: str = "general") -> Dict[str, Any]:
        """Manually store important fact"""
        try:
            memory_result = await self._brain_integration.store_memory(
                content=fact,
                tags=[category, 'important_fact', 'manual'],
                emotional_weight='important'
            )
            
            return {
                "success": True,
                "fact_stored": fact,
                "category": category,
                "memory_result": memory_result
            }
            
        except Exception as e:
            logger.error(f"Fact storage error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    # Internal Methods
    def _extract_important_info(self, message: str) -> List[Dict[str, Any]]:
        """Extract important information from message"""
        important_info = []
        message_lower = message.lower()
        
        # Check importance keywords
        has_important_keywords = any(keyword in message_lower for keyword in self._importance_keywords)
        
        # Extract using patterns
        for pattern in self._important_patterns:
            matches = re.finditer(pattern, message_lower, re.IGNORECASE)
            for match in matches:
                if match.group(1):
                    content = f"User information: {match.group(0)}"
                    
                    # Determine category and weight
                    if 'name' in pattern or 'call me' in pattern:
                        category = 'personal_name'
                        weight = 'critical'
                    elif 'like' in pattern or 'prefer' in pattern:
                        category = 'preference'
                        weight = 'important'
                    elif 'work' in pattern or 'project' in pattern:
                        category = 'professional'
                        weight = 'important'
                    else:
                        category = 'personal'
                        weight = 'important' if has_important_keywords else 'routine'
                    
                    important_info.append({
                        'content': content,
                        'tags': [category, 'user_info', 'extracted'],
                        'weight': weight
                    })
        
        # Store general conversation if it seems important
        if has_important_keywords and not important_info:
            important_info.append({
                'content': f"Important user message: {message}",
                'tags': ['important', 'user_message'],
                'weight': 'important'
            })
        
        return important_info
    
    async def _get_relevant_context(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get relevant context memories for query"""
        try:
            # Search for relevant memories
            search_result = await self._brain_integration.recall_memories(query, limit * 2)
            memories = search_result.get('memories', [])
            
            # Filter and prioritize
            relevant_memories = []
            for memory in memories[:limit]:
                relevant_memories.append({
                    'content': memory.get('content', ''),
                    'tags': memory.get('tags', []),
                    'emotional_weight': memory.get('emotional_weight', 'routine'),
                    'created_at': memory.get('created_at', ''),
                    'relevance': 'high' if any(tag in ['personal_name', 'preference', 'important_fact'] 
                                              for tag in memory.get('tags', [])) else 'medium'
                })
            
            return relevant_memories
            
        except Exception as e:
            logger.error(f"Context retrieval error: {str(e)}")
            return []
    
    async def _build_user_profile(self) -> Dict[str, Any]:
        """Build user profile from stored memories"""
        try:
            # Search for different types of user information
            profile_searches = {
                'name': 'name call me',
                'preferences': 'like prefer love hate dislike',
                'professional': 'work project building creating',
                'personal': 'live family relationship'
            }
            
            profile = {}
            
            for category, search_terms in profile_searches.items():
                search_result = await self._brain_integration.recall_memories(search_terms, 5)
                memories = search_result.get('memories', [])
                
                if memories:
                    profile[category] = [
                        {
                            'info': memory.get('content', ''),
                            'confidence': memory.get('confidence', 0.5),
                            'date': memory.get('created_at', '')
                        }
                        for memory in memories[:3]  # Top 3 for each category
                    ]
            
            return profile
            
        except Exception as e:
            logger.error(f"Profile building error: {str(e)}")
            return {}
    
    def _create_context_summary(self, memories: List[Dict[str, Any]], user_profile: Dict[str, Any]) -> str:
        """Create a context summary for the AI"""
        summary_parts = []
        
        # Add user profile information
        if user_profile.get('name'):
            names = [info['info'] for info in user_profile['name'] if 'call me' in info['info'].lower()]
            if names:
                summary_parts.append(f"User prefers to be called: {names[0]}")
        
        if user_profile.get('preferences'):
            prefs = [info['info'] for info in user_profile['preferences'][:2]]
            if prefs:
                summary_parts.append(f"User preferences: {'; '.join(prefs)}")
        
        # Add recent relevant memories
        high_relevance_memories = [m for m in memories if m.get('relevance') == 'high']
        if high_relevance_memories:
            summary_parts.append("Important context: " + 
                                "; ".join([m['content'][:100] for m in high_relevance_memories[:2]]))
        
        return " | ".join(summary_parts) if summary_parts else "No specific context found"
    
    def _assess_profile_completeness(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Assess how complete the user profile is"""
        completeness = {
            'name': bool(profile.get('name')),
            'preferences': bool(profile.get('preferences')),
            'professional': bool(profile.get('professional')),
            'personal': bool(profile.get('personal')),
        }
        
        total_score = sum(completeness.values()) / len(completeness)
        
        return {
            'categories': completeness,
            'overall_score': total_score,
            'suggestions': self._get_profile_suggestions(completeness)
        }
    
    def _get_profile_suggestions(self, completeness: Dict[str, bool]) -> List[str]:
        """Get suggestions for improving profile completeness"""
        suggestions = []
        
        if not completeness['name']:
            suggestions.append("Consider asking the user how they'd like to be addressed")
        if not completeness['preferences']:
            suggestions.append("Learn about user preferences and interests")
        if not completeness['professional']:
            suggestions.append("Understand user's work or projects")
            
        return suggestions


# Make sure the plugin class is available for import
__all__ = ['ConversationMemoryIntegration']