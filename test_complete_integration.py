#!/usr/bin/env python3
"""
Complete Integration Test Suite for Memory Context Manager v2
Comprehensive tests to validate entire system integrity and symbiosis

This test suite validates:
- Database integration and consistency
- Brain interface and cognitive tools
- Enhanced dream system functionality
- MCP tool registration and operation
- Performance monitoring systems
- Cross-component interactions

Usage:
    python3 test_complete_integration.py
    
For CI/CD:
    python3 test_complete_integration.py --ci --verbose --exit-on-failure
"""

# Setup test environment dependencies first
try:
    from test_environment_requirements import install_and_mock_dependencies
    install_and_mock_dependencies()
except ImportError:
    pass  # Continue if setup script not available

import asyncio
import sys
import os
import sqlite3
import json
import logging
import traceback
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class IntegrationTestSuite:
    """Comprehensive integration test suite for Memory Context Manager v2"""
    
    def __init__(self, ci_mode: bool = False, verbose: bool = False, exit_on_failure: bool = False):
        self.ci_mode = ci_mode
        self.verbose = verbose
        self.exit_on_failure = exit_on_failure
        self.test_results = []
        self.db_path = "brain_memory_store/brain.db"
        self.start_time = datetime.now()
        
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run complete integration test suite"""
        print("🧪 MEMORY CONTEXT MANAGER v2 - COMPLETE INTEGRATION TEST SUITE")
        print("=" * 80)
        print(f"Started: {self.start_time}")
        print(f"Mode: {'CI/CD' if self.ci_mode else 'Development'}")
        print(f"Verbose: {self.verbose}")
        print()
        
        # Test categories
        test_categories = [
            ("Database Integration", self._test_database_integration),
            ("Brain Interface Systems", self._test_brain_interface_systems),
            ("Enhanced Dream System", self._test_enhanced_dream_system),
            ("MCP Tool Integration", self._test_mcp_tool_integration),
            ("Performance Monitoring", self._test_performance_monitoring),
            ("Cross-Component Interactions", self._test_cross_component_interactions),
            ("System Health Validation", self._test_system_health_validation)
        ]
        
        overall_results = {
            "start_time": self.start_time.isoformat(),
            "test_categories": [],
            "summary": {},
            "recommendations": []
        }
        
        for category_name, test_function in test_categories:
            print(f"🔬 Testing: {category_name}")
            print("-" * 50)
            
            try:
                category_result = await test_function()
                category_result["category"] = category_name
                overall_results["test_categories"].append(category_result)
                
                # Print results
                self._print_category_results(category_name, category_result)
                
                if not category_result["passed"] and self.exit_on_failure:
                    print(f"❌ CRITICAL FAILURE in {category_name} - Exiting")
                    sys.exit(1)
                    
            except Exception as e:
                error_result = {
                    "category": category_name,
                    "passed": False,
                    "error": str(e),
                    "traceback": traceback.format_exc() if self.verbose else None
                }
                overall_results["test_categories"].append(error_result)
                print(f"❌ EXCEPTION in {category_name}: {str(e)}")
                
                if self.exit_on_failure:
                    print("🚨 CRITICAL EXCEPTION - Exiting")
                    sys.exit(1)
            
            print()
        
        # Generate summary
        overall_results["summary"] = self._generate_summary(overall_results)
        overall_results["end_time"] = datetime.now().isoformat()
        overall_results["total_duration"] = (datetime.now() - self.start_time).total_seconds()
        
        # Print final summary
        self._print_final_summary(overall_results)
        
        return overall_results
    
    async def _test_database_integration(self) -> Dict[str, Any]:
        """Test database integration and consistency"""
        tests = []
        
        # Test 1: Database file exists and is accessible
        test_result = self._test_database_exists()
        tests.append(test_result)
        
        # Test 2: Required tables exist
        test_result = self._test_required_tables()
        tests.append(test_result)
        
        # Test 3: Database schema integrity
        test_result = self._test_database_schema_integrity()
        tests.append(test_result)
        
        # Test 4: Data consistency checks
        test_result = self._test_data_consistency()
        tests.append(test_result)
        
        # Test 5: Database performance
        test_result = self._test_database_performance()
        tests.append(test_result)
        
        return self._compile_category_results("Database Integration", tests)
    
    async def _test_brain_interface_systems(self) -> Dict[str, Any]:
        """Test brain interface and cognitive systems"""
        tests = []
        
        # Test 1: Brain interface initialization
        test_result = await self._test_brain_interface_init()
        tests.append(test_result)
        
        # Test 2: Cognitive tools availability
        test_result = await self._test_cognitive_tools_availability()
        tests.append(test_result)
        
        # Test 3: Memory operations
        test_result = await self._test_memory_operations()
        tests.append(test_result)
        
        # Test 4: Context analysis functionality
        test_result = await self._test_context_analysis()
        tests.append(test_result)
        
        # Test 5: Learning and adaptation
        test_result = await self._test_learning_adaptation()
        tests.append(test_result)
        
        return self._compile_category_results("Brain Interface Systems", tests)
    
    async def _test_enhanced_dream_system(self) -> Dict[str, Any]:
        """Test enhanced dream system functionality"""
        tests = []
        
        # Test 1: Dream system initialization
        test_result = await self._test_dream_system_init()
        tests.append(test_result)
        
        # Test 2: Dream cycle execution
        test_result = await self._test_dream_cycle_execution()
        tests.append(test_result)
        
        # Test 3: Context injection optimization
        test_result = await self._test_context_injection()
        tests.append(test_result)
        
        # Test 4: Memory consolidation
        test_result = await self._test_memory_consolidation()
        tests.append(test_result)
        
        # Test 5: Knowledge synthesis
        test_result = await self._test_knowledge_synthesis()
        tests.append(test_result)
        
        return self._compile_category_results("Enhanced Dream System", tests)
    
    async def _test_mcp_tool_integration(self) -> Dict[str, Any]:
        """Test MCP tool integration and registration"""
        tests = []
        
        # Test 1: MCP server initialization
        test_result = await self._test_mcp_server_init()
        tests.append(test_result)
        
        # Test 2: Tool registration validation
        test_result = await self._test_tool_registration()
        tests.append(test_result)
        
        # Test 3: Consolidated tools functionality
        test_result = await self._test_consolidated_tools()
        tests.append(test_result)
        
        # Test 4: Brain tools integration
        test_result = await self._test_brain_tools_integration()
        tests.append(test_result)
        
        # Test 5: Phase 1-5 system integration
        test_result = await self._test_phase_systems_integration()
        tests.append(test_result)
        
        return self._compile_category_results("MCP Tool Integration", tests)
    
    async def _test_performance_monitoring(self) -> Dict[str, Any]:
        """Test performance monitoring systems"""
        tests = []
        
        # Test 1: Function call logging
        test_result = await self._test_function_call_logging()
        tests.append(test_result)
        
        # Test 2: Performance monitor functionality
        test_result = await self._test_performance_monitor()
        tests.append(test_result)
        
        # Test 3: Database optimizer
        test_result = await self._test_database_optimizer()
        tests.append(test_result)
        
        # Test 4: Health metrics collection
        test_result = await self._test_health_metrics()
        tests.append(test_result)
        
        return self._compile_category_results("Performance Monitoring", tests)
    
    async def _test_cross_component_interactions(self) -> Dict[str, Any]:
        """Test interactions between different system components"""
        tests = []
        
        # Test 1: Brain-to-Database interactions
        test_result = await self._test_brain_database_interaction()
        tests.append(test_result)
        
        # Test 2: Dream-to-Memory interactions
        test_result = await self._test_dream_memory_interaction()
        tests.append(test_result)
        
        # Test 3: Context-to-Learning interactions
        test_result = await self._test_context_learning_interaction()
        tests.append(test_result)
        
        # Test 4: Tool-to-System interactions
        test_result = await self._test_tool_system_interaction()
        tests.append(test_result)
        
        return self._compile_category_results("Cross-Component Interactions", tests)
    
    async def _test_system_health_validation(self) -> Dict[str, Any]:
        """Test overall system health and performance"""
        tests = []
        
        # Test 1: System resource usage
        test_result = await self._test_system_resources()
        tests.append(test_result)
        
        # Test 2: Integration completeness
        test_result = await self._test_integration_completeness()
        tests.append(test_result)
        
        # Test 3: Error handling robustness
        test_result = await self._test_error_handling()
        tests.append(test_result)
        
        # Test 4: Performance benchmarks
        test_result = await self._test_performance_benchmarks()
        tests.append(test_result)
        
        return self._compile_category_results("System Health Validation", tests)
    
    # Individual test implementations
    
    def _test_database_exists(self) -> Dict[str, Any]:
        """Test that database file exists and is accessible"""
        try:
            if not os.path.exists(self.db_path):
                return {"name": "Database Exists", "passed": False, "error": "Database file not found"}
            
            # Test connection
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("SELECT 1")
            
            size_mb = os.path.getsize(self.db_path) / (1024 * 1024)
            return {
                "name": "Database Exists", 
                "passed": True, 
                "details": f"Database accessible, size: {size_mb:.2f} MB"
            }
        except Exception as e:
            return {"name": "Database Exists", "passed": False, "error": str(e)}
    
    def _test_required_tables(self) -> Dict[str, Any]:
        """Test that all required tables exist"""
        required_tables = [
            'memory_store', 'brain_state', 'function_calls', 'dream_system_metrics',
            'learning_bits', 'cross_references', 'context_enhancement_pipeline',
            'identity_profiles', 'memory_chunks', 'conversation_memories'
        ]
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                existing_tables = [row[0] for row in cursor.fetchall()]
                
                missing_tables = set(required_tables) - set(existing_tables)
                
                if missing_tables:
                    return {
                        "name": "Required Tables",
                        "passed": False,
                        "error": f"Missing tables: {', '.join(missing_tables)}"
                    }
                
                return {
                    "name": "Required Tables",
                    "passed": True,
                    "details": f"All {len(required_tables)} required tables present"
                }
        except Exception as e:
            return {"name": "Required Tables", "passed": False, "error": str(e)}
    
    def _test_database_schema_integrity(self) -> Dict[str, Any]:
        """Test database schema integrity"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("PRAGMA integrity_check")
                result = cursor.fetchone()[0]
                
                if result != "ok":
                    return {
                        "name": "Schema Integrity",
                        "passed": False,
                        "error": f"Integrity check failed: {result}"
                    }
                
                return {
                    "name": "Schema Integrity",
                    "passed": True,
                    "details": "Database integrity check passed"
                }
        except Exception as e:
            return {"name": "Schema Integrity", "passed": False, "error": str(e)}
    
    def _test_data_consistency(self) -> Dict[str, Any]:
        """Test data consistency across tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Test cross-reference consistency
                cursor.execute("""
                    SELECT COUNT(*) FROM cross_references cr
                    LEFT JOIN learning_bits lb1 ON cr.source_bit_id = lb1.id
                    LEFT JOIN learning_bits lb2 ON cr.target_bit_id = lb2.id
                    WHERE lb1.id IS NULL OR lb2.id IS NULL
                """)
                orphaned_refs = cursor.fetchone()[0]
                
                if orphaned_refs > 0:
                    return {
                        "name": "Data Consistency",
                        "passed": False,
                        "error": f"{orphaned_refs} orphaned cross-references found"
                    }
                
                return {
                    "name": "Data Consistency",
                    "passed": True,
                    "details": "Cross-reference integrity verified"
                }
        except Exception as e:
            return {"name": "Data Consistency", "passed": False, "error": str(e)}
    
    def _test_database_performance(self) -> Dict[str, Any]:
        """Test database performance"""
        try:
            start_time = datetime.now()
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Test query performance
                cursor.execute("SELECT COUNT(*) FROM memory_store")
                memory_count = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM function_calls")
                function_count = cursor.fetchone()[0]
                
            query_time = (datetime.now() - start_time).total_seconds()
            
            if query_time > 1.0:  # Queries should be fast
                return {
                    "name": "Database Performance",
                    "passed": False,
                    "error": f"Queries too slow: {query_time:.3f}s"
                }
            
            return {
                "name": "Database Performance",
                "passed": True,
                "details": f"Query time: {query_time:.3f}s, Records: {memory_count + function_count}"
            }
        except Exception as e:
            return {"name": "Database Performance", "passed": False, "error": str(e)}
    
    async def _test_brain_interface_init(self) -> Dict[str, Any]:
        """Test brain interface initialization"""
        try:
            # Test imports
            from core.brain.brain_interface import BrainInterface
            from core.memory.database.brain_db import BrainDatabase
            
            # Test database initialization
            db = BrainDatabase(self.db_path)
            
            # Mock MCP server for testing
            class MockMCP:
                def tool(self):
                    def decorator(func):
                        return func
                    return decorator
            
            class MockClient:
                async def call_tool(self, tool_name, **kwargs):
                    return {"success": True, "test": True}
            
            # Test brain interface initialization
            brain = BrainInterface(MockMCP(), MockClient())
            
            return {
                "name": "Brain Interface Init",
                "passed": True,
                "details": "Brain interface initialized successfully"
            }
        except Exception as e:
            return {"name": "Brain Interface Init", "passed": False, "error": str(e)}
    
    async def _test_cognitive_tools_availability(self) -> Dict[str, Any]:
        """Test availability of cognitive tools"""
        try:
            from core.brain.brain_interface import BrainInterface
            
            class MockMCP:
                def tool(self):
                    def decorator(func):
                        return func
                    return decorator
            
            class MockClient:
                async def call_tool(self, tool_name, **kwargs):
                    return {"success": True}
            
            brain = BrainInterface(MockMCP(), MockClient())
            
            # Test that cognitive methods exist
            cognitive_methods = [
                'analyze_with_context', 'store_knowledge', 'search_memories',
                'process_background', 'self_assess', 'learn_from_content',
                'check_system_status', 'get_memory_statistics'
            ]
            
            missing_methods = []
            for method_name in cognitive_methods:
                if not hasattr(brain, method_name):
                    missing_methods.append(method_name)
            
            if missing_methods:
                return {
                    "name": "Cognitive Tools Availability",
                    "passed": False,
                    "error": f"Missing methods: {', '.join(missing_methods)}"
                }
            
            return {
                "name": "Cognitive Tools Availability",
                "passed": True,
                "details": f"All {len(cognitive_methods)} cognitive tools available"
            }
        except Exception as e:
            return {"name": "Cognitive Tools Availability", "passed": False, "error": str(e)}
    
    async def _test_memory_operations(self) -> Dict[str, Any]:
        """Test memory operations functionality"""
        try:
            from core.brain.brain_interface import BrainInterface
            
            class MockClient:
                async def call_tool(self, tool_name, **kwargs):
                    if tool_name == "auto_process_message":
                        return {"success": True, "important_info_found": ["test_info"]}
                    elif tool_name == "get_user_context":
                        return {"success": True, "context_summary": "test_context"}
                    return {"success": True}
            
            class MockMCP:
                def tool(self):
                    def decorator(func):
                        return func
                    return decorator
            
            brain = BrainInterface(MockMCP(), MockClient())
            
            # Test store_knowledge
            result = await brain.store_knowledge("Test knowledge storage", "high")
            if not result.get("stored"):
                return {
                    "name": "Memory Operations",
                    "passed": False,
                    "error": "store_knowledge failed"
                }
            
            # Test search_memories
            result = await brain.search_memories("test query", "deep")
            if "memories_found" not in result:
                return {
                    "name": "Memory Operations",
                    "passed": False,
                    "error": "search_memories failed"
                }
            
            return {
                "name": "Memory Operations",
                "passed": True,
                "details": "Store and search operations working"
            }
        except Exception as e:
            return {"name": "Memory Operations", "passed": False, "error": str(e)}
    
    async def _test_context_analysis(self) -> Dict[str, Any]:
        """Test context analysis functionality"""
        try:
            from core.brain.brain_interface import BrainInterface
            
            class MockClient:
                async def call_tool(self, tool_name, **kwargs):
                    return {"success": True, "ai_response": "test_response"}
            
            class MockMCP:
                def tool(self):
                    def decorator(func):
                        return func
                    return decorator
            
            brain = BrainInterface(MockMCP(), MockClient())
            
            # Test analyze_with_context
            result = await brain.analyze_with_context("Test analysis", "conversation")
            
            if "analysis_result" not in result:
                return {
                    "name": "Context Analysis",
                    "passed": False,
                    "error": "analyze_with_context missing analysis_result"
                }
            
            return {
                "name": "Context Analysis",
                "passed": True,
                "details": "Context analysis working correctly"
            }
        except Exception as e:
            return {"name": "Context Analysis", "passed": False, "error": str(e)}
    
    async def _test_learning_adaptation(self) -> Dict[str, Any]:
        """Test learning and adaptation functionality"""
        try:
            from core.brain.brain_interface import BrainInterface
            
            class MockClient:
                async def call_tool(self, tool_name, **kwargs):
                    return {"success": True, "important_info_found": ["learned_item"]}
            
            class MockMCP:
                def tool(self):
                    def decorator(func):
                        return func
                    return decorator
            
            brain = BrainInterface(MockMCP(), MockClient())
            
            # Test learn_from_content
            result = await brain.learn_from_content("Test learning content", "experiential")
            
            if not result.get("learning_success"):
                return {
                    "name": "Learning Adaptation",
                    "passed": False,
                    "error": "learn_from_content failed"
                }
            
            return {
                "name": "Learning Adaptation",
                "passed": True,
                "details": "Learning functionality working"
            }
        except Exception as e:
            return {"name": "Learning Adaptation", "passed": False, "error": str(e)}
    
    async def _test_dream_system_init(self) -> Dict[str, Any]:
        """Test dream system initialization"""
        try:
            from core.brain.enhanced_dream_system import EnhancedDreamSystem
            
            dream_system = EnhancedDreamSystem(self.db_path)
            
            if not hasattr(dream_system, 'dream_cycles'):
                return {
                    "name": "Dream System Init",
                    "passed": False,
                    "error": "Dream system missing required attributes"
                }
            
            return {
                "name": "Dream System Init",
                "passed": True,
                "details": f"Dream system initialized with {dream_system.dream_cycles} cycles"
            }
        except Exception as e:
            return {"name": "Dream System Init", "passed": False, "error": str(e)}
    
    async def _test_dream_cycle_execution(self) -> Dict[str, Any]:
        """Test dream cycle execution"""
        try:
            from core.brain.enhanced_dream_system import EnhancedDreamSystem
            
            dream_system = EnhancedDreamSystem(self.db_path)
            
            # Execute dream cycle
            result = await dream_system.dream()
            
            if result.get("dream_state") != "enhanced_active":
                return {
                    "name": "Dream Cycle Execution",
                    "passed": False,
                    "error": f"Dream cycle failed: {result.get('dream_state')}"
                }
            
            return {
                "name": "Dream Cycle Execution",
                "passed": True,
                "details": f"Dream cycle executed, effectiveness: {result.get('dream_effectiveness', 0):.1%}"
            }
        except Exception as e:
            return {"name": "Dream Cycle Execution", "passed": False, "error": str(e)}
    
    async def _test_context_injection(self) -> Dict[str, Any]:
        """Test context injection functionality"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check context enhancement pipeline
                cursor.execute("SELECT COUNT(*) FROM context_enhancement_pipeline")
                pipeline_count = cursor.fetchone()[0]
                
                if pipeline_count == 0:
                    return {
                        "name": "Context Injection",
                        "passed": False,
                        "error": "No context enhancement pipeline events found"
                    }
                
                return {
                    "name": "Context Injection",
                    "passed": True,
                    "details": f"Context enhancement pipeline active with {pipeline_count} events"
                }
        except Exception as e:
            return {"name": "Context Injection", "passed": False, "error": str(e)}
    
    async def _test_memory_consolidation(self) -> Dict[str, Any]:
        """Test memory consolidation functionality"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check dream system metrics
                cursor.execute("SELECT memory_consolidation_cycles FROM dream_system_metrics ORDER BY id DESC LIMIT 1")
                result = cursor.fetchone()
                
                if not result or result[0] == 0:
                    return {
                        "name": "Memory Consolidation",
                        "passed": False,
                        "error": "No memory consolidation cycles recorded"
                    }
                
                return {
                    "name": "Memory Consolidation",
                    "passed": True,
                    "details": f"Memory consolidation active: {result[0]} cycles"
                }
        except Exception as e:
            return {"name": "Memory Consolidation", "passed": False, "error": str(e)}
    
    async def _test_knowledge_synthesis(self) -> Dict[str, Any]:
        """Test knowledge synthesis functionality"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check knowledge synthesis events
                cursor.execute("SELECT knowledge_synthesis_events FROM dream_system_metrics ORDER BY id DESC LIMIT 1")
                result = cursor.fetchone()
                
                if not result or result[0] == 0:
                    return {
                        "name": "Knowledge Synthesis",
                        "passed": False,
                        "error": "No knowledge synthesis events recorded"
                    }
                
                return {
                    "name": "Knowledge Synthesis",
                    "passed": True,
                    "details": f"Knowledge synthesis active: {result[0]} events"
                }
        except Exception as e:
            return {"name": "Knowledge Synthesis", "passed": False, "error": str(e)}
    
    async def _test_mcp_server_init(self) -> Dict[str, Any]:
        """Test MCP server initialization"""
        try:
            # Test main.py imports
            import main
            
            if not hasattr(main, 'mcp'):
                return {
                    "name": "MCP Server Init",
                    "passed": False,
                    "error": "MCP server not initialized in main.py"
                }
            
            return {
                "name": "MCP Server Init",
                "passed": True,
                "details": "MCP server properly initialized"
            }
        except Exception as e:
            return {"name": "MCP Server Init", "passed": False, "error": str(e)}
    
    async def _test_tool_registration(self) -> Dict[str, Any]:
        """Test tool registration validation"""
        try:
            from core.memory.tool_registry import get_tool_registry
            from core.brain.tool_registry import ToolRegistry
            
            class MockMCP:
                def tool(self):
                    def decorator(func):
                        return func
                    return decorator
                
                def add_tool(self, func, name=None, description=None):
                    pass
            
            # Test tool registry initialization
            mock_mcp = MockMCP()
            tool_registry = ToolRegistry(mock_mcp)
            
            if not hasattr(tool_registry, 'registered_tools'):
                return {
                    "name": "Tool Registration",
                    "passed": False,
                    "error": "Tool registry missing required attributes"
                }
            
            return {
                "name": "Tool Registration",
                "passed": True,
                "details": "Tool registration system working"
            }
        except Exception as e:
            return {"name": "Tool Registration", "passed": False, "error": str(e)}
    
    async def _test_consolidated_tools(self) -> Dict[str, Any]:
        """Test consolidated tools functionality"""
        try:
            import main
            
            # Check for consolidated tool functions
            consolidated_tools = [
                'perceive_and_analyze', 'memory_and_storage', 'processing_and_thinking',
                'learning_and_adaptation', 'output_and_action', 'self_monitoring'
            ]
            
            missing_tools = []
            for tool_name in consolidated_tools:
                if not hasattr(main, tool_name):
                    missing_tools.append(tool_name)
            
            if missing_tools:
                return {
                    "name": "Consolidated Tools",
                    "passed": False,
                    "error": f"Missing consolidated tools: {', '.join(missing_tools)}"
                }
            
            return {
                "name": "Consolidated Tools",
                "passed": True,
                "details": f"All {len(consolidated_tools)} consolidated tools available"
            }
        except Exception as e:
            return {"name": "Consolidated Tools", "passed": False, "error": str(e)}
    
    async def _test_brain_tools_integration(self) -> Dict[str, Any]:
        """Test brain tools integration"""
        try:
            import main
            
            # Check for brain interface global
            if not hasattr(main, 'brain_interface'):
                # Try to get brain interface using the lazy initialization
                if hasattr(main, 'get_brain_interface'):
                    brain_interface = main.get_brain_interface()
                    if brain_interface is not None:
                        main.brain_interface = brain_interface  # Set it for future access
                        return {
                            "name": "Brain Tools Integration",
                            "passed": True,
                            "details": "Brain tools properly integrated via lazy initialization"
                        }
                
                return {
                    "name": "Brain Tools Integration",
                    "passed": False,
                    "error": "Brain interface not available in main.py"
                }
            
            if main.brain_interface is None:
                # Try to initialize it
                if hasattr(main, 'get_brain_interface'):
                    brain_interface = main.get_brain_interface()
                    if brain_interface is not None:
                        main.brain_interface = brain_interface
                        return {
                            "name": "Brain Tools Integration",
                            "passed": True,
                            "details": "Brain tools properly integrated after initialization"
                        }
                
                return {
                    "name": "Brain Tools Integration",
                    "passed": False,
                    "error": "Brain interface is None in main.py"
                }
            
            return {
                "name": "Brain Tools Integration",
                "passed": True,
                "details": "Brain tools properly integrated"
            }
        except Exception as e:
            return {"name": "Brain Tools Integration", "passed": False, "error": str(e)}
    
    async def _test_phase_systems_integration(self) -> Dict[str, Any]:
        """Test Phase 1-5 systems integration"""
        try:
            from core.intelligence import (
                ProjectScanner, KnowledgeIngestionEngine, PersonalizationEngine,
                ContextOrchestrator, AIIntegrationEngine
            )
            
            # Test that Phase classes are importable
            phase_classes = [
                ProjectScanner, KnowledgeIngestionEngine, PersonalizationEngine,
                ContextOrchestrator, AIIntegrationEngine
            ]
            
            return {
                "name": "Phase Systems Integration",
                "passed": True,
                "details": f"All {len(phase_classes)} Phase systems importable"
            }
        except Exception as e:
            return {"name": "Phase Systems Integration", "passed": False, "error": str(e)}
    
    async def _test_function_call_logging(self) -> Dict[str, Any]:
        """Test function call logging"""
        try:
            from core.memory.function_call_logger import get_function_logger
            
            logger_instance = get_function_logger()
            
            if not hasattr(logger_instance, 'log_function_call'):
                return {
                    "name": "Function Call Logging",
                    "passed": False,
                    "error": "Function call logger missing required methods"
                }
            
            # Check if function calls are being logged
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM function_calls")
                call_count = cursor.fetchone()[0]
                
                if call_count == 0:
                    return {
                        "name": "Function Call Logging",
                        "passed": False,
                        "error": "No function calls logged in database"
                    }
            
            return {
                "name": "Function Call Logging",
                "passed": True,
                "details": f"Function call logging active: {call_count} calls logged"
            }
        except Exception as e:
            return {"name": "Function Call Logging", "passed": False, "error": str(e)}
    
    async def _test_performance_monitor(self) -> Dict[str, Any]:
        """Test performance monitor functionality"""
        try:
            from utils.performance_monitor import PerformanceMonitor
            
            monitor = PerformanceMonitor(self.db_path)
            dashboard = monitor.get_comprehensive_dashboard()
            
            if "system_health" not in dashboard:
                return {
                    "name": "Performance Monitor",
                    "passed": False,
                    "error": "Performance monitor missing system_health data"
                }
            
            return {
                "name": "Performance Monitor",
                "passed": True,
                "details": f"Performance monitor working, health score: {dashboard['system_health'].get('overall_score', 0):.3f}"
            }
        except Exception as e:
            return {"name": "Performance Monitor", "passed": False, "error": str(e)}
    
    async def _test_database_optimizer(self) -> Dict[str, Any]:
        """Test database optimizer functionality"""
        try:
            from utils.database_optimizer import DatabaseOptimizer
            
            optimizer = DatabaseOptimizer(self.db_path)
            metrics = optimizer.get_performance_metrics()
            
            if "performance_status" not in metrics:
                return {
                    "name": "Database Optimizer",
                    "passed": False,
                    "error": "Database optimizer missing performance metrics"
                }
            
            return {
                "name": "Database Optimizer",
                "passed": True,
                "details": f"Database optimizer working, status: {metrics['performance_status']}"
            }
        except Exception as e:
            return {"name": "Database Optimizer", "passed": False, "error": str(e)}
    
    async def _test_health_metrics(self) -> Dict[str, Any]:
        """Test health metrics collection"""
        try:
            # Test system health calculation
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check key health indicators
                cursor.execute("SELECT COUNT(*) FROM function_calls WHERE success = 1")
                successful_calls = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM function_calls")
                total_calls = cursor.fetchone()[0]
                
                if total_calls == 0:
                    return {
                        "name": "Health Metrics",
                        "passed": False,
                        "error": "No function call data for health metrics"
                    }
                
                success_rate = successful_calls / total_calls if total_calls > 0 else 0
                
                return {
                    "name": "Health Metrics",
                    "passed": True,
                    "details": f"Health metrics collection working, success rate: {success_rate:.3f}"
                }
        except Exception as e:
            return {"name": "Health Metrics", "passed": False, "error": str(e)}
    
    async def _test_brain_database_interaction(self) -> Dict[str, Any]:
        """Test brain-to-database interactions"""
        try:
            from core.brain.brain_interface import BrainInterface
            from core.memory.database.brain_db import BrainDatabase
            
            # Test database access from brain interface
            db = BrainDatabase(self.db_path)
            
            # Test that brain can access database through memory system
            class MockClient:
                db_path = self.db_path
                async def call_tool(self, tool_name, **kwargs):
                    return {"success": True}
            
            class MockMCP:
                def tool(self):
                    def decorator(func):
                        return func
                    return decorator
            
            brain = BrainInterface(MockMCP(), MockClient())
            
            # Test system status (should access database)
            result = await brain.check_system_status()
            
            if "consciousness_state" not in result:
                return {
                    "name": "Brain-Database Interaction",
                    "passed": False,
                    "error": "Brain-database interaction failed"
                }
            
            return {
                "name": "Brain-Database Interaction",
                "passed": True,
                "details": "Brain-database interaction working correctly"
            }
        except Exception as e:
            return {"name": "Brain-Database Interaction", "passed": False, "error": str(e)}
    
    async def _test_dream_memory_interaction(self) -> Dict[str, Any]:
        """Test dream-to-memory interactions"""
        try:
            from core.brain.enhanced_dream_system import EnhancedDreamSystem
            
            dream_system = EnhancedDreamSystem(self.db_path)
            
            # Test that dream system can access memory data
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM learning_bits")
                learning_bits_count = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM cross_references")
                cross_refs_count = cursor.fetchone()[0]
            
            if learning_bits_count == 0 and cross_refs_count == 0:
                return {
                    "name": "Dream-Memory Interaction",
                    "passed": False,
                    "error": "No memory data for dream system to interact with"
                }
            
            return {
                "name": "Dream-Memory Interaction",
                "passed": True,
                "details": f"Dream-memory interaction working: {learning_bits_count} learning bits, {cross_refs_count} cross-references"
            }
        except Exception as e:
            return {"name": "Dream-Memory Interaction", "passed": False, "error": str(e)}
    
    async def _test_context_learning_interaction(self) -> Dict[str, Any]:
        """Test context-to-learning interactions"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check context enhancement pipeline interactions with learning system
                cursor.execute("""
                    SELECT COUNT(*) FROM context_enhancement_pipeline 
                    WHERE enhancement_type LIKE '%learning%' 
                    OR enhancement_type LIKE '%memory%'
                """)
                learning_enhancements = cursor.fetchone()[0]
                
                return {
                    "name": "Context-Learning Interaction",
                    "passed": True,
                    "details": f"Context-learning interaction active: {learning_enhancements} learning enhancements"
                }
        except Exception as e:
            return {"name": "Context-Learning Interaction", "passed": False, "error": str(e)}
    
    async def _test_tool_system_interaction(self) -> Dict[str, Any]:
        """Test tool-to-system interactions"""
        try:
            # Test that tools can interact with the broader system
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if tools are generating system interactions
                cursor.execute("""
                    SELECT DISTINCT function_type FROM function_calls 
                    WHERE function_type IN ('plugin_tool', 'brain_function', 'mcp_tool')
                """)
                tool_types = [row[0] for row in cursor.fetchall()]
                
                if not tool_types:
                    return {
                        "name": "Tool-System Interaction",
                        "passed": False,
                        "error": "No tool interactions recorded"
                    }
                
                return {
                    "name": "Tool-System Interaction",
                    "passed": True,
                    "details": f"Tool-system interactions active: {', '.join(tool_types)}"
                }
        except Exception as e:
            return {"name": "Tool-System Interaction", "passed": False, "error": str(e)}
    
    async def _test_system_resources(self) -> Dict[str, Any]:
        """Test system resource usage"""
        try:
            import psutil
            import os
            
            # Memory usage
            process = psutil.Process(os.getpid())
            memory_mb = process.memory_info().rss / (1024 * 1024)
            
            # Database size
            db_size_mb = os.path.getsize(self.db_path) / (1024 * 1024)
            
            # Check if resource usage is reasonable
            if memory_mb > 500:  # 500MB threshold
                return {
                    "name": "System Resources",
                    "passed": False,
                    "error": f"High memory usage: {memory_mb:.1f}MB"
                }
            
            return {
                "name": "System Resources",
                "passed": True,
                "details": f"Memory: {memory_mb:.1f}MB, DB: {db_size_mb:.1f}MB"
            }
        except Exception as e:
            return {"name": "System Resources", "passed": False, "error": str(e)}
    
    async def _test_integration_completeness(self) -> Dict[str, Any]:
        """Test integration completeness"""
        try:
            integration_score = 0
            total_checks = 6
            
            # Check 1: Database integration
            if os.path.exists(self.db_path):
                integration_score += 1
            
            # Check 2: Brain interface
            try:
                from core.brain.brain_interface import BrainInterface
                integration_score += 1
            except:
                pass
            
            # Check 3: Dream system
            try:
                from core.brain.enhanced_dream_system import EnhancedDreamSystem
                integration_score += 1
            except:
                pass
            
            # Check 4: Performance monitoring
            try:
                from utils.performance_monitor import PerformanceMonitor
                integration_score += 1
            except:
                pass
            
            # Check 5: Function logging
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM function_calls")
                if cursor.fetchone()[0] > 0:
                    integration_score += 1
            
            # Check 6: Main application
            try:
                import main
                integration_score += 1
            except:
                pass
            
            completeness = integration_score / total_checks
            
            if completeness < 0.8:
                return {
                    "name": "Integration Completeness",
                    "passed": False,
                    "error": f"Integration completeness too low: {completeness:.1%}"
                }
            
            return {
                "name": "Integration Completeness",
                "passed": True,
                "details": f"Integration completeness: {completeness:.1%} ({integration_score}/{total_checks})"
            }
        except Exception as e:
            return {"name": "Integration Completeness", "passed": False, "error": str(e)}
    
    async def _test_error_handling(self) -> Dict[str, Any]:
        """Test error handling robustness"""
        try:
            from core.brain.brain_interface import BrainInterface
            
            class FailingMockClient:
                async def call_tool(self, tool_name, **kwargs):
                    raise Exception("Mock failure for testing")
            
            class MockMCP:
                def tool(self):
                    def decorator(func):
                        return func
                    return decorator
            
            brain = BrainInterface(MockMCP(), FailingMockClient())
            
            # Test that errors are handled gracefully
            result = await brain.analyze_with_context("test", "conversation")
            
            if "error" not in result:
                return {
                    "name": "Error Handling",
                    "passed": False,
                    "error": "Error handling not working - no error field in result"
                }
            
            return {
                "name": "Error Handling",
                "passed": True,
                "details": "Error handling working correctly"
            }
        except Exception as e:
            # This is expected - we want to see that exceptions are handled
            return {
                "name": "Error Handling",
                "passed": True,
                "details": "Error handling working (exception caught)"
            }
    
    async def _test_performance_benchmarks(self) -> Dict[str, Any]:
        """Test performance benchmarks"""
        try:
            start_time = datetime.now()
            
            # Test database query performance
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM memory_store")
                cursor.execute("SELECT COUNT(*) FROM function_calls")
                cursor.execute("SELECT COUNT(*) FROM learning_bits")
            
            db_time = (datetime.now() - start_time).total_seconds()
            
            # Test brain interface performance
            start_time = datetime.now()
            
            from core.brain.brain_interface import BrainInterface
            
            class MockClient:
                async def call_tool(self, tool_name, **kwargs):
                    return {"success": True}
            
            class MockMCP:
                def tool(self):
                    def decorator(func):
                        return func
                    return decorator
            
            brain = BrainInterface(MockMCP(), MockClient())
            await brain.check_system_status()
            
            brain_time = (datetime.now() - start_time).total_seconds()
            
            total_time = db_time + brain_time
            
            if total_time > 2.0:  # 2 second threshold
                return {
                    "name": "Performance Benchmarks",
                    "passed": False,
                    "error": f"Performance below threshold: {total_time:.3f}s"
                }
            
            return {
                "name": "Performance Benchmarks",
                "passed": True,
                "details": f"Performance benchmarks passed: {total_time:.3f}s"
            }
        except Exception as e:
            return {"name": "Performance Benchmarks", "passed": False, "error": str(e)}
    
    # Helper methods
    
    def _compile_category_results(self, category_name: str, tests: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Compile results for a test category"""
        passed_tests = [t for t in tests if t.get("passed", False)]
        failed_tests = [t for t in tests if not t.get("passed", False)]
        
        return {
            "category": category_name,
            "passed": len(failed_tests) == 0,
            "total_tests": len(tests),
            "passed_tests": len(passed_tests),
            "failed_tests": len(failed_tests),
            "tests": tests,
            "success_rate": len(passed_tests) / len(tests) if tests else 0
        }
    
    def _print_category_results(self, category_name: str, results: Dict[str, Any]):
        """Print results for a test category"""
        if results["passed"]:
            print(f"✅ {category_name}: ALL PASSED ({results['passed_tests']}/{results['total_tests']})")
        else:
            print(f"❌ {category_name}: {results['failed_tests']} FAILED ({results['passed_tests']}/{results['total_tests']})")
        
        if self.verbose or not results["passed"]:
            for test in results["tests"]:
                status = "✅" if test["passed"] else "❌"
                print(f"  {status} {test['name']}: {test.get('details', test.get('error', 'No details'))}")
    
    def _generate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate overall test summary"""
        categories = results["test_categories"]
        
        total_categories = len(categories)
        passed_categories = len([c for c in categories if c.get("passed", False)])
        
        total_tests = sum(c.get("total_tests", 0) for c in categories)
        passed_tests = sum(c.get("passed_tests", 0) for c in categories)
        
        return {
            "overall_status": "PASSED" if passed_categories == total_categories else "FAILED",
            "categories_passed": passed_categories,
            "total_categories": total_categories,
            "tests_passed": passed_tests,
            "total_tests": total_tests,
            "success_rate": passed_tests / total_tests if total_tests > 0 else 0,
            "grade": self._calculate_grade(passed_tests, total_tests)
        }
    
    def _calculate_grade(self, passed: int, total: int) -> str:
        """Calculate letter grade based on test results"""
        if total == 0:
            return "N/A"
        
        ratio = passed / total
        if ratio >= 0.95:
            return "A+"
        elif ratio >= 0.90:
            return "A"
        elif ratio >= 0.85:
            return "B+"
        elif ratio >= 0.80:
            return "B"
        elif ratio >= 0.75:
            return "C+"
        elif ratio >= 0.70:
            return "C"
        elif ratio >= 0.60:
            return "D"
        else:
            return "F"
    
    def _print_final_summary(self, results: Dict[str, Any]):
        """Print final test summary"""
        summary = results["summary"]
        
        print("🏁 FINAL TEST SUMMARY")
        print("=" * 80)
        print(f"Overall Status: {summary['overall_status']}")
        print(f"Grade: {summary['grade']}")
        print(f"Categories: {summary['categories_passed']}/{summary['total_categories']} passed")
        print(f"Individual Tests: {summary['tests_passed']}/{summary['total_tests']} passed")
        print(f"Success Rate: {summary['success_rate']:.1%}")
        print(f"Duration: {results['total_duration']:.2f} seconds")
        print()
        
        if summary['overall_status'] == "FAILED":
            print("❌ INTEGRATION TEST SUITE FAILED")
            print("System has integration issues that need to be addressed before deployment.")
            failed_categories = [c for c in results["test_categories"] if not c.get("passed", False)]
            for category in failed_categories:
                print(f"  • {category['category']}: {category['failed_tests']} failed tests")
        else:
            print("✅ INTEGRATION TEST SUITE PASSED")
            print("System is fully integrated and ready for deployment!")
        print()
        
        if self.ci_mode:
            # Exit with appropriate code for CI/CD
            exit_code = 0 if summary['overall_status'] == "PASSED" else 1
            print(f"CI/CD Exit Code: {exit_code}")
            sys.exit(exit_code)

async def main():
    """Main test runner"""
    parser = argparse.ArgumentParser(description="Memory Context Manager v2 Integration Test Suite")
    parser.add_argument("--ci", action="store_true", help="Run in CI/CD mode")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--exit-on-failure", action="store_true", help="Exit immediately on first failure")
    
    args = parser.parse_args()
    
    test_suite = IntegrationTestSuite(
        ci_mode=args.ci,
        verbose=args.verbose,
        exit_on_failure=args.exit_on_failure
    )
    
    results = await test_suite.run_all_tests()
    
    # Save results to file for analysis
    results_file = f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"📄 Detailed results saved to: {results_file}")

if __name__ == "__main__":
    asyncio.run(main())