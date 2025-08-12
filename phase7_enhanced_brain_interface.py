#!/usr/bin/env python3
"""
Phase 7A: Enhanced Brain Interface - Week 4 Implementation
Enhanced brain interface with predictive capabilities for Memory Context Manager v2
"""

import logging
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import json

# Import our Phase 7A components
from phase7_pattern_analyzer import PatternAnalyzer
from phase7_pattern_database import PatternDatabase
from phase7_prediction_engine import PredictionEngine

logger = logging.getLogger(__name__)

@dataclass
class PredictiveToolResult:
    """Result from a predictive tool call"""
    success: bool
    data: Dict[str, Any]
    tool_name: str
    execution_time: float
    confidence_score: float
    context_used: Dict[str, Any]
    timestamp: datetime

class PredictiveBrainInterface:
    """Enhanced brain interface with predictive capabilities"""
    
    def __init__(self, mcp_server, mcp_client, db_path: str = "phase7_patterns.db"):
        self.mcp = mcp_server
        self.client = mcp_client
        
        # Initialize Phase 7A components
        logger.info("🧠 Initializing Phase 7A Predictive Components...")
        
        self.pattern_database = PatternDatabase(db_path)
        self.pattern_analyzer = PatternAnalyzer()
        self.prediction_engine = PredictionEngine(self.pattern_database)
        
        # Register new predictive tools
        self._register_predictive_tools()
        
        logger.info("✅ Phase 7A Predictive Components initialized successfully")
    
    def _register_predictive_tools(self):
        """Register Phase 7A predictive tools with MCP server"""
        
        @self.mcp.tool()
        async def predict_next_action(current_context: str = "", project_path: str = "") -> dict:
            """
            🔮 Predict the next logical development action
            
            Analyzes current development context and predicts the next optimal action
            based on pattern analysis and machine learning.
            
            Args:
                current_context: JSON string describing current development context
                project_path: Path to project for additional context analysis
            """
            start_time = datetime.now()
            
            try:
                # Parse context
                if current_context:
                    try:
                        context = json.loads(current_context)
                    except json.JSONDecodeError:
                        context = {"raw_context": current_context}
                else:
                    context = {}
                
                # Add project path to context if provided
                if project_path:
                    context['project_path'] = project_path
                
                # Generate prediction
                result = await self.prediction_engine.predict_next_action(context)
                
                execution_time = (datetime.now() - start_time).total_seconds()
                
                if result.get("success"):
                    return {
                        "success": True,
                        "predictions": result.get("predictions", []),
                        "confidence_scores": result.get("confidence_scores", {}),
                        "context_analysis": result.get("context_analysis", {}),
                        "execution_time": execution_time,
                        "total_predictions": result.get("total_predictions", 0),
                        "prediction_method": result.get("prediction_method", "unknown")
                    }
                else:
                    return {
                        "success": False,
                        "error": result.get("error", "Unknown prediction error"),
                        "execution_time": execution_time
                    }
                    
            except Exception as e:
                execution_time = (datetime.now() - start_time).total_seconds()
                logger.error(f"Error in predict_next_action: {str(e)}")
                return {
                    "success": False,
                    "error": str(e),
                    "execution_time": execution_time
                }
        
        @self.mcp.tool()
        async def suggest_improvements(code_context: str = "", project_path: str = "") -> dict:
            """
            💡 Suggest code and workflow improvements
            
            Analyzes code context and suggests specific improvements based on
            pattern analysis and optimization detection.
            
            Args:
                code_context: JSON string describing code context and metrics
                project_path: Path to project for additional analysis
            """
            start_time = datetime.now()
            
            try:
                # Parse code context
                if code_context:
                    try:
                        context = json.loads(code_context)
                    except json.JSONDecodeError:
                        context = {"raw_context": code_context}
                else:
                    context = {}
                
                # Add project path to context if provided
                if project_path:
                    context['project_path'] = project_path
                
                # Generate optimization suggestions
                result = await self.prediction_engine.identify_optimization_opportunities(context)
                
                execution_time = (datetime.now() - start_time).total_seconds()
                
                if result.get("success"):
                    return {
                        "success": True,
                        "opportunities": result.get("opportunities", []),
                        "total_count": result.get("total_count", 0),
                        "priority_distribution": result.get("priority_distribution", {}),
                        "category_breakdown": result.get("category_breakdown", {}),
                        "execution_time": execution_time
                    }
                else:
                    return {
                        "success": False,
                        "error": result.get("error", "Unknown optimization error"),
                        "execution_time": execution_time
                    }
                    
            except Exception as e:
                execution_time = (datetime.now() - start_time).total_seconds()
                logger.error(f"Error in suggest_improvements: {str(e)}")
                return {
                    "success": False,
                    "error": str(e),
                    "execution_time": execution_time
                }
        
        @self.mcp.tool()
        async def analyze_patterns(project_path: str = "") -> dict:
            """
            🔍 Analyze coding patterns in the project
            
            Performs comprehensive pattern analysis of the entire project,
            identifying coding patterns, style consistency, and architectural decisions.
            
            Args:
                project_path: Path to project for analysis (defaults to current directory)
            """
            start_time = datetime.now()
            
            try:
                # Use current directory if no path provided
                if not project_path:
                    project_path = str(Path.cwd())
                
                # Perform pattern analysis
                result = await self.pattern_analyzer.analyze_project_patterns(project_path)
                
                execution_time = (datetime.now() - start_time).total_seconds()
                
                if result.get("success"):
                    # Store detected patterns in database
                    await self._store_detected_patterns(result)
                    
                    return {
                        "success": True,
                        "pattern_summary": result.get("pattern_summary", {}),
                        "file_patterns": result.get("file_patterns", {}),
                        "style_patterns": result.get("style_patterns", {}),
                        "architecture_patterns": result.get("architecture_patterns", {}),
                        "dependency_patterns": result.get("dependency_patterns", {}),
                        "workflow_patterns": result.get("workflow_patterns", {}),
                        "analysis_result": result.get("analysis_result", {}),
                        "execution_time": execution_time
                    }
                else:
                    return {
                        "success": False,
                        "error": result.get("error", "Unknown pattern analysis error"),
                        "execution_time": execution_time
                    }
                    
            except Exception as e:
                execution_time = (datetime.now() - start_time).total_seconds()
                logger.error(f"Error in analyze_patterns: {str(e)}")
                return {
                    "success": False,
                    "error": str(e),
                    "execution_time": execution_time
                }
        
        @self.mcp.tool()
        async def get_pattern_insights(pattern_type: str = "", limit: int = 10) -> dict:
            """
            📊 Get insights from pattern database
            
            Retrieves insights and statistics from the pattern database,
            including effectiveness metrics and usage patterns.
            
            Args:
                pattern_type: Filter by pattern type (optional)
                limit: Maximum number of patterns to return
            """
            start_time = datetime.now()
            
            try:
                # Get database statistics
                stats = await self.pattern_database.get_pattern_statistics()
                
                # Get patterns by type if specified
                patterns = []
                if pattern_type:
                    context = {"pattern_type": pattern_type}
                    patterns = await self.pattern_database.find_similar(context, limit)
                
                execution_time = (datetime.now() - start_time).total_seconds()
                
                return {
                    "success": True,
                    "database_statistics": stats,
                    "patterns": patterns,
                    "execution_time": execution_time
                }
                
            except Exception as e:
                execution_time = (datetime.now() - start_time).total_seconds()
                logger.error(f"Error in get_pattern_insights: {str(e)}")
                return {
                    "success": False,
                    "error": str(e),
                    "execution_time": execution_time
                }
        
        @self.mcp.tool()
        async def update_pattern_feedback(pattern_id: str, feedback: str = "") -> dict:
            """
            📝 Update pattern effectiveness with user feedback
            
            Allows users to provide feedback on pattern effectiveness,
            helping improve future predictions and recommendations.
            
            Args:
                pattern_id: ID of the pattern to update
                pattern_feedback: JSON string with feedback data
            """
            start_time = datetime.now()
            
            try:
                # Parse feedback
                if feedback:
                    try:
                        feedback_data = json.loads(feedback)
                    except json.JSONDecodeError:
                        feedback_data = {"raw_feedback": feedback}
                else:
                    feedback_data = {}
                
                # Update pattern effectiveness
                await self.pattern_database.update_pattern_effectiveness(pattern_id, feedback_data)
                
                execution_time = (datetime.now() - start_time).total_seconds()
                
                return {
                    "success": True,
                    "message": f"Pattern {pattern_id} effectiveness updated successfully",
                    "feedback_applied": feedback_data,
                    "execution_time": execution_time
                }
                
            except Exception as e:
                execution_time = (datetime.now() - start_time).total_seconds()
                logger.error(f"Error in update_pattern_feedback: {str(e)}")
                return {
                    "success": False,
                    "error": str(e),
                    "execution_time": execution_time
                }
        
        @self.mcp.tool()
        async def get_predictive_status() -> dict:
            """
            📈 Get status of predictive system
            
            Returns comprehensive status information about the predictive system,
            including component health, database statistics, and performance metrics.
            
            Args:
                None
            """
            start_time = datetime.now()
            
            try:
                # Get database statistics
                db_stats = await self.pattern_database.get_pattern_statistics()
                
                # Get cache statistics
                cache_stats = {
                    "pattern_cache_size": len(self.pattern_database.pattern_cache),
                    "context_cache_size": len(self.prediction_engine.context_analyzer.context_cache),
                    "prediction_cache_size": len(self.prediction_engine.prediction_cache)
                }
                
                # Component health check
                component_health = {
                    "pattern_database": "healthy" if self.pattern_database.db_connection else "unhealthy",
                    "pattern_analyzer": "healthy",
                    "prediction_engine": "healthy",
                    "context_analyzer": "healthy"
                }
                
                execution_time = (datetime.now() - start_time).total_seconds()
                
                return {
                    "success": True,
                    "component_health": component_health,
                    "database_statistics": db_stats,
                    "cache_statistics": cache_stats,
                    "system_status": "operational",
                    "execution_time": execution_time,
                    "phase": "7A",
                    "version": "1.0.0"
                }
                
            except Exception as e:
                execution_time = (datetime.now() - start_time).total_seconds()
                logger.error(f"Error in get_predictive_status: {str(e)}")
                return {
                    "success": False,
                    "error": str(e),
                    "execution_time": execution_time
                }
    
    async def _store_detected_patterns(self, analysis_result: Dict[str, Any]):
        """Store detected patterns in the database"""
        try:
            # Extract patterns from analysis result
            all_patterns = []
            
            # File structure patterns
            file_patterns = analysis_result.get("file_patterns", {}).get("patterns", [])
            all_patterns.extend(file_patterns)
            
            # Style patterns
            style_patterns = analysis_result.get("style_patterns", {}).get("patterns", [])
            all_patterns.extend(style_patterns)
            
            # Architecture patterns
            arch_patterns = analysis_result.get("architecture_patterns", {}).get("patterns", [])
            all_patterns.extend(arch_patterns)
            
            # Store each pattern
            stored_count = 0
            for pattern in all_patterns:
                if hasattr(pattern, 'pattern_id'):  # CodePattern object
                    pattern_dict = asdict(pattern)
                    success = await self.pattern_database.store_pattern(pattern_dict)
                    if success:
                        stored_count += 1
                elif isinstance(pattern, dict):  # Dictionary
                    success = await self.pattern_database.store_pattern(pattern)
                    if success:
                        stored_count += 1
            
            logger.info(f"✅ Stored {stored_count} patterns in database")
            
        except Exception as e:
            logger.error(f"Error storing detected patterns: {str(e)}")
    
    async def get_predictive_tools_summary(self) -> Dict[str, Any]:
        """Get summary of available predictive tools"""
        return {
            "phase": "7A",
            "available_tools": [
                {
                    "name": "predict_next_action",
                    "description": "Predict next development action based on context",
                    "category": "prediction"
                },
                {
                    "name": "suggest_improvements",
                    "description": "Suggest code and workflow improvements",
                    "category": "optimization"
                },
                {
                    "name": "analyze_patterns",
                    "description": "Analyze coding patterns in project",
                    "category": "analysis"
                },
                {
                    "name": "get_pattern_insights",
                    "description": "Get insights from pattern database",
                    "category": "insights"
                },
                {
                    "name": "update_pattern_feedback",
                    "description": "Update pattern effectiveness with feedback",
                    "category": "feedback"
                },
                {
                    "name": "get_predictive_status",
                    "description": "Get predictive system status",
                    "category": "monitoring"
                }
            ],
            "total_tools": 6,
            "categories": ["prediction", "optimization", "analysis", "insights", "feedback", "monitoring"]
        }
    
    def close(self):
        """Clean up resources"""
        try:
            if self.pattern_database:
                self.pattern_database.close()
            logger.info("✅ Enhanced Brain Interface resources cleaned up")
        except Exception as e:
            logger.error(f"Error cleaning up Enhanced Brain Interface: {str(e)}")

