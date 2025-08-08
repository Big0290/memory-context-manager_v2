#!/usr/bin/env python3
"""
Test script for Auto Memory Integration
Shows how to use the automatic conversation memory system
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))
sys.path.insert(0, str(Path(__file__).parent / "plugins"))

from auto_memory import AutoMemoryPlugin

async def test_conversation_flow():
    """Test the automatic conversation memory flow"""
    
    print("🧠 Testing Automatic Conversation Memory")
    print("=" * 50)
    
    # Initialize the plugin
    plugin = AutoMemoryPlugin()
    plugin.initialize()
    
    # Test conversations
    conversations = [
        "Hi there! My name is Johny and I love working on AI projects.",
        "I prefer to be called Johny, not John or Jonathan.",
        "I'm building a memory system for AI agents right now.",
        "What's my name again?",  # This should retrieve the stored name
    ]
    
    for i, message in enumerate(conversations, 1):
        print(f"\n--- Conversation Turn {i} ---")
        print(f"USER: {message}")
        
        # Step 1: Auto-process the message (stores important info + gets context)
        result = await plugin._auto_process_handler(message)
        
        if result["success"]:
            print(f"📝 Important info found: {result['important_info_found']}")
            print(f"🧠 Context summary: {result['user_context_summary']}")
            
            # Step 2: Get full user context for AI response
            context_result = await plugin._get_user_context_handler()
            if context_result["success"]:
                print(f"👤 User context: {context_result['context_summary']}")
        
        print("-" * 30)
    
    print("\n🔍 Final Memory Search Test")
    print("Searching for 'Johny name'...")
    
    search_result = await plugin._search_memories_handler("Johny name")
    if search_result["success"]:
        print(f"Found {search_result['total_found']} memories:")
        for memory in search_result["memories"][:3]:
            content = memory.get('content', '')
            print(f"  - {content[:100]}...")
    
    print("\n✅ Auto Memory Test Complete!")
    print("\nNow your AI can use these tools to automatically:")
    print("  • Store: auto_process_message before each response")
    print("  • Retrieve: get_user_context to provide context")
    print("  • Remember: remember_fact for important info")
    print("  • Search: search_memories for specific queries")

if __name__ == "__main__":
    asyncio.run(test_conversation_flow())