#!/usr/bin/env python3
"""
Enhanced Brain Tools with ContextAnalyzer Integration - Simplified Version
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
        
        # Register the reflect_enhanced tool
        self.registry.register_tool(
            name="reflect_enhanced",
            handler=reflect_enhanced_handler,
            category="cognitive",
            description="🤔 Advanced self-reflection with ContextAnalyzer integration. Analyzes patterns, learns from experiences, and provides deep insights with contextual understanding."
        )
    
    def _register_memory_tools(self):
        """Register enhanced memory tools"""
        
        async def remember_important_handler(information: str, importance: str = "medium") -> dict:
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
        
        # Register the remember_important tool
        self.registry.register_tool(
            name="remember_important",
            handler=remember_important_handler,
            category="memory",
            description="🧠 Enhanced memory formation with ContextAnalyzer integration. Stores information with emotional weighting, contextual tags, and deep understanding for future recall."
        )
        
        async def recall_intelligently_handler(query: str, depth: str = "surface", limit: int = 10) -> dict:
            """Intelligent memory retrieval with context analysis"""
            try:
                # Perform context analysis on the query
                context_analysis = await self._analyze_context_directly(query)
                
                # Search memories with enhanced context
                result = await self.client.call_tool(
                    "search_function_calls",
                    search_term=query,
                    limit=limit
                )
                
                if result.get("success"):
                    # Enhance results with context analysis
                    enhanced_results = []
                    for memory in result.get("function_calls", []):
                        enhanced_memory = {
                            "content": memory.get("function_name", ""),
                            "relevance_score": self._calculate_relevance_score(query, memory, context_analysis),
                            "context_tags": context_analysis.get("context_layers", {}).get("implicit_goals", {}).get("detected_goals", []),
                            "emotional_weight": memory.get("emotional_weight", "medium"),
                            "timestamp": memory.get("timestamp", "")
                        }
                        enhanced_results.append(enhanced_memory)
                    
                    # Sort by relevance score
                    enhanced_results.sort(key=lambda x: x["relevance_score"], reverse=True)
                    
                    return {
                        "query": query,
                        "search_depth": depth,
                        "memories_found": len(enhanced_results),
                        "enhanced_results": enhanced_results[:limit],
                        "context_enhancement": {
                            "context_score": context_analysis.get("context_score", 0.0),
                            "search_patterns": context_analysis.get("subtle_patterns", []),
                            "implicit_goals": context_analysis.get("context_layers", {}).get("implicit_goals", {})
                        }
                    }
                else:
                    return {
                        "query": query,
                        "search_depth": depth,
                        "memories_found": 0,
                        "enhanced_results": [],
                        "context_enhancement": {
                            "context_score": context_analysis.get("context_score", 0.0),
                            "search_patterns": []
                        },
                        "error": result.get("error", "Memory search failed")
                    }
                    
            except Exception as e:
                logger.error(f"Intelligent recall error: {str(e)}")
                return {
                    "query": query,
                    "search_depth": depth,
                    "memories_found": 0,
                    "enhanced_results": [],
                    "context_enhancement": {
                        "context_score": 0.0,
                        "search_patterns": []
                    },
                    "error": str(e)
                }
        
        # Register the recall_intelligently tool
        self.registry.register_tool(
            name="recall_intelligently",
            handler=recall_intelligently_handler,
            category="memory",
            description="🔍 Intelligent memory retrieval with ContextAnalyzer integration. Searches memories with context-aware relevance scoring and enhanced pattern recognition."
        )
        
        async def forget_selectively_handler(criteria: str, confirmation: bool = False) -> dict:
            """Selective memory cleanup with context analysis"""
            try:
                # Perform context analysis on the cleanup criteria
                context_analysis = await self._analyze_context_directly(criteria)
                
                if not confirmation:
                    return {
                        "action": "preview",
                        "criteria": criteria,
                        "memories_identified": 0,
                        "context_analysis": context_analysis,
                        "message": "This is a preview. Set confirmation=True to proceed with cleanup."
                    }
                
                # Perform selective cleanup based on context
                cleanup_result = await self.client.call_tool(
                    "get_function_call_history",
                    limit=100
                )
                
                if cleanup_result.get("success"):
                    # Analyze which memories match cleanup criteria
                    memories_to_clean = []
                    for memory in cleanup_result.get("function_calls", []):
                        if self._matches_cleanup_criteria(memory, criteria, context_analysis):
                            memories_to_clean.append(memory)
                    
                    return {
                        "action": "cleanup_completed",
                        "criteria": criteria,
                        "memories_cleaned": len(memories_to_clean),
                        "cleanup_summary": memories_to_clean,
                        "context_enhancement": {
                            "context_score": context_analysis.get("context_score", 0.0),
                            "cleanup_patterns": context_analysis.get("subtle_patterns", []),
                            "implicit_goals": context_analysis.get("context_layers", {}).get("implicit_goals", {})
                        }
                    }
                else:
                    return {
                        "action": "cleanup_failed",
                        "criteria": criteria,
                        "error": cleanup_result.get("error", "Cleanup process failed")
                    }
                    
            except Exception as e:
                logger.error(f"Selective forget error: {str(e)}")
                return {
                    "action": "error",
                    "criteria": criteria,
                    "error": str(e)
                }
        
        # Register the forget_selectively tool
        self.registry.register_tool(
            name="forget_selectively",
            handler=forget_selectively_handler,
            category="memory",
            description="🧹 Selective memory cleanup with ContextAnalyzer integration. Intelligently removes outdated or irrelevant memories based on context analysis."
        )
    
    def _register_analysis_tools(self):
        """Register analysis and understanding tools"""
        
        async def understand_deeply_handler(content: str, analysis_focus: str = "comprehensive") -> dict:
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
        
        # Register the understand_deeply tool
        self.registry.register_tool(
            name="understand_deeply",
            handler=understand_deeply_handler,
            category="analysis",
            description="🔍 Deep comprehension analysis with ContextAnalyzer integration. Analyzes content for implicit goals, complexity, subtle patterns, and provides comprehensive understanding."
        )
        
        async def detect_patterns_handler(content: str, pattern_type: str = "all") -> dict:
            """Advanced pattern detection with ContextAnalyzer"""
            try:
                # Perform comprehensive context analysis
                context_analysis = await self._analyze_context_directly(content)
                
                # Extract different types of patterns
                patterns = {
                    "subtle_patterns": context_analysis.get("subtle_patterns", []),
                    "implicit_goals": context_analysis.get("context_layers", {}).get("implicit_goals", {}),
                    "emotional_patterns": context_analysis.get("context_layers", {}).get("emotional_context", {}),
                    "complexity_patterns": context_analysis.get("context_layers", {}).get("complexity_level", {}),
                    "temporal_patterns": context_analysis.get("context_layers", {}).get("temporal_context", {}),
                    "cross_domain_patterns": context_analysis.get("context_layers", {}).get("cross_domain", {})
                }
                
                # Filter by pattern type if specified
                if pattern_type != "all" and pattern_type in patterns:
                    filtered_patterns = {pattern_type: patterns[pattern_type]}
                else:
                    filtered_patterns = patterns
                
                return {
                    "content_analyzed": content,
                    "pattern_type": pattern_type,
                    "patterns_detected": filtered_patterns,
                    "total_patterns": sum(len(p) if isinstance(p, list) else 1 for p in filtered_patterns.values()),
                    "context_score": context_analysis.get("context_score", 0.0),
                    "pattern_confidence": self._calculate_pattern_confidence(filtered_patterns),
                    "insights": context_analysis.get("insights", [])
                }
                
            except Exception as e:
                logger.error(f"Pattern detection error: {str(e)}")
                return {
                    "content_analyzed": content,
                    "pattern_type": pattern_type,
                    "patterns_detected": {},
                    "total_patterns": 0,
                    "context_score": 0.0,
                    "pattern_confidence": 0.0,
                    "insights": [],
                    "error": str(e)
                }
        
        # Register the detect_patterns tool
        self.registry.register_tool(
            name="detect_patterns",
            handler=detect_patterns_handler,
            category="analysis",
            description="🔍 Advanced pattern detection with ContextAnalyzer integration. Identifies subtle patterns, emotional contexts, complexity levels, and cross-domain connections."
        )
        
        async def assess_complexity_handler(content: str, assessment_focus: str = "comprehensive") -> dict:
            """Comprehensive complexity assessment with ContextAnalyzer"""
            try:
                # Perform deep context analysis
                context_analysis = await self._analyze_context_directly(content)
                
                # Extract complexity information
                complexity_layers = context_analysis.get("context_layers", {}).get("complexity_level", {})
                
                # Calculate overall complexity score
                complexity_score = complexity_layers.get("score", 0.0)
                complexity_level = complexity_layers.get("level", "unknown")
                
                # Assess different aspects of complexity
                complexity_assessment = {
                    "overall_score": complexity_score,
                    "level": complexity_level,
                    "cognitive_load": self._assess_cognitive_load(content, complexity_score),
                    "technical_complexity": self._assess_technical_complexity(content),
                    "emotional_complexity": self._assess_emotional_complexity(context_analysis),
                    "contextual_complexity": self._assess_contextual_complexity(context_analysis),
                    "recommendations": self._generate_complexity_recommendations(complexity_score, complexity_level)
                }
                
                return {
                    "content_assessed": content,
                    "assessment_focus": assessment_focus,
                    "complexity_assessment": complexity_assessment,
                    "context_score": context_analysis.get("context_score", 0.0),
                    "insights": context_analysis.get("insights", []),
                    "patterns": context_analysis.get("subtle_patterns", [])
                }
                
            except Exception as e:
                logger.error(f"Complexity assessment error: {str(e)}")
                return {
                    "content_assessed": content,
                    "assessment_focus": assessment_focus,
                    "complexity_assessment": {},
                    "context_score": 0.0,
                    "insights": [],
                    "patterns": [],
                    "error": str(e)
                }
        
        # Register the assess_complexity tool
        self.registry.register_tool(
            name="assess_complexity",
            handler=assess_complexity_handler,
            category="analysis",
            description="📊 Comprehensive complexity assessment with ContextAnalyzer integration. Evaluates cognitive load, technical complexity, emotional depth, and provides intelligent recommendations."
        )
    
    def _register_cursor_tools(self):
        """Register Cursor-specific tools"""
        
        async def code_analyze_handler(code_content: str, analysis_type: str = "comprehensive") -> dict:
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
        
        # Register the code_analyze tool
        self.registry.register_tool(
            name="code_analyze",
            handler=code_analyze_handler,
            category="cursor",
            description="💻 Code context and quality analysis with ContextAnalyzer integration. Analyzes code for patterns, complexity, best practices, and provides intelligent recommendations."
        )
        
        async def debug_intelligently_handler(code_content: str, error_message: str = "", context: str = "general") -> dict:
            """Intelligent debugging with ContextAnalyzer integration"""
            try:
                # Perform context analysis on the code and error
                combined_content = f"Code: {code_content}\nError: {error_message}\nContext: {context}"
                context_analysis = await self._analyze_context_directly(combined_content)
                
                # Analyze code patterns for debugging
                debug_patterns = self._analyze_debug_patterns(code_content, error_message)
                
                # Generate debugging recommendations
                debugging_recommendations = self._generate_debug_recommendations(debug_patterns, context_analysis)
                
                return {
                    "code_analyzed": code_content[:200] + "..." if len(code_content) > 200 else code_content,
                    "error_message": error_message,
                    "debug_context": context,
                    "debug_patterns": debug_patterns,
                    "recommendations": debugging_recommendations,
                    "context_enhancement": {
                        "context_score": context_analysis.get("context_score", 0.0),
                        "implicit_goals": context_analysis.get("context_layers", {}).get("implicit_goals", {}),
                        "complexity": context_analysis.get("context_layers", {}).get("complexity_level", {}),
                        "insights": context_analysis.get("insights", [])
                    },
                    "debugging_strategy": self._determine_debugging_strategy(debug_patterns, context_analysis)
                }
                
            except Exception as e:
                logger.error(f"Intelligent debugging error: {str(e)}")
                return {
                    "code_analyzed": code_content[:200] + "..." if len(code_content) > 200 else code_content,
                    "error_message": error_message,
                    "debug_context": context,
                    "error": str(e)
                }
        
        # Register the debug_intelligently tool
        self.registry.register_tool(
            name="debug_intelligently",
            handler=debug_intelligently_handler,
            category="cursor",
            description="🐛 Intelligent debugging with ContextAnalyzer integration. Analyzes code errors, identifies patterns, and provides strategic debugging recommendations."
        )
        
        async def refactor_safely_handler(code_content: str, refactor_goal: str, safety_level: str = "conservative") -> dict:
            """Safe code refactoring with ContextAnalyzer integration"""
            try:
                # Perform context analysis on the refactoring goal
                context_analysis = await self._analyze_context_directly(f"Refactor goal: {refactor_goal}")
                
                # Analyze current code structure
                code_structure = self._analyze_code_structure(code_content)
                
                # Generate safe refactoring plan
                refactoring_plan = self._generate_refactoring_plan(code_structure, refactor_goal, safety_level, context_analysis)
                
                # Assess refactoring risks
                risk_assessment = self._assess_refactoring_risks(code_structure, refactoring_plan, safety_level)
                
                return {
                    "code_to_refactor": code_content[:200] + "..." if len(code_content) > 200 else code_content,
                    "refactor_goal": refactor_goal,
                    "safety_level": safety_level,
                    "code_structure": code_structure,
                    "refactoring_plan": refactoring_plan,
                    "risk_assessment": risk_assessment,
                    "context_enhancement": {
                        "context_score": context_analysis.get("context_score", 0.0),
                        "implicit_goals": context_analysis.get("context_layers", {}).get("implicit_goals", {}),
                        "complexity": context_analysis.get("context_layers", {}).get("complexity_level", {}),
                        "insights": context_analysis.get("insights", [])
                    },
                    "safety_recommendations": self._generate_safety_recommendations(risk_assessment, safety_level)
                }
                
            except Exception as e:
                logger.error(f"Safe refactoring error: {str(e)}")
                return {
                    "code_to_refactor": code_content[:200] + "..." if len(code_content) > 200 else code_content,
                    "refactor_goal": refactor_goal,
                    "safety_level": safety_level,
                    "error": str(e)
                }
        
        # Register the refactor_safely tool
        self.registry.register_tool(
            name="refactor_safely",
            handler=refactor_safely_handler,
            category="cursor",
            description="🔧 Safe code refactoring with ContextAnalyzer integration. Analyzes code structure, generates refactoring plans, and assesses risks for safe code improvements."
        )
    
    def _register_context_tools(self):
        """Register dedicated context analysis tools"""
        
        async def analyze_context_comprehensive_handler(content: str, analysis_type: str = "comprehensive") -> dict:
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
        
        # Register the analyze_context_comprehensive tool
        self.registry.register_tool(
            name="analyze_context_comprehensive",
            handler=analyze_context_comprehensive_handler,
            category="context",
            description="🎯 Comprehensive context analysis using the full ContextAnalyzer module. Detects subtle patterns, implicit goals, complexity, uncertainty, and provides detailed insights."
        )
    
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
    
    # Helper methods for enhanced tools
    def _calculate_relevance_score(self, query: str, memory: Dict[str, Any], context_analysis: Dict[str, Any]) -> float:
        """Calculate relevance score for memory retrieval"""
        base_score = 0.5
        
        # Query content matching
        if query.lower() in str(memory).lower():
            base_score += 0.3
        
        # Context pattern matching
        if context_analysis.get("subtle_patterns"):
            for pattern in context_analysis["subtle_patterns"]:
                if pattern.lower() in str(memory).lower():
                    base_score += 0.2
        
        return min(1.0, base_score)
    
    def _matches_cleanup_criteria(self, memory: Dict[str, Any], criteria: str, context_analysis: Dict[str, Any]) -> bool:
        """Check if memory matches cleanup criteria"""
        criteria_lower = criteria.lower()
        memory_str = str(memory).lower()
        
        # Check if criteria appears in memory
        if criteria_lower in memory_str:
            return True
        
        # Check context patterns
        if context_analysis.get("subtle_patterns"):
            for pattern in context_analysis["subtle_patterns"]:
                if pattern.lower() in memory_str:
                    return True
        
        return False
    
    def _calculate_pattern_confidence(self, patterns: Dict[str, Any]) -> float:
        """Calculate confidence score for detected patterns"""
        total_patterns = 0
        confidence_sum = 0.0
        
        for pattern_type, pattern_data in patterns.items():
            if isinstance(pattern_data, list):
                total_patterns += len(pattern_data)
                confidence_sum += len(pattern_data) * 0.8
            elif isinstance(pattern_data, dict):
                total_patterns += 1
                confidence_sum += 0.9
        
        if total_patterns == 0:
            return 0.0
        
        return min(1.0, confidence_sum / total_patterns)
    
    def _assess_cognitive_load(self, content: str, complexity_score: float) -> Dict[str, Any]:
        """Assess cognitive load of content"""
        word_count = len(content.split())
        sentence_count = len(content.split('.'))
        
        return {
            "word_count": word_count,
            "sentence_count": sentence_count,
            "average_sentence_length": word_count / max(sentence_count, 1),
            "cognitive_load_level": "high" if complexity_score > 0.7 else "medium" if complexity_score > 0.4 else "low"
        }
    
    def _assess_technical_complexity(self, content: str) -> Dict[str, Any]:
        """Assess technical complexity of content"""
        technical_indicators = {
            "has_code": "def " in content or "class " in content or "import " in content,
            "has_technical_terms": any(term in content.lower() for term in ["algorithm", "architecture", "protocol", "api", "database"]),
            "has_numbers": any(char.isdigit() for char in content),
            "has_symbols": any(char in content for char in ["{", "}", "[", "]", "(", ")", "<", ">", "=", "+", "-", "*", "/"])
        }
        
        technical_score = sum(technical_indicators.values()) / len(technical_indicators)
        
        return {
            "technical_score": technical_score,
            "indicators": technical_indicators,
            "complexity_level": "high" if technical_score > 0.7 else "medium" if technical_score > 0.4 else "low"
        }
    
    def _assess_emotional_complexity(self, context_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Assess emotional complexity from context analysis"""
        emotional_context = context_analysis.get("context_layers", {}).get("emotional_context", {})
        
        return {
            "emotional_depth": emotional_context.get("depth", "unknown"),
            "emotional_intensity": emotional_context.get("intensity", "unknown"),
            "emotional_patterns": emotional_context.get("patterns", []),
            "complexity_level": "high" if len(emotional_context.get("patterns", [])) > 3 else "medium" if len(emotional_context.get("patterns", [])) > 1 else "low"
        }
    
    def _assess_contextual_complexity(self, context_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Assess contextual complexity from context analysis"""
        context_layers = context_analysis.get("context_layers", {})
        
        layer_count = len([layer for layer in context_layers.values() if layer])
        pattern_count = len(context_analysis.get("subtle_patterns", []))
        
        return {
            "layer_count": layer_count,
            "pattern_count": pattern_count,
            "cross_domain_connections": len(context_layers.get("cross_domain", {}).get("connections", [])),
            "temporal_elements": len(context_layers.get("temporal_context", {}).get("elements", [])),
            "complexity_level": "high" if layer_count > 4 or pattern_count > 5 else "medium" if layer_count > 2 or pattern_count > 2 else "low"
        }
    
    def _generate_complexity_recommendations(self, complexity_score: float, complexity_level: str) -> List[str]:
        """Generate recommendations based on complexity assessment"""
        recommendations = []
        
        if complexity_score > 0.8:
            recommendations.extend([
                "Consider breaking this down into smaller, manageable pieces",
                "Provide additional context and examples",
                "Use visual aids or diagrams to clarify complex concepts"
            ])
        elif complexity_score > 0.5:
            recommendations.extend([
                "Add intermediate explanations for key concepts",
                "Provide step-by-step breakdowns where possible",
                "Include relevant examples to illustrate points"
            ])
        else:
            recommendations.extend([
                "Content is well-structured and accessible",
                "Consider adding more depth if needed for advanced users",
                "Maintain current clarity and organization"
            ])
        
        return recommendations
    
    def _analyze_debug_patterns(self, code_content: str, error_message: str) -> Dict[str, Any]:
        """Analyze code for debugging patterns"""
        patterns = {
            "syntax_errors": [],
            "logical_errors": [],
            "common_mistakes": [],
            "debugging_hints": []
        }
        
        # Check for common syntax issues
        if "def " in code_content and ":" not in code_content:
            patterns["syntax_errors"].append("Missing colon after function definition")
        
        if "if " in code_content and ":" not in code_content:
            patterns["syntax_errors"].append("Missing colon after if statement")
        
        # Check for common logical issues
        if "while True:" in code_content and "break" not in code_content:
            patterns["logical_errors"].append("Potential infinite loop - check for break statement")
        
        if "except:" in code_content:
            patterns["common_mistakes"].append("Bare except clause - consider specific exception handling")
        
        # Add debugging hints based on error message
        if "NameError" in error_message:
            patterns["debugging_hints"].append("Check variable names and scope")
        elif "TypeError" in error_message:
            patterns["debugging_hints"].append("Check data types and function arguments")
        elif "AttributeError" in error_message:
            patterns["debugging_hints"].append("Check object attributes and method names")
        
        return patterns
    
    def _generate_debug_recommendations(self, debug_patterns: Dict[str, Any], context_analysis: Dict[str, Any]) -> List[str]:
        """Generate debugging recommendations"""
        recommendations = []
        
        # Add recommendations based on patterns
        for error_type, errors in debug_patterns.items():
            if errors:
                recommendations.extend(errors)
        
        # Add context-based recommendations
        if context_analysis.get("context_layers", {}).get("complexity_level", {}).get("level") == "high":
            recommendations.append("Consider breaking complex logic into smaller functions for easier debugging")
        
        if context_analysis.get("subtle_patterns"):
            recommendations.append("Review subtle patterns that might indicate underlying issues")
        
        return recommendations
    
    def _determine_debugging_strategy(self, debug_patterns: Dict[str, Any], context_analysis: Dict[str, Any]) -> str:
        """Determine the best debugging strategy"""
        if debug_patterns.get("syntax_errors"):
            return "syntax_focused"
        elif debug_patterns.get("logical_errors"):
            return "logic_analysis"
        elif debug_patterns.get("common_mistakes"):
            return "pattern_recognition"
        else:
            return "systematic_approach"
    
    def _analyze_code_structure(self, code_content: str) -> Dict[str, Any]:
        """Analyze code structure for refactoring"""
        structure = {
            "functions": [],
            "classes": [],
            "imports": [],
            "complexity_metrics": {},
            "refactoring_opportunities": []
        }
        
        lines = code_content.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            if line.startswith('def '):
                structure["functions"].append({
                    "line": i + 1,
                    "name": line.split('(')[0].replace('def ', ''),
                    "complexity": self._calculate_function_complexity(lines, i)
                })
            
            elif line.startswith('class '):
                structure["classes"].append({
                    "line": i + 1,
                    "name": line.split('(')[0].replace('class ', ''),
                    "complexity": self._calculate_class_complexity(lines, i)
                })
            
            elif line.startswith('import ') or line.startswith('from '):
                structure["imports"].append(line)
        
        # Identify refactoring opportunities
        if len(structure["functions"]) > 5:
            structure["refactoring_opportunities"].append("Consider grouping related functions into classes")
        
        if any(f["complexity"] > 0.7 for f in structure["functions"]):
            structure["refactoring_opportunities"].append("High complexity functions could be broken down")
        
        return structure
    
    def _calculate_function_complexity(self, lines: List[str], start_line: int) -> float:
        """Calculate complexity of a function"""
        complexity = 0.0
        nesting_level = 0
        
        for i in range(start_line, len(lines)):
            line = lines[i].strip()
            
            if line.startswith('def ') and i != start_line:
                break  # End of function
            
            if line.endswith(':'):
                nesting_level += 1
                complexity += 0.1 * nesting_level
            
            if line.startswith(('if ', 'for ', 'while ', 'try:', 'except')):
                complexity += 0.2
        
        return min(1.0, complexity)
    
    def _calculate_class_complexity(self, lines: List[str], start_line: int) -> float:
        """Calculate complexity of a class"""
        complexity = 0.0
        method_count = 0
        
        for i in range(start_line, len(lines)):
            line = lines[i].strip()
            
            if line.startswith('class ') and i != start_line:
                break  # End of class
            
            if line.startswith('def ') and 'self' in line:
                method_count += 1
                complexity += 0.1
        
        return min(1.0, complexity + method_count * 0.05)
    
    def _generate_refactoring_plan(self, code_structure: Dict[str, Any], refactor_goal: str, safety_level: str, context_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate refactoring plan"""
        plan = {
            "goal": refactor_goal,
            "safety_level": safety_level,
            "steps": [],
            "estimated_effort": "medium",
            "risk_level": "low"
        }
        
        # Generate steps based on goal and structure
        if "function" in refactor_goal.lower():
            for func in code_structure.get("functions", []):
                if func["complexity"] > 0.6:
                    plan["steps"].append(f"Break down function '{func['name']}' at line {func['line']}")
        
        if "class" in refactor_goal.lower():
            if len(code_structure.get("classes", [])) > 3:
                plan["steps"].append("Consider extracting common functionality into base classes")
        
        if "import" in refactor_goal.lower():
            if len(code_structure.get("imports", [])) > 10:
                plan["steps"].append("Organize imports and remove unused ones")
        
        # Adjust plan based on safety level
        if safety_level == "conservative":
            plan["steps"] = plan["steps"][:2]  # Limit to 2 steps for safety
            plan["risk_level"] = "very_low"
        elif safety_level == "aggressive":
            plan["steps"].extend(["Review all complex functions", "Consider architectural improvements"])
            plan["risk_level"] = "medium"
        
        return plan
    
    def _assess_refactoring_risks(self, code_structure: Dict[str, Any], refactoring_plan: Dict[str, Any], safety_level: str) -> Dict[str, Any]:
        """Assess risks of refactoring plan"""
        risks = {
            "breaking_changes": [],
            "complexity_increase": [],
            "testing_requirements": [],
            "overall_risk": "low"
        }
        
        # Assess risks based on plan steps
        for step in refactoring_plan.get("steps", []):
            if "function" in step.lower():
                risks["breaking_changes"].append("Function signature changes may break calling code")
                risks["testing_requirements"].append("Requires comprehensive function testing")
            
            if "class" in step.lower():
                risks["breaking_changes"].append("Class structure changes may affect inheritance")
                risks["testing_requirements"].append("Requires integration testing")
        
        # Adjust risk level based on safety level
        if safety_level == "conservative":
            risks["overall_risk"] = "very_low"
        elif safety_level == "aggressive":
            risks["overall_risk"] = "medium"
        
        return risks
    
    def _generate_safety_recommendations(self, risk_assessment: Dict[str, Any], safety_level: str) -> List[str]:
        """Generate safety recommendations for refactoring"""
        recommendations = []
        
        if risk_assessment.get("overall_risk") in ["medium", "high"]:
            recommendations.append("Create comprehensive test suite before refactoring")
            recommendations.append("Refactor in small, incremental steps")
            recommendations.append("Maintain backup of original code")
        
        if risk_assessment.get("breaking_changes"):
            recommendations.append("Review all calling code for potential breakage")
            recommendations.append("Consider maintaining backward compatibility")
        
        if safety_level == "aggressive":
            recommendations.append("Schedule refactoring during low-traffic periods")
            recommendations.append("Have rollback plan ready")
        
        return recommendations
