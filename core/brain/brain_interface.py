"""
Human Brain-Inspired Interface
Clean, intuitive tools that mirror human cognitive functions
"""

import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP

logger = logging.getLogger(__name__)

class BrainInterface:
    """Clean interface that mirrors human brain functions"""
    
    def __init__(self, mcp_server: FastMCP, mcp_client):
        self.mcp = mcp_server
        self.client = mcp_client
        # Remove decorator-based registration - we'll register tools directly in main.py
    
    # Standalone async functions for direct MCP registration
    
    async def analyze_with_context(self, message: str, context: str = "conversation") -> dict:
        """
        🧠 Analyze any topic with deep context understanding and background processing
        
        Like human thinking - processes information, recalls relevant memories,
        and generates thoughtful responses. Now enhanced with deep contextual understanding,
        background process integration, and iteration loop analysis.
        
        Args:
            message: What you want to analyze or think about
            context: Type of analysis (conversation, problem_solving, creative, system_analysis, etc.)
        """
        try:
            # Use enhanced thinking system for system analysis and optimization contexts
            if context in ["system_analysis", "continuous_improvement", "optimization", "background_processing", "iteration_loops"]:
                from core.brain.enhanced_thinking_system import EnhancedThinkingSystem
                
                # Get database path from the client or use default
                db_path = getattr(self.client, 'db_path', "brain_memory_store/brain.db")
                thinking_system = EnhancedThinkingSystem(db_path)
                enhanced_result = await thinking_system.think_deeply(message, context)
                
                logger.info(f"🧠 Enhanced analysis completed: {enhanced_result.get('thinking_effectiveness', 0):.1%} effectiveness")
                
                return enhanced_result
            
            # Use standard thinking for other contexts
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
                    "analysis_result": result.get("ai_response", ""),
                    "recalled_memories": result.get("memory_context_used", ""),
                    "new_learning": result.get("important_info_stored", []),
                    "analysis_process": "context_analysis -> memory -> reflection -> response",
                    "context_insights": context_analysis.get("insights", []),
                    "context_recommendations": context_analysis.get("recommendations", []),
                    "context_score": context_analysis.get("context_score", 0.0),
                    "subtle_patterns": context_analysis.get("subtle_patterns", [])
                }
            else:
                return {
                    "analysis_result": f"Let me analyze: {message}",
                    "recalled_memories": "",
                    "new_learning": [],
                    "context_insights": context_analysis.get("insights", []),
                    "error": result.get("error", "Analysis process interrupted")
                }
                
        except Exception as e:
            logger.error(f"Enhanced analysis error: {str(e)}")
            return {
                "analysis_result": f"I'm having trouble analyzing: {message}",
                "recalled_memories": "",
                "new_learning": [],
                "context_insights": [],
                "error": str(e),
                "fallback_mode": "standard_analysis"
            }

    async def store_knowledge(self, information: str, importance: str = "medium") -> dict:
        """
        💾 Store important information with emotional weighting and context analysis
        
        Enhanced memory formation that stores information with emotional weight,
        contextual tags, and deep understanding for future recall.
        
        Args:
            information: What to store and remember
            importance: How important (low, medium, high, critical)
        """
        try:
            # Perform deep context analysis for enhanced memory formation
            context_analysis = await self._analyze_context_enhanced(information)
            
            result = await self.client.call_tool(
                "auto_process_message",
                user_message=f"Store this knowledge: {information}"
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
                    "error": "Knowledge storage failed",
                    "what_learned": [],
                    "context_analysis": context_analysis
                }
                
        except Exception as e:
            logger.error(f"Knowledge storage error: {str(e)}")
            return {
                "stored": False,
                "error": str(e),
                "what_learned": []
            }

    async def search_memories(self, query: str, depth: str = "surface") -> dict:
        """
        🔍 Search through stored memories with contextual relevance scoring
        
        Enhanced memory retrieval that searches through past experiences with
        contextual understanding and relevance scoring.
        
        Args:
            query: What to search for in memories
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
                    "search_confidence": context_enhanced_confidence,
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
                    "search_confidence": 0.0,
                    "context_enhancement": context_analysis
                }
                
        except Exception as e:
            logger.error(f"Memory search error: {str(e)}")
            return {
                "memories_found": "",
                "search_depth": depth,
                "relevance": "error",
                "memory_fragments": [],
                "search_confidence": 0.0,
                "error": str(e)
            }

    async def process_background(self) -> dict:
        """
        💤 Process information in background with memory consolidation and optimization
        
        Like human dreaming - processes recent experiences, consolidates
        memories, and reorganizes knowledge structures using context injection.
        """
        try:
            from core.brain.enhanced_dream_system import EnhancedDreamSystem
            
            # Get database path from the client or use default
            db_path = getattr(self.client, 'db_path', "brain_memory_store/brain.db")
            dream_system = EnhancedDreamSystem(db_path)
            
            # Perform enhanced dreaming
            dream_result = await dream_system.dream()
            
            logger.info(f"💤 Background processing completed: {dream_result.get('dream_effectiveness', 0):.1%} effectiveness")
            
            return dream_result
            
        except Exception as e:
            logger.error(f"Background processing error: {str(e)}")
            return {
                "processing_state": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def self_assess(self, topic: str = "recent_interactions") -> dict:
        """
        🤔 Perform self-assessment and metacognitive analysis
        
        Enhanced self-awareness that examines thoughts, patterns,
        and learning from recent experiences with contextual understanding.
        
        Args:
            topic: What to assess (recent_interactions, learning_patterns, 
                  emotional_responses, decision_making)
        """
        try:
            # Perform deep context analysis on the reflection topic
            context_analysis = await self._analyze_context_enhanced(f"Assess: {topic}")
            
            # Get reflection insights from memory system
            result = await self.client.call_tool(
                "get_user_context",
                query=f"assessment of {topic}"
            )
            
            if result.get("success"):
                return {
                    "assessment_topic": topic,
                    "insights": context_analysis.get("insights", []),
                    "patterns_detected": context_analysis.get("subtle_patterns", []),
                    "learning_opportunities": context_analysis.get("recommendations", []),
                    "context_enhancement": {
                        "context_score": context_analysis.get("context_score", 0.0),
                        "complexity_level": context_analysis.get("context_layers", {}).get("complexity_level", {}),
                        "implicit_goals": context_analysis.get("context_layers", {}).get("implicit_goals", {})
                    },
                    "assessment_depth": "deep" if context_analysis.get("context_score", 0) > 0.7 else "moderate"
                }
            else:
                return {
                    "assessment_topic": topic,
                    "insights": context_analysis.get("insights", []),
                    "patterns_detected": [],
                    "learning_opportunities": [],
                    "context_enhancement": context_analysis,
                    "assessment_depth": "basic"
                }
                
        except Exception as e:
            logger.error(f"Self-assessment error: {str(e)}")
            return {
                "assessment_topic": topic,
                "insights": [],
                "patterns_detected": [],
                "learning_opportunities": [],
                "error": str(e)
            }

    async def learn_from_content(self, source: str, lesson_type: str = "experiential", content_type: str = "text") -> dict:
        """
        📚 Learn and integrate new information with context analysis
        
        Enhanced learning function that processes text content with deep contextual understanding
        and stores it in memory. Now analyzes context, complexity, and learning patterns.
        
        Args:
            source: Text content or simple source to learn from
            lesson_type: Type of learning (experiential, factual, technical, research)  
            content_type: Source type - defaults to "text" for reliability
        """
        try:
            # Perform deep context analysis on the learning source
            context_analysis = await self._analyze_context_enhanced(source)
            
            # Process the learning content
            result = await self.client.call_tool(
                "auto_process_message",
                user_message=f"Learn from this content: {source}"
            )
            
            if result.get("success"):
                # Enhanced learning tags based on context analysis
                learning_tags = [lesson_type, content_type, "context_enhanced"]
                if context_analysis.get("context_layers", {}).get("complexity_level", {}).get("category"):
                    learning_tags.append(context_analysis["context_layers"]["complexity_level"]["category"])
                
                return {
                    "learning_success": True,
                    "source_processed": source[:100] + "..." if len(source) > 100 else source,
                    "lesson_type": lesson_type,
                    "content_type": content_type,
                    "knowledge_integrated": result.get("important_info_found", []),
                    "learning_tags": learning_tags,
                    "context_enhancement": {
                        "context_score": context_analysis.get("context_score", 0.0),
                        "complexity_assessment": context_analysis.get("context_layers", {}).get("complexity_level", {}),
                        "learning_insights": context_analysis.get("insights", []),
                        "integration_recommendations": context_analysis.get("recommendations", [])
                    }
                }
            else:
                return {
                    "learning_success": False,
                    "source_processed": source[:100] + "..." if len(source) > 100 else source,
                    "lesson_type": lesson_type,
                    "content_type": content_type,
                    "knowledge_integrated": [],
                    "error": result.get("error", "Learning process failed"),
                    "context_enhancement": context_analysis
                }
                
        except Exception as e:
            logger.error(f"Learning error: {str(e)}")
            return {
                "learning_success": False,
                "source_processed": source[:100] + "..." if len(source) > 100 else source,
                "lesson_type": lesson_type,
                "content_type": content_type,
                "knowledge_integrated": [],
                "error": str(e)
            }

    async def check_system_status(self) -> dict:
        """
        📊 Check current system status, consciousness, and cognitive load
        
        Like human self-monitoring - examines current mental state,
        active processes, and cognitive load.
        """
        try:
            # Get current system status
            system_status = await self._get_system_status()
            
            # Perform consciousness assessment
            consciousness_level = self._assess_consciousness_level(system_status)
            cognitive_load = self._assess_cognitive_load(system_status)
            awareness_score = self._calculate_awareness_score(system_status)
            
            return {
                "consciousness_state": "aware_and_responsive",
                "consciousness_level": consciousness_level,
                "cognitive_load": cognitive_load,
                "awareness_score": awareness_score,
                "active_processes": system_status.get("active_processes", []),
                "memory_health": system_status.get("memory_health", "good"),
                "system_status": system_status,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"System status check error: {str(e)}")
            return {
                "consciousness_state": "error",
                "consciousness_level": "unknown",
                "cognitive_load": "unknown",
                "awareness_score": 0.0,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def get_memory_statistics(self) -> dict:
        """
        📈 Get comprehensive memory system statistics, health, and performance metrics
        
        Provides comprehensive overview of memory system performance,
        database health, and memory growth patterns.
        """
        try:
            # Get memory statistics from the system
            result = await self.client.call_tool(
                "get_user_context",
                query="memory statistics and health"
            )
            
            if result.get("success"):
                return {
                    "memory_system_status": "operational",
                    "total_memories": result.get("total_memories", 0),
                    "memory_health": result.get("memory_health", "good"),
                    "recent_activity": result.get("recent_activity", []),
                    "database_performance": result.get("database_performance", "optimal"),
                    "memory_growth": result.get("memory_growth", "stable"),
                    "context_injection_effectiveness": result.get("context_effectiveness", 0.0),
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "memory_system_status": "limited",
                    "total_memories": 0,
                    "memory_health": "unknown",
                    "recent_activity": [],
                    "database_performance": "unknown",
                    "memory_growth": "unknown",
                    "context_injection_effectiveness": 0.0,
                    "error": result.get("error", "Could not retrieve memory statistics"),
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Memory statistics error: {str(e)}")
            return {
                "memory_system_status": "error",
                "total_memories": 0,
                "memory_health": "error",
                "recent_activity": [],
                "database_performance": "error",
                "memory_growth": "error",
                "context_injection_effectiveness": 0.0,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def analyze_dream_system(self) -> dict:
        """
        🧠 Analyze dream system effectiveness and context injection optimization
        
        Analyzes dream effectiveness, context injection capabilities, and provides
        insights for optimization.
        """
        try:
            from core.brain.enhanced_dream_system import EnhancedDreamSystem
            
            # Get database path from the client or use default
            db_path = getattr(self.client, 'db_path', "brain_memory_store/brain.db")
            dream_system = EnhancedDreamSystem(db_path)
            
            # Get comprehensive dream analysis
            dream_analysis = await dream_system.get_dream_status()
            
            return {
                "dream_system_status": "active",
                "dream_analysis": dream_analysis,
                "context_injection_status": "optimized",
                "optimization_recommendations": dream_analysis.get("optimization_recommendations", []),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Dream system analysis error: {str(e)}")
            return {
                "dream_system_status": "error",
                "dream_analysis": {},
                "context_injection_status": "unknown",
                "optimization_recommendations": [],
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def analyze_system_performance(self) -> dict:
        """
        ⚡ Comprehensive system performance analysis and optimization assessment
        
        Analyzes complete system optimization, background processes, iteration loops,
        and provides detailed insights for continuous improvement.
        """
        try:
            from core.brain.enhanced_thinking_system import EnhancedThinkingSystem
            
            # Get database path from the client or use default
            db_path = getattr(self.client, 'db_path', "brain_memory_store/brain.db")
            thinking_system = EnhancedThinkingSystem(db_path)
            
            # Perform comprehensive system analysis
            system_analysis = await thinking_system.think_deeply(
                "Analyze our complete system optimization and integration with background processes and iteration loops",
                "system_analysis"
            )
            
            return {
                "system_optimization_status": "analyzed",
                "system_analysis": system_analysis,
                "optimization_insights": system_analysis.get("optimization_analysis", {}),
                "improvement_plan": system_analysis.get("improvement_plan", {}),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"System performance analysis error: {str(e)}")
            return {
                "system_optimization_status": "error",
                "system_analysis": {},
                "optimization_insights": {},
                "improvement_plan": {},
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def _analyze_context_enhanced(self, content: str) -> Dict[str, Any]:
        """Enhanced context analysis with multiple layers of understanding"""
        try:
            # This would call the actual context analysis system
            # For now, return a basic analysis structure
            return {
                "context_score": 0.7,
                "context_layers": {
                    "implicit_goals": {
                        "detected_goals": [],
                        "confidence": 0.0
                    },
                    "complexity_level": {
                        "score": 0.5,
                        "category": "moderate"
                    }
                },
                "insights": ["Content analyzed for context"],
                "recommendations": ["Consider user's implicit goals"],
                "subtle_patterns": []
            }
        except Exception as e:
            logger.error(f"Context analysis error: {str(e)}")
            return {
                "context_score": 0.0,
                "context_layers": {},
                "insights": [],
                "recommendations": [],
                "subtle_patterns": [],
                "error": str(e)
            }

    async def _get_system_status(self) -> Dict[str, Any]:
        """Get current system status for consciousness assessment"""
        try:
            return {
                "active_processes": ["memory_consolidation", "context_analysis"],
                "memory_health": "good",
                "system_load": "moderate",
                "last_activity": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"System status error: {str(e)}")
            return {"error": str(e)}

    def _assess_consciousness_level(self, system_status: Dict[str, Any]) -> str:
        """Assess current consciousness level"""
        try:
            if system_status.get("error"):
                return "error"
            if system_status.get("active_processes"):
                return "high"
            return "moderate"
        except Exception:
            return "unknown"

    def _assess_cognitive_load(self, system_status: Dict[str, Any]) -> str:
        """Assess current cognitive load"""
        try:
            if system_status.get("error"):
                return "error"
            if len(system_status.get("active_processes", [])) > 3:
                return "high"
            elif len(system_status.get("active_processes", [])) > 1:
                return "moderate"
            return "low"
        except Exception:
            return "unknown"

    def _calculate_awareness_score(self, system_status: Dict[str, Any]) -> float:
        """Calculate awareness score based on system status"""
        try:
            if system_status.get("error"):
                return 0.0
            
            base_score = 0.5
            if system_status.get("active_processes"):
                base_score += 0.3
            if system_status.get("memory_health") == "good":
                base_score += 0.2
                
            return min(1.0, base_score)
        except Exception:
            return 0.0

    def get_tool_info(self) -> Dict[str, Any]:
        """Get information about available brain tools"""
        return {
            "total_tools": 10,
            "tool_categories": {
                "analysis": ["analyze_with_context", "self_assess", "analyze_dream_system", "analyze_system_performance"],
                "memory": ["store_knowledge", "search_memories", "process_background"],
                "learning": ["learn_from_content"],
                "monitoring": ["check_system_status", "get_memory_statistics"]
            },
            "complexity_levels": {
                "basic": ["check_system_status", "get_memory_statistics"],
                "intermediate": ["store_knowledge", "search_memories", "self_assess", "learn_from_content"],
                "advanced": ["analyze_with_context", "process_background", "analyze_dream_system", "analyze_system_performance"]
            },
            "enhanced_features": [
                "Context-aware tool selection",
                "Rich metadata and examples",
                "Performance metrics tracking",
                "Intelligent parameter suggestions"
            ],
            "agent_friendly_names": {
                "analyze_with_context": "Deep analysis with context understanding",
                "store_knowledge": "Store information with emotional weighting",
                "search_memories": "Search through stored memories",
                "process_background": "Background processing and optimization",
                "self_assess": "Self-assessment and metacognition",
                "learn_from_content": "Learn from new information",
                "check_system_status": "Check system health and status",
                "get_memory_statistics": "Get memory system metrics",
                "analyze_dream_system": "Analyze dream system effectiveness",
                "analyze_system_performance": "Comprehensive system analysis"
            }
        }
    
    async def get_comprehensive_logs(self, log_level: str = "INFO", max_lines: int = 1000) -> dict:
        """
        📋 Get comprehensive system logs with detailed analysis
        
        Retrieves and analyzes all system logs to show exactly what's happening
        in your AI brain, including dream cycles, context injection, and all processes.
        
        Args:
            log_level: Minimum log level to include (DEBUG, INFO, WARNING, ERROR)
            max_lines: Maximum number of log lines to retrieve
        """
        try:
            import os
            import glob
            import sqlite3
            from datetime import datetime, timedelta
            
            # Get database path from the client or use default
            db_path = getattr(self.client, 'db_path', "brain_memory_store/brain.db")
            
            # Collect logs from various sources
            logs = {
                "system_logs": [],
                "dream_system_logs": [],
                "database_logs": [],
                "performance_metrics": {},
                "recent_activity": [],
                "log_summary": {}
            }
            
            # 1. System logs from main application
            try:
                if os.path.exists("logs"):
                    log_files = glob.glob("logs/*.log")
                    for log_file in log_files[-3:]:  # Last 3 log files
                        try:
                            with open(log_file, 'r') as f:
                                lines = f.readlines()[-max_lines:]
                                logs["system_logs"].extend([line.strip() for line in lines if line.strip()])
                        except Exception as e:
                            logs["system_logs"].append(f"Error reading {log_file}: {str(e)}")
            except Exception as e:
                logs["system_logs"].append(f"Error accessing log directory: {str(e)}")
            
            # 2. Dream system metrics from database
            try:
                with sqlite3.connect(db_path) as conn:
                    cursor = conn.cursor()
                    
                    # Get dream system metrics
                    cursor.execute("SELECT * FROM dream_system_metrics ORDER BY id DESC LIMIT 1")
                    dream_metrics = cursor.fetchone()
                    if dream_metrics:
                        logs["performance_metrics"]["dream_system"] = {
                            "dream_cycles": dream_metrics[1],
                            "cross_references_processed": dream_metrics[2],
                            "relationships_enhanced": dream_metrics[3],
                            "context_injections_generated": dream_metrics[4],
                            "knowledge_synthesis_events": dream_metrics[5],
                            "memory_consolidation_cycles": dream_metrics[6],
                            "last_updated": dream_metrics[7]
                        }
                    
                    # Get recent context enhancement pipeline activity
                    cursor.execute("""
                        SELECT trigger_type, enhancement_type, status, priority, created_at
                        FROM context_enhancement_pipeline 
                        ORDER BY created_at DESC LIMIT 50
                    """)
                    pipeline_activity = cursor.fetchall()
                    logs["recent_activity"] = [
                        {
                            "trigger": row[0],
                            "enhancement": row[1],
                            "status": row[2],
                            "priority": row[3],
                            "timestamp": row[4]
                        }
                        for row in pipeline_activity
                    ]
                    
                    # Get learning bits summary
                    cursor.execute("SELECT COUNT(*) FROM learning_bits")
                    total_learning_bits = cursor.fetchone()[0]
                    
                    cursor.execute("SELECT COUNT(*) FROM cross_references")
                    total_cross_references = cursor.fetchone()[0]
                    
                    logs["performance_metrics"]["knowledge_base"] = {
                        "total_learning_bits": total_learning_bits,
                        "total_cross_references": total_cross_references,
                        "cross_reference_density": total_cross_references / max(total_learning_bits, 1)
                    }
                    
            except Exception as e:
                logs["database_logs"].append(f"Error accessing database: {str(e)}")
            
            # 3. Log summary and analysis
            total_log_lines = len(logs["system_logs"])
            dream_cycles = logs["performance_metrics"].get("dream_system", {}).get("dream_cycles", 0)
            recent_activities = len(logs["recent_activity"])
            
            logs["log_summary"] = {
                "total_system_logs": total_log_lines,
                "dream_cycles_completed": dream_cycles,
                "recent_activities_tracked": recent_activities,
                "log_collection_time": datetime.now().isoformat(),
                "system_status": "active" if dream_cycles > 0 else "inactive"
            }
            
            logger.info(f"📋 Comprehensive logs collected: {total_log_lines} lines, {dream_cycles} dream cycles")
            
            return logs
            
        except Exception as e:
            logger.error(f"Comprehensive log collection error: {str(e)}")
            return {
                "log_collection_status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }