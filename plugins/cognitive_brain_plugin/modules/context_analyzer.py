from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
import re
import json

from ..core.brain_core import BrainModule
from ..schemas.memory_schema import (
    BrainState, MemoryChunk, TaskContext, ContextType, EmotionalWeight
)


class ContextAnalyzer(BrainModule):
    """
    Enhanced Context Analyzer: Deep understanding of user requests and situational nuances
    Responsible for detecting subtle context, implicit goals, and hidden complexity
    """
    
    def __init__(self, storage_adapter):
        super().__init__("context_analyzer", storage_adapter)
        
        # Context pattern recognition
        self.context_patterns = {
            'implicit_goals': [
                r'\b(without breaking|safely|carefully|gently|gradually)\b',
                r'\b(best practice|properly|correctly|right way|standard)\b',
                r'\b(need to|should|must|have to|require)\b',
                r'\b(implement|add|create|build|develop)\b'
            ],
            'complexity_indicators': [
                r'\b(subtle|nuanced|complex|complicated|sophisticated)\b',
                r'\b(enhance|improve|upgrade|evolve|advance)\b',
                r'\b(understanding|comprehension|awareness|insight)\b',
                r'\b(context|situation|circumstance|environment)\b'
            ],
            'uncertainty_markers': [
                r'\b(maybe|possibly|perhaps|might|could)\b',
                r'\b(not sure|unclear|vague|ambiguous|uncertain)\b',
                r'\b(example|instance|case|scenario|situation)\b',
                r'\b(dont have|no idea|unsure|doubt)\b'
            ],
            'emotional_context': {
                'frustrated': [
                    r'\b(frustrated|confused|overwhelmed|stuck|blocked)\b'
                ],
                'excited': [
                    r'\b(excited|interested|curious|motivated|determined)\b'
                ],
                'concerned': [
                    r'\b(concerned|worried|anxious|stressed|pressured)\b'
                ],
                'confident': [
                    r'\b(confident|assured|certain|positive|optimistic)\b'
                ]
            }
        }
        
        # Subtlety detection patterns
        self.subtlety_patterns = {
            'indirect_requests': [
                r'\b(would like|could you|can we|should we|maybe we)\b',
                r'\b(it would be nice|it might help|perhaps we could|if possible)\b',
                r'\b(thinking about|considering|exploring|investigating)\b'
            ],
            'context_dependent': [
                r'\b(depending on|based on|given that|assuming|if)\b',
                r'\b(when|where|how|why|what if)\b',
                r'\b(under these circumstances|in this context|for this case)\b'
            ],
            'priority_indicators': [
                r'\b(important|critical|urgent|priority|focus)\b',
                r'\b(not urgent|low priority|when convenient|sometime)\b',
                r'\b(balance|trade-off|compromise|middle ground)\b'
            ]
        }
        
        # Context depth analysis
        self.context_depth_indicators = {
            'surface_level': ['simple', 'basic', 'straightforward', 'direct'],
            'medium_depth': ['moderate', 'standard', 'typical', 'usual'],
            'deep_level': ['complex', 'sophisticated', 'advanced', 'expert'],
            'meta_level': ['meta', 'self-referential', 'recursive', 'reflective']
        }
        
        # Learning and adaptation
        self.context_history: List[Dict[str, Any]] = []
        self.pattern_confidence: Dict[str, float] = {}
        self.learning_rate = 0.15
        
    def process(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Process input for deep contextual analysis"""
        operation_type = input_data.get("type", "context_analysis")
        
        # Update context activity
        brain_state.context_activity = 0.8
        self.set_activity_level(0.8)
        
        result = {
            "module": self.name,
            "timestamp": datetime.now().isoformat(),
            "operation": operation_type
        }
        
        if operation_type == "context_analysis":
            result.update(self._analyze_context_deeply(input_data, brain_state))
        
        elif operation_type == "subtlety_detection":
            result.update(self._detect_subtle_context(input_data, brain_state))
        
        elif operation_type == "context_depth_assessment":
            result.update(self._assess_context_depth(input_data, brain_state))
        
        elif operation_type == "implicit_goal_extraction":
            result.update(self._extract_implicit_goals(input_data, brain_state))
        
        elif operation_type == "context_complexity_analysis":
            result.update(self._analyze_context_complexity(input_data, brain_state))
        
        else:
            # Default: deep context analysis
            result.update(self._analyze_context_deeply(input_data, brain_state))
        
        return result
    
    def _analyze_context_deeply(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Perform deep contextual analysis of the input"""
        content = str(input_data.get("content", ""))
        user_id = input_data.get("user_id", "unknown")
        
        # Multi-layer context analysis
        context_layers = {
            "explicit_content": self._analyze_explicit_content(content),
            "implicit_goals": self._extract_implicit_goals_from_content(content),
            "emotional_context": self._analyze_emotional_context(content),
            "complexity_level": self._assess_complexity_level(content),
            "uncertainty_factors": self._detect_uncertainty(content),
            "priority_signals": self._detect_priority_signals(content),
            "context_dependencies": self._identify_context_dependencies(content)
        }
        
        # Calculate overall context score
        context_score = self._calculate_context_score(context_layers)
        
        # Identify subtle patterns
        subtle_patterns = self._detect_subtle_patterns(content)
        
        # Generate context insights
        insights = self._generate_context_insights(context_layers, subtle_patterns)
        
        # Store context analysis for learning
        self._store_context_analysis(content, context_layers, context_score, brain_state)
        
        return {
            "context_layers": context_layers,
            "context_score": context_score,
            "subtle_patterns": subtle_patterns,
            "insights": insights,
            "recommendations": self._generate_recommendations(context_layers, insights)
        }
    
    def _analyze_explicit_content(self, content: str) -> Dict[str, Any]:
        """Analyze the explicit content of the message"""
        return {
            "length": len(content),
            "word_count": len(content.split()),
            "sentence_count": len([s for s in content.split('.') if s.strip()]),
            "key_topics": self._extract_key_topics(content),
            "action_words": self._extract_action_words(content),
            "technical_terms": self._extract_technical_terms(content)
        }
    
    def _extract_implicit_goals_from_content(self, content: str) -> Dict[str, Any]:
        """Extract implicit goals and intentions from the content"""
        implicit_goals = []
        
        # Check for safety/quality concerns
        if any(word in content.lower() for word in ['without breaking', 'safely', 'carefully']):
            implicit_goals.append("safety_first")
        
        # Check for best practice adherence
        if any(word in content.lower() for word in ['best practice', 'properly', 'correctly']):
            implicit_goals.append("quality_standards")
        
        # Check for implementation requests
        if any(word in content.lower() for word in ['implement', 'add', 'create', 'build']):
            implicit_goals.append("implementation_needed")
        
        # Check for learning/understanding goals
        if any(word in content.lower() for word in ['understand', 'learn', 'explore', 'assess']):
            implicit_goals.append("knowledge_acquisition")
        
        return {
            "detected_goals": implicit_goals,
            "confidence": len(implicit_goals) / 4.0,  # Normalize to 0-1
            "primary_goal": implicit_goals[0] if implicit_goals else "general_inquiry"
        }
    
    def _analyze_emotional_context(self, content: str) -> Dict[str, Any]:
        """Analyze emotional context and tone"""
        emotional_indicators = {}
        
        for emotion_type, patterns in self.context_patterns['emotional_context'].items():
            matches = [pattern for pattern in patterns if re.search(pattern, content.lower())]
            if matches:
                emotional_indicators[emotion_type] = len(matches)
        
        # Calculate emotional intensity
        total_emotional_indicators = sum(emotional_indicators.values())
        emotional_intensity = min(1.0, total_emotional_indicators / 5.0)
        
        return {
            "detected_emotions": emotional_indicators,
            "emotional_intensity": emotional_intensity,
            "primary_emotion": max(emotional_indicators.items(), key=lambda x: x[1])[0] if emotional_indicators else "neutral"
        }
    
    def _assess_complexity_level(self, content: str) -> Dict[str, Any]:
        """Assess the complexity level of the request"""
        complexity_score = 0.0
        
        # Check for complexity indicators
        for pattern in self.context_patterns['complexity_indicators']:
            if re.search(pattern, content.lower()):
                complexity_score += 0.2
        
        # Check for uncertainty markers
        for pattern in self.context_patterns['uncertainty_markers']:
            if re.search(pattern, content.lower()):
                complexity_score += 0.15
        
        # Check for indirect language
        for pattern in self.subtlety_patterns['indirect_requests']:
            if re.search(pattern, content.lower()):
                complexity_score += 0.1
        
        # Normalize to 0-1 range
        complexity_score = min(1.0, complexity_score)
        
        # Determine complexity category
        if complexity_score < 0.3:
            complexity_category = "simple"
        elif complexity_score < 0.6:
            complexity_category = "moderate"
        else:
            complexity_category = "complex"
        
        return {
            "score": complexity_score,
            "category": complexity_category,
            "indicators": self._get_complexity_indicators(content)
        }
    
    def _detect_uncertainty(self, content: str) -> Dict[str, Any]:
        """Detect uncertainty and ambiguity in the request"""
        uncertainty_factors = []
        
        for pattern in self.context_patterns['uncertainty_markers']:
            if re.search(pattern, content.lower()):
                uncertainty_factors.append(pattern)
        
        # Check for lack of examples
        if "example" in content.lower() and "dont have" in content.lower():
            uncertainty_factors.append("no_examples_provided")
        
        # Check for vague language
        vague_words = ['something', 'thing', 'stuff', 'whatever', 'somehow']
        if any(word in content.lower() for word in vague_words):
            uncertainty_factors.append("vague_language")
        
        return {
            "factors": uncertainty_factors,
            "uncertainty_level": min(1.0, len(uncertainty_factors) / 5.0),
            "confidence_needed": len(uncertainty_factors) > 0
        }
    
    def _detect_priority_signals(self, content: str) -> Dict[str, Any]:
        """Detect priority and urgency signals"""
        priority_indicators = []
        urgency_level = "low"
        
        # Check for high priority indicators
        high_priority_words = ['urgent', 'critical', 'immediately', 'asap', 'emergency']
        if any(word in content.lower() for word in high_priority_words):
            priority_indicators.append("high_priority")
            urgency_level = "high"
        
        # Check for medium priority indicators
        medium_priority_words = ['important', 'soon', 'when possible', 'priority']
        if any(word in content.lower() for word in medium_priority_words):
            priority_indicators.append("medium_priority")
            if urgency_level == "low":
                urgency_level = "medium"
        
        # Check for low priority indicators
        low_priority_words = ['when convenient', 'sometime', 'low priority', 'not urgent']
        if any(word in content.lower() for word in low_priority_words):
            priority_indicators.append("low_priority")
        
        return {
            "indicators": priority_indicators,
            "urgency_level": urgency_level,
            "priority_score": self._calculate_priority_score(urgency_level)
        }
    
    def _identify_context_dependencies(self, content: str) -> Dict[str, Any]:
        """Identify dependencies and context requirements"""
        dependencies = []
        
        # Check for conditional dependencies
        conditional_words = ['if', 'when', 'assuming', 'given that', 'depending on']
        if any(word in content.lower() for word in conditional_words):
            dependencies.append("conditional_execution")
        
        # Check for resource dependencies
        resource_words = ['time', 'money', 'people', 'tools', 'access']
        if any(word in content.lower() for word in resource_words):
            dependencies.append("resource_requirements")
        
        # Check for knowledge dependencies
        knowledge_words = ['understand', 'know', 'learn', 'research', 'investigate']
        if any(word in content.lower() for word in knowledge_words):
            dependencies.append("knowledge_prerequisites")
        
        return {
            "dependencies": dependencies,
            "dependency_count": len(dependencies),
            "complexity_impact": len(dependencies) * 0.2
        }
    
    def _detect_subtle_patterns(self, content: str) -> List[Dict[str, Any]]:
        """Detect subtle patterns and implicit meanings"""
        subtle_patterns = []
        
        # Check for indirect requests
        for pattern in self.subtlety_patterns['indirect_requests']:
            if re.search(pattern, content.lower()):
                subtle_patterns.append({
                    "type": "indirect_request",
                    "pattern": pattern,
                    "confidence": 0.8
                })
        
        # Check for context-dependent language
        for pattern in self.subtlety_patterns['context_dependent']:
            if re.search(pattern, content.lower()):
                subtle_patterns.append({
                    "type": "context_dependent",
                    "pattern": pattern,
                    "confidence": 0.7
                })
        
        # Check for meta-level thinking
        meta_indicators = ['thinking about', 'considering', 'exploring', 'investigating']
        if any(indicator in content.lower() for indicator in meta_indicators):
            subtle_patterns.append({
                "type": "meta_cognitive",
                "pattern": "meta_thinking",
                "confidence": 0.9
            })
        
        return subtle_patterns
    
    def _calculate_context_score(self, context_layers: Dict[str, Any]) -> float:
        """Calculate overall context understanding score"""
        score = 0.0
        
        # Weight different layers
        weights = {
            "explicit_content": 0.2,
            "implicit_goals": 0.25,
            "emotional_context": 0.15,
            "complexity_level": 0.2,
            "uncertainty_factors": 0.1,
            "priority_signals": 0.05,
            "context_dependencies": 0.05
        }
        
        for layer, weight in weights.items():
            if layer in context_layers:
                layer_score = self._normalize_layer_score(context_layers[layer])
                score += layer_score * weight
        
        return min(1.0, score)
    
    def _normalize_layer_score(self, layer_data: Any) -> float:
        """Normalize layer data to a 0-1 score"""
        if isinstance(layer_data, dict):
            # Handle different layer types
            if "confidence" in layer_data:
                return layer_data["confidence"]
            elif "score" in layer_data:
                return layer_data["score"]
            elif "uncertainty_level" in layer_data:
                return 1.0 - layer_data["uncertainty_level"]  # Invert uncertainty
            else:
                return 0.5  # Default score
        elif isinstance(layer_data, (int, float)):
            return min(1.0, max(0.0, layer_data))
        else:
            return 0.5
    
    def _generate_context_insights(self, context_layers: Dict[str, Any], subtle_patterns: List[Dict[str, Any]]) -> List[str]:
        """Generate insights based on context analysis"""
        insights = []
        
        # Generate insights from implicit goals
        if context_layers.get("implicit_goals", {}).get("detected_goals"):
            goals = context_layers["implicit_goals"]["detected_goals"]
            insights.append(f"User has {len(goals)} implicit goals: {', '.join(goals)}")
        
        # Generate insights from complexity
        complexity = context_layers.get("complexity_level", {})
        if complexity.get("category") == "complex":
            insights.append("Request shows high complexity, suggesting need for careful analysis")
        
        # Generate insights from uncertainty
        uncertainty = context_layers.get("uncertainty_factors", {})
        if uncertainty.get("uncertainty_level", 0) > 0.5:
            insights.append("High uncertainty detected - user may need guidance and examples")
        
        # Generate insights from subtle patterns
        if subtle_patterns:
            pattern_types = [p["type"] for p in subtle_patterns]
            insights.append(f"Detected subtle patterns: {', '.join(pattern_types)}")
        
        return insights
    
    def _generate_recommendations(self, context_layers: Dict[str, Any], insights: List[str]) -> List[str]:
        """Generate actionable recommendations based on context analysis"""
        recommendations = []
        
        # Recommendations based on complexity
        complexity = context_layers.get("complexity_level", {})
        if complexity.get("category") == "complex":
            recommendations.append("Break down the request into smaller, manageable components")
            recommendations.append("Provide step-by-step implementation approach")
        
        # Recommendations based on uncertainty
        uncertainty = context_layers.get("uncertainty_factors", {})
        if uncertainty.get("uncertainty_level", 0) > 0.5:
            recommendations.append("Ask clarifying questions to reduce uncertainty")
            recommendations.append("Provide concrete examples and use cases")
        
        # Recommendations based on implicit goals
        implicit_goals = context_layers.get("implicit_goals", {})
        if "safety_first" in implicit_goals.get("detected_goals", []):
            recommendations.append("Implement with safety checks and validation")
            recommendations.append("Use gradual rollout approach")
        
        if "quality_standards" in implicit_goals.get("detected_goals", []):
            recommendations.append("Follow established best practices and patterns")
            recommendations.append("Include testing and validation steps")
        
        return recommendations
    
    def _extract_key_topics(self, content: str) -> List[str]:
        """Extract key topics from content"""
        # Simple topic extraction - can be enhanced with NLP
        words = content.lower().split()
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        topics = [word for word in words if word not in stop_words and len(word) > 3]
        return list(set(topics))[:5]  # Return top 5 unique topics
    
    def _extract_action_words(self, content: str) -> List[str]:
        """Extract action words from content"""
        action_words = []
        action_patterns = [
            r'\b(implement|create|build|develop|add|enhance|improve|fix|solve|analyze|understand|learn)\b'
        ]
        
        for pattern in action_patterns:
            matches = re.findall(pattern, content.lower())
            action_words.extend(matches)
        
        return list(set(action_words))
    
    def _extract_technical_terms(self, content: str) -> List[str]:
        """Extract technical terms from content"""
        technical_terms = []
        tech_patterns = [
            r'\b(api|database|function|module|plugin|integration|system|architecture|algorithm|protocol)\b',
            r'\b(implementation|deployment|configuration|optimization|scalability|security|performance)\b'
        ]
        
        for pattern in tech_patterns:
            matches = re.findall(pattern, content.lower())
            technical_terms.extend(matches)
        
        return list(set(technical_terms))
    
    def _get_complexity_indicators(self, content: str) -> List[str]:
        """Get specific complexity indicators from content"""
        indicators = []
        
        for pattern in self.context_patterns['complexity_indicators']:
            if re.search(pattern, content.lower()):
                indicators.append(pattern)
        
        return indicators
    
    def _calculate_priority_score(self, urgency_level: str) -> float:
        """Calculate priority score based on urgency level"""
        priority_scores = {
            "low": 0.3,
            "medium": 0.6,
            "high": 0.9
        }
        return priority_scores.get(urgency_level, 0.5)
    
    def _store_context_analysis(self, content: str, context_layers: Dict[str, Any], 
                               context_score: float, brain_state: BrainState):
        """Store context analysis for learning and improvement"""
        analysis_record = {
            "timestamp": datetime.now().isoformat(),
            "content": content[:200],  # Store first 200 chars
            "context_layers": context_layers,
            "context_score": context_score,
            "brain_state": brain_state.dict() if hasattr(brain_state, 'dict') else str(brain_state)
        }
        
        self.context_history.append(analysis_record)
        
        # Keep only last 100 analyses
        if len(self.context_history) > 100:
            self.context_history = self.context_history[-100:]
        
        # Update pattern confidence based on results
        self._update_pattern_confidence(context_score)
    
    def _update_pattern_confidence(self, context_score: float):
        """Update confidence in pattern recognition based on results"""
        for pattern_type in self.pattern_confidence:
            # Adjust confidence based on how well we performed
            if context_score > 0.7:
                self.pattern_confidence[pattern_type] = min(1.0, 
                    self.pattern_confidence.get(pattern_type, 0.5) + self.learning_rate)
            elif context_score < 0.3:
                self.pattern_confidence[pattern_type] = max(0.0, 
                    self.pattern_confidence.get(pattern_type, 0.5) - self.learning_rate * 0.5)
    
    def get_status(self) -> Dict[str, Any]:
        """Get module status and statistics"""
        return {
            "module": self.name,
            "status": "active",
            "context_analyses_performed": len(self.context_history),
            "pattern_confidence": self.pattern_confidence,
            "learning_rate": self.learning_rate,
            "last_analysis": self.context_history[-1]["timestamp"] if self.context_history else None
        }
    
    def _detect_subtle_context(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Detect subtle context patterns in the input"""
        content = str(input_data.get("content", ""))
        
        subtle_patterns = self._detect_subtle_patterns(content)
        context_score = self._calculate_subtlety_score(subtle_patterns)
        
        return {
            "subtle_patterns": subtle_patterns,
            "subtlety_score": context_score,
            "confidence": len(subtle_patterns) / 3.0,  # Normalize to 0-1
            "recommendations": self._generate_subtlety_recommendations(subtle_patterns)
        }
    
    def _assess_context_depth(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Assess the depth and sophistication of the context"""
        content = str(input_data.get("content", ""))
        
        depth_indicators = self._identify_depth_indicators(content)
        depth_score = self._calculate_depth_score(depth_indicators)
        
        return {
            "depth_indicators": depth_indicators,
            "depth_score": depth_score,
            "depth_category": self._categorize_depth(depth_score),
            "sophistication_level": self._assess_sophistication(content)
        }
    
    def _extract_implicit_goals(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Extract implicit goals from the input"""
        content = str(input_data.get("content", ""))
        
        implicit_goals = self._extract_implicit_goals_from_content(content)
        
        return {
            "implicit_goals": implicit_goals,
            "extraction_confidence": implicit_goals.get("confidence", 0.0),
            "goal_complexity": len(implicit_goals.get("detected_goals", [])),
            "recommendations": self._generate_goal_based_recommendations(implicit_goals)
        }
    
    def _analyze_context_complexity(self, input_data: Dict[str, Any], brain_state: BrainState) -> Dict[str, Any]:
        """Analyze the complexity of the context"""
        content = str(input_data.get("content", ""))
        
        complexity_analysis = self._assess_complexity_level(content)
        dependencies = self._identify_context_dependencies(content)
        
        return {
            "complexity_analysis": complexity_analysis,
            "dependencies": dependencies,
            "overall_complexity": complexity_analysis.get("score", 0.0) + dependencies.get("complexity_impact", 0.0),
            "risk_assessment": self._assess_complexity_risks(complexity_analysis, dependencies)
        }
    
    def _calculate_subtlety_score(self, subtle_patterns: List[Dict[str, Any]]) -> float:
        """Calculate a score for how subtle the context is"""
        if not subtle_patterns:
            return 0.0
        
        total_confidence = sum(pattern.get("confidence", 0.0) for pattern in subtle_patterns)
        pattern_count = len(subtle_patterns)
        
        return min(1.0, (total_confidence + pattern_count * 0.1) / 2.0)
    
    def _generate_subtlety_recommendations(self, subtle_patterns: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on detected subtlety"""
        recommendations = []
        
        for pattern in subtle_patterns:
            if pattern["type"] == "indirect_request":
                recommendations.append("User is making an indirect request - consider offering explicit options")
            elif pattern["type"] == "context_dependent":
                recommendations.append("Request depends on context - gather more information before proceeding")
            elif pattern["type"] == "meta_cognitive":
                recommendations.append("User is thinking meta-cognitively - provide reflective responses")
        
        return recommendations
    
    def _identify_depth_indicators(self, content: str) -> Dict[str, Any]:
        """Identify indicators of context depth"""
        depth_indicators = {}
        
        for depth_level, indicators in self.context_depth_indicators.items():
            matches = [indicator for indicator in indicators if indicator in content.lower()]
            if matches:
                depth_indicators[depth_level] = matches
        
        return depth_indicators
    
    def _calculate_depth_score(self, depth_indicators: Dict[str, Any]) -> float:
        """Calculate a score for context depth"""
        depth_weights = {
            "surface_level": 0.2,
            "medium_depth": 0.5,
            "deep_level": 0.8,
            "meta_level": 1.0
        }
        
        score = 0.0
        for depth_level, indicators in depth_indicators.items():
            if indicators:
                score += depth_weights.get(depth_level, 0.5) * len(indicators)
        
        return min(1.0, score / 3.0)  # Normalize
    
    def _categorize_depth(self, depth_score: float) -> str:
        """Categorize the depth level"""
        if depth_score < 0.3:
            return "surface"
        elif depth_score < 0.6:
            return "medium"
        elif depth_score < 0.9:
            return "deep"
        else:
            return "meta"
    
    def _assess_sophistication(self, content: str) -> str:
        """Assess the sophistication level of the content"""
        sophistication_indicators = [
            "architecture", "algorithm", "optimization", "scalability", "integration",
            "framework", "paradigm", "methodology", "strategy", "approach"
        ]
        
        matches = sum(1 for indicator in sophistication_indicators if indicator in content.lower())
        
        if matches >= 3:
            return "expert"
        elif matches >= 1:
            return "intermediate"
        else:
            return "beginner"
    
    def _generate_goal_based_recommendations(self, implicit_goals: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on detected implicit goals"""
        recommendations = []
        goals = implicit_goals.get("detected_goals", [])
        
        if "safety_first" in goals:
            recommendations.append("Prioritize safety and stability in implementation")
        
        if "quality_standards" in goals:
            recommendations.append("Follow industry best practices and coding standards")
        
        if "implementation_needed" in goals:
            recommendations.append("Provide concrete implementation steps and code examples")
        
        if "knowledge_acquisition" in goals:
            recommendations.append("Include explanations and learning resources")
        
        return recommendations
    
    def _assess_complexity_risks(self, complexity_analysis: Dict[str, Any], dependencies: Dict[str, Any]) -> Dict[str, Any]:
        """Assess risks associated with complexity"""
        complexity_score = complexity_analysis.get("score", 0.0)
        dependency_count = dependencies.get("dependency_count", 0)
        
        risks = []
        risk_level = "low"
        
        if complexity_score > 0.7:
            risks.append("High complexity may lead to implementation challenges")
            risk_level = "high"
        
        if dependency_count > 2:
            risks.append("Multiple dependencies increase failure points")
            risk_level = "medium" if risk_level == "low" else "high"
        
        if complexity_score > 0.5 and dependency_count > 1:
            risks.append("Complex request with dependencies requires careful planning")
            risk_level = "high"
        
        return {
            "risks": risks,
            "risk_level": risk_level,
            "mitigation_strategies": self._generate_risk_mitigation(risks, risk_level)
        }
    
    def _generate_risk_mitigation(self, risks: List[str], risk_level: str) -> List[str]:
        """Generate risk mitigation strategies"""
        strategies = []
        
        if risk_level == "high":
            strategies.append("Break down into smaller, manageable tasks")
            strategies.append("Implement with extensive testing and validation")
            strategies.append("Use iterative development approach")
        
        elif risk_level == "medium":
            strategies.append("Implement with careful testing")
            strategies.append("Monitor for potential issues")
            strategies.append("Have fallback plans ready")
        
        else:
            strategies.append("Standard implementation approach")
            strategies.append("Basic testing and validation")
        
        return strategies
