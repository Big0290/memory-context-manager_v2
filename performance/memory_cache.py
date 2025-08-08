"""
High-Performance Memory Context Caching System
Intelligent caching for user contexts, conversation history, and brain states
"""

import asyncio
import time
import json
import hashlib
import logging
from typing import Dict, Any, Optional, List, Set
from dataclasses import dataclass, field
from collections import OrderedDict
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)

@dataclass
class CacheEntry:
    """Cache entry with metadata"""
    key: str
    data: Any
    timestamp: float
    access_count: int = 0
    ttl: float = 300  # 5 minutes default
    tags: Set[str] = field(default_factory=set)
    size_bytes: int = 0

    def __post_init__(self):
        if isinstance(self.data, (dict, list)):
            self.size_bytes = len(json.dumps(self.data).encode('utf-8'))
        else:
            self.size_bytes = len(str(self.data).encode('utf-8'))
    
    def is_expired(self) -> bool:
        """Check if cache entry has expired"""
        return time.time() - self.timestamp > self.ttl
    
    def touch(self):
        """Update access count and timestamp"""
        self.access_count += 1
        # Don't update timestamp on access to preserve TTL

class MemoryContextCache:
    """
    High-performance memory context cache with intelligent eviction
    """
    
    def __init__(self, max_size: int = 1000, max_memory_mb: int = 100):
        self.max_size = max_size
        self.max_memory_bytes = max_memory_mb * 1024 * 1024
        
        # Main cache storage (LRU-like)
        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self._size_bytes = 0
        self._hits = 0
        self._misses = 0
        
        # Tag-based indexing for bulk operations
        self._tag_index: Dict[str, Set[str]] = {}
        
        # Async locks
        self._lock = asyncio.Lock()  # Use regular lock for compatibility
        
        # Background cleanup task
        self._cleanup_task = None
        self._cleanup_interval = 60  # seconds
        
        logger.info(f"🧠 Memory cache initialized: {max_size} entries, {max_memory_mb}MB")
    
    async def start_background_cleanup(self):
        """Start background cleanup task"""
        if self._cleanup_task is None:
            self._cleanup_task = asyncio.create_task(self._background_cleanup())
            logger.info("🗑️ Background cache cleanup started")
    
    async def stop_background_cleanup(self):
        """Stop background cleanup task"""
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass
            self._cleanup_task = None
            logger.info("🛑 Background cache cleanup stopped")
    
    async def _background_cleanup(self):
        """Background task to clean expired entries"""
        while True:
            try:
                await asyncio.sleep(self._cleanup_interval)
                cleaned = await self._cleanup_expired()
                if cleaned > 0:
                    logger.debug(f"🧹 Background cleanup: removed {cleaned} expired entries")
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Background cleanup error: {e}")
    
    def _generate_key(self, *args, **kwargs) -> str:
        """Generate cache key from arguments"""
        content = json.dumps([args, sorted(kwargs.items())], sort_keys=True)
        return hashlib.md5(content.encode()).hexdigest()
    
    async def get(self, key: str) -> Optional[Any]:
        """Get cached value by key"""
        async with self._lock:
            if key in self._cache:
                entry = self._cache[key]
                
                if entry.is_expired():
                    await self._remove_entry(key)
                    self._misses += 1
                    return None
                
                # Move to end (LRU)
                self._cache.move_to_end(key)
                entry.touch()
                self._hits += 1
                return entry.data
            
            self._misses += 1
            return None
    
    async def set(self, key: str, data: Any, ttl: float = 300, tags: Set[str] = None) -> bool:
        """Set cached value with TTL and tags"""
        async with self._lock:
            # Create entry
            entry = CacheEntry(
                key=key,
                data=data,
                timestamp=time.time(),
                ttl=ttl,
                tags=tags or set()
            )
            
            # Check memory limits
            if self._size_bytes + entry.size_bytes > self.max_memory_bytes:
                await self._evict_lru(entry.size_bytes)
            
            # Remove old entry if exists
            if key in self._cache:
                await self._remove_entry(key)
            
            # Add new entry
            self._cache[key] = entry
            self._size_bytes += entry.size_bytes
            
            # Update tag index
            for tag in entry.tags:
                if tag not in self._tag_index:
                    self._tag_index[tag] = set()
                self._tag_index[tag].add(key)
            
            # Check size limits
            if len(self._cache) > self.max_size:
                await self._evict_lru(0)
            
            return True
    
    async def _remove_entry(self, key: str):
        """Remove entry and update indexes"""
        if key not in self._cache:
            return
        
        entry = self._cache[key]
        
        # Update size
        self._size_bytes -= entry.size_bytes
        
        # Update tag index
        for tag in entry.tags:
            if tag in self._tag_index:
                self._tag_index[tag].discard(key)
                if not self._tag_index[tag]:
                    del self._tag_index[tag]
        
        # Remove from cache
        del self._cache[key]
    
    async def _evict_lru(self, needed_bytes: int):
        """Evict least recently used entries"""
        evicted = 0
        freed_bytes = 0
        
        # Evict from the beginning (oldest)
        keys_to_remove = []
        for key in list(self._cache.keys()):
            if (needed_bytes == 0 and len(self._cache) <= self.max_size) or \
               (needed_bytes > 0 and freed_bytes >= needed_bytes):
                break
            
            keys_to_remove.append(key)
            freed_bytes += self._cache[key].size_bytes
            evicted += 1
        
        for key in keys_to_remove:
            await self._remove_entry(key)
        
        if evicted > 0:
            logger.debug(f"🗑️ Evicted {evicted} LRU entries, freed {freed_bytes} bytes")
    
    async def _cleanup_expired(self) -> int:
        """Clean up expired entries"""
        async with self._lock:
            expired_keys = [
                key for key, entry in self._cache.items() 
                if entry.is_expired()
            ]
            
            for key in expired_keys:
                await self._remove_entry(key)
            
            return len(expired_keys)
    
    async def delete(self, key: str) -> bool:
        """Delete cached value by key"""
        async with self._lock:
            if key in self._cache:
                await self._remove_entry(key)
                return True
            return False
    
    async def delete_by_tags(self, tags: Set[str]) -> int:
        """Delete all entries with any of the specified tags"""
        async with self._lock:
            keys_to_delete = set()
            
            for tag in tags:
                if tag in self._tag_index:
                    keys_to_delete.update(self._tag_index[tag])
            
            for key in keys_to_delete:
                await self._remove_entry(key)
            
            return len(keys_to_delete)
    
    async def clear(self):
        """Clear all cache entries"""
        async with self._lock:
            self._cache.clear()
            self._tag_index.clear()
            self._size_bytes = 0
            logger.info("🗑️ Memory cache cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache performance statistics"""
        total_requests = self._hits + self._misses
        hit_rate = (self._hits / max(total_requests, 1)) * 100
        
        return {
            "entries": len(self._cache),
            "size_mb": round(self._size_bytes / (1024 * 1024), 2),
            "max_size": self.max_size,
            "max_memory_mb": self.max_memory_bytes // (1024 * 1024),
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": f"{hit_rate:.1f}%",
            "tags": len(self._tag_index),
            "memory_usage": f"{(self._size_bytes / self.max_memory_bytes) * 100:.1f}%"
        }

class SpecializedCaches:
    """
    Specialized caches for different types of brain memory data
    """
    
    def __init__(self):
        # Different caches for different data types with optimized settings
        self.user_contexts = MemoryContextCache(max_size=200, max_memory_mb=20)  # Smaller, longer TTL
        self.brain_states = MemoryContextCache(max_size=50, max_memory_mb=5)     # Very small, fast access
        self.conversation_history = MemoryContextCache(max_size=500, max_memory_mb=50)  # Large, medium TTL
        self.llm_responses = MemoryContextCache(max_size=300, max_memory_mb=30)  # Medium, short TTL
        
        # Start background cleanup for all caches
        self._cleanup_tasks = []
    
    async def start_all_cleanup_tasks(self):
        """Start background cleanup for all caches"""
        caches = [self.user_contexts, self.brain_states, self.conversation_history, self.llm_responses]
        for cache in caches:
            await cache.start_background_cleanup()
        logger.info("🚀 All specialized cache cleanup tasks started")
    
    async def stop_all_cleanup_tasks(self):
        """Stop all background cleanup tasks"""
        caches = [self.user_contexts, self.brain_states, self.conversation_history, self.llm_responses]
        for cache in caches:
            await cache.stop_background_cleanup()
        logger.info("🛑 All specialized cache cleanup tasks stopped")
    
    # User Context Cache Methods
    async def cache_user_context(self, user_id: str, context: Dict[str, Any], ttl: float = 600):
        """Cache user context with 10-minute TTL"""
        await self.user_contexts.set(f"user:{user_id}", context, ttl=ttl, tags={"user_context", user_id})
    
    async def get_user_context(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get cached user context"""
        return await self.user_contexts.get(f"user:{user_id}")
    
    # Brain State Cache Methods  
    async def cache_brain_state(self, state: Dict[str, Any], ttl: float = 30):
        """Cache brain state with 30-second TTL"""
        await self.brain_states.set("current_brain_state", state, ttl=ttl, tags={"brain_state"})
    
    async def get_brain_state(self) -> Optional[Dict[str, Any]]:
        """Get cached brain state"""
        return await self.brain_states.get("current_brain_state")
    
    # Conversation History Cache Methods
    async def cache_conversation_history(self, session_id: str, history: List[Dict[str, Any]], ttl: float = 900):
        """Cache conversation history with 15-minute TTL"""
        await self.conversation_history.set(f"conv:{session_id}", history, ttl=ttl, 
                                          tags={"conversation", session_id})
    
    async def get_conversation_history(self, session_id: str) -> Optional[List[Dict[str, Any]]]:
        """Get cached conversation history"""
        return await self.conversation_history.get(f"conv:{session_id}")
    
    # LLM Response Cache Methods
    async def cache_llm_response(self, prompt_hash: str, response: str, ttl: float = 300):
        """Cache LLM response with 5-minute TTL"""
        await self.llm_responses.set(f"llm:{prompt_hash}", response, ttl=ttl, tags={"llm_response"})
    
    async def get_llm_response(self, prompt_hash: str) -> Optional[str]:
        """Get cached LLM response"""
        return await self.llm_responses.get(f"llm:{prompt_hash}")
    
    # Bulk Operations
    async def invalidate_user_data(self, user_id: str):
        """Invalidate all cached data for a user"""
        await self.user_contexts.delete_by_tags({user_id})
        await self.conversation_history.delete_by_tags({user_id})
    
    async def clear_all_caches(self):
        """Clear all specialized caches"""
        await asyncio.gather(
            self.user_contexts.clear(),
            self.brain_states.clear(),
            self.conversation_history.clear(),
            self.llm_responses.clear()
        )
        logger.info("🧹 All specialized caches cleared")
    
    def get_all_stats(self) -> Dict[str, Any]:
        """Get statistics for all caches"""
        return {
            "user_contexts": self.user_contexts.get_stats(),
            "brain_states": self.brain_states.get_stats(),
            "conversation_history": self.conversation_history.get_stats(),
            "llm_responses": self.llm_responses.get_stats(),
            "total_entries": (
                len(self.user_contexts._cache) + 
                len(self.brain_states._cache) +
                len(self.conversation_history._cache) + 
                len(self.llm_responses._cache)
            )
        }

# Global cache instance
_global_caches = None

async def get_memory_caches() -> SpecializedCaches:
    """Get global memory caches instance"""
    global _global_caches
    if _global_caches is None:
        _global_caches = SpecializedCaches()
        await _global_caches.start_all_cleanup_tasks()
        logger.info("🧠 Global memory caches initialized")
    return _global_caches

async def close_memory_caches():
    """Close all memory caches"""
    global _global_caches
    if _global_caches is not None:
        await _global_caches.stop_all_cleanup_tasks()
        await _global_caches.clear_all_caches()
        _global_caches = None
        logger.info("🔒 Memory caches closed")

# Context managers for cache operations
@asynccontextmanager
async def cached_operation(cache_key: str, ttl: float = 300, tags: Set[str] = None):
    """Context manager for cached operations"""
    caches = await get_memory_caches()
    
    # Try to get from cache first
    cached_result = await caches.user_contexts.get(cache_key)
    if cached_result is not None:
        yield cached_result, True  # (result, from_cache)
        return
    
    # Provide a setter function for caching results
    async def set_result(result):
        await caches.user_contexts.set(cache_key, result, ttl=ttl, tags=tags)
        return result
    
    yield set_result, False  # (setter_function, from_cache)