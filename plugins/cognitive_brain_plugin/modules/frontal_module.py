from datetime import datetime
from typing import Dict, Any, List, Optional
import uuid

from ..core.brain_core import BrainModule
from ..schemas.memory_schema import (
    BrainState, MemoryChunk, TaskContext, ContextType, EmotionalWeight
)


class FrontalModule(BrainModule):
    """
    Frontal Lobe Module: Executive functions, planning, reasoning, decision making
    Responsible for high-level cognitive control and strategic thinking
    """
    
    def __init__(self, storage_adapter):
        super().__init__("frontal_lobe", storage_adapter)
        self.current_reasoning_chain = []
        self.decision_history = []
        self.planning_depth = 3  # How many steps ahead to plan
        
    def process(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Process input through executive functions"""
        input_type = input_data.get("type", "unknown")
        
        # Update activity based on input complexity
        complexity = self._assess_complexity(input_data)
        self.set_activity_level(min(1.0, 0.5 + complexity * 0.5))
        
        result = {
            "module": self.name,
            "timestamp": datetime.now().isoformat(),
            "processing_type": input_type
        }
        
        if input_type == "task_planning":
            result.update(self._handle_task_planning(input_data, brain_state))
        
        elif input_type == "decision_request":
            result.update(self._handle_decision_making(input_data, brain_state))
        
        elif input_type == "reasoning_request":
            result.update(self._handle_reasoning(input_data, brain_state))
        
        elif input_type == "context_switch":
            result.update(self._handle_context_switching(input_data, brain_state))
        
        elif input_type == "priority_assessment":
            result.update(self._handle_priority_assessment(input_data, brain_state))
        
        else:
            # Default processing: analyze and route
            result.update(self._analyze_and_route(input_data, brain_state))
        
        # Store reasoning process as memory
        if self.current_reasoning_chain:
            self._store_reasoning_memory(result, brain_state)
        
        return result
    
    def _assess_complexity(self, input_data: Dict[str, Any]) -> float:
        """Assess the complexity of the input (0.0 to 1.0)"""
        complexity = 0.0
        
        # Length of input
        content = str(input_data.get("content", ""))
        complexity += min(0.3, len(content) / 1000)
        
        # Number of sub-tasks or components
        if "subtasks" in input_data:
            complexity += min(0.4, len(input_data["subtasks"]) * 0.1)
        
        # Presence of uncertainty or ambiguity indicators
        uncertainty_words = ["maybe", "possibly", "unclear", "ambiguous", "uncertain"]
        if any(word in content.lower() for word in uncertainty_words):
            complexity += 0.2
        
        # Multiple objectives or constraints
        if "objectives" in input_data:
            complexity += min(0.3, len(input_data.get("objectives", [])) * 0.1)
        
        return min(1.0, complexity)
    
    def _handle_task_planning(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Handle task planning and decomposition"""
        task_description = input_data.get("task", "")
        constraints = input_data.get("constraints", [])
        objectives = input_data.get("objectives", [])
        
        self.current_reasoning_chain = [
            f"Analyzing task: {task_description}",
            f"Considering {len(constraints)} constraints",
            f"Working toward {len(objectives)} objectives"
        ]
        
        # Retrieve relevant past experiences
        similar_memories = self.storage.search_memories(task_description, limit=5)
        past_successes = [m for m in similar_memories if m.success_score > 0.7]
        
        if past_successes:
            self.current_reasoning_chain.append(f"Found {len(past_successes)} similar successful experiences")
        
        # Generate plan steps
        plan_steps = self._decompose_task(task_description, constraints, objectives)
        
        # Assess risks and alternatives
        risk_assessment = self._assess_task_risks(plan_steps, similar_memories)
        
        # Create task context
        task_id = f"plan_{uuid.uuid4().hex[:8]}"
        task_context = TaskContext(
            id=task_id,
            name=task_description,
            description=f"Planned task with {len(plan_steps)} steps",
            priority=self._calculate_priority(objectives, constraints),
            decisions_made=[{
                "decision": "task_decomposition",
                "reasoning": self.current_reasoning_chain.copy(),
                "timestamp": datetime.now().isoformat()
            }]
        )
        
        self.storage.store_task_context(task_context)
        
        return {
            "task_id": task_id,
            "plan_steps": plan_steps,
            "risk_assessment": risk_assessment,
            "similar_experiences": len(similar_memories),
            "confidence": self._calculate_confidence(past_successes, risk_assessment),
            "reasoning_chain": self.current_reasoning_chain.copy()
        }
    
    def _handle_decision_making(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Handle decision making processes"""
        decision_context = input_data.get("context", "")
        options = input_data.get("options", [])
        criteria = input_data.get("criteria", [])
        
        self.current_reasoning_chain = [
            f"Making decision in context: {decision_context}",
            f"Evaluating {len(options)} options",
            f"Using {len(criteria)} criteria"
        ]
        
        # Retrieve relevant decision history
        decision_memories = self.storage.get_memories_by_context_type(ContextType.DECISION)
        relevant_decisions = [m for m in decision_memories if 
                            any(keyword in m.content.lower() for keyword in decision_context.lower().split())]
        
        # Evaluate each option
        option_evaluations = []
        for option in options:
            evaluation = self._evaluate_option(option, criteria, relevant_decisions)
            option_evaluations.append(evaluation)
            self.current_reasoning_chain.append(f"Option '{option}': score {evaluation['score']:.2f}")
        
        # Select best option
        best_option = max(option_evaluations, key=lambda x: x["score"]) if option_evaluations else None
        
        # Record decision
        decision_record = {
            "context": decision_context,
            "options_considered": len(options),
            "selected_option": best_option["option"] if best_option else None,
            "confidence": best_option["confidence"] if best_option else 0.0,
            "reasoning": self.current_reasoning_chain.copy(),
            "timestamp": datetime.now().isoformat()
        }
        
        self.decision_history.append(decision_record)
        
        return {
            "decision": best_option["option"] if best_option else None,
            "confidence": best_option["confidence"] if best_option else 0.0,
            "option_evaluations": option_evaluations,
            "reasoning_chain": self.current_reasoning_chain.copy(),
            "similar_past_decisions": len(relevant_decisions)
        }
    
    def _handle_reasoning(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Handle reasoning and logical analysis"""
        query = input_data.get("query", "")
        reasoning_type = input_data.get("reasoning_type", "deductive")  # deductive, inductive, abductive
        
        self.current_reasoning_chain = [f"Starting {reasoning_type} reasoning for: {query}"]
        
        # Retrieve relevant knowledge
        relevant_memories = self.storage.search_memories(query, limit=10)
        facts = [m for m in relevant_memories if m.emotional_weight in [EmotionalWeight.IMPORTANT, EmotionalWeight.CRITICAL]]
        
        # Apply reasoning strategy
        if reasoning_type == "deductive":
            conclusion = self._deductive_reasoning(query, facts)
        elif reasoning_type == "inductive":
            conclusion = self._inductive_reasoning(query, facts)
        elif reasoning_type == "abductive":
            conclusion = self._abductive_reasoning(query, facts)
        else:
            conclusion = self._general_reasoning(query, facts)
        
        confidence = self._calculate_reasoning_confidence(facts, conclusion)
        
        return {
            "query": query,
            "reasoning_type": reasoning_type,
            "conclusion": conclusion,
            "confidence": confidence,
            "supporting_facts": len(facts),
            "reasoning_chain": self.current_reasoning_chain.copy()
        }
    
    def _handle_context_switching(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Handle switching between different contexts or tasks"""
        new_context = input_data.get("new_context", "")
        current_context = brain_state.current_focus
        
        # Calculate switching cost
        switching_cost = 0.3  # Base cost
        if current_context:
            # Higher cost if contexts are very different
            context_similarity = self._calculate_context_similarity(current_context, new_context)
            switching_cost += (1.0 - context_similarity) * 0.4
        
        self.current_reasoning_chain = [
            f"Switching from '{current_context}' to '{new_context}'",
            f"Estimated switching cost: {switching_cost:.2f}"
        ]
        
        # Update brain state
        brain_state.current_focus = new_context
        
        return {
            "previous_context": current_context,
            "new_context": new_context,
            "switching_cost": switching_cost,
            "success": True,
            "reasoning_chain": self.current_reasoning_chain.copy()
        }
    
    def _handle_priority_assessment(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Assess and rank task priorities"""
        tasks = input_data.get("tasks", [])
        
        self.current_reasoning_chain = [f"Assessing priorities for {len(tasks)} tasks"]
        
        priority_rankings = []
        for task in tasks:
            priority_score = self._calculate_task_priority(task)
            priority_rankings.append({
                "task": task,
                "priority_score": priority_score,
                "urgency": self._assess_urgency(task),
                "importance": self._assess_importance(task)
            })
            
            self.current_reasoning_chain.append(f"Task '{task}': priority {priority_score:.2f}")
        
        # Sort by priority score
        priority_rankings.sort(key=lambda x: x["priority_score"], reverse=True)
        
        return {
            "prioritized_tasks": priority_rankings,
            "top_priority": priority_rankings[0]["task"] if priority_rankings else None,
            "reasoning_chain": self.current_reasoning_chain.copy()
        }
    
    def _analyze_and_route(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Default analysis and routing for unknown input types"""
        content = str(input_data.get("content", ""))
        
        # Determine what kind of processing is needed
        if "plan" in content.lower() or "strategy" in content.lower():
            suggested_routing = "task_planning"
        elif "decide" in content.lower() or "choose" in content.lower():
            suggested_routing = "decision_request"
        elif "why" in content.lower() or "explain" in content.lower():
            suggested_routing = "reasoning_request"
        else:
            suggested_routing = "general_processing"
        
        self.current_reasoning_chain = [
            f"Analyzing unknown input type",
            f"Content length: {len(content)} characters",
            f"Suggested routing: {suggested_routing}"
        ]
        
        return {
            "analysis": "general_input_analysis",
            "suggested_routing": suggested_routing,
            "complexity": self._assess_complexity(input_data),
            "reasoning_chain": self.current_reasoning_chain.copy()
        }
    
    # Helper methods for specific reasoning types
    def _deductive_reasoning(self, query: str, facts: List[MemoryChunk]) -> str:
        """Apply deductive reasoning"""
        self.current_reasoning_chain.append("Applying deductive logic")
        # Simplified deductive reasoning implementation
        if facts:
            return f"Based on {len(facts)} established facts, the logical conclusion is derived"
        return "Insufficient facts for deductive reasoning"
    
    def _inductive_reasoning(self, query: str, facts: List[MemoryChunk]) -> str:
        """Apply inductive reasoning"""
        self.current_reasoning_chain.append("Applying inductive logic")
        # Look for patterns in facts
        if len(facts) >= 3:
            return "Pattern-based conclusion from observed instances"
        return "Insufficient examples for inductive reasoning"
    
    def _abductive_reasoning(self, query: str, facts: List[MemoryChunk]) -> str:
        """Apply abductive reasoning"""
        self.current_reasoning_chain.append("Applying abductive logic")
        # Find best explanation
        return "Most likely explanation given available evidence"
    
    def _general_reasoning(self, query: str, facts: List[MemoryChunk]) -> str:
        """Apply general reasoning"""
        self.current_reasoning_chain.append("Applying general reasoning")
        return f"Analysis based on {len(facts)} relevant facts"
    
    # Utility methods
    def _decompose_task(self, task: str, constraints: List[str], objectives: List[str]) -> List[Dict[str, Any]]:
        """Decompose a task into steps"""
        # Simplified task decomposition
        steps = []
        
        # Analysis phase
        steps.append({
            "step": 1,
            "name": "Analysis",
            "description": "Analyze requirements and constraints",
            "estimated_effort": 0.2
        })
        
        # Planning phase
        steps.append({
            "step": 2,
            "name": "Planning",
            "description": "Create detailed execution plan",
            "estimated_effort": 0.3
        })
        
        # Execution phase
        steps.append({
            "step": 3,
            "name": "Execution",
            "description": "Implement the solution",
            "estimated_effort": 0.4
        })
        
        # Validation phase
        steps.append({
            "step": 4,
            "name": "Validation",
            "description": "Verify results against objectives",
            "estimated_effort": 0.1
        })
        
        return steps
    
    def _assess_task_risks(self, plan_steps: List[Dict[str, Any]], similar_memories: List[MemoryChunk]) -> Dict[str, Any]:
        """Assess risks in task execution"""
        risks = []
        
        if not similar_memories:
            risks.append("No prior experience with similar tasks")
        
        if len(plan_steps) > 5:
            risks.append("Complex task with many steps")
        
        total_effort = sum(step.get("estimated_effort", 0) for step in plan_steps)
        if total_effort > 1.0:
            risks.append("Task may require more resources than available")
        
        return {
            "identified_risks": risks,
            "risk_level": "high" if len(risks) > 2 else "medium" if len(risks) > 0 else "low"
        }
    
    def _evaluate_option(self, option: str, criteria: List[str], past_decisions: List[MemoryChunk]) -> Dict[str, Any]:
        """Evaluate a decision option"""
        score = 0.5  # Base score
        
        # Check against criteria (simplified)
        for criterion in criteria:
            if criterion.lower() in option.lower():
                score += 0.1
        
        # Consider past decisions
        for decision in past_decisions:
            if option.lower() in decision.content.lower():
                score += decision.success_score * 0.2
        
        confidence = min(0.9, score)
        
        return {
            "option": option,
            "score": min(1.0, score),
            "confidence": confidence
        }
    
    def _calculate_priority(self, objectives: List[str], constraints: List[str]) -> float:
        """Calculate task priority"""
        priority = 0.5
        priority += len(objectives) * 0.1
        priority -= len(constraints) * 0.05
        return max(0.1, min(1.0, priority))
    
    def _calculate_confidence(self, past_successes: List[MemoryChunk], risk_assessment: Dict[str, Any]) -> float:
        """Calculate confidence in plan"""
        confidence = 0.5
        
        if past_successes:
            avg_success = sum(m.success_score for m in past_successes) / len(past_successes)
            confidence += avg_success * 0.3
        
        if risk_assessment["risk_level"] == "low":
            confidence += 0.2
        elif risk_assessment["risk_level"] == "high":
            confidence -= 0.2
        
        return max(0.1, min(1.0, confidence))
    
    def _calculate_context_similarity(self, context1: str, context2: str) -> float:
        """Calculate similarity between two contexts"""
        if not context1 or not context2:
            return 0.0
        
        # Simplified similarity calculation
        words1 = set(context1.lower().split())
        words2 = set(context2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _calculate_task_priority(self, task: str) -> float:
        """Calculate priority score for a task"""
        priority = 0.5
        
        # Check for urgency indicators
        urgency_words = ["urgent", "asap", "immediate", "critical", "now"]
        if any(word in task.lower() for word in urgency_words):
            priority += 0.3
        
        # Check for importance indicators
        importance_words = ["important", "key", "essential", "vital", "crucial"]
        if any(word in task.lower() for word in importance_words):
            priority += 0.2
        
        return min(1.0, priority)
    
    def _assess_urgency(self, task: str) -> float:
        """Assess task urgency"""
        urgency_words = ["urgent", "asap", "immediate", "deadline", "soon"]
        urgency = 0.3
        for word in urgency_words:
            if word in task.lower():
                urgency += 0.2
        return min(1.0, urgency)
    
    def _assess_importance(self, task: str) -> float:
        """Assess task importance"""
        importance_words = ["important", "critical", "essential", "key", "vital"]
        importance = 0.3
        for word in importance_words:
            if word in task.lower():
                importance += 0.2
        return min(1.0, importance)
    
    def _calculate_reasoning_confidence(self, facts: List[MemoryChunk], conclusion: str) -> float:
        """Calculate confidence in reasoning conclusion"""
        if not facts:
            return 0.2
        
        # Base confidence from number of supporting facts
        confidence = min(0.8, len(facts) * 0.1 + 0.3)
        
        # Adjust based on fact quality
        high_quality_facts = [f for f in facts if f.confidence > 0.7]
        confidence += len(high_quality_facts) * 0.05
        
        return min(0.95, confidence)
    
    def _store_reasoning_memory(self, result: Dict[str, Any], brain_state: BrainState):
        """Store the reasoning process as a memory"""
        memory_content = f"Frontal lobe processing: {result.get('processing_type', 'unknown')}\n"
        memory_content += f"Reasoning: {'; '.join(self.current_reasoning_chain)}"
        
        memory_chunk = MemoryChunk(
            id=f"frontal_{uuid.uuid4().hex[:8]}",
            content=memory_content,
            context_type=ContextType.DECISION,
            emotional_weight=EmotionalWeight.IMPORTANT if self.activity_level > 0.7 else EmotionalWeight.ROUTINE,
            tags=["frontal_lobe", "reasoning", result.get('processing_type', 'unknown')],
            keywords=self._extract_keywords_from_reasoning(),
            summary=f"Frontal lobe {result.get('processing_type', 'processing')} with confidence {result.get('confidence', 0.5):.2f}",
            success_score=result.get('confidence', 0.5),
            confidence=self.activity_level,
            identity_context=brain_state.active_identity
        )
        
        self.storage.store_memory_chunk(memory_chunk)
        
        # Clear reasoning chain for next process
        self.current_reasoning_chain.clear()
    
    def _extract_keywords_from_reasoning(self) -> List[str]:
        """Extract keywords from reasoning chain"""
        keywords = set()
        for thought in self.current_reasoning_chain:
            # Simple keyword extraction
            words = thought.lower().split()
            keywords.update([word for word in words if len(word) > 4])
        return list(keywords)[:10]  # Limit to 10 keywords
    
    def get_status(self) -> Dict[str, Any]:
        """Get current module status"""
        return {
            "name": self.name,
            "active": self.active,
            "activity_level": self.activity_level,
            "last_activity": self.last_activity.isoformat(),
            "current_reasoning_steps": len(self.current_reasoning_chain),
            "decisions_made": len(self.decision_history),
            "planning_depth": self.planning_depth
        }