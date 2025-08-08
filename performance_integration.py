"""
Performance Integration Layer
Gracefully integrates performance optimizations with fallback to existing systems
"""

import asyncio
import logging
import time
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

class PerformanceIntegration:
    """
    Integrates performance optimizations with graceful fallbacks
    """
    
    def __init__(self):
        # Component availability flags
        self.async_db_available = False
        self.optimized_llm_available = False
        self.memory_cache_available = False
        
        # Component instances
        self._async_db = None
        self._optimized_llm = None
        self._memory_cache = None
        self._sync_db = None  # Fallback to sync database
        
        # Performance tracking
        self._performance_enabled = False
        self._metrics = {
            'requests_served': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'fallback_used': 0
        }
        
        logger.info("⚡ Performance integration layer initialized")
    
    async def initialize_optimizations(self):
        """
        Initialize performance components with graceful fallbacks
        """
        logger.info("🚀 Initializing performance optimizations...")
        
        # Try to initialize async database
        try:
            from database.async_brain_db import get_async_brain_db
            self._async_db = await get_async_brain_db()
            self.async_db_available = True
            logger.info("✅ Async database enabled")
        except Exception as e:
            logger.warning(f"⚠️ Async database unavailable, using fallback: {e}")
            try:
                from database import get_brain_db
                self._sync_db = get_brain_db()
                logger.info("✅ Fallback sync database enabled")
            except Exception as sync_e:
                logger.error(f"❌ Database fallback failed: {sync_e}")
        
        # Try to initialize optimized LLM
        try:
            from llm_client_optimized import get_optimized_llm_client
            self._optimized_llm = await get_optimized_llm_client()
            self.optimized_llm_available = True
            logger.info("✅ Optimized LLM client enabled")
        except Exception as e:
            logger.warning(f"⚠️ Optimized LLM unavailable, will use fallback: {e}")
        
        # Try to initialize memory cache
        try:
            from performance.memory_cache import get_memory_caches
            self._memory_cache = await get_memory_caches()
            self.memory_cache_available = True
            logger.info("✅ Memory caching enabled")
        except Exception as e:
            logger.warning(f"⚠️ Memory cache unavailable: {e}")
        
        # Enable performance tracking if any optimization is available
        self._performance_enabled = (
            self.async_db_available or 
            self.optimized_llm_available or 
            self.memory_cache_available
        )
        
        if self._performance_enabled:
            logger.info("🎯 Performance optimizations active")
        else:
            logger.info("📊 Running in compatibility mode with standard performance")
        
        return {
            'async_db': self.async_db_available,
            'optimized_llm': self.optimized_llm_available,
            'memory_cache': self.memory_cache_available,
            'performance_enabled': self._performance_enabled
        }
    
    async def get_user_context_optimized(self, user_id: str, fallback_func=None) -> Optional[Dict[str, Any]]:
        """Get user context with performance optimizations and fallback"""
        start_time = time.time()
        
        try:
            # Try cache first if available
            if self.memory_cache_available and self._memory_cache:
                cached_context = await self._memory_cache.get_user_context(user_id)
                if cached_context:
                    self._metrics['cache_hits'] += 1
                    logger.debug(f"🎯 User context cache hit for {user_id}")
                    return cached_context
                else:
                    self._metrics['cache_misses'] += 1
            
            # Try async database if available
            if self.async_db_available and self._async_db:
                try:
                    # Search for user-related memories
                    memories = await self._async_db.search_memory_store(user_id, limit=5)
                    
                    # Get identity profiles
                    profiles = await self._async_db.get_identity_profiles()
                    user_profile = None
                    for identity in profiles.get("identities", []):
                        if identity.get("name", "").lower() == user_id.lower():
                            user_profile = identity
                            break
                    
                    context = {
                        "user_id": user_id,
                        "memories": memories,
                        "profile": user_profile,
                        "timestamp": time.time(),
                        "source": "async_db"
                    }
                    
                    # Cache if available
                    if self.memory_cache_available and self._memory_cache:
                        await self._memory_cache.cache_user_context(user_id, context)
                    
                    return context
                    
                except Exception as e:
                    logger.warning(f"Async database failed, trying fallback: {e}")
            
            # Try sync database fallback
            if self._sync_db:
                try:
                    memories = self._sync_db.search_memory_store(user_id, limit=5)
                    profiles = self._sync_db.get_identity_profiles()
                    
                    user_profile = None
                    for identity in profiles.get("identities", []):
                        if identity.get("name", "").lower() == user_id.lower():
                            user_profile = identity
                            break
                    
                    context = {
                        "user_id": user_id,
                        "memories": memories,
                        "profile": user_profile,
                        "timestamp": time.time(),
                        "source": "sync_db_fallback"
                    }
                    
                    self._metrics['fallback_used'] += 1
                    return context
                    
                except Exception as e:
                    logger.error(f"Sync database fallback failed: {e}")
            
            # Final fallback to provided function
            if fallback_func:
                self._metrics['fallback_used'] += 1
                return await fallback_func(user_id) if asyncio.iscoroutinefunction(fallback_func) else fallback_func(user_id)
            
            return None
            
        except Exception as e:
            logger.error(f"User context retrieval failed: {e}")
            return None
        
        finally:
            self._metrics['requests_served'] += 1
            elapsed = time.time() - start_time
            if elapsed > 1.0:
                logger.warning(f"⚠️ Slow user context retrieval: {elapsed:.3f}s")
    
    async def generate_response_optimized(self, user_message: str, memory_context: str = "", 
                                        learned_something: bool = False, fallback_func=None) -> str:
        """Generate LLM response with optimizations and fallback"""
        start_time = time.time()
        
        try:
            # Try optimized LLM client
            if self.optimized_llm_available and self._optimized_llm:
                try:
                    response = await self._optimized_llm.generate_memory_response(
                        user_message=user_message,
                        memory_context=memory_context,
                        learned_something=learned_something,
                        use_cache=True
                    )
                    return response
                except Exception as e:
                    logger.warning(f"Optimized LLM failed, trying fallback: {e}")
            
            # Fallback to provided function
            if fallback_func:
                self._metrics['fallback_used'] += 1
                return await fallback_func(user_message, memory_context, learned_something) if asyncio.iscoroutinefunction(fallback_func) else fallback_func(user_message, memory_context, learned_something)
            
            # Final fallback response
            return f"I understand you said: {user_message}. I'm processing this with standard capabilities."
            
        except Exception as e:
            logger.error(f"Response generation failed: {e}")
            return "I'd be happy to help, but I'm experiencing some technical difficulties."
        
        finally:
            self._metrics['requests_served'] += 1
            elapsed = time.time() - start_time
            if elapsed > 3.0:
                logger.warning(f"⚠️ Slow response generation: {elapsed:.3f}s")
    
    async def store_memory_optimized(self, key: str, value: str, tags: List[str] = None,
                                   emotional_weight: str = "medium", fallback_func=None) -> bool:
        """Store memory with optimizations and fallback"""
        try:
            # Try async database
            if self.async_db_available and self._async_db:
                try:
                    success = await self._async_db.set_memory_item(key, value, tags, emotional_weight)
                    if success and self.memory_cache_available and self._memory_cache:
                        # Invalidate related caches
                        if tags:
                            for tag in tags:
                                if tag.startswith("user:"):
                                    user_id = tag[5:]
                                    await self._memory_cache.invalidate_user_data(user_id)
                    return success
                except Exception as e:
                    logger.warning(f"Async database store failed, trying fallback: {e}")
            
            # Try sync database fallback
            if self._sync_db:
                try:
                    success = self._sync_db.set_memory_item(key, value, tags, emotional_weight)
                    self._metrics['fallback_used'] += 1
                    return success
                except Exception as e:
                    logger.error(f"Sync database fallback failed: {e}")
            
            # Fallback to provided function
            if fallback_func:
                self._metrics['fallback_used'] += 1
                return await fallback_func(key, value, tags, emotional_weight) if asyncio.iscoroutinefunction(fallback_func) else fallback_func(key, value, tags, emotional_weight)
            
            return False
            
        except Exception as e:
            logger.error(f"Memory storage failed: {e}")
            return False
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        cache_hit_rate = 0
        if (self._metrics['cache_hits'] + self._metrics['cache_misses']) > 0:
            cache_hit_rate = (self._metrics['cache_hits'] / (self._metrics['cache_hits'] + self._metrics['cache_misses'])) * 100
        
        return {
            "performance_enabled": self._performance_enabled,
            "optimizations_active": {
                "async_database": self.async_db_available,
                "optimized_llm": self.optimized_llm_available,
                "memory_cache": self.memory_cache_available
            },
            "metrics": {
                "requests_served": self._metrics['requests_served'],
                "cache_hit_rate": f"{cache_hit_rate:.1f}%",
                "fallback_usage": self._metrics['fallback_used'],
                "fallback_rate": f"{(self._metrics['fallback_used'] / max(self._metrics['requests_served'], 1)) * 100:.1f}%"
            }
        }
    
    async def health_check(self) -> Dict[str, str]:
        """Check health of performance components"""
        health = {
            "integration_layer": "healthy",
            "async_database": "not_available",
            "optimized_llm": "not_available", 
            "memory_cache": "not_available"
        }
        
        # Check async database
        if self.async_db_available and self._async_db:
            try:
                await self._async_db.get_brain_state()
                health["async_database"] = "healthy"
            except:
                health["async_database"] = "unhealthy"
        
        # Check optimized LLM
        if self.optimized_llm_available and self._optimized_llm:
            try:
                test_result = await self._optimized_llm.test_connection()
                health["optimized_llm"] = "healthy" if test_result.get("connection_working") else "unhealthy"
            except:
                health["optimized_llm"] = "unhealthy"
        
        # Check memory cache
        if self.memory_cache_available and self._memory_cache:
            try:
                stats = self._memory_cache.get_all_stats()
                health["memory_cache"] = "healthy"
            except:
                health["memory_cache"] = "unhealthy"
        
        return health

