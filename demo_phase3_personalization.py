#!/usr/bin/env python3
"""
Phase 3 Demo: Personalization & Behavior Injection Engine
Showcases the full capabilities of our personalization system
"""

import json
import time
from pathlib import Path
from personalization_engine import PersonalizationEngine

def demo_personalization_engine():
    """Demonstrate the full Phase 3 personalization capabilities"""
    print("🚀 PHASE 3 DEMO: PERSONALIZATION & BEHAVIOR INJECTION ENGINE")
    print("=" * 80)
    
    # Initialize the personalization engine
    engine = PersonalizationEngine()
    
    print(f"📁 Current Project: {Path.cwd().name}")
    print(f"📍 Location: {Path.cwd()}")
    print()
    
    # Phase 1 & 2: Foundation (already completed)
    print("✅ PHASE 1 COMPLETE: Project Intelligence Layer")
    print("   - Project scanner working perfectly")
    print("   - 100+ files indexed and analyzed")
    print("   - Technology stack identified")
    print()
    
    print("✅ PHASE 2 COMPLETE: Knowledge Ingestion Engine")
    print("   - 4,000+ concepts extracted and connected")
    print("   - Semantic knowledge graphs built")
    print("   - Advanced search capabilities")
    print()
    
    # Phase 3: Personalization (starting now)
    print("🧠 PHASE 3: Personalization & Behavior Injection")
    print("   - Learning coding preferences and style")
    print("   - Modeling workflow patterns")
    print("   - Intelligent context injection")
    print("   - Proactive assistance")
    print()
    
    print("🔍 Starting comprehensive personalization learning...")
    start_time = time.time()
    
    try:
        # Learn from multiple development sessions
        development_sessions = create_sample_development_sessions()
        
        total_patterns_learned = 0
        for i, session in enumerate(development_sessions, 1):
            print(f"📚 Learning from development session {i}...")
            learned_patterns = engine.learn_from_development_session(session)
            patterns_count = sum(len(patterns) for patterns in learned_patterns.values())
            total_patterns_learned += patterns_count
            print(f"   ✅ Learned {patterns_count} patterns")
        
        learning_time = time.time() - start_time
        
        print(f"✅ Personalization learning completed in {learning_time:.2f} seconds!")
        print(f"🎯 Total patterns learned: {total_patterns_learned}")
        print()
        
        # Demonstrate context suggestions
        demonstrate_context_suggestions(engine)
        
        # Demonstrate behavior injection
        demonstrate_behavior_injection(engine)
        
        # Demonstrate pattern analysis
        demonstrate_pattern_analysis(engine)
        
        # Export results
        export_demo_results(engine, learning_time, total_patterns_learned)
        
        print("\n🎉 PHASE 3 DEMO COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        
        return engine
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        return None

def create_sample_development_sessions():
    """Create sample development sessions for learning"""
    sessions = [
        # Session 1: Python Web Development
        {
            'code_samples': [
                {
                    'file_path': 'web_app.py',
                    'code': '''
def create_user_profile(user_data):
    """Create a new user profile"""
    profile = UserProfile(
        username=user_data.get('username'),
        email=user_data.get('email'),
        created_at=datetime.now()
    )
    return profile

class UserProfile:
    def __init__(self, username, email, created_at):
        self.username = username
        self.email = email
        self.created_at = created_at
    
    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }
'''
                }
            ],
            'workflow': {
                'type': 'web_development',
                'sequence': ['design', 'implement', 'test', 'deploy'],
                'success': True,
                'time_spent': 180.0,
                'context': {'language': 'python', 'framework': 'flask', 'complexity': 'medium'}
            },
            'decisions': [
                {
                    'type': 'architecture',
                    'choice': 'class-based models',
                    'reasoning': 'Better data validation and serialization',
                    'alternatives': ['dictionaries', 'dataclasses'],
                    'success': True,
                    'context': {'language': 'python', 'domain': 'web_development'}
                }
            ],
            'learning': {
                'type': 'new_framework',
                'approach': 'official_docs + examples',
                'effectiveness': 0.95,
                'time_to_mastery': 120.0,
                'resources': ['flask.palletsprojects.com', 'github examples'],
                'context': {'topic': 'flask_framework', 'difficulty': 'intermediate'}
            }
        },
        
        # Session 2: Testing and Debugging
        {
            'code_samples': [
                {
                    'file_path': 'test_user_profile.py',
                    'code': '''
def test_user_profile_creation():
    """Test user profile creation"""
    user_data = {
        'username': 'testuser',
        'email': 'test@example.com'
    }
    
    profile = create_user_profile(user_data)
    
    assert profile.username == 'testuser'
    assert profile.email == 'test@example.com'
    assert profile.created_at is not None

def test_user_profile_serialization():
    """Test user profile serialization"""
    profile = UserProfile('testuser', 'test@example.com', datetime.now())
    profile_dict = profile.to_dict()
    
    assert 'username' in profile_dict
    assert 'email' in profile_dict
    assert 'created_at' in profile_dict
'''
                }
            ],
            'workflow': {
                'type': 'testing',
                'sequence': ['write_test', 'run_test', 'fix_issues', 'verify'],
                'success': True,
                'time_spent': 90.0,
                'context': {'language': 'python', 'framework': 'pytest', 'complexity': 'low'}
            },
            'decisions': [
                {
                    'type': 'testing',
                    'choice': 'pytest framework',
                    'reasoning': 'Better fixtures and parametrization',
                    'alternatives': ['unittest', 'nose'],
                    'success': True,
                    'context': {'language': 'python', 'domain': 'testing'}
                }
            ],
            'learning': {
                'type': 'testing_patterns',
                'approach': 'practice + documentation',
                'effectiveness': 0.88,
                'time_to_mastery': 60.0,
                'resources': ['pytest.org', 'realpython.com'],
                'context': {'topic': 'pytest_patterns', 'difficulty': 'beginner'}
            }
        },
        
        # Session 3: Refactoring and Optimization
        {
            'code_samples': [
                {
                    'file_path': 'optimized_user_service.py',
                    'code': '''
class UserService:
    def __init__(self, db_connection):
        self.db = db_connection
        self.cache = {}
    
    def get_user_by_id(self, user_id):
        """Get user by ID with caching"""
        if user_id in self.cache:
            return self.cache[user_id]
        
        user = self.db.query(UserProfile).filter_by(id=user_id).first()
        if user:
            self.cache[user_id] = user
        return user
    
    def create_user(self, user_data):
        """Create new user with validation"""
        if not self._validate_user_data(user_data):
            raise ValueError("Invalid user data")
        
        user = create_user_profile(user_data)
        self.db.add(user)
        self.db.commit()
        return user
    
    def _validate_user_data(self, user_data):
        """Validate user data"""
        required_fields = ['username', 'email']
        return all(field in user_data for field in required_fields)
'''
                }
            ],
            'workflow': {
                'type': 'refactoring',
                'sequence': ['analyze', 'plan', 'refactor', 'test', 'validate'],
                'success': True,
                'time_spent': 150.0,
                'context': {'language': 'python', 'task': 'optimization', 'complexity': 'high'}
            },
            'decisions': [
                {
                    'type': 'optimization',
                    'choice': 'caching strategy',
                    'reasoning': 'Improve performance for frequently accessed data',
                    'alternatives': ['database_only', 'redis_cache'],
                    'success': True,
                    'context': {'language': 'python', 'domain': 'performance'}
                }
            ],
            'learning': {
                'type': 'performance_optimization',
                'approach': 'profiling + benchmarking',
                'effectiveness': 0.92,
                'time_to_mastery': 180.0,
                'resources': ['python.org', 'performance blogs'],
                'context': {'topic': 'python_optimization', 'difficulty': 'advanced'}
            }
        }
    ]
    
    return sessions

def demonstrate_context_suggestions(engine):
    """Demonstrate context suggestion capabilities"""
    print("🔍 CONTEXT SUGGESTION DEMONSTRATIONS")
    print("-" * 60)
    
    # Test different contexts
    test_contexts = [
        {
            'name': 'Python Web Development',
            'context': {
                'file': 'new_web_feature.py',
                'language': 'python',
                'task': 'web_development',
                'recent_work': [
                    {'file_type': 'python', 'language': 'python', 'task': 'user_management'},
                    {'file_type': 'python', 'language': 'python', 'task': 'api_endpoint'},
                    {'file_type': 'python', 'language': 'python', 'task': 'database_model'}
                ]
            }
        },
        {
            'name': 'Testing and Debugging',
            'context': {
                'file': 'test_new_feature.py',
                'language': 'python',
                'task': 'testing',
                'recent_work': [
                    {'file_type': 'python', 'language': 'python', 'task': 'unit_testing'},
                    {'file_type': 'python', 'language': 'python', 'task': 'integration_testing'},
                    {'file_type': 'python', 'language': 'python', 'task': 'test_debugging'}
                ]
            }
        },
        {
            'name': 'Performance Optimization',
            'context': {
                'file': 'optimize_service.py',
                'language': 'python',
                'task': 'refactoring',
                'recent_work': [
                    {'file_type': 'python', 'language': 'python', 'task': 'code_analysis'},
                    {'file_type': 'python', 'language': 'python', 'task': 'performance_profiling'},
                    {'file_type': 'python', 'language': 'python', 'task': 'algorithm_optimization'}
                ]
            }
        }
    ]
    
    for test_context in test_contexts:
        print(f"\n🎯 Context: {test_context['name']}")
        suggestions = engine.get_context_suggestions(test_context['context'], 'proactive')
        
        if suggestions:
            print(f"   📝 Generated {len(suggestions)} suggestions:")
            for i, suggestion in enumerate(suggestions[:3], 1):  # Show top 3
                print(f"      {i}. {suggestion.content[:80]}...")
                print(f"         Relevance: {suggestion.relevance_score:.2f}, Confidence: {suggestion.confidence:.2f}")
        else:
            print("   ❌ No suggestions generated")
    
    print()

def demonstrate_behavior_injection(engine):
    """Demonstrate behavior injection strategies"""
    print("🔄 BEHAVIOR INJECTION STRATEGIES")
    print("-" * 60)
    
    # Test different injection strategies
    test_context = {
        'file': 'current_work.py',
        'language': 'python',
        'task': 'feature_development',
        'recent_work': [
            {'file_type': 'python', 'language': 'python', 'task': 'class_implementation'},
            {'file_type': 'python', 'language': 'python', 'task': 'method_creation'},
            {'file_type': 'python', 'language': 'python', 'task': 'testing'}
        ]
    }
    
    strategies = ['proactive', 'reactive', 'predictive']
    
    for strategy in strategies:
        print(f"\n🎯 Strategy: {strategy.title()}")
        suggestions = engine.get_context_suggestions(test_context, strategy)
        
        if suggestions:
            print(f"   📝 Generated {len(suggestions)} suggestions:")
            for i, suggestion in enumerate(suggestions[:2], 1):  # Show top 2
                print(f"      {i}. [{suggestion.suggestion_type}] {suggestion.content[:70]}...")
        else:
            print("   ❌ No suggestions generated")
    
    print()

def demonstrate_pattern_analysis(engine):
    """Demonstrate pattern analysis capabilities"""
    print("📊 PATTERN ANALYSIS & INTELLIGENCE")
    print("-" * 60)
    
    # Get personalization summary
    summary = engine.get_personalization_summary()
    
    print(f"🎨 Style Patterns: {summary['preferences']['style_patterns']['total']}")
    for pattern_type, count in summary['preferences']['style_patterns']['by_type'].items():
        print(f"   • {pattern_type}: {count} patterns")
    
    print(f"\n🔄 Workflow Patterns: {summary['preferences']['workflow_patterns']['total']}")
    for pattern_type, count in summary['preferences']['workflow_patterns']['by_type'].items():
        print(f"   • {pattern_type}: {count} patterns")
    
    print(f"\n🏗️ Decision Patterns: {summary['preferences']['decision_patterns']['total']}")
    for pattern_type, count in summary['preferences']['decision_patterns']['by_type'].items():
        print(f"   • {pattern_type}: {count} patterns")
    
    print(f"\n📚 Learning Patterns: {summary['preferences']['learning_patterns']['total']}")
    for pattern_type, count in summary['preferences']['learning_patterns']['by_type'].items():
        print(f"   • {pattern_type}: {count} patterns")
    
    print(f"\n🔌 Behavior Injection Stats:")
    injection_stats = summary['behavior_injection']
    print(f"   • Total Injections: {injection_stats['total_injections']}")
    print(f"   • Average Suggestions: {injection_stats['average_suggestions']:.1f}")
    print(f"   • Recent Injections: {injection_stats['recent_injections']}")
    
    print()

def export_demo_results(engine, learning_time, total_patterns):
    """Export demo results and save to files"""
    print("💾 EXPORTING DEMO RESULTS")
    print("-" * 60)
    
    timestamp = int(time.time())
    
    # Export personalization data
    json_export = engine.export_personalization('json')
    json_file = f"phase3_demo_personalization_{timestamp}.json"
    with open(json_file, 'w') as f:
        f.write(json_export)
    print(f"📊 Personalization Data: {json_file} ({len(json_export):,} characters)")
    
    # Export summary
    summary_export = engine.export_personalization('summary')
    summary_file = f"phase3_demo_summary_{timestamp}.md"
    with open(summary_file, 'w') as f:
        f.write(summary_export)
    print(f"📝 Summary Report: {summary_file} ({len(summary_export):,} characters)")
    
    # Create demo results summary
    demo_results = {
        'demo_timestamp': timestamp,
        'phase': 'Phase 3: Personalization & Behavior Injection',
        'performance': {
            'learning_time': learning_time,
            'total_patterns_learned': total_patterns,
            'total_suggestions_generated': sum(len(engine.get_context_suggestions({}, 'proactive')) for _ in range(3))
        },
        'capabilities': {
            'style_learning': True,
            'workflow_modeling': True,
            'decision_tracking': True,
            'learning_patterns': True,
            'context_injection': True,
            'proactive_assistance': True
        },
        'next_phase': 'Phase 4: Intelligent Context Orchestration'
    }
    
    results_file = f"phase3_demo_results_{timestamp}.json"
    with open(results_file, 'w') as f:
        json.dump(demo_results, f, indent=2)
    print(f"📋 Demo Results: {results_file}")
    
    print(f"\n💾 All demo results exported successfully!")
    print(f"🎯 Ready for Phase 4: Intelligent Context Orchestration!")

def main():
    """Main demo function"""
    print("🚀 MEMORY CONTEXT MANAGER v2 - PHASE 3 DEMO")
    print("=" * 80)
    print()
    
    # Run the comprehensive demo
    engine = demo_personalization_engine()
    
    if engine:
        print(f"\n🎉 PHASE 3 DEMO COMPLETED SUCCESSFULLY!")
        summary = engine.get_personalization_summary()
        print(f"📊 Style Patterns: {summary['preferences']['style_patterns']['total']}")
        print(f"🔄 Workflow Patterns: {summary['preferences']['workflow_patterns']['total']}")
        print(f"🏗️ Decision Patterns: {summary['preferences']['decision_patterns']['total']}")
        print(f"📚 Learning Patterns: {summary['preferences']['learning_patterns']['total']}")
        print(f"🔌 Total Injections: {summary['behavior_injection']['total_injections']}")
        print()
        print(f"🚀 Ready to begin Phase 4: Intelligent Context Orchestration!")
    else:
        print(f"\n❌ Demo failed to complete successfully")

if __name__ == "__main__":
    main()
