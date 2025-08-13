#!/usr/bin/env python3
"""
Database Performance Optimizer
Optimizes SQLite database performance and maintains system health
"""

import sqlite3
import os
import logging
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)

class DatabaseOptimizer:
    """SQLite database performance optimizer and maintenance utility"""
    
    def __init__(self, db_path: str = "brain_memory_store/brain.db"):
        self.db_path = db_path
        self.optimization_log = []
        
    def optimize_database(self) -> dict:
        """Perform comprehensive database optimization"""
        logger.info("🔧 Starting database optimization...")
        start_time = datetime.now()
        
        optimizations = {
            "vacuum": self._perform_vacuum(),
            "analyze": self._perform_analyze(),
            "reindex": self._perform_reindex(),
            "pragma_optimize": self._perform_pragma_optimize(),
            "cleanup_old_data": self._cleanup_old_data(),
            "update_statistics": self._update_table_statistics()
        }
        
        optimization_time = (datetime.now() - start_time).total_seconds()
        
        result = {
            "optimization_completed": True,
            "total_time_seconds": optimization_time,
            "optimizations": optimizations,
            "database_size_mb": self._get_database_size_mb(),
            "optimization_log": self.optimization_log,
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"✅ Database optimization completed in {optimization_time:.2f}s")
        return result
    
    def _perform_vacuum(self) -> dict:
        """Vacuum database to reclaim space and optimize structure"""
        logger.info("🧹 Running VACUUM operation...")
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("VACUUM")
                self.optimization_log.append("VACUUM completed successfully")
                return {"status": "success", "operation": "VACUUM"}
        except Exception as e:
            error_msg = f"VACUUM failed: {str(e)}"
            self.optimization_log.append(error_msg)
            logger.error(error_msg)
            return {"status": "failed", "error": str(e)}
    
    def _perform_analyze(self) -> dict:
        """Update database statistics for optimal query planning"""
        logger.info("📊 Running ANALYZE operation...")
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("ANALYZE")
                self.optimization_log.append("ANALYZE completed successfully")
                return {"status": "success", "operation": "ANALYZE"}
        except Exception as e:
            error_msg = f"ANALYZE failed: {str(e)}"
            self.optimization_log.append(error_msg)
            logger.error(error_msg)
            return {"status": "failed", "error": str(e)}
    
    def _perform_reindex(self) -> dict:
        """Rebuild all database indexes"""
        logger.info("🔧 Running REINDEX operation...")
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("REINDEX")
                self.optimization_log.append("REINDEX completed successfully")
                return {"status": "success", "operation": "REINDEX"}
        except Exception as e:
            error_msg = f"REINDEX failed: {str(e)}"
            self.optimization_log.append(error_msg)
            logger.error(error_msg)
            return {"status": "failed", "error": str(e)}
    
    def _perform_pragma_optimize(self) -> dict:
        """Run SQLite's built-in optimization"""
        logger.info("⚡ Running PRAGMA optimize...")
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("PRAGMA optimize")
                self.optimization_log.append("PRAGMA optimize completed successfully")
                return {"status": "success", "operation": "PRAGMA optimize"}
        except Exception as e:
            error_msg = f"PRAGMA optimize failed: {str(e)}"
            self.optimization_log.append(error_msg)
            logger.error(error_msg)
            return {"status": "failed", "error": str(e)}
    
    def _cleanup_old_data(self, days_to_keep: int = 30) -> dict:
        """Clean up old data to maintain performance"""
        logger.info(f"🗑️ Cleaning up data older than {days_to_keep} days...")
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        cutoff_str = cutoff_date.isoformat()
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Clean up old function calls (keep last 30 days)
                cursor.execute("""
                    DELETE FROM function_calls 
                    WHERE created_at < ? AND success = 0
                """, (cutoff_str,))
                deleted_calls = cursor.rowcount
                
                # Clean up old context enhancement pipeline entries
                cursor.execute("""
                    DELETE FROM context_enhancement_pipeline 
                    WHERE created_at < ? AND status = 'completed'
                """, (cutoff_str,))
                deleted_pipeline = cursor.rowcount
                
                conn.commit()
                
                cleanup_msg = f"Cleaned up {deleted_calls} old function calls, {deleted_pipeline} pipeline entries"
                self.optimization_log.append(cleanup_msg)
                logger.info(cleanup_msg)
                
                return {
                    "status": "success",
                    "deleted_function_calls": deleted_calls,
                    "deleted_pipeline_entries": deleted_pipeline
                }
                
        except Exception as e:
            error_msg = f"Data cleanup failed: {str(e)}"
            self.optimization_log.append(error_msg)
            logger.error(error_msg)
            return {"status": "failed", "error": str(e)}
    
    def _update_table_statistics(self) -> dict:
        """Update table statistics for monitoring"""
        logger.info("📈 Updating table statistics...")
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get table sizes
                cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name NOT LIKE 'sqlite_%'
                    ORDER BY name
                """)
                tables = cursor.fetchall()
                
                table_stats = {}
                for (table_name,) in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    count = cursor.fetchone()[0]
                    table_stats[table_name] = count
                
                self.optimization_log.append(f"Updated statistics for {len(table_stats)} tables")
                return {"status": "success", "table_statistics": table_stats}
                
        except Exception as e:
            error_msg = f"Statistics update failed: {str(e)}"
            self.optimization_log.append(error_msg)
            logger.error(error_msg)
            return {"status": "failed", "error": str(e)}
    
    def _get_database_size_mb(self) -> float:
        """Get current database size in MB"""
        try:
            size_bytes = os.path.getsize(self.db_path)
            return round(size_bytes / (1024 * 1024), 2)
        except Exception:
            return 0.0
    
    def get_performance_metrics(self) -> dict:
        """Get comprehensive database performance metrics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Database size and page info
                cursor.execute("PRAGMA page_count")
                page_count = cursor.fetchone()[0]
                cursor.execute("PRAGMA page_size")
                page_size = cursor.fetchone()[0]
                
                # Cache info
                cursor.execute("PRAGMA cache_size")
                cache_size = cursor.fetchone()[0]
                
                # Journal mode
                cursor.execute("PRAGMA journal_mode")
                journal_mode = cursor.fetchone()[0]
                
                # Table count
                cursor.execute("""
                    SELECT COUNT(*) FROM sqlite_master 
                    WHERE type='table' AND name NOT LIKE 'sqlite_%'
                """)
                table_count = cursor.fetchone()[0]
                
                # Index count
                cursor.execute("""
                    SELECT COUNT(*) FROM sqlite_master 
                    WHERE type='index' AND name NOT LIKE 'sqlite_%'
                """)
                index_count = cursor.fetchone()[0]
                
                return {
                    "database_size_mb": self._get_database_size_mb(),
                    "page_count": page_count,
                    "page_size": page_size,
                    "total_size_bytes": page_count * page_size,
                    "cache_size": cache_size,
                    "journal_mode": journal_mode,
                    "table_count": table_count,
                    "index_count": index_count,
                    "performance_status": "optimal" if self._get_database_size_mb() < 50 else "needs_attention"
                }
                
        except Exception as e:
            logger.error(f"Failed to get performance metrics: {e}")
            return {"error": str(e)}

def main():
    """Run database optimization from command line"""
    optimizer = DatabaseOptimizer()
    
    print("🔧 Memory Context Manager - Database Optimizer")
    print("=" * 50)
    
    # Get current metrics
    print("\n📊 Current Performance Metrics:")
    metrics = optimizer.get_performance_metrics()
    for key, value in metrics.items():
        print(f"  {key}: {value}")
    
    # Run optimization
    print(f"\n🚀 Starting optimization...")
    result = optimizer.optimize_database()
    
    print(f"\n✅ Optimization Results:")
    print(f"  Total time: {result['total_time_seconds']:.2f}s")
    print(f"  Database size: {result['database_size_mb']} MB")
    
    for operation, details in result['optimizations'].items():
        status = details.get('status', 'unknown')
        print(f"  {operation}: {status}")
    
    print(f"\n📋 Optimization Log:")
    for log_entry in result['optimization_log']:
        print(f"  • {log_entry}")

if __name__ == "__main__":
    main()