# Global performance integration instance
_global_performance = None

async def get_performance_integration() -> PerformanceIntegration:
    """Get global performance integration instance"""
    global _global_performance
    
    if _global_performance is None:
        _global_performance = PerformanceIntegration()
        await _global_performance.initialize_optimizations()
        logger.info("⚡ Global performance integration ready")
    
    return _global_performance

async def test_performance_integration():
    """Test performance integration with fallbacks"""
    print("⚡ Testing Performance Integration:")
    
    perf = await get_performance_integration()
    
    # Test initialization status
    stats = perf.get_performance_stats()
    print(f"✅ Performance enabled: {stats['performance_enabled']}")
    print(f"✅ Active optimizations: {list(k for k, v in stats['optimizations_active'].items() if v)}")
    
    # Test user context with fallback
    context = await perf.get_user_context_optimized("test_user")
    print(f"✅ User context retrieval: {'Success' if context else 'Failed'}")
    if context:
        print(f"   Source: {context.get('source', 'unknown')}")
    
    # Test memory storage
    success = await perf.store_memory_optimized("perf_test", "Performance test memory", ["test"])
    print(f"✅ Memory storage: {'Success' if success else 'Failed'}")
    
    # Test health check
    health = await perf.health_check()
    print(f"✅ Health check: {health}")
    
    # Final stats
    final_stats = perf.get_performance_stats()
    print(f"✅ Final metrics: {final_stats['metrics']}")
    
    return perf

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_performance_integration())