#!/usr/bin/env python3
"""
Enhanced Brain Tools with ContextAnalyzer Integration
Clean, purposeful tools designed for Cursor workflows
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class EnhancedBrainTools:
    """Enhanced brain tools with ContextAnalyzer integration"""
    
    def __init__(self, mcp_client, tool_registry):
        self.client = mcp_client
        self.registry = tool_registry
        self._register_enhanced_tools()
    
    def _register_enhanced_tools(self):
        """Register all enhanced brain tools with clear purposes"""
        
        # 🧠 COGNITIVE CORE TOOLS
        self._register_cognitive_tools()
        
        # 🧠 MEMORY MANAGEMENT TOOLS  
        self._register_memory_tools()
        
        # 🔍 ANALYSIS & UNDERSTANDING TOOLS
        self._register_analysis_tools()
        
        # 🚀 CURSOR-SPECIFIC TOOLS
        self._register_cursor_tools()
        
        # 🌟 CONTEXT ANALYSIS TOOLS
        self._register_context_tools()
    
    def _register_cognitive_tools(self):
        """Register enhanced cognitive tools"""
        
        async def think_deeply_handler(message: str, context: str = "conversation") -> dict:
            """Deep thinking with full context analysis"""
            try:
                # Perform deep context analysis
                context_analysis = await self._analyze_context_directly(message)
                
                # Use memory-enhanced chat
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
                        "subtle_patterns": context_analysis.get("subtle_patterns", []),
                        "implicit_goals": context_analysis.get("context_layers", {}).get("implicit_goals", {}),
                        "complexity_level": context_analysis.get("context_layers", {}).get("complexity_level", {})
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
                logger.error(f"Deep thinking error: {str(e)}")
                return {
                    "thought": f"I'm having trouble thinking clearly about: {message}",
                    "recalled_memories": "",
                    "new_learning": [],
                    "context_insights": [],
                    "error": str(e)
                }
        
        # Register the think_deeply tool
        self.registry.register_tool(
            name="think_deeply",
            handler=think_deeply_handler,
            category="cognitive",
            description="🧠 Deep reasoning with full ContextAnalyzer integration. Processes information with deep contextual understanding, recalls relevant memories, and generates thoughtful responses."
        )
        
        async def reflect_enhanced_handler(topic: str = "recent_interactions", focus_areas: List[str] = None) -> dict:
            """Enhanced reflection with context analysis"""
            try:
                # Perform context analysis on the reflection topic
                context_analysis = await self._analyze_context_directly(f"Reflecting on: {topic}")
                
                # Get reflection insights
                result = await self.client.call_tool(
                    "ai_chat_with_memory",
                    user_message=f"Help me reflect on: {topic}",
                    ai_model_name="phi3:mini"
                )
                
                if result.get("success"):
                    return {
                        "reflection_topic": topic,
                        "insights": result.get("ai_response", ""),
                        "patterns_identified": context_analysis.get("subtle_patterns", []),
                        "context_insights": context_analysis.get("insights", []),
                        "recommendations": context_analysis.get("recommendations", []),
                        "context_score": context_analysis.get("context_score", 0.0),
                        "reflection_depth": "enhanced_with_context"
                    }
                else:
                    return {
                        "reflection_topic": topic,
                        "insights": f"Reflecting on: {topic}",
                        "patterns_identified": [],
                        "context_insights": context_analysis.get("insights", []),
                        "recommendations": [],
                        "context_score": context_analysis.get("context_score", 0.0),
                        "reflection_depth": "basic",
                        "error": result.get("error", "Reflection process interrupted")
                    }
                    
            except Exception as e:
                logger.error(f"Enhanced reflection error: {str(e)}")
                return {
                    "reflection_topic": topic,
                    "insights": f"Having trouble reflecting on: {topic}",
                    "patterns_identified": [],
                    "context_insights": [],
                    "recommendations": [],
                    "context_score": 0.0,
                    "reflection_depth": "error",
                    "error": str(e)
                }
    
    def _register_memory_tools(self):
        """Register enhanced memory tools"""
        
        @self.registry.register_tool(
            name="remember_important",
            handler=self._remember_important_handler,
            category="memory",
            description="🧠 Enhanced memory formation with ContextAnalyzer integration. Stores information with emotional weighting, contextual tags, and deep understanding for future recall."
        )
        async def _remember_important_handler(information: str, importance: str = "medium") -> dict:
            """Enhanced memory formation with context analysis"""
            try:
                # Perform deep context analysis
                context_analysis = await self._analyze_context_directly(information)
                
                # Store in memory
                result = await self.client.call_tool(
                    "auto_process_message",
                    user_message=f"Remember this: {information}"
                )
                
                if result.get("success"):
                    # Enhanced memory tags based on context analysis
                    enhanced_tags = ["user_input", importance, "context_enhanced"]
                    if context_analysis.get("subtle_patterns"):
                        enhanced_tags.append("pattern_detected")
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
                            "insights": context_analysis.get("insights", []),
                            "subtle_patterns": context_analysis.get("subtle_patterns", [])
                        }
                    }
                else:
                    return {
                        "stored": False,
                        "what_learned": [],
                        "memory_type": "failed",
                        "emotional_weight": importance,
                        "recall_tags": ["user_input", importance],
                        "context_enhancement": {
                            "context_score": context_analysis.get("context_score", 0.0),
                            "insights": context_analysis.get("insights", [])
                        },
                        "error": result.get("error", "Memory storage failed")
                    }
                    
            except Exception as e:
                logger.error(f"Enhanced memory error: {str(e)}")
                return {
                    "stored": False,
                    "what_learned": [],
                    "memory_type": "error",
                    "emotional_weight": importance,
                    "recall_tags": ["user_input", importance],
                    "context_enhancement": {
                        "context_score": 0.0,
                        "insights": []
                    },
                    "error": str(e)
                }
    
    def _register_analysis_tools(self):
        """Register analysis and understanding tools"""
        
        @self.registry.register_tool(
            name="understand_deeply",
            handler=self._understand_deeply_handler,
            category="analysis",
            description="🔍 Deep comprehension analysis with ContextAnalyzer integration. Analyzes content for implicit goals, complexity, subtle patterns, and provides comprehensive understanding."
        )
        async def _understand_deeply_handler(content: str, analysis_focus: str = "comprehensive") -> dict:
            """Deep understanding with context analysis"""
            try:
                # Perform comprehensive context analysis
                context_analysis = await self._analyze_context_directly(content)
                
                return {
                    "content_analyzed": content,
                    "analysis_focus": analysis_focus,
                    "comprehension_level": "deep_with_context",
                    "context_score": context_analysis.get("context_score", 0.0),
                    "implicit_goals": context_analysis.get("context_layers", {}).get("implicit_goals", {}),
                    "complexity_assessment": context_analysis.get("context_layers", {}).get("complexity_level", {}),
                    "subtle_patterns": context_analysis.get("subtle_patterns", []),
                    "emotional_context": context_analysis.get("context_layers", {}).get("emotional_context", {}),
                    "insights": context_analysis.get("insights", []),
                    "recommendations": context_analysis.get("recommendations", []),
                    "uncertainty_level": context_analysis.get("context_layers", {}).get("uncertainty", {}).get("detected_uncertainty", "low")
                }
                
            except Exception as e:
                logger.error(f"Deep understanding error: {str(e)}")
                return {
                    "content_analyzed": content,
                    "analysis_focus": analysis_focus,
                    "comprehension_level": "error",
                    "context_score": 0.0,
                    "error": str(e)
                }
    
    def _register_cursor_tools(self):
        """Register Cursor-specific tools"""
        
        @self.registry.register_tool(
            name="code_analyze",
            handler=self._code_analyze_handler,
            category="cursor",
            description="💻 Code context and quality analysis with ContextAnalyzer integration. Analyzes code for patterns, complexity, best practices, and provides intelligent recommendations."
        )
        async def _code_analyze_handler(code_content: str, analysis_type: str = "comprehensive") -> dict:
            """Code analysis with context understanding"""
            try:
                # Perform context analysis on code
                context_analysis = await self._analyze_context_directly(code_content)
                
                # Analyze code patterns
                code_patterns = self._analyze_code_patterns(code_content)
                
                return {
                    "code_analyzed": code_content[:200] + "..." if len(code_content) > 200 else code_content,
                    "analysis_type": analysis_type,
                    "code_quality": code_patterns.get("quality", "unknown"),
                    "complexity_level": context_analysis.get("context_layers", {}).get("complexity_level", {}),
                    "best_practices": code_patterns.get("best_practices", []),
                    "potential_issues": code_patterns.get("potential_issues", []),
                    "context_insights": context_analysis.get("insights", []),
                    "recommendations": context_analysis.get("recommendations", []),
                    "context_score": context_analysis.get("context_score", 0.0)
                }
                
            except Exception as e:
                logger.error(f"Code analysis error: {str(e)}")
                return {
                    "code_analyzed": code_content[:200] + "..." if len(code_content) > 200 else code_content,
                    "analysis_type": analysis_type,
                    "error": str(e)
                }
    
    def _register_context_tools(self):
        """Register dedicated context analysis tools"""
        
        @self.registry.register_tool(
            name="analyze_context_comprehensive",
            handler=self._analyze_context_comprehensive_handler,
            category="context",
            description="🎯 Comprehensive context analysis using the full ContextAnalyzer module. Detects subtle patterns, implicit goals, complexity, uncertainty, and provides detailed insights."
        )
        async def _analyze_context_comprehensive_handler(content: str, analysis_type: str = "comprehensive") -> dict:
            """Comprehensive context analysis"""
            try:
                # Use the full ContextAnalyzer functionality
                context_analysis = await self._analyze_context_directly(content)
                
                return {
                    "content_analyzed": content,
                    "analysis_type": analysis_type,
                    "analysis_method": "full_context_analyzer",
                    "context_score": context_analysis.get("context_score", 0.0),
                    "context_layers": context_analysis.get("context_layers", {}),
                    "insights": context_analysis.get("insights", []),
                    "recommendations": context_analysis.get("recommendations", []),
                    "subtle_patterns": context_analysis.get("subtle_patterns", []),
                    "implicit_goals": context_analysis.get("context_layers", {}).get("implicit_goals", {}),
                    "complexity_assessment": context_analysis.get("context_layers", {}).get("complexity_level", {}),
                    "emotional_context": context_analysis.get("context_layers", {}).get("emotional_context", {}),
                    "uncertainty_detection": context_analysis.get("context_layers", {}).get("uncertainty", {}),
                    "temporal_context": context_analysis.get("context_layers", {}).get("temporal_context", {}),
                    "cross_domain_connections": context_analysis.get("context_layers", {}).get("cross_domain", {})
                }
                
            except Exception as e:
                logger.error(f"Comprehensive context analysis error: {str(e)}")
                return {
                    "content_analyzed": content,
                    "analysis_type": analysis_type,
                    "analysis_method": "error",
                    "context_score": 0.0,
                    "error": str(e)
                }
    
    def _analyze_code_patterns(self, code_content: str) -> Dict[str, Any]:
        """Analyze code for patterns and quality"""
        patterns = {
            "quality": "good",
            "best_practices": [],
            "potential_issues": []
        }
        
        # Simple code pattern analysis
        if "TODO" in code_content or "FIXME" in code_content:
            patterns["potential_issues"].append("Contains TODO/FIXME comments")
        
        if "print(" in code_content and "logging" not in code_content:
            patterns["best_practices"].append("Consider using logging instead of print statements")
        
        if "except:" in code_content:
            patterns["potential_issues"].append("Bare except clause - consider specific exception handling")
        
        if "def " in code_content and "->" in code_content:
            patterns["best_practices"].append("Good use of type hints")
        
        return patterns
    
    async def _analyze_context_directly(self, content: str) -> Dict[str, Any]:
        """Direct context analysis using ContextAnalyzer module"""
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
        """Fallback context analysis when ContextAnalyzer is unavailable"""
        # Simple pattern matching as fallback
        complexity_score = min(1.0, len(content.split()) / 100.0)
        
        return {
            "context_score": min(1.0, complexity_score + 0.3),
            "context_layers": {
                "implicit_goals": {
                    "detected_goals": ["general_communication"],
                    "confidence": 0.7
                },
                "complexity_level": {
                    "level": "medium" if complexity_score > 0.5 else "low",
                    "score": complexity_score
                }
            },
            "insights": ["Content analyzed with fallback method"],
            "recommendations": ["Use comprehensive analysis for deeper insights"],
            "subtle_patterns": []
        }
