#!/usr/bin/env python3
"""
Personalization Engine - Phase 3 of Memory Context Manager v2
Learns coding preferences, workflow patterns, and provides intelligent context injection
"""

import os
import json
import time
import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import logging
from collections import defaultdict
import hashlib

logger = logging.getLogger(__name__)

@dataclass
class StylePattern:
    """Pattern representing coding style preferences"""
    pattern_type: str  # 'naming', 'structure', 'documentation', 'testing'
    pattern: str
    confidence: float
    frequency: int
    examples: List[str]
    source_files: List[str]
    created_at: float
    updated_at: float

@dataclass
class WorkflowPattern:
    """Pattern representing development workflow preferences"""
    pattern_type: str  # 'debugging', 'testing', 'refactoring', 'documentation'
    sequence: List[str]
    frequency: int
    success_rate: float
    time_spent: float
    context: Dict[str, Any]
    created_at: float
    updated_at: float

@dataclass
class DecisionPattern:
    """Pattern representing architectural decision preferences"""
    decision_type: str  # 'architecture', 'library', 'pattern', 'structure'
    choice: str
    reasoning: str
    alternatives: List[str]
    frequency: int
    success_rate: float
    context: Dict[str, Any]
    created_at: float
    updated_at: float

@dataclass
class LearningPattern:
    """Pattern representing how you learn and adapt"""
    learning_type: str  # 'new_technology', 'problem_solving', 'code_review'
    approach: str
    effectiveness: float
    time_to_mastery: float
    resources_used: List[str]
    context: Dict[str, Any]
    created_at: float
    updated_at: float

@dataclass
class ContextSuggestion:
    """Suggestion for context injection based on learned patterns"""
    suggestion_type: str  # 'proactive', 'reactive', 'predictive'
    content: str
    relevance_score: float
    confidence: float
    source_pattern: str
    context: Dict[str, Any]
    created_at: float

