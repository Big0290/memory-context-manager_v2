from datetime import datetime
from typing import Dict, Any, List, Optional, Callable
import uuid

from ..core.brain_core import BrainModule
from ..schemas.memory_schema import BrainState, ContextType


class Router(BrainModule):
    """
    Thalamus-inspired Router: Routes inputs to appropriate modules and manages information flow
    Responsible for intelligent routing, priority management, and module coordination
    """
    
    def __init__(self, storage_adapter):
        super().__init__("router", storage_adapter)
        
        # Routing rules and patterns
        self.routing_rules: Dict[str, Dict[str, Any]] = {}
        self.module_capabilities: Dict[str, List[str]] = {}
        self.routing_history: List[Dict[str, Any]] = []
        
        # Load balancing and priority management
        self.module_load: Dict[str, float] = {}
        self.priority_queue: List[Dict[str, Any]] = []
        
        # Learning and adaptation
        self.routing_success_rates: Dict[str, float] = {}
        self.adaptive_routing = True
        
        self._initialize_default_rules()
    
    def _initialize_default_rules(self):
        """Initialize default routing rules"""
        self.routing_rules = {
            # Content-based routing
            "planning": {
                "target_modules": ["frontal_lobe"],
                "keywords": ["plan", "strategy", "goal", "objective", "task"],
                "confidence": 0.8
            },
            "memory": {
                "target_modules": ["memory_core"],
                "keywords": ["remember", "recall", "store", "forget", "memory"],
                "confidence": 0.9
            },
            "emotional": {
                "target_modules": ["emotion_tagger"],
                "keywords": ["feel", "emotion", "important", "urgent", "critical"],
                "confidence": 0.7
            },
            "decision": {
                "target_modules": ["frontal_lobe", "emotion_tagger"],
                "keywords": ["decide", "choose", "option", "alternative", "selection"],
                "confidence": 0.8
            },
            "reflection": {
                "target_modules": ["self_reflector"],
                "keywords": ["reflect", "learn", "analyze", "improve", "pattern"],
                "confidence": 0.7
            },
            "sync": {
                "target_modules": ["sync_bridge"],
                "keywords": ["sync", "share", "collaborate", "multi-agent", "bridge"],
                "confidence": 0.8
            }
        }
        
        # Initialize module capabilities
        self.module_capabilities = {
            "frontal_lobe": ["planning", "reasoning", "decision_making", "task_management"],
            "memory_core": ["storage", "retrieval", "search", "consolidation"],
            "emotion_tagger": ["emotional_analysis", "importance_assessment", "priority_tagging"],
            "router": ["routing", "load_balancing", "priority_management"],
            "self_reflector": ["analysis", "learning", "pattern_recognition", "improvement"],
            "sync_bridge": ["multi_agent_sync", "context_sharing", "collaboration"]
        }
    
    def register_module_capabilities(self, module_name: str, capabilities: List[str]):
        """Register capabilities of a module"""
        self.module_capabilities[module_name] = capabilities
        self.module_load[module_name] = 0.0
    
    def process(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Process routing decisions"""
        operation_type = input_data.get("type", "route_input")
        
        self.set_activity_level(0.9)  # Router is highly active
        
        result = {
            "module": self.name,
            "timestamp": datetime.now().isoformat(),
            "operation": operation_type
        }
        
        if operation_type == "route_input":
            result.update(self._route_input(input_data, brain_state))
        
        elif operation_type == "priority_management":
            result.update(self._manage_priorities(input_data, brain_state))
        
        elif operation_type == "load_balancing":
            result.update(self._balance_module_load(input_data, brain_state))
        
        elif operation_type == "adaptive_routing":
            result.update(self._adaptive_route_learning(input_data, brain_state))
        
        elif operation_type == "route_analysis":
            result.update(self._analyze_routing_patterns(input_data, brain_state))
        
        elif operation_type == "emergency_routing":
            result.update(self._handle_emergency_routing(input_data, brain_state))
        
        else:
            # Default routing behavior
            result.update(self._route_input(input_data, brain_state))
        
        return result
    
    def _route_input(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Route input to appropriate modules"""
        content = input_data.get("content", "")
        context_type = input_data.get("context_type", "general")
        priority = input_data.get("priority", 0.5)
        available_modules = input_data.get("available_modules", list(self.module_capabilities.keys()))
        
        if not content and not context_type:
            return {"success": False, "error": "No content or context provided for routing"}
        
        # Analyze input to determine routing
        routing_analysis = self._analyze_input_for_routing(content, context_type)
        
        # Get routing recommendations
        routing_recommendations = self._get_routing_recommendations(
            routing_analysis, available_modules, priority
        )
        
        # Apply load balancing
        balanced_routing = self._apply_load_balancing(routing_recommendations)
        
        # Apply priority considerations
        prioritized_routing = self._apply_priority_routing(balanced_routing, priority)
        
        # Record routing decision
        routing_record = {
            "input_id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "content_length": len(content),
            "context_type": context_type,
            "priority": priority,
            "routing_analysis": routing_analysis,
            "selected_modules": [r["module"] for r in prioritized_routing],
            "routing_confidence": sum(r["confidence"] for r in prioritized_routing) / len(prioritized_routing) if prioritized_routing else 0
        }
        
        self.routing_history.append(routing_record)
        
        # Keep history manageable
        if len(self.routing_history) > 100:
            self.routing_history = self.routing_history[-50:]
        
        return {
            "success": True,
            "routing_recommendations": prioritized_routing,
            "routing_analysis": routing_analysis,
            "modules_selected": len(prioritized_routing),
            "average_confidence": routing_record["routing_confidence"],
            "load_balancing_applied": len(balanced_routing) != len(routing_recommendations),
            "routing_id": routing_record["input_id"]
        }
    
    def _manage_priorities(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Manage priority queue and processing order"""
        operation = input_data.get("priority_operation", "process_queue")
        
        if operation == "add_to_queue":
            item = input_data.get("item", {})
            priority = item.get("priority", 0.5)
            
            # Add to priority queue with timestamp
            queue_item = {
                "id": str(uuid.uuid4()),
                "timestamp": datetime.now().isoformat(),
                "content": item,
                "priority": priority,
                "urgency_score": self._calculate_urgency(item),
                "deadline": item.get("deadline")
            }
            
            self.priority_queue.append(queue_item)
            self._sort_priority_queue()
            
            return {
                "success": True,
                "item_added": queue_item["id"],
                "queue_position": self._find_queue_position(queue_item["id"]),
                "queue_size": len(self.priority_queue)
            }
        
        elif operation == "process_queue":
            # Process items in priority order
            processed_items = []
            max_items = input_data.get("max_items", 5)
            
            for _ in range(min(max_items, len(self.priority_queue))):
                if self.priority_queue:
                    item = self.priority_queue.pop(0)  # Get highest priority
                    processed_items.append(item)
            
            return {
                "success": True,
                "processed_count": len(processed_items),
                "remaining_in_queue": len(self.priority_queue),
                "processed_items": [item["id"] for item in processed_items]
            }
        
        elif operation == "queue_status":
            return {
                "success": True,
                "queue_size": len(self.priority_queue),
                "high_priority_count": len([item for item in self.priority_queue if item["priority"] > 0.7]),
                "average_priority": sum(item["priority"] for item in self.priority_queue) / len(self.priority_queue) if self.priority_queue else 0,
                "oldest_item_age": (datetime.now() - datetime.fromisoformat(self.priority_queue[-1]["timestamp"])).total_seconds() / 60 if self.priority_queue else 0
            }
    
    def _balance_module_load(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Balance load across available modules"""
        current_loads = input_data.get("module_loads", {})
        target_modules = input_data.get("target_modules", [])
        
        # Update load information
        self.module_load.update(current_loads)
        
        # Calculate load balancing recommendations
        load_balancing_actions = []
        
        # Find overloaded modules
        overloaded_threshold = 0.8
        underloaded_threshold = 0.3
        
        overloaded_modules = {name: load for name, load in self.module_load.items() if load > overloaded_threshold}
        underloaded_modules = {name: load for name, load in self.module_load.items() if load < underloaded_threshold}
        
        # Recommend load redistribution
        for overloaded_module, load in overloaded_modules.items():
            if underloaded_modules:
                # Find best alternative module
                alternative_module = min(underloaded_modules.items(), key=lambda x: x[1])[0]
                
                load_balancing_actions.append({
                    "action": "redistribute_load",
                    "from_module": overloaded_module,
                    "to_module": alternative_module,
                    "estimated_benefit": (load - overloaded_threshold) * 0.5
                })
        
        # Apply load balancing if requested
        if input_data.get("apply_balancing", False):
            for action in load_balancing_actions:
                if action["action"] == "redistribute_load":
                    # Simulate load redistribution
                    from_module = action["from_module"]
                    to_module = action["to_module"]
                    transfer_amount = action["estimated_benefit"]
                    
                    self.module_load[from_module] -= transfer_amount
                    self.module_load[to_module] += transfer_amount
        
        return {
            "success": True,
            "overloaded_modules": list(overloaded_modules.keys()),
            "underloaded_modules": list(underloaded_modules.keys()),
            "load_balancing_actions": load_balancing_actions,
            "balancing_applied": input_data.get("apply_balancing", False),
            "average_load": sum(self.module_load.values()) / len(self.module_load) if self.module_load else 0
        }
    
    def _adaptive_route_learning(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Learn and adapt routing patterns based on success feedback"""
        feedback_data = input_data.get("feedback", {})
        routing_id = input_data.get("routing_id", "")
        
        if not feedback_data:
            return {"success": False, "error": "No feedback data provided"}
        
        # Find the routing record
        routing_record = None
        for record in self.routing_history:
            if record.get("input_id") == routing_id:
                routing_record = record
                break
        
        if not routing_record:
            return {"success": False, "error": "Routing record not found"}
        
        # Update success rates
        success_score = feedback_data.get("success_score", 0.5)
        routing_pattern = self._extract_routing_pattern(routing_record)
        
        if routing_pattern in self.routing_success_rates:
            # Moving average update
            current_rate = self.routing_success_rates[routing_pattern]
            self.routing_success_rates[routing_pattern] = 0.8 * current_rate + 0.2 * success_score
        else:
            self.routing_success_rates[routing_pattern] = success_score
        
        # Adapt routing rules if enabled
        adaptations_made = 0
        if self.adaptive_routing:
            adaptations_made = self._adapt_routing_rules(routing_record, success_score)
        
        return {
            "success": True,
            "routing_id": routing_id,
            "success_score": success_score,
            "routing_pattern": routing_pattern,
            "updated_success_rate": self.routing_success_rates[routing_pattern],
            "adaptations_made": adaptations_made,
            "adaptive_routing_enabled": self.adaptive_routing
        }
    
    def _analyze_routing_patterns(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Analyze routing patterns and performance"""
        analysis_type = input_data.get("analysis_type", "general")
        
        if not self.routing_history:
            return {"success": False, "message": "No routing history available"}
        
        analysis_results = {}
        
        if analysis_type in ["general", "all"]:
            # General routing statistics
            total_routings = len(self.routing_history)
            recent_routings = [r for r in self.routing_history if 
                             (datetime.now() - datetime.fromisoformat(r["timestamp"])).total_seconds() < 3600]
            
            # Module usage patterns
            module_usage = {}
            for record in self.routing_history:
                for module in record["selected_modules"]:
                    module_usage[module] = module_usage.get(module, 0) + 1
            
            analysis_results["general"] = {
                "total_routings": total_routings,
                "recent_routings": len(recent_routings),
                "most_used_modules": sorted(module_usage.items(), key=lambda x: x[1], reverse=True)[:5],
                "average_modules_per_routing": sum(len(r["selected_modules"]) for r in self.routing_history) / total_routings,
                "average_confidence": sum(r["routing_confidence"] for r in self.routing_history) / total_routings
            }
        
        if analysis_type in ["success_rates", "all"]:
            # Success rate analysis
            analysis_results["success_rates"] = {
                "tracked_patterns": len(self.routing_success_rates),
                "success_rates": dict(sorted(self.routing_success_rates.items(), key=lambda x: x[1], reverse=True)),
                "average_success_rate": sum(self.routing_success_rates.values()) / len(self.routing_success_rates) if self.routing_success_rates else 0
            }
        
        if analysis_type in ["load_patterns", "all"]:
            # Load pattern analysis
            analysis_results["load_patterns"] = {
                "current_loads": self.module_load.copy(),
                "load_distribution": self._analyze_load_distribution(),
                "bottlenecks": [module for module, load in self.module_load.items() if load > 0.8]
            }
        
        return {
            "success": True,
            "analysis_type": analysis_type,
            "analysis_results": analysis_results
        }
    
    def _handle_emergency_routing(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Handle emergency routing for critical situations"""
        emergency_type = input_data.get("emergency_type", "general")
        content = input_data.get("content", "")
        
        # Emergency routing bypasses normal load balancing and queuing
        if emergency_type == "critical_error":
            emergency_modules = ["frontal_lobe", "emotion_tagger"]  # Decision making and assessment
        elif emergency_type == "system_failure":
            emergency_modules = ["memory_core", "self_reflector"]  # Preserve state and analyze
        elif emergency_type == "urgent_decision":
            emergency_modules = ["frontal_lobe"]  # Fast decision making
        else:
            emergency_modules = ["frontal_lobe", "emotion_tagger"]  # General emergency
        
        # Create high-priority routing
        emergency_routing = []
        for module in emergency_modules:
            if module in self.module_capabilities:
                emergency_routing.append({
                    "module": module,
                    "confidence": 0.9,
                    "priority": 1.0,
                    "emergency": True,
                    "bypass_queue": True
                })
        
        # Log emergency routing
        emergency_record = {
            "timestamp": datetime.now().isoformat(),
            "emergency_type": emergency_type,
            "content_length": len(content),
            "emergency_modules": emergency_modules,
            "routing_bypassed": True
        }
        
        return {
            "success": True,
            "emergency_type": emergency_type,
            "emergency_routing": emergency_routing,
            "modules_activated": len(emergency_routing),
            "bypass_normal_routing": True,
            "emergency_record": emergency_record
        }
    
    # Helper methods
    def _analyze_input_for_routing(self, content: str, context_type: str) -> Dict[str, Any]:
        """Analyze input to determine routing patterns"""
        content_lower = content.lower()
        
        # Match against routing rules
        rule_matches = {}
        for rule_name, rule in self.routing_rules.items():
            score = 0
            for keyword in rule["keywords"]:
                if keyword in content_lower:
                    score += 1
            
            if score > 0:
                rule_matches[rule_name] = {
                    "score": score,
                    "confidence": rule["confidence"],
                    "target_modules": rule["target_modules"]
                }
        
        # Analyze content characteristics
        content_analysis = {
            "length": len(content),
            "complexity": self._assess_content_complexity(content),
            "emotional_indicators": self._detect_emotional_indicators(content),
            "question_indicators": "?" in content,
            "action_indicators": any(word in content_lower for word in ["do", "make", "create", "execute", "run"])
        }
        
        return {
            "rule_matches": rule_matches,
            "content_analysis": content_analysis,
            "context_type": context_type
        }
    
    def _get_routing_recommendations(self, routing_analysis: Dict[str, Any], 
                                  available_modules: List[str], priority: float) -> List[Dict[str, Any]]:
        """Get routing recommendations based on analysis"""
        recommendations = []
        
        # Process rule matches
        for rule_name, match_data in routing_analysis["rule_matches"].items():
            for module in match_data["target_modules"]:
                if module in available_modules:
                    recommendations.append({
                        "module": module,
                        "confidence": match_data["confidence"] * (match_data["score"] / len(self.routing_rules[rule_name]["keywords"])),
                        "reason": f"matched_rule_{rule_name}",
                        "priority": priority
                    })
        
        # Add default routing if no strong matches
        if not recommendations or max(r["confidence"] for r in recommendations) < 0.5:
            # Route to frontal lobe for general processing
            if "frontal_lobe" in available_modules:
                recommendations.append({
                    "module": "frontal_lobe",
                    "confidence": 0.6,
                    "reason": "default_frontal_processing",
                    "priority": priority
                })
        
        # Remove duplicates and sort by confidence
        unique_recommendations = {}
        for rec in recommendations:
            module = rec["module"]
            if module not in unique_recommendations or rec["confidence"] > unique_recommendations[module]["confidence"]:
                unique_recommendations[module] = rec
        
        final_recommendations = list(unique_recommendations.values())
        final_recommendations.sort(key=lambda x: x["confidence"], reverse=True)
        
        return final_recommendations
    
    def _apply_load_balancing(self, routing_recommendations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Apply load balancing to routing recommendations"""
        balanced_recommendations = []
        
        for rec in routing_recommendations:
            module = rec["module"]
            current_load = self.module_load.get(module, 0.0)
            
            # Adjust confidence based on load
            load_penalty = min(0.3, current_load * 0.5)  # Up to 30% penalty for high load
            adjusted_confidence = rec["confidence"] * (1.0 - load_penalty)
            
            balanced_rec = rec.copy()
            balanced_rec["confidence"] = adjusted_confidence
            balanced_rec["load_penalty"] = load_penalty
            balanced_rec["original_confidence"] = rec["confidence"]
            
            balanced_recommendations.append(balanced_rec)
        
        # Re-sort after load balancing
        balanced_recommendations.sort(key=lambda x: x["confidence"], reverse=True)
        
        return balanced_recommendations
    
    def _apply_priority_routing(self, routing_recommendations: List[Dict[str, Any]], 
                              priority: float) -> List[Dict[str, Any]]:
        """Apply priority considerations to routing"""
        prioritized_recommendations = []
        
        for rec in routing_recommendations:
            # Boost confidence for high priority items
            if priority > 0.8:
                priority_boost = 0.2
            elif priority > 0.6:
                priority_boost = 0.1
            else:
                priority_boost = 0.0
            
            prioritized_rec = rec.copy()
            prioritized_rec["confidence"] = min(1.0, rec["confidence"] + priority_boost)
            prioritized_rec["priority_boost"] = priority_boost
            
            prioritized_recommendations.append(prioritized_rec)
        
        return prioritized_recommendations
    
    def _calculate_urgency(self, item: Dict[str, Any]) -> float:
        """Calculate urgency score for queue item"""
        urgency = 0.0
        
        # Time-based urgency
        if "deadline" in item:
            # This would calculate time until deadline
            urgency += 0.5  # Simplified
        
        # Content-based urgency
        content = str(item.get("content", "")).lower()
        urgent_words = ["urgent", "asap", "immediately", "critical", "emergency"]
        for word in urgent_words:
            if word in content:
                urgency += 0.3
                break
        
        return min(1.0, urgency)
    
    def _sort_priority_queue(self):
        """Sort priority queue by priority and urgency"""
        self.priority_queue.sort(key=lambda item: (item["priority"], item["urgency_score"]), reverse=True)
    
    def _find_queue_position(self, item_id: str) -> int:
        """Find position of item in queue"""
        for i, item in enumerate(self.priority_queue):
            if item["id"] == item_id:
                return i + 1  # 1-based position
        return -1
    
    def _extract_routing_pattern(self, routing_record: Dict[str, Any]) -> str:
        """Extract routing pattern for learning"""
        # Create pattern string from context type and selected modules
        modules = sorted(routing_record["selected_modules"])
        pattern = f"{routing_record['context_type']}:{'-'.join(modules)}"
        return pattern
    
    def _adapt_routing_rules(self, routing_record: Dict[str, Any], success_score: float) -> int:
        """Adapt routing rules based on feedback"""
        adaptations = 0
        
        # If routing was very successful (>0.8), strengthen the pattern
        if success_score > 0.8:
            pattern_type = routing_record["routing_analysis"]["content_analysis"]
            # This would update routing rule weights/patterns
            adaptations += 1
        
        # If routing was unsuccessful (<0.3), weaken or modify the pattern
        elif success_score < 0.3:
            # This would adjust routing rules to avoid similar patterns
            adaptations += 1
        
        return adaptations
    
    def _analyze_load_distribution(self) -> Dict[str, Any]:
        """Analyze load distribution across modules"""
        if not self.module_load:
            return {"error": "No load data available"}
        
        loads = list(self.module_load.values())
        
        return {
            "average_load": sum(loads) / len(loads),
            "max_load": max(loads),
            "min_load": min(loads),
            "load_variance": self._calculate_variance(loads),
            "balanced": max(loads) - min(loads) < 0.3  # Considered balanced if difference < 0.3
        }
    
    def _assess_content_complexity(self, content: str) -> float:
        """Assess complexity of content"""
        # Simple complexity assessment
        complexity = 0.0
        
        # Length factor
        complexity += min(0.3, len(content) / 1000)
        
        # Sentence count
        sentences = content.split('.')
        complexity += min(0.2, len(sentences) / 10)
        
        # Question marks (indicates complexity)
        complexity += content.count('?') * 0.1
        
        # Technical terms (words > 8 chars)
        long_words = [word for word in content.split() if len(word) > 8]
        complexity += min(0.3, len(long_words) / 20)
        
        return min(1.0, complexity)
    
    def _detect_emotional_indicators(self, content: str) -> List[str]:
        """Detect emotional indicators in content"""
        emotional_words = [
            "urgent", "critical", "important", "excited", "worried", 
            "happy", "sad", "angry", "frustrated", "pleased"
        ]
        
        content_lower = content.lower()
        found_indicators = [word for word in emotional_words if word in content_lower]
        
        return found_indicators
    
    def _calculate_variance(self, values: List[float]) -> float:
        """Calculate variance of values"""
        if len(values) < 2:
            return 0.0
        
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        
        return variance
    
    def get_status(self) -> Dict[str, Any]:
        """Get current module status"""
        return {
            "name": self.name,
            "active": self.active,
            "activity_level": self.activity_level,
            "last_activity": self.last_activity.isoformat(),
            "routing_rules": len(self.routing_rules),
            "module_capabilities": len(self.module_capabilities),
            "routing_history_size": len(self.routing_history),
            "priority_queue_size": len(self.priority_queue),
            "success_patterns_tracked": len(self.routing_success_rates),
            "adaptive_routing_enabled": self.adaptive_routing,
            "current_module_loads": self.module_load.copy()
        }