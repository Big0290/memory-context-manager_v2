#!/usr/bin/env python3
"""
Context Orchestrator - Phase 4 of Memory Context Manager v2
Intelligently orchestrates all context sources and provides seamless integration
"""

import os
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import logging
from collections import defaultdict
import asyncio
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

@dataclass
class ContextSource:
    """A source of context information"""
    source_id: str
    source_type: str  # 'project', 'knowledge', 'personal', 'external'
    name: str
    description: str
    priority: float  # 0.0 to 1.0
    freshness: float  # Last update timestamp
    reliability: float  # 0.0 to 1.0
    metadata: Dict[str, Any]

@dataclass
class ContextRequest:
    """A request for context information"""
    request_id: str
    user_id: str
    context_type: str  # 'immediate', 'comprehensive', 'predictive'
    scope: str  # 'file', 'module', 'project', 'global'
    filters: Dict[str, Any]
    priority: float
    created_at: float
    deadline: Optional[float] = None

@dataclass
class ContextResponse:
    """A response with orchestrated context"""
    response_id: str
    request_id: str
    context_sources: List[str]
    context_data: Dict[str, Any]
    relevance_score: float
    confidence: float
    freshness: float
    orchestration_time: float
    metadata: Dict[str, Any]

@dataclass
class OrchestrationStrategy:
    """Strategy for orchestrating context sources"""
    strategy_id: str
    name: str
    description: str
    source_priorities: Dict[str, float]
    combination_rules: Dict[str, Any]
    quality_thresholds: Dict[str, float]
    performance_targets: Dict[str, float]

class ContextSourceManager:
    """Manages and tracks all available context sources"""
    
    def __init__(self):
        self.sources: Dict[str, ContextSource] = {}
        self.source_health: Dict[str, Dict[str, Any]] = {}
        self.performance_metrics: Dict[str, List[float]] = defaultdict(list)
    
    def register_source(self, source: ContextSource) -> bool:
        """Register a new context source"""
        try:
            self.sources[source.source_id] = source
            self.source_health[source.source_id] = {
                'status': 'active',
                'last_check': time.time(),
                'response_time': 0.0,
                'error_count': 0,
                'success_count': 0
            }
            logger.info(f"✅ Registered context source: {source.name} ({source.source_type})")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to register source {source.source_id}: {str(e)}")
            return False
    
    def update_source_health(self, source_id: str, health_data: Dict[str, Any]):
        """Update health information for a source"""
        if source_id in self.source_health:
            self.source_health[source_id].update(health_data)
            self.source_health[source_id]['last_check'] = time.time()
    
    def get_available_sources(self, context_type: str = None) -> List[ContextSource]:
        """Get available context sources, optionally filtered by type"""
        available_sources = []
        
        for source_id, source in self.sources.items():
            health = self.source_health.get(source_id, {})
            
            # Check if source is healthy
            if health.get('status') == 'active' and health.get('error_count', 0) < 5:
                if context_type is None or source.source_type == context_type:
                    available_sources.append(source)
        
        # Sort by priority and reliability
        available_sources.sort(key=lambda x: (x.priority, x.reliability), reverse=True)
        
        return available_sources
    
    def get_source_performance(self, source_id: str) -> Dict[str, Any]:
        """Get performance metrics for a specific source"""
        if source_id not in self.sources:
            return {}
        
        health = self.source_health.get(source_id, {})
        metrics = self.performance_metrics.get(source_id, [])
        
        return {
            'source': asdict(self.sources[source_id]),
            'health': health,
            'performance': {
                'average_response_time': sum(metrics) / len(metrics) if metrics else 0.0,
                'total_requests': len(metrics),
                'success_rate': health.get('success_count', 0) / max(health.get('success_count', 0) + health.get('error_count', 0), 1)
            }
        }

