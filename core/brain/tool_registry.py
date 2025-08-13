"""
Comprehensive Tool Registry System
Standardized tool registration for agent-friendly cognitive functions
"""

import logging
from typing import Dict, Any, List, Optional, Callable
from mcp.server.fastmcp import FastMCP
from datetime import datetime

logger = logging.getLogger(__name__)

class ToolRegistry:
    """Standardized tool registry for agent-friendly cognitive functions"""
    
    def __init__(self, mcp_server: FastMCP):
        self.mcp = mcp_server
        self.registered_tools = {}
        self.tool_categories = {}
        self.tool_metadata = {}
        
    def register_tool(self, 
                     name: str, 
                     handler: Callable, 
                     description: str,
                     category: str = "general",
                     complexity: str = "intermediate",
                     examples: List[str] = None,
                     dependencies: List[str] = None,
                     performance_metrics: List[str] = None) -> bool:
        """
        Register a tool with comprehensive metadata
        
        Args:
            name: Tool name (agent-friendly)
            handler: Async function that implements the tool
            description: Clear description of what the tool does
            category: Tool category (analysis, memory, learning, monitoring)
            complexity: Complexity level (basic, intermediate, advanced)
            examples: List of usage examples
            dependencies: List of system dependencies
            performance_metrics: List of metrics to track
        """
        try:
            # Store tool metadata
            self.tool_metadata[name] = {
                "description": description,
                "category": category,
                "complexity": complexity,
                "examples": examples or [],
                "dependencies": dependencies or [],
                "performance_metrics": performance_metrics or [],
                "registered_at": datetime.now().isoformat()
            }
            
            # Register with MCP server
            self.mcp.tool()(handler)
            
            # Store in our registry
            self.registered_tools[name] = handler
            
            # Add to category
            if category not in self.tool_categories:
                self.tool_categories[category] = []
            self.tool_categories[category].append(name)
            
            logger.info(f"✅ Registered tool: {name} ({category}/{complexity})")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to register tool {name}: {str(e)}")
            return False
    
    def register_brain_tools(self, brain_interface) -> Dict[str, bool]:
        """Register all brain interface tools with standardized metadata"""
        
        # Define our agent-friendly tools with rich metadata
        brain_tools = [
            {
                "name": "analyze_with_context",
                "handler": brain_interface.analyze_with_context,
                "description": "🧠 Analyze any topic with deep context understanding and background processing",
                "category": "analysis",
                "complexity": "advanced",
                "examples": [
                    "analyze_with_context: Analyze this problem with deep context",
                    "analyze_with_context: Reflect on our conversation progress",
                    "analyze_with_context: System analysis and optimization assessment"
                ],
                "dependencies": ["memory_system", "context_analyzer", "enhanced_thinking_system"],
                "performance_metrics": ["thinking_effectiveness", "context_score", "response_time"]
            },
            {
                "name": "store_knowledge",
                "handler": brain_interface.store_knowledge,
                "description": "💾 Store important information with emotional weighting and context analysis",
                "category": "memory",
                "complexity": "intermediate",
                "examples": [
                    "store_knowledge: Store this important fact",
                    "store_knowledge: Remember this user preference",
                    "store_knowledge: Save this technical insight"
                ],
                "dependencies": ["memory_system", "context_analyzer"],
                "performance_metrics": ["storage_success", "emotional_weight", "context_score"]
            },
            {
                "name": "search_memories",
                "handler": brain_interface.search_memories,
                "description": "🔍 Search through stored memories with contextual relevance scoring",
                "category": "memory",
                "complexity": "intermediate",
                "examples": [
                    "search_memories: Search for previous conversations about AI",
                    "search_memories: Find memories related to web development",
                    "search_memories: Comprehensive search for project insights"
                ],
                "dependencies": ["memory_system", "context_analyzer"],
                "performance_metrics": ["relevance_score", "search_depth", "context_effectiveness"]
            },
            {
                "name": "process_background",
                "handler": brain_interface.process_background,
                "description": "💤 Process information in background with memory consolidation and optimization",
                "category": "memory",
                "complexity": "advanced",
                "examples": [
                    "process_background: Consolidate recent memories",
                    "process_background: Background processing and optimization",
                    "process_background: Memory pattern analysis and synthesis"
                ],
                "dependencies": ["enhanced_dream_system", "memory_system"],
                "performance_metrics": ["dream_effectiveness", "consolidation_impact", "context_injection_score"]
            },
            {
                "name": "self_assess",
                "handler": brain_interface.self_assess,
                "description": "🤔 Perform self-assessment and metacognitive analysis",
                "category": "analysis",
                "complexity": "intermediate",
                "examples": [
                    "self_assess: Analyze my recent performance",
                    "self_assess: Self-assessment and improvement planning",
                    "self_assess: Metacognitive analysis of learning patterns"
                ],
                "dependencies": ["memory_system", "context_analyzer"],
                "performance_metrics": ["reflection_depth", "insights_generated", "improvement_actions"]
            },
            {
                "name": "learn_from_content",
                "handler": brain_interface.learn_from_content,
                "description": "📚 Learn and integrate new information with context analysis",
                "category": "learning",
                "complexity": "intermediate",
                "examples": [
                    "learn_from_content: Process this new information",
                    "learn_from_content: Integrate this knowledge into memory",
                    "learn_from_content: Learn from this conversation"
                ],
                "dependencies": ["memory_system", "knowledge_ingestion"],
                "performance_metrics": ["learning_success", "knowledge_integration", "memory_impact"]
            },
            {
                "name": "check_system_status",
                "handler": brain_interface.check_system_status,
                "description": "📊 Check current system status, consciousness, and cognitive load",
                "category": "monitoring",
                "complexity": "basic",
                "examples": [
                    "check_system_status: Check my current mental state",
                    "check_system_status: Assess cognitive load and awareness",
                    "check_system_status: Monitor system consciousness status"
                ],
                "dependencies": ["memory_system", "context_analyzer"],
                "performance_metrics": ["consciousness_level", "cognitive_load", "awareness_score"]
            },
            {
                "name": "get_memory_statistics",
                "handler": brain_interface.get_memory_statistics,
                "description": "📈 Get comprehensive memory system statistics, health, and performance metrics",
                "category": "monitoring",
                "complexity": "basic",
                "examples": [
                    "get_memory_statistics: Get memory system statistics",
                    "get_memory_statistics: Check database health and performance",
                    "get_memory_statistics: Monitor memory growth and usage"
                ],
                "dependencies": ["memory_system", "database"],
                "performance_metrics": ["memory_count", "database_health", "growth_rate"]
            },
            {
                "name": "analyze_dream_system",
                "handler": brain_interface.analyze_dream_system,
                "description": "🧠 Analyze dream system effectiveness and context injection optimization",
                "category": "analysis",
                "complexity": "advanced",
                "examples": [
                    "analyze_dream_system: Analyze dream system effectiveness",
                    "analyze_dream_system: Check context injection optimization",
                    "analyze_dream_system: Dream system performance metrics"
                ],
                "dependencies": ["enhanced_dream_system", "memory_system"],
                "performance_metrics": ["dream_effectiveness", "context_injection_score", "optimization_opportunities"]
            },
            {
                "name": "analyze_system_performance",
                "handler": brain_interface.analyze_system_performance,
                "description": "⚡ Comprehensive system performance analysis and optimization assessment",
                "category": "analysis",
                "complexity": "advanced",
                "examples": [
                    "analyze_system_performance: Complete system analysis",
                    "analyze_system_performance: Background process optimization",
                    "analyze_system_performance: Iteration loop analysis"
                ],
                "dependencies": ["enhanced_thinking_system", "memory_system"],
                "performance_metrics": ["optimization_score", "background_health", "iteration_effectiveness"]
            }
        ]
        
        # Register each tool
        registration_results = {}
        for tool_def in brain_tools:
            success = self.register_tool(
                name=tool_def["name"],
                handler=tool_def["handler"],
                description=tool_def["description"],
                category=tool_def["category"],
                complexity=tool_def["complexity"],
                examples=tool_def["examples"],
                dependencies=tool_def["dependencies"],
                performance_metrics=tool_def["performance_metrics"]
            )
            registration_results[tool_def["name"]] = success
        
        # Log registration summary
        successful_registrations = sum(registration_results.values())
        total_tools = len(brain_tools)
        
        logger.info(f"🧠 Brain tools registration complete: {successful_registrations}/{total_tools} tools registered")
        
        if successful_registrations == total_tools:
            logger.info("🎉 All agent-friendly brain tools successfully registered!")
        else:
            failed_tools = [name for name, success in registration_results.items() if not success]
            logger.warning(f"⚠️ Failed to register tools: {failed_tools}")
        
        return registration_results
    
    def get_tool_info(self) -> Dict[str, Any]:
        """Get comprehensive information about registered tools"""
        return {
            "total_tools": len(self.registered_tools),
            "tool_categories": self.tool_categories,
            "tool_metadata": self.tool_metadata,
            "complexity_distribution": self._get_complexity_distribution(),
            "category_distribution": self._get_category_distribution(),
            "registration_status": {
                "total_registered": len(self.registered_tools),
                "total_expected": 10,  # We expect 10 brain tools
                "success_rate": len(self.registered_tools) / 10 if 10 > 0 else 0
            }
        }
    
    def _get_complexity_distribution(self) -> Dict[str, int]:
        """Get distribution of tools by complexity level"""
        distribution = {}
        for metadata in self.tool_metadata.values():
            complexity = metadata.get("complexity", "unknown")
            distribution[complexity] = distribution.get(complexity, 0) + 1
        return distribution
    
    def _get_category_distribution(self) -> Dict[str, int]:
        """Get distribution of tools by category"""
        distribution = {}
        for metadata in self.tool_metadata.values():
            category = metadata.get("category", "unknown")
            distribution[category] = distribution.get(category, 0) + 1
        return distribution
    
    def list_tools(self) -> List[str]:
        """Get list of all registered tool names"""
        return list(self.registered_tools.keys())
    
    def get_tool_metadata(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """Get metadata for a specific tool"""
        return self.tool_metadata.get(tool_name)
    
    def is_tool_registered(self, tool_name: str) -> bool:
        """Check if a tool is registered"""
        return tool_name in self.registered_tools
    
    def get_tools_by_category(self, category: str) -> List[str]:
        """Get all tools in a specific category"""
        return self.tool_categories.get(category, [])
    
    def get_tools_by_complexity(self, complexity: str) -> List[str]:
        """Get all tools with a specific complexity level"""
        tools = []
        for name, metadata in self.tool_metadata.items():
            if metadata.get("complexity") == complexity:
                tools.append(name)
        return tools
