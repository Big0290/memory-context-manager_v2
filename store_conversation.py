"""
Manual conversation storage script
Use this to manually store important conversations in memory
"""

import asyncio
import sys
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent))

async def store_conversation(user_message: str, ai_response: str = ""):
    """Store a conversation in memory"""
    
    # Initialize the system
    from main import initialize_server, mcp_client
    initialize_server()
    
    if mcp_client:
        try:
            # Track the conversation
            result = await mcp_client.call_tool(
                "track_cursor_conversation",
                user_message=user_message,
                assistant_response=ai_response,
                conversation_type="manual_storage"
            )
            
            print(f"✅ Conversation stored: {result.get('success', False)}")
            print(f"📚 Learned: {result.get('learned', [])}")
            
            return result
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    else:
        print("❌ MCP client not available")
        return None

if __name__ == "__main__":
    # Example usage
    asyncio.run(store_conversation(
        user_message="We've been working on fixing the memory retrieval system for the brain-inspired AI. The assistant name should be 'Johny' and we want full Cursor integration with conversation tracking.",
        ai_response="Successfully fixed memory retrieval, LLM context injection, and set up full Cursor MCP integration with conversation tracking and auto context injection."
    ))