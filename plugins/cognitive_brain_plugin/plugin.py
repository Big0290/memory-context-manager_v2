"""
Cognitive Brain Plugin for MCP Server
Main plugin registration and interface
"""

from typing import Dict, Any, Optional
import logging

from .integration.brain_plugin_integration import BrainPluginIntegration


class CognitiveBrainPlugin:
    """
    Main plugin class for the Cognitive Brain system
    Implements the plugin interface expected by the MCP server
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.name = "cognitive_brain"
        self.version = "1.0.0"
        self.description = "Brain-inspired memory and cognitive processing plugin"
        
        # Initialize integration layer
        storage_dir = self.config.get("storage_dir", "brain_memory_store")
        self.integration = BrainPluginIntegration(storage_dir)
        
        # Plugin state
        self.initialized = False
        self.logger = logging.getLogger(f"mcp.plugin.{self.name}")
    
    def get_info(self) -> Dict[str, Any]:
        """Get plugin information"""
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "author": "MCP Brain Plugin Team",
            "capabilities": [
                "memory_storage",
                "emotional_analysis", 
                "pattern_recognition",
                "self_reflection",
                "context_routing",
                "multi_agent_sync"
            ],
            "config_schema": {
                "storage_dir": {"type": "string", "default": "brain_memory_store"},
                "auto_analyze": {"type": "boolean", "default": True},
                "debug_mode": {"type": "boolean", "default": False},
                "memory_threshold": {"type": "integer", "default": 100}
            }
        }
    
    def initialize(self, mcp_server) -> bool:
        """
        Initialize the plugin with the MCP server
        
        Args:
            mcp_server: The MCP server instance
            
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            self.logger.info(f"Initializing {self.name} plugin...")
            
            # Configure integration layer
            self.integration.auto_analyze_enabled = self.config.get("auto_analyze", True)
            self.integration.debug_mode = self.config.get("debug_mode", False)
            self.integration.memory_threshold = self.config.get("memory_threshold", 100)
            
            # Register with server
            success = self.integration.register_with_server(mcp_server)
            
            if success:
                self.initialized = True
                self.logger.info(f"{self.name} plugin initialized successfully")
                return True
            else:
                self.logger.error(f"Failed to register {self.name} plugin with server")
                return False
                
        except Exception as e:
            self.logger.error(f"Error initializing {self.name} plugin: {str(e)}")
            return False
    
    def shutdown(self):
        """Shutdown the plugin gracefully"""
        try:
            self.logger.info(f"Shutting down {self.name} plugin...")
            
            # Save any pending data
            if hasattr(self.integration.brain, 'save_state'):
                self.integration.brain.save_state()
            
            self.initialized = False
            self.logger.info(f"{self.name} plugin shutdown complete")
            
        except Exception as e:
            self.logger.error(f"Error during {self.name} plugin shutdown: {str(e)}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current plugin status"""
        if not self.initialized:
            return {
                "name": self.name,
                "status": "not_initialized",
                "initialized": False
            }
        
        try:
            # Get brain status through integration layer
            brain_status = self.integration.get_brain_status()
            
            return {
                "name": self.name,
                "status": "active",
                "initialized": self.initialized,
                "version": self.version,
                "config": self.config,
                "brain_status": brain_status
            }
            
        except Exception as e:
            return {
                "name": self.name,
                "status": "error",
                "initialized": self.initialized,
                "error": str(e)
            }
    
    def handle_event(self, event_type: str, event_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Handle events from the MCP server
        
        Args:
            event_type: Type of event
            event_data: Event data
            
        Returns:
            Optional response data
        """
        if not self.initialized:
            return {"error": "Plugin not initialized"}
        
        try:
            if event_type == "request_processed":
                # Learn from request processing outcomes
                return self._handle_request_processed(event_data)
            
            elif event_type == "error_occurred":
                # Learn from errors for improvement
                return self._handle_error_occurred(event_data)
            
            elif event_type == "session_started":
                # New session - prepare brain context
                return self._handle_session_started(event_data)
            
            elif event_type == "session_ended":
                # Session ended - consolidate memories
                return self._handle_session_ended(event_data)
            
            else:
                self.logger.debug(f"Unhandled event type: {event_type}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error handling event {event_type}: {str(e)}")
            return {"error": str(e)}
    
    def _handle_request_processed(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle request processed event"""
        # This could trigger learning and pattern recognition
        request_type = event_data.get("request_type")
        success = event_data.get("success", True)
        
        # Feed to self-reflector for learning
        if hasattr(self.integration, '_process_with_module'):
            result = self.integration._process_with_module("self_reflector", {
                "type": "pattern_analysis",
                "request_type": request_type,
                "success_score": 1.0 if success else 0.3,
                "event_data": event_data
            })
            return {"processed": True, "learning_triggered": True}
        
        return {"processed": True}
    
    def _handle_error_occurred(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle error occurred event"""
        error_type = event_data.get("error_type")
        error_message = event_data.get("error_message")
        
        # Store error in memory for learning
        error_content = f"Error: {error_type} - {error_message}"
        
        if hasattr(self.integration, 'store_memory'):
            result = self.integration.store_memory(
                error_content, 
                ["error", "system_event"], 
                "critical"
            )
            return {"error_logged": True, "memory_stored": True}
        
        return {"error_logged": True}
    
    def _handle_session_started(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle session started event"""
        session_id = event_data.get("session_id")
        
        # Initialize session context in brain
        if hasattr(self.integration.brain, 'start_session'):
            self.integration.brain.start_session(session_id)
        
        return {"session_initialized": True, "session_id": session_id}
    
    def _handle_session_ended(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle session ended event"""
        session_id = event_data.get("session_id")
        
        # Trigger memory consolidation
        if hasattr(self.integration, '_process_with_module'):
            result = self.integration._process_with_module("memory_core", {
                "type": "consolidate_memory",
                "force": False
            })
            
            # Trigger reflection on session
            reflection_result = self.integration._process_with_module("self_reflector", {
                "type": "general_reflection",
                "focus_areas": ["memories", "decisions"],
                "period_hours": 1  # Just this session
            })
            
            return {
                "session_ended": True,
                "session_id": session_id,
                "consolidation_triggered": True,
                "reflection_triggered": True
            }
        
        return {"session_ended": True, "session_id": session_id}


# Plugin factory function
def create_plugin(config: Dict[str, Any] = None) -> CognitiveBrainPlugin:
    """
    Factory function to create a new plugin instance
    
    Args:
        config: Plugin configuration
        
    Returns:
        New plugin instance
    """
    return CognitiveBrainPlugin(config)


# Plugin metadata for registration
PLUGIN_METADATA = {
    "name": "cognitive_brain",
    "version": "1.0.0",
    "description": "Brain-inspired memory and cognitive processing plugin",
    "factory": create_plugin,
    "required_mcp_version": "1.0.0"
}