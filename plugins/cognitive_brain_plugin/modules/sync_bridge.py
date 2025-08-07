from datetime import datetime
from typing import Dict, Any, List, Optional, Set
import uuid
import json

from ..core.brain_core import BrainModule
from ..schemas.memory_schema import BrainState, MemoryChunk, IdentityProfile, ContextType, EmotionalWeight


class SyncBridge(BrainModule):
    """
    Corpus Callosum-inspired Sync Bridge: Multi-agent memory sync and context sharing
    Responsible for sharing context between different AI agents, models, or brain instances
    """
    
    def __init__(self, storage_adapter):
        super().__init__("sync_bridge", storage_adapter)
        
        # Multi-agent coordination
        self.connected_agents: Dict[str, Dict[str, Any]] = {}
        self.sync_channels: Dict[str, List[str]] = {}  # channel -> agent_ids
        self.sync_history: List[Dict[str, Any]] = []
        
        # Context sharing protocols
        self.sharing_protocols = {
            "full_context": {"security_level": "trusted", "data_types": ["all"]},
            "memory_only": {"security_level": "secure", "data_types": ["memories"]},
            "metadata_only": {"security_level": "public", "data_types": ["metadata"]},
            "selective": {"security_level": "controlled", "data_types": ["filtered"]}
        }
        
        # Sync configurations
        self.auto_sync_enabled = False
        self.sync_filters: Dict[str, Any] = {}
        self.conflict_resolution_strategy = "timestamp_priority"
        
        # Security and privacy
        self.access_permissions: Dict[str, List[str]] = {}  # agent_id -> permissions
        self.privacy_settings = {
            "share_personal_memories": False,
            "share_critical_decisions": True,
            "share_learning_patterns": True,
            "anonymize_data": True
        }
    
    def process(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Process multi-agent synchronization operations"""
        operation_type = input_data.get("type", "sync_request")
        
        self.set_activity_level(0.7)  # Moderate to high activity for sync operations
        
        result = {
            "module": self.name,
            "timestamp": datetime.now().isoformat(),
            "operation": operation_type
        }
        
        if operation_type == "sync_request":
            result.update(self._handle_sync_request(input_data, brain_state))
        
        elif operation_type == "agent_registration":
            result.update(self._register_agent(input_data, brain_state))
        
        elif operation_type == "context_share":
            result.update(self._share_context(input_data, brain_state))
        
        elif operation_type == "memory_sync":
            result.update(self._sync_memories(input_data, brain_state))
        
        elif operation_type == "identity_sync":
            result.update(self._sync_identities(input_data, brain_state))
        
        elif operation_type == "conflict_resolution":
            result.update(self._resolve_sync_conflicts(input_data, brain_state))
        
        elif operation_type == "broadcast_update":
            result.update(self._broadcast_update(input_data, brain_state))
        
        elif operation_type == "sync_status":
            result.update(self._get_sync_status(input_data, brain_state))
        
        else:
            result.update(self._handle_generic_sync(input_data, brain_state))
        
        return result
    
    def _handle_sync_request(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Handle incoming synchronization requests"""
        requesting_agent_id = input_data.get("agent_id", "")
        sync_type = input_data.get("sync_type", "memory_only")
        data_request = input_data.get("data_request", {})
        
        if not requesting_agent_id:
            return {"success": False, "error": "No agent ID provided"}
        
        # Check permissions
        if not self._check_sync_permissions(requesting_agent_id, sync_type):
            return {"success": False, "error": "Insufficient permissions for sync request"}
        
        # Prepare data based on sync type and permissions
        sync_data = self._prepare_sync_data(requesting_agent_id, sync_type, data_request)
        
        # Create sync package
        sync_package = {
            "sync_id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "source_agent": brain_state.active_identity,
            "target_agent": requesting_agent_id,
            "sync_type": sync_type,
            "data": sync_data,
            "metadata": {
                "data_count": len(sync_data.get("items", [])),
                "security_level": self.sharing_protocols[sync_type]["security_level"],
                "expiry": self._calculate_sync_expiry()
            }
        }
        
        # Log sync operation
        self._log_sync_operation("outgoing", sync_package)
        
        return {
            "success": True,
            "sync_package": sync_package,
            "data_shared": len(sync_data.get("items", [])),
            "security_level": sync_package["metadata"]["security_level"]
        }
    
    def _register_agent(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Register a new agent for synchronization"""
        agent_id = input_data.get("agent_id", "")
        agent_info = input_data.get("agent_info", {})
        permissions = input_data.get("permissions", [])
        
        if not agent_id:
            return {"success": False, "error": "No agent ID provided"}
        
        if agent_id in self.connected_agents:
            return {"success": False, "error": "Agent already registered"}
        
        # Register agent
        self.connected_agents[agent_id] = {
            "id": agent_id,
            "name": agent_info.get("name", agent_id),
            "type": agent_info.get("type", "unknown"),
            "capabilities": agent_info.get("capabilities", []),
            "registered_at": datetime.now().isoformat(),
            "last_sync": None,
            "sync_count": 0,
            "status": "active"
        }
        
        # Set permissions
        self.access_permissions[agent_id] = permissions
        
        # Add to default sync channel
        default_channel = "general"
        if default_channel not in self.sync_channels:
            self.sync_channels[default_channel] = []
        self.sync_channels[default_channel].append(agent_id)
        
        return {
            "success": True,
            "agent_registered": agent_id,
            "permissions_granted": len(permissions),
            "sync_channels": [ch for ch, agents in self.sync_channels.items() if agent_id in agents]
        }
    
    def _share_context(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Share current context with specified agents"""
        target_agents = input_data.get("target_agents", [])
        context_data = input_data.get("context_data", {})
        sharing_level = input_data.get("sharing_level", "metadata_only")
        
        if not target_agents:
            target_agents = list(self.connected_agents.keys())
        
        # Prepare context package
        context_package = self._prepare_context_package(context_data, sharing_level, brain_state)
        
        # Share with each target agent
        sharing_results = []
        for agent_id in target_agents:
            if agent_id in self.connected_agents:
                share_result = self._send_context_to_agent(agent_id, context_package)
                sharing_results.append({
                    "agent_id": agent_id,
                    "success": share_result["success"],
                    "data_sent": share_result.get("data_size", 0)
                })
        
        return {
            "success": True,
            "context_shared_with": len(sharing_results),
            "successful_shares": len([r for r in sharing_results if r["success"]]),
            "sharing_level": sharing_level,
            "sharing_results": sharing_results
        }
    
    def _sync_memories(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Synchronize memories with other agents"""
        sync_mode = input_data.get("sync_mode", "bidirectional")  # unidirectional, bidirectional
        agent_ids = input_data.get("agent_ids", [])
        memory_filters = input_data.get("filters", {})
        
        if not agent_ids:
            agent_ids = list(self.connected_agents.keys())
        
        sync_results = []
        
        for agent_id in agent_ids:
            if not self._check_sync_permissions(agent_id, "memory_only"):
                continue
            
            # Get memories to sync
            memories_to_sync = self._filter_memories_for_sync(memory_filters, agent_id)
            
            # Create memory sync package
            memory_sync_data = {
                "memories": [self._serialize_memory_for_sync(m) for m in memories_to_sync],
                "sync_mode": sync_mode,
                "timestamp": datetime.now().isoformat()
            }
            
            # Send sync data (simulated - in real implementation would use network/API)
            sync_result = self._simulate_memory_sync(agent_id, memory_sync_data)
            
            sync_results.append({
                "agent_id": agent_id,
                "memories_sent": len(memories_to_sync),
                "memories_received": sync_result.get("received_count", 0),
                "conflicts_detected": sync_result.get("conflicts", 0),
                "sync_success": sync_result.get("success", False)
            })
            
            # Update agent sync status
            if sync_result.get("success", False):
                self.connected_agents[agent_id]["last_sync"] = datetime.now().isoformat()
                self.connected_agents[agent_id]["sync_count"] += 1
        
        return {
            "success": True,
            "sync_mode": sync_mode,
            "agents_synced": len(sync_results),
            "total_memories_sent": sum(r["memories_sent"] for r in sync_results),
            "total_memories_received": sum(r["memories_received"] for r in sync_results),
            "sync_results": sync_results
        }
    
    def _sync_identities(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Synchronize identity profiles with other agents"""
        target_agents = input_data.get("target_agents", [])
        identity_ids = input_data.get("identity_ids", [])
        
        if not target_agents:
            target_agents = list(self.connected_agents.keys())
        
        # Get identities to sync
        identities_to_sync = []
        if identity_ids:
            for identity_id in identity_ids:
                identity = self.storage.retrieve_identity(identity_id)
                if identity:
                    identities_to_sync.append(identity)
        else:
            identities_to_sync = self.storage.get_all_identities()
        
        sync_results = []
        
        for agent_id in target_agents:
            if not self._check_sync_permissions(agent_id, "full_context"):
                continue
            
            # Prepare identity sync data
            identity_sync_data = {
                "identities": [self._serialize_identity_for_sync(i) for i in identities_to_sync],
                "timestamp": datetime.now().isoformat()
            }
            
            # Send identity sync (simulated)
            sync_result = self._simulate_identity_sync(agent_id, identity_sync_data)
            
            sync_results.append({
                "agent_id": agent_id,
                "identities_sent": len(identities_to_sync),
                "sync_success": sync_result.get("success", False)
            })
        
        return {
            "success": True,
            "identities_synced": len(identities_to_sync),
            "agents_updated": len(sync_results),
            "sync_results": sync_results
        }
    
    def _resolve_sync_conflicts(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Resolve conflicts in synchronized data"""
        conflicts = input_data.get("conflicts", [])
        resolution_strategy = input_data.get("strategy", self.conflict_resolution_strategy)
        
        resolved_conflicts = []
        
        for conflict in conflicts:
            resolution = self._apply_conflict_resolution(conflict, resolution_strategy)
            resolved_conflicts.append(resolution)
        
        return {
            "success": True,
            "conflicts_resolved": len(resolved_conflicts),
            "resolution_strategy": resolution_strategy,
            "resolutions": resolved_conflicts
        }
    
    def _broadcast_update(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Broadcast an update to all connected agents"""
        update_type = input_data.get("update_type", "general")
        update_data = input_data.get("update_data", {})
        channel = input_data.get("channel", "general")
        
        # Get agents in channel
        target_agents = self.sync_channels.get(channel, [])
        
        # Create broadcast package
        broadcast_package = {
            "broadcast_id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "source": brain_state.active_identity,
            "update_type": update_type,
            "data": update_data,
            "channel": channel
        }
        
        # Send to all agents in channel
        broadcast_results = []
        for agent_id in target_agents:
            if agent_id in self.connected_agents:
                result = self._send_broadcast_to_agent(agent_id, broadcast_package)
                broadcast_results.append(result)
        
        return {
            "success": True,
            "broadcast_id": broadcast_package["broadcast_id"],
            "channel": channel,
            "agents_notified": len(broadcast_results),
            "successful_deliveries": len([r for r in broadcast_results if r.get("success", False)])
        }
    
    def _get_sync_status(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Get current synchronization status"""
        
        # Calculate sync statistics
        total_syncs = sum(agent["sync_count"] for agent in self.connected_agents.values())
        active_agents = [a for a in self.connected_agents.values() if a["status"] == "active"]
        
        # Recent sync activity
        recent_syncs = [s for s in self.sync_history if 
                       (datetime.now() - datetime.fromisoformat(s["timestamp"])).total_seconds() < 3600]
        
        return {
            "success": True,
            "connected_agents": len(self.connected_agents),
            "active_agents": len(active_agents),
            "sync_channels": len(self.sync_channels),
            "total_syncs_performed": total_syncs,
            "recent_sync_activity": len(recent_syncs),
            "auto_sync_enabled": self.auto_sync_enabled,
            "agent_details": list(self.connected_agents.values()),
            "channel_details": {ch: len(agents) for ch, agents in self.sync_channels.items()}
        }
    
    def _handle_generic_sync(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Handle generic synchronization operations"""
        return {
            "success": True,
            "message": "Generic sync operation completed",
            "connected_agents": len(self.connected_agents)
        }
    
    # Helper methods
    def _check_sync_permissions(self, agent_id: str, sync_type: str) -> bool:
        """Check if agent has permission for sync type"""
        if agent_id not in self.access_permissions:
            return False
        
        permissions = self.access_permissions[agent_id]
        
        if "all" in permissions:
            return True
        
        if sync_type in permissions:
            return True
        
        # Check specific permissions
        if sync_type == "memory_only" and "read_memories" in permissions:
            return True
        
        if sync_type == "full_context" and "full_access" in permissions:
            return True
        
        return False
    
    def _prepare_sync_data(self, agent_id: str, sync_type: str, data_request: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare data for synchronization based on type and permissions"""
        sync_data = {"items": []}
        
        if sync_type == "memory_only":
            # Get memories based on request filters
            memories = self._filter_memories_for_sync(data_request.get("filters", {}), agent_id)
            sync_data["items"] = [self._serialize_memory_for_sync(m) for m in memories]
        
        elif sync_type == "metadata_only":
            # Only metadata, no content
            memories = self._filter_memories_for_sync(data_request.get("filters", {}), agent_id)
            sync_data["items"] = [self._extract_memory_metadata(m) for m in memories]
        
        elif sync_type == "full_context":
            # Full context including memories, identities, etc.
            memories = self._filter_memories_for_sync(data_request.get("filters", {}), agent_id)
            identities = self.storage.get_all_identities()
            
            sync_data = {
                "memories": [self._serialize_memory_for_sync(m) for m in memories],
                "identities": [self._serialize_identity_for_sync(i) for i in identities],
                "brain_state": self._serialize_brain_state_for_sync()
            }
        
        return sync_data
    
    def _filter_memories_for_sync(self, filters: Dict[str, Any], agent_id: str) -> List[MemoryChunk]:
        """Filter memories for synchronization based on privacy settings"""
        # Get recent memories as base
        memories = self.storage.get_recent_memories(24)
        
        # Apply privacy filters
        filtered_memories = []
        for memory in memories:
            if self._should_share_memory(memory, agent_id):
                filtered_memories.append(memory)
        
        # Apply additional filters
        if "emotional_weight" in filters:
            target_weight = EmotionalWeight(filters["emotional_weight"])
            filtered_memories = [m for m in filtered_memories if m.emotional_weight == target_weight]
        
        if "context_type" in filters:
            target_context = ContextType(filters["context_type"])
            filtered_memories = [m for m in filtered_memories if m.context_type == target_context]
        
        if "limit" in filters:
            filtered_memories = filtered_memories[:filters["limit"]]
        
        return filtered_memories
    
    def _should_share_memory(self, memory: MemoryChunk, agent_id: str) -> bool:
        """Determine if memory should be shared with specific agent"""
        # Check privacy settings
        if not self.privacy_settings.get("share_personal_memories", False):
            if "personal" in memory.tags or memory.emotional_weight == EmotionalWeight.NEGATIVE:
                return False
        
        if not self.privacy_settings.get("share_critical_decisions", True):
            if memory.context_type == ContextType.DECISION and memory.emotional_weight == EmotionalWeight.CRITICAL:
                return False
        
        # Check agent-specific permissions
        agent_permissions = self.access_permissions.get(agent_id, [])
        if "sensitive_data" not in agent_permissions and memory.emotional_weight == EmotionalWeight.CRITICAL:
            return False
        
        return True
    
    def _serialize_memory_for_sync(self, memory: MemoryChunk) -> Dict[str, Any]:
        """Serialize memory for synchronization"""
        serialized = memory.dict()
        
        # Anonymize if required
        if self.privacy_settings.get("anonymize_data", True):
            serialized = self._anonymize_memory_data(serialized)
        
        return serialized
    
    def _serialize_identity_for_sync(self, identity: IdentityProfile) -> Dict[str, Any]:
        """Serialize identity for synchronization"""
        return identity.dict()
    
    def _serialize_brain_state_for_sync(self) -> Dict[str, Any]:
        """Serialize brain state for synchronization"""
        # Return a simplified brain state without sensitive information
        return {
            "active_identity": "anonymized" if self.privacy_settings.get("anonymize_data", True) else None,
            "current_focus": None,  # Don't share current focus
            "debug_mode": False  # Don't share debug info
        }
    
    def _extract_memory_metadata(self, memory: MemoryChunk) -> Dict[str, Any]:
        """Extract only metadata from memory"""
        return {
            "id": memory.id,
            "context_type": memory.context_type.value,
            "emotional_weight": memory.emotional_weight.value,
            "created_at": memory.created_at.isoformat(),
            "access_count": memory.access_count,
            "tags": memory.tags,
            "success_score": memory.success_score,
            "confidence": memory.confidence
        }
    
    def _anonymize_memory_data(self, memory_data: Dict[str, Any]) -> Dict[str, Any]:
        """Anonymize memory data for sharing"""
        anonymized = memory_data.copy()
        
        # Remove or anonymize sensitive fields
        if "identity_context" in anonymized:
            anonymized["identity_context"] = "anonymized"
        
        # Hash the content to provide structure without exposing data
        if "content" in anonymized:
            content = anonymized["content"]
            anonymized["content_hash"] = str(hash(content))
            anonymized["content_length"] = len(content)
            del anonymized["content"]
        
        return anonymized
    
    def _calculate_sync_expiry(self) -> str:
        """Calculate when sync data expires"""
        expiry_time = datetime.now() + timedelta(hours=24)  # 24 hour expiry
        return expiry_time.isoformat()
    
    def _log_sync_operation(self, direction: str, sync_package: Dict[str, Any]):
        """Log synchronization operations"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "direction": direction,  # incoming, outgoing
            "sync_id": sync_package.get("sync_id"),
            "agent_involved": sync_package.get("target_agent") or sync_package.get("source_agent"),
            "sync_type": sync_package.get("sync_type"),
            "data_size": len(str(sync_package.get("data", {}))),
            "success": True
        }
        
        self.sync_history.append(log_entry)
        
        # Keep history manageable
        if len(self.sync_history) > 100:
            self.sync_history = self.sync_history[-50:]
    
    def _prepare_context_package(self, context_data: Dict[str, Any], 
                                sharing_level: str, brain_state: BrainState) -> Dict[str, Any]:
        """Prepare context package for sharing"""
        package = {
            "context_id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "sharing_level": sharing_level,
            "source_identity": brain_state.active_identity if not self.privacy_settings.get("anonymize_data") else "anonymized"
        }
        
        if sharing_level == "full_context":
            package["context_data"] = context_data
            package["brain_state"] = self._serialize_brain_state_for_sync()
        elif sharing_level == "metadata_only":
            package["metadata"] = {
                "data_types": list(context_data.keys()),
                "data_count": len(context_data),
                "timestamp": datetime.now().isoformat()
            }
        
        return package
    
    def _send_context_to_agent(self, agent_id: str, context_package: Dict[str, Any]) -> Dict[str, Any]:
        """Send context to specific agent (simulated)"""
        # In real implementation, this would send data over network/API
        return {
            "success": True,
            "agent_id": agent_id,
            "data_size": len(str(context_package))
        }
    
    def _simulate_memory_sync(self, agent_id: str, sync_data: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate memory synchronization with agent"""
        # Simulate bidirectional sync
        return {
            "success": True,
            "received_count": len(sync_data["memories"]) // 2,  # Simulate receiving some memories back
            "conflicts": 0,  # No conflicts in simulation
            "agent_id": agent_id
        }
    
    def _simulate_identity_sync(self, agent_id: str, identity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate identity synchronization with agent"""
        return {
            "success": True,
            "identities_received": len(identity_data["identities"]),
            "agent_id": agent_id
        }
    
    def _apply_conflict_resolution(self, conflict: Dict[str, Any], strategy: str) -> Dict[str, Any]:
        """Apply conflict resolution strategy"""
        if strategy == "timestamp_priority":
            # Use most recent version
            resolution = "use_newest"
        elif strategy == "confidence_priority":
            # Use version with higher confidence
            resolution = "use_highest_confidence"
        elif strategy == "manual_review":
            # Flag for manual review
            resolution = "flag_for_review"
        else:
            resolution = "use_local"
        
        return {
            "conflict_id": conflict.get("id", "unknown"),
            "resolution": resolution,
            "strategy_used": strategy,
            "timestamp": datetime.now().isoformat()
        }
    
    def _send_broadcast_to_agent(self, agent_id: str, broadcast_package: Dict[str, Any]) -> Dict[str, Any]:
        """Send broadcast to specific agent (simulated)"""
        return {
            "success": True,
            "agent_id": agent_id,
            "broadcast_id": broadcast_package["broadcast_id"]
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Get current module status"""
        return {
            "name": self.name,
            "active": self.active,
            "activity_level": self.activity_level,
            "last_activity": self.last_activity.isoformat(),
            "connected_agents": len(self.connected_agents),
            "sync_channels": len(self.sync_channels),
            "sync_history_size": len(self.sync_history),
            "auto_sync_enabled": self.auto_sync_enabled,
            "sharing_protocols": len(self.sharing_protocols),
            "conflict_resolution_strategy": self.conflict_resolution_strategy,
            "privacy_settings": self.privacy_settings
        }