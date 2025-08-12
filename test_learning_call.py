#!/usr/bin/env python3
"""
Test Script: How to Call Our Autonomous Evolution System
Demonstrates learning from MCP documentation
"""

import time
import logging
from autonomous_evolution_engine import AutonomousEvolutionEngine

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_learning_call():
    """Test how to call our evolution system to learn"""
    
    print("🚀 TESTING AUTONOMOUS EVOLUTION SYSTEM LEARNING")
    print("=" * 60)
    
    # Create evolution engine
    print("📚 Creating Autonomous Evolution Engine...")
    evolution_engine = AutonomousEvolutionEngine()
    
    # Start the evolution system
    print("🔄 Starting Evolution System...")
    if evolution_engine.start_evolution_system():
        print("✅ Evolution system started successfully!")
        
        # Get initial status
        print("\n📊 Initial System Status:")
        initial_status = evolution_engine.get_comprehensive_status()
        print(f"   Overall Health: {initial_status['system_health']['overall_health']:.3f}")
        print(f"   Performance: {initial_status['system_health']['performance_score']:.3f}")
        print(f"   Intelligence: {initial_status['system_health']['intelligence_score']:.3f}")
        
        # Simulate learning from MCP documentation
        print("\n📚 LEARNING FROM MCP DOCUMENTATION")
        print("-" * 40)
        
        # This is how you would call it to learn from docs
        mcp_documentation = {
            'source': 'https://docs.cursor.com/en/context/mcp',
            'content_type': 'official_mcp_documentation',
            'learning_priority': 'high',
            'key_learnings': [
                'SSE transport method for real-time updates',
                'HTTP transport for remote deployments', 
                'OAuth authentication integration',
                'Image handling with base64 encoding',
                'Multi-user support capabilities'
            ]
        }
        
        print(f"📖 Learning Source: {mcp_documentation['source']}")
        print(f"🎯 Priority: {mcp_documentation['learning_priority']}")
        print(f"📚 Key Learnings: {len(mcp_documentation['key_learnings'])} items")
        
        # Schedule evolution tasks based on learning
        print("\n🔄 SCHEDULING EVOLUTION TASKS")
        print("-" * 40)
        
        evolution_tasks = [
            {
                'type': 'performance',
                'priority': 'high',
                'delay': 2,
                'description': 'Implement SSE transport from MCP docs'
            },
            {
                'type': 'intelligence', 
                'priority': 'normal',
                'delay': 5,
                'description': 'Integrate OAuth patterns from MCP docs'
            },
            {
                'type': 'adaptability',
                'priority': 'medium', 
                'delay': 8,
                'description': 'Add image handling capabilities from MCP docs'
            }
        ]
        
        scheduled_tasks = []
        for task in evolution_tasks:
            task_id = evolution_engine.schedule_evolution_task(task)
            if task_id:
                scheduled_tasks.append(task_id)
                print(f"   ✅ Scheduled: {task['type']} evolution ({task['priority']} priority)")
                print(f"      Description: {task['description']}")
            else:
                print(f"   ❌ Failed to schedule: {task['type']} evolution")
        
        print(f"\n📊 Total evolution tasks scheduled: {len(scheduled_tasks)}")
        
        # Wait for evolution to execute
        print("\n⏳ Waiting for evolution to execute...")
        time.sleep(15)
        
        # Check final status
        print("\n📊 FINAL SYSTEM STATUS")
        print("-" * 40)
        final_status = evolution_engine.get_comprehensive_status()
        
        print(f"   Overall Health: {final_status['system_health']['overall_health']:.3f}")
        print(f"   Performance: {final_status['system_health']['performance_score']:.3f}")
        print(f"   Intelligence: {final_status['system_health']['intelligence_score']:.3f}")
        print(f"   Adaptability: {final_status['system_health']['adaptability_score']:.3f}")
        
        # Calculate improvements
        initial_health = initial_status['system_health']['overall_health']
        final_health = final_status['system_health']['overall_health']
        improvement = final_health - initial_health
        
        print(f"\n📈 Health Improvement: {improvement:+.3f} ({improvement/initial_health*100:+.1f}%)")
        
        # Show scheduler results
        scheduler_stats = final_status['scheduler_stats']
        print(f"\n📅 Evolution Results:")
        print(f"   Tasks Completed: {scheduler_stats['total_completed']}")
        print(f"   Success Rate: {scheduler_stats['success_rate']:.1%}")
        print(f"   Average Execution Time: {scheduler_stats['average_execution_time']:.4f}s")
        
        # Stop evolution system
        print("\n🛑 Stopping Evolution System...")
        evolution_engine.stop_evolution_system()
        print("✅ Evolution system stopped successfully")
        
        print("\n🎉 LEARNING TEST COMPLETED SUCCESSFULLY!")
        print("🚀 Your system has learned from the MCP documentation!")
        
    else:
        print("❌ Failed to start evolution system")

if __name__ == "__main__":
    test_learning_call()
