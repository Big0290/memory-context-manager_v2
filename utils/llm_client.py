"""
LLM Client for Ollama Integration
Handles communication with the Ollama LLM service
"""

import aiohttp
import asyncio
import json
import logging
import os
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class OllamaClient:
    """
    Async client for Ollama LLM service
    """
    
    def __init__(self, base_url: str = None, model: str = None):
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = model or os.getenv("OLLAMA_MODEL", "llama3.1:8b")
        self.session = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def generate_response(self, prompt: str, system_prompt: str = None, 
                              temperature: float = 0.7, max_tokens: int = 500) -> Dict[str, Any]:
        """
        Generate response from Ollama
        """
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        # Construct messages
        messages = []
        
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        messages.append({
            "role": "user", 
            "content": prompt
        })
        
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }
        
        try:
            async with self.session.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=aiohttp.ClientTimeout(total=60)
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    return {
                        "success": True,
                        "response": result.get("message", {}).get("content", ""),
                        "model": self.model,
                        "tokens_used": result.get("eval_count", 0),
                        "generation_time": result.get("total_duration", 0) / 1000000000  # Convert to seconds
                    }
                else:
                    error_text = await response.text()
                    return {
                        "success": False,
                        "error": f"HTTP {response.status}: {error_text}",
                        "response": ""
                    }
                    
        except asyncio.TimeoutError:
            return {
                "success": False,
                "error": "Request timeout - LLM took too long to respond",
                "response": ""
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"LLM request failed: {str(e)}",
                "response": ""
            }
    
    async def health_check(self) -> bool:
        """
        Check if Ollama service is healthy
        """
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        try:
            async with self.session.get(
                f"{self.base_url}/api/tags",
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                return response.status == 200
        except:
            return False
    
    async def list_models(self) -> Dict[str, Any]:
        """
        List available models
        """
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        try:
            async with self.session.get(f"{self.base_url}/api/tags") as response:
                if response.status == 200:
                    result = await response.json()
                    return {
                        "success": True,
                        "models": [model["name"] for model in result.get("models", [])]
                    }
                else:
                    return {"success": False, "error": "Failed to list models"}
        except Exception as e:
            return {"success": False, "error": str(e)}


class MemoryEnhancedLLM:
    """
    LLM client specifically designed for memory-enhanced conversations
    """
    
    def __init__(self, ollama_client: OllamaClient):
        self.ollama = ollama_client
        self.system_prompt = self._create_system_prompt()
    
    def _create_system_prompt(self) -> str:
        """Create system prompt for memory-enhanced conversations"""
        return """You are an AI assistant with access to conversation memory and context.

CRITICAL RULES:
1. When "Context Information:" is provided in the prompt, you MUST use it to answer the question
2. If context contains your name or identity, use it when asked about yourself
3. If context contains user information, reference it naturally in responses
4. Always prioritize context information over general knowledge
5. Be conversational and natural while using the provided context

Example:
- Context: "User name/identity: Johny"
- Question: "What is your name?" 
- Response: "My name is Johny!"

Use the context information directly and naturally in your responses."""
    
    async def generate_memory_response(self, user_message: str, memory_context: str = "", 
                                     learned_something: bool = False) -> str:
        """
        Generate response using memory context
        """
        # Build enhanced prompt that forces the LLM to use context
        if memory_context:
            # Create a more structured prompt that the LLM can't ignore
            full_prompt = f"""Context Information: {memory_context}

User Question: {user_message}

Instructions: Answer the user's question using the context information provided above. If the context contains information relevant to the question, use it directly in your response. Be conversational and natural.

Response:"""
        else:
            full_prompt = f"User Question: {user_message}\n\nResponse:"
        
        # Generate response
        result = await self.ollama.generate_response(
            prompt=full_prompt,
            system_prompt=self.system_prompt,
            temperature=0.7,
            max_tokens=300
        )
        
        if result["success"]:
            return result["response"].strip()
        else:
            # Fallback response
            logger.error(f"LLM generation failed: {result.get('error')}")
            return "I'd be happy to help! (Note: I'm having trouble with my AI processing right now)"
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test LLM connection with a simple prompt"""
        test_result = await self.ollama.generate_response(
            "Hello! Please respond with 'Connection test successful.'",
            temperature=0.1,
            max_tokens=50
        )
        
        return {
            "connection_working": test_result["success"],
            "response": test_result.get("response", ""),
            "error": test_result.get("error"),
            "model": self.ollama.model
        }


# Global LLM client instance
_global_llm_client = None

async def get_llm_client() -> MemoryEnhancedLLM:
    """Get global LLM client instance"""
    global _global_llm_client
    
    if _global_llm_client is None:
        ollama_client = OllamaClient()
        _global_llm_client = MemoryEnhancedLLM(ollama_client)
    
    return _global_llm_client

async def test_llm_integration():
    """Test the LLM integration"""
    print("🤖 Testing LLM Integration...")
    
    async with OllamaClient() as ollama:
        # Test connection
        health_ok = await ollama.health_check()
        print(f"✅ Ollama Health: {'OK' if health_ok else 'FAILED'}")
        
        if not health_ok:
            print("❌ Cannot connect to Ollama service")
            return
        
        # List models
        models_result = await ollama.list_models()
        if models_result["success"]:
            print(f"📦 Available models: {', '.join(models_result['models'])}")
        
        # Test memory-enhanced LLM
        llm = MemoryEnhancedLLM(ollama)
        
        # Test basic response
        test_result = await llm.test_connection()
        print(f"🧠 LLM Test: {'PASSED' if test_result['connection_working'] else 'FAILED'}")
        print(f"   Response: {test_result['response']}")
        
        # Test memory-enhanced response
        memory_response = await llm.generate_memory_response(
            user_message="Hi, my name is Johny!",
            memory_context="",
            learned_something=True
        )
        print(f"💭 Memory Response: {memory_response}")

if __name__ == "__main__":
    asyncio.run(test_llm_integration())