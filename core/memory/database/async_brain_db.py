"""
Async Brain Memory Database Adapter
High-performance async SQLite operations for brain memory system with connection pooling
"""

import aiosqlite
import asyncio
import json
import os
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional, AsyncContextManager
from pathlib import Path
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)

class AsyncBrainDatabase:
    """High-performance async SQLite-based storage for brain memory system"""
    
    def __init__(self, db_path: str = "brain_memory_store/brain.db", pool_size: int = 10):
        """Initialize async database with connection pooling"""
        self.db_path = db_path
        self.pool_size = pool_size
        self._connection_pool = asyncio.Queue(maxsize=pool_size)
        self._pool_initialized = False
        self._lock = asyncio.Lock()
        
        # Ensure directory exists
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    
    async def _init_pool(self):
        """Initialize connection pool"""
        if self._pool_initialized:
            return
        
        async with self._lock:
            if self._pool_initialized:
                return
            
            # Create initial connections
            for _ in range(self.pool_size):
                conn = await aiosqlite.connect(self.db_path)
                await conn.execute("PRAGMA journal_mode=WAL")
                await conn.execute("PRAGMA synchronous=NORMAL") 
                await conn.execute("PRAGMA cache_size=10000")
                await conn.execute("PRAGMA temp_store=memory")
                await self._connection_pool.put(conn)
            
            # Initialize database schema
            await self._init_database()
            self._pool_initialized = True
            logger.info(f"🚀 Async Brain Database initialized with {self.pool_size} connections at {self.db_path}")
    
    @asynccontextmanager
    async def _get_connection(self) -> AsyncContextManager[aiosqlite.Connection]:
        """Get connection from pool with automatic return"""
        if not self._pool_initialized:
            await self._init_pool()
        
        conn = await self._connection_pool.get()
        try:
            yield conn
        finally:
            await self._connection_pool.put(conn)
    
    async def _init_database(self):
        """Create database tables if they don't exist"""
        async with self._get_connection() as conn:
            # Memory store table (replaces memory_store.json)
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS memory_store (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    tags TEXT, -- JSON array of tags
                    emotional_weight TEXT DEFAULT 'medium',
                    context_type TEXT DEFAULT 'general',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Context history table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS context_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    context_data TEXT, -- JSON blob
                    timestamp TEXT,
                    interaction_type TEXT DEFAULT 'conversation',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Brain state table (replaces brain_state.json)
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS brain_state (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL, -- JSON blob for complex values
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Identity profiles table (replaces identities.json)
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS identity_profiles (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    description TEXT,
                    profile_data TEXT, -- JSON blob for full profile
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_active TIMESTAMP,
                    total_interactions INTEGER DEFAULT 0
                )
            """)
            
            # Memory chunks table (for brain cognitive system)
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS memory_chunks (
                    id TEXT PRIMARY KEY,
                    content TEXT NOT NULL,
                    context_type TEXT,
                    emotional_weight TEXT,
                    metadata TEXT, -- JSON blob
                    associations TEXT, -- JSON array of related chunk IDs
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    access_count INTEGER DEFAULT 0,
                    last_accessed TIMESTAMP
                )
            """)
            
            # Conversation memories (for conversation plugin)
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS conversation_memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_message TEXT,
                    ai_response TEXT,
                    context_data TEXT, -- JSON blob
                    emotional_analysis TEXT, -- JSON blob
                    importance_score REAL DEFAULT 0.5,
                    session_id TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Performance indexes
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_memory_store_timestamp ON memory_store(timestamp)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_memory_store_emotional ON memory_store(emotional_weight, updated_at)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_memory_store_context ON memory_store(context_type)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_memory_chunks_context ON memory_chunks(context_type)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_memory_chunks_emotional ON memory_chunks(emotional_weight)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_conversation_session ON conversation_memories(session_id)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_context_history_session ON context_history(session_id)")
            
            # Full-text search for content
            await conn.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts USING fts5(
                    key, value, tags, content='memory_store'
                )
            """)
            
            await conn.commit()
            logger.info("🗄️ Async database schema initialized with performance indexes")
    
    async def close_pool(self):
        """Close all connections in pool"""
        if not self._pool_initialized:
            return
        
        connections = []
        while not self._connection_pool.empty():
            try:
                conn = self._connection_pool.get_nowait()
                connections.append(conn)
            except asyncio.QueueEmpty:
                break
        
        for conn in connections:
            await conn.close()
        
        self._pool_initialized = False
        logger.info("🔒 Async database connection pool closed")
    
    # Memory Store Interface (JSON compatibility)
    async def get_memory_store(self) -> Dict[str, Any]:
        """Get all memory store data (compatible with JSON format)"""
        async with self._get_connection() as conn:
            async with conn.execute("""
                SELECT key, value, timestamp, tags FROM memory_store 
                ORDER BY updated_at DESC
            """) as cursor:
                memory_store = {}
                async for row in cursor:
                    key, value, timestamp, tags = row
                    memory_store[key] = {
                        "value": value,
                        "timestamp": timestamp,
                        "tags": json.loads(tags) if tags else []
                    }
                
                return {
                    "memory_store": memory_store,
                    "context_history": await self._get_recent_context_history(),
                    "last_updated": datetime.now().isoformat()
                }
    
    async def set_memory_item(self, key: str, value: str, tags: List[str] = None, 
                       emotional_weight: str = "medium") -> bool:
        """Store memory item (compatible with JSON format)"""
        try:
            async with self._get_connection() as conn:
                await conn.execute("""
                    INSERT OR REPLACE INTO memory_store 
                    (key, value, timestamp, tags, emotional_weight, updated_at)
                    VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                """, (
                    key, 
                    value, 
                    datetime.now().isoformat(),
                    json.dumps(tags or []),
                    emotional_weight
                ))
                
                # Update FTS index
                await conn.execute("""
                    INSERT OR REPLACE INTO memory_fts (key, value, tags)
                    VALUES (?, ?, ?)
                """, (key, value, json.dumps(tags or [])))
                
                await conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to store memory item {key}: {e}")
            return False
    
    async def search_memory_store(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search memory store for relevant items using FTS"""
        async with self._get_connection() as conn:
            # Try FTS first for better performance
            try:
                async with conn.execute("""
                    SELECT m.key, m.value, m.timestamp, m.tags, m.emotional_weight
                    FROM memory_store m
                    JOIN memory_fts f ON m.key = f.key
                    WHERE memory_fts MATCH ?
                    ORDER BY 
                        CASE m.emotional_weight 
                            WHEN 'critical' THEN 4
                            WHEN 'high' THEN 3  
                            WHEN 'medium' THEN 2
                            ELSE 1
                        END DESC,
                        m.updated_at DESC
                    LIMIT ?
                """, (query, limit)) as cursor:
                    results = []
                    async for row in cursor:
                        key, value, timestamp, tags, weight = row
                        results.append({
                            "key": key,
                            "value": value,
                            "timestamp": timestamp,
                            "tags": json.loads(tags) if tags else [],
                            "emotional_weight": weight
                        })
                    
                    if results:
                        return results
            except Exception:
                pass  # Fall back to LIKE search
            
            # Fallback to LIKE search
            async with conn.execute("""
                SELECT key, value, timestamp, tags, emotional_weight
                FROM memory_store 
                WHERE value LIKE ? OR key LIKE ?
                ORDER BY 
                    CASE emotional_weight 
                        WHEN 'critical' THEN 4
                        WHEN 'high' THEN 3  
                        WHEN 'medium' THEN 2
                        ELSE 1
                    END DESC,
                    updated_at DESC
                LIMIT ?
            """, (f"%{query}%", f"%{query}%", limit)) as cursor:
                results = []
                async for row in cursor:
                    key, value, timestamp, tags, weight = row
                    results.append({
                        "key": key,
                        "value": value,
                        "timestamp": timestamp,
                        "tags": json.loads(tags) if tags else [],
                        "emotional_weight": weight
                    })
                
                return results
    
    # Brain State Interface with caching
    _brain_state_cache = None
    _cache_timestamp = None
    _cache_ttl = 30  # seconds
    
    async def get_brain_state(self) -> Dict[str, Any]:
        """Get current brain state with caching"""
        now = datetime.now().timestamp()
        
        # Return cached if valid
        if (self._brain_state_cache and self._cache_timestamp and 
            now - self._cache_timestamp < self._cache_ttl):
            return self._brain_state_cache.copy()
        
        async with self._get_connection() as conn:
            brain_state = {}
            async with conn.execute("SELECT key, value FROM brain_state") as cursor:
                async for key, value in cursor:
                    try:
                        brain_state[key] = json.loads(value)
                    except:
                        brain_state[key] = value
            
            # Provide defaults for expected fields
            defaults = {
                "active_task_id": None,
                "active_identity": "default",
                "current_focus": None,
                "current_session_id": "server_session",
                "session_start_time": datetime.now().isoformat(),
                "frontal_activity": 0.5,
                "memory_activity": 0.5,
                "emotion_activity": 0.5,
                "last_reflection": None,
                "memory_consolidation_needed": False,
                "debug_mode": False,
                "thought_trace": []
            }
            
            for key, default_value in defaults.items():
                if key not in brain_state:
                    brain_state[key] = default_value
            
            # Cache the result
            self._brain_state_cache = brain_state.copy()
            self._cache_timestamp = now
            
            return brain_state
    
    async def update_brain_state(self, updates: Dict[str, Any]) -> bool:
        """Update brain state items"""
        try:
            async with self._get_connection() as conn:
                # Batch updates in single transaction
                for key, value in updates.items():
                    json_value = json.dumps(value) if isinstance(value, (dict, list)) else str(value)
                    await conn.execute("""
                        INSERT OR REPLACE INTO brain_state (key, value, updated_at)
                        VALUES (?, ?, CURRENT_TIMESTAMP)
                    """, (key, json_value))
                
                await conn.commit()
                
                # Invalidate cache
                self._cache_timestamp = None
                self._brain_state_cache = None
            
            return True
        except Exception as e:
            logger.error(f"Failed to update brain state: {e}")
            return False
    
    async def _get_recent_context_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent context history"""
        async with self._get_connection() as conn:
            async with conn.execute("""
                SELECT context_data, timestamp, interaction_type 
                FROM context_history 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (limit,)) as cursor:
                history = []
                async for context_data, timestamp, interaction_type in cursor:
                    try:
                        context = json.loads(context_data) if context_data else {}
                        context.update({
                            "timestamp": timestamp,
                            "type": interaction_type
                        })
                        history.append(context)
                    except:
                        continue
                
                return history
    
    # Additional optimized methods for high-frequency operations
    async def batch_store_memories(self, memories: List[Dict[str, Any]]) -> bool:
        """Batch store multiple memories in single transaction"""
        try:
            async with self._get_connection() as conn:
                for memory in memories:
                    await conn.execute("""
                        INSERT OR REPLACE INTO memory_store 
                        (key, value, timestamp, tags, emotional_weight, updated_at)
                        VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                    """, (
                        memory['key'],
                        memory['value'],
                        datetime.now().isoformat(),
                        json.dumps(memory.get('tags', [])),
                        memory.get('emotional_weight', 'medium')
                    ))
                
                await conn.commit()
            return True
        except Exception as e:
            logger.error(f"Batch memory storage failed: {e}")
            return False

# Global async database instance
_async_brain_db = None

async def get_async_brain_db() -> AsyncBrainDatabase:
    """Get global async brain database instance"""
    global _async_brain_db
    if _async_brain_db is None:
        db_path = os.getenv("BRAIN_DB_PATH", "brain_memory_store/brain.db")
        _async_brain_db = AsyncBrainDatabase(db_path)
        await _async_brain_db._init_pool()
    return _async_brain_db

async def close_async_brain_db():
    """Close async database connection pool"""
    global _async_brain_db
    if _async_brain_db is not None:
        await _async_brain_db.close_pool()
        _async_brain_db = None