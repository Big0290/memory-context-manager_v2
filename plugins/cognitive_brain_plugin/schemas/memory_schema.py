from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field


class EmotionalWeight(str, Enum):
    """Emotional tags for memory chunks (Amygdala-inspired)"""
    CRITICAL = "critical"      # Urgent, high-stakes
    IMPORTANT = "important"    # Significant but not urgent
    NOVEL = "novel"           # New, interesting patterns
    ROUTINE = "routine"       # Common, predictable
    NEGATIVE = "negative"     # Errors, failures, warnings
    POSITIVE = "positive"     # Successes, achievements


class ContextType(str, Enum):
    """Types of context chunks"""
    CONVERSATION = "conversation"
    TASK_EXECUTION = "task_execution"
    API_CALL = "api_call"
    DECISION = "decision"
    REFLECTION = "reflection"
    LEARNING = "learning"


class MemoryChunk(BaseModel):
    """Individual memory unit (inspired by hippocampal memory formation)"""
    id: str = Field(..., description="Unique identifier")
    content: str = Field(..., description="The actual memory content")
    context_type: ContextType = Field(..., description="Type of context")
    emotional_weight: EmotionalWeight = Field(default=EmotionalWeight.ROUTINE)
    
    # Temporal information
    created_at: datetime = Field(default_factory=datetime.now)
    last_accessed: datetime = Field(default_factory=datetime.now)
    access_count: int = Field(default=0)
    
    # Relationships and associations
    parent_context_id: Optional[str] = Field(None, description="Parent context if nested")
    related_chunks: List[str] = Field(default_factory=list, description="Associated memory IDs")
    
    # Metadata for retrieval and organization
    tags: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)
    summary: Optional[str] = Field(None, description="AI-generated summary")
    
    # Learning and adaptation
    success_score: float = Field(default=0.5, ge=0.0, le=1.0, description="How successful this memory was")
    confidence: float = Field(default=0.5, ge=0.0, le=1.0, description="Confidence in this memory")
    
    # Identity awareness
    identity_context: Optional[str] = Field(None, description="Which identity/persona this memory belongs to")
    
    def update_access(self):
        """Update access statistics"""
        self.last_accessed = datetime.now()
        self.access_count += 1


class TaskContext(BaseModel):
    """High-level task context (Frontal lobe planning)"""
    id: str = Field(..., description="Unique task identifier")
    name: str = Field(..., description="Human-readable task name")
    description: str = Field(..., description="Task description")
    
    # Task state
    status: str = Field(default="active", description="Current task status")
    priority: float = Field(default=0.5, ge=0.0, le=1.0)
    
    # Memory references
    memory_chunks: List[str] = Field(default_factory=list, description="Associated memory chunk IDs")
    
    # Decision tracking
    decisions_made: List[Dict[str, Any]] = Field(default_factory=list)
    outcomes: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Temporal
    started_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    
    # Learning
    lessons_learned: List[str] = Field(default_factory=list)


class ReflectionEntry(BaseModel):
    """Self-reflection entries for continuous learning"""
    id: str = Field(..., description="Unique reflection ID")
    trigger: str = Field(..., description="What triggered this reflection")
    
    # Analysis
    observations: List[str] = Field(default_factory=list)
    patterns_noticed: List[str] = Field(default_factory=list)
    improvements_suggested: List[str] = Field(default_factory=list)
    
    # Context
    related_memories: List[str] = Field(default_factory=list)
    related_tasks: List[str] = Field(default_factory=list)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)


class BrainState(BaseModel):
    """Current state of the brain system"""
    active_task_id: Optional[str] = None
    active_identity: Optional[str] = None
    current_focus: Optional[str] = None
    current_session_id: Optional[str] = None
    session_start_time: Optional[datetime] = None
    
    # Activity levels (0.0 to 1.0)
    frontal_activity: float = Field(default=0.5, ge=0.0, le=1.0)
    memory_activity: float = Field(default=0.0, ge=0.0, le=1.0)
    emotion_activity: float = Field(default=0.5, ge=0.0, le=1.0)
    context_activity: float = Field(default=0.5, ge=0.0, le=1.0)
    
    # System health
    last_reflection: Optional[datetime] = None
    memory_consolidation_needed: bool = False
    
    # Debug information
    debug_mode: bool = False
    thought_trace: List[str] = Field(default_factory=list)


class IdentityProfile(BaseModel):
    """Identity-specific memory and behavior patterns"""
    id: str = Field(..., description="Identity identifier")
    name: str = Field(..., description="Identity name")
    description: str = Field(..., description="Identity description")
    
    # Behavioral patterns
    preferred_reasoning_style: str = Field(default="analytical")
    emotional_baseline: Dict[str, float] = Field(default_factory=dict)
    
    # Memory organization
    memory_retention_strategy: str = Field(default="importance_based")
    context_switching_cost: float = Field(default=0.3, ge=0.0, le=1.0)
    
    # Learning preferences
    learning_rate: float = Field(default=0.5, ge=0.0, le=1.0)
    exploration_tendency: float = Field(default=0.5, ge=0.0, le=1.0)
    
    # Statistics
    created_at: datetime = Field(default_factory=datetime.now)
    last_active: datetime = Field(default_factory=datetime.now)
    total_interactions: int = Field(default=0)