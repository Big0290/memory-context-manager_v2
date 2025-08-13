#!/usr/bin/env python3
"""
Test Environment Setup Script
Prepares the complete testing environment for Memory Context Manager v2 integration tests

This script:
1. Sets up the proper directory structure
2. Initializes the test database
3. Configures mock dependencies
4. Validates the environment
5. Prepares for GitHub Actions CI/CD
"""

import os
import sys
import json
import sqlite3
import shutil
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== ENVIRONMENT CONFIGURATION ====================

class TestEnvironmentSetup:
    """Complete test environment setup and validation"""
    
    def __init__(self, project_root: Path = None, ci_mode: bool = False):
        self.project_root = project_root or Path(__file__).parent.parent.parent
        self.ci_mode = ci_mode
        self.setup_results = {
            "timestamp": datetime.now().isoformat(),
            "success": False,
            "steps_completed": [],
            "errors": [],
            "warnings": []
        }
        
    def log_step(self, step: str, success: bool = True, details: str = ""):
        """Log a setup step"""
        status = "✅" if success else "❌"
        logger.info(f"{status} {step}")
        
        if details:
            logger.info(f"   {details}")
        
        self.setup_results["steps_completed"].append({
            "step": step,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
        
        if not success:
            self.setup_results["errors"].append(f"{step}: {details}")
    
    def log_warning(self, message: str):
        """Log a warning"""
        logger.warning(f"⚠️ {message}")
        self.setup_results["warnings"].append(message)
    
    def setup_directory_structure(self):
        """Ensure proper directory structure exists"""
        logger.info("📁 Setting up directory structure...")
        
        required_dirs = [
            "brain_memory_store",
            "tests/integration",
            "core/brain",
            "core/intelligence",
            "core/memory",
            "plugins",
            "logs",
            "scripts"
        ]
        
        created_dirs = []
        for dir_path in required_dirs:
            full_path = self.project_root / dir_path
            try:
                full_path.mkdir(parents=True, exist_ok=True)
                created_dirs.append(str(dir_path))
            except Exception as e:
                self.log_step(f"Create directory {dir_path}", False, str(e))
                return False
        
        self.log_step(
            "Directory structure setup",
            True,
            f"Ensured {len(created_dirs)} directories exist"
        )
        return True
    
    def initialize_test_database(self):
        """Initialize test database with comprehensive schema"""
        logger.info("🗄️ Initializing test database...")
        
        db_path = self.project_root / "brain_memory_store" / "brain.db"
        
        try:
            with sqlite3.connect(str(db_path)) as conn:
                cursor = conn.cursor()
                
                # Comprehensive database schema for testing
                tables = [
                    # Core memory storage
                    """CREATE TABLE IF NOT EXISTS memory_store (
                        key TEXT PRIMARY KEY,
                        value TEXT,
                        timestamp TEXT,
                        importance REAL DEFAULT 0.5,
                        category TEXT DEFAULT 'general',
                        context TEXT DEFAULT '',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )""",
                    
                    # Brain state management
                    """CREATE TABLE IF NOT EXISTS brain_state (
                        key TEXT PRIMARY KEY,
                        value TEXT,
                        state_type TEXT DEFAULT 'general',
                        confidence REAL DEFAULT 1.0,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )""",
                    
                    # Function call logging
                    """CREATE TABLE IF NOT EXISTS function_calls (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT,
                        timestamp TEXT,
                        function_name TEXT,
                        function_type TEXT,
                        input_data TEXT,
                        output_data TEXT,
                        execution_time REAL,
                        success BOOLEAN DEFAULT 1,
                        user_message TEXT,
                        memory_context TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )""",
                    
                    # Dream system metrics
                    """CREATE TABLE IF NOT EXISTS dream_system_metrics (
                        id INTEGER PRIMARY KEY,
                        dream_cycles INTEGER DEFAULT 1,
                        cross_references_processed INTEGER DEFAULT 10,
                        relationships_enhanced INTEGER DEFAULT 5,
                        context_injections_generated INTEGER DEFAULT 15,
                        knowledge_synthesis_events INTEGER DEFAULT 8,
                        memory_consolidation_cycles INTEGER DEFAULT 3,
                        dream_effectiveness REAL DEFAULT 0.8,
                        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )""",
                    
                    # Learning and knowledge management
                    """CREATE TABLE IF NOT EXISTS learning_bits (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        content TEXT NOT NULL,
                        content_type TEXT DEFAULT 'general',
                        category TEXT DEFAULT 'learning',
                        importance_score REAL DEFAULT 0.5,
                        source TEXT DEFAULT 'unknown',
                        learning_context TEXT DEFAULT '',
                        processed BOOLEAN DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )""",
                    
                    # Cross-references between learning bits
                    """CREATE TABLE IF NOT EXISTS cross_references (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        source_bit_id INTEGER,
                        target_bit_id INTEGER,
                        relationship_type TEXT DEFAULT 'related',
                        strength REAL DEFAULT 1.0,
                        confidence REAL DEFAULT 0.8,
                        created_by TEXT DEFAULT 'system',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (source_bit_id) REFERENCES learning_bits(id),
                        FOREIGN KEY (target_bit_id) REFERENCES learning_bits(id)
                    )""",
                    
                    # Context enhancement pipeline
                    """CREATE TABLE IF NOT EXISTS context_enhancement_pipeline (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        trigger_type TEXT,
                        enhancement_type TEXT,
                        input_context TEXT,
                        enhanced_context TEXT,
                        improvement_score REAL DEFAULT 0.0,
                        processing_time REAL DEFAULT 0.0,
                        status TEXT DEFAULT 'completed',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )""",
                    
                    # Identity and personalization
                    """CREATE TABLE IF NOT EXISTS identity_profiles (
                        id TEXT PRIMARY KEY,
                        name TEXT,
                        profile_data TEXT,
                        preferences TEXT DEFAULT '{}',
                        behavior_patterns TEXT DEFAULT '{}',
                        interaction_history TEXT DEFAULT '{}',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )""",
                    
                    # Memory chunks for large content
                    """CREATE TABLE IF NOT EXISTS memory_chunks (
                        id TEXT PRIMARY KEY,
                        content TEXT,
                        chunk_type TEXT DEFAULT 'text',
                        parent_id TEXT,
                        chunk_order INTEGER DEFAULT 0,
                        metadata TEXT DEFAULT '{}',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )""",
                    
                    # Conversation memories
                    """CREATE TABLE IF NOT EXISTS conversation_memories (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        content TEXT,
                        conversation_type TEXT DEFAULT 'general',
                        participants TEXT DEFAULT '{}',
                        context_tags TEXT DEFAULT '{}',
                        importance REAL DEFAULT 0.5,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )""",
                    
                    # Context history tracking
                    """CREATE TABLE IF NOT EXISTS context_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        context_type TEXT,
                        context_data TEXT,
                        user_id TEXT,
                        session_id TEXT,
                        effectiveness_score REAL DEFAULT 0.0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )""",
                    
                    # System performance metrics
                    """CREATE TABLE IF NOT EXISTS performance_metrics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        metric_name TEXT,
                        metric_value REAL,
                        metric_type TEXT DEFAULT 'performance',
                        measurement_context TEXT DEFAULT '',
                        recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )""",
                    
                    # Integration test results
                    """CREATE TABLE IF NOT EXISTS integration_test_results (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        test_name TEXT,
                        test_category TEXT,
                        success BOOLEAN,
                        execution_time REAL,
                        test_details TEXT DEFAULT '{}',
                        test_run_id TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )"""
                ]
                
                # Create all tables
                tables_created = 0
                for table_sql in tables:
                    try:
                        cursor.execute(table_sql)
                        tables_created += 1
                    except sqlite3.Error as e:
                        self.log_step(f"Create table", False, str(e))
                        return False
                
                # Create indexes for performance
                indexes = [
                    "CREATE INDEX IF NOT EXISTS idx_memory_store_key ON memory_store(key)",
                    "CREATE INDEX IF NOT EXISTS idx_memory_store_category ON memory_store(category)",
                    "CREATE INDEX IF NOT EXISTS idx_function_calls_session ON function_calls(session_id)",
                    "CREATE INDEX IF NOT EXISTS idx_function_calls_function ON function_calls(function_name)",
                    "CREATE INDEX IF NOT EXISTS idx_learning_bits_category ON learning_bits(category)",
                    "CREATE INDEX IF NOT EXISTS idx_cross_references_source ON cross_references(source_bit_id)",
                    "CREATE INDEX IF NOT EXISTS idx_conversation_memories_type ON conversation_memories(conversation_type)",
                    "CREATE INDEX IF NOT EXISTS idx_context_history_type ON context_history(context_type)",
                    "CREATE INDEX IF NOT EXISTS idx_performance_metrics_name ON performance_metrics(metric_name)",
                    "CREATE INDEX IF NOT EXISTS idx_integration_test_category ON integration_test_results(test_category)"
                ]
                
                indexes_created = 0
                for index_sql in indexes:
                    try:
                        cursor.execute(index_sql)
                        indexes_created += 1
                    except sqlite3.Error as e:
                        self.log_warning(f"Index creation warning: {str(e)}")
                
                # Insert sample test data
                self._insert_sample_test_data(cursor)
                
                conn.commit()
                
                # Verify database
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                created_tables = [row[0] for row in cursor.fetchall()]
                
                self.log_step(
                    "Test database initialization",
                    True,
                    f"Created {tables_created} tables, {indexes_created} indexes"
                )
                
                # Get database size
                db_size = os.path.getsize(str(db_path)) / 1024  # KB
                logger.info(f"   Database size: {db_size:.1f}KB")
                
                return True
                
        except Exception as e:
            self.log_step("Test database initialization", False, str(e))
            return False
    
    def _insert_sample_test_data(self, cursor):
        """Insert sample data for testing"""
        try:
            # Sample memory store data
            sample_memories = [
                ("test_integration_setup", json.dumps({
                    "type": "system_memory",
                    "content": "Integration test environment initialized",
                    "importance": "high"
                }), datetime.now().isoformat(), 0.8, "system", "test_setup"),
                
                ("user_preferences", json.dumps({
                    "name": "Test User",
                    "preferences": ["detailed_responses", "technical_explanations"],
                    "interaction_style": "analytical"
                }), datetime.now().isoformat(), 0.9, "user", "preferences")
            ]
            
            for key, value, timestamp, importance, category, context in sample_memories:
                cursor.execute("""
                    INSERT OR REPLACE INTO memory_store 
                    (key, value, timestamp, importance, category, context)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (key, value, timestamp, importance, category, context))
            
            # Sample brain state
            brain_states = [
                ("consciousness_level", "0.85", "cognitive", 1.0),
                ("memory_efficiency", "0.92", "performance", 0.9),
                ("learning_rate", "0.78", "adaptation", 0.8)
            ]
            
            for key, value, state_type, confidence in brain_states:
                cursor.execute("""
                    INSERT OR REPLACE INTO brain_state 
                    (key, value, state_type, confidence)
                    VALUES (?, ?, ?, ?)
                """, (key, value, state_type, confidence))
            
            # Sample dream system metrics
            cursor.execute("""
                INSERT OR REPLACE INTO dream_system_metrics 
                (id, dream_cycles, cross_references_processed, relationships_enhanced,
                 context_injections_generated, knowledge_synthesis_events, 
                 memory_consolidation_cycles, dream_effectiveness)
                VALUES (1, 3, 25, 12, 18, 8, 5, 0.87)
            """)
            
            # Sample learning bits
            learning_samples = [
                ("Integration testing is crucial for system validation", "concept", "testing", 0.8, "test_setup"),
                ("Memory consolidation improves recall efficiency", "insight", "memory", 0.9, "research"),
                ("Cross-references enhance knowledge connectivity", "principle", "architecture", 0.85, "design")
            ]
            
            for content, content_type, category, importance, source in learning_samples:
                cursor.execute("""
                    INSERT INTO learning_bits 
                    (content, content_type, category, importance_score, source)
                    VALUES (?, ?, ?, ?, ?)
                """, (content, content_type, category, importance, source))
            
            # Sample performance metrics
            performance_samples = [
                ("database_query_time", 0.025, "latency", "Initial test setup"),
                ("memory_usage", 128.5, "resource", "System baseline"),
                ("success_rate", 96.9, "effectiveness", "Target performance")
            ]
            
            for metric_name, metric_value, metric_type, context in performance_samples:
                cursor.execute("""
                    INSERT INTO performance_metrics 
                    (metric_name, metric_value, metric_type, measurement_context)
                    VALUES (?, ?, ?, ?)
                """, (metric_name, metric_value, metric_type, context))
                
        except Exception as e:
            self.log_warning(f"Sample data insertion warning: {str(e)}")
    
    def setup_mock_dependencies(self):
        """Setup mock dependencies for testing"""
        logger.info("🔧 Setting up mock dependencies...")
        
        try:
            # Import and setup test environment requirements
            from tests.integration.test_environment_requirements import (
                setup_mock_environment, 
                setup_project_mocks, 
                validate_dependencies
            )
            
            # Setup mocks
            setup_mock_environment()
            setup_project_mocks()
            
            # Validate dependencies
            deps_valid, missing_deps = validate_dependencies()
            
            if missing_deps:
                self.log_warning(f"Missing optional dependencies: {missing_deps}")
            
            self.log_step(
                "Mock dependencies setup",
                True,
                f"Dependencies valid: {deps_valid}, Mocks installed"
            )
            
            return True
            
        except Exception as e:
            self.log_step("Mock dependencies setup", False, str(e))
            return False
    
    def create_configuration_files(self):
        """Create necessary configuration files"""
        logger.info("📝 Creating configuration files...")
        
        try:
            configs_created = []
            
            # Test configuration
            test_config = {
                "test_environment": {
                    "database_path": "brain_memory_store/brain.db",
                    "mock_dependencies": True,
                    "verbose_logging": True,
                    "performance_monitoring": True
                },
                "integration_tests": {
                    "target_success_rate": 96.9,
                    "timeout_seconds": 300,
                    "retry_failed_tests": False,
                    "categories": [
                        "Database Integration",
                        "Brain Interface Systems", 
                        "Enhanced Dream System",
                        "MCP Tool Integration",
                        "Performance Monitoring",
                        "Cross-Component Interactions",
                        "System Health Validation"
                    ]
                },
                "ci_cd": {
                    "generate_reports": True,
                    "upload_artifacts": True,
                    "fail_on_low_success": True,
                    "minimum_success_rate": 80
                }
            }
            
            config_path = self.project_root / "tests" / "integration" / "test_config.json"
            with open(config_path, 'w') as f:
                json.dump(test_config, f, indent=2)
            configs_created.append("test_config.json")
            
            # GitHub Actions test script
            test_script = """#!/bin/bash
# GitHub Actions Integration Test Runner
set -e

echo "🧪 Running Memory Context Manager v2 Integration Tests"
echo "=" * 60

# Set environment variables
export PYTHONPATH="${PYTHONPATH}:."
export TEST_ENVIRONMENT="github_actions"

# Create test database directory
mkdir -p brain_memory_store

# Run integration tests
python3 tests/integration/test_complete_integration.py --ci --verbose

echo "✅ Integration tests completed"
"""
            
            script_path = self.project_root / "tests" / "integration" / "run_tests.sh"
            with open(script_path, 'w') as f:
                f.write(test_script)
            os.chmod(script_path, 0o755)  # Make executable
            configs_created.append("run_tests.sh")
            
            # Pytest configuration
            pytest_ini = """[tool:pytest]
testpaths = tests/integration
python_files = test_*.py
python_functions = test_*
python_classes = Test* *Tests
addopts = 
    --verbose
    --tb=short
    --durations=10
    --strict-markers
markers =
    integration: marks tests as integration tests
    slow: marks tests as slow running
    database: marks tests that require database
    mcp: marks tests that require MCP tools
"""
            
            pytest_path = self.project_root / "pytest.ini"
            with open(pytest_path, 'w') as f:
                f.write(pytest_ini)
            configs_created.append("pytest.ini")
            
            self.log_step(
                "Configuration files creation",
                True,
                f"Created {len(configs_created)} config files"
            )
            
            return True
            
        except Exception as e:
            self.log_step("Configuration files creation", False, str(e))
            return False
    
    def validate_environment(self):
        """Validate the complete test environment"""
        logger.info("✅ Validating test environment...")
        
        validation_results = {
            "directory_structure": False,
            "database_accessible": False,
            "dependencies_available": False,
            "config_files_present": False,
            "import_paths_working": False
        }
        
        try:
            # Check directory structure
            required_dirs = [
                "brain_memory_store", "tests/integration", "core/brain", 
                "core/intelligence", "plugins"
            ]
            
            dirs_exist = all((self.project_root / d).exists() for d in required_dirs)
            validation_results["directory_structure"] = dirs_exist
            
            # Check database
            db_path = self.project_root / "brain_memory_store" / "brain.db"
            if db_path.exists():
                try:
                    with sqlite3.connect(str(db_path)) as conn:
                        cursor = conn.cursor()
                        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
                        table_count = cursor.fetchone()[0]
                        validation_results["database_accessible"] = table_count > 5
                except:
                    validation_results["database_accessible"] = False
            
            # Check dependencies
            try:
                from tests.integration.test_environment_requirements import validate_dependencies
                deps_valid, _ = validate_dependencies()
                validation_results["dependencies_available"] = deps_valid
            except:
                validation_results["dependencies_available"] = False
            
            # Check config files
            config_files = [
                "tests/integration/test_config.json",
                "tests/integration/run_tests.sh",
                "pytest.ini"
            ]
            
            configs_exist = all((self.project_root / f).exists() for f in config_files)
            validation_results["config_files_present"] = configs_exist
            
            # Check import paths
            try:
                sys.path.insert(0, str(self.project_root))
                import tests.integration.test_complete_integration
                import tests.integration.test_environment_requirements
                validation_results["import_paths_working"] = True
            except:
                validation_results["import_paths_working"] = False
            
            # Overall validation
            all_valid = all(validation_results.values())
            
            if all_valid:
                self.log_step(
                    "Environment validation",
                    True,
                    "All validation checks passed"
                )
            else:
                failed_checks = [k for k, v in validation_results.items() if not v]
                self.log_step(
                    "Environment validation",
                    False,
                    f"Failed checks: {failed_checks}"
                )
            
            return all_valid, validation_results
            
        except Exception as e:
            self.log_step("Environment validation", False, str(e))
            return False, validation_results
    
    def run_basic_tests(self):
        """Run basic environment tests"""
        logger.info("🧪 Running basic environment tests...")
        
        try:
            test_results = {
                "database_connection": False,
                "mock_imports": False,
                "basic_functionality": False
            }
            
            # Test database connection
            db_path = self.project_root / "brain_memory_store" / "brain.db"
            try:
                with sqlite3.connect(str(db_path)) as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT COUNT(*) FROM memory_store")
                    count = cursor.fetchone()[0]
                    test_results["database_connection"] = True
                    logger.info(f"   Database connection: ✅ ({count} records in memory_store)")
            except Exception as e:
                logger.error(f"   Database connection: ❌ {str(e)}")
            
            # Test mock imports
            try:
                from tests.integration.test_environment_requirements import (
                    MockBrainInterface, MockEnhancedDreamSystem
                )
                brain = MockBrainInterface()
                dream = MockEnhancedDreamSystem("test.db")
                test_results["mock_imports"] = True
                logger.info("   Mock imports: ✅")
            except Exception as e:
                logger.error(f"   Mock imports: ❌ {str(e)}")
            
            # Test basic functionality
            try:
                import asyncio
                async def test_async():
                    brain = MockBrainInterface()
                    result = await brain.analyze_with_context("Test message")
                    return result.get("analysis_result") is not None
                
                # Run async test
                if hasattr(asyncio, 'run'):
                    basic_test_result = asyncio.run(test_async())
                else:
                    loop = asyncio.get_event_loop()
                    basic_test_result = loop.run_until_complete(test_async())
                
                test_results["basic_functionality"] = basic_test_result
                logger.info("   Basic functionality: ✅")
            except Exception as e:
                logger.error(f"   Basic functionality: ❌ {str(e)}")
            
            all_tests_passed = all(test_results.values())
            
            self.log_step(
                "Basic environment tests",
                all_tests_passed,
                f"Passed: {sum(test_results.values())}/{len(test_results)}"
            )
            
            return all_tests_passed, test_results
            
        except Exception as e:
            self.log_step("Basic environment tests", False, str(e))
            return False, {}
    
    def generate_setup_report(self):
        """Generate comprehensive setup report"""
        total_steps = len(self.setup_results["steps_completed"])
        successful_steps = sum(1 for step in self.setup_results["steps_completed"] if step["success"])
        
        self.setup_results["success"] = len(self.setup_results["errors"]) == 0
        
        logger.info("\n" + "=" * 80)
        logger.info("📊 TEST ENVIRONMENT SETUP REPORT")
        logger.info("=" * 80)
        
        logger.info(f"🎯 OVERALL RESULT: {'✅ SUCCESS' if self.setup_results['success'] else '❌ FAILED'}")
        logger.info(f"📈 STEPS COMPLETED: {successful_steps}/{total_steps}")
        
        if self.setup_results["warnings"]:
            logger.info(f"⚠️ WARNINGS: {len(self.setup_results['warnings'])}")
            for warning in self.setup_results["warnings"]:
                logger.info(f"   - {warning}")
        
        if self.setup_results["errors"]:
            logger.info(f"❌ ERRORS: {len(self.setup_results['errors'])}")
            for error in self.setup_results["errors"]:
                logger.info(f"   - {error}")
        
        # Save report to file
        try:
            report_path = self.project_root / "tests" / "integration" / "setup_report.json"
            with open(report_path, 'w') as f:
                json.dump(self.setup_results, f, indent=2)
            logger.info(f"📁 Setup report saved: {report_path}")
        except Exception as e:
            logger.error(f"Failed to save setup report: {str(e)}")
        
        logger.info("=" * 80)
        
        return self.setup_results
    
    def run_complete_setup(self):
        """Run complete environment setup"""
        logger.info("🚀 STARTING TEST ENVIRONMENT SETUP")
        logger.info("=" * 80)
        
        setup_steps = [
            ("Directory Structure", self.setup_directory_structure),
            ("Test Database", self.initialize_test_database),
            ("Mock Dependencies", self.setup_mock_dependencies),
            ("Configuration Files", self.create_configuration_files),
            ("Environment Validation", lambda: self.validate_environment()[0]),
            ("Basic Tests", lambda: self.run_basic_tests()[0])
        ]
        
        for step_name, step_function in setup_steps:
            logger.info(f"\n📋 Step: {step_name}")
            try:
                success = step_function()
                if not success:
                    logger.error(f"❌ Step failed: {step_name}")
                    if not self.ci_mode:
                        break
            except Exception as e:
                logger.error(f"❌ Step error: {step_name} - {str(e)}")
                self.setup_results["errors"].append(f"{step_name}: {str(e)}")
                if not self.ci_mode:
                    break
        
        return self.generate_setup_report()


# ==================== MAIN EXECUTION ====================

def main():
    """Main function for test environment setup"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Test Environment Setup')
    parser.add_argument('--ci', action='store_true', help='Run in CI mode')
    parser.add_argument('--project-root', type=str, help='Project root directory')
    parser.add_argument('--validate-only', action='store_true', help='Only validate environment')
    
    args = parser.parse_args()
    
    # Determine project root
    if args.project_root:
        project_root = Path(args.project_root)
    else:
        project_root = Path(__file__).parent.parent.parent
    
    # Create setup instance
    setup = TestEnvironmentSetup(project_root=project_root, ci_mode=args.ci)
    
    if args.validate_only:
        # Only run validation
        logger.info("🔍 Running environment validation only...")
        valid, validation_results = setup.validate_environment()
        
        if valid:
            logger.info("✅ Environment validation passed")
            return 0
        else:
            logger.error("❌ Environment validation failed")
            logger.error(f"Failed checks: {[k for k, v in validation_results.items() if not v]}")
            return 1
    else:
        # Run complete setup
        report = setup.run_complete_setup()
        
        if report["success"]:
            logger.info("\n✅ TEST ENVIRONMENT SETUP COMPLETED SUCCESSFULLY!")
            logger.info("🚀 Ready to run integration tests!")
            return 0
        else:
            logger.error("\n❌ TEST ENVIRONMENT SETUP FAILED!")
            logger.error("Please check the errors above and retry.")
            return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)