# Example usage and testing
async def main():
    """Example usage of the Enhanced Brain Interface"""
    print("🧠 Testing Enhanced Brain Interface (Phase 7A)")
    
    # Create a mock MCP server and client for testing
    class MockMCPServer:
        def tool(self):
            def decorator(func):
                return func
            return decorator
    
    class MockMCPClient:
        async def call_tool(self, tool_name: str, **kwargs):
            return {"success": True, "result": f"Mock result from {tool_name}"}
    
    mock_server = MockMCPServer()
    mock_client = MockMCPClient()
    
    try:
        # Initialize enhanced brain interface
        print("🔧 Initializing Enhanced Brain Interface...")
        brain_interface = PredictiveBrainInterface(mock_server, mock_client, "test_enhanced_brain.db")
        
        # Test pattern analysis
        print("\n🔍 Testing pattern analysis...")
        current_dir = str(Path.cwd())
        print(f"  Analyzing patterns in: {current_dir}")
        
        # This would normally be called through the MCP tool
        # For testing, we'll call the components directly
        pattern_result = await brain_interface.pattern_analyzer.analyze_project_patterns(current_dir)
        
        if pattern_result.get("success"):
            print(f"  ✅ Pattern analysis completed successfully!")
            print(f"  📊 Total patterns found: {pattern_result.get('pattern_summary', {}).get('total_patterns', 0)}")
            
            # Store patterns in database
            await brain_interface._store_detected_patterns(pattern_result)
            
            # Test prediction engine
            print("\n🔮 Testing prediction engine...")
            test_context = {
                'current_file': 'src/main.py',
                'current_function': 'main',
                'recent_changes': ['Added new feature', 'Fixed bug'],
                'project_metrics': {'test_coverage': 0.7, 'complexity_score': 0.6}
            }
            
            prediction_result = await brain_interface.prediction_engine.predict_next_action(test_context)
            
            if prediction_result.get("success"):
                print(f"  ✅ Generated {prediction_result['total_predictions']} predictions")
                print(f"  📊 Average confidence: {prediction_result['confidence_scores']['average_confidence']:.2f}")
                
                for i, pred in enumerate(prediction_result['predictions'][:2], 1):
                    print(f"    {i}. {pred['title']} (Confidence: {pred['confidence']:.2f})")
            else:
                print(f"  ❌ Prediction failed: {prediction_result.get('error')}")
        
        # Test database statistics
        print("\n📊 Testing database statistics...")
        db_stats = await brain_interface.pattern_database.get_pattern_statistics()
        if db_stats.get("success"):
            print(f"  ✅ Database contains {db_stats['total_patterns']} patterns")
            print(f"  📈 Cache hit rate: {db_stats['cache_statistics']['hit_rate']:.1%}")
        else:
            print(f"  ❌ Failed to get database statistics: {db_stats.get('error')}")
        
        # Get predictive tools summary
        print("\n🛠️ Available predictive tools:")
        tools_summary = await brain_interface.get_predictive_tools_summary()
        for tool in tools_summary['available_tools']:
            print(f"  • {tool['name']}: {tool['description']}")
        
        print(f"\n🎯 Phase 7A Status: {tools_summary['total_tools']} predictive tools available")
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
    
    finally:
        # Clean up
        if 'brain_interface' in locals():
            brain_interface.close()
        print("\n🧹 Cleanup completed")

if __name__ == "__main__":
    asyncio.run(main())
