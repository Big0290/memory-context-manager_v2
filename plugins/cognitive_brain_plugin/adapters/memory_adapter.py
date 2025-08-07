import json
import os
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
import hashlib
from ..schemas.memory_schema import (
    MemoryChunk, TaskContext, ReflectionEntry, 
    BrainState, IdentityProfile, EmotionalWeight, ContextType
)


class MemoryStorageAdapter(ABC):
    """Abstract adapter for different storage backends"""
    
    @abstractmethod
    def store_memory_chunk(self, chunk: MemoryChunk) -> str:
        pass
    
    @abstractmethod
    def retrieve_memory_chunk(self, chunk_id: str) -> Optional[MemoryChunk]:
        pass
    
    @abstractmethod
    def search_memories(self, query: str, limit: int = 10) -> List[MemoryChunk]:
        pass
    
    @abstractmethod
    def get_memories_by_emotional_weight(self, weight: EmotionalWeight) -> List[MemoryChunk]:
        pass
    
    @abstractmethod
    def get_memories_by_context_type(self, context_type: ContextType) -> List[MemoryChunk]:
        pass


class JsonFileStorageAdapter(MemoryStorageAdapter):
    """File-based storage adapter using JSON (integrates with existing memory system)"""
    
    def __init__(self, storage_dir: str = "brain_memory_store"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        
        # Storage files
        self.memories_file = self.storage_dir / "memories.json"
        self.tasks_file = self.storage_dir / "tasks.json"
        self.reflections_file = self.storage_dir / "reflections.json"
        self.brain_state_file = self.storage_dir / "brain_state.json"
        self.identities_file = self.storage_dir / "identities.json"
        
        # In-memory caches for performance
        self._memory_cache: Dict[str, MemoryChunk] = {}
        self._task_cache: Dict[str, TaskContext] = {}
        self._reflection_cache: Dict[str, ReflectionEntry] = {}
        self._identity_cache: Dict[str, IdentityProfile] = {}
        
        self._load_all_data()
    
    def _load_all_data(self):
        """Load all data from storage into memory"""
        self._load_memories()
        self._load_tasks()
        self._load_reflections()
        self._load_identities()
    
    def _load_memories(self):
        """Load memories from storage"""
        if self.memories_file.exists():
            try:
                with open(self.memories_file, 'r') as f:
                    data = json.load(f)
                    for chunk_data in data.get('memories', []):
                        chunk = MemoryChunk(**chunk_data)
                        self._memory_cache[chunk.id] = chunk
            except (json.JSONDecodeError, Exception) as e:
                print(f"Warning: Could not load memories: {e}")
    
    def _save_memories(self):
        """Save memories to storage"""
        data = {
            'memories': [chunk.dict() for chunk in self._memory_cache.values()],
            'last_updated': datetime.now().isoformat()
        }
        with open(self.memories_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def _load_tasks(self):
        """Load tasks from storage"""
        if self.tasks_file.exists():
            try:
                with open(self.tasks_file, 'r') as f:
                    data = json.load(f)
                    for task_data in data.get('tasks', []):
                        task = TaskContext(**task_data)
                        self._task_cache[task.id] = task
            except (json.JSONDecodeError, Exception) as e:
                print(f"Warning: Could not load tasks: {e}")
    
    def _save_tasks(self):
        """Save tasks to storage"""
        data = {
            'tasks': [task.dict() for task in self._task_cache.values()],
            'last_updated': datetime.now().isoformat()
        }
        with open(self.tasks_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def _load_reflections(self):
        """Load reflections from storage"""
        if self.reflections_file.exists():
            try:
                with open(self.reflections_file, 'r') as f:
                    data = json.load(f)
                    for reflection_data in data.get('reflections', []):
                        reflection = ReflectionEntry(**reflection_data)
                        self._reflection_cache[reflection.id] = reflection
            except (json.JSONDecodeError, Exception) as e:
                print(f"Warning: Could not load reflections: {e}")
    
    def _save_reflections(self):
        """Save reflections to storage"""
        data = {
            'reflections': [reflection.dict() for reflection in self._reflection_cache.values()],
            'last_updated': datetime.now().isoformat()
        }
        with open(self.reflections_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def _load_identities(self):
        """Load identities from storage"""
        if self.identities_file.exists():
            try:
                with open(self.identities_file, 'r') as f:
                    data = json.load(f)
                    for identity_data in data.get('identities', []):
                        identity = IdentityProfile(**identity_data)
                        self._identity_cache[identity.id] = identity
            except (json.JSONDecodeError, Exception) as e:
                print(f"Warning: Could not load identities: {e}")
    
    def _save_identities(self):
        """Save identities to storage"""
        data = {
            'identities': [identity.dict() for identity in self._identity_cache.values()],
            'last_updated': datetime.now().isoformat()
        }
        with open(self.identities_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def get_brain_state(self) -> BrainState:
        """Get current brain state"""
        if self.brain_state_file.exists():
            try:
                with open(self.brain_state_file, 'r') as f:
                    data = json.load(f)
                    return BrainState(**data)
            except (json.JSONDecodeError, Exception) as e:
                print(f"Warning: Could not load brain state: {e}")
        
        return BrainState()
    
    def save_brain_state(self, state: BrainState):
        """Save brain state"""
        with open(self.brain_state_file, 'w') as f:
            json.dump(state.dict(), f, indent=2, default=str)
    
    # Memory operations
    def store_memory_chunk(self, chunk: MemoryChunk) -> str:
        """Store a memory chunk"""
        if not chunk.id:
            # Generate ID from content hash
            content_hash = hashlib.md5(chunk.content.encode()).hexdigest()
            chunk.id = f"mem_{content_hash[:8]}_{int(datetime.now().timestamp())}"
        
        self._memory_cache[chunk.id] = chunk
        self._save_memories()
        return chunk.id
    
    def retrieve_memory_chunk(self, chunk_id: str) -> Optional[MemoryChunk]:
        """Retrieve a specific memory chunk"""
        chunk = self._memory_cache.get(chunk_id)
        if chunk:
            chunk.update_access()
            self._save_memories()
        return chunk
    
    def search_memories(self, query: str, limit: int = 10) -> List[MemoryChunk]:
        """Search memories by content, tags, or keywords"""
        query_lower = query.lower()
        matches = []
        
        for chunk in self._memory_cache.values():
            score = 0
            
            # Content matching
            if query_lower in chunk.content.lower():
                score += 3
            
            # Tag matching
            for tag in chunk.tags:
                if query_lower in tag.lower():
                    score += 2
            
            # Keyword matching
            for keyword in chunk.keywords:
                if query_lower in keyword.lower():
                    score += 1
            
            # Summary matching
            if chunk.summary and query_lower in chunk.summary.lower():
                score += 2
            
            if score > 0:
                matches.append((chunk, score))
        
        # Sort by score and access patterns
        matches.sort(key=lambda x: (x[1], x[0].access_count, -x[0].last_accessed.timestamp()), reverse=True)
        
        result = [chunk for chunk, _ in matches[:limit]]
        
        # Update access for retrieved memories
        for chunk in result:
            chunk.update_access()
        
        if result:
            self._save_memories()
        
        return result
    
    def get_memories_by_emotional_weight(self, weight: EmotionalWeight) -> List[MemoryChunk]:
        """Get memories by emotional weight"""
        return [chunk for chunk in self._memory_cache.values() if chunk.emotional_weight == weight]
    
    def get_memories_by_context_type(self, context_type: ContextType) -> List[MemoryChunk]:
        """Get memories by context type"""
        return [chunk for chunk in self._memory_cache.values() if chunk.context_type == context_type]
    
    def get_recent_memories(self, hours: int = 24) -> List[MemoryChunk]:
        """Get memories from the last N hours"""
        cutoff = datetime.now() - timedelta(hours=hours)
        recent = [chunk for chunk in self._memory_cache.values() if chunk.created_at > cutoff]
        return sorted(recent, key=lambda x: x.created_at, reverse=True)
    
    def get_frequently_accessed(self, limit: int = 10) -> List[MemoryChunk]:
        """Get most frequently accessed memories"""
        sorted_memories = sorted(self._memory_cache.values(), key=lambda x: x.access_count, reverse=True)
        return sorted_memories[:limit]
    
    # Task operations
    def store_task_context(self, task: TaskContext) -> str:
        """Store a task context"""
        self._task_cache[task.id] = task
        self._save_tasks()
        return task.id
    
    def retrieve_task_context(self, task_id: str) -> Optional[TaskContext]:
        """Retrieve a task context"""
        return self._task_cache.get(task_id)
    
    def get_active_tasks(self) -> List[TaskContext]:
        """Get all active tasks"""
        return [task for task in self._task_cache.values() if task.status == "active"]
    
    # Reflection operations
    def store_reflection(self, reflection: ReflectionEntry) -> str:
        """Store a reflection entry"""
        if not reflection.id:
            reflection.id = f"refl_{int(datetime.now().timestamp())}"
        
        self._reflection_cache[reflection.id] = reflection
        self._save_reflections()
        return reflection.id
    
    def get_recent_reflections(self, limit: int = 5) -> List[ReflectionEntry]:
        """Get recent reflection entries"""
        reflections = sorted(self._reflection_cache.values(), key=lambda x: x.created_at, reverse=True)
        return reflections[:limit]
    
    # Identity operations
    def store_identity(self, identity: IdentityProfile) -> str:
        """Store an identity profile"""
        self._identity_cache[identity.id] = identity
        self._save_identities()
        return identity.id
    
    def retrieve_identity(self, identity_id: str) -> Optional[IdentityProfile]:
        """Retrieve an identity profile"""
        return self._identity_cache.get(identity_id)
    
    def get_all_identities(self) -> List[IdentityProfile]:
        """Get all identity profiles"""
        return list(self._identity_cache.values())
    
    # Utility methods
    def cleanup_old_memories(self, days: int = 30):
        """Clean up memories older than specified days with low access"""
        cutoff = datetime.now() - timedelta(days=days)
        to_remove = []
        
        for chunk_id, chunk in self._memory_cache.items():
            if (chunk.created_at < cutoff and 
                chunk.access_count < 2 and 
                chunk.emotional_weight in [EmotionalWeight.ROUTINE]):
                to_remove.append(chunk_id)
        
        for chunk_id in to_remove:
            del self._memory_cache[chunk_id]
        
        if to_remove:
            self._save_memories()
        
        return len(to_remove)
    
    def export_memories(self, filter_tags: Optional[List[str]] = None, 
                       filter_weight: Optional[EmotionalWeight] = None) -> Dict[str, Any]:
        """Export memories with optional filtering"""
        memories = list(self._memory_cache.values())
        
        if filter_tags:
            memories = [m for m in memories if any(tag in m.tags for tag in filter_tags)]
        
        if filter_weight:
            memories = [m for m in memories if m.emotional_weight == filter_weight]
        
        return {
            'memories': [chunk.dict() for chunk in memories],
            'export_timestamp': datetime.now().isoformat(),
            'total_count': len(memories),
            'filters_applied': {
                'tags': filter_tags,
                'emotional_weight': filter_weight.value if filter_weight else None
            }
        }