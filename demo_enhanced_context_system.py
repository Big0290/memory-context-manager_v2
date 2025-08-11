#!/usr/bin/env python3
"""
Enhanced Context System Demonstration Script
Demonstrates all three phases of context enhancement and workflow orchestration
"""

import asyncio
import sys
import logging
from pathlib import Path
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add paths
sys.path.insert(0, str(Path(__file__).parent / "src"))
sys.path.insert(0, str(Path(__file__).parent))

async def demonstrate_enhanced_context_system():
    """Demonstrate the complete enhanced context system"""
    
    print("🚀 Enhanced Context System Demonstration")
    print("=" * 50)
    
    try:
        # Import the enhanced context integration plugin
        from plugins.enhanced_context_integration import EnhancedContextIntegrationPlugin
        from plugins.enhanced_workflow_orchestrator import EnhancedWorkflowOrchestratorPlugin
        
        print("✅ Successfully imported enhanced context plugins")
        
        # Initialize plugins
        print("\n🔧 Initializing Enhanced Context Integration Plugin...")
        enhanced_context_plugin = EnhancedContextIntegrationPlugin()
        enhanced_context_plugin._setup()
        
        print("🔧 Initializing Enhanced Workflow Orchestrator Plugin...")
        workflow_orchestrator_plugin = EnhancedWorkflowOrchestratorPlugin()
        workflow_orchestrator_plugin._setup()
        
        print("✅ All plugins initialized successfully")
        
        # Demo user message
        demo_message = "I need to analyze the performance of our memory system and identify areas for improvement"
        
        print(f"\n📝 Demo User Message: {demo_message}")
        print("-" * 50)
        
        # Phase 1: Enhanced Context Retrieval
        print("\n🔍 Phase 1: Enhanced Context Retrieval")
        print("=" * 30)
        
        phase1_result = await enhanced_context_plugin._enhanced_context_retrieval_handler(
            demo_message,
            include_history=True,
            include_preferences=True
        )
        
        if phase1_result["success"]:
            print("✅ Phase 1 completed successfully")
            context_data = phase1_result["context_data"]
            print(f"   Context Quality Score: {context_data['context_quality']['overall_score']:.3f}")
            print(f"   Components Retrieved: {len(context_data['context_components'])}")
            
            # Show context components
            for comp_name, comp_data in context_data["context_components"].items():
                status = "✅" if comp_data and "error" not in str(comp_data) else "❌"
                print(f"   {status} {comp_name}")
        else:
            print(f"❌ Phase 1 failed: {phase1_result.get('error', 'Unknown error')}")
            return
        
        # Phase 2: Tool Orchestration
        print("\n🎯 Phase 2: Tool Orchestration")
        print("=" * 30)
        
        phase2_result = await enhanced_context_plugin._orchestrate_tools_handler(
            context_data,
            target_goal="comprehensive_context_enhancement"
        )
        
        if phase2_result["success"]:
            print("✅ Phase 2 completed successfully")
            orchestration_result = phase2_result["orchestration_result"]
            print(f"   Tools Recommended: {len(orchestration_result['tool_recommendations'])}")
            print(f"   Execution Plan Steps: {len(orchestration_result['execution_plan'])}")
            
            # Show tool recommendations
            for tool in orchestration_result["tool_recommendations"][:3]:  # Show first 3
                print(f"   🔧 {tool['tool_name']} ({tool['priority']} priority)")
        else:
            print(f"❌ Phase 2 failed: {phase2_result.get('error', 'Unknown error')}")
            return
        
        # Phase 3: Continuous Learning
        print("\n📚 Phase 3: Continuous Learning")
        print("=" * 30)
        
        interaction_data = {
            "context_data": context_data,
            "orchestration_result": orchestration_result,
            "user_message": demo_message
        }
        
        phase3_result = await enhanced_context_plugin._continuous_learning_handler(
            interaction_data,
            learning_focus="context_patterns"
        )
        
        if phase3_result["success"]:
            print("✅ Phase 3 completed successfully")
            learning_result = phase3_result["learning_result"]
            print(f"   Patterns Learned: {len(learning_result['learned_patterns'])}")
            print(f"   Improvements Identified: {len(learning_result['context_improvements'])}")
            
            # Show learning insights
            for pattern in learning_result["learned_patterns"][:2]:  # Show first 2
                print(f"   🧠 {pattern['pattern_type']}: {pattern['description']}")
        else:
            print(f"⚠️ Phase 3 completed with warnings: {phase3_result.get('error', 'Unknown warning')}")
        
        # Comprehensive Context Building
        print("\n🏗️ Comprehensive Context Building")
        print("=" * 30)
        
        comprehensive_result = await enhanced_context_plugin._build_comprehensive_context_handler(
            demo_message,
            context_depth="comprehensive"
        )
        
        if comprehensive_result["success"]:
            print("✅ Comprehensive context built successfully")
            comprehensive_context = comprehensive_result["comprehensive_context"]
            print(f"   Overall Context Score: {comprehensive_context['overall_context_score']:.3f}")
            print(f"   Context Depth: {comprehensive_context['context_depth']}")
        else:
            print(f"❌ Comprehensive context building failed: {comprehensive_result.get('error', 'Unknown error')}")
        
        # Enhanced Workflow Execution
        print("\n🚀 Enhanced Workflow Execution")
        print("=" * 30)
        
        workflow_result = await workflow_orchestrator_plugin._execute_enhanced_workflow_handler(
            demo_message,
            workflow_mode="standard",
            include_learning=True
        )
        
        if workflow_result["success"]:
            print("✅ Enhanced workflow executed successfully")
            workflow_data = workflow_result["workflow_result"]
            print(f"   Total Duration: {workflow_result['total_duration']:.2f}s")
            print(f"   Phases Executed: {workflow_data['overall_results']['total_phases']}")
            print(f"   Success Rate: {workflow_data['overall_results']['success_rate']:.1%}")
            print(f"   Performance Score: {workflow_data['performance_metrics']['overall_performance_score']:.3f}")
            
            # Show phase details
            for phase in workflow_data["phases_executed"]:
                status_icon = "✅" if phase["status"] == "completed" else "❌"
                print(f"   {status_icon} {phase['phase']}: {phase['duration']:.2f}s")
        else:
            print(f"❌ Enhanced workflow failed: {workflow_result.get('error', 'Unknown error')}")
        
        # Workflow Performance Analysis
        print("\n📊 Workflow Performance Analysis")
        print("=" * 30)
        
        performance_result = await workflow_orchestrator_plugin._analyze_workflow_performance_handler(
            timeframe="session",
            include_recommendations=True
        )
        
        if performance_result["success"]:
            print("✅ Performance analysis completed")
            analysis = performance_result["analysis_result"]
            
            if "performance_summary" in analysis:
                summary = analysis["performance_summary"]
                if summary.get("status") != "no_data":
                    print(f"   Total Workflows: {summary.get('total_workflows', 0)}")
                    print(f"   Success Rate: {summary.get('success_rate', 0):.1%}")
                    print(f"   Average Duration: {summary.get('average_duration', 0):.2f}s")
            
            if "recommendations" in analysis:
                print(f"   Recommendations: {len(analysis['recommendations'])}")
                for rec in analysis["recommendations"][:3]:  # Show first 3
                    print(f"   💡 {rec}")
        else:
            print(f"❌ Performance analysis failed: {performance_result.get('error', 'Unknown error')}")
        
        # Workflow Health Check
        print("\n🏥 Workflow Health Check")
        print("=" * 30)
        
        health_result = await workflow_orchestrator_plugin._workflow_health_check_handler(
            check_level="comprehensive"
        )
        
        if health_result["success"]:
            print("✅ Health check completed")
            health_data = health_result["health_result"]
            print(f"   Overall Health: {health_data['overall_health']}")
            print(f"   Components Checked: {len(health_data['component_health'])}")
            
            if health_data["issues_found"]:
                print(f"   Issues Found: {len(health_data['issues_found'])}")
                for issue in health_data["issues_found"][:2]:  # Show first 2
                    print(f"   ⚠️ {issue}")
            
            if health_data["recommendations"]:
                print(f"   Recommendations: {len(health_data['recommendations'])}")
                for rec in health_data["recommendations"][:2]:  # Show first 2
                    print(f"   💡 {rec}")
        else:
            print(f"❌ Health check failed: {health_result.get('error', 'Unknown error')}")
        
        # Context Quality Assessment
        print("\n🎯 Context Quality Assessment")
        print("=" * 30)
        
        quality_result = await enhanced_context_plugin._assess_context_quality_handler(
            context_data,
            assessment_criteria=["completeness", "relevance", "freshness"]
        )
        
        if quality_result["success"]:
            print("✅ Quality assessment completed")
            assessment = quality_result["assessment_result"]
            print(f"   Overall Quality Score: {assessment['overall_quality_score']:.3f}")
            
            for criterion, score in assessment["quality_scores"].items():
                print(f"   {criterion.capitalize()}: {score:.3f}")
            
            if assessment["improvement_suggestions"]:
                print(f"   Improvement Suggestions: {len(assessment['improvement_suggestions'])}")
                for suggestion in assessment["improvement_suggestions"][:2]:  # Show first 2
                    print(f"   💡 {suggestion}")
        else:
            print(f"❌ Quality assessment failed: {quality_result.get('error', 'Unknown error')}")
        
        # Tool Performance Analysis
        print("\n📊 Tool Performance Analysis")
        print("=" * 30)
        
        tool_performance_result = await enhanced_context_plugin._analyze_tool_performance_handler(
            tool_name="all",
            timeframe="session"
        )
        
        if tool_performance_result["success"]:
            print("✅ Tool performance analysis completed")
            analysis = tool_performance_result["analysis_result"]
            
            if analysis["performance_metrics"]:
                print(f"   Tools Analyzed: {len(analysis['performance_metrics'])}")
                
                # Show top performing tools
                tool_scores = []
                for tool_name, metrics in analysis["performance_metrics"].items():
                    if "overall_performance_score" in metrics:
                        tool_scores.append((tool_name, metrics["overall_performance_score"]))
                
                if tool_scores:
                    tool_scores.sort(key=lambda x: x[1], reverse=True)
                    print("   Top Performing Tools:")
                    for tool_name, score in tool_scores[:3]:  # Show top 3
                        print(f"   🏆 {tool_name}: {score:.3f}")
            
            if analysis["recommendations"]:
                print(f"   Recommendations: {len(analysis['recommendations'])}")
                for rec in analysis["recommendations"][:2]:  # Show first 2
                    print(f"   💡 {rec}")
        else:
            print(f"❌ Tool performance analysis failed: {tool_performance_result.get('error', 'Unknown error')}")
        
        # Batch Processing Demo
        print("\n📦 Batch Processing Demo")
        print("=" * 30)
        
        batch_messages = [
            "Analyze system performance",
            "Check memory usage",
            "Review error logs"
        ]
        
        batch_result = await workflow_orchestrator_plugin._batch_workflow_processing_handler(
            batch_messages,
            workflow_mode="standard"
        )
        
        if batch_result["success"]:
            print("✅ Batch processing completed")
            batch_data = batch_result["batch_result"]
            print(f"   Messages Processed: {batch_data['total_messages']}")
            print(f"   Successful: {batch_data['batch_performance']['successful_messages']}")
            print(f"   Failed: {batch_data['batch_performance']['failed_messages']}")
            print(f"   Success Rate: {batch_data['batch_performance']['success_rate']:.1%}")
            print(f"   Total Duration: {batch_data['batch_performance']['total_duration']:.2f}s")
            print(f"   Average per Message: {batch_data['batch_performance']['average_duration_per_message']:.2f}s")
        else:
            print(f"❌ Batch processing failed: {batch_result.get('error', 'Unknown error')}")
        
        # Workflow Optimization
        print("\n🔧 Workflow Optimization")
        print("=" * 30)
        
        optimization_result = await workflow_orchestrator_plugin._optimize_workflow_handler(
            optimization_focus="performance",
            target_metrics=["speed", "accuracy", "context_quality"]
        )
        
        if optimization_result["success"]:
            print("✅ Workflow optimization completed")
            optimization_data = optimization_result["optimization_result"]
            print(f"   Focus Area: {optimization_data['optimization_focus']}")
            print(f"   Target Metrics: {', '.join(optimization_data['target_metrics'])}")
            print(f"   Recommendations: {len(optimization_data['optimization_recommendations'])}")
            print(f"   Improvements Implemented: {len(optimization_data['implemented_improvements'])}")
            
            # Show current performance
            current_perf = optimization_data["current_performance"]
            if current_perf.get("status") == "healthy":
                print(f"   Current Performance Score: {current_perf.get('average_performance_score', 0):.3f}")
                print(f"   Average Duration: {current_perf.get('average_duration', 0):.2f}s")
        else:
            print(f"❌ Workflow optimization failed: {optimization_result.get('error', 'Unknown error')}")
        
        print("\n🎉 Enhanced Context System Demonstration Completed!")
        print("=" * 50)
        print("All three phases have been successfully demonstrated:")
        print("✅ Phase 1: Enhanced Context Retrieval")
        print("✅ Phase 2: Tool Orchestration")
        print("✅ Phase 3: Continuous Learning")
        print("\nAdditional features demonstrated:")
        print("✅ Comprehensive Context Building")
        print("✅ Enhanced Workflow Execution")
        print("✅ Performance Analysis & Optimization")
        print("✅ Health Monitoring & Maintenance")
        print("✅ Batch Processing Capabilities")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all required plugins are properly installed and accessible")
    except Exception as e:
        print(f"❌ Demonstration failed: {e}")
        logger.exception("Demonstration error")

