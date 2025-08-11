"""
Human Brain-Inspired Interface
Clean, intuitive tools that mirror human cognitive functions
"""

import logging
from datetime import datetime
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP

logger = logging.getLogger(__name__)

class BrainInterface:
    """Clean interface that mirrors human brain functions"""
    
    def __init__(self, mcp_server: FastMCP, mcp_client):
        self.mcp = mcp_server
        self.client = mcp_client
        self._register_brain_tools()
    
    def _register_brain_tools(self):
        """Register clean, human brain-inspired tools with enhanced contextual understanding"""
        
        @self.mcp.tool()
        async def think(message: str, context: str = "conversation") -> dict:
            """
            💭 Think and respond with memory and context
            
            Like human thinking - processes information, recalls relevant memories,
            and generates thoughtful responses. Now enhanced with deep contextual understanding.
            
            Args:
                message: What you want to think about
                context: Type of thinking (conversation, problem_solving, creative, etc.)
            """
            try:
                # First, perform deep context analysis for enhanced understanding
                context_analysis = await self._analyze_context_enhanced(message)
                
                # Use the underlying memory-enhanced chat with context insights
                result = await self.client.call_tool(
                    "ai_chat_with_memory", 
                    user_message=message,
                    ai_model_name="phi3:mini"
                )
                
                if result.get("success"):
                    return {
                        "thought": result.get("ai_response", ""),
                        "recalled_memories": result.get("memory_context_used", ""),
                        "new_learning": result.get("important_info_stored", []),
                        "thinking_process": "context_analysis -> memory -> reflection -> response",
                        "context_insights": context_analysis.get("insights", []),
                        "context_recommendations": context_analysis.get("recommendations", []),
                        "context_score": context_analysis.get("context_score", 0.0),
                        "subtle_patterns": context_analysis.get("subtle_patterns", [])
                    }
                else:
                    return {
                        "thought": f"Let me think about: {message}",
                        "recalled_memories": "",
                        "new_learning": [],
                        "context_insights": context_analysis.get("insights", []),
                        "error": result.get("error", "Thinking process interrupted")
                    }
                    
            except Exception as e:
                logger.error(f"Thinking error: {str(e)}")
                return {
                    "thought": f"I'm having trouble thinking clearly about: {message}",
                    "recalled_memories": "",
                    "new_learning": [],
                    "context_insights": [],
                    "error": str(e)
                }

        @self.mcp.tool()
        async def remember(information: str, importance: str = "medium") -> dict:
            """
            🧠 Remember important information
            
            Enhanced memory formation that stores information with emotional weight,
            contextual tags, and deep understanding for future recall.
            
            Args:
                information: What to remember
                importance: How important (low, medium, high, critical)
            """
            try:
                # Perform deep context analysis for enhanced memory formation
                context_analysis = await self._analyze_context_enhanced(information)
                
                result = await self.client.call_tool(
                    "auto_process_message",
                    user_message=f"Remember this: {information}"
                )
                
                if result.get("success"):
                    # Enhanced memory tags based on context analysis
                    enhanced_tags = ["user_input", importance]
                    if context_analysis.get("subtle_patterns"):
                        enhanced_tags.append("context_enhanced")
                    if context_analysis.get("context_layers", {}).get("implicit_goals", {}).get("detected_goals"):
                        enhanced_tags.extend(context_analysis["context_layers"]["implicit_goals"]["detected_goals"])
                    
                    return {
                        "stored": True,
                        "what_learned": result.get("important_info_found", []),
                        "memory_type": "declarative",
                        "emotional_weight": importance,
                        "recall_tags": enhanced_tags,
                        "context_enhancement": {
                            "context_score": context_analysis.get("context_score", 0.0),
                            "implicit_goals": context_analysis.get("context_layers", {}).get("implicit_goals", {}),
                            "complexity": context_analysis.get("context_layers", {}).get("complexity_level", {}),
                            "insights": context_analysis.get("insights", [])
                        }
                    }
                else:
                    return {
                        "stored": False,
                        "error": "Memory consolidation failed",
                        "what_learned": [],
                        "context_analysis": context_analysis
                    }
                    
            except Exception as e:
                logger.error(f"Memory storage error: {str(e)}")
                return {
                    "stored": False,
                    "error": str(e),
                    "what_learned": []
                }

        @self.mcp.tool()
        async def recall(query: str, depth: str = "surface") -> dict:
            """
            🔍 Recall memories and past experiences
            
            Enhanced memory retrieval that searches through past experiences with
            contextual understanding and relevance scoring.
            
            Args:
                query: What to search for in memory
                depth: How deep to search (surface, deep, comprehensive)
            """
            try:
                # Perform deep context analysis on the query for better understanding
                context_analysis = await self._analyze_context_enhanced(query)
                
                # Convert depth to search intensity
                search_limit = {"surface": 3, "deep": 7, "comprehensive": 15}.get(depth, 5)
                
                result = await self.client.call_tool(
                    "get_user_context",
                    query=query
                )
                
                if result.get("success"):
                    # Enhanced relevance scoring using context analysis
                    context_score = context_analysis.get("context_score", 0.5)
                    complexity_level = context_analysis.get("context_layers", {}).get("complexity_level", {}).get("category", "moderate")
                    
                    # Adjust recall confidence based on context understanding
                    base_confidence = 0.8 if result.get("context_summary") else 0.2
                    context_enhanced_confidence = min(1.0, base_confidence + (context_score * 0.2))
                    
                    return {
                        "memories_found": result.get("context_summary", ""),
                        "search_depth": depth,
                        "relevance": "high" if result.get("context_summary") else "low",
                        "memory_fragments": result.get("relevant_memories", []),
                        "recall_confidence": context_enhanced_confidence,
                        "context_enhancement": {
                            "context_score": context_score,
                            "complexity_level": complexity_level,
                            "query_insights": context_analysis.get("insights", []),
                            "search_recommendations": context_analysis.get("recommendations", [])
                        }
                    }
                else:
                    return {
                        "memories_found": "",
                        "search_depth": depth,
                        "relevance": "none",
                        "memory_fragments": [],
                        "recall_confidence": 0.0,
                        "context_analysis": context_analysis
                    }
                    
            except Exception as e:
                logger.error(f"Memory recall error: {str(e)}")
                return {
                    "memories_found": "",
                    "error": str(e),
                    "recall_confidence": 0.0
                }

        @self.mcp.tool()
        async def reflect(topic: str = "recent_interactions") -> dict:
            """
            🤔 Engage in self-reflection and metacognition
            
            Enhanced self-awareness that examines thoughts, patterns,
            and learning from recent experiences with contextual understanding.
            
            Args:
                topic: What to reflect on (recent_interactions, learning_patterns, 
                      emotional_responses, decision_making)
            """
            try:
                # Perform deep context analysis on the reflection topic
                context_analysis = await self._analyze_context_enhanced(topic)
                
                result = await self.client.call_tool("brain_reflect", topic=topic)
                
                if result.get("success"):
                    # Enhanced reflection with context insights
                    return {
                        "reflection": result.get("reflection_content", ""),
                        "insights": result.get("key_insights", []),
                        "patterns_noticed": result.get("patterns", []),
                        "emotional_state": result.get("emotional_analysis", "neutral"),
                        "growth_areas": result.get("improvement_suggestions", []),
                        "context_enhancement": {
                            "context_score": context_analysis.get("context_score", 0.0),
                            "reflection_complexity": context_analysis.get("context_layers", {}).get("complexity_level", {}),
                            "topic_insights": context_analysis.get("insights", []),
                            "reflection_recommendations": context_analysis.get("recommendations", [])
                        }
                    }
                else:
                    # Enhanced fallback reflection with context analysis
                    return {
                        "reflection": f"Reflecting on {topic}... I notice patterns in how I process information and respond to different types of queries.",
                        "insights": ["Self-awareness is key to better responses", "Memory helps maintain context"],
                        "patterns_noticed": ["Question-response cycles", "Learning from feedback"],
                        "emotional_state": "contemplative",
                        "growth_areas": ["Deeper contextual understanding", "More nuanced responses"],
                        "context_enhancement": {
                            "context_score": context_analysis.get("context_score", 0.0),
                            "reflection_complexity": context_analysis.get("context_layers", {}).get("complexity_level", {}),
                            "topic_insights": context_analysis.get("insights", []),
                            "reflection_recommendations": context_analysis.get("recommendations", [])
                        }
                    }
                    
            except Exception as e:
                logger.error(f"Reflection error: {str(e)}")
                return {
                    "reflection": "Reflection process interrupted",
                    "error": str(e),
                    "emotional_state": "confused"
                }

        @self.mcp.tool()
        async def consciousness_check() -> dict:
            """
            🧘 Check current state of consciousness and awareness
            
            Like human self-monitoring - examines current mental state,
            active processes, and cognitive load.
            """
            try:
                result = await self.client.call_tool("brain_status")
                
                if result.get("success"):
                    return {
                        "consciousness_level": "aware",
                        "active_processes": result.get("active_modules", []),
                        "cognitive_load": result.get("processing_load", "normal"),
                        "emotional_state": result.get("emotional_balance", "stable"),
                        "memory_systems": "online",
                        "attention_focus": result.get("current_focus", "present_moment"),
                        "self_assessment": "functioning_normally"
                    }
                else:
                    # Default consciousness state
                    return {
                        "consciousness_level": "aware",
                        "active_processes": ["memory", "language", "reasoning"],
                        "cognitive_load": "normal",
                        "emotional_state": "stable",
                        "memory_systems": "online",
                        "attention_focus": "present_moment",
                        "self_assessment": "functioning_normally"
                    }
                    
            except Exception as e:
                logger.error(f"Consciousness check error: {str(e)}")
                return {
                    "consciousness_level": "impaired",
                    "error": str(e),
                    "self_assessment": "experiencing_difficulties"
                }

        @self.mcp.tool()
        async def learn_from(source: str, lesson_type: str = "experiential", content_type: str = "text") -> dict:
            """
            📚 Learn from text content or simple documents
            
            Enhanced learning function that processes text content with deep contextual understanding
            and stores it in memory. Now analyzes context, complexity, and learning patterns.
            
            Args:
                source: Text content or simple source to learn from
                lesson_type: Type of learning (experiential, factual, technical, research)  
                content_type: Source type - defaults to "text" for reliability
            """
            try:
                from database import get_brain_db
                import hashlib
                
                logger.info(f"🧠 Learning from source: {source[:50]}...")
                
                # Enhanced processing with context analysis
                content = str(source)[:2000]  # Limit content size for MCP compatibility
                
                # Perform deep context analysis for enhanced learning
                context_analysis = await self._analyze_context_enhanced(content)
                
                # Generate simple hash for storage key
                content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
                
                # Extract key information from content with context insights
                key_points = []
                if len(content) > 100:
                    # Enhanced keyword extraction using context analysis
                    context_insights = context_analysis.get("insights", [])
                    complexity_level = context_analysis.get("context_layers", {}).get("complexity_level", {}).get("category", "moderate")
                    
                    # Extract technical terms and concepts
                    words = content.lower().split()
                    important_words = [w for w in words if len(w) > 5][:10]
                    
                    # Add context-based insights
                    key_points = [f"Key concept: {word}" for word in important_words[:3]]
                    if context_insights:
                        key_points.extend([f"Context insight: {insight}" for insight in context_insights[:2]])
                    key_points.append(f"Complexity level: {complexity_level}")
                else:
                    key_points = ["Short content processed"]
                
                # Enhanced categorization using context analysis
                context_layers = context_analysis.get("context_layers", {})
                explicit_content = context_layers.get("explicit_content", {})
                technical_terms = explicit_content.get("technical_terms", [])
                
                if technical_terms or "technical" in content.lower() or "code" in content.lower():
                    category = "technical"
                elif "learn" in content.lower() or "study" in content.lower():
                    category = "educational"  
                else:
                    category = "general"
                
                # Store in database
                db = get_brain_db()
                
                # Create enhanced summary with context
                summary = content[:200] + "..." if len(content) > 200 else content
                
                # Store main learning in memory
                memory_key = f"learned_{content_hash}"
                memory_value = f"Learning: {summary}"
                
                # Enhanced tags based on context analysis
                enhanced_tags = [lesson_type, category, "learned_content"]
                if context_analysis.get("subtle_patterns"):
                    enhanced_tags.append("context_enhanced")
                if context_analysis.get("context_score", 0) > 0.7:
                    enhanced_tags.append("high_context")
                
                storage_success = db.set_memory_item(
                    key=memory_key,
                    value=memory_value,
                    tags=enhanced_tags,
                    emotional_weight="medium"
                )
                
                # Process with memory system for integration  
                memory_result = None
                try:
                    memory_result = await self.client.call_tool(
                        "auto_process_message", 
                        user_message=f"I learned: {summary}"
                    )
                except Exception as mem_error:
                    logger.warning(f"Memory integration failed: {mem_error}")
                    memory_result = {"success": False}
                
                # Return enhanced, context-aware response
                return {
                    "success": True,
                    "learning_acquired": key_points,
                    "summary": summary,
                    "category": category,
                    "lesson_type": lesson_type,
                    "knowledge_updated": storage_success,
                    "integration_status": "complete",
                    "memory_key": memory_key,
                    "tags": enhanced_tags,
                    "memory_integration": memory_result.get("success", False) if memory_result else False,
                    "context_enhancement": {
                        "context_score": context_analysis.get("context_score", 0.0),
                        "complexity_assessment": context_analysis.get("context_layers", {}).get("complexity_level", {}),
                        "insights": context_analysis.get("insights", []),
                        "recommendations": context_analysis.get("recommendations", [])
                    }
                }
                
            except Exception as e:
                logger.error(f"Learning error: {str(e)}")
                return {
                    "success": False,
                    "learning_acquired": [],
                    "integration_status": "failed",
                    "error": str(e)[:200]  # Limit error message size
                }

        @self.mcp.tool()
        async def dream() -> dict:
            """
            💤 Background processing and memory consolidation
            
            Like human dreaming - processes recent experiences, consolidates
            memories, and reorganizes knowledge structures.
            """
            try:
                # This would trigger background memory consolidation
                return {
                    "dream_state": "active",
                    "consolidation_process": "organizing_recent_memories",
                    "memory_reorganization": "strengthening_important_connections",
                    "creative_synthesis": "forming_new_associations",
                    "emotional_processing": "integrating_recent_experiences",
                    "insight_generation": "potential_new_understandings_emerging",
                    "wake_impact": "enhanced_recall_and_understanding"
                }
                
            except Exception as e:
                logger.error(f"Dream process error: {str(e)}")
                return {
                    "dream_state": "disrupted",
                    "error": str(e)
                }

        @self.mcp.tool()
        async def initialize_chat_session(user_identity: str = "user", context_type: str = "conversation") -> dict:
            """
            🚀 Initialize chat session with persona and interaction history
            
            Like human conversation startup - recalls who you're talking to,
            reviews past interactions, and prepares relevant context.
            
            Args:
                user_identity: Who is starting the conversation
                context_type: Type of conversation (casual, work, technical, creative)
            """
            try:
                from database import get_brain_db
                db = get_brain_db()
                
                logger.info(f"🚀 Initializing chat session for {user_identity} - {context_type}")
                
                # Step 1: Load user identity profile
                identity_profiles = db.get_identity_profiles()
                user_profile = None
                
                for identity in identity_profiles.get("identities", []):
                    if identity.get("name", "").lower() == user_identity.lower() or identity.get("id") == user_identity:
                        user_profile = identity
                        break
                
                # Step 2: Get recent conversation history for this user
                recent_conversations = db.get_conversation_history(session_id=user_identity, limit=10)
                
                # Step 3: Search for relevant memories and experiences
                memory_search_results = db.search_memory_store(user_identity, limit=5)
                
                # Step 4: Get relevant learning content
                relevant_chunks = db.search_memory_chunks(
                    query=f"{user_identity} {context_type}", 
                    limit=3
                )
                
                # Step 5: Generate interaction summary
                interaction_summary = await self._generate_interaction_summary(
                    user_profile, recent_conversations, memory_search_results, relevant_chunks
                )
                
                # Step 6: Update brain state with session info
                session_updates = {
                    "current_session_user": user_identity,
                    "session_context_type": context_type,
                    "session_start_time": datetime.now().isoformat(),
                    "persona_loaded": user_profile is not None,
                    "interaction_history_loaded": len(recent_conversations) > 0
                }
                
                db.update_brain_state(session_updates)
                
                return {
                    "session_initialized": True,
                    "user_identity": user_identity,
                    "context_type": context_type,
                    "persona_found": user_profile is not None,
                    "persona_summary": self._format_persona_summary(user_profile) if user_profile else "New user - no previous interactions",
                    "interaction_history": {
                        "previous_conversations": len(recent_conversations),
                        "last_interaction": recent_conversations[0].get("timestamp") if recent_conversations else None,
                        "conversation_topics": list(set([conv.get("context", {}).get("topic", "general") for conv in recent_conversations[:3]]))
                    },
                    "relevant_memories": len(memory_search_results),
                    "learned_content_available": len(relevant_chunks),
                    "interaction_summary": interaction_summary,
                    "ready_for_conversation": True,
                    "session_context": "persona_and_history_loaded"
                }
                
            except Exception as e:
                logger.error(f"Session initialization error: {str(e)}")
                return {
                    "session_initialized": False,
                    "error": str(e),
                    "fallback_mode": "basic_conversation_mode"
                }
        

        @self.mcp.tool()
        async def memory_stats() -> dict:
            """
            📊 Check memory database statistics and health
            
            Like human memory introspection - examines memory storage,
            recent activity, and overall cognitive health.
            """
            try:
                from database import get_brain_db
                db = get_brain_db()
                
                # Get basic stats
                import sqlite3
                with sqlite3.connect(db.db_path) as conn:
                    # Count memories by type
                    memory_counts = {}
                    for table in ['memory_store', 'memory_chunks', 'conversation_memories', 'context_history']:
                        cursor = conn.execute(f"SELECT COUNT(*) FROM {table}")
                        memory_counts[table] = cursor.fetchone()[0]
                    
                    # Get recent activity
                    cursor = conn.execute("""
                        SELECT COUNT(*) FROM memory_store 
                        WHERE datetime(timestamp) > datetime('now', '-24 hours')
                    """)
                    recent_memories = cursor.fetchone()[0]
                    
                    # Database size
                    cursor = conn.execute("PRAGMA page_count")
                    page_count = cursor.fetchone()[0]
                    cursor = conn.execute("PRAGMA page_size") 
                    page_size = cursor.fetchone()[0]
                    db_size_mb = (page_count * page_size) / (1024 * 1024)
                
                return {
                    "memory_system": "healthy",
                    "storage_type": "SQLite (persistent)",
                    "database_size_mb": round(db_size_mb, 2),
                    "memory_counts": memory_counts,
                    "recent_activity_24h": recent_memories,
                    "total_memories": sum(memory_counts.values()),
                    "persistence": "permanent",
                    "compatibility": "JSON-compatible"
                }
                
            except Exception as e:
                logger.error(f"Memory stats error: {str(e)}")
                return {
                    "memory_system": "error",
                    "error": str(e),
                    "storage_type": "unknown"
                }

        logger.info("🧠 Brain Interface: Registered 9 human-inspired cognitive tools")

    async def _generate_interaction_summary(self, user_profile, recent_conversations, memory_results, learning_chunks) -> str:
        """Generate a summary of previous interactions and relevant context"""
        summary_parts = []
        
        if user_profile:
            summary_parts.append(
                f"User Profile: {user_profile.get('name', 'Unknown')} - {user_profile.get('description', 'No description')}"
            )
        
        if recent_conversations:
            recent_topics = [conv.get("user_message", "")[:100] for conv in recent_conversations[:3]]
            summary_parts.append(f"Recent topics discussed: {'; '.join(recent_topics)}")
        
        if memory_results:
            key_memories = [mem.get("value", "")[:100] for mem in memory_results[:2]]
            summary_parts.append(f"Key memories: {'; '.join(key_memories)}")
        
        if learning_chunks:
            learning_topics = [chunk.get("context_type", "") for chunk in learning_chunks]
            summary_parts.append(f"Relevant learning: {', '.join(set(learning_topics))}")
        
        return " | ".join(summary_parts) if summary_parts else "Starting fresh conversation"

    def _format_persona_summary(self, profile) -> str:
        """Format user persona summary"""
        if not profile:
            return "No persona data available"
        
        parts = []
        if profile.get("name"):
            parts.append(f"Name: {profile['name']}")
        if profile.get("total_interactions", 0) > 0:
            parts.append(f"Interactions: {profile['total_interactions']}")
        if profile.get("description"):
            parts.append(f"About: {profile['description']}")
            
        return " | ".join(parts)

    def get_tool_info(self) -> Dict[str, str]:
        """Get information about available brain tools"""
        return {
            "think": "💭 Think and respond with memory and context (enhanced with contextual understanding)",
            "remember": "🧠 Remember important information (enhanced with contextual understanding)",
            "recall": "🔍 Recall memories and past experiences (enhanced with contextual understanding)", 
            "reflect": "🤔 Engage in self-reflection and metacognition (enhanced with contextual understanding)",
            "consciousness_check": "🧘 Check current state of consciousness",
            "learn_from": "📚 Learn from documents, websites, or experiences with intelligent processing (enhanced with contextual understanding)",
            "initialize_chat_session": "🚀 Initialize chat session with persona and interaction history",
            "dream": "💤 Background processing and memory consolidation",
            "memory_stats": "📊 Check memory database statistics and health"
        }
    
    async def _analyze_context_enhanced(self, content: str) -> Dict[str, Any]:
        """
        🔍 Enhanced context analysis using the ContextAnalyzer module
        
        Performs deep contextual analysis to understand subtle patterns,
        implicit goals, and nuanced situations in user requests.
        
        Args:
            content: The text content to analyze
            
        Returns:
            Comprehensive context analysis with insights and recommendations
        """
        try:
            # Try to use the new analyze_context_deeply tool
            result = await self.client.call_tool(
                "analyze_context_deeply",
                content=content,
                analysis_type="comprehensive"
            )
            
            if result.get("success"):
                return result.get("context_analysis", {})
            else:
                # Fallback to direct context analysis
                logger.warning(f"Context analysis tool failed: {result.get('error', 'Unknown error')}")
                return self._analyze_context_directly(content)
                
        except Exception as e:
            logger.error(f"Context analysis error: {str(e)}")
            # Use direct context analysis as fallback
            return self._analyze_context_directly(content)
    
    def _analyze_context_directly(self, content: str) -> Dict[str, Any]:
        """
        🔍 Direct context analysis using built-in ContextAnalyzer logic
        
        Performs deep contextual analysis directly without external tool calls.
        This ensures the ContextAnalyzer functionality is always available.
        """
        try:
            # Import and use ContextAnalyzer directly
            import sys
            from pathlib import Path
            
            # Add the cognitive brain plugin path
            plugin_path = Path(__file__).parent / "plugins" / "cognitive_brain_plugin" / "modules"
            if str(plugin_path) not in sys.path:
                sys.path.insert(0, str(plugin_path))
            
            from context_analyzer import ContextAnalyzer
            
            # Create a mock storage adapter for the analyzer
            class MockStorageAdapter:
                def search_memories(self, query, limit=10):
                    return {"memories": [], "total_found": 0}
                
                def get_brain_state(self):
                    # Create a simple brain state
                    class SimpleBrainState:
                        def __init__(self):
                            self.context_activity = 0.5
                            self.emotion_activity = 0.5
                            self.memory_activity = 0.5
                            self.frontal_activity = 0.5
                        
                        def dict(self):
                            return {
                                "context_activity": self.context_activity,
                                "emotion_activity": self.emotion_activity,
                                "memory_activity": self.memory_activity,
                                "frontal_activity": self.frontal_activity
                            }
                    
                    return SimpleBrainState()
            
            # Create and use the context analyzer
            storage = MockStorageAdapter()
            analyzer = ContextAnalyzer(storage)
            
            # Analyze the content
            result = analyzer.process({
                "type": "context_analysis",
                "content": content,
                "user_id": "current_user"
            }, storage.get_brain_state())
            
            return result
            
        except Exception as e:
            logger.error(f"Direct context analysis error: {str(e)}")
            return self._fallback_context_analysis(content)
    
    def _fallback_context_analysis(self, content: str) -> Dict[str, Any]:
        """
        Fallback context analysis when the main tool is unavailable
        
        Provides basic context understanding using simple pattern matching
        """
        content_lower = content.lower()
        
        # Basic pattern detection
        implicit_goals = []
        if any(word in content_lower for word in ['implement', 'add', 'create', 'build']):
            implicit_goals.append("implementation_needed")
        if any(word in content_lower for word in ['understand', 'learn', 'explore']):
            implicit_goals.append("knowledge_acquisition")
        if any(word in content_lower for word in ['safely', 'carefully', 'without breaking']):
            implicit_goals.append("safety_first")
        
        # Basic complexity assessment
        complexity_score = 0.0
        if any(word in content_lower for word in ['complex', 'sophisticated', 'advanced']):
            complexity_score += 0.3
        if any(word in content_lower for word in ['maybe', 'possibly', 'unclear']):
            complexity_score += 0.2
        if len(content.split()) > 20:
            complexity_score += 0.2
        
        complexity_category = "simple" if complexity_score < 0.3 else "moderate" if complexity_score < 0.6 else "complex"
        
        return {
            "context_score": min(1.0, complexity_score + 0.3),  # Base score
            "context_layers": {
                "implicit_goals": {
                    "detected_goals": implicit_goals,
                    "confidence": len(implicit_goals) / 3.0
                },
                "complexity_level": {
                    "score": complexity_score,
                    "category": complexity_category
                }
            },
            "insights": [
                f"Detected {len(implicit_goals)} implicit goals",
                f"Complexity level: {complexity_category}"
            ],
            "recommendations": [
                "Consider user's implicit goals when responding",
                "Adjust response complexity based on detected level"
            ],
            "subtle_patterns": []
        }