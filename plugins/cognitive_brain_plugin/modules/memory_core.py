from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Set
import uuid
import hashlib

from ..core.brain_core import BrainModule
from ..schemas.memory_schema import (
    BrainState, MemoryChunk, ContextType, EmotionalWeight
)


class MemoryCore(BrainModule):
    """
    Hippocampus-inspired Memory Core: Long-term memory storage, retrieval, and consolidation
    Responsible for encoding, storing, and retrieving contextual memories
    """
    
    def __init__(self, storage_adapter):
        super().__init__("memory_core", storage_adapter)
        self.consolidation_threshold = 0.7  # Memory strength threshold for consolidation
        self.max_working_memory = 7  # Miller's magic number
        self.working_memory: List[MemoryChunk] = []
        self.consolidation_queue: List[str] = []
        self.last_consolidation = datetime.now()
        
    def process(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Process memory-related operations"""
        operation_type = input_data.get("type", "unknown")
        
        # Update memory activity
        brain_state.memory_activity = 0.8
        self.set_activity_level(0.8)
        
        result = {
            "module": self.name,
            "timestamp": datetime.now().isoformat(),
            "operation": operation_type
        }
        
        if operation_type == "store_memory":
            result.update(self._store_new_memory(input_data, brain_state))
        
        elif operation_type == "retrieve_memory":
            result.update(self._retrieve_memories(input_data, brain_state))
        
        elif operation_type == "search_memory":
            result.update(self._search_memories(input_data, brain_state))
        
        elif operation_type == "consolidate_memory":
            result.update(self._consolidate_memories(input_data, brain_state))
        
        elif operation_type == "associate_memories":
            result.update(self._create_associations(input_data, brain_state))
        
        elif operation_type == "forget_memory":
            result.update(self._forget_memories(input_data, brain_state))
        
        elif operation_type == "memory_replay":
            result.update(self._replay_memories(input_data, brain_state))
        
        elif operation_type == "context_recall":
            result.update(self._contextual_recall(input_data, brain_state))
        
        else:
            # Default: try to determine what kind of memory operation is needed
            result.update(self._analyze_memory_request(input_data, brain_state))
        
        # Check if consolidation is needed
        self._check_consolidation_needs()
        
        return result
    
    def _store_new_memory(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Store a new memory chunk"""
        content = input_data.get("content", "")
        context_type = ContextType(input_data.get("context_type", "conversation"))
        emotional_weight = EmotionalWeight(input_data.get("emotional_weight", "routine"))
        
        if not content:
            return {"success": False, "error": "No content provided for memory storage"}
        
        # Create memory chunk
        memory_chunk = MemoryChunk(
            id=self._generate_memory_id(content),
            content=content,
            context_type=context_type,
            emotional_weight=emotional_weight,
            tags=input_data.get("tags", []),
            keywords=self._extract_keywords(content),
            summary=self._generate_summary(content),
            confidence=input_data.get("confidence", 0.7),
            identity_context=brain_state.active_identity,
            parent_context_id=input_data.get("parent_context_id")
        )
        
        # Store in working memory first
        self._add_to_working_memory(memory_chunk)
        
        # Store persistently
        memory_id = self.storage.store_memory_chunk(memory_chunk)
        
        # Check for immediate associations
        associations = self._find_immediate_associations(memory_chunk)
        if associations:
            memory_chunk.related_chunks.extend([a.id for a in associations])
            self.storage.store_memory_chunk(memory_chunk)
        
        # Queue for consolidation if important
        if (emotional_weight in [EmotionalWeight.IMPORTANT, EmotionalWeight.CRITICAL] or
            memory_chunk.confidence > self.consolidation_threshold):
            self.consolidation_queue.append(memory_id)
        
        return {
            "success": True,
            "memory_id": memory_id,
            "working_memory_size": len(self.working_memory),
            "associations_found": len(associations),
            "queued_for_consolidation": memory_id in self.consolidation_queue
        }
    
    def _retrieve_memories(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Retrieve specific memories"""
        memory_ids = input_data.get("memory_ids", [])
        
        if not memory_ids:
            return {"success": False, "error": "No memory IDs provided"}
        
        retrieved_memories = []
        for memory_id in memory_ids:
            memory = self.storage.retrieve_memory_chunk(memory_id)
            if memory:
                retrieved_memories.append(memory.dict())
                # Add to working memory for quick access
                self._add_to_working_memory(memory)
        
        return {
            "success": True,
            "retrieved_count": len(retrieved_memories),
            "memories": retrieved_memories,
            "working_memory_size": len(self.working_memory)
        }
    
    def _search_memories(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Search memories based on query"""
        query = input_data.get("query", "")
        limit = input_data.get("limit", 10)
        filters = input_data.get("filters", {})
        
        if not query:
            return {"success": False, "error": "No search query provided"}
        
        # Perform search
        memories = self.storage.search_memories(query, limit)
        
        # Apply additional filters
        if filters:
            memories = self._apply_search_filters(memories, filters)
        
        # Rank by relevance and recency
        ranked_memories = self._rank_search_results(memories, query, brain_state)
        
        # Add top results to working memory
        for memory in ranked_memories[:3]:
            self._add_to_working_memory(memory)
        
        return {
            "success": True,
            "query": query,
            "total_found": len(memories),
            "returned_count": len(ranked_memories),
            "memories": [m.dict() for m in ranked_memories],
            "search_relevance_scores": [self._calculate_relevance(m, query) for m in ranked_memories]
        }
    
    def _consolidate_memories(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Consolidate memories for long-term storage"""
        force_consolidation = input_data.get("force", False)
        
        # Get memories to consolidate
        if force_consolidation:
            memories_to_consolidate = self.consolidation_queue.copy()
        else:
            # Only consolidate if enough time has passed
            if (datetime.now() - self.last_consolidation).hours < 1:
                return {"success": True, "message": "Consolidation not needed yet", "consolidated_count": 0}
            
            memories_to_consolidate = self.consolidation_queue[:10]  # Limit batch size
        
        consolidated_count = 0
        consolidation_results = []
        
        for memory_id in memories_to_consolidate:
            memory = self.storage.retrieve_memory_chunk(memory_id)
            if memory:
                consolidation_result = self._consolidate_single_memory(memory)
                consolidation_results.append(consolidation_result)
                
                if consolidation_result["consolidated"]:
                    consolidated_count += 1
                    self.consolidation_queue.remove(memory_id)
        
        self.last_consolidation = datetime.now()
        
        return {
            "success": True,
            "consolidated_count": consolidated_count,
            "remaining_in_queue": len(self.consolidation_queue),
            "consolidation_results": consolidation_results
        }
    
    def _create_associations(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Create associations between memories"""
        memory_id = input_data.get("memory_id", "")
        target_ids = input_data.get("target_ids", [])
        association_type = input_data.get("type", "semantic")
        
        if not memory_id:
            return {"success": False, "error": "No source memory ID provided"}
        
        source_memory = self.storage.retrieve_memory_chunk(memory_id)
        if not source_memory:
            return {"success": False, "error": "Source memory not found"}
        
        associations_created = 0
        
        if target_ids:
            # Create explicit associations
            for target_id in target_ids:
                target_memory = self.storage.retrieve_memory_chunk(target_id)
                if target_memory:
                    # Bidirectional association
                    if target_id not in source_memory.related_chunks:
                        source_memory.related_chunks.append(target_id)
                        associations_created += 1
                    
                    if memory_id not in target_memory.related_chunks:
                        target_memory.related_chunks.append(memory_id)
                        self.storage.store_memory_chunk(target_memory)
        else:
            # Find automatic associations
            similar_memories = self._find_similar_memories(source_memory)
            for similar_memory in similar_memories[:5]:  # Limit associations
                if similar_memory.id not in source_memory.related_chunks:
                    source_memory.related_chunks.append(similar_memory.id)
                    associations_created += 1
                    
                    # Create reverse association
                    if memory_id not in similar_memory.related_chunks:
                        similar_memory.related_chunks.append(memory_id)
                        self.storage.store_memory_chunk(similar_memory)
        
        # Save updated source memory
        self.storage.store_memory_chunk(source_memory)
        
        return {
            "success": True,
            "source_memory_id": memory_id,
            "associations_created": associations_created,
            "total_associations": len(source_memory.related_chunks)
        }
    
    def _forget_memories(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Forget (remove or weaken) memories"""
        memory_ids = input_data.get("memory_ids", [])
        forget_type = input_data.get("type", "weaken")  # "weaken" or "remove"
        
        if not memory_ids:
            return {"success": False, "error": "No memory IDs provided"}
        
        forgotten_count = 0
        weakened_count = 0
        
        for memory_id in memory_ids:
            memory = self.storage.retrieve_memory_chunk(memory_id)
            if memory:
                if forget_type == "remove":
                    # This would require implementing deletion in storage adapter
                    # For now, just mark as forgotten
                    memory.tags.append("forgotten")
                    memory.confidence = 0.1
                    forgotten_count += 1
                else:  # weaken
                    memory.confidence *= 0.5  # Halve the confidence
                    memory.success_score *= 0.7
                    weakened_count += 1
                
                self.storage.store_memory_chunk(memory)
        
        return {
            "success": True,
            "forgotten_count": forgotten_count,
            "weakened_count": weakened_count,
            "forget_type": forget_type
        }
    
    def _replay_memories(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Replay memories to strengthen them or extract patterns"""
        replay_type = input_data.get("replay_type", "recent")  # recent, important, random
        count = input_data.get("count", 5)
        
        if replay_type == "recent":
            memories_to_replay = self.storage.get_recent_memories(24)[:count]
        elif replay_type == "important":
            important_memories = self.storage.get_memories_by_emotional_weight(EmotionalWeight.IMPORTANT)
            critical_memories = self.storage.get_memories_by_emotional_weight(EmotionalWeight.CRITICAL)
            memories_to_replay = (important_memories + critical_memories)[:count]
        elif replay_type == "frequent":
            memories_to_replay = self.storage.get_frequently_accessed(count)
        else:
            # Random sampling from all memories
            all_memories = self.storage.search_memories("", 100)  # Get many memories
            import random
            memories_to_replay = random.sample(all_memories, min(count, len(all_memories)))
        
        patterns_found = []
        strengthened_count = 0
        
        for memory in memories_to_replay:
            # Strengthen the memory through replay
            memory.access_count += 1
            memory.confidence = min(1.0, memory.confidence + 0.1)
            self.storage.store_memory_chunk(memory)
            strengthened_count += 1
            
            # Look for patterns with other memories
            similar_memories = self._find_similar_memories(memory, limit=3)
            if len(similar_memories) >= 2:
                pattern = self._extract_pattern(memory, similar_memories)
                if pattern:
                    patterns_found.append(pattern)
        
        return {
            "success": True,
            "replay_type": replay_type,
            "replayed_count": len(memories_to_replay),
            "strengthened_count": strengthened_count,
            "patterns_found": patterns_found,
            "memory_ids_replayed": [m.id for m in memories_to_replay]
        }
    
    def _contextual_recall(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Recall memories based on current context"""
        current_context = input_data.get("context", "")
        context_type = ContextType(input_data.get("context_type", "conversation"))
        limit = input_data.get("limit", 10)
        
        # Get memories from similar contexts
        context_memories = self.storage.get_memories_by_context_type(context_type)
        
        # Filter by context similarity
        relevant_memories = []
        for memory in context_memories:
            if current_context:
                similarity = self._calculate_context_similarity(current_context, memory.content)
                if similarity > 0.3:  # Threshold for relevance
                    relevant_memories.append((memory, similarity))
        
        # Sort by similarity and recency
        relevant_memories.sort(key=lambda x: (x[1], x[0].last_accessed), reverse=True)
        
        # Get top memories
        recalled_memories = [mem for mem, _ in relevant_memories[:limit]]
        
        # Add to working memory
        for memory in recalled_memories[:3]:
            self._add_to_working_memory(memory)
        
        return {
            "success": True,
            "context": current_context,
            "context_type": context_type.value,
            "recalled_count": len(recalled_memories),
            "memories": [m.dict() for m in recalled_memories],
            "similarity_scores": [score for _, score in relevant_memories[:limit]]
        }
    
    def _analyze_memory_request(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Analyze what kind of memory operation is being requested"""
        content = str(input_data.get("content", ""))
        
        # Determine operation type from content
        if "remember" in content.lower() or "recall" in content.lower():
            suggested_operation = "retrieve_memory"
        elif "forget" in content.lower():
            suggested_operation = "forget_memory"
        elif "associate" in content.lower() or "connect" in content.lower():
            suggested_operation = "associate_memories"
        elif "search" in content.lower() or "find" in content.lower():
            suggested_operation = "search_memory"
        else:
            suggested_operation = "store_memory"
        
        return {
            "analysis": "memory_request_analysis",
            "suggested_operation": suggested_operation,
            "content_length": len(content),
            "working_memory_size": len(self.working_memory)
        }
    
    # Helper methods
    def _generate_memory_id(self, content: str) -> str:
        """Generate a unique memory ID"""
        content_hash = hashlib.md5(content.encode()).hexdigest()
        timestamp = int(datetime.now().timestamp())
        return f"mem_{content_hash[:8]}_{timestamp}"
    
    def _extract_keywords(self, content: str) -> List[str]:
        """Extract keywords from content"""
        # Simple keyword extraction
        words = content.lower().split()
        keywords = [word for word in words if len(word) > 3]
        
        # Remove common words
        stop_words = {"the", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "this", "that"}
        keywords = [word for word in keywords if word not in stop_words]
        
        # Return top keywords
        return list(set(keywords))[:10]
    
    def _generate_summary(self, content: str) -> str:
        """Generate a summary of the content"""
        # Simple summary generation
        sentences = content.split('.')
        if len(sentences) <= 2:
            return content[:100] + "..." if len(content) > 100 else content
        
        # Take first sentence and last sentence
        return f"{sentences[0].strip()}... {sentences[-1].strip()}"
    
    def _add_to_working_memory(self, memory: MemoryChunk):
        """Add memory to working memory with capacity management"""
        # Remove duplicates
        self.working_memory = [m for m in self.working_memory if m.id != memory.id]
        
        # Add new memory
        self.working_memory.append(memory)
        
        # Manage capacity (Miller's 7±2 rule)
        if len(self.working_memory) > self.max_working_memory:
            # Remove oldest or least important
            self.working_memory.sort(key=lambda m: (m.last_accessed, m.emotional_weight.value))
            self.working_memory = self.working_memory[-(self.max_working_memory):]
    
    def _find_immediate_associations(self, memory: MemoryChunk, limit: int = 5) -> List[MemoryChunk]:
        """Find immediate associations for a new memory"""
        associations = []
        
        # Search by keywords
        for keyword in memory.keywords[:3]:  # Limit to top keywords
            similar_memories = self.storage.search_memories(keyword, limit=3)
            associations.extend(similar_memories)
        
        # Search by tags
        for tag in memory.tags:
            tagged_memories = self.storage.search_memories(tag, limit=2)
            associations.extend(tagged_memories)
        
        # Remove duplicates and self
        seen_ids = {memory.id}
        unique_associations = []
        for assoc in associations:
            if assoc.id not in seen_ids:
                unique_associations.append(assoc)
                seen_ids.add(assoc.id)
        
        return unique_associations[:limit]
    
    def _apply_search_filters(self, memories: List[MemoryChunk], filters: Dict[str, Any]) -> List[MemoryChunk]:
        """Apply filters to search results"""
        filtered_memories = memories
        
        if "context_type" in filters:
            context_type = ContextType(filters["context_type"])
            filtered_memories = [m for m in filtered_memories if m.context_type == context_type]
        
        if "emotional_weight" in filters:
            emotional_weight = EmotionalWeight(filters["emotional_weight"])
            filtered_memories = [m for m in filtered_memories if m.emotional_weight == emotional_weight]
        
        if "min_confidence" in filters:
            min_confidence = filters["min_confidence"]
            filtered_memories = [m for m in filtered_memories if m.confidence >= min_confidence]
        
        if "tags" in filters:
            required_tags = filters["tags"]
            filtered_memories = [m for m in filtered_memories if 
                               any(tag in m.tags for tag in required_tags)]
        
        if "date_range" in filters:
            start_date = datetime.fromisoformat(filters["date_range"]["start"])
            end_date = datetime.fromisoformat(filters["date_range"]["end"])
            filtered_memories = [m for m in filtered_memories if 
                               start_date <= m.created_at <= end_date]
        
        return filtered_memories
    
    def _rank_search_results(self, memories: List[MemoryChunk], query: str, brain_state: BrainState) -> List[MemoryChunk]:
        """Rank search results by relevance"""
        scored_memories = []
        
        for memory in memories:
            score = self._calculate_relevance(memory, query)
            
            # Boost score for recent memories
            hours_old = (datetime.now() - memory.created_at).total_seconds() / 3600
            if hours_old < 24:
                score += 0.2
            elif hours_old < 168:  # 1 week
                score += 0.1
            
            # Boost score for frequently accessed memories
            score += min(0.3, memory.access_count * 0.05)
            
            # Boost score for memories from current identity
            if memory.identity_context == brain_state.active_identity:
                score += 0.1
            
            scored_memories.append((memory, score))
        
        # Sort by score
        scored_memories.sort(key=lambda x: x[1], reverse=True)
        
        return [memory for memory, _ in scored_memories]
    
    def _calculate_relevance(self, memory: MemoryChunk, query: str) -> float:
        """Calculate relevance score between memory and query"""
        query_lower = query.lower()
        score = 0.0
        
        # Content similarity
        if query_lower in memory.content.lower():
            score += 0.4
        
        # Keyword matches
        query_words = set(query_lower.split())
        memory_keywords = set([k.lower() for k in memory.keywords])
        keyword_overlap = len(query_words.intersection(memory_keywords))
        if keyword_overlap > 0:
            score += keyword_overlap * 0.1
        
        # Tag matches
        memory_tags = set([t.lower() for t in memory.tags])
        tag_overlap = len(query_words.intersection(memory_tags))
        if tag_overlap > 0:
            score += tag_overlap * 0.15
        
        # Summary similarity
        if memory.summary and query_lower in memory.summary.lower():
            score += 0.2
        
        # Confidence boost
        score *= memory.confidence
        
        return min(1.0, score)
    
    def _consolidate_single_memory(self, memory: MemoryChunk) -> Dict[str, Any]:
        """Consolidate a single memory"""
        original_confidence = memory.confidence
        
        # Strengthen based on access patterns
        if memory.access_count > 3:
            memory.confidence = min(1.0, memory.confidence + 0.1)
        
        # Strengthen based on associations
        if len(memory.related_chunks) > 2:
            memory.confidence = min(1.0, memory.confidence + 0.05)
        
        # Strengthen important memories
        if memory.emotional_weight in [EmotionalWeight.IMPORTANT, EmotionalWeight.CRITICAL]:
            memory.confidence = min(1.0, memory.confidence + 0.15)
        
        # Update success score based on retrieval patterns
        if memory.access_count > 5:
            memory.success_score = min(1.0, memory.success_score + 0.1)
        
        # Save consolidated memory
        self.storage.store_memory_chunk(memory)
        
        return {
            "memory_id": memory.id,
            "consolidated": memory.confidence > original_confidence,
            "confidence_change": memory.confidence - original_confidence,
            "new_confidence": memory.confidence
        }
    
    def _find_similar_memories(self, memory: MemoryChunk, limit: int = 5) -> List[MemoryChunk]:
        """Find similar memories to the given memory"""
        # Use keywords for similarity search
        similar_memories = []
        
        for keyword in memory.keywords[:3]:
            found_memories = self.storage.search_memories(keyword, limit=3)
            similar_memories.extend(found_memories)
        
        # Remove self and duplicates
        seen_ids = {memory.id}
        unique_similar = []
        
        for similar_memory in similar_memories:
            if similar_memory.id not in seen_ids:
                unique_similar.append(similar_memory)
                seen_ids.add(similar_memory.id)
        
        return unique_similar[:limit]
    
    def _extract_pattern(self, memory: MemoryChunk, similar_memories: List[MemoryChunk]) -> Optional[Dict[str, Any]]:
        """Extract patterns from a memory and similar memories"""
        # Simple pattern extraction
        all_memories = [memory] + similar_memories
        
        # Find common keywords
        common_keywords = set(all_memories[0].keywords)
        for mem in all_memories[1:]:
            common_keywords = common_keywords.intersection(set(mem.keywords))
        
        if len(common_keywords) >= 2:
            return {
                "type": "keyword_pattern",
                "common_keywords": list(common_keywords),
                "memory_count": len(all_memories),
                "pattern_strength": len(common_keywords) / len(all_memories[0].keywords) if all_memories[0].keywords else 0
            }
        
        return None
    
    def _calculate_context_similarity(self, context1: str, context2: str) -> float:
        """Calculate similarity between two contexts"""
        if not context1 or not context2:
            return 0.0
        
        words1 = set(context1.lower().split())
        words2 = set(context2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _check_consolidation_needs(self):
        """Check if consolidation is needed and update brain state"""
        # Set consolidation flag if queue is getting large
        if len(self.consolidation_queue) > 20:
            # This would be checked by the brain core
            pass
    
    def get_status(self) -> Dict[str, Any]:
        """Get current module status"""
        return {
            "name": self.name,
            "active": self.active,
            "activity_level": self.activity_level,
            "last_activity": self.last_activity.isoformat(),
            "working_memory_size": len(self.working_memory),
            "consolidation_queue_size": len(self.consolidation_queue),
            "last_consolidation": self.last_consolidation.isoformat(),
            "consolidation_threshold": self.consolidation_threshold,
            "max_working_memory": self.max_working_memory
        }