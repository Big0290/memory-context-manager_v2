"""
Comprehensive Function Call Logger and Data Storage System
Captures ALL function calls, inputs, outputs, and context for complete traceability
"""

import json
import asyncio
import logging
import inspect
from datetime import datetime
from typing import Any, Dict, List, Optional, Callable
from functools import wraps
from contextlib import asynccontextmanager
import hashlib
import traceback

logger = logging.getLogger(__name__)

class FunctionCallLogger:
    """
    Comprehensive function call logging and storage system
    Captures every function call with full context for cross-referencing
    """
    
    def __init__(self):
        self._database = None
        self._session_id = self._generate_session_id()
        self._call_stack: List[Dict] = []
        self._enabled = True
        
    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        timestamp = datetime.now().isoformat()
        return hashlib.md5(f"session_{timestamp}".encode()).hexdigest()[:12]
    
    def initialize(self):
        """Initialize the logger with database connection"""
        try:
            from database import get_brain_db
            self._database = get_brain_db()
            
            # Create function_calls table if it doesn't exist
            self._ensure_function_calls_table()
            
            logger.info(f"🔍 Function Call Logger initialized - Session: {self._session_id}")
            
        except Exception as e:
            logger.error(f"Failed to initialize function call logger: {e}")
            self._enabled = False
    
    def _ensure_function_calls_table(self):
        """Create function_calls table for comprehensive logging"""
        if not self._database:
            return
            
        import sqlite3
        with sqlite3.connect(self._database.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS function_calls (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    function_name TEXT NOT NULL,
                    function_type TEXT NOT NULL,
                    input_data TEXT,
                    output_data TEXT,
                    context_data TEXT,
                    execution_time_ms INTEGER,
                    success BOOLEAN,
                    error_message TEXT,
                    call_stack_depth INTEGER,
                    parent_call_id INTEGER,
                    user_message TEXT,
                    memory_context TEXT,
                    learning_info TEXT,
                    cross_references TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create indexes for fast queries
            conn.execute("CREATE INDEX IF NOT EXISTS idx_function_calls_session ON function_calls(session_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_function_calls_function_name ON function_calls(function_name)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_function_calls_timestamp ON function_calls(timestamp)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_function_calls_user_message ON function_calls(user_message)")
            
            conn.commit()
    
    def log_function_call(
        self, 
        function_name: str,
        function_type: str,
        input_data: Any = None,
        output_data: Any = None,
        context_data: Dict = None,
        execution_time_ms: int = 0,
        success: bool = True,
        error_message: str = None,
        user_message: str = None,
        memory_context: str = None,
        learning_info: List[str] = None,
        cross_references: List[str] = None
    ) -> int:
        """
        Log comprehensive function call data
        Returns call_id for cross-referencing
        """
        if not self._enabled or not self._database:
            return 0
            
        try:
            call_data = {
                "session_id": self._session_id,
                "timestamp": datetime.now().isoformat(),
                "function_name": function_name,
                "function_type": function_type,
                "input_data": self._serialize_data(input_data),
                "output_data": self._serialize_data(output_data),
                "context_data": json.dumps(context_data or {}),
                "execution_time_ms": execution_time_ms,
                "success": success,
                "error_message": error_message,
                "call_stack_depth": len(self._call_stack),
                "parent_call_id": self._call_stack[-1]["call_id"] if self._call_stack else None,
                "user_message": user_message,
                "memory_context": memory_context,
                "learning_info": json.dumps(learning_info or []),
                "cross_references": json.dumps(cross_references or [])
            }
            
            import sqlite3
            with sqlite3.connect(self._database.db_path) as conn:
                cursor = conn.execute("""
                    INSERT INTO function_calls (
                        session_id, timestamp, function_name, function_type,
                        input_data, output_data, context_data, execution_time_ms,
                        success, error_message, call_stack_depth, parent_call_id,
                        user_message, memory_context, learning_info, cross_references
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, tuple(call_data.values()))
                
                call_id = cursor.lastrowid
                conn.commit()
                
                return call_id
                
        except Exception as e:
            logger.error(f"Failed to log function call: {e}")
            return 0
    
    def _serialize_data(self, data: Any) -> str:
        """Safely serialize data to JSON"""
        try:
            if data is None:
                return ""
            
            # Handle common types
            if isinstance(data, (str, int, float, bool)):
                return json.dumps(data)
            elif isinstance(data, (list, dict)):
                return json.dumps(data, default=str)
            else:
                return str(data)[:1000]  # Truncate long strings
                
        except Exception:
            return str(data)[:1000]
    
    @asynccontextmanager
    async def track_function_call(
        self, 
        function_name: str,
        function_type: str = "unknown",
        input_data: Any = None,
        user_message: str = None,
        memory_context: str = None
    ):
        """
        Context manager to track function execution with timing
        """
        start_time = datetime.now()
        call_id = 0
        success = True
        error_message = None
        output_data = None
        
        # Add to call stack
        call_info = {
            "function_name": function_name,
            "start_time": start_time,
            "call_id": call_id
        }
        self._call_stack.append(call_info)
        
        try:
            yield call_info
            
        except Exception as e:
            success = False
            error_message = str(e)
            output_data = {"error": str(e), "traceback": traceback.format_exc()}
            raise
            
        finally:
            # Calculate execution time
            end_time = datetime.now()
            execution_time_ms = int((end_time - start_time).total_seconds() * 1000)
            
            # Log the complete function call
            call_id = self.log_function_call(
                function_name=function_name,
                function_type=function_type,
                input_data=input_data,
                output_data=output_data,
                execution_time_ms=execution_time_ms,
                success=success,
                error_message=error_message,
                user_message=user_message,
                memory_context=memory_context
            )
            
            # Update call info
            call_info["call_id"] = call_id
            
            # Remove from call stack
            if self._call_stack and self._call_stack[-1] == call_info:
                self._call_stack.pop()
    
    def get_call_history(self, limit: int = 50, function_name: str = None) -> List[Dict]:
        """Get function call history"""
        if not self._database:
            return []
            
        try:
            import sqlite3
            with sqlite3.connect(self._database.db_path) as conn:
                if function_name:
                    cursor = conn.execute("""
                        SELECT * FROM function_calls 
                        WHERE function_name = ?
                        ORDER BY timestamp DESC 
                        LIMIT ?
                    """, (function_name, limit))
                else:
                    cursor = conn.execute("""
                        SELECT * FROM function_calls 
                        ORDER BY timestamp DESC 
                        LIMIT ?
                    """, (limit,))
                
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
                
        except Exception as e:
            logger.error(f"Failed to get call history: {e}")
            return []
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Get comprehensive statistics for current session"""
        if not self._database:
            return {}
            
        try:
            import sqlite3
            with sqlite3.connect(self._database.db_path) as conn:
                # Total calls in session
                cursor = conn.execute("SELECT COUNT(*) FROM function_calls WHERE session_id = ?", (self._session_id,))
                total_calls = cursor.fetchone()[0]
                
                # Success rate
                cursor = conn.execute("SELECT COUNT(*) FROM function_calls WHERE session_id = ? AND success = 1", (self._session_id,))
                successful_calls = cursor.fetchone()[0]
                
                # Function breakdown
                cursor = conn.execute("""
                    SELECT function_name, COUNT(*) as call_count 
                    FROM function_calls 
                    WHERE session_id = ? 
                    GROUP BY function_name 
                    ORDER BY call_count DESC
                """, (self._session_id,))
                function_breakdown = dict(cursor.fetchall())
                
                # Average execution time
                cursor = conn.execute("SELECT AVG(execution_time_ms) FROM function_calls WHERE session_id = ?", (self._session_id,))
                avg_execution_time = cursor.fetchone()[0] or 0
                
                return {
                    "session_id": self._session_id,
                    "total_calls": total_calls,
                    "successful_calls": successful_calls,
                    "success_rate": successful_calls / max(total_calls, 1) * 100,
                    "function_breakdown": function_breakdown,
                    "average_execution_time_ms": round(avg_execution_time, 2),
                    "current_call_stack_depth": len(self._call_stack)
                }
                
        except Exception as e:
            logger.error(f"Failed to get session stats: {e}")
            return {"error": str(e)}
    
    def search_calls_by_context(self, search_term: str, limit: int = 20) -> List[Dict]:
        """Search function calls by context or content"""
        if not self._database:
            return []
            
        try:
            import sqlite3
            with sqlite3.connect(self._database.db_path) as conn:
                cursor = conn.execute("""
                    SELECT * FROM function_calls 
                    WHERE input_data LIKE ? 
                       OR output_data LIKE ? 
                       OR context_data LIKE ?
                       OR user_message LIKE ?
                       OR memory_context LIKE ?
                    ORDER BY timestamp DESC 
                    LIMIT ?
                """, (f"%{search_term}%",) * 5 + (limit,))
                
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
                
        except Exception as e:
            logger.error(f"Failed to search calls: {e}")
            return []

# Global function call logger instance
_global_logger: Optional[FunctionCallLogger] = None

def get_function_logger() -> FunctionCallLogger:
    """Get or create global function call logger"""
    global _global_logger
    if _global_logger is None:
        _global_logger = FunctionCallLogger()
        _global_logger.initialize()
    return _global_logger

def log_all_calls(function_type: str = "unknown"):
    """
    Decorator to automatically log all function calls
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            logger_instance = get_function_logger()
            
            # Extract user message if present
            user_message = kwargs.get('user_message') or kwargs.get('message') or kwargs.get('query')
            
            # Combine args and kwargs for input data
            input_data = {
                "args": args,
                "kwargs": kwargs
            }
            
            async with logger_instance.track_function_call(
                function_name=func.__name__,
                function_type=function_type,
                input_data=input_data,
                user_message=user_message
            ) as call_info:
                result = await func(*args, **kwargs)
                
                # Store output data
                call_info["output_data"] = result
                
                return result
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            # For sync functions, create a simple log entry
            logger_instance = get_function_logger()
            
            user_message = kwargs.get('user_message') or kwargs.get('message') or kwargs.get('query')
            input_data = {"args": args, "kwargs": kwargs}
            
            start_time = datetime.now()
            success = True
            error_message = None
            output_data = None
            
            try:
                result = func(*args, **kwargs)
                output_data = result
                return result
                
            except Exception as e:
                success = False
                error_message = str(e)
                output_data = {"error": str(e)}
                raise
                
            finally:
                end_time = datetime.now()
                execution_time_ms = int((end_time - start_time).total_seconds() * 1000)
                
                logger_instance.log_function_call(
                    function_name=func.__name__,
                    function_type=function_type,
                    input_data=input_data,
                    output_data=output_data,
                    execution_time_ms=execution_time_ms,
                    success=success,
                    error_message=error_message,
                    user_message=user_message
                )
        
        # Return appropriate wrapper based on function type
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator

def log_mcp_tool(func: Callable) -> Callable:
    """Specific decorator for MCP tools"""
    return log_all_calls("mcp_tool")(func)

def log_brain_function(func: Callable) -> Callable:
    """Specific decorator for brain functions"""
    return log_all_calls("brain_function")(func)

def log_memory_operation(func: Callable) -> Callable:
    """Specific decorator for memory operations"""
    return log_all_calls("memory_operation")(func)

def log_database_operation(func: Callable) -> Callable:
    """Specific decorator for database operations"""
    return log_all_calls("database_operation")(func)

__all__ = [
    'FunctionCallLogger', 
    'get_function_logger', 
    'log_all_calls', 
    'log_mcp_tool', 
    'log_brain_function',
    'log_memory_operation',
    'log_database_operation'
]