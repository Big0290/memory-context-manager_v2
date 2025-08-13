#!/usr/bin/env python3
"""
Phase 7A: Prediction Engine - Week 3 Implementation
Core prediction engine for development intelligence with pattern matching and ML integration
"""

import logging
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import json
import hashlib
from collections import defaultdict
import random

# Import our pattern database
from phase7_pattern_database import PatternDatabase

logger = logging.getLogger(__name__)

@dataclass
class Prediction:
    """Represents a development prediction"""
    prediction_id: str
    prediction_type: str  # 'next_action', 'optimization', 'improvement', 'risk'
    title: str
    description: str
    confidence: float  # 0.0 to 1.0
    priority: str  # 'low', 'normal', 'high', 'critical'
    context: Dict[str, Any]
    suggested_actions: List[str]
    estimated_impact: str  # 'low', 'medium', 'high'
    time_to_implement: str  # 'quick', 'moderate', 'extensive'
    created_at: datetime
    source_patterns: List[str]  # IDs of patterns that influenced this prediction

@dataclass
class ContextAnalysis:
    """Analysis of current development context"""
    context_hash: str
    current_file: Optional[str]
    current_function: Optional[str]
    current_class: Optional[str]
    recent_changes: List[str]
    active_patterns: List[str]
    development_phase: str  # 'planning', 'development', 'testing', 'deployment'
    user_activity: Dict[str, Any]
    project_metrics: Dict[str, Any]
    analyzed_at: datetime

