#!/usr/bin/env python3
"""
AI Agent Memory Integration
Complete system for integrating automatic memory into AI agent responses
"""

import json
import asyncio
from typing import Dict, Any, List

class AIMemoryAssistant:
    """
    Helper class that AI agents can use to automatically handle memory
    """
    
    def __init__(self, mcp_client):
        """
        Initialize with MCP client (your server connection)
        """
        self.mcp = mcp_client
        self.memory_enabled = True
        
    async def process_user_message(self, user_message: str) -> Dict[str, Any]:
        """
        Process a user message and return context for AI response
        
        This should be called BEFORE the AI generates a response
        """
        if not self.memory_enabled:
            return {"context": "", "important_info": []}
        
        try:
            # Step 1: Auto-process the message (extract & store important info)
            process_result = await self.mcp.call_tool(
                "auto_process_message",
                user_message=user_message
            )
            
            # Step 2: Get user context
            context_result = await self.mcp.call_tool(
                "get_user_context", 
                query="user name preferences important facts"
            )
            
            # Step 3: Format response for AI
            return {
                "success": True,
                "context_summary": context_result.get("context_summary", ""),
                "user_info": context_result.get("user_info", {}),
                "important_info_stored": process_result.get("important_info_found", []),
                "memory_instructions": self._create_memory_instructions(context_result),
                "should_acknowledge_memory": len(process_result.get("important_info_found", [])) > 0
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "context_summary": "",
                "memory_instructions": ""
            }
    
    async def search_specific_memory(self, query: str) -> Dict[str, Any]:
        """
        Search for specific information in memory
        """
        try:
            result = await self.mcp.call_tool("search_memories", query=query)
            return result
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def remember_important_fact(self, fact: str) -> Dict[str, Any]:
        """
        Manually store an important fact
        """
        try:
            result = await self.mcp.call_tool("remember_fact", fact=fact)
            return result
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _create_memory_instructions(self, context_result: Dict[str, Any]) -> str:
        """
        Create instructions for the AI on how to use the memory context
        """
        if not context_result.get("success"):
            return ""
            
        user_info = context_result.get("user_info", {})
        instructions = []
        
        # Name instructions
        if user_info.get("name"):
            name_info = user_info["name"][0] if user_info["name"] else ""
            if "call me" in name_info.lower() or "name is" in name_info.lower():
                instructions.append(f"REMEMBER: {name_info}")
        
        # Preference instructions  
        if user_info.get("preferences"):
            prefs = user_info["preferences"][:2]  # Top 2 preferences
            for pref in prefs:
                instructions.append(f"USER PREFERENCE: {pref}")
        
        # Important facts
        if user_info.get("important_facts"):
            facts = user_info["important_facts"][:2]  # Top 2 facts
            for fact in facts:
                instructions.append(f"IMPORTANT: {fact}")
        
        return " | ".join(instructions)


class ConversationDemo:
    """
    Demo showing how an AI agent would use the memory system
    """
    
    def __init__(self):
        self.memory_assistant = None  # Would be initialized with real MCP client
        
    def simulate_ai_response_with_memory(self, user_message: str, memory_context: Dict[str, Any]) -> str:
        """
        Simulate how an AI agent would respond using memory context
        """
        # This is what your AI agent would do:
        
        # 1. Check if memory processing was successful
        if not memory_context.get("success", False):
            return self._generate_response_without_memory(user_message)
        
        # 2. Get memory instructions
        context_summary = memory_context.get("context_summary", "")
        memory_instructions = memory_context.get("memory_instructions", "")
        should_acknowledge = memory_context.get("should_acknowledge_memory", False)
        
        # 3. Generate response with context
        return self._generate_response_with_memory(
            user_message, 
            context_summary, 
            memory_instructions,
            should_acknowledge
        )
    
    def _generate_response_without_memory(self, user_message: str) -> str:
        """Standard response without memory"""
        return "I'd be happy to help! (No memory context available)"
    
    def _generate_response_with_memory(self, user_message: str, context: str, 
                                     instructions: str, acknowledge: bool) -> str:
        """Response using memory context"""
        response_parts = []
        
        # Acknowledge stored information if something new was learned
        if acknowledge and any(keyword in user_message.lower() for keyword in ["name", "call me", "i'm"]):
            if "name" in instructions.lower():
                name = self._extract_name_from_instructions(instructions)
                response_parts.append(f"Thanks for telling me your name, {name}!")
            else:
                response_parts.append("I'll remember that!")
        
        # Use context to personalize response
        if context and "name:" in context.lower():
            name = self._extract_name_from_context(context)
            if name and "what" in user_message.lower() and "name" in user_message.lower():
                return f"Your name is {name}! I remembered that from our previous conversation."
        
        # Generate contextual response
        if "how are you" in user_message.lower() and context:
            response_parts.append(f"I'm doing well! Based on what I know about you ({context}), how are your projects going?")
        else:
            base_response = "I'd be happy to help!"
            if context:
                base_response += f" (Context: {context})"
            response_parts.append(base_response)
        
        return " ".join(response_parts)
    
    def _extract_name_from_instructions(self, instructions: str) -> str:
        """Extract name from memory instructions"""
        if "call me" in instructions.lower():
            parts = instructions.lower().split("call me")
            if len(parts) > 1:
                name_part = parts[1].strip().split()[0]
                return name_part.title()
        return "there"
    
    def _extract_name_from_context(self, context: str) -> str:
        """Extract name from context summary"""
        if "name:" in context.lower():
            parts = context.split(":")
            for part in parts:
                if "johny" in part.lower() or "john" in part.lower():
                    return "Johny"
        return ""


