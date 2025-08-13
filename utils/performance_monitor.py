#!/usr/bin/env python3
"""
Real-Time Performance Monitor for Memory Context Manager
Provides comprehensive system health and performance metrics
"""

import sqlite3
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List
from pathlib import Path

logger = logging.getLogger(__name__)

class PerformanceMonitor:
    """Real-time performance monitoring and health assessment"""
    
    def __init__(self, db_path: str = "brain_memory_store/brain.db"):
        self.db_path = db_path
        
    def get_comprehensive_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive real-time performance dashboard"""
        logger.info("📊 Generating comprehensive performance dashboard...")
        
        return {
            "timestamp": datetime.now().isoformat(),
            "system_health": self._get_system_health_score(),
            "function_performance": self._get_function_performance_metrics(),
            "dream_system_health": self._get_dream_system_health(),
            "memory_system_metrics": self._get_memory_system_metrics(),
            "database_health": self._get_database_health_metrics(),
            "integration_status": self._check_integration_status(),
            "performance_trends": self._analyze_performance_trends(),
            "recommendations": self._generate_optimization_recommendations()
        }
    
    def _get_system_health_score(self) -> Dict[str, Any]:
        """Calculate overall system health score"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Calculate success rates
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total_calls,
                        SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful_calls
                    FROM function_calls 
                    WHERE created_at > datetime('now', '-24 hours')
                """)
                call_stats = cursor.fetchone()
                
                if call_stats[0] > 0:
                    success_rate = call_stats[1] / call_stats[0]
                else:
                    success_rate = 0.0
                
                # Check dream system activity
                cursor.execute("""
                    SELECT dream_cycles, last_updated 
                    FROM dream_system_metrics 
                    ORDER BY id DESC LIMIT 1
                """)
                dream_data = cursor.fetchone()
                
                dream_health = 1.0 if dream_data and dream_data[0] > 0 else 0.5
                
                # Check data freshness
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM memory_store 
                    WHERE updated_at > datetime('now', '-7 days')
                """)
                fresh_memories = cursor.fetchone()[0]
                memory_freshness = min(1.0, fresh_memories / 10)  # Target: 10 fresh memories per week
                
                # Calculate overall health score
                health_score = (success_rate * 0.4 + dream_health * 0.3 + memory_freshness * 0.3)
                
                return {
                    "overall_score": round(health_score, 3),
                    "grade": self._score_to_grade(health_score),
                    "components": {
                        "function_success_rate": round(success_rate, 3),
                        "dream_system_health": round(dream_health, 3),
                        "memory_freshness": round(memory_freshness, 3)
                    },
                    "total_function_calls_24h": call_stats[0],
                    "successful_calls_24h": call_stats[1]
                }
                
        except Exception as e:
            logger.error(f"Failed to calculate system health: {e}")
            return {"overall_score": 0.0, "error": str(e)}
    
    def _get_function_performance_metrics(self) -> Dict[str, Any]:
        """Get detailed function performance metrics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Function call statistics
                cursor.execute("""
                    SELECT 
                        function_name,
                        function_type,
                        COUNT(*) as call_count,
                        AVG(CASE WHEN success = 1 THEN 1.0 ELSE 0.0 END) as success_rate,
                        AVG(execution_time_ms) as avg_execution_time,
                        MAX(created_at) as last_call
                    FROM function_calls 
                    WHERE created_at > datetime('now', '-7 days')
                    GROUP BY function_name, function_type
                    ORDER BY call_count DESC
                    LIMIT 10
                """)
                
                function_stats = []
                for row in cursor.fetchall():
                    function_stats.append({
                        "function_name": row[0],
                        "function_type": row[1],
                        "call_count": row[2],
                        "success_rate": round(row[3], 3),
                        "avg_execution_time_ms": round(row[4] or 0, 2),
                        "last_call": row[5],
                        "performance_grade": self._score_to_grade(row[3])
                    })
                
                return {
                    "top_functions": function_stats,
                    "total_unique_functions": len(function_stats)
                }
                
        except Exception as e:
            logger.error(f"Failed to get function performance: {e}")
            return {"error": str(e)}
    
    def _get_dream_system_health(self) -> Dict[str, Any]:
        """Get dream system health and performance metrics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Dream system metrics
                cursor.execute("""
                    SELECT * FROM dream_system_metrics 
                    ORDER BY id DESC LIMIT 1
                """)
                dream_data = cursor.fetchone()
                
                if not dream_data:
                    return {"status": "no_data", "health_score": 0.0}
                
                # Calculate effectiveness based on activity
                effectiveness_metrics = {
                    "dream_cycles": dream_data[1],
                    "cross_references_processed": dream_data[2],
                    "relationships_enhanced": dream_data[3],
                    "context_injections_generated": dream_data[4],
                    "knowledge_synthesis_events": dream_data[5],
                    "memory_consolidation_cycles": dream_data[6],
                    "last_updated": dream_data[7]
                }
                
                # Calculate dream effectiveness score
                total_activity = sum([
                    dream_data[2],  # cross_references_processed
                    dream_data[3],  # relationships_enhanced
                    dream_data[4],  # context_injections_generated
                    dream_data[5],  # knowledge_synthesis_events
                    dream_data[6]   # memory_consolidation_cycles
                ])
                
                effectiveness = min(1.0, total_activity / 100)  # Target: 100 total activities
                
                return {
                    "status": "active",
                    "health_score": round(effectiveness, 3),
                    "grade": self._score_to_grade(effectiveness),
                    "metrics": effectiveness_metrics,
                    "recommendations": self._get_dream_system_recommendations(effectiveness_metrics)
                }
                
        except Exception as e:
            logger.error(f"Failed to get dream system health: {e}")
            return {"error": str(e)}
    
    def _get_memory_system_metrics(self) -> Dict[str, Any]:
        """Get memory system health and statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Memory store statistics
                cursor.execute("SELECT COUNT(*) FROM memory_store")
                total_memories = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM learning_bits")
                learning_bits = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM cross_references")
                cross_references = cursor.fetchone()[0]
                
                # Calculate cross-reference density
                if learning_bits > 0:
                    cross_ref_density = cross_references / learning_bits
                else:
                    cross_ref_density = 0.0
                
                # Memory freshness
                cursor.execute("""
                    SELECT COUNT(*) FROM memory_store 
                    WHERE updated_at > datetime('now', '-24 hours')
                """)
                fresh_memories_24h = cursor.fetchone()[0]
                
                # Memory health score
                memory_health = min(1.0, (
                    (total_memories / 50) * 0.3 +  # Target: 50 memories
                    (cross_ref_density / 2.0) * 0.4 +  # Target: 2.0 density
                    (fresh_memories_24h / 5) * 0.3  # Target: 5 fresh per day
                ))
                
                return {
                    "health_score": round(memory_health, 3),
                    "grade": self._score_to_grade(memory_health),
                    "statistics": {
                        "total_memories": total_memories,
                        "learning_bits": learning_bits,
                        "cross_references": cross_references,
                        "cross_reference_density": round(cross_ref_density, 2),
                        "fresh_memories_24h": fresh_memories_24h
                    }
                }
                
        except Exception as e:
            logger.error(f"Failed to get memory system metrics: {e}")
            return {"error": str(e)}
    
    def _get_database_health_metrics(self) -> Dict[str, Any]:
        """Get database health and performance metrics"""
        try:
            import os
            
            # Database size
            size_bytes = os.path.getsize(self.db_path)
            size_mb = size_bytes / (1024 * 1024)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Table count
                cursor.execute("""
                    SELECT COUNT(*) FROM sqlite_master 
                    WHERE type='table' AND name NOT LIKE 'sqlite_%'
                """)
                table_count = cursor.fetchone()[0]
                
                # Check database integrity
                cursor.execute("PRAGMA integrity_check")
                integrity = cursor.fetchone()[0]
                
                # Database health score
                db_health = 1.0 if integrity == "ok" else 0.5
                if size_mb > 100:  # If DB is getting too large
                    db_health *= 0.8
                
                return {
                    "health_score": round(db_health, 3),
                    "grade": self._score_to_grade(db_health),
                    "metrics": {
                        "size_mb": round(size_mb, 2),
                        "table_count": table_count,
                        "integrity_check": integrity,
                        "needs_optimization": size_mb > 50
                    }
                }
                
        except Exception as e:
            logger.error(f"Failed to get database health: {e}")
            return {"error": str(e)}
    
    def _check_integration_status(self) -> Dict[str, Any]:
        """Check integration status of all system components"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check key tables exist
                required_tables = [
                    'memory_store', 'brain_state', 'function_calls',
                    'dream_system_metrics', 'learning_bits', 'cross_references'
                ]
                
                existing_tables = []
                for table in required_tables:
                    try:
                        cursor.execute(f"SELECT COUNT(*) FROM {table}")
                        existing_tables.append(table)
                    except:
                        pass
                
                integration_score = len(existing_tables) / len(required_tables)
                
                return {
                    "integration_score": round(integration_score, 3),
                    "grade": self._score_to_grade(integration_score),
                    "required_tables": required_tables,
                    "existing_tables": existing_tables,
                    "missing_tables": list(set(required_tables) - set(existing_tables))
                }
                
        except Exception as e:
            logger.error(f"Failed to check integration status: {e}")
            return {"error": str(e)}
    
    def _analyze_performance_trends(self) -> Dict[str, Any]:
        """Analyze performance trends over time"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Function call trends (last 7 days)
                cursor.execute("""
                    SELECT 
                        DATE(created_at) as call_date,
                        COUNT(*) as daily_calls,
                        AVG(CASE WHEN success = 1 THEN 1.0 ELSE 0.0 END) as daily_success_rate
                    FROM function_calls 
                    WHERE created_at > datetime('now', '-7 days')
                    GROUP BY DATE(created_at)
                    ORDER BY call_date DESC
                """)
                
                daily_trends = []
                for row in cursor.fetchall():
                    daily_trends.append({
                        "date": row[0],
                        "calls": row[1],
                        "success_rate": round(row[2], 3)
                    })
                
                return {
                    "daily_trends": daily_trends,
                    "trend_analysis": "stable" if len(daily_trends) > 0 else "no_data"
                }
                
        except Exception as e:
            logger.error(f"Failed to analyze trends: {e}")
            return {"error": str(e)}
    
    def _generate_optimization_recommendations(self) -> List[Dict[str, str]]:
        """Generate optimization recommendations based on current performance"""
        recommendations = []
        
        try:
            # Get current health scores
            system_health = self._get_system_health_score()
            dream_health = self._get_dream_system_health()
            memory_metrics = self._get_memory_system_metrics()
            
            # Function success rate recommendations
            if system_health.get("components", {}).get("function_success_rate", 0) < 0.8:
                recommendations.append({
                    "priority": "HIGH",
                    "category": "Function Performance",
                    "issue": "Low function success rate detected",
                    "recommendation": "Review function call logging and error handling mechanisms",
                    "impact": "Improved monitoring accuracy and debugging capabilities"
                })
            
            # Dream system recommendations  
            if dream_health.get("health_score", 0) < 0.6:
                recommendations.append({
                    "priority": "MEDIUM",
                    "category": "Dream System",
                    "issue": "Dream system effectiveness below optimal",
                    "recommendation": "Increase dream cycle frequency and context injection triggers",
                    "impact": "Enhanced memory consolidation and knowledge synthesis"
                })
            
            # Memory system recommendations
            memory_density = memory_metrics.get("statistics", {}).get("cross_reference_density", 0)
            if memory_density < 1.5:
                recommendations.append({
                    "priority": "MEDIUM",
                    "category": "Memory System", 
                    "issue": "Low cross-reference density in learning bits",
                    "recommendation": "Enhance automatic relationship detection between learning concepts",
                    "impact": "Improved context awareness and knowledge interconnection"
                })
            
            # Database optimization recommendations
            db_health = self._get_database_health_metrics()
            if db_health.get("metrics", {}).get("needs_optimization", False):
                recommendations.append({
                    "priority": "LOW",
                    "category": "Database Performance",
                    "issue": "Database size growing, optimization recommended",
                    "recommendation": "Run database vacuum, analyze, and cleanup old data",
                    "impact": "Improved query performance and reduced storage usage"
                })
            
        except Exception as e:
            logger.error(f"Failed to generate recommendations: {e}")
            recommendations.append({
                "priority": "HIGH",
                "category": "System Error",
                "issue": "Failed to analyze system for recommendations",
                "recommendation": "Check system logs and database connectivity",
                "impact": "Restore monitoring and optimization capabilities"
            })
        
        return recommendations
    
    def _get_dream_system_recommendations(self, metrics: Dict[str, Any]) -> List[str]:
        """Get specific recommendations for dream system optimization"""
        recommendations = []
        
        if metrics["dream_cycles"] < 5:
            recommendations.append("Consider increasing dream cycle frequency")
        
        if metrics["cross_references_processed"] < 50:
            recommendations.append("Enhance cross-reference processing in dream cycles")
        
        if metrics["knowledge_synthesis_events"] < 10:
            recommendations.append("Optimize knowledge synthesis triggers")
        
        return recommendations
    
    def _score_to_grade(self, score: float) -> str:
        """Convert numeric score to letter grade"""
        if score >= 0.9:
            return "A"
        elif score >= 0.8:
            return "B" 
        elif score >= 0.7:
            return "C"
        elif score >= 0.6:
            return "D"
        else:
            return "F"

def main():
    """Run performance monitor from command line"""
    monitor = PerformanceMonitor()
    
    print("📊 Memory Context Manager - Performance Monitor")
    print("=" * 60)
    
    dashboard = monitor.get_comprehensive_dashboard()
    
    # System Health Overview
    print(f"\n🏥 SYSTEM HEALTH OVERVIEW")
    health = dashboard["system_health"]
    print(f"  Overall Score: {health['overall_score']:.3f} (Grade: {health['grade']})")
    print(f"  Function Success Rate: {health['components']['function_success_rate']:.3f}")
    print(f"  Dream System Health: {health['components']['dream_system_health']:.3f}")
    print(f"  Memory Freshness: {health['components']['memory_freshness']:.3f}")
    
    # Top Recommendations
    print(f"\n🎯 TOP RECOMMENDATIONS")
    for rec in dashboard["recommendations"][:3]:
        print(f"  [{rec['priority']}] {rec['category']}: {rec['recommendation']}")
    
    # Key Metrics
    print(f"\n📈 KEY METRICS")
    memory = dashboard["memory_system_metrics"]
    print(f"  Total Memories: {memory['statistics']['total_memories']}")
    print(f"  Learning Bits: {memory['statistics']['learning_bits']}")
    print(f"  Cross-Reference Density: {memory['statistics']['cross_reference_density']}")
    
    dream = dashboard["dream_system_health"]
    if "metrics" in dream:
        print(f"  Dream Cycles: {dream['metrics']['dream_cycles']}")
        print(f"  Knowledge Synthesis Events: {dream['metrics']['knowledge_synthesis_events']}")

if __name__ == "__main__":
    main()