class PreferenceLearningEngine:
    """Learns and models your coding preferences and workflow patterns"""
    
    def __init__(self):
        self.style_patterns: Dict[str, StylePattern] = {}
        self.workflow_patterns: Dict[str, WorkflowPattern] = {}
        self.decision_patterns: Dict[str, DecisionPattern] = {}
        self.learning_patterns: Dict[str, LearningPattern] = {}
        
        # Pattern detection rules
        self.naming_patterns = {
            'snake_case': r'\b[a-z][a-z0-9_]*\b',
            'camel_case': r'\b[a-z][a-zA-Z0-9]*\b',
            'pascal_case': r'\b[A-Z][a-zA-Z0-9]*\b',
            'kebab_case': r'\b[a-z][a-z0-9-]*\b',
            'screaming_snake': r'\b[A-Z][A-Z0-9_]*\b'
        }
        
        self.structure_patterns = {
            'class_organization': r'class\s+\w+.*?:\s*\n(.*?)(?=\n\S|\Z)',
            'function_organization': r'def\s+\w+.*?:\s*\n(.*?)(?=\n\S|\Z)',
            'import_organization': r'(?:from|import)\s+.*?(?=\n|$)',
            'comment_style': r'#\s*(.+)|"""(.+?)"""|/\*\*(.+?)\*/'
        }
        
        self.workflow_indicators = {
            'debugging': ['print', 'debug', 'log', 'breakpoint', 'pdb'],
            'testing': ['test', 'assert', 'pytest', 'unittest', 'mock'],
            'refactoring': ['refactor', 'extract', 'rename', 'move', 'restructure'],
            'documentation': ['docstring', 'comment', 'readme', 'docs', 'api']
        }
    
    def learn_from_code(self, code_sample: str, file_path: str) -> List[StylePattern]:
        """Learn coding style from code samples"""
        discovered_patterns = []
        
        # Analyze naming conventions
        naming_patterns = self._analyze_naming_conventions(code_sample)
        for pattern_type, pattern_info in naming_patterns.items():
            pattern_id = f"naming_{pattern_type}_{hash(file_path) % 1000}"
            
            if pattern_id in self.style_patterns:
                # Update existing pattern
                existing = self.style_patterns[pattern_id]
                existing.frequency += 1
                existing.examples.append(pattern_info['example'])
                existing.updated_at = time.time()
                discovered_patterns.append(existing)
            else:
                # Create new pattern
                new_pattern = StylePattern(
                    pattern_type='naming',
                    pattern=pattern_type,
                    confidence=0.8,
                    frequency=1,
                    examples=[pattern_info['example']],
                    source_files=[file_path],
                    created_at=time.time(),
                    updated_at=time.time()
                )
                self.style_patterns[pattern_id] = new_pattern
                discovered_patterns.append(new_pattern)
        
        # Analyze structural patterns
        structure_patterns = self._analyze_structure_patterns(code_sample)
        for pattern_type, pattern_info in structure_patterns.items():
            pattern_id = f"structure_{pattern_type}_{hash(file_path) % 1000}"
            
            if pattern_id in self.style_patterns:
                existing = self.style_patterns[pattern_id]
                existing.frequency += 1
                existing.examples.append(pattern_info['example'])
                existing.updated_at = time.time()
                discovered_patterns.append(existing)
            else:
                new_pattern = StylePattern(
                    pattern_type='structure',
                    pattern=pattern_type,
                    confidence=0.7,
                    frequency=1,
                    examples=[pattern_info['example']],
                    source_files=[file_path],
                    created_at=time.time(),
                    updated_at=time.time()
                )
                self.style_patterns[pattern_id] = new_pattern
                discovered_patterns.append(new_pattern)
        
        return discovered_patterns
    
    def _analyze_naming_conventions(self, code: str) -> Dict[str, Dict[str, Any]]:
        """Analyze naming conventions in code"""
        patterns = {}
        
        for convention, regex in self.naming_patterns.items():
            matches = re.findall(regex, code)
            if matches:
                # Filter out common words and short names
                filtered_matches = [m for m in matches if len(m) > 2 and m.lower() not in ['the', 'and', 'or', 'for', 'in', 'on', 'at', 'to', 'of', 'a', 'an']]
                
                if filtered_matches:
                    patterns[convention] = {
                        'count': len(filtered_matches),
                        'example': filtered_matches[0],
                        'confidence': min(0.9, len(filtered_matches) / 10)
                    }
        
        return patterns
    
    def _analyze_structure_patterns(self, code: str) -> Dict[str, Dict[str, Any]]:
        """Analyze structural patterns in code"""
        patterns = {}
        
        for pattern_type, regex in self.structure_patterns.items():
            matches = re.findall(regex, code, re.DOTALL | re.MULTILINE)
            if matches:
                patterns[pattern_type] = {
                    'count': len(matches),
                    'example': matches[0][:100] + '...' if len(matches[0]) > 100 else matches[0],
                    'confidence': min(0.8, len(matches) / 5)
                }
        
        return patterns
    
    def learn_from_workflow(self, workflow_data: Dict[str, Any]) -> WorkflowPattern:
        """Learn workflow patterns from development activities"""
        workflow_type = workflow_data.get('type', 'unknown')
        workflow_id = f"workflow_{workflow_type}_{int(time.time())}"
        
        # Extract workflow information
        sequence = workflow_data.get('sequence', [])
        success = workflow_data.get('success', True)
        time_spent = workflow_data.get('time_spent', 0.0)
        context = workflow_data.get('context', {})
        
        # Create or update workflow pattern
        if workflow_id in self.workflow_patterns:
            existing = self.workflow_patterns[workflow_id]
            existing.frequency += 1
            existing.success_rate = (existing.success_rate * existing.frequency + (1.0 if success else 0.0)) / (existing.frequency + 1)
            existing.time_spent = (existing.time_spent + time_spent) / 2
            existing.updated_at = time.time()
            return existing
        else:
            new_pattern = WorkflowPattern(
                pattern_type=workflow_type,
                sequence=sequence,
                frequency=1,
                success_rate=1.0 if success else 0.0,
                time_spent=time_spent,
                context=context,
                created_at=time.time(),
                updated_at=time.time()
            )
            self.workflow_patterns[workflow_id] = new_pattern
            return new_pattern
    
    def learn_architectural_decisions(self, decision_data: Dict[str, Any]) -> DecisionPattern:
        """Learn from architectural decisions and choices"""
        decision_type = decision_data.get('type', 'unknown')
        decision_id = f"decision_{decision_type}_{int(time.time())}"
        
        # Extract decision information
        choice = decision_data.get('choice', '')
        reasoning = decision_data.get('reasoning', '')
        alternatives = decision_data.get('alternatives', [])
        success = decision_data.get('success', True)
        context = decision_data.get('context', {})
        
        # Create or update decision pattern
        if decision_id in self.decision_patterns:
            existing = self.decision_patterns[decision_id]
            existing.frequency += 1
            existing.success_rate = (existing.success_rate * existing.frequency + (1.0 if success else 0.0)) / (existing.frequency + 1)
            existing.updated_at = time.time()
            return existing
        else:
            new_pattern = DecisionPattern(
                decision_type=decision_type,
                choice=choice,
                reasoning=reasoning,
                alternatives=alternatives,
                frequency=1,
                success_rate=1.0 if success else 0.0,
                context=context,
                created_at=time.time(),
                updated_at=time.time()
            )
            self.decision_patterns[decision_id] = new_pattern
            return new_pattern
    
    def learn_learning_patterns(self, learning_data: Dict[str, Any]) -> LearningPattern:
        """Learn how you approach learning and adaptation"""
        learning_type = learning_data.get('type', 'unknown')
        learning_id = f"learning_{learning_type}_{int(time.time())}"
        
        # Extract learning information
        approach = learning_data.get('approach', '')
        effectiveness = learning_data.get('effectiveness', 0.5)
        time_to_mastery = learning_data.get('time_to_mastery', 0.0)
        resources = learning_data.get('resources', [])
        context = learning_data.get('context', {})
        
        # Create or update learning pattern
        if learning_id in self.learning_patterns:
            existing = self.learning_patterns[learning_id]
            existing.effectiveness = (existing.effectiveness + effectiveness) / 2
            existing.time_to_mastery = (existing.time_to_mastery + time_to_mastery) / 2
            existing.updated_at = time.time()
            return existing
        else:
            new_pattern = LearningPattern(
                learning_type=learning_type,
                approach=approach,
                effectiveness=effectiveness,
                time_to_mastery=time_to_mastery,
                resources_used=resources,
                context=context,
                created_at=time.time(),
                updated_at=time.time()
            )
            self.learning_patterns[learning_id] = new_pattern
            return new_pattern
    
    def predict_context_needs(self, current_context: Dict[str, Any]) -> List[ContextSuggestion]:
        """Predict what context you'll need based on learned patterns"""
        suggestions = []
        
        # Analyze current context
        current_file = current_context.get('file', '')
        current_language = current_context.get('language', '')
        current_task = current_context.get('task', '')
        recent_work = current_context.get('recent_work', [])
        
        # Generate suggestions based on style patterns
        style_suggestions = self._generate_style_suggestions(current_context)
        suggestions.extend(style_suggestions)
        
        # Generate suggestions based on workflow patterns
        workflow_suggestions = self._generate_workflow_suggestions(current_context)
        suggestions.extend(workflow_suggestions)
        
        # Generate suggestions based on decision patterns
        decision_suggestions = self._generate_decision_suggestions(current_context)
        suggestions.extend(decision_suggestions)
        
        # Generate suggestions based on learning patterns
        learning_suggestions = self._generate_learning_suggestions(current_context)
        suggestions.extend(learning_suggestions)
        
        # Sort by relevance and confidence
        suggestions.sort(key=lambda x: (x.relevance_score, x.confidence), reverse=True)
        
        return suggestions[:5]  # Return top 5 suggestions
    
    def _generate_style_suggestions(self, context: Dict[str, Any]) -> List[ContextSuggestion]:
        """Generate style-based context suggestions"""
        suggestions = []
        current_language = context.get('language', '')
        
        # Find relevant style patterns
        for pattern_id, pattern in self.style_patterns.items():
            if pattern.pattern_type == 'naming':
                # Suggest naming conventions
                if pattern.frequency > 2:  # Only suggest if pattern is well-established
                    suggestion = ContextSuggestion(
                        suggestion_type='proactive',
                        content=f"Consider using {pattern.pattern} naming convention (used {pattern.frequency} times in your codebase)",
                        relevance_score=0.8,
                        confidence=pattern.confidence,
                        source_pattern=f"naming_{pattern.pattern}",
                        context={'language': current_language, 'pattern_type': 'naming'},
                        created_at=time.time()
                    )
                    suggestions.append(suggestion)
        
        return suggestions
    
    def _generate_workflow_suggestions(self, context: Dict[str, Any]) -> List[ContextSuggestion]:
        """Generate workflow-based context suggestions"""
        suggestions = []
        current_task = context.get('task', '')
        
        # Find relevant workflow patterns
        for pattern_id, pattern in self.workflow_patterns.items():
            if pattern.pattern_type in current_task.lower():
                # Suggest workflow improvements
                if pattern.success_rate > 0.7:  # Only suggest successful patterns
                    suggestion = ContextSuggestion(
                        suggestion_type='proactive',
                        content=f"Your {pattern.pattern_type} workflow has {pattern.success_rate:.1%} success rate. Consider following: {' → '.join(pattern.sequence)}",
                        relevance_score=0.9,
                        confidence=pattern.success_rate,
                        source_pattern=f"workflow_{pattern.pattern_type}",
                        context={'task': current_task, 'pattern_type': 'workflow'},
                        created_at=time.time()
                    )
                    suggestions.append(suggestion)
        
        return suggestions
    
    def _generate_decision_suggestions(self, context: Dict[str, Any]) -> List[ContextSuggestion]:
        """Generate decision-based context suggestions"""
        suggestions = []
        current_language = context.get('language', '')
        
        # Find relevant decision patterns
        for pattern_id, pattern in self.decision_patterns.items():
            if pattern.decision_type in ['architecture', 'library']:
                # Suggest architectural decisions
                if pattern.success_rate > 0.8:  # Only suggest very successful decisions
                    suggestion = ContextSuggestion(
                        suggestion_type='proactive',
                        content=f"Previous {pattern.decision_type} decision: {pattern.choice} (success rate: {pattern.success_rate:.1%})",
                        relevance_score=0.85,
                        confidence=pattern.success_rate,
                        source_pattern=f"decision_{pattern.decision_type}",
                        context={'language': current_language, 'pattern_type': 'decision'},
                        created_at=time.time()
                    )
                    suggestions.append(suggestion)
        
        return suggestions
    
    def _generate_learning_suggestions(self, context: Dict[str, Any]) -> List[ContextSuggestion]:
        """Generate learning-based context suggestions"""
        suggestions = []
        current_task = context.get('task', '')
        
        # Find relevant learning patterns
        for pattern_id, pattern in self.learning_patterns.items():
            if pattern.learning_type in current_task.lower():
                # Suggest learning approaches
                if pattern.effectiveness > 0.7:  # Only suggest effective approaches
                    suggestion = ContextSuggestion(
                        suggestion_type='proactive',
                        content=f"Your effective {pattern.learning_type} approach: {pattern.approach} (effectiveness: {pattern.effectiveness:.1%})",
                        relevance_score=0.8,
                        confidence=pattern.effectiveness,
                        source_pattern=f"learning_{pattern.learning_type}",
                        context={'task': current_task, 'pattern_type': 'learning'},
                        created_at=time.time()
                    )
                    suggestions.append(suggestion)
        
        return suggestions
    
    def get_personalization_summary(self) -> Dict[str, Any]:
        """Get a summary of learned personalization patterns"""
        return {
            'style_patterns': {
                'total': len(self.style_patterns),
                'by_type': self._count_patterns_by_type(self.style_patterns),
                'top_patterns': self._get_top_patterns(self.style_patterns, 5)
            },
            'workflow_patterns': {
                'total': len(self.workflow_patterns),
                'by_type': self._count_patterns_by_type(self.workflow_patterns),
                'top_patterns': self._get_top_patterns(self.workflow_patterns, 5)
            },
            'decision_patterns': {
                'total': len(self.decision_patterns),
                'by_type': self._count_patterns_by_type(self.decision_patterns),
                'top_patterns': self._get_top_patterns(self.decision_patterns, 5)
            },
            'learning_patterns': {
                'total': len(self.learning_patterns),
                'by_type': self._count_patterns_by_type(self.learning_patterns),
                'top_patterns': self._get_top_patterns(self.learning_patterns, 5)
            }
        }
    
    def _count_patterns_by_type(self, patterns: Dict[str, Any]) -> Dict[str, int]:
        """Count patterns by type"""
        counts = defaultdict(int)
        for pattern in patterns.values():
            # Handle different pattern types with different attribute names
            if hasattr(pattern, 'pattern_type'):
                counts[pattern.pattern_type] += 1
            elif hasattr(pattern, 'decision_type'):
                counts[pattern.decision_type] += 1
            elif hasattr(pattern, 'learning_type'):
                counts[pattern.learning_type] += 1
        return dict(counts)
    
    def _get_top_patterns(self, patterns: Dict[str, Any], limit: int) -> List[Dict[str, Any]]:
        """Get top patterns by frequency or success rate"""
        sorted_patterns = sorted(
            patterns.values(),
            key=lambda x: getattr(x, 'frequency', 0) + getattr(x, 'success_rate', 0),
            reverse=True
        )
        
        top_patterns = []
        for pattern in sorted_patterns[:limit]:
            pattern_dict = asdict(pattern)
            pattern_dict['id'] = next(k for k, v in patterns.items() if v == pattern)
            top_patterns.append(pattern_dict)
        
        return top_patterns
    
    def export_patterns(self, format: str = 'json') -> str:
        """Export learned patterns in various formats"""
        if format == 'json':
            return json.dumps(self.get_personalization_summary(), indent=2, default=str)
        elif format == 'summary':
            return self._generate_summary()
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _generate_summary(self) -> str:
        """Generate a human-readable summary of learned patterns"""
        summary = self.get_personalization_summary()
        
        report = f"""
# Personalization Patterns Summary

## 🎨 Style Patterns: {summary['style_patterns']['total']}
"""
        
        for pattern_type, count in summary['style_patterns']['by_type'].items():
            report += f"- **{pattern_type}**: {count} patterns\n"
        
        report += f"""
## 🔄 Workflow Patterns: {summary['workflow_patterns']['total']}
"""
        
        for pattern_type, count in summary['workflow_patterns']['by_type'].items():
            report += f"- **{pattern_type}**: {count} patterns\n"
        
        report += f"""
## 🏗️ Decision Patterns: {summary['decision_patterns']['total']}
"""
        
        for pattern_type, count in summary['decision_patterns']['by_type'].items():
            report += f"- **{pattern_type}**: {count} patterns\n"
        
        report += f"""
## 📚 Learning Patterns: {summary['learning_patterns']['total']}
"""
        
        for pattern_type, count in summary['learning_patterns']['by_type'].items():
            report += f"- **{pattern_type}**: {count} patterns\n"
        
        return report

