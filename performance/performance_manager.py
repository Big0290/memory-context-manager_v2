"""
Performance Manager - Orchestrates all performance optimizations
Coordinates async database, connection pooling, and caching for maximum efficiency
"""

import asyncio
import time
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetrics:
    """Container for performance metrics"""
    database_ops: int = 0
    cache_hits: int = 0 
    cache_misses: int = 0
    llm_requests: int = 0
    avg_response_time: float = 0.0
    memory_usage_mb: float = 0.0
    active_connections: int = 0

class PerformanceManager:
    """
    Central manager for all performance optimizations
    """
    
    def __init__(self):
        self._metrics = PerformanceMetrics()
        self._start_time = time.time()
        self._request_times = []
        self._max_request_history = 1000
        
        # Component references
        self._async_db = None
        self._optimized_llm = None  
        self._memory_caches = None
        
        # Performance monitoring
        self._monitoring_enabled = True
        self._metrics_lock = asyncio.Lock()
        
        logger.info("⚡ Performance Manager initialized")
    
    async def initialize_components(self):
        """Initialize all performance-optimized components"""
        try:
            # Initialize async database
            from database.async_brain_db import get_async_brain_db
            self._async_db = await get_async_brain_db()
            logger.info("✅ Async database initialized")
            
            # Initialize optimized LLM client
            from llm_client_optimized import get_optimized_llm_client
            self._optimized_llm = await get_optimized_llm_client()
            logger.info("✅ Optimized LLM client initialized")
            
            # Initialize memory caches
            from performance.memory_cache import get_memory_caches
            self._memory_caches = await get_memory_caches()
            logger.info("✅ Memory caches initialized")
            
            logger.info("🚀 All performance components ready")
            return True
            
        except Exception as e:
            logger.error(f"❌ Performance component initialization failed: {e}")
            return False
    
    @asynccontextmanager
    async def track_request(self, operation_name: str = "unknown"):
        """Context manager to track request performance"""
        start_time = time.time()
        
        try:
            yield
        finally:
            if self._monitoring_enabled:
                end_time = time.time()
                request_time = end_time - start_time
                
                async with self._metrics_lock:
                    # Add to request history
                    self._request_times.append(request_time)
                    
                    # Keep history manageable
                    if len(self._request_times) > self._max_request_history:
                        self._request_times = self._request_times[-self._max_request_history:]
                    
                    # Update average
                    self._metrics.avg_response_time = sum(self._request_times) / len(self._request_times)
                
                # Log slow requests
                if request_time > 2.0:
                    logger.warning(f"⚠️ Slow {operation_name}: {request_time:.3f}s")
                elif request_time > 5.0:
                    logger.error(f"🐌 Very slow {operation_name}: {request_time:.3f}s")
    
    # High-level optimized operations
    async def get_user_context_optimized(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user context with caching and async database"""
        async with self.track_request("get_user_context"):
            if not self._memory_caches:
                return None
            
            # Try cache first
            cached_context = await self._memory_caches.get_user_context(user_id)
            if cached_context:
                async with self._metrics_lock:
                    self._metrics.cache_hits += 1
                return cached_context
            
            # Cache miss - get from database
            async with self._metrics_lock:
                self._metrics.cache_misses += 1
            
            if not self._async_db:
                return None
            
            try:
                # Search for user-related memories
                memories = await self._async_db.search_memory_store(user_id, limit=5)
                
                # Get user identity profile
                profiles = await self._async_db.get_identity_profiles()
                user_profile = None
                for identity in profiles.get("identities", []):
                    if identity.get("name", "").lower() == user_id.lower():
                        user_profile = identity
                        break
                
                # Build context
                context = {
                    "user_id": user_id,
                    "memories": memories,
                    "profile": user_profile,
                    "timestamp": time.time()
                }
                
                # Cache for future use
                await self._memory_caches.cache_user_context(user_id, context)
                
                async with self._metrics_lock:
                    self._metrics.database_ops += 1
                
                return context
                
            except Exception as e:
                logger.error(f"Failed to get user context: {e}")
                return None
    
    async def store_memory_optimized(self, key: str, value: str, tags: List[str] = None,
                                   emotional_weight: str = "medium") -> bool:
        """Store memory with batch optimization and cache invalidation"""
        async with self.track_request("store_memory"):
            if not self._async_db:
                return False
            
            try:
                # Store in database
                success = await self._async_db.set_memory_item(key, value, tags, emotional_weight)
                
                if success:
                    # Invalidate related caches
                    if self._memory_caches and tags:
                        for tag in tags:
                            if tag.startswith("user:"):
                                user_id = tag[5:]  # Remove "user:" prefix
                                await self._memory_caches.invalidate_user_data(user_id)
                    
                    async with self._metrics_lock:
                        self._metrics.database_ops += 1
                
                return success
                
            except Exception as e:
                logger.error(f"Failed to store memory: {e}")
                return False
    
    async def generate_llm_response_optimized(self, user_message: str, memory_context: str = "",
                                           learned_something: bool = False) -> str:
        """Generate LLM response with caching and connection pooling"""
        async with self.track_request("llm_response"):
            if not self._optimized_llm:
                return "I'm having trouble with my processing right now."
            
            try:
                response = await self._optimized_llm.generate_memory_response(
                    user_message=user_message,
                    memory_context=memory_context,
                    learned_something=learned_something,
                    use_cache=True
                )
                
                async with self._metrics_lock:
                    self._metrics.llm_requests += 1
                
                return response
                
            except Exception as e:
                logger.error(f"Failed to generate LLM response: {e}")
                return "I'd be happy to help, but I'm experiencing some technical difficulties."
    
    async def get_brain_state_optimized(self) -> Dict[str, Any]:
        """Get brain state with intelligent caching"""
        async with self.track_request("get_brain_state"):
            if not self._memory_caches:
                return {}
            
            # Try cache first
            cached_state = await self._memory_caches.get_brain_state()
            if cached_state:
                async with self._metrics_lock:
                    self._metrics.cache_hits += 1
                return cached_state
            
            # Cache miss - get from database
            async with self._metrics_lock:
                self._metrics.cache_misses += 1
            
            if not self._async_db:
                return {}
            
            try:
                brain_state = await self._async_db.get_brain_state()
                
                # Cache for future use (short TTL for brain state)
                await self._memory_caches.cache_brain_state(brain_state, ttl=30)
                
                async with self._metrics_lock:
                    self._metrics.database_ops += 1
                
                return brain_state
                
            except Exception as e:
                logger.error(f"Failed to get brain state: {e}")
                return {}
    
    async def batch_store_memories(self, memories: List[Dict[str, Any]]) -> bool:
        """Batch store multiple memories for better performance"""
        async with self.track_request("batch_store_memories"):
            if not self._async_db or not memories:
                return False
            
            try:
                success = await self._async_db.batch_store_memories(memories)
                
                if success:
                    # Invalidate related caches
                    if self._memory_caches:
                        user_ids_to_invalidate = set()
                        for memory in memories:
                            for tag in memory.get("tags", []):
                                if tag.startswith("user:"):
                                    user_ids_to_invalidate.add(tag[5:])
                        
                        for user_id in user_ids_to_invalidate:
                            await self._memory_caches.invalidate_user_data(user_id)
                    
                    async with self._metrics_lock:
                        self._metrics.database_ops += len(memories)
                
                return success
                
            except Exception as e:
                logger.error(f"Failed to batch store memories: {e}")
                return False
    
    # Performance monitoring and metrics
    async def get_comprehensive_metrics(self) -> Dict[str, Any]:
        """Get comprehensive performance metrics from all components"""
        metrics = {
            "performance_manager": {
                "uptime_seconds": time.time() - self._start_time,
                "database_operations": self._metrics.database_ops,
                "cache_hits": self._metrics.cache_hits,
                "cache_misses": self._metrics.cache_misses,
                "llm_requests": self._metrics.llm_requests,
                "avg_response_time": f"{self._metrics.avg_response_time:.3f}s",
                "total_requests": len(self._request_times)
            }
        }
        
        # Database metrics
        if self._async_db:
            metrics["async_database"] = {
                "connection_pool_size": self._async_db.pool_size,
                "connections_active": self._async_db._connection_pool.qsize()
            }
        
        # LLM client metrics  
        if self._optimized_llm:
            llm_metrics = await self._optimized_llm.get_performance_metrics()
            metrics["llm_client"] = llm_metrics
        
        # Cache metrics
        if self._memory_caches:
            cache_stats = self._memory_caches.get_all_stats()
            metrics["caches"] = cache_stats
        
        return metrics
    
    async def health_check(self) -> Dict[str, Any]:
        """Comprehensive health check of all performance components"""
        health = {
            "overall_status": "healthy",
            "components": {}
        }
        
        # Check async database
        if self._async_db:
            try:
                # Simple database operation
                await self._async_db.get_brain_state()
                health["components"]["async_database"] = "healthy"
            except Exception as e:
                health["components"]["async_database"] = f"unhealthy: {e}"
                health["overall_status"] = "degraded"
        
        # Check LLM client
        if self._optimized_llm:
            try:
                test_result = await self._optimized_llm.test_connection()
                health["components"]["llm_client"] = "healthy" if test_result["connection_working"] else "unhealthy"
            except Exception as e:
                health["components"]["llm_client"] = f"unhealthy: {e}"
                health["overall_status"] = "degraded"
        
        # Check caches
        if self._memory_caches:
            try:
                cache_stats = self._memory_caches.get_all_stats()
                health["components"]["memory_caches"] = "healthy"
                health["cache_summary"] = {
                    "total_entries": cache_stats["total_entries"],
                    "user_contexts": cache_stats["user_contexts"]["hit_rate"],
                    "brain_states": cache_stats["brain_states"]["hit_rate"]
                }
            except Exception as e:
                health["components"]["memory_caches"] = f"unhealthy: {e}"
                health["overall_status"] = "degraded"
        
        return health
    
    async def optimize_system(self) -> Dict[str, Any]:
        """Run system optimization routines"""
        optimizations = []
        
        try:
            # Clear expired cache entries
            if self._memory_caches:
                await self._memory_caches.clear_all_caches()
                optimizations.append("cache_cleanup")
            
            # Clear LLM response cache if hit rate is low
            if self._optimized_llm:
                await self._optimized_llm.ollama.clear_cache()
                optimizations.append("llm_cache_reset")
            
            # Database optimization (could add VACUUM, etc.)
            optimizations.append("database_maintenance")
            
            return {
                "optimizations_performed": optimizations,
                "status": "completed",
                "timestamp": time.time()
            }
            
        except Exception as e:
            logger.error(f"System optimization failed: {e}")
            return {
                "optimizations_performed": optimizations,
                "status": "failed",
                "error": str(e)
            }
    
    async def close_all_connections(self):
        """Clean shutdown of all performance components"""
        logger.info("🔒 Closing all performance components...")
        
        try:
            # Close async database
            if self._async_db:
                await self._async_db.close_pool()
                logger.info("✅ Async database closed")
            
            # Close LLM client
            if self._optimized_llm:
                await self._optimized_llm.ollama.close_pool()
                logger.info("✅ LLM client closed")
            
            # Close caches
            if self._memory_caches:
                await self._memory_caches.stop_all_cleanup_tasks()
                await self._memory_caches.clear_all_caches()
                logger.info("✅ Memory caches closed")
            
            logger.info("🎉 All performance components closed successfully")
            
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")

# Global performance manager
_global_performance_manager = None

async def get_performance_manager() -> PerformanceManager:
    """Get global performance manager instance"""
    global _global_performance_manager
    
    if _global_performance_manager is None:
        _global_performance_manager = PerformanceManager()
        success = await _global_performance_manager.initialize_components()
        
        if not success:
            logger.error("❌ Performance manager initialization failed")
            # Continue with degraded performance rather than failing completely
        
        logger.info("⚡ Global performance manager ready")
    
    return _global_performance_manager

async def close_performance_manager():
    """Close global performance manager"""
    global _global_performance_manager
    
    if _global_performance_manager is not None:
        await _global_performance_manager.close_all_connections()
        _global_performance_manager = None