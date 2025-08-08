"""
Brain Memory Database Adapter
Provides persistent SQLite storage while maintaining compatibility with existing JSON-based systems
"""

import sqlite3
import json
import os
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class BrainDatabase:
    """SQLite-based persistent storage for brain memory system"""
    
    def __init__(self, db_path: str = "brain_memory_store/brain.db"):
        """Initialize database connection and create tables if needed"""
        self.db_path = db_path
        
        # Ensure directory exists
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize database
        self._init_database()
        logger.info(f"🗄️ Brain Database initialized at {db_path}")
    
    def _init_database(self):
        """Create database tables if they don't exist"""
        with sqlite3.connect(self.db_path) as conn:
            # Memory store table (replaces memory_store.json)
            conn.execute("""
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
            conn.execute("""
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
            conn.execute("""
                CREATE TABLE IF NOT EXISTS brain_state (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL, -- JSON blob for complex values
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Identity profiles table (replaces identities.json)
            conn.execute("""
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
            conn.execute("""
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
            conn.execute("""
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
            
            # Create indexes for better performance
            conn.execute("CREATE INDEX IF NOT EXISTS idx_memory_store_timestamp ON memory_store(timestamp)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_memory_chunks_context ON memory_chunks(context_type)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_conversation_session ON conversation_memories(session_id)")
            
            conn.commit()
            logger.info("🗄️ Database schema initialized successfully")
    
    # Memory Store Interface (JSON compatibility)
    def get_memory_store(self) -> Dict[str, Any]:
        """Get all memory store data (compatible with JSON format)"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT key, value, timestamp, tags FROM memory_store 
                ORDER BY updated_at DESC
            """)
            
            memory_store = {}
            for key, value, timestamp, tags in cursor.fetchall():
                memory_store[key] = {
                    "value": value,
                    "timestamp": timestamp,
                    "tags": json.loads(tags) if tags else []
                }
            
            return {
                "memory_store": memory_store,
                "context_history": self._get_recent_context_history(),
                "last_updated": datetime.now().isoformat()
            }
    
    def set_memory_item(self, key: str, value: str, tags: List[str] = None, 
                       emotional_weight: str = "medium") -> bool:
        """Store memory item (compatible with JSON format)"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
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
                conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to store memory item {key}: {e}")
            return False
    
    def search_memory_store(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search memory store for relevant items"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
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
            """, (f"%{query}%", f"%{query}%", limit))
            
            results = []
            for key, value, timestamp, tags, weight in cursor.fetchall():
                results.append({
                    "key": key,
                    "value": value,
                    "timestamp": timestamp,
                    "tags": json.loads(tags) if tags else [],
                    "emotional_weight": weight
                })
            
            return results
    
    # Brain State Interface
    def get_brain_state(self) -> Dict[str, Any]:
        """Get current brain state (compatible with JSON format)"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT key, value FROM brain_state")
            brain_state = {}
            
            for key, value in cursor.fetchall():
                try:
                    # Try to parse JSON, fallback to string
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
            
            # Merge defaults with stored data
            for key, default_value in defaults.items():
                if key not in brain_state:
                    brain_state[key] = default_value
            
            return brain_state
    
    def update_brain_state(self, updates: Dict[str, Any]) -> bool:
        """Update brain state items"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                for key, value in updates.items():
                    # Convert complex objects to JSON
                    json_value = json.dumps(value) if isinstance(value, (dict, list)) else str(value)
                    
                    conn.execute("""
                        INSERT OR REPLACE INTO brain_state (key, value, updated_at)
                        VALUES (?, ?, CURRENT_TIMESTAMP)
                    """, (key, json_value))
                
                conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to update brain state: {e}")
            return False
    
    # Context History Interface
    def _get_recent_context_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent context history"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT context_data, timestamp, interaction_type 
                FROM context_history 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (limit,))
            
            history = []
            for context_data, timestamp, interaction_type in cursor.fetchall():
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
    
    def add_context_history(self, context_data: Dict[str, Any], 
                           interaction_type: str = "conversation") -> bool:
        """Add entry to context history"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO context_history 
                    (session_id, context_data, timestamp, interaction_type)
                    VALUES (?, ?, ?, ?)
                """, (
                    context_data.get("session_id", "default"),
                    json.dumps(context_data),
                    datetime.now().isoformat(),
                    interaction_type
                ))
                conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to add context history: {e}")
            return False
    
    # Identity Profiles Interface
    def get_identity_profiles(self) -> Dict[str, Any]:
        """Get all identity profiles (compatible with JSON format)"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT id, name, description, profile_data, created_at, last_active, total_interactions
                FROM identity_profiles
                ORDER BY last_active DESC
            """)
            
            identities = []
            for row in cursor.fetchall():
                identity_data = json.loads(row[3]) if row[3] else {}
                identity_data.update({
                    "id": row[0],
                    "name": row[1],
                    "description": row[2],
                    "created_at": row[4],
                    "last_active": row[5],
                    "total_interactions": row[6]
                })
                identities.append(identity_data)
            
            return {
                "identities": identities,
                "last_updated": datetime.now().isoformat()
            }
    
    def update_identity_profile(self, identity_id: str, profile_data: Dict[str, Any]) -> bool:
        """Update or create identity profile"""
        try:
            # Convert datetime objects to strings for JSON serialization
            clean_data = {}
            for key, value in profile_data.items():
                if hasattr(value, 'isoformat'):  # datetime object
                    clean_data[key] = value.isoformat()
                else:
                    clean_data[key] = value
            
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO identity_profiles 
                    (id, name, description, profile_data, last_active, total_interactions)
                    VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, 
                           COALESCE((SELECT total_interactions FROM identity_profiles WHERE id = ?), 0) + 1)
                """, (
                    identity_id,
                    clean_data.get("name", "Unknown"),
                    clean_data.get("description", ""),
                    json.dumps(clean_data, default=str),
                    identity_id
                ))
                conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to update identity profile {identity_id}: {e}")
            return False
    
    # Advanced Memory Functions
    def store_memory_chunk(self, chunk_id: str, content: str, context_type: str = "general",
                          emotional_weight: str = "medium", metadata: Dict[str, Any] = None) -> bool:
        """Store memory chunk for brain cognitive system"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO memory_chunks 
                    (id, content, context_type, emotional_weight, metadata, created_at)
                    VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                """, (
                    chunk_id,
                    content,
                    context_type,
                    emotional_weight,
                    json.dumps(metadata or {})
                ))
                conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to store memory chunk {chunk_id}: {e}")
            return False
    
    def search_memory_chunks(self, query: str, context_type: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Search memory chunks with optional context filtering"""
        conditions = ["content LIKE ?"]
        params = [f"%{query}%"]
        
        if context_type:
            conditions.append("context_type = ?")
            params.append(context_type)
        
        params.append(limit)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(f"""
                SELECT id, content, context_type, emotional_weight, metadata, created_at
                FROM memory_chunks 
                WHERE {' AND '.join(conditions)}
                ORDER BY 
                    CASE emotional_weight 
                        WHEN 'critical' THEN 4
                        WHEN 'high' THEN 3
                        WHEN 'medium' THEN 2  
                        ELSE 1
                    END DESC,
                    created_at DESC
                LIMIT ?
            """, params)
            
            chunks = []
            for row in cursor.fetchall():
                chunks.append({
                    "id": row[0],
                    "content": row[1],
                    "context_type": row[2],
                    "emotional_weight": row[3],
                    "metadata": json.loads(row[4]) if row[4] else {},
                    "created_at": row[5]
                })
            
            return chunks
    
    def store_conversation(self, user_message: str, ai_response: str, context: Dict[str, Any] = None,
                          session_id: str = "default", importance: float = 0.5) -> bool:
        """Store conversation for memory system"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO conversation_memories 
                    (user_message, ai_response, context_data, importance_score, session_id)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    user_message,
                    ai_response,
                    json.dumps(context or {}),
                    importance,
                    session_id
                ))
                conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to store conversation: {e}")
            return False
    
    def get_conversation_history(self, session_id: str = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Get conversation history"""
        conditions = []
        params = []
        
        if session_id:
            conditions.append("session_id = ?")
            params.append(session_id)
        
        params.append(limit)
        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(f"""
                SELECT user_message, ai_response, context_data, importance_score, session_id, created_at
                FROM conversation_memories 
                {where_clause}
                ORDER BY created_at DESC
                LIMIT ?
            """, params)
            
            conversations = []
            for row in cursor.fetchall():
                conversations.append({
                    "user_message": row[0],
                    "ai_response": row[1], 
                    "context": json.loads(row[2]) if row[2] else {},
                    "importance": row[3],
                    "session_id": row[4],
                    "timestamp": row[5]
                })
            
            return conversations
    
    def cleanup_old_data(self, days_to_keep: int = 30) -> Dict[str, int]:
        """Clean up old data to prevent database bloat"""
        cutoff_date = datetime.now().timestamp() - (days_to_keep * 24 * 60 * 60)
        
        with sqlite3.connect(self.db_path) as conn:
            # Clean old context history
            cursor = conn.execute("""
                DELETE FROM context_history 
                WHERE created_at < datetime(?, 'unixepoch')
            """, (cutoff_date,))
            context_deleted = cursor.rowcount
            
            # Clean old conversation memories (keep important ones)
            cursor = conn.execute("""
                DELETE FROM conversation_memories 
                WHERE created_at < datetime(?, 'unixepoch') 
                AND importance_score < 0.7
            """, (cutoff_date,))
            conversations_deleted = cursor.rowcount
            
            conn.commit()
        
        return {
            "context_entries_deleted": context_deleted,
            "conversations_deleted": conversations_deleted
        }

# Global database instance
_brain_db = None

def get_brain_db() -> BrainDatabase:
    """Get global brain database instance"""
    global _brain_db
    if _brain_db is None:
        db_path = os.getenv("BRAIN_DB_PATH", "brain_memory_store/brain.db")
        _brain_db = BrainDatabase(db_path)
    return _brain_db