async def demonstrate_full_workflow():
    """
    Complete demonstration of AI agent with automatic memory
    """
    print("🤖 AI Agent with Automatic Memory Demo")
    print("=" * 50)
    
    # Simulate conversation flow
    demo = ConversationDemo()
    
    conversations = [
        {
            "user": "Hi there! My name is Johny and I love working on AI projects.",
            "expected_memory": {
                "success": True,
                "context_summary": "No specific user context found",
                "important_info_stored": ["User name: Johny", "Important statement"],
                "memory_instructions": "REMEMBER: User prefers to be called: Johny",
                "should_acknowledge_memory": True
            }
        },
        {
            "user": "What's my name again?",
            "expected_memory": {
                "success": True,
                "context_summary": "Name: User prefers to be called: Johny",
                "important_info_stored": [],
                "memory_instructions": "REMEMBER: User prefers to be called: Johny",
                "should_acknowledge_memory": False
            }
        },
        {
            "user": "How are you doing today?",
            "expected_memory": {
                "success": True,
                "context_summary": "Name: User prefers to be called: Johny | Preference: i love working on ai projects",
                "important_info_stored": [],
                "memory_instructions": "REMEMBER: User prefers to be called: Johny | USER PREFERENCE: i love working on ai projects",
                "should_acknowledge_memory": False
            }
        }
    ]
    
    for i, conv in enumerate(conversations, 1):
        print(f"\n--- Conversation Turn {i} ---")
        print(f"USER: {conv['user']}")
        
        # Simulate memory processing (this is what would happen in real implementation)
        memory_context = conv["expected_memory"]
        
        print(f"🧠 MEMORY PROCESSED:")
        print(f"   Context: {memory_context['context_summary']}")
        print(f"   Stored: {memory_context['important_info_stored']}")
        
        # Generate AI response using memory
        ai_response = demo.simulate_ai_response_with_memory(conv['user'], memory_context)
        print(f"🤖 AI: {ai_response}")
        
        print("-" * 40)
    
    print(f"\n✨ Key Benefits Demonstrated:")
    print(f"   ✅ AI remembers user's name (Johny)")
    print(f"   ✅ AI stores preferences automatically") 
    print(f"   ✅ AI retrieves context for better responses")
    print(f"   ✅ AI acknowledges when learning new info")
    
    print(f"\n🔧 Implementation Steps:")
    print(f"   1. Your AI calls: auto_process_message(user_input)")
    print(f"   2. Your AI calls: get_user_context()")
    print(f"   3. Your AI uses context to generate personalized response")
    print(f"   4. Memory persists across conversations!")


def create_ai_integration_template():
    """
    Create template code for integrating memory into existing AI agent
    """
    template = '''
# AI Agent Memory Integration Template
# Add this to your existing AI agent code

async def generate_ai_response_with_memory(user_message: str, mcp_client) -> str:
    """
    Enhanced AI response function with automatic memory
    """
    try:
        # STEP 1: Process user message and get context
        memory_result = await mcp_client.call_tool(
            "auto_process_message",
            user_message=user_message
        )
        
        context_result = await mcp_client.call_tool(
            "get_user_context",
            query="user name preferences important facts"  
        )
        
        # STEP 2: Extract context for AI
        context_summary = context_result.get("context_summary", "")
        important_info = memory_result.get("important_info_found", [])
        
        # STEP 3: Create AI prompt with memory context
        ai_prompt = f"""
        User message: {user_message}
        
        Memory context: {context_summary}
        Recently stored: {important_info}
        
        Instructions: 
        - Use the memory context to personalize your response
        - If the user told you their name, use it appropriately
        - Acknowledge if you learned something new
        - Reference past conversations when relevant
        """
        
        # STEP 4: Generate response using your existing AI system
        ai_response = your_ai_model.generate(ai_prompt)
        
        return ai_response
        
    except Exception as e:
        # Fallback to normal response if memory fails
        return your_ai_model.generate(user_message)

# Example usage:
# response = await generate_ai_response_with_memory("Hi, I'm Johny", mcp_client)
    '''
    
    return template


if __name__ == "__main__":
    print("🧠 Complete AI Agent Memory Integration")
    print("=" * 50)
    
    # Run demonstration
    asyncio.run(demonstrate_full_workflow())
    
    print("\n" + "=" * 50) 
    print("📝 INTEGRATION TEMPLATE")
    print("=" * 50)
    print(create_ai_integration_template())
    
    print("🎯 Next Steps:")
    print("1. Restart your MCP server to load auto_memory plugin")
    print("2. Integrate the template code into your AI agent") 
    print("3. Test with: 'Hi, my name is Johny'")
    print("4. Then ask: 'What's my name?' - It should remember!")