class ContextOrchestrator:
    """Main orchestrator for combining and providing context"""
    
    def __init__(self):
        self.source_manager = ContextSourceManager()
        self.orchestration_strategies: Dict[str, OrchestrationStrategy] = {}
        self.request_history: List[ContextRequest] = []
        self.response_cache: Dict[str, ContextResponse] = {}
        
        # Initialize default strategies
        self._initialize_default_strategies()
        
        # Performance tracking
        self.total_requests = 0
        self.successful_requests = 0
        self.average_response_time = 0.0
    
    def _initialize_default_strategies(self):
        """Initialize default orchestration strategies"""
        
        # Strategy 1: Immediate Context (Fast, focused)
        immediate_strategy = OrchestrationStrategy(
            strategy_id='immediate',
            name='Immediate Context',
            description='Fast context retrieval for immediate needs',
            source_priorities={
                'personal': 0.9,
                'project': 0.8,
                'knowledge': 0.6,
                'external': 0.3
            },
            combination_rules={
                'max_sources': 3,
                'timeout': 0.5,
                'quality_threshold': 0.7
            },
            quality_thresholds={
                'relevance': 0.8,
                'confidence': 0.7,
                'freshness': 0.6
            },
            performance_targets={
                'response_time': 0.5,
                'accuracy': 0.8
            }
        )
        
        # Strategy 2: Comprehensive Context (Thorough, complete)
        comprehensive_strategy = OrchestrationStrategy(
            strategy_id='comprehensive',
            name='Comprehensive Context',
            description='Complete context gathering for complex needs',
            source_priorities={
                'knowledge': 0.9,
                'project': 0.8,
                'personal': 0.7,
                'external': 0.5
            },
            combination_rules={
                'max_sources': 10,
                'timeout': 2.0,
                'quality_threshold': 0.9
            },
            quality_thresholds={
                'relevance': 0.9,
                'confidence': 0.8,
                'freshness': 0.7
            },
            performance_targets={
                'response_time': 2.0,
                'accuracy': 0.95
            }
        )
        
        # Strategy 3: Predictive Context (Anticipatory, proactive)
        predictive_strategy = OrchestrationStrategy(
            strategy_id='predictive',
            name='Predictive Context',
            description='Anticipatory context for future needs',
            source_priorities={
                'personal': 0.9,
                'knowledge': 0.8,
                'project': 0.7,
                'external': 0.6
            },
            combination_rules={
                'max_sources': 5,
                'timeout': 1.0,
                'quality_threshold': 0.8
            },
            quality_thresholds={
                'relevance': 0.8,
                'confidence': 0.7,
                'freshness': 0.8
            },
            performance_targets={
                'response_time': 1.0,
                'accuracy': 0.85
            }
        )
        
        self.orchestration_strategies = {
            'immediate': immediate_strategy,
            'comprehensive': comprehensive_strategy,
            'predictive': predictive_strategy
        }
    
    def register_context_source(self, source: ContextSource) -> bool:
        """Register a new context source"""
        return self.source_manager.register_source(source)
    
    def orchestrate_context(self, request: ContextRequest) -> ContextResponse:
        """Orchestrate context based on the request"""
        start_time = time.time()
        
        try:
            # Determine strategy based on request
            strategy = self._select_strategy(request)
            
            # Get available sources
            available_sources = self.source_manager.get_available_sources()
            
            # Filter and prioritize sources
            selected_sources = self._select_sources(request, strategy, available_sources)
            
            # Gather context from selected sources
            context_data = self._gather_context(request, selected_sources, strategy)
            
            # Combine and optimize context
            orchestrated_context = self._combine_context(context_data, strategy)
            
            # Calculate quality metrics
            relevance_score = self._calculate_relevance(request, orchestrated_context)
            confidence = self._calculate_confidence(orchestrated_context)
            freshness = self._calculate_freshness(orchestrated_context)
            
            # Create response
            response = ContextResponse(
                response_id=f"resp_{int(time.time())}",
                request_id=request.request_id,
                context_sources=[s.source_id for s in selected_sources],
                context_data=orchestrated_context,
                relevance_score=relevance_score,
                confidence=confidence,
                freshness=freshness,
                orchestration_time=time.time() - start_time,
                metadata={
                    'strategy_used': strategy.strategy_id,
                    'sources_used': len(selected_sources),
                    'quality_metrics': {
                        'relevance': relevance_score,
                        'confidence': confidence,
                        'freshness': freshness
                    }
                }
            )
            
            # Cache response
            self._cache_response(response)
            
            # Update performance metrics
            self._update_performance_metrics(response)
            
            # Record request
            self._record_request(request, response)
            
            logger.info(f"✅ Context orchestrated successfully: {len(selected_sources)} sources, {response.orchestration_time:.3f}s")
            
            return response
            
        except Exception as e:
            logger.error(f"❌ Context orchestration failed: {str(e)}")
            # Return fallback response
            return self._create_fallback_response(request, str(e))
    
    def _select_strategy(self, request: ContextRequest) -> OrchestrationStrategy:
        """Select the appropriate orchestration strategy"""
        if request.context_type == 'immediate':
            return self.orchestration_strategies['immediate']
        elif request.context_type == 'comprehensive':
            return self.orchestration_strategies['comprehensive']
        elif request.context_type == 'predictive':
            return self.orchestration_strategies['predictive']
        else:
            # Default to immediate for unknown types
            return self.orchestration_strategies['immediate']
    
    def _select_sources(self, request: ContextRequest, strategy: OrchestrationStrategy, available_sources: List[ContextSource]) -> List[ContextSource]:
        """Select the best sources for the request"""
        # Filter sources by priority and reliability
        filtered_sources = []
        
        for source in available_sources:
            priority = strategy.source_priorities.get(source.source_type, 0.5)
            combined_score = (priority * 0.6) + (source.reliability * 0.4)
            
            if combined_score >= strategy.combination_rules.get('quality_threshold', 0.7):
                filtered_sources.append((source, combined_score))
        
        # Sort by combined score
        filtered_sources.sort(key=lambda x: x[1], reverse=True)
        
        # Limit by max sources
        max_sources = strategy.combination_rules.get('max_sources', 5)
        selected_sources = [source for source, score in filtered_sources[:max_sources]]
        
        return selected_sources
    
    def _gather_context(self, request: ContextRequest, sources: List[ContextSource], strategy: OrchestrationStrategy) -> Dict[str, Any]:
        """Gather context from selected sources"""
        context_data = {}
        
        # Use ThreadPoolExecutor for parallel context gathering
        with ThreadPoolExecutor(max_workers=min(len(sources), 5)) as executor:
            future_to_source = {
                executor.submit(self._gather_from_source, source, request): source
                for source in sources
            }
            
            for future in future_to_source:
                try:
                    source = future_to_source[future]
                    source_context = future.result(timeout=strategy.combination_rules.get('timeout', 1.0))
                    
                    if source_context:
                        context_data[source.source_id] = {
                            'source': asdict(source),
                            'context': source_context,
                            'timestamp': time.time()
                        }
                        
                        # Update source health
                        self.source_manager.update_source_health(source.source_id, {
                            'success_count': self.source_manager.source_health[source.source_id].get('success_count', 0) + 1,
                            'response_time': time.time() - source.freshness
                        })
                    
                except Exception as e:
                    source = future_to_source[future]
                    logger.warning(f"⚠️ Failed to gather context from {source.source_id}: {str(e)}")
                    
                    # Update source health
                    self.source_manager.update_source_health(source.source_id, {
                        'error_count': self.source_manager.source_health[source.source_id].get('error_count', 0) + 1
                    })
        
        return context_data
    
    def _gather_from_source(self, source: ContextSource, request: ContextRequest) -> Optional[Dict[str, Any]]:
        """Gather context from a specific source"""
        # This is a placeholder - in real implementation, this would call the actual source
        # For now, we'll simulate context gathering
        
        if source.source_type == 'project':
            return {
                'file_structure': {'total_files': 100, 'languages': ['python', 'javascript']},
                'dependencies': ['flask', 'pytest', 'requests'],
                'architecture': 'modular'
            }
        elif source.source_type == 'knowledge':
            return {
                'concepts': ['context_orchestration', 'intelligent_routing'],
                'relationships': 150,
                'patterns': ['orchestration', 'integration']
            }
        elif source.source_type == 'personal':
            return {
                'preferences': ['python', 'modular_architecture'],
                'workflow_patterns': ['test_driven', 'iterative'],
                'learning_style': 'hands_on'
            }
        elif source.source_type == 'external':
            return {
                'documentation': ['api_docs', 'tutorials'],
                'community': ['stack_overflow', 'github'],
                'standards': ['pep8', 'rest_api']
            }
        else:
            return None
    
    def _combine_context(self, context_data: Dict[str, Any], strategy: OrchestrationStrategy) -> Dict[str, Any]:
        """Combine context from multiple sources"""
        combined_context = {
            'summary': {},
            'details': {},
            'relationships': {},
            'recommendations': []
        }
        
        # Combine summary information
        for source_id, data in context_data.items():
            source_type = data['source']['source_type']
            
            if source_type not in combined_context['summary']:
                combined_context['summary'][source_type] = {}
            
            # Merge context data
            for key, value in data['context'].items():
                if key in combined_context['summary'][source_type]:
                    if isinstance(value, list) and isinstance(combined_context['summary'][source_type][key], list):
                        combined_context['summary'][source_type][key].extend(value)
                    elif isinstance(value, dict) and isinstance(combined_context['summary'][source_type][key], dict):
                        combined_context['summary'][source_type][key].update(value)
                    else:
                        combined_context['summary'][source_type][key] = value
                else:
                    combined_context['summary'][source_type][key] = value
        
        # Generate recommendations based on combined context
        combined_context['recommendations'] = self._generate_recommendations(combined_context, strategy)
        
        return combined_context
    
    def _generate_recommendations(self, context: Dict[str, Any], strategy: OrchestrationStrategy) -> List[str]:
        """Generate intelligent recommendations based on combined context"""
        recommendations = []
        
        # Analyze project context
        if 'project' in context['summary']:
            project = context['summary']['project']
            
            if 'dependencies' in project and 'flask' in project['dependencies']:
                recommendations.append("Consider using Flask's built-in testing utilities for your web application")
            
            if 'architecture' in project and project['architecture'] == 'modular':
                recommendations.append("Your modular architecture supports easy testing and maintenance")
        
        # Analyze personal context
        if 'personal' in context['summary']:
            personal = context['summary']['personal']
            
            if 'workflow_patterns' in personal and 'test_driven' in personal['workflow_patterns']:
                recommendations.append("Your test-driven approach aligns well with the current project structure")
            
            if 'preferences' in personal and 'python' in personal['preferences']:
                recommendations.append("Python-first development approach detected - consider Python-specific best practices")
        
        # Analyze knowledge context
        if 'knowledge' in context['summary']:
            knowledge = context['summary']['knowledge']
            
            if 'concepts' in knowledge and 'context_orchestration' in knowledge['concepts']:
                recommendations.append("Context orchestration patterns detected - leverage for better integration")
        
        return recommendations[:5]  # Limit to top 5 recommendations
    
    def _calculate_relevance(self, request: ContextRequest, context: Dict[str, Any]) -> float:
        """Calculate relevance score for the context"""
        # Simple relevance calculation - in real implementation, this would be more sophisticated
        relevance_score = 0.8  # Base score
        
        # Adjust based on request scope
        if request.scope in ['file', 'module']:
            relevance_score += 0.1
        elif request.scope == 'project':
            relevance_score += 0.05
        
        # Adjust based on context type
        if request.context_type == 'immediate':
            relevance_score += 0.1
        
        return min(relevance_score, 1.0)
    
    def _calculate_confidence(self, context: Dict[str, Any]) -> float:
        """Calculate confidence score for the context"""
        # Simple confidence calculation
        confidence_score = 0.7  # Base score
        
        # Adjust based on number of sources
        if 'summary' in context:
            source_count = len(context['summary'])
            confidence_score += min(source_count * 0.05, 0.2)
        
        # Adjust based on recommendations
        if 'recommendations' in context and context['recommendations']:
            confidence_score += 0.1
        
        return min(confidence_score, 1.0)
    
    def _calculate_freshness(self, context: Dict[str, Any]) -> float:
        """Calculate freshness score for the context"""
        # Simple freshness calculation
        current_time = time.time()
        freshness_score = 0.8  # Base score
        
        # Adjust based on context age
        # In real implementation, this would check actual timestamps
        
        return min(freshness_score, 1.0)
    
    def _cache_response(self, response: ContextResponse):
        """Cache the response for future use"""
        cache_key = f"{response.request_id}_{response.context_sources}"
        self.response_cache[cache_key] = response
        
        # Limit cache size
        if len(self.response_cache) > 100:
            # Remove oldest entries
            oldest_keys = sorted(self.response_cache.keys(), 
                               key=lambda k: self.response_cache[k].created_at)[:20]
            for key in oldest_keys:
                del self.response_cache[key]
    
    def _update_performance_metrics(self, response: ContextResponse):
        """Update performance tracking metrics"""
        self.total_requests += 1
        self.successful_requests += 1
        
        # Update average response time
        self.average_response_time = (
            (self.average_response_time * (self.total_requests - 1) + response.orchestration_time) 
            / self.total_requests
        )
    
    def _record_request(self, request: ContextRequest, response: ContextResponse):
        """Record the request and response for analysis"""
        self.request_history.append({
            'request': asdict(request),
            'response': asdict(response),
            'timestamp': time.time()
        })
        
        # Limit history size
        if len(self.request_history) > 1000:
            self.request_history = self.request_history[-500:]
    
    def _create_fallback_response(self, request: ContextRequest, error: str) -> ContextResponse:
        """Create a fallback response when orchestration fails"""
        return ContextResponse(
            response_id=f"fallback_{int(time.time())}",
            request_id=request.request_id,
            context_sources=[],
            context_data={
                'error': error,
                'fallback': True,
                'message': 'Context orchestration failed, using fallback'
            },
            relevance_score=0.3,
            confidence=0.2,
            freshness=0.5,
            orchestration_time=0.0,
            metadata={'error': error, 'fallback': True}
        )
    
    def get_orchestration_stats(self) -> Dict[str, Any]:
        """Get comprehensive orchestration statistics"""
        return {
            'performance': {
                'total_requests': self.total_requests,
                'successful_requests': self.successful_requests,
                'success_rate': self.successful_requests / max(self.total_requests, 1),
                'average_response_time': self.average_response_time
            },
            'sources': {
                'total_sources': len(self.source_manager.sources),
                'active_sources': len([s for s in self.source_manager.get_available_sources()]),
                'source_health': self.source_manager.source_health
            },
            'cache': {
                'cached_responses': len(self.response_cache),
                'cache_hit_rate': 0.0  # Would calculate based on actual usage
            },
            'strategies': {
                'available_strategies': list(self.orchestration_strategies.keys()),
                'strategy_details': {
                    strategy_id: asdict(strategy) 
                    for strategy_id, strategy in self.orchestration_strategies.items()
                }
            }
        }
    
    def export_orchestration_data(self, format: str = 'json') -> str:
        """Export orchestration data in various formats"""
        if format == 'json':
            return json.dumps(self.get_orchestration_stats(), indent=2, default=str)
        elif format == 'summary':
            return self._generate_summary()
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _generate_summary(self) -> str:
        """Generate a human-readable summary of orchestration"""
        stats = self.get_orchestration_stats()
        
        summary = f"""
# Context Orchestration Summary

## 📊 Performance Metrics
- **Total Requests**: {stats['performance']['total_requests']}
- **Success Rate**: {stats['performance']['success_rate']:.1%}
- **Average Response Time**: {stats['performance']['average_response_time']:.3f}s

## 🔌 Context Sources
- **Total Sources**: {stats['sources']['total_sources']}
- **Active Sources**: {stats['sources']['active_sources']}

## 🎯 Orchestration Strategies
- **Available Strategies**: {', '.join(stats['strategies']['available_strategies'])}
- **Strategy Count**: {len(stats['strategies']['available_strategies'])}

## 💾 Cache & Storage
- **Cached Responses**: {stats['cache']['cached_responses']}
"""
        
        return summary

