"""
Cognitive Brain Plugin Adapter for MCP Server Plugin Manager
Integrates the brain-inspired cognitive system with the existing plugin architecture
"""

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
import logging
import asyncio

# Add the plugin package to the path
plugin_path = Path(__file__).parent / "cognitive_brain_plugin"
sys.path.insert(0, str(plugin_path))

# Import the plugin interface from src
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from plugin_interface import BasePlugin, PluginMetadata, ToolDefinition

logger = logging.getLogger(__name__)


class CognitiveBrainPlugin(BasePlugin):
    """
    Adapter that integrates the brain-inspired plugin with the MCP server plugin manager
    """
    
    def __init__(self):
        super().__init__()
        self._brain_integration = None
        self._config = {
            "storage_dir": "brain_memory_store",
            "auto_analyze": True,
            "debug_mode": False,
            "memory_threshold": 100
        }
    
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="cognitive_brain",
            version="1.0.0", 
            description="Brain-inspired memory and cognitive processing system with emotional weighting, self-reflection, and multi-agent capabilities",
            author="Brain Plugin Team",
            dependencies=["pydantic", "typing-extensions"]
        )
    
    def _setup(self) -> None:
        """Initialize the brain plugin system"""
        try:
            logger.info("Setting up Cognitive Brain Plugin...")
            
            # Import brain components
            from .cognitive_brain_plugin.integration.brain_plugin_integration import BrainPluginIntegration
            
            # Initialize brain integration
            storage_dir = self._config.get("storage_dir", "brain_memory_store")
            self._brain_integration = BrainPluginIntegration(storage_dir)
            
            # Configure brain settings
            self._brain_integration.auto_analyze_enabled = self._config.get("auto_analyze", True)
            self._brain_integration.debug_mode = self._config.get("debug_mode", False)
            self._brain_integration.memory_threshold = self._config.get("memory_threshold", 100)
            
            # Initialize brain system
            success = self._brain_integration.brain.initialize()
            if not success:
                raise Exception("Failed to initialize brain system")
            
            logger.info("✅ Cognitive Brain Plugin initialized successfully")
            logger.info(f"📊 Loaded {len(self._brain_integration.brain.modules)} brain modules")
            
        except Exception as e:
            logger.error(f"❌ Failed to setup Cognitive Brain Plugin: {str(e)}")
            raise
    
    def _teardown(self) -> None:
        """Cleanup brain plugin resources"""
        try:
            if self._brain_integration:
                self._brain_integration.brain.shutdown()
                logger.info("🧠 Cognitive Brain Plugin shutdown complete")
        except Exception as e:
            logger.error(f"Error during brain plugin teardown: {str(e)}")
    
    def get_tools(self) -> List[ToolDefinition]:
        """Get brain-specific tools"""
        if not self._brain_integration:
            return []
        
        tools = []
        
        # Brain Analysis Tool
        tools.append(ToolDefinition(
            name="brain_analyze",
            description="Analyze content using the cognitive brain system for emotional weight, importance, and contextual understanding",
            handler=self._brain_analyze_handler,
            parameters={
                "content": {"type": "string", "description": "Text content to analyze"},
                "context_type": {"type": "string", "description": "Type of context (conversation, task, decision, etc.)", "default": "conversation"}
            }
        ))
        
        # Memory Storage Tool
        tools.append(ToolDefinition(
            name="brain_remember",
            description="Store content in brain memory with emotional weighting and intelligent tagging",
            handler=self._brain_remember_handler,
            parameters={
                "content": {"type": "string", "description": "Content to remember"},
                "tags": {"type": "array", "description": "Optional tags for categorization", "default": []},
                "emotional_weight": {"type": "string", "description": "Emotional importance (routine, important, critical, positive, negative, novel)", "default": "routine"}
            }
        ))
        
        # Memory Recall Tool
        tools.append(ToolDefinition(
            name="brain_recall",
            description="Search and recall memories from the brain using contextual relevance",
            handler=self._brain_recall_handler,
            parameters={
                "query": {"type": "string", "description": "Search query"},
                "limit": {"type": "integer", "description": "Maximum number of memories to return", "default": 10}
            }
        ))
        
        # Reflection Tool
        tools.append(ToolDefinition(
            name="brain_reflect",
            description="Trigger brain reflection and learning to identify patterns and generate insights",
            handler=self._brain_reflect_handler,
            parameters={
                "focus_areas": {"type": "array", "description": "Areas to focus reflection on", "default": ["all"]},
                "period_hours": {"type": "integer", "description": "Time period to reflect on in hours", "default": 24}
            }
        ))
        
        # Status Tool
        tools.append(ToolDefinition(
            name="brain_status",
            description="Get current brain system status, activity levels, and module information",
            handler=self._brain_status_handler,
            parameters={}
        ))
        
        # Debug Tool
        tools.append(ToolDefinition(
            name="brain_debug",
            description="Control debug mode and get detailed brain introspection information",
            handler=self._brain_debug_handler,
            parameters={
                "enable": {"type": "boolean", "description": "Enable or disable debug mode", "required": False}
            }
        ))
        
        return tools
    
    # Tool Handlers
    async def _brain_analyze_handler(self, content: str, context_type: str = "conversation") -> Dict[str, Any]:
        """Handle brain content analysis"""
        try:
            result = await self._brain_integration.analyze_content(content, context_type)
            return {
                "success": True,
                "analysis": result,
                "module": "cognitive_brain"
            }
        except Exception as e:
            logger.error(f"Brain analyze error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "module": "cognitive_brain"
            }
    
    async def _brain_remember_handler(self, content: str, tags: List[str] = None, emotional_weight: str = "routine") -> Dict[str, Any]:
        """Handle memory storage"""
        try:
            result = await self._brain_integration.store_memory(content, tags or [], emotional_weight)
            return {
                "success": True,
                "memory_result": result,
                "module": "cognitive_brain"
            }
        except Exception as e:
            logger.error(f"Brain remember error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "module": "cognitive_brain"
            }
    
    async def _brain_recall_handler(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Handle memory recall"""
        try:
            result = await self._brain_integration.recall_memories(query, limit)
            return {
                "success": True,
                "recall_result": result,
                "module": "cognitive_brain"
            }
        except Exception as e:
            logger.error(f"Brain recall error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "module": "cognitive_brain"
            }
    
    async def _brain_reflect_handler(self, focus_areas: List[str] = None, period_hours: int = 24) -> Dict[str, Any]:
        """Handle brain reflection"""
        try:
            result = await self._brain_integration.trigger_reflection(focus_areas or ["all"], period_hours)
            return {
                "success": True,
                "reflection_result": result,
                "module": "cognitive_brain"
            }
        except Exception as e:
            logger.error(f"Brain reflect error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "module": "cognitive_brain"
            }
    
    async def _brain_status_handler(self) -> Dict[str, Any]:
        """Handle brain status request"""
        try:
            result = await self._brain_integration.get_brain_status()
            return {
                "success": True,
                "brain_status": result,
                "module": "cognitive_brain"
            }
        except Exception as e:
            logger.error(f"Brain status error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "module": "cognitive_brain"
            }
    
    async def _brain_debug_handler(self, enable: Optional[bool] = None) -> Dict[str, Any]:
        """Handle brain debug operations"""
        try:
            result = await self._brain_integration.debug_brain(enable)
            return {
                "success": True,
                "debug_info": result,
                "module": "cognitive_brain"
            }
        except Exception as e:
            logger.error(f"Brain debug error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "module": "cognitive_brain"
            }
    
    def on_server_startup(self) -> None:
        """Handle server startup event"""
        try:
            logger.info("🚀 Cognitive Brain Plugin: Server startup detected")
            if self._brain_integration and self._brain_integration.brain:
                # Start a session for the server
                self._brain_integration.brain.start_session("server_session")
                
                # Log initial brain status
                brain_status = self._brain_integration.brain.get_system_status()
                logger.info(f"🧠 Brain modules active: {len(brain_status['active_modules'])}")
        except Exception as e:
            logger.error(f"Error in brain plugin server startup: {str(e)}")
    
    def on_server_shutdown(self) -> None:
        """Handle server shutdown event"""
        try:
            logger.info("🛑 Cognitive Brain Plugin: Server shutdown detected")
            if self._brain_integration and self._brain_integration.brain:
                # End the server session
                self._brain_integration.brain.end_session("server_session")
                
                # Trigger final memory consolidation
                if "memory_core" in self._brain_integration.brain.modules:
                    self._brain_integration.brain.modules["memory_core"].process({
                        "type": "consolidate_memory",
                        "force": True
                    }, self._brain_integration.brain.state)
                
        except Exception as e:
            logger.error(f"Error in brain plugin server shutdown: {str(e)}")


# Make sure the plugin class is available for import
__all__ = ['CognitiveBrainPlugin']