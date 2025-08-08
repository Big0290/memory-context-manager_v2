"""
Auto Memory Plugin - Simplified automatic conversation memory
Automatically processes conversations and provides context
"""

import sys
import re
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime
import logging

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from plugin_interface import BasePlugin, PluginMetadata, ToolDefinition

logger = logging.getLogger(__name__)


class AutoMemoryPlugin(BasePlugin):
    """
    Simplified plugin for automatic conversation memory
    """
    
    def __init__(self):
        super().__init__()
        self._brain_integration = None
        
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="auto_memory",
            version="1.0.0",
            description="Automatic conversation memory - stores important info and retrieves context",
            author="Auto Memory Team"
        )
    
    def _setup(self) -> None:
        """Initialize auto memory"""
        try:
            logger.info("🤖 Setting up Auto Memory...")
            
            # Import brain integration
            sys.path.insert(0, str(Path(__file__).parent))
            from cognitive_brain_plugin.integration.brain_plugin_integration import BrainPluginIntegration
            
            self._brain_integration = BrainPluginIntegration("brain_memory_store")
            
            # Initialize if needed
            if not self._brain_integration.brain.modules:
                self._brain_integration.brain.initialize()
            
            logger.info("✅ Auto Memory ready")
            
        except Exception as e:
            logger.error(f"❌ Auto Memory setup failed: {str(e)}")
            # Don't raise - allow server to continue
    
    def get_tools(self) -> List[ToolDefinition]:
        """Get auto memory tools"""
        return [
            ToolDefinition(
                name="auto_process_message",
                description="Automatically process user message - extract important info and get relevant context",
                handler=self._auto_process_handler,
                parameters={
                    "user_message": {"type": "string", "description": "The user's message"}
                }
            ),
            
            ToolDefinition(
                name="get_user_context",
                description="Get what we know about the user for providing better responses",
                handler=self._get_user_context_handler,
                parameters={
                    "query": {"type": "string", "description": "What to search for", "default": "user name preferences"}
                }
            ),
            
            ToolDefinition(
                name="remember_fact",
                description="Store an important fact about the user",
                handler=self._remember_fact_handler,
                parameters={
                    "fact": {"type": "string", "description": "Important fact to remember"}
                }
            ),
            
            ToolDefinition(
                name="search_memories",
                description="Search stored memories for specific information",
                handler=self._search_memories_handler,  
                parameters={
                    "query": {"type": "string", "description": "What to search for"}
                }
            )
        ]
    
    async def _auto_process_handler(self, user_message: str) -> Dict[str, Any]:
        """Automatically process a user message"""
        if not self._brain_integration:
            return {"success": False, "error": "Brain integration not available"}
        
        try:
            result = {
                "success": True,
                "message_processed": True,
                "important_info_found": [],
                "relevant_context": [],
                "user_context_summary": ""
            }
            
            # 1. Check for important information to store
            important_facts = self._extract_important_facts(user_message)
            
            # 2. Store important facts
            for fact in important_facts:
                try:
                    memory_result = await self._brain_integration.store_memory(
                        content=fact['content'],
                        tags=fact['tags'],
                        emotional_weight=fact['weight']
                    )
                    result["important_info_found"].append(fact['summary'])
                except Exception as e:
                    logger.error(f"Failed to store fact: {e}")
            
            # 3. Get relevant context
            context_result = await self._brain_integration.recall_memories(user_message, 5)
            memories = context_result.get('memories', [])
            
            # 4. Build context summary
            context_summary = self._build_context_summary(memories)
            result["user_context_summary"] = context_summary
            result["relevant_context"] = [
                {
                    "content": m.get('content', '')[:100] + "..." if len(m.get('content', '')) > 100 else m.get('content', ''),
                    "relevance": "high" if any(tag in ['name', 'preference', 'important'] for tag in m.get('tags', [])) else "medium"
                }
                for m in memories[:3]
            ]
            
            # 5. Store conversation turn
            try:
                await self._brain_integration.store_memory(
                    content=f"User message: {user_message}",
                    tags=['conversation', 'user_message'],
                    emotional_weight='routine'
                )
            except Exception as e:
                logger.error(f"Failed to store conversation: {e}")
            
            return result
            
        except Exception as e:
            logger.error(f"Auto process error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def _get_user_context_handler(self, query: str = "user name preferences") -> Dict[str, Any]:
        """Get user context"""
        if not self._brain_integration:
            return {"success": False, "error": "Brain integration not available"}
        
        try:
            # Search for user information with multiple queries
            all_memories = []
            
            # Try the original query
            search_result = await self._brain_integration.recall_memories(query, 10)
            all_memories.extend(search_result.get('memories', []))
            
            # Also try more specific searches 
            for search_term in ['assistant', 'identity', 'name', 'user']:
                search_result = await self._brain_integration.recall_memories(search_term, 5)
                all_memories.extend(search_result.get('memories', []))
            
            # Remove duplicates based on key
            seen_keys = set()
            memories = []
            for memory in all_memories:
                key = memory.get('key', '')
                if key not in seen_keys:
                    memories.append(memory)
                    seen_keys.add(key)
            
            # Build user profile
            user_info = {
                "name": [],
                "preferences": [],
                "important_facts": [],
                "recent_topics": []
            }
            
            for memory in memories:
                content = memory.get('content', '').lower()
                tags = memory.get('tags', [])
                
                if any(tag in ['name', 'personal_name', 'assistant', 'identity'] for tag in tags) or 'call me' in content or 'name is' in content or 'assistant_name' in memory.get('key', ''):
                    user_info["name"].append(memory.get('content', ''))
                elif any(tag in ['preference'] for tag in tags) or 'like' in content or 'prefer' in content:
                    user_info["preferences"].append(memory.get('content', ''))
                elif any(tag in ['important', 'critical'] for tag in tags):
                    user_info["important_facts"].append(memory.get('content', ''))
                else:
                    user_info["recent_topics"].append(memory.get('content', ''))
            
            # Create summary
            summary_parts = []
            if user_info["name"]:
                summary_parts.append(f"User name/identity: {user_info['name'][0]}")
            if user_info["preferences"]:
                summary_parts.append(f"Preferences: {'; '.join(user_info['preferences'][:2])}")
            if user_info["important_facts"]:
                summary_parts.append(f"Important: {'; '.join(user_info['important_facts'][:2])}")
            
            return {
                "success": True,
                "user_info": user_info,
                "context_summary": " | ".join(summary_parts) if summary_parts else "No specific user context found",
                "total_memories": len(memories)
            }
            
        except Exception as e:
            logger.error(f"Context retrieval error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def _remember_fact_handler(self, fact: str) -> Dict[str, Any]:
        """Store an important fact"""
        if not self._brain_integration:
            return {"success": False, "error": "Brain integration not available"}
        
        try:
            memory_result = await self._brain_integration.store_memory(
                content=fact,
                tags=['important_fact', 'manual'],
                emotional_weight='important'
            )
            
            return {
                "success": True,
                "fact_stored": fact,
                "memory_result": memory_result
            }
            
        except Exception as e:
            logger.error(f"Fact storage error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def _search_memories_handler(self, query: str) -> Dict[str, Any]:
        """Search memories"""
        if not self._brain_integration:
            return {"success": False, "error": "Brain integration not available"}
        
        try:
            search_result = await self._brain_integration.recall_memories(query, 10)
            
            return {
                "success": True,
                "query": query,
                "memories": search_result.get('memories', []),
                "total_found": len(search_result.get('memories', []))
            }
            
        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _extract_important_facts(self, message: str) -> List[Dict[str, Any]]:
        """Extract important facts from message"""
        facts = []
        message_lower = message.lower()
        
        # Name extraction patterns
        name_patterns = [
            r"(?:my name is|i'm|i am|call me|you can call me)\s+([a-zA-Z]+)",
            r"(?:i go by|please call me)\s+([a-zA-Z]+)"
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, message_lower)
            if match:
                name = match.group(1).title()
                facts.append({
                    'content': f"User prefers to be called: {name}",
                    'tags': ['name', 'personal_name', 'user_preference'],
                    'weight': 'critical',
                    'summary': f"User name: {name}"
                })
        
        # Preference patterns
        pref_patterns = [
            r"i (?:like|love|prefer|enjoy)\s+([^.!?]+)",
            r"i (?:hate|dislike|don't like)\s+([^.!?]+)"
        ]
        
        for pattern in pref_patterns:
            match = re.search(pattern, message_lower)
            if match:
                preference = match.group(0)
                facts.append({
                    'content': f"User preference: {preference}",
                    'tags': ['preference', 'user_preference'],
                    'weight': 'important',
                    'summary': preference
                })
        
        # Important keywords
        important_keywords = ['remember', 'important', 'always', 'never', 'project', 'working on']
        if any(keyword in message_lower for keyword in important_keywords):
            facts.append({
                'content': f"Important user statement: {message}",
                'tags': ['important', 'user_statement'],
                'weight': 'important',
                'summary': "Important statement"
            })
        
        return facts
    
    def _build_context_summary(self, memories: List[Dict[str, Any]]) -> str:
        """Build a context summary from memories"""
        if not memories:
            return "No previous context found"
        
        # Priority: name, preferences, important facts
        summary_parts = []
        
        for memory in memories[:5]:
            content = memory.get('content', '')
            tags = memory.get('tags', [])
            
            if any(tag in ['name', 'personal_name', 'assistant', 'identity'] for tag in tags):
                summary_parts.insert(0, f"Name: {content}")  # Put name first
            elif any(tag in ['preference'] for tag in tags):
                summary_parts.append(f"Preference: {content}")
            elif any(tag in ['important'] for tag in tags):
                summary_parts.append(f"Important: {content}")
        
        if summary_parts:
            return " | ".join(summary_parts[:3])  # Limit to 3 key points
        else:
            return f"Recent context available ({len(memories)} memories)"


__all__ = ['AutoMemoryPlugin']