class ContextAnalyzer:
    """Analyzes current development context for prediction generation"""
    
    def __init__(self):
        self.context_cache = {}
        self.analysis_patterns = {
            'development_phases': ['planning', 'development', 'testing', 'deployment', 'maintenance'],
            'file_types': ['.py', '.js', '.ts', '.java', '.cpp', '.go', '.rs'],
            'activity_types': ['typing', 'reading', 'debugging', 'testing', 'planning']
        }
    
    async def analyze(self, context: Dict[str, Any]) -> ContextAnalysis:
        """Analyze current development context"""
        try:
            # Generate context hash for caching
            context_hash = self._generate_context_hash(context)
            
            # Check cache first
            if context_hash in self.context_cache:
                return self.context_cache[context_hash]
            
            # Perform context analysis
            analysis = await self._perform_context_analysis(context)
            
            # Cache the result
            self.context_cache[context_hash] = analysis
            
            # Limit cache size
            if len(self.context_cache) > 100:
                oldest_key = min(self.context_cache.keys(), key=lambda k: self.context_cache[k].analyzed_at)
                del self.context_cache[oldest_key]
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing context: {str(e)}")
            return self._create_default_context_analysis(context)
    
    async def _perform_context_analysis(self, context: Dict[str, Any]) -> ContextAnalysis:
        """Perform detailed context analysis"""
        try:
            # Extract basic context information
            current_file = context.get('current_file')
            current_function = context.get('current_function')
            current_class = context.get('current_class')
            
            # Analyze recent changes
            recent_changes = self._analyze_recent_changes(context.get('recent_changes', []))
            
            # Identify active patterns
            active_patterns = self._identify_active_patterns(context)
            
            # Determine development phase
            development_phase = self._determine_development_phase(context)
            
            # Analyze user activity
            user_activity = self._analyze_user_activity(context.get('user_activity', {}))
            
            # Extract project metrics
            project_metrics = self._extract_project_metrics(context.get('project_metrics', {}))
            
            # Create context analysis
            analysis = ContextAnalysis(
                context_hash=self._generate_context_hash(context),
                current_file=current_file,
                current_function=current_function,
                current_class=current_class,
                recent_changes=recent_changes,
                active_patterns=active_patterns,
                development_phase=development_phase,
                user_activity=user_activity,
                project_metrics=project_metrics,
                analyzed_at=datetime.now()
            )
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error performing context analysis: {str(e)}")
            return self._create_default_context_analysis(context)
    
    def _analyze_recent_changes(self, changes: List[str]) -> List[str]:
        """Analyze recent changes for patterns"""
        analyzed_changes = []
        
        for change in changes:
            if isinstance(change, str):
                # Simple change analysis - can be enhanced
                if 'test' in change.lower():
                    analyzed_changes.append('testing_activity')
                elif 'fix' in change.lower() or 'bug' in change.lower():
                    analyzed_changes.append('bug_fixing')
                elif 'refactor' in change.lower():
                    analyzed_changes.append('refactoring')
                elif 'feature' in change.lower() or 'add' in change.lower():
                    analyzed_changes.append('feature_development')
                else:
                    analyzed_changes.append('general_development')
        
        return analyzed_changes
    
    def _identify_active_patterns(self, context: Dict[str, Any]) -> List[str]:
        """Identify patterns currently active in the context"""
        active_patterns = []
        
        # Check for file-based patterns
        if 'current_file' in context:
            file_path = context['current_file']
            if file_path:
                if 'test' in file_path.lower():
                    active_patterns.append('testing_pattern')
                elif 'model' in file_path.lower():
                    active_patterns.append('data_modeling_pattern')
                elif 'view' in file_path.lower():
                    active_patterns.append('ui_pattern')
                elif 'controller' in file_path.lower():
                    active_patterns.append('control_pattern')
        
        # Check for function-based patterns
        if 'current_function' in context:
            func_name = context['current_function']
            if func_name:
                if 'get' in func_name.lower():
                    active_patterns.append('getter_pattern')
                elif 'set' in func_name.lower():
                    active_patterns.append('setter_pattern')
                elif 'validate' in func_name.lower():
                    active_patterns.append('validation_pattern')
                elif 'process' in func_name.lower():
                    active_patterns.append('processing_pattern')
        
        # Check for class-based patterns
        if 'current_class' in context:
            class_name = context['current_class']
            if class_name:
                if 'service' in class_name.lower():
                    active_patterns.append('service_pattern')
                elif 'factory' in class_name.lower():
                    active_patterns.append('factory_pattern')
                elif 'adapter' in class_name.lower():
                    active_patterns.append('adapter_pattern')
                elif 'observer' in class_name.lower():
                    active_patterns.append('observer_pattern')
        
        return active_patterns
    
    def _determine_development_phase(self, context: Dict[str, Any]) -> str:
        """Determine current development phase based on context"""
        # Simple phase detection - can be enhanced with ML
        recent_changes = context.get('recent_changes', [])
        current_file = context.get('current_file', '')
        
        # Check for testing indicators
        if any('test' in str(change).lower() for change in recent_changes) or 'test' in current_file.lower():
            return 'testing'
        
        # Check for deployment indicators
        if any('deploy' in str(change).lower() for change in recent_changes):
            return 'deployment'
        
        # Check for planning indicators
        if any('plan' in str(change).lower() or 'design' in str(change).lower() for change in recent_changes):
            return 'planning'
        
        # Default to development
        return 'development'
    
    def _analyze_user_activity(self, activity: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze user activity patterns"""
        analyzed_activity = {
            'typing_speed': activity.get('typing_speed', 'normal'),
            'pause_frequency': activity.get('pause_frequency', 'normal'),
            'error_rate': activity.get('error_rate', 'low'),
            'focus_level': activity.get('focus_level', 'medium'),
            'activity_intensity': 'high' if activity.get('typing_speed') == 'fast' else 'medium'
        }
        
        return analyzed_activity
    
    def _extract_project_metrics(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Extract relevant project metrics"""
        extracted_metrics = {
            'code_complexity': metrics.get('complexity', 'medium'),
            'test_coverage': metrics.get('test_coverage', 0.0),
            'bug_count': metrics.get('bug_count', 0),
            'performance_score': metrics.get('performance', 0.8),
            'maintainability': metrics.get('maintainability', 0.7)
        }
        
        return extracted_metrics
    
    def _create_default_context_analysis(self, context: Dict[str, Any]) -> ContextAnalysis:
        """Create default context analysis when analysis fails"""
        return ContextAnalysis(
            context_hash=self._generate_context_hash(context),
            current_file=context.get('current_file'),
            current_function=context.get('current_function'),
            current_class=context.get('current_class'),
            recent_changes=[],
            active_patterns=[],
            development_phase='development',
            user_activity={},
            project_metrics={},
            analyzed_at=datetime.now()
        )
    
    def _generate_context_hash(self, context: Dict[str, Any]) -> str:
        """Generate hash for context caching"""
        context_str = json.dumps(context, sort_keys=True, default=str)
        return hashlib.md5(context_str.encode()).hexdigest()

class MLPredictor:
    """Machine learning predictor for development actions"""
    
    def __init__(self):
        self.prediction_models = {}
        self.feature_extractors = {}
        self.initialize_models()
    
    def initialize_models(self):
        """Initialize basic prediction models"""
        # Simple rule-based models for now - can be enhanced with actual ML
        self.prediction_models = {
            'next_action': self._rule_based_next_action,
            'optimization': self._rule_based_optimization,
            'improvement': self._rule_based_improvement,
            'risk': self._rule_based_risk_assessment
        }
    
    async def predict_next_action(self, context_analysis: ContextAnalysis) -> List[Dict[str, Any]]:
        """Predict next development actions using ML models"""
        try:
            predictions = []
            
            # Generate different types of predictions
            next_action_pred = await self.prediction_models['next_action'](context_analysis)
            if next_action_pred:
                predictions.extend(next_action_pred)
            
            optimization_pred = await self.prediction_models['optimization'](context_analysis)
            if optimization_pred:
                predictions.extend(optimization_pred)
            
            improvement_pred = await self.prediction_models['improvement'](context_analysis)
            if improvement_pred:
                predictions.extend(improvement_pred)
            
            risk_pred = await self.prediction_models['risk'](context_analysis)
            if risk_pred:
                predictions.extend(risk_pred)
            
            return predictions
            
        except Exception as e:
            logger.error(f"Error generating ML predictions: {str(e)}")
            return []
    
    async def _rule_based_next_action(self, context: ContextAnalysis) -> List[Dict[str, Any]]:
        """Rule-based next action prediction"""
        predictions = []
        
        # Predict based on development phase
        if context.development_phase == 'planning':
            predictions.append({
                'type': 'next_action',
                'title': 'Create Implementation Plan',
                'description': 'Based on current planning phase, consider creating a detailed implementation plan',
                'confidence': 0.8,
                'priority': 'high',
                'suggested_actions': [
                    'Break down requirements into tasks',
                    'Estimate time for each task',
                    'Identify dependencies between tasks'
                ]
            })
        
        elif context.development_phase == 'development':
            predictions.append({
                'type': 'next_action',
                'title': 'Write Unit Tests',
                'description': 'Consider writing tests for the current functionality',
                'confidence': 0.7,
                'priority': 'normal',
                'suggested_actions': [
                    'Create test cases for current function',
                    'Ensure edge cases are covered',
                    'Run existing tests to verify nothing broke'
                ]
            })
        
        elif context.development_phase == 'testing':
            predictions.append({
                'type': 'next_action',
                'title': 'Fix Identified Issues',
                'description': 'Address any issues found during testing',
                'confidence': 0.9,
                'priority': 'high',
                'suggested_actions': [
                    'Review test results',
                    'Prioritize issues by severity',
                    'Fix critical issues first'
                ]
            })
        
        return predictions
    
    async def _rule_based_optimization(self, context: ContextAnalysis) -> List[Dict[str, Any]]:
        """Rule-based optimization prediction"""
        predictions = []
        
        # Check project metrics for optimization opportunities
        metrics = context.project_metrics
        
        if metrics.get('test_coverage', 0) < 0.8:
            predictions.append({
                'type': 'optimization',
                'title': 'Improve Test Coverage',
                'description': f'Current test coverage is {metrics.get("test_coverage", 0):.1%}, aim for 80%+',
                'confidence': 0.85,
                'priority': 'normal',
                'suggested_actions': [
                    'Identify untested code paths',
                    'Add unit tests for critical functions',
                    'Consider integration tests for complex workflows'
                ]
            })
        
        if metrics.get('performance_score', 1.0) < 0.7:
            predictions.append({
                'type': 'optimization',
                'title': 'Performance Optimization',
                'description': 'Performance score indicates room for improvement',
                'confidence': 0.8,
                'priority': 'normal',
                'suggested_actions': [
                    'Profile code for bottlenecks',
                    'Optimize database queries',
                    'Consider caching strategies'
                ]
            })
        
        return predictions
    
    async def _rule_based_improvement(self, context: ContextAnalysis) -> List[Dict[str, Any]]:
        """Rule-based improvement prediction"""
        predictions = []
        
        # Suggest improvements based on active patterns
        if 'testing_pattern' in context.active_patterns:
            predictions.append({
                'type': 'improvement',
                'title': 'Enhance Testing Strategy',
                'description': 'Consider advanced testing techniques',
                'confidence': 0.7,
                'priority': 'low',
                'suggested_actions': [
                    'Implement property-based testing',
                    'Add performance testing',
                    'Consider mutation testing'
                ]
            })
        
        if 'service_pattern' in context.active_patterns:
            predictions.append({
                'type': 'improvement',
                'title': 'Service Layer Enhancement',
                'description': 'Optimize service layer architecture',
                'confidence': 0.75,
                'priority': 'normal',
                'suggested_actions': [
                    'Add service interfaces',
                    'Implement dependency injection',
                    'Add service monitoring'
                ]
            })
        
        return predictions
    
    async def _rule_based_risk_assessment(self, context: ContextAnalysis) -> List[Dict[str, Any]]:
        """Rule-based risk assessment"""
        predictions = []
        
        # Assess risks based on context
        metrics = context.project_metrics
        
        if metrics.get('bug_count', 0) > 10:
            predictions.append({
                'type': 'risk',
                'title': 'High Bug Count Risk',
                'description': f'Current bug count ({metrics.get("bug_count", 0)}) indicates potential quality issues',
                'confidence': 0.8,
                'priority': 'high',
                'suggested_actions': [
                    'Review bug patterns',
                    'Implement code review process',
                    'Add automated quality checks'
                ]
            })
        
        if metrics.get('maintainability', 1.0) < 0.6:
            predictions.append({
                'type': 'risk',
                'title': 'Maintainability Risk',
                'description': 'Low maintainability score suggests technical debt accumulation',
                'confidence': 0.75,
                'priority': 'normal',
                'suggested_actions': [
                    'Refactor complex functions',
                    'Improve code documentation',
                    'Reduce cyclomatic complexity'
                ]
            })
        
        return predictions

class OptimizationDetector:
    """Detects optimization opportunities in codebase"""
    
    def __init__(self):
        self.optimization_patterns = {
            'performance': ['slow_queries', 'memory_leaks', 'inefficient_algorithms'],
            'quality': ['code_duplication', 'complex_functions', 'poor_naming'],
            'architecture': ['tight_coupling', 'violation_of_principles', 'poor_separation'],
            'security': ['input_validation', 'authentication', 'authorization']
        }
    
    async def find_performance_issues(self, codebase: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find performance optimization opportunities"""
        opportunities = []
        
        # Simple performance detection - can be enhanced
        if codebase.get('complexity_score', 0) > 0.8:
            opportunities.append({
                'type': 'performance',
                'title': 'High Complexity Impact',
                'description': 'High complexity may impact performance',
                'priority': 'normal',
                'estimated_impact': 'medium',
                'time_to_implement': 'moderate'
            })
        
        if codebase.get('memory_usage', 0) > 100:  # MB
            opportunities.append({
                'type': 'performance',
                'title': 'Memory Usage Optimization',
                'description': 'High memory usage detected',
                'priority': 'high',
                'estimated_impact': 'high',
                'time_to_implement': 'moderate'
            })
        
        return opportunities
    
    async def find_quality_issues(self, codebase: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find code quality improvement opportunities"""
        opportunities = []
        
        if codebase.get('duplication_rate', 0) > 0.1:  # 10%
            opportunities.append({
                'type': 'quality',
                'title': 'Code Duplication',
                'description': f'Code duplication rate is {codebase.get("duplication_rate", 0):.1%}',
                'priority': 'normal',
                'estimated_impact': 'medium',
                'time_to_implement': 'moderate'
            })
        
        if codebase.get('test_coverage', 0) < 0.8:
            opportunities.append({
                'type': 'quality',
                'title': 'Low Test Coverage',
                'description': f'Test coverage is {codebase.get("test_coverage", 0):.1%}',
                'priority': 'high',
                'estimated_impact': 'high',
                'time_to_implement': 'extensive'
            })
        
        return opportunities
    
    async def find_architecture_issues(self, codebase: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find architecture optimization opportunities"""
        opportunities = []
        
        if codebase.get('coupling_score', 0) > 0.7:
            opportunities.append({
                'type': 'architecture',
                'title': 'High Coupling',
                'description': 'High coupling between modules detected',
                'priority': 'normal',
                'estimated_impact': 'medium',
                'time_to_implement': 'extensive'
            })
        
        return opportunities
    
    async def find_security_issues(self, codebase: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find security optimization opportunities"""
        opportunities = []
        
        if not codebase.get('input_validation', False):
            opportunities.append({
                'type': 'security',
                'title': 'Input Validation',
                'description': 'Input validation not implemented',
                'priority': 'high',
                'estimated_impact': 'high',
                'time_to_implement': 'moderate'
            })
        
        return opportunities

class PredictionEngine:
    """Core prediction engine for development intelligence"""
    
    def __init__(self, pattern_database: PatternDatabase):
        self.pattern_database = pattern_database
        self.context_analyzer = ContextAnalyzer()
        self.ml_predictor = MLPredictor()
        self.optimization_detector = OptimizationDetector()
        self.prediction_cache = {}
    
    async def predict_next_action(self, current_context: Dict[str, Any]) -> Dict[str, Any]:
        """Predict the next logical development action"""
        try:
            # 1. Analyze current context
            context_analysis = await self.context_analyzer.analyze(current_context)
            
            # 2. Find similar patterns in database
            similar_patterns = await self.pattern_database.find_similar({
                'pattern_type': context_analysis.active_patterns[0] if context_analysis.active_patterns else 'general',
                'confidence_threshold': 0.7
            })
            
            # 3. Generate predictions using ML
            ml_predictions = await self.ml_predictor.predict_next_action(context_analysis)
            
            # 4. Combine pattern-based and ML predictions
            combined_predictions = self._combine_predictions(similar_patterns, ml_predictions, context_analysis)
            
            # 5. Rank and filter predictions
            ranked_predictions = self._rank_predictions(combined_predictions, context_analysis)
            
            return {
                "success": True,
                "predictions": ranked_predictions[:5],  # Top 5 predictions
                "confidence_scores": self._calculate_confidence(ranked_predictions),
                "context_analysis": asdict(context_analysis),
                "prediction_method": "pattern_ml_hybrid",
                "total_predictions": len(ranked_predictions)
            }
            
        except Exception as e:
            logger.error(f"Error predicting next action: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    async def identify_optimization_opportunities(self, codebase: Dict[str, Any]) -> Dict[str, Any]:
        """Identify areas for improvement and optimization"""
        try:
            opportunities = []
            
            # 1. Performance optimization opportunities
            perf_opportunities = await self.optimization_detector.find_performance_issues(codebase)
            opportunities.extend(perf_opportunities)
            
            # 2. Code quality opportunities
            quality_opportunities = await self.optimization_detector.find_quality_issues(codebase)
            opportunities.extend(quality_opportunities)
            
            # 3. Architecture optimization opportunities
            arch_opportunities = await self.optimization_detector.find_architecture_issues(codebase)
            opportunities.extend(arch_opportunities)
            
            # 4. Security optimization opportunities
            security_opportunities = await self.optimization_detector.find_security_issues(codebase)
            opportunities.extend(security_opportunities)
            
            return {
                "success": True,
                "opportunities": opportunities,
                "total_count": len(opportunities),
                "priority_distribution": self._analyze_priority_distribution(opportunities),
                "category_breakdown": self._analyze_category_breakdown(opportunities)
            }
            
        except Exception as e:
            logger.error(f"Error identifying optimization opportunities: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    def _combine_predictions(self, similar_patterns: List[Dict[str, Any]], ml_predictions: List[Dict[str, Any]], context: ContextAnalysis) -> List[Dict[str, Any]]:
        """Combine pattern-based and ML predictions"""
        combined = []
        
        # Add pattern-based predictions
        for pattern in similar_patterns:
            combined.append({
                'type': 'pattern_based',
                'title': f"Apply {pattern.get('pattern_name', 'Pattern')}",
                'description': f"Based on similar pattern: {pattern.get('description', '')}",
                'confidence': pattern.get('confidence', 0.5),
                'priority': 'normal',
                'source_patterns': [pattern.get('pattern_id', '')],
                'suggested_actions': [
                    'Review pattern implementation',
                    'Adapt to current context',
                    'Test pattern effectiveness'
                ]
            })
        
        # Add ML predictions
        for pred in ml_predictions:
            combined.append({
                'type': 'ml_based',
                'title': pred.get('title', 'ML Prediction'),
                'description': pred.get('description', ''),
                'confidence': pred.get('confidence', 0.5),
                'priority': pred.get('priority', 'normal'),
                'source_patterns': [],
                'suggested_actions': pred.get('suggested_actions', [])
            })
        
        return combined
    
    def _rank_predictions(self, predictions: List[Dict[str, Any]], context: ContextAnalysis) -> List[Dict[str, Any]]:
        """Rank predictions by relevance and confidence"""
        try:
            # Calculate ranking scores
            scored_predictions = []
            
            for pred in predictions:
                score = self._calculate_prediction_score(pred, context)
                scored_predictions.append({
                    'prediction': pred,
                    'score': score
                })
            
            # Sort by score (descending)
            scored_predictions.sort(key=lambda x: x['score'], reverse=True)
            
            # Return ranked predictions
            return [item['prediction'] for item in scored_predictions]
            
        except Exception as e:
            logger.error(f"Error ranking predictions: {str(e)}")
            return predictions  # Return original order if ranking fails
    
    def _calculate_prediction_score(self, prediction: Dict[str, Any], context: ContextAnalysis) -> float:
        """Calculate ranking score for a prediction"""
        try:
            score = 0.0
            
            # Base confidence score (40% weight)
            score += 0.4 * prediction.get('confidence', 0.5)
            
            # Priority score (30% weight)
            priority_weights = {'low': 0.3, 'normal': 0.6, 'high': 0.8, 'critical': 1.0}
            priority = prediction.get('priority', 'normal')
            score += 0.3 * priority_weights.get(priority, 0.6)
            
            # Context relevance score (30% weight)
            context_relevance = self._calculate_context_relevance(prediction, context)
            score += 0.3 * context_relevance
            
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating prediction score: {str(e)}")
            return 0.5
    
    def _calculate_context_relevance(self, prediction: Dict[str, Any], context: ContextAnalysis) -> float:
        """Calculate how relevant a prediction is to current context"""
        try:
            relevance = 0.5  # Base relevance
            
            # Check if prediction matches current development phase
            if context.development_phase in prediction.get('title', '').lower():
                relevance += 0.2
            
            # Check if prediction matches active patterns
            if any(pattern in prediction.get('title', '').lower() for pattern in context.active_patterns):
                relevance += 0.2
            
            # Check if prediction addresses recent changes
            if any(change in prediction.get('description', '').lower() for change in context.recent_changes):
                relevance += 0.1
            
            return min(relevance, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating context relevance: {str(e)}")
            return 0.5
    
    def _calculate_confidence(self, predictions: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate confidence metrics for predictions"""
        try:
            if not predictions:
                return {'average_confidence': 0.0, 'high_confidence_count': 0}
            
            confidences = [pred.get('confidence', 0.0) for pred in predictions]
            avg_confidence = sum(confidences) / len(confidences)
            high_confidence_count = len([c for c in confidences if c >= 0.8])
            
            return {
                'average_confidence': avg_confidence,
                'high_confidence_count': high_confidence_count,
                'total_predictions': len(predictions)
            }
            
        except Exception as e:
            logger.error(f"Error calculating confidence: {str(e)}")
            return {'average_confidence': 0.0, 'high_confidence_count': 0}
    
    def _analyze_priority_distribution(self, opportunities: List[Dict[str, Any]]) -> Dict[str, int]:
        """Analyze distribution of opportunities by priority"""
        distribution = defaultdict(int)
        
        for opp in opportunities:
            priority = opp.get('priority', 'normal')
            distribution[priority] += 1
        
        return dict(distribution)
    
    def _analyze_category_breakdown(self, opportunities: List[Dict[str, Any]]) -> Dict[str, int]:
        """Analyze breakdown of opportunities by category"""
        breakdown = defaultdict(int)
        
        for opp in opportunities:
            category = opp.get('type', 'unknown')
            breakdown[category] += 1
        
        return dict(breakdown)

# Example usage and testing
async def main():
    """Example usage of the PredictionEngine"""
    # Initialize pattern database
    db = PatternDatabase("test_prediction.db")
    
    try:
        # Initialize prediction engine
        engine = PredictionEngine(db)
        
        # Test context analysis
        print("🔍 Testing context analysis...")
        context = {
            'current_file': 'src/service.py',
            'current_function': 'process_data',
            'current_class': 'DataService',
            'recent_changes': ['Added new feature', 'Fixed bug in validation'],
            'user_activity': {'typing_speed': 'fast', 'focus_level': 'high'},
            'project_metrics': {'test_coverage': 0.75, 'complexity_score': 0.6}
        }
        
        # Predict next action
        print("\n🔮 Predicting next action...")
        prediction_result = await engine.predict_next_action(context)
        
        if prediction_result.get("success"):
            print(f"✅ Generated {prediction_result['total_predictions']} predictions")
            print(f"📊 Average confidence: {prediction_result['confidence_scores']['average_confidence']:.2f}")
            
            for i, pred in enumerate(prediction_result['predictions'][:3], 1):
                print(f"\n  {i}. {pred['title']}")
                print(f"     Confidence: {pred['confidence']:.2f}")
                print(f"     Priority: {pred['priority']}")
                print(f"     Description: {pred['description']}")
        else:
            print(f"❌ Prediction failed: {prediction_result.get('error')}")
        
        # Test optimization detection
        print("\n🔍 Testing optimization detection...")
        codebase = {
            'complexity_score': 0.85,
            'memory_usage': 150,
            'duplication_rate': 0.15,
            'test_coverage': 0.65,
            'coupling_score': 0.75
        }
        
        optimization_result = await engine.identify_optimization_opportunities(codebase)
        
        if optimization_result.get("success"):
            print(f"✅ Found {optimization_result['total_count']} optimization opportunities")
            
            for opp in optimization_result['opportunities'][:3]:
                print(f"\n  • {opp['title']}")
                print(f"    Type: {opp['type']}, Priority: {opp['priority']}")
                print(f"    Impact: {opp['estimated_impact']}")
        else:
            print(f"❌ Optimization detection failed: {optimization_result.get('error')}")
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
    
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(main())
