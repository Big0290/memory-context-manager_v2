"""
Cognitive Brain Plugin Usage Example
Demonstrates how to use the brain-inspired plugin in real tasks
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any

# Simulated MCP server class for demonstration
class MockMCPServer:
    def __init__(self):
        self.tools = {}
        self.resources = {}
    
    def tool(self, name: str):
        def decorator(func):
            self.tools[name] = func
            return func
        return decorator
    
    def resource(self, name: str):
        def decorator(func):
            self.resources[name] = func
            return func
        return decorator
    
    async def call_tool(self, tool_name: str, **kwargs):
        if tool_name in self.tools:
            return await self.tools[tool_name](**kwargs)
        else:
            return {"error": f"Tool {tool_name} not found"}


async def demonstrate_brain_plugin():
    """
    Comprehensive demonstration of the cognitive brain plugin
    """
    print("🧠 Cognitive Brain Plugin Demonstration")
    print("=" * 50)
    
    # Import the plugin
    from plugins.cognitive_brain_plugin.plugin import create_plugin
    
    # Create mock MCP server
    server = MockMCPServer()
    
    # Create and initialize plugin
    plugin_config = {
        "storage_dir": "demo_brain_memory",
        "auto_analyze": True,
        "debug_mode": True,
        "memory_threshold": 50
    }
    
    brain_plugin = create_plugin(plugin_config)
    
    # Initialize with server
    print("\n1. Initializing Brain Plugin...")
    success = brain_plugin.initialize(server)
    print(f"   ✅ Plugin initialized: {success}")
    
    # Get plugin status
    status = brain_plugin.get_status()
    print(f"   📊 Plugin status: {status['status']}")
    
    print("\n2. Demonstrating Brain Tools...")
    
    # Example 1: Analyze complex content
    print("\n   📝 Example 1: Content Analysis")
    analysis_content = """
    We need to implement a new authentication system for our application. 
    This is critical because our current system has security vulnerabilities 
    that could be exploited. The deadline is next Friday, and we need to 
    coordinate with the security team and update all client applications.
    """
    
    analysis_result = await server.call_tool(
        "brain_analyze",
        content=analysis_content,
        context_type="task"
    )
    
    print(f"   🔍 Analysis completed: {analysis_result.get('analyzed', False)}")
    if analysis_result.get('emotional_analysis'):
        emotion_data = analysis_result['emotional_analysis']
        print(f"   😊 Emotional weight: {emotion_data.get('emotional_weight', 'N/A')}")
        print(f"   ⭐ Importance score: {emotion_data.get('importance_score', 0):.2f}")
        print(f"   🚨 Priority: {emotion_data.get('recommended_priority', 'N/A')}")
    
    # Example 2: Store specific memories
    print("\n   💾 Example 2: Memory Storage")
    
    memories_to_store = [
        {
            "content": "Authentication system vulnerability discovered in login module",
            "tags": ["security", "critical", "authentication"],
            "emotional_weight": "critical"
        },
        {
            "content": "Team meeting scheduled for Friday to discuss security fixes",
            "tags": ["meeting", "team", "security"],
            "emotional_weight": "important"
        },
        {
            "content": "Successfully completed user interface redesign last month",
            "tags": ["ui", "completed", "success"],
            "emotional_weight": "positive"
        }
    ]
    
    for i, memory in enumerate(memories_to_store, 1):
        result = await server.call_tool("brain_remember", **memory)
        print(f"   📚 Memory {i} stored: {result.get('success', False)} (ID: {result.get('memory_id', 'N/A')[:12]}...)")
    
    # Example 3: Memory recall
    print("\n   🔍 Example 3: Memory Recall")
    
    search_queries = [
        "security vulnerability",
        "team meeting",
        "user interface",
        "authentication system"
    ]
    
    for query in search_queries:
        recall_result = await server.call_tool("brain_recall", query=query, limit=3)
        memories = recall_result.get('memories', [])
        print(f"   🎯 Query '{query}': Found {len(memories)} memories")
        
        for memory in memories[:1]:  # Show first result
            content_preview = memory['content'][:60] + "..." if len(memory['content']) > 60 else memory['content']
            print(f"      └─ {content_preview}")
    
    # Example 4: Brain reflection
    print("\n   🤔 Example 4: Brain Reflection")
    
    reflection_result = await server.call_tool(
        "brain_reflect",
        focus_areas=["memories", "decisions", "emotions"],
        period_hours=1  # Last hour
    )
    
    if reflection_result.get('success'):
        insights = reflection_result.get('insights_generated', 0)
        patterns = reflection_result.get('patterns_identified', 0)
        improvements = reflection_result.get('improvements_suggested', 0)
        
        print(f"   💡 Generated {insights} insights")
        print(f"   🔗 Identified {patterns} patterns")
        print(f"   📈 Suggested {improvements} improvements")
    
    # Example 5: Brain status monitoring
    print("\n   📊 Example 5: Brain Status")
    
    brain_status = await server.call_tool("brain_status")
    if brain_status.get('brain_state'):
        brain_state = brain_status['brain_state']
        print(f"   🧠 Active identity: {brain_state.get('active_identity', 'default')}")
        print(f"   💭 Current focus: {brain_state.get('current_focus', 'none')}")
        print(f"   📊 Memory activity: {brain_state.get('memory_activity', 0):.2f}")
        print(f"   😊 Emotion activity: {brain_state.get('emotion_activity', 0):.2f}")
    
    if brain_status.get('modules'):
        print("   🔧 Module status:")
        for module_name, module_status in brain_status['modules'].items():
            activity = module_status.get('activity_level', 0)
            status_icon = "🟢" if activity > 0.5 else "🟡" if activity > 0 else "🔴"
            print(f"      {status_icon} {module_name}: {activity:.2f}")
    
    # Example 6: Debug mode
    print("\n   🐛 Example 6: Debug Information")
    
    debug_result = await server.call_tool("brain_debug", enable=True)
    if debug_result.get('debug_mode'):
        print("   🔍 Debug mode enabled")
        
        if debug_result.get('memory_statistics'):
            mem_stats = debug_result['memory_statistics']
            total_memories = mem_stats.get('total_memories_24h', 0)
            avg_confidence = mem_stats.get('average_confidence', 0)
            print(f"   📈 Memories (24h): {total_memories}")
            print(f"   🎯 Avg confidence: {avg_confidence:.2f}")
            
            if mem_stats.get('emotional_distribution'):
                print("   😊 Emotional distribution:")
                for emotion, count in mem_stats['emotional_distribution'].items():
                    print(f"      └─ {emotion}: {count}")
    
    print("\n3. Demonstrating Real-World Task Scenario...")
    
    # Real-world scenario: Project management task
    await demonstrate_project_management_scenario(server)
    
    print("\n4. Plugin Shutdown...")
    brain_plugin.shutdown()
    print("   ✅ Brain plugin shutdown complete")
    
    print("\n🎉 Brain Plugin Demonstration Complete!")


async def demonstrate_project_management_scenario(server):
    """
    Demonstrate the brain plugin handling a complex project management scenario
    """
    print("\n   📋 Scenario: Software Project Crisis Management")
    
    # Simulate a series of events in a software project
    events = [
        {
            "content": "Critical bug discovered in production affecting 50% of users",
            "context_type": "incident",
            "tags": ["critical", "production", "bug"],
            "emotional_weight": "critical"
        },
        {
            "content": "Emergency team meeting called for immediate resolution",
            "context_type": "task",
            "tags": ["emergency", "meeting", "team"],
            "emotional_weight": "important"
        },
        {
            "content": "Root cause identified: database connection pool exhaustion",
            "context_type": "investigation",
            "tags": ["root-cause", "database", "connection-pool"],
            "emotional_weight": "important"
        },
        {
            "content": "Hotfix deployed successfully, monitoring system recovery",
            "context_type": "resolution",
            "tags": ["hotfix", "deployment", "monitoring"],
            "emotional_weight": "positive"
        },
        {
            "content": "System fully recovered, all users can access application normally",
            "context_type": "resolution",
            "tags": ["recovery", "success", "users"],
            "emotional_weight": "positive"
        }
    ]
    
    print(f"   📥 Processing {len(events)} crisis events...")
    
    # Store all events and analyze
    for i, event in enumerate(events, 1):
        # Store in memory
        memory_result = await server.call_tool("brain_remember", **event)
        
        # Analyze the content
        analysis_result = await server.call_tool(
            "brain_analyze",
            content=event["content"],
            context_type=event["context_type"]
        )
        
        print(f"   📝 Event {i}: {event['context_type']} - {analysis_result.get('analyzed', False)}")
    
    # After all events, trigger comprehensive analysis
    print("\n   🤔 Triggering post-incident reflection...")
    
    reflection_result = await server.call_tool(
        "brain_reflect",
        focus_areas=["decisions", "patterns", "learning"],
        period_hours=1
    )
    
    if reflection_result.get('success'):
        print(f"   💡 Reflection insights: {reflection_result.get('insights_generated', 0)}")
        
        # Search for lessons learned
        lessons_result = await server.call_tool(
            "brain_recall",
            query="root cause database connection",
            limit=5
        )
        
        memories = lessons_result.get('memories', [])
        print(f"   📚 Related memories found: {len(memories)}")
        
        # Look for patterns
        pattern_result = await server.call_tool(
            "brain_recall",
            query="production bug critical",
            limit=3
        )
        
        patterns = pattern_result.get('memories', [])
        print(f"   🔍 Similar incident patterns: {len(patterns)}")
    
    print("   ✅ Crisis management scenario analysis complete")


def demonstrate_memory_consolidation():
    """
    Demonstrate memory consolidation and pattern recognition
    """
    print("\n🧠 Memory Consolidation Demo")
    print("-" * 30)
    
    # This would typically run as a background process
    print("Memory consolidation happens automatically based on:")
    print("  • Emotional weight (critical/important memories)")
    print("  • Access frequency (often recalled memories)")
    print("  • Recency (recent memories)")
    print("  • Association strength (well-connected memories)")
    
    print("\nConsolidation benefits:")
    print("  ✅ Strengthens important memories")
    print("  ✅ Creates new associations")
    print("  ✅ Identifies recurring patterns")
    print("  ✅ Improves retrieval efficiency")


def demonstrate_multi_agent_sync():
    """
    Demonstrate multi-agent synchronization capabilities
    """
    print("\n🤝 Multi-Agent Synchronization Demo")
    print("-" * 35)
    
    print("The brain plugin supports multi-agent scenarios:")
    print("  • Agent registration and capability sharing")
    print("  • Context synchronization with privacy controls")
    print("  • Collaborative memory formation")
    print("  • Conflict resolution strategies")
    print("  • Broadcast updates across agent networks")
    
    print("\nUse cases:")
    print("  🤖 Multiple AI assistants sharing knowledge")
    print("  🧠 Distributed cognitive processing")
    print("  🔄 Cross-agent learning and adaptation")
    print("  🛡️ Privacy-preserving information sharing")


if __name__ == "__main__":
    print("Starting Brain Plugin Demonstration...")
    asyncio.run(demonstrate_brain_plugin())
    
    print("\nAdditional Features:")
    demonstrate_memory_consolidation()
    demonstrate_multi_agent_sync()
    
    print("\n" + "=" * 50)
    print("🎯 Key Benefits of the Cognitive Brain Plugin:")
    print("  • Intelligent memory management with emotional weighting")
    print("  • Contextual analysis and routing")
    print("  • Self-reflection and continuous learning")
    print("  • Pattern recognition and insight generation")  
    print("  • Multi-agent collaboration capabilities")
    print("  • Debug and introspection tools")
    print("=" * 50)