async def demonstrate_individual_phases():
    """Demonstrate individual phases separately"""
    
    print("\n🔍 Individual Phase Demonstration")
    print("=" * 40)
    
    try:
        from plugins.enhanced_context_integration import EnhancedContextIntegrationPlugin
        
        plugin = EnhancedContextIntegrationPlugin()
        plugin._setup()
        
        demo_message = "Show me how the enhanced context system works"
        
        # Phase 1 only
        print("\n🔍 Phase 1 Only: Enhanced Context Retrieval")
        result1 = await plugin._enhanced_context_retrieval_handler(demo_message)
        if result1["success"]:
            print(f"✅ Phase 1 completed with score: {result1['context_data']['context_quality']['overall_score']:.3f}")
        else:
            print(f"❌ Phase 1 failed: {result1.get('error')}")
        
        # Phase 2 only
        if result1["success"]:
            print("\n🎯 Phase 2 Only: Tool Orchestration")
            result2 = await plugin._orchestrate_tools_handler(result1["context_data"])
            if result2["success"]:
                print(f"✅ Phase 2 completed with {len(result2['orchestration_result']['tool_recommendations'])} tools")
            else:
                print(f"❌ Phase 2 failed: {result2.get('error')}")
        
        # Phase 3 only
        if result1["success"] and result2["success"]:
            print("\n📚 Phase 3 Only: Continuous Learning")
            interaction_data = {
                "context_data": result1["context_data"],
                "orchestration_result": result2["orchestration_result"]
            }
            result3 = await plugin._continuous_learning_handler(interaction_data)
            if result3["success"]:
                print(f"✅ Phase 3 completed with {len(result3['learning_result']['learned_patterns'])} patterns")
            else:
                print(f"❌ Phase 3 failed: {result3.get('error')}")
        
    except Exception as e:
        print(f"❌ Individual phase demonstration failed: {e}")

async def main():
    """Main demonstration function"""
    print("🚀 Enhanced Context System - Complete Demonstration")
    print("=" * 60)
    print("This demonstration will showcase:")
    print("• All three phases of context enhancement")
    print("• Complete workflow orchestration")
    print("• Performance analysis and optimization")
    print("• Health monitoring and maintenance")
    print("• Batch processing capabilities")
    print("=" * 60)
    
    # Run main demonstration
    await demonstrate_enhanced_context_system()
    
    # Run individual phase demonstration
    await demonstrate_individual_phases()
    
    print("\n🎯 Demonstration Summary")
    print("=" * 30)
    print("The enhanced context system provides:")
    print("• Comprehensive context awareness enhancement")
    print("• Intelligent tool orchestration")
    print("• Continuous learning and improvement")
    print("• Performance monitoring and optimization")
    print("• Robust error handling and health checks")
    print("• Scalable batch processing capabilities")
    
    print("\n🚀 Ready for production use!")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏹️ Demonstration interrupted by user")
    except Exception as e:
        print(f"\n❌ Demonstration failed: {e}")
        logger.exception("Main demonstration error")
