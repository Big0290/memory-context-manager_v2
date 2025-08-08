"""
Memory Integration Helper
Simple wrapper to make it easy for AI agents to use automatic memory
"""

class MemoryHelper:
    """
    Simple helper class that AI agents can use for memory operations
    Usage: memory = MemoryHelper(mcp_client)
    """
    
    def __init__(self, mcp_client):
        self.mcp = mcp_client
        
    async def process_and_get_context(self, user_message: str) -> str:
        """
        One-shot method: process message and return context string for AI
        
        Returns a context string that can be added to the AI prompt
        """
        try:
            # Process message
            await self.mcp.call_tool("auto_process_message", user_message=user_message)
            
            # Get context
            result = await self.mcp.call_tool("get_user_context")
            
            if result.get("success"):
                context = result.get("context_summary", "")
                return f"[MEMORY CONTEXT: {context}]" if context else ""
            else:
                return ""
                
        except Exception as e:
            return f"[MEMORY ERROR: {str(e)}]"
    
    async def remember_fact(self, fact: str) -> bool:
        """Store an important fact, returns True if successful"""
        try:
            result = await self.mcp.call_tool("remember_fact", fact=fact)
            return result.get("success", False)
        except:
            return False
    
    async def search_memory(self, query: str) -> str:
        """Search memory and return formatted results"""
        try:
            result = await self.mcp.call_tool("search_memories", query=query)
            if result.get("success"):
                memories = result.get("memories", [])
                if memories:
                    return f"Found {len(memories)} memories: " + "; ".join([m.get('content', '')[:50] for m in memories[:3]])
                else:
                    return "No memories found"
            else:
                return "Search failed"
        except Exception as e:
            return f"Search error: {str(e)}"


# Example usage for AI agents:
"""
# In your AI agent code:

from memory_integration_helper import MemoryHelper

# Initialize 
memory = MemoryHelper(your_mcp_client)

# Before generating AI response:
context = await memory.process_and_get_context(user_message)

# Add context to your AI prompt:
full_prompt = f"{user_message}\n{context}"

# Generate response with your AI model:
ai_response = your_ai_model.generate(full_prompt)
"""

def create_simple_integration_example():
    """
    Create the simplest possible integration example
    """
    return '''
# SIMPLEST INTEGRATION - Add this to your AI agent:

async def ai_response_with_memory(user_input, mcp_client):
    """Your AI response function with memory"""
    
    # Step 1: Process memory (stores important info, gets context)
    context = ""
    try:
        await mcp_client.call_tool("auto_process_message", user_message=user_input)
        result = await mcp_client.call_tool("get_user_context")
        if result.get("success"):
            context = result.get("context_summary", "")
    except:
        pass  # Continue without memory if it fails
    
    # Step 2: Create AI prompt with context
    if context:
        prompt = f"User: {user_input}\\nContext: {context}\\nResponse:"
    else:
        prompt = f"User: {user_input}\\nResponse:"
    
    # Step 3: Generate response with your AI model
    return your_ai_model.generate(prompt)

# Test it:
# response = await ai_response_with_memory("Hi, I'm Johny", mcp_client)
# Later: response = await ai_response_with_memory("What's my name?", mcp_client)
# Should remember "Johny"!
'''

if __name__ == "__main__":
    print("🔧 Memory Integration Helper")
    print("=" * 40)
    print(create_simple_integration_example())