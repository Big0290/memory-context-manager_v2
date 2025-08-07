from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
import re

from ..core.brain_core import BrainModule
from ..schemas.memory_schema import (
    BrainState, MemoryChunk, EmotionalWeight, ContextType
)


class EmotionTagger(BrainModule):
    """
    Amygdala-inspired Emotion Tagger: Tags contexts with emotional weight and importance
    Responsible for emotional assessment and prioritization of memories and experiences
    """
    
    def __init__(self, storage_adapter):
        super().__init__("emotion_tagger", storage_adapter)
        
        # Emotional pattern recognition
        self.emotion_patterns = {
            EmotionalWeight.CRITICAL: [
                r'\b(critical|urgent|emergency|danger|error|fail|crash|security|breach)\b',
                r'\b(must|immediately|asap|deadline|urgent)\b',
                r'\b(problem|issue|bug|broken|down|offline)\b'
            ],
            EmotionalWeight.IMPORTANT: [
                r'\b(important|key|significant|vital|essential|major)\b',
                r'\b(complete|success|achieve|goal|milestone)\b',
                r'\b(decision|choice|option|strategy)\b'
            ],
            EmotionalWeight.NOVEL: [
                r'\b(new|novel|first|discover|learn|innovative|creative)\b',
                r'\b(interesting|curious|unusual|different|unique)\b',
                r'\b(experiment|try|test|explore)\b'
            ],
            EmotionalWeight.POSITIVE: [
                r'\b(good|great|excellent|perfect|success|win|achieve)\b',
                r'\b(happy|pleased|satisfied|glad|enjoy)\b',
                r'\b(thank|appreciate|helpful|useful)\b'
            ],
            EmotionalWeight.NEGATIVE: [
                r'\b(bad|terrible|awful|horrible|fail|lose|wrong)\b',
                r'\b(sad|angry|frustrated|disappointed|upset)\b',
                r'\b(sorry|mistake|error|problem|issue)\b'
            ]
        }
        
        # Context importance indicators
        self.importance_indicators = {
            'time_pressure': [r'\b(now|asap|urgent|immediately|quickly|soon)\b'],
            'magnitude': [r'\b(all|every|entire|whole|complete|total)\b'],
            'consequence': [r'\b(result|consequence|impact|effect|outcome)\b'],
            'stakeholder': [r'\b(customer|user|client|team|company|business)\b'],
            'resource': [r'\b(money|cost|budget|time|effort|resource)\b']
        }
        
        # Emotional baseline and learning
        self.emotional_baseline = 0.5
        self.emotion_history: List[Dict[str, Any]] = []
        self.learning_rate = 0.1
        
    def process(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Process input for emotional tagging"""
        operation_type = input_data.get("type", "emotional_analysis")
        
        # Update emotion activity
        brain_state.emotion_activity = 0.7
        self.set_activity_level(0.7)
        
        result = {
            "module": self.name,
            "timestamp": datetime.now().isoformat(),
            "operation": operation_type
        }
        
        if operation_type == "emotional_analysis":
            result.update(self._analyze_emotional_content(input_data, brain_state))
        
        elif operation_type == "tag_memory":
            result.update(self._tag_memory_emotionally(input_data, brain_state))
        
        elif operation_type == "assess_importance":
            result.update(self._assess_importance(input_data, brain_state))
        
        elif operation_type == "emotional_context_switch":
            result.update(self._handle_emotional_context_switch(input_data, brain_state))
        
        elif operation_type == "update_emotional_baseline":
            result.update(self._update_emotional_baseline(input_data, brain_state))
        
        elif operation_type == "emotional_memory_review":
            result.update(self._review_emotional_memories(input_data, brain_state))
        
        else:
            # Default: analyze emotional content
            result.update(self._analyze_emotional_content(input_data, brain_state))
        
        return result
    
    def _analyze_emotional_content(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Analyze content for emotional weight and importance"""
        content = input_data.get("content", "")
        context_type = input_data.get("context_type", "conversation")
        
        if not content:
            return {"success": False, "error": "No content provided for emotional analysis"}
        
        # Detect emotional patterns
        emotional_weights = self._detect_emotional_patterns(content)
        primary_emotion = self._determine_primary_emotion(emotional_weights)
        
        # Assess importance
        importance_score = self._calculate_importance_score(content)
        
        # Assess urgency
        urgency_score = self._calculate_urgency_score(content)
        
        # Assess novelty
        novelty_score = self._calculate_novelty_score(content, brain_state)
        
        # Calculate overall emotional weight
        emotional_weight = self._calculate_emotional_weight(
            primary_emotion, importance_score, urgency_score, novelty_score
        )
        
        # Record emotional analysis
        self._record_emotional_analysis(content, emotional_weight, {
            "importance": importance_score,
            "urgency": urgency_score,
            "novelty": novelty_score,
            "primary_emotion": primary_emotion
        })
        
        return {
            "success": True,
            "content_analyzed": len(content),
            "emotional_weight": emotional_weight.value,
            "primary_emotion": primary_emotion,
            "importance_score": importance_score,
            "urgency_score": urgency_score,
            "novelty_score": novelty_score,
            "detected_patterns": emotional_weights,
            "recommended_priority": self._recommend_priority(emotional_weight, importance_score, urgency_score)
        }
    
    def _tag_memory_emotionally(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Tag an existing memory with emotional weight"""
        memory_id = input_data.get("memory_id", "")
        override_emotion = input_data.get("emotional_weight")
        
        if not memory_id:
            return {"success": False, "error": "No memory ID provided"}
        
        memory = self.storage.retrieve_memory_chunk(memory_id)
        if not memory:
            return {"success": False, "error": "Memory not found"}
        
        original_weight = memory.emotional_weight
        
        if override_emotion:
            # Manual override
            memory.emotional_weight = EmotionalWeight(override_emotion)
            tagging_method = "manual_override"
        else:
            # Automatic analysis
            analysis_result = self._analyze_emotional_content({
                "content": memory.content,
                "context_type": memory.context_type.value
            }, brain_state)
            
            memory.emotional_weight = EmotionalWeight(analysis_result["emotional_weight"])
            tagging_method = "automatic_analysis"
        
        # Update memory
        self.storage.store_memory_chunk(memory)
        
        return {
            "success": True,
            "memory_id": memory_id,
            "original_weight": original_weight.value,
            "new_weight": memory.emotional_weight.value,
            "tagging_method": tagging_method,
            "weight_changed": original_weight != memory.emotional_weight
        }
    
    def _assess_importance(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Assess the importance of content or situation"""
        content = input_data.get("content", "")
        context_factors = input_data.get("context_factors", {})
        
        base_importance = self._calculate_importance_score(content)
        
        # Adjust for context factors
        adjusted_importance = base_importance
        
        if context_factors.get("active_task"):
            adjusted_importance += 0.2
        
        if context_factors.get("involves_stakeholders"):
            adjusted_importance += 0.15
        
        if context_factors.get("has_deadline"):
            adjusted_importance += 0.25
        
        if context_factors.get("resource_intensive"):
            adjusted_importance += 0.1
        
        # Cap at 1.0
        adjusted_importance = min(1.0, adjusted_importance)
        
        # Categorize importance level
        if adjusted_importance >= 0.8:
            importance_level = "critical"
        elif adjusted_importance >= 0.6:
            importance_level = "high"
        elif adjusted_importance >= 0.4:
            importance_level = "medium"
        else:
            importance_level = "low"
        
        return {
            "success": True,
            "base_importance": base_importance,
            "adjusted_importance": adjusted_importance,
            "importance_level": importance_level,
            "context_factors_applied": len(context_factors),
            "recommended_emotional_weight": self._importance_to_emotional_weight(adjusted_importance).value
        }
    
    def _handle_emotional_context_switch(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Handle emotional aspects of context switching"""
        previous_context = input_data.get("previous_context", "")
        new_context = input_data.get("new_context", "")
        
        # Analyze emotional weight of contexts
        prev_analysis = self._analyze_emotional_content({"content": previous_context}, brain_state)
        new_analysis = self._analyze_emotional_content({"content": new_context}, brain_state)
        
        # Calculate emotional switching cost
        emotional_distance = self._calculate_emotional_distance(
            prev_analysis["emotional_weight"],
            new_analysis["emotional_weight"]
        )
        
        # Higher switching cost for large emotional jumps
        emotional_switching_cost = emotional_distance * 0.3
        
        # Recommend transition strategy
        transition_strategy = self._recommend_transition_strategy(
            prev_analysis["emotional_weight"],
            new_analysis["emotional_weight"],
            emotional_distance
        )
        
        return {
            "success": True,
            "previous_emotional_weight": prev_analysis["emotional_weight"],
            "new_emotional_weight": new_analysis["emotional_weight"],
            "emotional_distance": emotional_distance,
            "emotional_switching_cost": emotional_switching_cost,
            "transition_strategy": transition_strategy
        }
    
    def _update_emotional_baseline(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Update emotional baseline based on recent experiences"""
        learning_enabled = input_data.get("learning_enabled", True)
        
        if not learning_enabled or len(self.emotion_history) < 5:
            return {"success": False, "message": "Insufficient data for baseline update"}
        
        # Calculate new baseline from recent emotions
        recent_emotions = self.emotion_history[-20:]  # Last 20 emotional assessments
        
        emotion_values = {
            EmotionalWeight.CRITICAL: 1.0,
            EmotionalWeight.IMPORTANT: 0.8,
            EmotionalWeight.NOVEL: 0.6,
            EmotionalWeight.POSITIVE: 0.7,
            EmotionalWeight.NEGATIVE: 0.3,
            EmotionalWeight.ROUTINE: 0.4
        }
        
        # Calculate weighted average
        total_weight = 0
        total_value = 0
        
        for emotion_record in recent_emotions:
            emotion_weight = EmotionalWeight(emotion_record["emotional_weight"])
            weight = 1.0  # Could be adjusted based on recency
            
            total_weight += weight
            total_value += emotion_values[emotion_weight] * weight
        
        new_baseline = total_value / total_weight if total_weight > 0 else self.emotional_baseline
        
        # Smooth transition using learning rate
        old_baseline = self.emotional_baseline
        self.emotional_baseline = (1 - self.learning_rate) * old_baseline + self.learning_rate * new_baseline
        
        return {
            "success": True,
            "old_baseline": old_baseline,
            "new_baseline": self.emotional_baseline,
            "change": self.emotional_baseline - old_baseline,
            "emotions_analyzed": len(recent_emotions)
        }
    
    def _review_emotional_memories(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Review and potentially re-tag emotional memories"""
        review_type = input_data.get("review_type", "recent")  # recent, all, by_weight
        limit = input_data.get("limit", 10)
        
        if review_type == "recent":
            memories = self.storage.get_recent_memories(24)[:limit]
        elif review_type == "critical":
            memories = self.storage.get_memories_by_emotional_weight(EmotionalWeight.CRITICAL)[:limit]
        elif review_type == "important":
            memories = self.storage.get_memories_by_emotional_weight(EmotionalWeight.IMPORTANT)[:limit]
        else:
            # Get a sample of all memories
            all_memories = self.storage.search_memories("", limit * 2)
            memories = all_memories[:limit]
        
        review_results = []
        retagged_count = 0
        
        for memory in memories:
            original_weight = memory.emotional_weight
            
            # Re-analyze emotional content
            analysis = self._analyze_emotional_content({
                "content": memory.content,
                "context_type": memory.context_type.value
            }, brain_state)
            
            suggested_weight = EmotionalWeight(analysis["emotional_weight"])
            
            # Check if retagging is recommended
            if suggested_weight != original_weight:
                # Consider time decay and access patterns
                should_retag = self._should_retag_memory(memory, suggested_weight, original_weight)
                
                if should_retag:
                    memory.emotional_weight = suggested_weight
                    self.storage.store_memory_chunk(memory)
                    retagged_count += 1
                
                review_results.append({
                    "memory_id": memory.id,
                    "original_weight": original_weight.value,
                    "suggested_weight": suggested_weight.value,
                    "retagged": should_retag,
                    "confidence": analysis["importance_score"]
                })
        
        return {
            "success": True,
            "review_type": review_type,
            "memories_reviewed": len(memories),
            "retagged_count": retagged_count,
            "review_results": review_results
        }
    
    # Helper methods for emotional pattern detection
    def _detect_emotional_patterns(self, content: str) -> Dict[EmotionalWeight, float]:
        """Detect emotional patterns in content"""
        content_lower = content.lower()
        emotion_scores = {}
        
        for emotion, patterns in self.emotion_patterns.items():
            score = 0.0
            for pattern in patterns:
                matches = len(re.findall(pattern, content_lower))
                score += matches * 0.2  # Each match adds 0.2 to score
            
            emotion_scores[emotion] = min(1.0, score)
        
        return emotion_scores
    
    def _determine_primary_emotion(self, emotional_weights: Dict[EmotionalWeight, float]) -> str:
        """Determine primary emotion from detected patterns"""
        if not emotional_weights:
            return "neutral"
        
        max_emotion = max(emotional_weights, key=emotional_weights.get)
        max_score = emotional_weights[max_emotion]
        
        if max_score > 0.3:
            return max_emotion.value
        else:
            return "neutral"
    
    def _calculate_importance_score(self, content: str) -> float:
        """Calculate importance score based on content analysis"""
        content_lower = content.lower()
        importance_score = 0.3  # Base score
        
        for category, patterns in self.importance_indicators.items():
            for pattern in patterns:
                matches = len(re.findall(pattern, content_lower))
                if matches > 0:
                    if category == 'time_pressure':
                        importance_score += 0.3
                    elif category == 'magnitude':
                        importance_score += 0.2
                    elif category == 'consequence':
                        importance_score += 0.25
                    elif category == 'stakeholder':
                        importance_score += 0.15
                    elif category == 'resource':
                        importance_score += 0.1
        
        # Length factor (longer content might be more important)
        length_factor = min(0.2, len(content) / 1000)
        importance_score += length_factor
        
        return min(1.0, importance_score)
    
    def _calculate_urgency_score(self, content: str) -> float:
        """Calculate urgency score"""
        urgency_words = [
            r'\b(urgent|asap|immediately|now|quick|fast|soon|deadline)\b',
            r'\b(emergency|critical|rush|hurry)\b'
        ]
        
        content_lower = content.lower()
        urgency_score = 0.2
        
        for pattern in urgency_words:
            matches = len(re.findall(pattern, content_lower))
            urgency_score += matches * 0.3
        
        return min(1.0, urgency_score)
    
    def _calculate_novelty_score(self, content: str, brain_state: BrainState) -> float:
        """Calculate novelty score based on similarity to existing memories"""
        # Search for similar content
        similar_memories = self.storage.search_memories(content[:100], limit=5)
        
        if not similar_memories:
            return 0.8  # High novelty if no similar memories
        
        # Calculate average similarity
        total_similarity = 0
        for memory in similar_memories:
            similarity = self._calculate_content_similarity(content, memory.content)
            total_similarity += similarity
        
        avg_similarity = total_similarity / len(similar_memories)
        novelty_score = 1.0 - avg_similarity  # Invert similarity for novelty
        
        # Check for novel words/concepts
        novel_words = self._detect_novel_words(content)
        novelty_score += len(novel_words) * 0.1
        
        return min(1.0, novelty_score)
    
    def _calculate_emotional_weight(self, primary_emotion: str, importance: float, 
                                  urgency: float, novelty: float) -> EmotionalWeight:
        """Calculate overall emotional weight"""
        # Critical conditions
        if urgency > 0.7 or importance > 0.8:
            return EmotionalWeight.CRITICAL
        
        # Important conditions
        if importance > 0.6 or (urgency > 0.5 and importance > 0.4):
            return EmotionalWeight.IMPORTANT
        
        # Novel conditions
        if novelty > 0.7:
            return EmotionalWeight.NOVEL
        
        # Emotional conditions
        if primary_emotion in ["positive"]:
            return EmotionalWeight.POSITIVE
        elif primary_emotion in ["negative"]:
            return EmotionalWeight.NEGATIVE
        
        # Default to routine
        return EmotionalWeight.ROUTINE
    
    def _recommend_priority(self, emotional_weight: EmotionalWeight, importance: float, urgency: float) -> str:
        """Recommend processing priority"""
        if emotional_weight == EmotionalWeight.CRITICAL or urgency > 0.8:
            return "immediate"
        elif emotional_weight == EmotionalWeight.IMPORTANT or importance > 0.7:
            return "high"
        elif emotional_weight == EmotionalWeight.NOVEL:
            return "medium"
        else:
            return "low"
    
    def _record_emotional_analysis(self, content: str, emotional_weight: EmotionalWeight, metrics: Dict[str, Any]):
        """Record emotional analysis for learning"""
        self.emotion_history.append({
            "timestamp": datetime.now().isoformat(),
            "content_length": len(content),
            "emotional_weight": emotional_weight.value,
            "metrics": metrics
        })
        
        # Keep history manageable
        if len(self.emotion_history) > 100:
            self.emotion_history = self.emotion_history[-50:]
    
    def _calculate_emotional_distance(self, emotion1: str, emotion2: str) -> float:
        """Calculate distance between two emotional states"""
        emotion_map = {
            "critical": 1.0,
            "important": 0.8,
            "novel": 0.6,
            "positive": 0.7,
            "negative": 0.3,
            "routine": 0.4
        }
        
        val1 = emotion_map.get(emotion1, 0.5)
        val2 = emotion_map.get(emotion2, 0.5)
        
        return abs(val1 - val2)
    
    def _recommend_transition_strategy(self, prev_emotion: str, new_emotion: str, distance: float) -> str:
        """Recommend strategy for emotional context transition"""
        if distance < 0.2:
            return "smooth_transition"
        elif distance < 0.5:
            return "gradual_transition"
        elif prev_emotion == "critical" and new_emotion == "routine":
            return "decompression_needed"
        elif prev_emotion == "routine" and new_emotion == "critical":
            return "alert_activation"
        else:
            return "careful_transition"
    
    def _importance_to_emotional_weight(self, importance: float) -> EmotionalWeight:
        """Convert importance score to emotional weight"""
        if importance >= 0.8:
            return EmotionalWeight.CRITICAL
        elif importance >= 0.6:
            return EmotionalWeight.IMPORTANT
        elif importance >= 0.4:
            return EmotionalWeight.ROUTINE
        else:
            return EmotionalWeight.ROUTINE
    
    def _should_retag_memory(self, memory: MemoryChunk, suggested_weight: EmotionalWeight, 
                           original_weight: EmotionalWeight) -> bool:
        """Determine if memory should be retagged"""
        # Don't retag if memory is very recent (less than 1 hour)
        if (datetime.now() - memory.created_at).total_seconds() < 3600:
            return False
        
        # Don't retag frequently accessed memories
        if memory.access_count > 10:
            return False
        
        # Retag if confidence is low
        if memory.confidence < 0.5:
            return True
        
        # Retag if suggested weight is significantly different
        weight_hierarchy = {
            EmotionalWeight.ROUTINE: 1,
            EmotionalWeight.POSITIVE: 2,
            EmotionalWeight.NEGATIVE: 2,
            EmotionalWeight.NOVEL: 3,
            EmotionalWeight.IMPORTANT: 4,
            EmotionalWeight.CRITICAL: 5
        }
        
        orig_level = weight_hierarchy[original_weight]
        sugg_level = weight_hierarchy[suggested_weight]
        
        # Retag if difference is significant (2+ levels)
        return abs(orig_level - sugg_level) >= 2
    
    def _calculate_content_similarity(self, content1: str, content2: str) -> float:
        """Calculate similarity between two pieces of content"""
        words1 = set(content1.lower().split())
        words2 = set(content2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _detect_novel_words(self, content: str) -> List[str]:
        """Detect potentially novel words or concepts"""
        words = content.lower().split()
        
        # Simple novelty detection: long words, technical terms, etc.
        novel_candidates = []
        for word in words:
            if len(word) > 8:  # Long words might be technical terms
                novel_candidates.append(word)
            elif word.endswith(('tion', 'sion', 'ment', 'ness', 'ity')):  # Abstract concepts
                novel_candidates.append(word)
        
        return novel_candidates[:5]  # Limit to 5 novel words
    
    def get_status(self) -> Dict[str, Any]:
        """Get current module status"""
        return {
            "name": self.name,
            "active": self.active,
            "activity_level": self.activity_level,
            "last_activity": self.last_activity.isoformat(),
            "emotional_baseline": self.emotional_baseline,
            "emotion_history_size": len(self.emotion_history),
            "learning_rate": self.learning_rate,
            "pattern_categories": len(self.emotion_patterns),
            "importance_indicators": len(self.importance_indicators)
        }