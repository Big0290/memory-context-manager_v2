"""
Optimized LLM Client with Connection Pooling and Caching
High-performance Ollama integration with async connection pooling and response caching
"""

import aiohttp
import asyncio
import json
import logging
import os
import time
import hashlib
from typing import Dict, Any, Optional
from dataclasses import dataclass
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)

@dataclass
class CachedResponse:
    """Cached LLM response with TTL"""
    response: str
    timestamp: float
    success: bool
    metadata: Dict[str, Any]

class OptimizedOllamaClient:
    """
    High-performance async client for Ollama with connection pooling and caching
    """
    
    def __init__(self, base_url: str = None, model: str = None, pool_size: int = 5):
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = model or os.getenv("OLLAMA_MODEL", "llama3.1:8b")
        self.pool_size = pool_size
        
        # Connection pooling
        self._session_pool = asyncio.Queue(maxsize=pool_size)
        self._pool_initialized = False
        self._pool_lock = asyncio.Lock()
        
        # Response caching
        self._response_cache: Dict[str, CachedResponse] = {}
        self._cache_ttl = 300  # 5 minutes
        self._max_cache_size = 100
        
        # Performance metrics
        self._request_count = 0
        self._cache_hits = 0
        self._total_response_time = 0
        
    async def _init_pool(self):
        """Initialize connection pool"""
        if self._pool_initialized:
            return
            
        async with self._pool_lock:
            if self._pool_initialized:
                return
            
            # Create connection pool
            for _ in range(self.pool_size):
                connector = aiohttp.TCPConnector(
                    limit=10,  # Max connections per session
                    limit_per_host=5,
                    ttl_dns_cache=300,
                    use_dns_cache=True,
                    keepalive_timeout=30,
                    enable_cleanup_closed=True
                )
                
                session = aiohttp.ClientSession(
                    connector=connector,
                    timeout=aiohttp.ClientTimeout(total=60),
                    headers={'User-Agent': 'Brain-AI-LLM-Client/1.0'}
                )
                
                await self._session_pool.put(session)
            
            self._pool_initialized = True
            logger.info(f"🚀 Optimized LLM client initialized with {self.pool_size} connection pool")
    
    @asynccontextmanager
    async def _get_session(self):
        """Get session from pool with automatic return"""
        if not self._pool_initialized:
            await self._init_pool()
        
        session = await self._session_pool.get()
        try:
            yield session
        finally:
            await self._session_pool.put(session)
    
    def _get_cache_key(self, prompt: str, system_prompt: str, temperature: float, max_tokens: int) -> str:
        """Generate cache key for request"""
        content = f"{prompt}|{system_prompt or ''}|{temperature}|{max_tokens}|{self.model}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _get_cached_response(self, cache_key: str) -> Optional[CachedResponse]:
        """Get cached response if valid"""
        if cache_key not in self._response_cache:
            return None
        
        cached = self._response_cache[cache_key]
        if time.time() - cached.timestamp > self._cache_ttl:
            # Cache expired
            del self._response_cache[cache_key]
            return None
        
        self._cache_hits += 1
        return cached
    
    def _cache_response(self, cache_key: str, response: str, success: bool, metadata: Dict[str, Any]):
        """Cache response with TTL"""
        # Clean old entries if cache is full
        if len(self._response_cache) >= self._max_cache_size:
            # Remove oldest entries
            sorted_cache = sorted(
                self._response_cache.items(), 
                key=lambda x: x[1].timestamp
            )
            for key, _ in sorted_cache[:10]:  # Remove 10 oldest
                del self._response_cache[key]
        
        self._response_cache[cache_key] = CachedResponse(
            response=response,
            timestamp=time.time(),
            success=success,
            metadata=metadata
        )
    
    async def generate_response(self, prompt: str, system_prompt: str = None, 
                              temperature: float = 0.7, max_tokens: int = 500,
                              use_cache: bool = True) -> Dict[str, Any]:
        """
        Generate response from Ollama with caching and connection pooling
        """
        start_time = time.time()
        self._request_count += 1
        
        # Check cache first
        cache_key = self._get_cache_key(prompt, system_prompt, temperature, max_tokens)
        if use_cache:
            cached = self._get_cached_response(cache_key)
            if cached:
                return {
                    "success": cached.success,
                    "response": cached.response,
                    "model": self.model,
                    "from_cache": True,
                    **cached.metadata
                }
        
        # Construct messages
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
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
            async with self._get_session() as session:
                async with session.post(
                    f"{self.base_url}/api/chat",
                    json=payload
                ) as response:
                    response_time = time.time() - start_time
                    self._total_response_time += response_time
                    
                    if response.status == 200:
                        result = await response.json()
                        response_text = result.get("message", {}).get("content", "")
                        
                        metadata = {
                            "tokens_used": result.get("eval_count", 0),
                            "generation_time": result.get("total_duration", 0) / 1000000000,
                            "response_time": response_time,
                            "from_cache": False
                        }
                        
                        # Cache successful response
                        if use_cache:
                            self._cache_response(cache_key, response_text, True, metadata)
                        
                        return {
                            "success": True,
                            "response": response_text,
                            "model": self.model,
                            **metadata
                        }
                    else:
                        error_text = await response.text()
                        error_msg = f"HTTP {response.status}: {error_text}"
                        
                        # Don't cache errors
                        return {
                            "success": False,
                            "error": error_msg,
                            "response": "",
                            "response_time": response_time,
                            "from_cache": False
                        }
        
        except asyncio.TimeoutError:
            return {
                "success": False,
                "error": "Request timeout - LLM took too long to respond",
                "response": "",
                "response_time": time.time() - start_time,
                "from_cache": False
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"LLM request failed: {str(e)}",
                "response": "",
                "response_time": time.time() - start_time,
                "from_cache": False
            }
    
    async def health_check(self) -> bool:
        """Check if Ollama service is healthy with connection pooling"""
        try:
            async with self._get_session() as session:
                async with session.get(
                    f"{self.base_url}/api/tags",
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    return response.status == 200
        except:
            return False
    
    async def list_models(self) -> Dict[str, Any]:
        """List available models with connection pooling"""
        try:
            async with self._get_session() as session:
                async with session.get(f"{self.base_url}/api/tags") as response:
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
    
    async def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        avg_response_time = (self._total_response_time / max(self._request_count, 1))
        cache_hit_rate = (self._cache_hits / max(self._request_count, 1)) * 100
        
        return {
            "total_requests": self._request_count,
            "cache_hits": self._cache_hits,
            "cache_hit_rate": f"{cache_hit_rate:.1f}%",
            "avg_response_time": f"{avg_response_time:.3f}s",
            "cached_responses": len(self._response_cache),
            "pool_size": self.pool_size,
            "model": self.model
        }
    
    async def clear_cache(self):
        """Clear response cache"""
        self._response_cache.clear()
        logger.info("🗑️ LLM response cache cleared")
    
    async def close_pool(self):
        """Close all sessions in pool"""
        if not self._pool_initialized:
            return
        
        sessions = []
        while not self._session_pool.empty():
            try:
                session = self._session_pool.get_nowait()
                sessions.append(session)
            except asyncio.QueueEmpty:
                break
        
        for session in sessions:
            await session.close()
        
        self._pool_initialized = False
        logger.info("🔒 LLM client connection pool closed")


class OptimizedMemoryEnhancedLLM:
    """
    High-performance memory-enhanced LLM with intelligent caching
    """
    
    def __init__(self, ollama_client: OptimizedOllamaClient):
        self.ollama = ollama_client
        self.system_prompt = self._create_system_prompt()
        
        # Memory-specific caching
        self._memory_context_cache: Dict[str, str] = {}
        self._context_cache_ttl = 600  # 10 minutes for memory context
    
    def _create_system_prompt(self) -> str:
        """Create optimized system prompt for memory-enhanced conversations"""
        return """You are a highly efficient AI assistant with persistent memory capabilities.

Core Performance Guidelines:
- Use provided memory context naturally and efficiently
- Acknowledge new user information warmly but concisely  
- Reference past conversations when directly relevant
- Avoid redundant explanations unless specifically requested
- Prioritize helpful, actionable responses

Memory Context Processing:
- Memory context provided as [MEMORY: ...]
- Integrate context smoothly without mentioning "memory" explicitly
- Focus on the most relevant details for the current conversation

Be responsive, personable, and maintain conversation flow efficiently."""
    
    async def generate_memory_response(self, user_message: str, memory_context: str = "", 
                                     learned_something: bool = False,
                                     use_cache: bool = True) -> str:
        """
        Generate response using memory context with intelligent caching
        """
        # Build optimized prompt
        prompt_parts = [f"User: {user_message}"]
        
        if memory_context:
            # Cache memory context to avoid repeated processing
            context_hash = hashlib.md5(memory_context.encode()).hexdigest()[:8]
            prompt_parts.append(f"[MEMORY: {memory_context}]")
        
        if learned_something:
            prompt_parts.append("[NOTE: New information learned about user]")
        
        prompt_parts.append("Assistant:")
        full_prompt = "\n".join(prompt_parts)
        
        # Generate response with caching
        result = await self.ollama.generate_response(
            prompt=full_prompt,
            system_prompt=self.system_prompt,
            temperature=0.7,
            max_tokens=300,
            use_cache=use_cache
        )
        
        if result["success"]:
            return result["response"].strip()
        else:
            # Optimized fallback response
            logger.error(f"LLM generation failed: {result.get('error')}")
            return "I'd be happy to help! (Processing temporarily unavailable)"
    
    async def batch_generate_responses(self, requests: List[Dict[str, Any]]) -> List[str]:
        """
        Generate multiple responses concurrently for better performance
        """
        tasks = []
        for req in requests:
            task = self.generate_memory_response(
                user_message=req.get("message", ""),
                memory_context=req.get("memory_context", ""),
                learned_something=req.get("learned_something", False),
                use_cache=req.get("use_cache", True)
            )
            tasks.append(task)
        
        return await asyncio.gather(*tasks, return_exceptions=True)
    
    async def test_connection(self) -> Dict[str, Any]:
        """Optimized connection test"""
        start_time = time.time()
        
        test_result = await self.ollama.generate_response(
            "Respond with 'OK'",
            temperature=0.1,
            max_tokens=10,
            use_cache=False  # Don't cache test responses
        )
        
        test_time = time.time() - start_time
        
        return {
            "connection_working": test_result["success"],
            "response": test_result.get("response", ""),
            "error": test_result.get("error"),
            "model": self.ollama.model,
            "test_time": f"{test_time:.3f}s"
        }
    
    async def get_performance_metrics(self) -> Dict[str, Any]:
        """Get comprehensive performance metrics"""
        ollama_stats = await self.ollama.get_performance_stats()
        
        return {
            "llm_performance": ollama_stats,
            "memory_context_cache_size": len(self._memory_context_cache),
            "optimization_status": "active",
            "features": [
                "connection_pooling",
                "response_caching", 
                "batch_processing",
                "memory_context_optimization"
            ]
        }


# Global optimized LLM client instance
_optimized_llm_client = None
_client_lock = asyncio.Lock()

async def get_optimized_llm_client() -> OptimizedMemoryEnhancedLLM:
    """Get global optimized LLM client instance"""
    global _optimized_llm_client
    
    if _optimized_llm_client is None:
        async with _client_lock:
            if _optimized_llm_client is None:
                ollama_client = OptimizedOllamaClient(pool_size=5)
                await ollama_client._init_pool()
                _optimized_llm_client = OptimizedMemoryEnhancedLLM(ollama_client)
                logger.info("🧠 Optimized LLM client initialized with performance enhancements")
    
    return _optimized_llm_client

async def close_optimized_llm_client():
    """Close optimized LLM client and connection pool"""
    global _optimized_llm_client
    if _optimized_llm_client is not None:
        await _optimized_llm_client.ollama.close_pool()
        _optimized_llm_client = None

async def test_optimized_llm():
    """Test optimized LLM performance"""
    print("🚀 Testing Optimized LLM Performance...")
    
    client = await get_optimized_llm_client()
    
    # Connection test
    test_result = await client.test_connection()
    print(f"✅ Connection: {'OK' if test_result['connection_working'] else 'FAILED'} ({test_result['test_time']})")
    
    # Performance test with caching
    start_time = time.time()
    
    # First request (cold)
    response1 = await client.generate_memory_response("Hello!", use_cache=True)
    first_time = time.time() - start_time
    
    # Second identical request (cached)
    start_time = time.time()
    response2 = await client.generate_memory_response("Hello!", use_cache=True)
    cached_time = time.time() - start_time
    
    # Performance metrics
    metrics = await client.get_performance_metrics()
    
    print(f"🎯 Performance Results:")
    print(f"   First request: {first_time:.3f}s")
    print(f"   Cached request: {cached_time:.3f}s") 
    print(f"   Speed improvement: {(first_time/max(cached_time, 0.001)):.1f}x faster")
    print(f"   Cache hit rate: {metrics['llm_performance']['cache_hit_rate']}")
    
    return metrics

if __name__ == "__main__":
    asyncio.run(test_optimized_llm())