def main():
    """Main function for testing the context orchestrator"""
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python context_orchestrator.py <project_root>")
        sys.exit(1)
    
    project_root = sys.argv[1]
    
    if not os.path.exists(project_root):
        print(f"Error: Project root '{project_root}' does not exist")
        sys.exit(1)
    
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Create context orchestrator
    orchestrator = ContextOrchestrator()
    
    try:
        print(f"🧠 Starting context orchestration: {project_root}")
        
        # Register sample context sources
        sample_sources = [
            ContextSource(
                source_id='project_scanner',
                source_type='project',
                name='Project Scanner',
                description='Scans and analyzes project structure',
                priority=0.9,
                freshness=time.time(),
                reliability=0.95,
                metadata={'version': '1.0', 'capabilities': ['file_scanning', 'dependency_analysis']}
            ),
            ContextSource(
                source_id='knowledge_engine',
                source_type='knowledge',
                name='Knowledge Engine',
                description='Provides semantic knowledge and relationships',
                priority=0.8,
                freshness=time.time(),
                reliability=0.9,
                metadata={'version': '1.0', 'capabilities': ['concept_extraction', 'relationship_building']}
            ),
            ContextSource(
                source_id='personalization_engine',
                source_type='personal',
                name='Personalization Engine',
                description='Learns and provides personalized context',
                priority=0.85,
                freshness=time.time(),
                reliability=0.88,
                metadata={'version': '1.0', 'capabilities': ['pattern_learning', 'behavior_injection']}
            )
        ]
        
        for source in sample_sources:
            orchestrator.register_context_source(source)
        
        print(f"✅ Registered {len(sample_sources)} context sources")
        
        # Test different orchestration strategies
        test_requests = [
            ContextRequest(
                request_id='req_immediate',
                user_id='user1',
                context_type='immediate',
                scope='file',
                filters={'language': 'python'},
                priority=0.9,
                created_at=time.time()
            ),
            ContextRequest(
                request_id='req_comprehensive',
                user_id='user1',
                context_type='comprehensive',
                scope='project',
                filters={'include_external': True},
                priority=0.8,
                created_at=time.time()
            ),
            ContextRequest(
                request_id='req_predictive',
                user_id='user1',
                context_type='predictive',
                scope='module',
                filters={'task': 'development'},
                priority=0.7,
                created_at=time.time()
            )
        ]
        
        # Process requests
        for request in test_requests:
            print(f"\n🔍 Processing {request.context_type} request...")
            response = orchestrator.orchestrate_context(request)
            
            print(f"   ✅ Response generated in {response.orchestration_time:.3f}s")
            print(f"   📊 Relevance: {response.relevance_score:.2f}, Confidence: {response.confidence:.2f}")
            print(f"   🔌 Sources used: {len(response.context_sources)}")
            
            if 'recommendations' in response.context_data:
                print(f"   💡 Recommendations: {len(response.context_data['recommendations'])}")
        
        # Export results
        print("\n📊 Orchestration Summary:")
        print(orchestrator.export_orchestration_data('summary'))
        
        # Save detailed data
        output_file = f"context_orchestration_{int(time.time())}.json"
        with open(output_file, 'w') as f:
            f.write(orchestrator.export_orchestration_data('json'))
        print(f"\n💾 Detailed orchestration data saved to: {output_file}")
        
    except Exception as e:
        print(f"❌ Error during context orchestration: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
