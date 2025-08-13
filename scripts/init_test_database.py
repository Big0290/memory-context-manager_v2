#!/usr/bin/env python3
"""
Initialize test database for GitHub Actions CI/CD pipeline.
This script creates the minimal required database structure for testing.
"""

import sqlite3
import os
import sys
from datetime import datetime

def create_test_database():
    """Create minimal test database with required tables and sample data."""
    try:
        # Ensure directory exists
        os.makedirs('brain_memory_store', exist_ok=True)
        
        # Create database connection
        db_path = 'brain_memory_store/brain.db'
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            print("🔧 Creating test database tables...")
            
            # Create minimal required tables for testing
            tables = [
                """CREATE TABLE IF NOT EXISTS memory_store (
                    key TEXT PRIMARY KEY, 
                    value TEXT, 
                    timestamp TEXT, 
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )""",
                
                """CREATE TABLE IF NOT EXISTS brain_state (
                    key TEXT PRIMARY KEY, 
                    value TEXT, 
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )""",
                
                """CREATE TABLE IF NOT EXISTS function_calls (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    session_id TEXT, 
                    timestamp TEXT, 
                    function_name TEXT, 
                    function_type TEXT, 
                    success BOOLEAN DEFAULT 1, 
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )""",
                
                """CREATE TABLE IF NOT EXISTS dream_system_metrics (
                    id INTEGER PRIMARY KEY, 
                    dream_cycles INTEGER DEFAULT 1, 
                    cross_references_processed INTEGER DEFAULT 10, 
                    relationships_enhanced INTEGER DEFAULT 5, 
                    context_injections_generated INTEGER DEFAULT 15, 
                    knowledge_synthesis_events INTEGER DEFAULT 8, 
                    memory_consolidation_cycles INTEGER DEFAULT 3, 
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )""",
                
                """CREATE TABLE IF NOT EXISTS learning_bits (
                    id INTEGER PRIMARY KEY, 
                    content TEXT, 
                    content_type TEXT, 
                    category TEXT, 
                    importance_score REAL DEFAULT 0.5, 
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )""",
                
                """CREATE TABLE IF NOT EXISTS cross_references (
                    id INTEGER PRIMARY KEY, 
                    source_bit_id INTEGER, 
                    target_bit_id INTEGER, 
                    relationship_type TEXT DEFAULT 'related', 
                    strength REAL DEFAULT 1.0, 
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )""",
                
                """CREATE TABLE IF NOT EXISTS context_enhancement_pipeline (
                    id INTEGER PRIMARY KEY, 
                    trigger_type TEXT, 
                    enhancement_type TEXT, 
                    status TEXT DEFAULT 'completed', 
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )""",
                
                """CREATE TABLE IF NOT EXISTS identity_profiles (
                    id TEXT PRIMARY KEY, 
                    name TEXT, 
                    profile_data TEXT, 
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )""",
                
                """CREATE TABLE IF NOT EXISTS memory_chunks (
                    id TEXT PRIMARY KEY, 
                    content TEXT, 
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )""",
                
                """CREATE TABLE IF NOT EXISTS conversation_memories (
                    id INTEGER PRIMARY KEY, 
                    content TEXT, 
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )"""
            ]
            
            # Create tables
            for table_sql in tables:
                cursor.execute(table_sql)
            
            print("📊 Inserting test data...")
            
            # Insert test data
            test_data = [
                """INSERT OR IGNORE INTO dream_system_metrics 
                   (dream_cycles, cross_references_processed, relationships_enhanced, 
                    context_injections_generated, knowledge_synthesis_events, memory_consolidation_cycles) 
                   VALUES (3, 30, 15, 25, 12, 8)""",
                
                """INSERT OR IGNORE INTO memory_store (key, value, timestamp) 
                   VALUES ('test_memory', 'test_value', '2024-01-01T00:00:00')""",
                
                """INSERT OR IGNORE INTO function_calls (function_name, function_type, success) 
                   VALUES ('test_function', 'test_type', 1)""",
                
                """INSERT OR IGNORE INTO learning_bits (content, content_type, category, importance_score) 
                   VALUES ('test_learning', 'concept', 'testing', 0.8)""",
                
                """INSERT OR IGNORE INTO cross_references (source_bit_id, target_bit_id, relationship_type, strength) 
                   VALUES (1, 1, 'related', 1.0)""",
                
                """INSERT OR IGNORE INTO context_enhancement_pipeline (trigger_type, enhancement_type) 
                   VALUES ('test_trigger', 'test_enhancement')"""
            ]
            
            # Insert test data
            for data_sql in test_data:
                cursor.execute(data_sql)
            
            conn.commit()
            
            # Verify database creation
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            print(f"✅ Test database initialized successfully")
            print(f"📊 Created {len(tables)} tables:")
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
                count = cursor.fetchone()[0]
                print(f"   - {table[0]}: {count} records")
            
            # Get database file size
            db_size = os.path.getsize(db_path) / 1024
            print(f"💾 Database size: {db_size:.1f}KB")
            
            return True
            
    except Exception as e:
        print(f"❌ Database initialization failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = create_test_database()
    sys.exit(0 if success else 1)