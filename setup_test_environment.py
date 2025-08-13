#!/usr/bin/env python3
"""
Test Environment Setup for Memory Context Manager v2
Prepares the system for integration testing by installing dependencies and creating minimal test data
"""

import subprocess
import sys
import os
import sqlite3
from pathlib import Path
from datetime import datetime

def install_missing_packages():
    """Install required packages for testing"""
    required_packages = [
        "psutil>=5.9.0",
        "aiohttp>=3.9.0", 
        "aiosqlite>=0.21.0",
        "requests>=2.31.0",
        "beautifulsoup4>=4.11.0",
        "pydantic>=2.0.0"
    ]
    
    print("📦 Installing required packages for testing...")
    
    for package in required_packages:
        try:
            package_name = package.split(">=")[0]
            __import__(package_name.replace("-", "_"))
            print(f"✅ {package_name} already installed")
        except ImportError:
            print(f"⬇️ Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"])
            print(f"✅ {package} installed")

def create_test_database():
    """Create a minimal test database with required structure"""
    db_path = "brain_memory_store/brain.db"
    
    # Ensure directory exists
    os.makedirs("brain_memory_store", exist_ok=True)
    
    print(f"🗄️ Creating test database: {db_path}")
    
    with sqlite3.connect(db_path) as conn:
        # Create all required tables with minimal structure
        tables = [
            """CREATE TABLE IF NOT EXISTS memory_store (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                tags TEXT,
                emotional_weight TEXT DEFAULT 'medium',
                context_type TEXT DEFAULT 'general',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",
            """CREATE TABLE IF NOT EXISTS brain_state (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",
            """CREATE TABLE IF NOT EXISTS function_calls (
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
            )""",
            """CREATE TABLE IF NOT EXISTS dream_system_metrics (
                id INTEGER PRIMARY KEY,
                dream_cycles INTEGER DEFAULT 0,
                cross_references_processed INTEGER DEFAULT 0,
                relationships_enhanced INTEGER DEFAULT 0,
                context_injections_generated INTEGER DEFAULT 0,
                knowledge_synthesis_events INTEGER DEFAULT 0,
                memory_consolidation_cycles INTEGER DEFAULT 0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",
            """CREATE TABLE IF NOT EXISTS learning_bits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                content_type TEXT,
                category TEXT,
                importance_score REAL DEFAULT 0.5,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",
            """CREATE TABLE IF NOT EXISTS cross_references (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_bit_id INTEGER,
                target_bit_id INTEGER,
                relationship_type TEXT DEFAULT 'related',
                strength REAL DEFAULT 1.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",
            """CREATE TABLE IF NOT EXISTS context_enhancement_pipeline (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trigger_type TEXT,
                source_id INTEGER,
                target_id INTEGER,
                relationship_type TEXT,
                enhancement_type TEXT,
                status TEXT DEFAULT 'pending',
                priority INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",
            """CREATE TABLE IF NOT EXISTS identity_profiles (
                id TEXT PRIMARY KEY,
                name TEXT,
                description TEXT,
                profile_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP,
                total_interactions INTEGER DEFAULT 0
            )""",
            """CREATE TABLE IF NOT EXISTS memory_chunks (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                context_type TEXT,
                emotional_weight TEXT,
                metadata TEXT,
                associations TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                access_count INTEGER DEFAULT 0,
                last_accessed TIMESTAMP
            )""",
            """CREATE TABLE IF NOT EXISTS conversation_memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                context TEXT,
                emotional_tone TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )"""
        ]
        
        for table_sql in tables:
            conn.execute(table_sql)
        
        # Insert test data
        test_data = [
            # Dream system metrics
            """INSERT OR REPLACE INTO dream_system_metrics 
            (id, dream_cycles, cross_references_processed, relationships_enhanced, 
             context_injections_generated, knowledge_synthesis_events, memory_consolidation_cycles)
            VALUES (1, 3, 30, 15, 25, 12, 8)""",
            
            # Memory store
            """INSERT OR IGNORE INTO memory_store 
            (key, value, timestamp, tags, emotional_weight) VALUES 
            ('test_memory_1', 'Test memory content 1', '2024-01-01T00:00:00', '["test", "memory"]', 'high'),
            ('test_memory_2', 'Test memory content 2', '2024-01-02T00:00:00', '["test", "system"]', 'medium')""",
            
            # Function calls
            """INSERT OR IGNORE INTO function_calls 
            (session_id, timestamp, function_name, function_type, success, execution_time_ms) VALUES 
            ('test_session', '2024-01-01T00:00:00', 'test_function_1', 'brain_function', 1, 100),
            ('test_session', '2024-01-01T00:01:00', 'test_function_2', 'plugin_tool', 1, 150),
            ('test_session', '2024-01-01T00:02:00', 'test_function_3', 'mcp_tool', 0, 200)""",
            
            # Learning bits
            """INSERT OR IGNORE INTO learning_bits 
            (content, content_type, category, importance_score) VALUES 
            ('Test learning content 1', 'concept', 'testing', 0.8),
            ('Test learning content 2', 'definition', 'system', 0.9),
            ('Test learning content 3', 'example', 'integration', 0.7)""",
            
            # Cross references
            """INSERT OR IGNORE INTO cross_references 
            (source_bit_id, target_bit_id, relationship_type, strength) VALUES 
            (1, 2, 'related', 1.0),
            (2, 3, 'depends_on', 0.8),
            (1, 3, 'similar', 0.6)""",
            
            # Context enhancement pipeline
            """INSERT OR IGNORE INTO context_enhancement_pipeline 
            (trigger_type, enhancement_type, status, priority) VALUES 
            ('dream_consolidation', 'memory_consolidation', 'completed', 3),
            ('context_optimization', 'cross_reference_generation', 'completed', 1),
            ('knowledge_synthesis', 'insight_generation', 'pending', 2)""",
            
            # Identity profiles
            """INSERT OR IGNORE INTO identity_profiles 
            (id, name, description, profile_data, total_interactions) VALUES 
            ('test_user', 'Test User', 'Test user profile', '{"preferences": ["testing"]}', 5)""",
            
            # Memory chunks
            """INSERT OR IGNORE INTO memory_chunks 
            (id, content, context_type, emotional_weight, access_count) VALUES 
            ('chunk_1', 'Test memory chunk 1', 'conversation', 'medium', 3),
            ('chunk_2', 'Test memory chunk 2', 'system', 'low', 1)""",
            
            # Conversation memories
            """INSERT OR IGNORE INTO conversation_memories 
            (content, context, emotional_tone) VALUES 
            ('Test conversation 1', 'integration_testing', 'neutral')"""
        ]
        
        for data_sql in test_data:
            conn.execute(data_sql)
        
        conn.commit()
        
    print("✅ Test database created successfully")
    
    # Verify data
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM function_calls")
        function_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM learning_bits")  
        learning_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM cross_references")
        cross_ref_count = cursor.fetchone()[0]
        
        print(f"📊 Test data created: {function_count} function calls, {learning_count} learning bits, {cross_ref_count} cross-references")

def setup_mock_mcp():
    """Create a mock MCP module for testing"""
    print("🔧 Setting up mock MCP module...")
    
    mock_mcp_content = '''"""
Mock MCP module for testing purposes
Provides minimal interface compatibility for tests
"""

class FastMCP:
    """Mock FastMCP server"""
    def __init__(self, name="test"):
        self.name = name
        self._tools = {}
    
    def tool(self, name=None, description=None):
        """Mock tool decorator"""
        def decorator(func):
            tool_name = name or func.__name__
            self._tools[tool_name] = {
                "function": func,
                "description": description
            }
            return func
        return decorator
    
    def add_tool(self, func, name=None, description=None):
        """Mock add_tool method"""
        tool_name = name or func.__name__
        self._tools[tool_name] = {
            "function": func,
            "description": description
        }
    
    def run(self, transport="stdio"):
        """Mock run method"""
        print(f"Mock MCP server running with {transport}")

class Server:
    """Mock MCP Server"""
    def __init__(self, name="test"):
        self.name = name

# Mock server module
server = type('module', (), {
    'FastMCP': FastMCP,
    'Server': Server
})()
'''
    
    # Create mock mcp module
    os.makedirs("mcp", exist_ok=True)
    os.makedirs("mcp/server", exist_ok=True)
    
    with open("mcp/__init__.py", "w") as f:
        f.write("# Mock MCP module for testing\n")
    
    with open("mcp/server/__init__.py", "w") as f:
        f.write("# Mock MCP server module for testing\n")
    
    with open("mcp/server/fastmcp.py", "w") as f:
        f.write(mock_mcp_content)
    
    print("✅ Mock MCP module created")

def create_test_imports():
    """Create test-compatible import structure"""
    print("🔗 Setting up test import structure...")
    
    # Create __init__.py files where needed
    init_dirs = [
        "core",
        "core/brain",
        "core/memory",
        "core/memory/database",
        "core/intelligence",
        "utils"
    ]
    
    for dir_path in init_dirs:
        if os.path.exists(dir_path):
            init_file = os.path.join(dir_path, "__init__.py")
            if not os.path.exists(init_file):
                with open(init_file, "w") as f:
                    f.write(f"# {dir_path} module\n")
                print(f"✅ Created {init_file}")
    
    print("✅ Test import structure ready")

def main():
    """Main setup function"""
    print("🧪 MEMORY CONTEXT MANAGER v2 - TEST ENVIRONMENT SETUP")
    print("=" * 65)
    print("This script will prepare your system for integration testing")
    print()
    
    try:
        # Step 1: Install packages
        install_missing_packages()
        print()
        
        # Step 2: Create test database
        create_test_database() 
        print()
        
        # Step 3: Setup mock MCP
        setup_mock_mcp()
        print()
        
        # Step 4: Create test imports
        create_test_imports()
        print()
        
        print("🎉 TEST ENVIRONMENT SETUP COMPLETE!")
        print("=" * 65)
        print("✅ All dependencies installed")
        print("✅ Test database created with sample data")
        print("✅ Mock MCP module configured")
        print("✅ Import structure ready")
        print()
        print("🚀 You can now run: python3 test_complete_integration.py")
        print("🚀 Or run: ./run_integration_tests.sh")
        
    except Exception as e:
        print(f"❌ Setup failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()