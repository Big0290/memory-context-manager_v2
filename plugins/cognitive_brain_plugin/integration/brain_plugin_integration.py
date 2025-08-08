"""
Brain Plugin Integration for MCP Server
Provides hooks and integration points to attach the cognitive brain plugin to the existing MCP server
"""

from datetime import datetime
from typing import Dict, Any, Optional, List
import asyncio
import json

from ..core.brain_core import CognitiveBrain
from ..adapters.memory_adapter import JsonFileStorageAdapter
from ..schemas.memory_schema import BrainState, ContextType, EmotionalWeight

# Import database adapter
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from database import get_brain_db


class DatabaseStorageAdapter:
    """Adapter to make our SQLite database work with the cognitive brain system"""
    
    def __init__(self, db):
        self.db = db
    
    def get_memory_store(self):
        """Get all memories in the format expected by the brain"""
        memory_data = self.db.get_memory_store()
        return memory_data.get("memory_store", {})
    
    def search_memories(self, query: str, limit: int = 10):
        """Search memories and return in brain-compatible format"""
        results = self.db.search_memory_store(query, limit)
        
        # Convert to brain-compatible format
        memories = []
        for result in results:
            memories.append({
                "key": result.get("key", ""),
                "content": result.get("value", ""),
                "tags": result.get("tags", []),
                "confidence": 1.0,  # Default confidence
                "emotional_weight": result.get("emotional_weight", "routine"),
                "timestamp": result.get("timestamp", "")
            })
        
        return {"memories": memories, "total_found": len(memories)}
    
    def store_memory(self, key: str, content: str, tags: list, emotional_weight: str = "routine"):
        """Store memory in database"""
        return self.db.set_memory_item(key, content, tags, emotional_weight)
    
    def get_brain_state(self):
        """Get brain state - using default for now"""
        brain_state_data = self.db.get_brain_state()
        
        # Convert to BrainState object if needed
        from ..schemas.memory_schema import BrainState
        
        return BrainState(
            active_identity=brain_state_data.get("active_identity", "default"),
            current_focus=brain_state_data.get("current_focus", "general"),
            memory_activity=brain_state_data.get("memory_activity", 0.5),
            emotion_activity=brain_state_data.get("emotion_activity", 0.5),
            last_reflection=None
        )
    
    def store_brain_state(self, brain_state):
        """Store brain state to database"""
        # Convert brain state to serializable format
        if hasattr(brain_state, 'dict'):
            state_data = brain_state.dict()
        else:
            state_data = brain_state
        
        # Convert any datetime objects to strings
        def make_serializable(obj):
            if hasattr(obj, 'isoformat'):
                return obj.isoformat()
            elif isinstance(obj, dict):
                return {k: make_serializable(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [make_serializable(v) for v in obj]
            else:
                return obj
        
        serializable_state = make_serializable(state_data)
        return self.db.update_brain_state(serializable_state)
    
    def get_recent_memories(self, hours: int = 24):
        """Get recent memories - simplified version"""
        # For now, just return empty list as this is mostly for debugging
        return []
    
    def get_all_identities(self):
        """Get all stored identities"""
        identities_data = self.db.get_brain_state().get("identities", {})
        return identities_data
    
    def store_identity(self, identity, identity_data: dict = None):
        """Store identity data"""
        # Handle IdentityProfile objects
        if hasattr(identity, 'dict'):
            # It's a Pydantic model (IdentityProfile)
            identity_data = identity.dict()
            identity_id = identity.id
        elif isinstance(identity, str):
            # It's an identity_id string
            identity_id = identity
            if identity_data is None:
                identity_data = {"id": identity_id, "stored": True}
        else:
            # Unknown format, try to handle gracefully
            identity_id = str(identity)
            identity_data = {"id": identity_id, "stored": True, "raw": str(identity)}
        
        # Store in brain state
        brain_state = self.db.get_brain_state()
        if "identities" not in brain_state:
            brain_state["identities"] = {}
        brain_state["identities"][identity_id] = identity_data
        return self.db.update_brain_state(brain_state)
    
    def get_context_history(self):
        """Get context history"""
        # Use brain state to get recent context or fallback
        try:
            brain_state = self.db.get_brain_state()
            return brain_state.get("context_history", [])
        except:
            return []
    
    def store_context(self, context_data: dict):
        """Store context data"""
        return self.db.add_context_history(context_data)
    
    def retrieve_identity(self, identity_id: str):
        """Retrieve identity by ID"""
        brain_state = self.db.get_brain_state()
        identities = brain_state.get("identities", {})
        if identity_id in identities:
            identity_data = identities[identity_id]
            # Convert back to IdentityProfile if needed
            from ..schemas.memory_schema import IdentityProfile
            try:
                return IdentityProfile(**identity_data)
            except:
                # If conversion fails, return None
                return None
        return None
    
    def save_brain_state(self, brain_state):
        """Save brain state - alias for store_brain_state"""
        return self.store_brain_state(brain_state)
    
    def store_task_context(self, task_context):
        """Store task context"""
        # For now, store in brain state
        brain_state = self.db.get_brain_state()
        if "tasks" not in brain_state:
            brain_state["tasks"] = {}
        
        if hasattr(task_context, 'dict'):
            task_data = task_context.dict()
            task_id = task_context.id
        else:
            task_data = task_context
            task_id = task_context.get('id', 'unknown')
            
        brain_state["tasks"][task_id] = task_data
        return self.db.update_brain_state(brain_state)
    
    def retrieve_task_context(self, task_id: str):
        """Retrieve task context by ID"""
        brain_state = self.db.get_brain_state()
        tasks = brain_state.get("tasks", {})
        if task_id in tasks:
            task_data = tasks[task_id]
            # Convert back to TaskContext if needed
            from ..schemas.memory_schema import TaskContext
            try:
                return TaskContext(**task_data)
            except:
                return None
        return None
    
    def get_active_tasks(self):
        """Get all active tasks"""
        brain_state = self.db.get_brain_state()
        tasks = brain_state.get("tasks", {})
        active_tasks = []
        for task_data in tasks.values():
            if task_data.get('status') == 'active':
                active_tasks.append(task_data)
        return active_tasks


class BrainPluginIntegration:
    """
    Integration layer that connects the cognitive brain plugin to the MCP server
    """
    
    def __init__(self, storage_dir: str = "brain_memory_store"):
        # Use database storage instead of JSON files
        self.db = get_brain_db()
        
        # Create a database adapter wrapper for the cognitive brain
        self.storage_adapter = DatabaseStorageAdapter(self.db)
        
        # Initialize cognitive brain
        self.brain = CognitiveBrain(self.storage_adapter)
        
        # Integration settings
        self.auto_analyze_enabled = True
        self.memory_threshold = 100  # Characters
        self.debug_mode = False
        
        # Hook registry
        self.pre_processing_hooks: List[callable] = []
        self.post_processing_hooks: List[callable] = []
        self.memory_hooks: List[callable] = []
    
    def register_with_server(self, mcp_server):
        """
        Register brain plugin with the MCP server
        """
        # Add brain-specific tools/resources
        self._register_brain_tools(mcp_server)
        
        # Hook into server lifecycle events
        self._register_lifecycle_hooks(mcp_server)
        
        # Initialize brain for this server instance
        self.brain.initialize()
        
        return True
    
    def _register_brain_tools(self, mcp_server):
        """Register brain-specific tools with the MCP server"""
        
        @mcp_server.tool("brain_analyze")
        async def brain_analyze_tool(content: str, context_type: str = "conversation") -> Dict[str, Any]:
            """
            Analyze content using the cognitive brain system
            
            Args:
                content: Text content to analyze
                context_type: Type of context (conversation, task, decision, etc.)
            
            Returns:
                Analysis results from the brain system
            """
            return await self.analyze_content(content, context_type)
        
        @mcp_server.tool("brain_remember")
        async def brain_remember_tool(content: str, tags: List[str] = None, 
                                    emotional_weight: str = "routine") -> Dict[str, Any]:
            """
            Store content in brain memory
            
            Args:
                content: Content to remember
                tags: Optional tags for categorization
                emotional_weight: Emotional importance (routine, important, critical, etc.)
            
            Returns:
                Memory storage confirmation
            """
            return await self.store_memory(content, tags or [], emotional_weight)
        
        @mcp_server.tool("brain_recall")
        async def brain_recall_tool(query: str, limit: int = 10) -> Dict[str, Any]:
            """
            Search and recall memories from the brain
            
            Args:
                query: Search query
                limit: Maximum number of memories to return
            
            Returns:
                Retrieved memories and relevance scores
            """
            return await self.recall_memories(query, limit)
        
        @mcp_server.tool("brain_reflect")
        async def brain_reflect_tool(focus_areas: List[str] = None, 
                                   period_hours: int = 24) -> Dict[str, Any]:
            """
            Trigger brain reflection and learning
            
            Args:
                focus_areas: Areas to focus reflection on (memories, tasks, emotions, decisions)
                period_hours: Time period to reflect on
            
            Returns:
                Reflection insights and suggestions
            """
            return await self.trigger_reflection(focus_areas or ["all"], period_hours)
        
        @mcp_server.tool("brain_status")
        async def brain_status_tool() -> Dict[str, Any]:
            """
            Get current brain status and activity
            
            Returns:
                Brain system status and module activity levels
            """
            return await self.get_brain_status()
        
        @mcp_server.tool("brain_debug")
        async def brain_debug_tool(enable: bool = None) -> Dict[str, Any]:
            """
            Control debug mode and get debug information
            
            Args:
                enable: Enable or disable debug mode (None to just get status)
            
            Returns:
                Debug information and current debug status
            """
            return await self.debug_brain(enable)
    
    def _register_lifecycle_hooks(self, mcp_server):
        """Register hooks for server lifecycle events"""
        
        # Hook into request processing
        original_handle_request = getattr(mcp_server, 'handle_request', None)
        if original_handle_request:
            async def enhanced_handle_request(request):
                # Pre-process with brain
                if self.auto_analyze_enabled:
                    await self._pre_process_request(request)
                
                # Execute original request
                response = await original_handle_request(request)
                
                # Post-process with brain
                if self.auto_analyze_enabled:
                    await self._post_process_response(request, response)
                
                return response
            
            mcp_server.handle_request = enhanced_handle_request
    
    async def analyze_content(self, content: str, context_type: str = "conversation") -> Dict[str, Any]:
        """
        Analyze content using the full brain system
        """
        if len(content) < self.memory_threshold:
            return {"analyzed": False, "reason": "Content too short for analysis"}
        
        # Route through frontal module for initial processing
        frontal_result = self._process_with_module("frontal_module", {
            "type": "analyze_content", 
            "content": content,
            "context_type": context_type
        })
        
        # Tag emotions
        emotion_result = self._process_with_module("emotion_tagger", {
            "type": "emotional_analysis",
            "content": content,
            "context_type": context_type
        })
        
        # Store in memory if significant
        if emotion_result.get("importance_score", 0) > 0.5:
            memory_result = self._process_with_module("memory_core", {
                "type": "store_memory",
                "content": content,
                "context_type": context_type,
                "emotional_weight": emotion_result.get("emotional_weight", "routine"),
                "tags": [context_type, "auto_analyzed"]
            })
        else:
            memory_result = {"stored": False, "reason": "Below significance threshold"}
        
        return {
            "analyzed": True,
            "timestamp": datetime.now().isoformat(),
            "frontal_analysis": frontal_result,
            "emotional_analysis": emotion_result,
            "memory_storage": memory_result,
            "brain_activity": self.get_brain_activity()
        }
    
    async def store_memory(self, content: str, tags: List[str], emotional_weight: str) -> Dict[str, Any]:
        """Store content in brain memory system"""
        return self._process_with_module("memory_core", {
            "type": "store_memory",
            "content": content,
            "tags": tags,
            "emotional_weight": emotional_weight,
            "context_type": "user_request"
        })
    
    async def recall_memories(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Search and recall memories"""
        # Use the database adapter directly for searching
        return self.storage_adapter.search_memories(query, limit)
    
    async def trigger_reflection(self, focus_areas: List[str], period_hours: int) -> Dict[str, Any]:
        """Trigger brain reflection process"""
        return self._process_with_module("self_reflector", {
            "type": "general_reflection",
            "focus_areas": focus_areas,
            "period_hours": period_hours
        })
    
    async def get_brain_status(self) -> Dict[str, Any]:
        """Get comprehensive brain status"""
        status = {
            "timestamp": datetime.now().isoformat(),
            "brain_active": self.brain.active,
            "auto_analyze_enabled": self.auto_analyze_enabled,
            "debug_mode": self.debug_mode,
            "modules": {}
        }
        
        # Get status from each module
        for module_name, module in self.brain.modules.items():
            status["modules"][module_name] = module.get_status()
        
        # Get brain state
        brain_state = self.brain.storage.get_brain_state()
        status["brain_state"] = {
            "active_identity": brain_state.active_identity,
            "current_focus": brain_state.current_focus,
            "memory_activity": brain_state.memory_activity,
            "emotion_activity": brain_state.emotion_activity,
            "last_reflection": brain_state.last_reflection.isoformat() if brain_state.last_reflection else None
        }
        
        return status
    
    async def debug_brain(self, enable: Optional[bool] = None) -> Dict[str, Any]:
        """Control and get debug information"""
        if enable is not None:
            self.debug_mode = enable
            self.brain.debug_mode = enable
        
        debug_info = {
            "debug_mode": self.debug_mode,
            "timestamp": datetime.now().isoformat()
        }
        
        if self.debug_mode:
            # Get detailed debug information
            debug_info.update({
                "recent_activities": self._get_recent_activities(),
                "memory_statistics": self._get_memory_statistics(),
                "module_activities": self._get_module_debug_info(),
                "brain_thoughts": self.brain.debug_thoughts() if hasattr(self.brain, 'debug_thoughts') else []
            })
        
        return debug_info
    
    def get_brain_activity(self) -> Dict[str, float]:
        """Get current activity levels of all brain modules"""
        activities = {}
        for module_name, module in self.brain.modules.items():
            activities[module_name] = module.activity_level
        return activities
    
    # Internal processing methods
    def _process_with_module(self, module_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input with a specific brain module"""
        if module_name not in self.brain.modules:
            return {"error": f"Module {module_name} not found"}
        
        module = self.brain.modules[module_name]
        brain_state = self.brain.storage.get_brain_state()
        
        try:
            result = module.process(input_data, brain_state)
            
            # Update brain state after processing
            self.brain.storage.store_brain_state(brain_state)
            
            return result
        except Exception as e:
            return {"error": f"Module processing failed: {str(e)}"}
    
    def _pre_process_request(self, request: Dict[str, Any]):
        """Pre-process incoming requests with brain analysis"""
        if self.debug_mode:
            print(f"[BRAIN] Pre-processing request: {request.get('method', 'unknown')}")
        
        # Analyze request context
        request_content = json.dumps(request, default=str)
        if len(request_content) > self.memory_threshold:
            self.analyze_content(request_content, "mcp_request")
    
    def _post_process_response(self, request: Dict[str, Any], response: Dict[str, Any]):
        """Post-process responses to learn from outcomes"""
        if self.debug_mode:
            print(f"[BRAIN] Post-processing response for: {request.get('method', 'unknown')}")
        
        # Learn from request-response patterns
        success_score = 1.0 if not response.get("error") else 0.3
        
        # Feed back to self-reflector for learning
        self._process_with_module("self_reflector", {
            "type": "pattern_analysis",
            "request_type": request.get("method", "unknown"),
            "success_score": success_score,
            "response_data": response
        })
    
    def _get_recent_activities(self) -> List[Dict[str, Any]]:
        """Get recent brain activities for debugging"""
        activities = []
        for module_name, module in self.brain.modules.items():
            if hasattr(module, 'last_activity'):
                activities.append({
                    "module": module_name,
                    "last_activity": module.last_activity.isoformat(),
                    "activity_level": module.activity_level
                })
        return sorted(activities, key=lambda x: x["last_activity"], reverse=True)
    
    def _get_memory_statistics(self) -> Dict[str, Any]:
        """Get memory system statistics"""
        recent_memories = self.storage_adapter.get_recent_memories(24)
        
        return {
            "total_memories_24h": len(recent_memories),
            "emotional_distribution": self._analyze_emotional_distribution(recent_memories),
            "context_distribution": self._analyze_context_distribution(recent_memories),
            "average_confidence": sum(m.confidence for m in recent_memories) / len(recent_memories) if recent_memories else 0
        }
    
    def _get_module_debug_info(self) -> Dict[str, Dict[str, Any]]:
        """Get debug information from all modules"""
        debug_info = {}
        for module_name, module in self.brain.modules.items():
            if hasattr(module, 'get_debug_info'):
                debug_info[module_name] = module.get_debug_info()
            else:
                debug_info[module_name] = {"status": "no debug info available"}
        return debug_info
    
    def _analyze_emotional_distribution(self, memories) -> Dict[str, int]:
        """Analyze emotional weight distribution in memories"""
        distribution = {}
        for memory in memories:
            weight = memory.emotional_weight.value
            distribution[weight] = distribution.get(weight, 0) + 1
        return distribution
    
    def _analyze_context_distribution(self, memories) -> Dict[str, int]:
        """Analyze context type distribution in memories"""
        distribution = {}
        for memory in memories:
            context = memory.context_type.value
            distribution[context] = distribution.get(context, 0) + 1
        return distribution
    
    # Hook management
    def add_pre_processing_hook(self, hook: callable):
        """Add a pre-processing hook"""
        self.pre_processing_hooks.append(hook)
    
    def add_post_processing_hook(self, hook: callable):
        """Add a post-processing hook"""
        self.post_processing_hooks.append(hook)
    
    def add_memory_hook(self, hook: callable):
        """Add a memory-related hook"""
        self.memory_hooks.append(hook)