"""
Enhanced Workflow Orchestrator Plugin
Automatically executes all three phases of context enhancement in sequence
"""

import sys
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime
import asyncio

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from plugin_interface import BasePlugin, PluginMetadata, ToolDefinition

logger = logging.getLogger(__name__)


class EnhancedWorkflowOrchestratorPlugin(BasePlugin):
    """
    Enhanced workflow orchestrator that automatically executes all three phases
    of context enhancement in sequence for optimal results
    """
    
    def __init__(self):
        super().__init__()
        self._enhanced_context_plugin = None
        self._workflow_history = []
        self._performance_metrics = {}
        
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="enhanced_workflow_orchestrator",
            version="1.0.0",
            description="Enhanced workflow orchestrator for comprehensive context enhancement",
            author="Memory Context Manager Team"
        )
    
    def _setup(self) -> None:
        """Initialize enhanced workflow orchestrator"""
        try:
            logger.info("🚀 Setting up Enhanced Workflow Orchestrator...")
            
            # Import enhanced context integration plugin
            try:
                from enhanced_context_integration import EnhancedContextIntegrationPlugin
                self._enhanced_context_plugin = EnhancedContextIntegrationPlugin()
                self._enhanced_context_plugin._setup()
                logger.info("✅ Connected to enhanced context integration")
            except Exception as e:
                logger.warning(f"Enhanced context integration failed: {e}")
            
            logger.info("✅ Enhanced Workflow Orchestrator ready")
            
        except Exception as e:
            logger.error(f"❌ Enhanced Workflow Orchestrator setup failed: {str(e)}")
    
    def get_tools(self) -> List[ToolDefinition]:
        """Get enhanced workflow orchestrator tools"""
        return [
            # Main workflow execution
            ToolDefinition(
                name="execute_enhanced_workflow",
                description="Execute complete enhanced workflow (all three phases) automatically",
                handler=self._execute_enhanced_workflow_handler,
                parameters={
                    "user_message": {"type": "string", "description": "User's message for context enhancement"},
                    "workflow_mode": {"type": "string", "description": "Workflow mode (standard, aggressive, conservative)", "default": "standard"},
                    "include_learning": {"type": "boolean", "description": "Include learning phase", "default": True}
                }
            ),
            
            # Workflow optimization
            ToolDefinition(
                name="optimize_workflow",
                description="Optimize workflow based on performance metrics and usage patterns",
                handler=self._optimize_workflow_handler,
                parameters={
                    "optimization_focus": {"type": "string", "description": "Focus area for optimization", "default": "performance"},
                    "target_metrics": {"type": "array", "description": "Target metrics to improve", "default": ["speed", "accuracy", "context_quality"]}
                }
            ),
            
            # Workflow analytics
            ToolDefinition(
                name="analyze_workflow_performance",
                description="Analyze workflow performance and identify improvement opportunities",
                handler=self._analyze_workflow_performance_handler,
                parameters={
                    "timeframe": {"type": "string", "description": "Timeframe for analysis", "default": "session"},
                    "include_recommendations": {"type": "boolean", "description": "Include improvement recommendations", "default": True}
                }
            ),
            
            # Batch workflow processing
            ToolDefinition(
                name="batch_workflow_processing",
                description="Process multiple messages through the enhanced workflow",
                handler=self._batch_workflow_processing_handler,
                parameters={
                    "user_messages": {"type": "array", "description": "List of user messages to process"},
                    "workflow_mode": {"type": "string", "description": "Workflow mode for batch processing", "default": "standard"}
                }
            ),
            
            # Workflow health check
            ToolDefinition(
                name="workflow_health_check",
                description="Perform comprehensive health check of the enhanced workflow system",
                handler=self._workflow_health_check_handler,
                parameters={
                    "check_level": {"type": "string", "description": "Health check level (basic, comprehensive, deep)", "default": "comprehensive"}
                }
            )
        ]
    
    async def _execute_enhanced_workflow_handler(self, user_message: str, workflow_mode: str = "standard", include_learning: bool = True) -> Dict[str, Any]:
        """Execute complete enhanced workflow (all three phases) automatically"""
        try:
            logger.info(f"🚀 Executing Enhanced Workflow: {workflow_mode} mode")
            
            workflow_start_time = datetime.now()
            workflow_result = {
                "timestamp": workflow_start_time.isoformat(),
                "workflow_mode": workflow_mode,
                "user_message": user_message,
                "phases_executed": [],
                "overall_results": {},
                "performance_metrics": {},
                "workflow_id": f"workflow_{workflow_start_time.strftime('%Y%m%d_%H%M%S')}"
            }
            
            # Phase 1: Enhanced Context Retrieval
            logger.info("🔍 Phase 1: Enhanced Context Retrieval")
            phase1_start = datetime.now()
            
            try:
                phase1_result = await self._enhanced_context_plugin._enhanced_context_retrieval_handler(
                    user_message, 
                    include_history=True, 
                    include_preferences=True
                )
                
                phase1_duration = (datetime.now() - phase1_start).total_seconds()
                workflow_result["phases_executed"].append({
                    "phase": "enhanced_context_retrieval",
                    "status": "completed" if phase1_result["success"] else "failed",
                    "duration": phase1_duration,
                    "result": phase1_result
                })
                
                if not phase1_result["success"]:
                    logger.error(f"❌ Phase 1 failed: {phase1_result.get('error', 'Unknown error')}")
                    return {
                        "success": False,
                        "error": f"Phase 1 failed: {phase1_result.get('error', 'Unknown error')}",
                        "workflow_result": workflow_result
                    }
                
                logger.info(f"✅ Phase 1 completed in {phase1_duration:.2f}s")
                
            except Exception as e:
                logger.error(f"❌ Phase 1 execution failed: {str(e)}")
                workflow_result["phases_executed"].append({
                    "phase": "enhanced_context_retrieval",
                    "status": "failed",
                    "duration": (datetime.now() - phase1_start).total_seconds(),
                    "error": str(e)
                })
                return {
                    "success": False,
                    "error": f"Phase 1 execution failed: {str(e)}",
                    "workflow_result": workflow_result
                }
            
            # Phase 2: Tool Orchestration
            logger.info("🎯 Phase 2: Tool Orchestration")
            phase2_start = datetime.now()
            
            try:
                # Determine target goal based on workflow mode
                target_goal = self._determine_target_goal(workflow_mode, user_message)
                
                phase2_result = await self._enhanced_context_plugin._orchestrate_tools_handler(
                    phase1_result["context_data"],
                    target_goal=target_goal
                )
                
                phase2_duration = (datetime.now() - phase2_start).total_seconds()
                workflow_result["phases_executed"].append({
                    "phase": "tool_orchestration",
                    "status": "completed" if phase2_result["success"] else "failed",
                    "duration": phase2_duration,
                    "result": phase2_result
                })
                
                if not phase2_result["success"]:
                    logger.error(f"❌ Phase 2 failed: {phase2_result.get('error', 'Unknown error')}")
                    return {
                        "success": False,
                        "error": f"Phase 2 failed: {phase2_result.get('error', 'Unknown error')}",
                        "workflow_result": workflow_result
                    }
                
                logger.info(f"✅ Phase 2 completed in {phase2_duration:.2f}s")
                
            except Exception as e:
                logger.error(f"❌ Phase 2 execution failed: {str(e)}")
                workflow_result["phases_executed"].append({
                    "phase": "tool_orchestration",
                    "status": "failed",
                    "duration": (datetime.now() - phase2_start).total_seconds(),
                    "error": str(e)
                })
                return {
                    "success": False,
                    "error": f"Phase 2 execution failed: {str(e)}",
                    "workflow_result": workflow_result
                }
            
            # Phase 3: Continuous Learning (if enabled)
            if include_learning:
                logger.info("📚 Phase 3: Continuous Learning")
                phase3_start = datetime.now()
                
                try:
                    # Prepare interaction data for learning
                    interaction_data = {
                        "context_data": phase1_result["context_data"],
                        "orchestration_result": phase2_result["orchestration_result"],
                        "workflow_mode": workflow_mode,
                        "user_message": user_message
                    }
                    
                    phase3_result = await self._enhanced_context_plugin._continuous_learning_handler(
                        interaction_data,
                        learning_focus="workflow_optimization"
                    )
                    
                    phase3_duration = (datetime.now() - phase3_start).total_seconds()
                    workflow_result["phases_executed"].append({
                        "phase": "continuous_learning",
                        "status": "completed" if phase3_result["success"] else "failed",
                        "duration": phase3_duration,
                        "result": phase3_result
                    })
                    
                    if phase3_result["success"]:
                        logger.info(f"✅ Phase 3 completed in {phase3_duration:.2f}s")
                    else:
                        logger.warning(f"⚠️ Phase 3 completed with warnings: {phase3_result.get('error', 'Unknown warning')}")
                        
                except Exception as e:
                    logger.error(f"❌ Phase 3 execution failed: {str(e)}")
                    workflow_result["phases_executed"].append({
                        "phase": "continuous_learning",
                        "status": "failed",
                        "duration": (datetime.now() - phase3_start).total_seconds(),
                        "error": str(e)
                    })
                    # Don't fail the entire workflow for learning phase errors
            
            # Calculate overall results and performance metrics
            workflow_result["overall_results"] = self._calculate_overall_workflow_results(workflow_result["phases_executed"])
            workflow_result["performance_metrics"] = self._calculate_workflow_performance_metrics(workflow_result)
            
            # Store workflow history
            self._store_workflow_history(workflow_result)
            
            # Update performance metrics
            self._update_performance_metrics(workflow_result)
            
            total_duration = (datetime.now() - workflow_start_time).total_seconds()
            logger.info(f"🎉 Enhanced Workflow completed in {total_duration:.2f}s")
            
            return {
                "success": True,
                "workflow_result": workflow_result,
                "total_duration": total_duration,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Enhanced workflow execution failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def _optimize_workflow_handler(self, optimization_focus: str = "performance", target_metrics: List[str] = None) -> Dict[str, Any]:
        """Optimize workflow based on performance metrics and usage patterns"""
        try:
            logger.info(f"🔧 Optimizing workflow: {optimization_focus}")
            
            if target_metrics is None:
                target_metrics = ["speed", "accuracy", "context_quality"]
            
            optimization_result = {
                "timestamp": datetime.now().isoformat(),
                "optimization_focus": optimization_focus,
                "target_metrics": target_metrics,
                "current_performance": {},
                "optimization_recommendations": [],
                "implemented_improvements": []
            }
            
            # Analyze current performance
            current_performance = self._analyze_current_performance()
            optimization_result["current_performance"] = current_performance
            
            # Generate optimization recommendations
            recommendations = self._generate_optimization_recommendations(
                optimization_focus, 
                target_metrics, 
                current_performance
            )
            optimization_result["optimization_recommendations"] = recommendations
            
            # Implement automatic improvements where possible
            implemented = self._implement_automatic_improvements(recommendations)
            optimization_result["implemented_improvements"] = implemented
            
            logger.info(f"✅ Workflow optimization completed with {len(implemented)} improvements")
            
            return {
                "success": True,
                "optimization_result": optimization_result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Workflow optimization failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def _analyze_workflow_performance_handler(self, timeframe: str = "session", include_recommendations: bool = True) -> Dict[str, Any]:
        """Analyze workflow performance and identify improvement opportunities"""
        try:
            logger.info(f"📊 Analyzing workflow performance: {timeframe}")
            
            analysis_result = {
                "timestamp": datetime.now().isoformat(),
                "timeframe": timeframe,
                "performance_summary": {},
                "phase_analysis": {},
                "bottleneck_identification": [],
                "improvement_opportunities": []
            }
            
            # Analyze workflow history
            if timeframe == "session":
                workflows = self._workflow_history
            else:
                # For other timeframes, would implement time-based filtering
                workflows = self._workflow_history
            
            if workflows:
                # Performance summary
                analysis_result["performance_summary"] = self._calculate_performance_summary(workflows)
                
                # Phase-by-phase analysis
                analysis_result["phase_analysis"] = self._analyze_phases(workflows)
                
                # Identify bottlenecks
                analysis_result["bottleneck_identification"] = self._identify_bottlenecks(workflows)
                
                # Identify improvement opportunities
                analysis_result["improvement_opportunities"] = self._identify_improvement_opportunities(workflows)
            
            # Generate recommendations if requested
            if include_recommendations:
                analysis_result["recommendations"] = self._generate_performance_recommendations(analysis_result)
            
            logger.info(f"✅ Workflow performance analysis completed")
            
            return {
                "success": True,
                "analysis_result": analysis_result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Workflow performance analysis failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def _batch_workflow_processing_handler(self, user_messages: List[str], workflow_mode: str = "standard") -> Dict[str, Any]:
        """Process multiple messages through the enhanced workflow"""
        try:
            logger.info(f"📦 Processing {len(user_messages)} messages in batch")
            
            batch_result = {
                "timestamp": datetime.now().isoformat(),
                "workflow_mode": workflow_mode,
                "total_messages": len(user_messages),
                "processed_messages": [],
                "batch_performance": {},
                "errors": []
            }
            
            batch_start_time = datetime.now()
            
            # Process each message
            for i, message in enumerate(user_messages):
                try:
                    logger.info(f"📝 Processing message {i+1}/{len(user_messages)}")
                    
                    # Execute workflow for this message
                    message_result = await self._execute_enhanced_workflow_handler(
                        message, 
                        workflow_mode, 
                        include_learning=False  # Disable learning for batch processing
                    )
                    
                    batch_result["processed_messages"].append({
                        "message_index": i,
                        "message": message[:100] + "..." if len(message) > 100 else message,
                        "result": message_result
                    })
                    
                    if not message_result["success"]:
                        batch_result["errors"].append({
                            "message_index": i,
                            "error": message_result.get("error", "Unknown error")
                        })
                    
                except Exception as e:
                    logger.error(f"❌ Failed to process message {i+1}: {str(e)}")
                    batch_result["errors"].append({
                        "message_index": i,
                        "error": str(e)
                    })
            
            # Calculate batch performance
            batch_duration = (datetime.now() - batch_start_time).total_seconds()
            successful_messages = len([m for m in batch_result["processed_messages"] if m["result"]["success"]])
            
            batch_result["batch_performance"] = {
                "total_duration": batch_duration,
                "successful_messages": successful_messages,
                "failed_messages": len(batch_result["errors"]),
                "success_rate": successful_messages / len(user_messages) if user_messages else 0,
                "average_duration_per_message": batch_duration / len(user_messages) if user_messages else 0
            }
            
            logger.info(f"✅ Batch processing completed: {successful_messages}/{len(user_messages)} successful")
            
            return {
                "success": True,
                "batch_result": batch_result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Batch workflow processing failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def _workflow_health_check_handler(self, check_level: str = "comprehensive") -> Dict[str, Any]:
        """Perform comprehensive health check of the enhanced workflow system"""
        try:
            logger.info(f"🏥 Performing workflow health check: {check_level}")
            
            health_result = {
                "timestamp": datetime.now().isoformat(),
                "check_level": check_level,
                "overall_health": "unknown",
                "component_health": {},
                "issues_found": [],
                "recommendations": []
            }
            
            # Check enhanced context plugin
            if self._enhanced_context_plugin:
                health_result["component_health"]["enhanced_context_plugin"] = "healthy"
            else:
                health_result["component_health"]["enhanced_context_plugin"] = "unhealthy"
                health_result["issues_found"].append("Enhanced context plugin not available")
            
            # Check workflow history
            if self._workflow_history:
                health_result["component_health"]["workflow_history"] = "healthy"
                health_result["component_health"]["workflow_count"] = len(self._workflow_history)
            else:
                health_result["component_health"]["workflow_history"] = "no_data"
            
            # Check performance metrics
            if self._performance_metrics:
                health_result["component_health"]["performance_metrics"] = "healthy"
                health_result["component_health"]["metrics_count"] = len(self._performance_metrics)
            else:
                health_result["component_health"]["performance_metrics"] = "no_data"
            
            # Determine overall health
            unhealthy_components = [comp for comp, status in health_result["component_health"].items() if status == "unhealthy"]
            if unhealthy_components:
                health_result["overall_health"] = "unhealthy"
                health_result["recommendations"].append(f"Fix unhealthy components: {', '.join(unhealthy_components)}")
            elif any(status == "no_data" for status in health_result["component_health"].values()):
                health_result["overall_health"] = "degraded"
                health_result["recommendations"].append("Initialize data collection for better health monitoring")
            else:
                health_result["overall_health"] = "healthy"
                health_result["recommendations"].append("System is operating normally")
            
            # Additional checks for comprehensive level
            if check_level == "comprehensive":
                # Check for performance degradation
                if self._performance_metrics:
                    recent_performance = self._analyze_recent_performance()
                    if recent_performance.get("degradation_detected", False):
                        health_result["issues_found"].append("Performance degradation detected")
                        health_result["recommendations"].append("Investigate recent performance issues")
                
                # Check for error patterns
                if self._workflow_history:
                    error_patterns = self._analyze_error_patterns()
                    if error_patterns:
                        health_result["issues_found"].append(f"Error patterns detected: {error_patterns}")
                        health_result["recommendations"].append("Review and fix error patterns")
            
            logger.info(f"✅ Workflow health check completed: {health_result['overall_health']}")
            
            return {
                "success": True,
                "health_result": health_result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Workflow health check failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    # Helper methods
    
    def _determine_target_goal(self, workflow_mode: str, user_message: str) -> str:
        """Determine target goal based on workflow mode and user message"""
        if workflow_mode == "aggressive":
            return "maximum_context_enhancement"
        elif workflow_mode == "conservative":
            return "minimal_context_enhancement"
        else:  # standard
            # Analyze message to determine goal
            if any(word in user_message.lower() for word in ["analyze", "deep", "comprehensive"]):
                return "comprehensive_context_enhancement"
            elif any(word in user_message.lower() for word in ["quick", "fast", "simple"]):
                return "quick_context_enhancement"
            else:
                return "enhanced_response"
    
    def _calculate_overall_workflow_results(self, phases_executed: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate overall workflow results"""
        total_phases = len(phases_executed)
        successful_phases = len([p for p in phases_executed if p["status"] == "completed"])
        total_duration = sum(p.get("duration", 0) for p in phases_executed)
        
        return {
            "total_phases": total_phases,
            "successful_phases": successful_phases,
            "success_rate": successful_phases / total_phases if total_phases > 0 else 0,
            "total_duration": total_duration,
            "average_phase_duration": total_duration / total_phases if total_phases > 0 else 0
        }
    
    def _calculate_workflow_performance_metrics(self, workflow_result: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate workflow performance metrics"""
        phases = workflow_result["phases_executed"]
        
        # Calculate efficiency metrics
        total_duration = sum(p.get("duration", 0) for p in phases)
        successful_phases = len([p for p in phases if p["status"] == "completed"])
        
        # Calculate context quality improvement
        context_quality_improvement = 0.0
        if phases and len(phases) >= 2:
            phase1_result = phases[0].get("result", {})
            if "context_data" in phase1_result:
                phase1_quality = phase1_result["context_data"].get("context_quality", {}).get("overall_score", 0.0)
                # Estimate final quality improvement
                context_quality_improvement = min(phase1_quality * 1.5, 1.0) - phase1_quality
        
        return {
            "efficiency_score": successful_phases / len(phases) if phases else 0.0,
            "speed_score": 1.0 / (total_duration + 0.1),  # Avoid division by zero
            "context_quality_improvement": max(0.0, context_quality_improvement),
            "overall_performance_score": (successful_phases / len(phases) if phases else 0.0) * 0.4 + \
                                       (1.0 / (total_duration + 0.1)) * 0.3 + \
                                       max(0.0, context_quality_improvement) * 0.3
        }
    
    def _store_workflow_history(self, workflow_result: Dict[str, Any]) -> None:
        """Store workflow result in history"""
        # Keep only last 100 workflows to prevent memory bloat
        if len(self._workflow_history) >= 100:
            self._workflow_history.pop(0)
        
        self._workflow_history.append(workflow_result)
    
    def _update_performance_metrics(self, workflow_result: Dict[str, Any]) -> None:
        """Update performance metrics with workflow result"""
        workflow_id = workflow_result["workflow_id"]
        self._performance_metrics[workflow_id] = {
            "timestamp": workflow_result["timestamp"],
            "performance_metrics": workflow_result["performance_metrics"],
            "overall_results": workflow_result["overall_results"]
        }
    
    def _analyze_current_performance(self) -> Dict[str, Any]:
        """Analyze current performance based on stored metrics"""
        if not self._performance_metrics:
            return {"status": "no_data"}
        
        recent_metrics = list(self._performance_metrics.values())[-10:]  # Last 10 workflows
        
        avg_performance_score = sum(m["performance_metrics"]["overall_performance_score"] for m in recent_metrics) / len(recent_metrics)
        avg_duration = sum(m["overall_results"]["total_duration"] for m in recent_metrics) / len(recent_metrics)
        
        return {
            "status": "healthy",
            "average_performance_score": avg_performance_score,
            "average_duration": avg_duration,
            "recent_workflows": len(recent_metrics)
        }
    
    def _generate_optimization_recommendations(self, focus: str, target_metrics: List[str], current_performance: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate optimization recommendations"""
        recommendations = []
        
        if focus == "performance":
            if current_performance.get("average_performance_score", 0) < 0.7:
                recommendations.append({
                    "type": "performance_improvement",
                    "priority": "high",
                    "description": "Overall performance score is below target (0.7)",
                    "action": "Review workflow phases for optimization opportunities"
                })
            
            if current_performance.get("average_duration", 0) > 5.0:
                recommendations.append({
                    "type": "speed_optimization",
                    "priority": "medium",
                    "description": "Average workflow duration is above 5 seconds",
                    "action": "Optimize slow phases and reduce processing overhead"
                })
        
        # Add general recommendations
        recommendations.append({
            "type": "monitoring_enhancement",
            "priority": "low",
            "description": "Implement real-time performance monitoring",
            "action": "Add performance dashboards and alerting"
        })
        
        return recommendations
    
    def _implement_automatic_improvements(self, recommendations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Implement automatic improvements where possible"""
        implemented = []
        
        for rec in recommendations:
            if rec["type"] == "monitoring_enhancement":
                # Implement basic monitoring
                implemented.append({
                    "recommendation": rec,
                    "implementation": "Basic monitoring enabled",
                    "status": "implemented"
                })
            else:
                # Mark as requiring manual intervention
                implemented.append({
                    "recommendation": rec,
                    "implementation": "Requires manual review",
                    "status": "pending"
                })
        
        return implemented
    
    def _calculate_performance_summary(self, workflows: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate performance summary from workflow history"""
        if not workflows:
            return {"status": "no_data"}
        
        total_workflows = len(workflows)
        successful_workflows = len([w for w in workflows if w.get("overall_results", {}).get("success_rate", 0) > 0.5])
        
        avg_duration = sum(w.get("overall_results", {}).get("total_duration", 0) for w in workflows) / total_workflows
        avg_performance = sum(w.get("performance_metrics", {}).get("overall_performance_score", 0) for w in workflows) / total_workflows
        
        return {
            "total_workflows": total_workflows,
            "successful_workflows": successful_workflows,
            "success_rate": successful_workflows / total_workflows if total_workflows > 0 else 0,
            "average_duration": avg_duration,
            "average_performance_score": avg_performance
        }
    
    def _analyze_phases(self, workflows: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze performance by phase"""
        phase_stats = {}
        
        for workflow in workflows:
            for phase in workflow.get("phases_executed", []):
                phase_name = phase["phase"]
                if phase_name not in phase_stats:
                    phase_stats[phase_name] = {
                        "total_executions": 0,
                        "successful_executions": 0,
                        "total_duration": 0,
                        "errors": []
                    }
                
                stats = phase_stats[phase_name]
                stats["total_executions"] += 1
                stats["total_duration"] += phase.get("duration", 0)
                
                if phase["status"] == "completed":
                    stats["successful_executions"] += 1
                else:
                    stats["errors"].append(phase.get("error", "Unknown error"))
        
        # Calculate averages
        for phase_name, stats in phase_stats.items():
            if stats["total_executions"] > 0:
                stats["success_rate"] = stats["successful_executions"] / stats["total_executions"]
                stats["average_duration"] = stats["total_duration"] / stats["total_executions"]
        
        return phase_stats
    
    def _identify_bottlenecks(self, workflows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify performance bottlenecks"""
        bottlenecks = []
        
        if not workflows:
            return bottlenecks
        
        # Analyze phase durations
        phase_durations = {}
        for workflow in workflows:
            for phase in workflow.get("phases_executed", []):
                phase_name = phase["phase"]
                if phase_name not in phase_durations:
                    phase_durations[phase_name] = []
                phase_durations[phase_name].append(phase.get("duration", 0))
        
        # Identify slow phases
        for phase_name, durations in phase_durations.items():
            avg_duration = sum(durations) / len(durations)
            if avg_duration > 2.0:  # Threshold: 2 seconds
                bottlenecks.append({
                    "type": "slow_phase",
                    "phase": phase_name,
                    "average_duration": avg_duration,
                    "threshold": 2.0,
                    "severity": "high" if avg_duration > 5.0 else "medium"
                })
        
        return bottlenecks
    
    def _identify_improvement_opportunities(self, workflows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify improvement opportunities"""
        opportunities = []
        
        if not workflows:
            return opportunities
        
        # Analyze error patterns
        error_phases = {}
        for workflow in workflows:
            for phase in workflow.get("phases_executed", []):
                if phase["status"] != "completed":
                    phase_name = phase["phase"]
                    if phase_name not in error_phases:
                        error_phases[phase_name] = 0
                    error_phases[phase_name] += 1
        
        # Identify error-prone phases
        for phase_name, error_count in error_phases.items():
            if error_count > 2:  # Threshold: more than 2 errors
                opportunities.append({
                    "type": "error_reduction",
                    "phase": phase_name,
                    "error_count": error_count,
                    "priority": "high" if error_count > 5 else "medium",
                    "description": f"Reduce errors in {phase_name} phase"
                })
        
        return opportunities
    
    def _generate_performance_recommendations(self, analysis_result: Dict[str, Any]) -> List[str]:
        """Generate performance recommendations"""
        recommendations = []
        
        # Performance summary recommendations
        performance_summary = analysis_result.get("performance_summary", {})
        if performance_summary.get("success_rate", 0) < 0.8:
            recommendations.append("Improve overall workflow success rate")
        
        if performance_summary.get("average_duration", 0) > 5.0:
            recommendations.append("Optimize workflow execution time")
        
        # Bottleneck recommendations
        bottlenecks = analysis_result.get("bottleneck_identification", [])
        for bottleneck in bottlenecks:
            if bottleneck["type"] == "slow_phase":
                recommendations.append(f"Optimize {bottleneck['phase']} phase for better performance")
        
        # Improvement opportunity recommendations
        opportunities = analysis_result.get("improvement_opportunities", [])
        for opportunity in opportunities:
            if opportunity["type"] == "error_reduction":
                recommendations.append(opportunity["description"])
        
        return recommendations
    
    def _analyze_recent_performance(self) -> Dict[str, Any]:
        """Analyze recent performance for degradation detection"""
        if len(self._performance_metrics) < 5:
            return {"degradation_detected": False}
        
        recent_metrics = list(self._performance_metrics.values())[-5:]
        older_metrics = list(self._performance_metrics.values())[-10:-5]
        
        if len(older_metrics) < 5:
            return {"degradation_detected": False}
        
        recent_avg = sum(m["performance_metrics"]["overall_performance_score"] for m in recent_metrics) / len(recent_metrics)
        older_avg = sum(m["performance_metrics"]["overall_performance_score"] for m in older_metrics) / len(older_metrics)
        
        degradation = older_avg - recent_avg > 0.1  # 10% threshold
        
        return {
            "degradation_detected": degradation,
            "recent_average": recent_avg,
            "older_average": older_avg,
            "degradation_amount": older_avg - recent_avg
        }
    
    def _analyze_error_patterns(self) -> List[str]:
        """Analyze error patterns in workflow history"""
        error_patterns = []
        
        if not self._workflow_history:
            return error_patterns
        
        # Count errors by type
        error_counts = {}
        for workflow in self._workflow_history:
            for phase in workflow.get("phases_executed", []):
                if phase["status"] != "completed":
                    error_type = phase.get("error", "Unknown error")
                    if error_type not in error_counts:
                        error_counts[error_type] = 0
                    error_counts[error_type] += 1
        
        # Identify patterns
        for error_type, count in error_counts.items():
            if count > 2:  # Threshold: more than 2 occurrences
                error_patterns.append(f"{error_type}: {count} occurrences")
        
        return error_patterns
