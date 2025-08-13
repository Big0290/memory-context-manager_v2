#!/usr/bin/env python3
"""
Enhanced Dream System for AI Brain
Leverages context injection capabilities for advanced memory consolidation and knowledge synthesis
"""

import asyncio
import sqlite3
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)

class EnhancedDreamSystem:
    """Enhanced dream system that leverages context injection for advanced memory processing"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.dream_cycles = 0
        self.consolidation_metrics = {
            'cross_references_processed': 0,
            'relationships_enhanced': 0,
            'context_injections_generated': 0,
            'knowledge_synthesis_events': 0,
            'memory_consolidation_cycles': 0
        }
    
    async def dream(self) -> Dict[str, Any]:
        """Enhanced dream process leveraging context injection capabilities"""
        logger.info("💤 ENHANCED DREAM SYSTEM ACTIVATED")
        logger.info("=" * 50)
        
        try:
            # Phase 1: Context-Aware Memory Consolidation
            consolidation_result = await self._context_aware_memory_consolidation()
            
            # Phase 2: Cross-Reference Pattern Analysis
            pattern_result = await self._analyze_cross_reference_patterns()
            
            # Phase 3: Learning Relationship Enhancement
            relationship_result = await self._enhance_learning_relationships()
            
            # Phase 4: Context Injection Optimization
            context_result = await self._optimize_context_injection()
            
            # Phase 5: Knowledge Synthesis and Creativity
            synthesis_result = await self._knowledge_synthesis_and_creativity()
            
            # Update dream cycle
            self.dream_cycles += 1
            
            # Calculate dream effectiveness
            dream_effectiveness = self._calculate_dream_effectiveness()
            
            logger.info(f"💤 DREAM CYCLE {self.dream_cycles} COMPLETED")
            logger.info(f"📊 Dream Effectiveness: {dream_effectiveness:.1%}")
            
            return {
                "dream_state": "enhanced_active",
                "dream_cycle": self.dream_cycles,
                "dream_effectiveness": dream_effectiveness,
                "consolidation_process": consolidation_result,
                "pattern_analysis": pattern_result,
                "relationship_enhancement": relationship_result,
                "context_optimization": context_result,
                "knowledge_synthesis": synthesis_result,
                "consolidation_metrics": self.consolidation_metrics,
                "wake_impact": "enhanced_context_injection_and_knowledge_synthesis",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Enhanced dream process failed: {e}")
            return {
                "dream_state": "enhanced_disrupted",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def _context_aware_memory_consolidation(self) -> Dict[str, Any]:
        """Context-aware memory consolidation using cross-references"""
        logger.info("🧠 Phase 1: Context-Aware Memory Consolidation...")
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get recent learning bits with cross-references
                cursor.execute("""
                    SELECT lb.id, lb.content, lb.content_type, lb.category, lb.importance_score,
                           COUNT(cr.id) as cross_ref_count
                    FROM learning_bits lb
                    LEFT JOIN cross_references cr ON lb.id = cr.source_bit_id
                    WHERE lb.created_at >= datetime('now', '-7 days')
                    GROUP BY lb.id
                    ORDER BY lb.importance_score DESC, cross_ref_count DESC
                    LIMIT 20
                """)
                
                recent_bits = cursor.fetchall()
                consolidation_events = 0
                
                for bit in recent_bits:
                    bit_id, content, content_type, category, importance, cross_ref_count = bit
                    
                    # Consolidate based on cross-reference patterns
                    if cross_ref_count > 0:
                        consolidation_events += 1
                        
                        # Update importance based on cross-reference activity
                        new_importance = min(1.0, importance + (cross_ref_count * 0.1))
                        
                        cursor.execute("""
                            UPDATE learning_bits 
                            SET importance_score = ?, updated_at = CURRENT_TIMESTAMP
                            WHERE id = ?
                        """, (new_importance, bit_id))
                        
                        # Create consolidation record
                        cursor.execute("""
                            INSERT INTO context_enhancement_pipeline 
                            (trigger_type, source_id, enhancement_type, status, priority, created_at)
                            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                        """, ('dream_consolidation', bit_id, 'memory_consolidation', 'completed', 3))
                
                conn.commit()
                self.consolidation_metrics['memory_consolidation_cycles'] += 1
                
                logger.info(f"✅ Memory consolidation completed: {consolidation_events} events")
                
                return {
                    "status": "success",
                    "consolidation_events": consolidation_events,
                    "recent_bits_processed": len(recent_bits),
                    "cross_references_utilized": True
                }
                
        except Exception as e:
            logger.error(f"❌ Memory consolidation failed: {e}")
            return {"status": "failed", "error": str(e)}
    
    async def _analyze_cross_reference_patterns(self) -> Dict[str, Any]:
        """Analyze cross-reference patterns for insights"""
        logger.info("🔗 Phase 2: Cross-Reference Pattern Analysis...")
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Analyze cross-reference patterns
                cursor.execute("""
                    SELECT cr.relationship_type, cr.strength, 
                           lb1.content_type as source_type, lb1.category as source_category,
                           lb2.content_type as target_type, lb2.category as target_category,
                           COUNT(*) as pattern_frequency
                    FROM cross_references cr
                    JOIN learning_bits lb1 ON cr.source_bit_id = lb1.id
                    JOIN learning_bits lb2 ON cr.target_bit_id = lb2.id
                    GROUP BY cr.relationship_type, lb1.content_type, lb1.category, 
                             lb2.content_type, lb2.category
                    ORDER BY pattern_frequency DESC, cr.strength DESC
                    LIMIT 10
                """)
                
                patterns = cursor.fetchall()
                insights_generated = 0
                
                for pattern in patterns:
                    rel_type, strength, src_type, src_cat, tgt_type, tgt_cat, frequency = pattern
                    
                    # Generate insights based on patterns
                    if frequency >= 3 and strength > 0.6:
                        insights_generated += 1
                        
                        # Create insight record
                        cursor.execute("""
                            INSERT INTO context_enhancement_pipeline 
                            (trigger_type, source_id, target_id, relationship_type, 
                             enhancement_type, status, priority, created_at)
                            VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                        """, ('pattern_insight', None, None, rel_type, 'insight_generation', 'pending', 2))
                
                conn.commit()
                self.consolidation_metrics['cross_references_processed'] += len(patterns)
                
                logger.info(f"✅ Pattern analysis completed: {insights_generated} insights generated")
                
                return {
                    "status": "success",
                    "patterns_analyzed": len(patterns),
                    "insights_generated": insights_generated,
                    "strong_patterns": len([p for p in patterns if p[1] > 0.6])
                }
                
        except Exception as e:
            logger.error(f"❌ Pattern analysis failed: {e}")
            return {"status": "failed", "error": str(e)}
    
    async def _enhance_learning_relationships(self) -> Dict[str, Any]:
        """Enhance learning relationships using context injection"""
        logger.info("🧠 Phase 3: Learning Relationship Enhancement...")
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Find learning bits that could benefit from relationships
                cursor.execute("""
                    SELECT lb.id, lb.content, lb.content_type, lb.category, lb.importance_score
                    FROM learning_bits lb
                    LEFT JOIN learning_relationships lr ON lb.id = lr.source_bit_id
                    WHERE lr.id IS NULL
                    AND lb.importance_score > 0.7
                    ORDER BY lb.importance_score DESC
                    LIMIT 15
                """)
                
                unconnected_bits = cursor.fetchall()
                relationships_created = 0
                
                for bit in unconnected_bits:
                    bit_id, content, content_type, category, importance = bit
                    
                    # Find potential relationships
                    cursor.execute("""
                        SELECT lb2.id, lb2.content_type, lb2.category, lb2.importance_score
                        FROM learning_bits lb2
                        WHERE lb2.id != ? 
                        AND lb2.category = ?
                        AND lb2.importance_score > 0.5
                        ORDER BY lb2.importance_score DESC
                        LIMIT 3
                    """, (bit_id, category))
                    
                    potential_relations = cursor.fetchall()
                    
                    for rel in potential_relations:
                        rel_id, rel_type, rel_cat, rel_importance = rel
                        
                        # Calculate relationship strength
                        strength = min(1.0, (importance + rel_importance) / 2)
                        
                        if strength > 0.4:
                            cursor.execute("""
                                INSERT OR IGNORE INTO learning_relationships 
                                (source_bit_id, target_bit_id, relationship_type, 
                                 strength, bidirectional, created_at)
                                VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                            """, (bit_id, rel_id, 'related', strength, True))
                            
                            relationships_created += 1
                
                conn.commit()
                self.consolidation_metrics['relationships_enhanced'] += relationships_created
                
                logger.info(f"✅ Relationship enhancement completed: {relationships_created} relationships created")
                
                return {
                    "status": "success",
                    "unconnected_bits_processed": len(unconnected_bits),
                    "relationships_created": relationships_created,
                    "relationship_strength_avg": 0.6 if relationships_created > 0 else 0.0
                }
                
        except Exception as e:
            logger.error(f"❌ Relationship enhancement failed: {e}")
            return {"status": "failed", "error": str(e)}
    
    async def _optimize_context_injection(self) -> Dict[str, Any]:
        """Optimize context injection based on dream insights"""
        logger.info("⚙️ Phase 4: Context Injection Optimization...")
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Analyze context injection effectiveness
                cursor.execute("""
                    SELECT COUNT(*) FROM cross_references
                """)
                total_cross_refs = cursor.fetchone()[0]
                
                cursor.execute("""
                    SELECT COUNT(*) FROM learning_bits
                """)
                total_learning_bits = cursor.fetchone()[0]
                
                if total_learning_bits > 0:
                    current_effectiveness = min(1.0, total_cross_refs / (total_learning_bits * 2))
                    
                    # Generate context injection triggers for low-effectiveness areas
                    if current_effectiveness < 0.8:
                        cursor.execute("""
                            SELECT lb.id, lb.content_type, lb.category
                            FROM learning_bits lb
                            LEFT JOIN cross_references cr ON lb.id = cr.source_bit_id
                            WHERE cr.id IS NULL
                            AND lb.importance_score > 0.6
                            ORDER BY lb.importance_score DESC
                            LIMIT 10
                        """)
                        
                        low_context_bits = cursor.fetchall()
                        triggers_created = 0
                        
                        for bit in low_context_bits:
                            bit_id, content_type, category = bit
                            
                            cursor.execute("""
                                INSERT INTO context_enhancement_pipeline 
                                (trigger_type, source_id, enhancement_type, status, priority, created_at)
                                VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                            """, ('context_optimization', bit_id, 'cross_reference_generation', 'pending', 1))
                            
                            triggers_created += 1
                        
                        conn.commit()
                        self.consolidation_metrics['context_injections_generated'] += triggers_created
                        
                        logger.info(f"✅ Context optimization completed: {triggers_created} triggers created")
                        
                        return {
                            "status": "success",
                            "current_effectiveness": current_effectiveness,
                            "target_effectiveness": 0.8,
                            "triggers_created": triggers_created,
                            "optimization_needed": True
                        }
                    else:
                        return {
                            "status": "success",
                            "current_effectiveness": current_effectiveness,
                            "target_effectiveness": 0.8,
                            "triggers_created": 0,
                            "optimization_needed": False
                        }
                
                return {"status": "failed", "error": "No learning bits found"}
                
        except Exception as e:
            logger.error(f"❌ Context optimization failed: {e}")
            return {"status": "failed", "error": str(e)}
    
    async def _knowledge_synthesis_and_creativity(self) -> Dict[str, Any]:
        """Generate new knowledge through synthesis and creativity"""
        logger.info("🌟 Phase 5: Knowledge Synthesis and Creativity...")
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Find high-value knowledge combinations
                cursor.execute("""
                    SELECT lb1.content_type, lb1.category, lb2.content_type, lb2.category,
                           COUNT(*) as combination_frequency
                    FROM cross_references cr
                    JOIN learning_bits lb1 ON cr.source_bit_id = lb1.id
                    JOIN learning_bits lb2 ON cr.target_bit_id = lb2.id
                    WHERE cr.strength > 0.7
                    GROUP BY lb1.content_type, lb1.category, lb2.content_type, lb2.category
                    HAVING combination_frequency >= 2
                    ORDER BY combination_frequency DESC
                    LIMIT 5
                """)
                
                knowledge_combinations = cursor.fetchall()
                synthesis_events = 0
                
                for combo in knowledge_combinations:
                    src_type, src_cat, tgt_type, tgt_cat, frequency = combo
                    
                    # Generate synthesis insights
                    if frequency >= 2:
                        synthesis_events += 1
                        
                        # Create synthesis record
                        cursor.execute("""
                            INSERT INTO context_enhancement_pipeline 
                            (trigger_type, source_id, target_id, relationship_type,
                             enhancement_type, status, priority, created_at)
                            VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                        """, ('knowledge_synthesis', None, None, 'synthesis', 'insight_generation', 'pending', 1))
                
                conn.commit()
                self.consolidation_metrics['knowledge_synthesis_events'] += synthesis_events
                
                logger.info(f"✅ Knowledge synthesis completed: {synthesis_events} events")
                
                return {
                    "status": "success",
                    "combinations_analyzed": len(knowledge_combinations),
                    "synthesis_events": synthesis_events,
                    "creative_insights": synthesis_events
                }
                
        except Exception as e:
            logger.error(f"❌ Knowledge synthesis failed: {e}")
            return {"status": "failed", "error": str(e)}
    
    def _calculate_dream_effectiveness(self) -> float:
        """Calculate overall dream effectiveness"""
        total_metrics = sum(self.consolidation_metrics.values())
        if total_metrics == 0:
            return 0.0
        
        # Weight different aspects of dream processing
        weights = {
            'cross_references_processed': 0.25,
            'relationships_enhanced': 0.25,
            'context_injections_generated': 0.25,
            'knowledge_synthesis_events': 0.15,
            'memory_consolidation_cycles': 0.10
        }
        
        effectiveness = 0.0
        for metric, weight in weights.items():
            if self.consolidation_metrics[metric] > 0:
                effectiveness += weight * min(1.0, self.consolidation_metrics[metric] / 10)
        
        return min(1.0, effectiveness)
    
    async def get_dream_status(self) -> Dict[str, Any]:
        """Get current dream system status"""
        return {
            "dream_cycles": self.dream_cycles,
            "consolidation_metrics": self.consolidation_metrics,
            "dream_effectiveness": self._calculate_dream_effectiveness(),
            "last_dream": datetime.now().isoformat(),
            "system_health": "optimal" if self._calculate_dream_effectiveness() > 0.5 else "needs_attention"
        }

# Example usage
async def main():
    """Test enhanced dream system"""
    dream_system = EnhancedDreamSystem("brain_memory_store/brain.db")
    
    # Run dream cycle
    result = await dream_system.dream()
    print(f"Dream result: {result}")
    
    # Get status
    status = await dream_system.get_dream_status()
    print(f"Dream status: {status}")

if __name__ == "__main__":
    asyncio.run(main())
