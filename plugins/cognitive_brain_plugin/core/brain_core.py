from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid

from ..schemas.memory_schema import BrainState, IdentityProfile
from ..adapters.memory_adapter import MemoryStorageAdapter


class BrainModule(ABC):
    """Base class for all brain modules"""
    
    def __init__(self, name: str, storage_adapter: MemoryStorageAdapter):
        self.name = name
        self.storage = storage_adapter
        self.active = True
        self.activity_level = 0.5
        self.last_activity = datetime.now()
    
    @abstractmethod
    def process(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Process input and return output"""
        pass
    
    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Get current module status"""
        pass
    
    def activate(self):
        """Activate this module"""
        self.active = True
        self.last_activity = datetime.now()
    
    def deactivate(self):
        """Deactivate this module"""
        self.active = False
    
    def set_activity_level(self, level: float):
        """Set activity level (0.0 to 1.0)"""
        self.activity_level = max(0.0, min(1.0, level))
        self.last_activity = datetime.now()


class CognitiveBrain:
    """Main brain orchestrator that coordinates all modules"""
    
    def __init__(self, storage_adapter: MemoryStorageAdapter):
        self.storage = storage_adapter
        self.modules: Dict[str, BrainModule] = {}
        self.state = self.storage.get_brain_state()
        self.debug_mode = False
        self.thought_trace: List[str] = []
        self.active = True
        
        # Load or create default identity
        self._setup_default_identity()
    
    def _setup_default_identity(self):
        """Setup default identity if none exists"""
        identities = self.storage.get_all_identities()
        if not identities:
            default_identity = IdentityProfile(
                id="default",
                name="Default Assistant",
                description="Default cognitive identity",
                preferred_reasoning_style="analytical",
                emotional_baseline={"curiosity": 0.7, "helpfulness": 0.8, "caution": 0.6},
                memory_retention_strategy="importance_based"
            )
            self.storage.store_identity(default_identity)
            self.state.active_identity = "default"
        else:
            self.state.active_identity = identities[0].id
    
    def register_module(self, module: BrainModule):
        """Register a brain module"""
        self.modules[module.name] = module
        self._log_thought(f"Registered module: {module.name}")
    
    def unregister_module(self, module_name: str):
        """Unregister a brain module"""
        if module_name in self.modules:
            del self.modules[module_name]
            self._log_thought(f"Unregistered module: {module_name}")
    
    def set_debug_mode(self, enabled: bool):
        """Enable/disable debug mode for thought tracing"""
        self.debug_mode = enabled
        self.state.debug_mode = enabled
        if not enabled:
            self.thought_trace.clear()
            self.state.thought_trace.clear()
    
    def _log_thought(self, thought: str):
        """Log a thought for debugging"""
        if self.debug_mode:
            timestamp = datetime.now().isoformat()
            thought_entry = f"[{timestamp}] {thought}"
            self.thought_trace.append(thought_entry)
            self.state.thought_trace.append(thought_entry)
            
            # Keep only recent thoughts
            if len(self.thought_trace) > 100:
                self.thought_trace = self.thought_trace[-50:]
                self.state.thought_trace = self.state.thought_trace[-50:]
    
    def process_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input through the brain modules"""
        self._log_thought(f"Processing input: {input_data.get('type', 'unknown')}")
        
        # Update brain state
        self.state.frontal_activity = 0.8  # High activity during processing
        
        # Route through active modules
        results = {}
        for module_name, module in self.modules.items():
            if module.active:
                try:
                    self._log_thought(f"Routing to module: {module_name}")
                    module_result = module.process(input_data, self.state)
                    results[module_name] = module_result
                    
                    # Update module activity
                    module.set_activity_level(0.7)
                    
                except Exception as e:
                    self._log_thought(f"Error in module {module_name}: {str(e)}")
                    results[module_name] = {"error": str(e)}
        
        # Save updated state
        self._save_state()
        
        return {
            "results": results,
            "brain_state": self.state.dict(),
            "debug_thoughts": self.thought_trace if self.debug_mode else None
        }
    
    def switch_identity(self, identity_id: str) -> bool:
        """Switch to a different identity context"""
        identity = self.storage.retrieve_identity(identity_id)
        if identity:
            self.state.active_identity = identity_id
            identity.last_active = datetime.now()
            self.storage.store_identity(identity)
            self._log_thought(f"Switched to identity: {identity.name}")
            self._save_state()
            return True
        return False
    
    def get_active_identity(self) -> Optional[IdentityProfile]:
        """Get the currently active identity"""
        if self.state.active_identity:
            return self.storage.retrieve_identity(self.state.active_identity)
        return None
    
    def start_task(self, task_name: str, description: str = "") -> str:
        """Start a new task context"""
        task_id = f"task_{uuid.uuid4().hex[:8]}"
        
        from ..schemas.memory_schema import TaskContext
        task = TaskContext(
            id=task_id,
            name=task_name,
            description=description,
            status="active",
            priority=0.7
        )
        
        self.storage.store_task_context(task)
        self.state.active_task_id = task_id
        
        self._log_thought(f"Started new task: {task_name}")
        self._save_state()
        
        return task_id
    
    def complete_task(self, task_id: str, outcome: str = "") -> bool:
        """Complete a task and record outcomes"""
        task = self.storage.retrieve_task_context(task_id)
        if task:
            task.status = "completed"
            task.completed_at = datetime.now()
            
            if outcome:
                task.outcomes.append({
                    "outcome": outcome,
                    "timestamp": datetime.now().isoformat()
                })
            
            self.storage.store_task_context(task)
            
            if self.state.active_task_id == task_id:
                self.state.active_task_id = None
            
            self._log_thought(f"Completed task: {task.name}")
            self._save_state()
            
            return True
        return False
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        active_modules = [name for name, module in self.modules.items() if module.active]
        module_status = {name: module.get_status() for name, module in self.modules.items()}
        
        active_identity = self.get_active_identity()
        active_task = None
        if self.state.active_task_id:
            active_task = self.storage.retrieve_task_context(self.state.active_task_id)
        
        return {
            "brain_state": self.state.dict(),
            "active_modules": active_modules,
            "module_details": module_status,
            "active_identity": active_identity.dict() if active_identity else None,
            "active_task": active_task.dict() if active_task else None,
            "total_modules": len(self.modules),
            "debug_mode": self.debug_mode,
            "recent_thoughts": self.thought_trace[-10:] if self.debug_mode else None
        }
    
    def trigger_reflection(self, trigger: str) -> str:
        """Trigger a self-reflection process"""
        self._log_thought(f"Triggering reflection: {trigger}")
        
        # This will be implemented by the SelfReflector module
        if "self_reflector" in self.modules:
            reflection_input = {
                "type": "reflection_trigger",
                "trigger": trigger,
                "recent_memories": self.storage.get_recent_memories(24),
                "active_tasks": self.storage.get_active_tasks()
            }
            
            result = self.modules["self_reflector"].process(reflection_input, self.state)
            return result.get("reflection_id", "")
        
        return ""
    
    def _save_state(self):
        """Save current brain state to storage"""
        self.storage.save_brain_state(self.state)
    
    def debug_thoughts(self) -> List[str]:
        """Get recent debug thoughts"""
        return self.thought_trace.copy()
    
    def initialize(self) -> bool:
        """Initialize the brain system"""
        try:
            self._log_thought("Initializing brain system")
            
            # Initialize all modules
            from ..modules.frontal_module import FrontalModule
            from ..modules.memory_core import MemoryCore
            from ..modules.emotion_tagger import EmotionTagger
            from ..modules.router import Router
            from ..modules.self_reflector import SelfReflector
            from ..modules.sync_bridge import SyncBridge
            from ..modules.context_analyzer import ContextAnalyzer
            
            # Register modules
            self.register_module(FrontalModule(self.storage))
            self.register_module(MemoryCore(self.storage))
            self.register_module(EmotionTagger(self.storage))
            self.register_module(Router(self.storage))
            self.register_module(SelfReflector(self.storage))
            self.register_module(SyncBridge(self.storage))
            self.register_module(ContextAnalyzer(self.storage))
            
            self._log_thought("All modules registered successfully")
            self._save_state()
            
            return True
            
        except Exception as e:
            self._log_thought(f"Brain initialization failed: {str(e)}")
            return False
    
    def start_session(self, session_id: str):
        """Start a new session context"""
        self.state.current_session_id = session_id
        self.state.session_start_time = datetime.now()
        self._log_thought(f"Started session: {session_id}")
        self._save_state()
    
    def end_session(self, session_id: str):
        """End current session and consolidate memories"""
        if self.state.current_session_id == session_id:
            self.state.current_session_id = None
            self._log_thought(f"Ended session: {session_id}")
            
            # Trigger memory consolidation
            if "memory_core" in self.modules:
                self.modules["memory_core"].process({
                    "type": "consolidate_memory",
                    "force": False
                }, self.state)
            
            self._save_state()
    
    def save_state(self):
        """Public method to save brain state"""
        self._save_state()
    
    def shutdown(self):
        """Shutdown the brain system gracefully"""
        self._log_thought("Shutting down brain system")
        
        # Deactivate all modules
        for module in self.modules.values():
            module.deactivate()
        
        # Save final state
        self.state.frontal_activity = 0.0
        self.state.memory_activity = 0.0
        self.state.emotion_activity = 0.0
        self._save_state()
        
        self._log_thought("Brain system shutdown complete")