class BehaviorInjectionEngine:
    """Injects learned behaviors and preferences into context"""
    
    def __init__(self, preference_engine: PreferenceLearningEngine):
        self.preference_engine = preference_engine
        self.injection_history: List[Dict[str, Any]] = []
        
        # Injection strategies
        self.injection_strategies = {
            'proactive': self._proactive_injection,
            'reactive': self._reactive_injection,
            'predictive': self._predictive_injection
        }
    
    def inject_context(self, current_context: Dict[str, Any], strategy: str = 'proactive') -> List[ContextSuggestion]:
        """Inject relevant context based on learned patterns"""
        if strategy in self.injection_strategies:
            suggestions = self.injection_strategies[strategy](current_context)
        else:
            suggestions = self._proactive_injection(current_context)
        
        # Record injection
        self._record_injection(current_context, suggestions, strategy)
        
        return suggestions
    
    def _proactive_injection(self, context: Dict[str, Any]) -> List[ContextSuggestion]:
        """Proactively inject context before you ask"""
        return self.preference_engine.predict_context_needs(context)
    
    def _reactive_injection(self, context: Dict[str, Any]) -> List[ContextSuggestion]:
        """Reactively inject context based on current situation"""
        suggestions = []
        
        # Analyze current context for immediate needs
        current_file = context.get('file', '')
        current_language = context.get('language', '')
        
        # Find relevant patterns for immediate context
        for pattern_id, pattern in self.preference_engine.style_patterns.items():
            if pattern.source_files and any(current_file in source for source in pattern.source_files):
                suggestion = ContextSuggestion(
                    suggestion_type='reactive',
                    content=f"Style pattern detected: {pattern.pattern} (used {pattern.frequency} times)",
                    relevance_score=0.9,
                    confidence=pattern.confidence,
                    source_pattern=pattern_id,
                    context={'file': current_file, 'language': current_language},
                    created_at=time.time()
                )
                suggestions.append(suggestion)
        
        return suggestions
    
    def _predictive_injection(self, context: Dict[str, Any]) -> List[ContextSuggestion]:
        """Predictively inject context based on learned patterns"""
        suggestions = []
        
        # Analyze recent work patterns
        recent_work = context.get('recent_work', [])
        if len(recent_work) >= 3:
            # Look for patterns in recent work
            recent_patterns = self._analyze_recent_patterns(recent_work)
            
            for pattern_type, pattern_info in recent_patterns.items():
                suggestion = ContextSuggestion(
                    suggestion_type='predictive',
                    content=f"Based on recent work, you might need: {pattern_info['suggestion']}",
                    relevance_score=0.8,
                    confidence=pattern_info['confidence'],
                    source_pattern=f"recent_{pattern_type}",
                    context={'recent_work': recent_work},
                    created_at=time.time()
                )
                suggestions.append(suggestion)
        
        return suggestions
    
    def _analyze_recent_patterns(self, recent_work: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """Analyze patterns in recent work"""
        patterns = {}
        
        # Analyze file types
        file_types = [work.get('file_type', 'unknown') for work in recent_work]
        if len(set(file_types)) == 1:
            patterns['file_type'] = {
                'suggestion': f"Continue working with {file_types[0]} files",
                'confidence': 0.8
            }
        
        # Analyze languages
        languages = [work.get('language', 'unknown') for work in recent_work]
        if len(set(languages)) == 1:
            patterns['language'] = {
                'suggestion': f"Focus on {languages[0]} development",
                'confidence': 0.8
            }
        
        return patterns
    
    def _record_injection(self, context: Dict[str, Any], suggestions: List[ContextSuggestion], strategy: str):
        """Record context injection for analysis"""
        injection_record = {
            'timestamp': time.time(),
            'strategy': strategy,
            'context': context,
            'suggestions_count': len(suggestions),
            'suggestions': [asdict(s) for s in suggestions]
        }
        
        self.injection_history.append(injection_record)
        
        # Keep only last 100 injections
        if len(self.injection_history) > 100:
            self.injection_history = self.injection_history[-100:]
    
    def get_injection_stats(self) -> Dict[str, Any]:
        """Get statistics about context injection"""
        if not self.injection_history:
            return {'total_injections': 0}
        
        total_injections = len(self.injection_history)
        strategy_counts = defaultdict(int)
        suggestion_counts = []
        
        for injection in self.injection_history:
            strategy_counts[injection['strategy']] += 1
            suggestion_counts.append(injection['suggestions_count'])
        
        return {
            'total_injections': total_injections,
            'strategy_distribution': dict(strategy_counts),
            'average_suggestions': sum(suggestion_counts) / len(suggestion_counts) if suggestion_counts else 0,
            'recent_injections': len([i for i in self.injection_history if time.time() - i['timestamp'] < 3600])  # Last hour
        }

class PersonalizationEngine:
    """Main engine for personalization and behavior injection"""
    
    def __init__(self):
        self.preference_engine = PreferenceLearningEngine()
        self.behavior_engine = BehaviorInjectionEngine(self.preference_engine)
        self.learning_history: List[Dict[str, Any]] = []
    
    def learn_from_development_session(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Learn from a complete development session"""
        session_id = f"session_{int(time.time())}"
        learned_patterns = {}
        
        # Extract code samples
        code_samples = session_data.get('code_samples', [])
        for sample in code_samples:
            file_path = sample.get('file_path', '')
            code = sample.get('code', '')
            
            if code and file_path:
                style_patterns = self.preference_engine.learn_from_code(code, file_path)
                learned_patterns['style'] = learned_patterns.get('style', []) + style_patterns
        
        # Extract workflow data
        workflow_data = session_data.get('workflow', {})
        if workflow_data:
            workflow_pattern = self.preference_engine.learn_from_workflow(workflow_data)
            learned_patterns['workflow'] = [workflow_pattern]
        
        # Extract decision data
        decisions = session_data.get('decisions', [])
        for decision in decisions:
            decision_pattern = self.preference_engine.learn_architectural_decisions(decision)
            learned_patterns['decisions'] = learned_patterns.get('decisions', []) + [decision_pattern]
        
        # Extract learning data
        learning_data = session_data.get('learning', {})
        if learning_data:
            learning_pattern = self.preference_engine.learn_learning_patterns(learning_data)
            learned_patterns['learning'] = [learning_pattern]
        
        # Record learning session
        self._record_learning_session(session_id, session_data, learned_patterns)
        
        return learned_patterns
    
    def _record_learning_session(self, session_id: str, session_data: Dict[str, Any], learned_patterns: Dict[str, Any]):
        """Record a learning session for analysis"""
        session_record = {
            'session_id': session_id,
            'timestamp': time.time(),
            'session_data': session_data,
            'learned_patterns': learned_patterns,
            'total_patterns': sum(len(patterns) for patterns in learned_patterns.values())
        }
        
        self.learning_history.append(session_record)
        
        # Keep only last 50 sessions
        if len(self.learning_history) > 50:
            self.learning_history = self.learning_history[-50:]
    
    def get_context_suggestions(self, current_context: Dict[str, Any], strategy: str = 'proactive') -> List[ContextSuggestion]:
        """Get context suggestions based on learned patterns"""
        return self.behavior_engine.inject_context(current_context, strategy)
    
    def get_personalization_summary(self) -> Dict[str, Any]:
        """Get comprehensive personalization summary"""
        return {
            'preferences': self.preference_engine.get_personalization_summary(),
            'behavior_injection': self.behavior_engine.get_injection_stats(),
            'learning_history': {
                'total_sessions': len(self.learning_history),
                'recent_sessions': len([s for s in self.learning_history if time.time() - s['timestamp'] < 86400])  # Last 24 hours
            }
        }
    
    def export_personalization(self, format: str = 'json') -> str:
        """Export personalization data in various formats"""
        if format == 'json':
            return json.dumps(self.get_personalization_summary(), indent=2, default=str)
        elif format == 'summary':
            return self._generate_summary()
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _generate_summary(self) -> str:
        """Generate a human-readable summary of personalization"""
        summary = self.get_personalization_summary()
        
        report = f"""
# Personalization & Behavior Injection Summary

## 🎨 Learned Preferences
- **Style Patterns**: {summary['preferences']['style_patterns']['total']}
- **Workflow Patterns**: {summary['preferences']['workflow_patterns']['total']}
- **Decision Patterns**: {summary['preferences']['decision_patterns']['total']}
- **Learning Patterns**: {summary['preferences']['learning_patterns']['total']}

## 🔄 Behavior Injection
- **Total Injections**: {summary['behavior_injection']['total_injections']}
- **Average Suggestions**: {summary['behavior_injection']['average_suggestions']:.1f}
- **Recent Injections**: {summary['behavior_injection']['recent_injections']}

## 📚 Learning History
- **Total Sessions**: {summary['learning_history']['total_sessions']}
- **Recent Sessions**: {summary['learning_history']['recent_sessions']}
"""
        
        return report

def main():
    """Main function for testing the personalization engine"""
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python personalization_engine.py <project_root>")
        sys.exit(1)
    
    project_root = sys.argv[1]
    
    if not os.path.exists(project_root):
        print(f"Error: Project root '{project_root}' does not exist")
        sys.exit(1)
    
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Create personalization engine
    engine = PersonalizationEngine()
    
    try:
        print(f"🧠 Starting personalization learning: {project_root}")
        
        # Simulate learning from development session
        sample_session = {
            'code_samples': [
                {
                    'file_path': 'sample.py',
                    'code': '''
def calculate_total(items):
    """Calculate total price of items"""
    total = 0
    for item in items:
        total += item.price
    return total

class ShoppingCart:
    def __init__(self):
        self.items = []
    
    def add_item(self, item):
        self.items.append(item)
'''
                }
            ],
            'workflow': {
                'type': 'feature_development',
                'sequence': ['plan', 'code', 'test', 'refactor'],
                'success': True,
                'time_spent': 120.0,
                'context': {'language': 'python', 'complexity': 'medium'}
            },
            'decisions': [
                {
                    'type': 'architecture',
                    'choice': 'class-based design',
                    'reasoning': 'Better encapsulation and maintainability',
                    'alternatives': ['functional', 'procedural'],
                    'success': True,
                    'context': {'language': 'python', 'domain': 'e-commerce'}
                }
            ],
            'learning': {
                'type': 'new_pattern',
                'approach': 'tutorial + practice',
                'effectiveness': 0.9,
                'time_to_mastery': 60.0,
                'resources': ['docs.python.org', 'stackoverflow'],
                'context': {'topic': 'python_classes', 'difficulty': 'beginner'}
            }
        }
        
        # Learn from session
        learned_patterns = engine.learn_from_development_session(sample_session)
        
        print(f"✅ Learned {sum(len(patterns) for patterns in learned_patterns.values())} patterns")
        
        # Get context suggestions
        current_context = {
            'file': 'new_feature.py',
            'language': 'python',
            'task': 'feature_development',
            'recent_work': [
                {'file_type': 'python', 'language': 'python', 'task': 'class_implementation'},
                {'file_type': 'python', 'language': 'python', 'task': 'method_creation'},
                {'file_type': 'python', 'language': 'python', 'task': 'testing'}
            ]
        }
        
        suggestions = engine.get_context_suggestions(current_context, 'proactive')
        print(f"🔍 Generated {len(suggestions)} context suggestions")
        
        # Export results
        print("\n📊 Personalization Summary:")
        print(engine.export_personalization('summary'))
        
        # Save detailed data
        output_file = f"personalization_data_{int(time.time())}.json"
        with open(output_file, 'w') as f:
            f.write(engine.export_personalization('json'))
        print(f"\n💾 Detailed personalization data saved to: {output_file}")
        
    except Exception as e:
        print(f"❌ Error during personalization learning: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
