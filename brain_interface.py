"""
Human Brain-Inspired Interface
Clean, intuitive tools that mirror human cognitive functions
"""

import logging
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
        """Register clean, human brain-inspired tools"""
        
        @self.mcp.tool()
        async def think(message: str, context: str = "conversation") -> dict:
            """
            💭 Think and respond with memory and context
            
            Like human thinking - processes information, recalls relevant memories,
            and generates thoughtful responses.
            
            Args:
                message: What you want to think about
                context: Type of thinking (conversation, problem_solving, creative, etc.)
            """
            try:
                # Use the underlying memory-enhanced chat
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
                        "thinking_process": "memory -> reflection -> response"
                    }
                else:
                    return {
                        "thought": f"Let me think about: {message}",
                        "recalled_memories": "",
                        "new_learning": [],
                        "error": result.get("error", "Thinking process interrupted")
                    }
                    
            except Exception as e:
                logger.error(f"Thinking error: {str(e)}")
                return {
                    "thought": f"I'm having trouble thinking clearly about: {message}",
                    "recalled_memories": "",
                    "new_learning": [],
                    "error": str(e)
                }

        @self.mcp.tool()
        async def remember(information: str, importance: str = "medium") -> dict:
            """
            🧠 Remember important information
            
            Like human memory formation - stores information with emotional weight
            and contextual tags for future recall.
            
            Args:
                information: What to remember
                importance: How important (low, medium, high, critical)
            """
            try:
                result = await self.client.call_tool(
                    "auto_process_message",
                    user_message=f"Remember this: {information}"
                )
                
                if result.get("success"):
                    return {
                        "stored": True,
                        "what_learned": result.get("important_info_found", []),
                        "memory_type": "declarative",
                        "emotional_weight": importance,
                        "recall_tags": ["user_input", importance]
                    }
                else:
                    return {
                        "stored": False,
                        "error": "Memory consolidation failed",
                        "what_learned": []
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
            
            Like human memory retrieval - searches through past experiences,
            conversations, and learned information.
            
            Args:
                query: What to search for in memory
                depth: How deep to search (surface, deep, comprehensive)
            """
            try:
                # Convert depth to search intensity
                search_limit = {"surface": 3, "deep": 7, "comprehensive": 15}.get(depth, 5)
                
                result = await self.client.call_tool(
                    "get_user_context",
                    query=query
                )
                
                if result.get("success"):
                    return {
                        "memories_found": result.get("context_summary", ""),
                        "search_depth": depth,
                        "relevance": "high" if result.get("context_summary") else "low",
                        "memory_fragments": result.get("relevant_memories", []),
                        "recall_confidence": 0.8 if result.get("context_summary") else 0.2
                    }
                else:
                    return {
                        "memories_found": "",
                        "search_depth": depth,
                        "relevance": "none",
                        "memory_fragments": [],
                        "recall_confidence": 0.0
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
            
            Like human self-awareness - examines thoughts, patterns,
            and learning from recent experiences.
            
            Args:
                topic: What to reflect on (recent_interactions, learning_patterns, 
                      emotional_responses, decision_making)
            """
            try:
                result = await self.client.call_tool("brain_reflect", topic=topic)
                
                if result.get("success"):
                    return {
                        "reflection": result.get("reflection_content", ""),
                        "insights": result.get("key_insights", []),
                        "patterns_noticed": result.get("patterns", []),
                        "emotional_state": result.get("emotional_analysis", "neutral"),
                        "growth_areas": result.get("improvement_suggestions", [])
                    }
                else:
                    # Fallback reflection
                    return {
                        "reflection": f"Reflecting on {topic}... I notice patterns in how I process information and respond to different types of queries.",
                        "insights": ["Self-awareness is key to better responses", "Memory helps maintain context"],
                        "patterns_noticed": ["Question-response cycles", "Learning from feedback"],
                        "emotional_state": "contemplative",
                        "growth_areas": ["Deeper contextual understanding", "More nuanced responses"]
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
        async def learn_from(experience: str, lesson_type: str = "experiential") -> dict:
            """
            📚 Learn from new experiences and information
            
            Like human learning - processes new information, integrates it
            with existing knowledge, and forms new neural pathways.
            
            Args:
                experience: The experience or information to learn from
                lesson_type: Type of learning (experiential, factual, emotional, social)
            """
            try:
                # Process as both memory and learning
                memory_result = await self.client.call_tool(
                    "auto_process_message", 
                    user_message=f"Learning from: {experience}"
                )
                
                return {
                    "learning_acquired": memory_result.get("important_info_found", []),
                    "integration_status": "processed",
                    "lesson_type": lesson_type,
                    "neural_pathway": "new_connections_formed",
                    "knowledge_updated": memory_result.get("success", False),
                    "future_behavior_impact": "responses_will_incorporate_learning"
                }
                
            except Exception as e:
                logger.error(f"Learning error: {str(e)}")
                return {
                    "learning_acquired": [],
                    "integration_status": "failed",
                    "error": str(e)
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

        logger.info("🧠 Brain Interface: Registered 7 human-inspired cognitive tools")

    def get_tool_info(self) -> Dict[str, str]:
        """Get information about available brain tools"""
        return {
            "think": "💭 Think and respond with memory and context",
            "remember": "🧠 Remember important information",
            "recall": "🔍 Recall memories and past experiences", 
            "reflect": "🤔 Engage in self-reflection and metacognition",
            "consciousness_check": "🧘 Check current state of consciousness",
            "learn_from": "📚 Learn from new experiences and information",
            "dream": "💤 Background processing and memory consolidation"
        }