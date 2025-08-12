#!/usr/bin/env python3
"""
Phase 7A: Pattern Database - Week 2 Implementation
Database for storing and retrieving coding patterns with caching and effectiveness tracking
"""

import sqlite3
import json
import logging
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib
import pickle
from collections import defaultdict

logger = logging.getLogger(__name__)

@dataclass
class PatternRecord:
    """Database record for a coding pattern"""
    pattern_id: str
    pattern_type: str
    pattern_name: str
    description: str
    confidence: float
    file_path: str
    line_numbers: List[int]
    pattern_data: Dict[str, Any]
    detected_at: datetime
    effectiveness_score: float
    usage_count: int
    success_count: int
    failure_count: int
    last_used: Optional[datetime]
    created_at: datetime
    updated_at: datetime

@dataclass
class PatternRelationship:
    """Relationship between patterns"""
    relationship_id: str
    source_pattern_id: str
    target_pattern_id: str
    relationship_type: str  # 'similar', 'depends_on', 'conflicts_with', 'enhances'
    strength: float  # 0.0 to 1.0
    created_at: datetime

class PatternDatabase:
    """Database for storing and retrieving coding patterns"""
    
    def __init__(self, db_path: str = "patterns.db"):
        self.db_path = db_path
        self.db_connection = None
        self.pattern_cache = {}
        self.relationship_cache = {}
        self.cache_stats = {
            "hits": 0,
            "misses": 0,
            "size": 0,
            "max_size": 1000
        }
        self.initialize_database()
    
    def initialize_database(self):
        """Initialize pattern database tables"""
        try:
            self.db_connection = sqlite3.connect(self.db_path)
            self.db_connection.row_factory = sqlite3.Row
            
            # Create tables
            self._create_patterns_table()
            self._create_relationships_table()
            self._create_effectiveness_table()
            self._create_usage_history_table()
            
            # Create indexes for performance
            self._create_indexes()
            
            logger.info("✅ Pattern database initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize pattern database: {str(e)}")
            raise
    
    def _create_patterns_table(self):
        """Create the main patterns table"""
        cursor = self.db_connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patterns (
                pattern_id TEXT PRIMARY KEY,
                pattern_type TEXT NOT NULL,
                pattern_name TEXT NOT NULL,
                description TEXT,
                confidence REAL NOT NULL,
                file_path TEXT,
                line_numbers TEXT,  -- JSON array of line numbers
                pattern_data TEXT,  -- JSON object of pattern data
                detected_at TEXT NOT NULL,  -- ISO format datetime
                effectiveness_score REAL DEFAULT 0.0,
                usage_count INTEGER DEFAULT 0,
                success_count INTEGER DEFAULT 0,
                failure_count INTEGER DEFAULT 0,
                last_used TEXT,  -- ISO format datetime
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        self.db_connection.commit()
    
    def _create_relationships_table(self):
        """Create the pattern relationships table"""
        cursor = self.db_connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pattern_relationships (
                relationship_id TEXT PRIMARY KEY,
                source_pattern_id TEXT NOT NULL,
                target_pattern_id TEXT NOT NULL,
                relationship_type TEXT NOT NULL,
                strength REAL NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (source_pattern_id) REFERENCES patterns (pattern_id),
                FOREIGN KEY (target_pattern_id) REFERENCES patterns (pattern_id)
            )
        """)
        self.db_connection.commit()
    
    def _create_effectiveness_table(self):
        """Create the pattern effectiveness tracking table"""
        cursor = self.db_connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pattern_effectiveness (
                effectiveness_id TEXT PRIMARY KEY,
                pattern_id TEXT NOT NULL,
                effectiveness_score REAL NOT NULL,
                success_rate REAL NOT NULL,
                usage_count INTEGER NOT NULL,
                measured_at TEXT NOT NULL,
                context_hash TEXT,  -- Hash of context when effectiveness was measured
                FOREIGN KEY (pattern_id) REFERENCES patterns (pattern_id)
            )
        """)
        self.db_connection.commit()
    
    def _create_usage_history_table(self):
        """Create the pattern usage history table"""
        cursor = self.db_connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usage_history (
                usage_id TEXT PRIMARY KEY,
                pattern_id TEXT NOT NULL,
                used_at TEXT NOT NULL,
                context_hash TEXT,  -- Hash of context when pattern was used
                success BOOLEAN NOT NULL,
                user_feedback INTEGER,  -- 1-5 rating from user
                notes TEXT,
                FOREIGN KEY (pattern_id) REFERENCES patterns (pattern_id)
            )
        """)
        self.db_connection.commit()
    
    def _create_indexes(self):
        """Create database indexes for performance"""
        cursor = self.db_connection.cursor()
        
        # Indexes for patterns table
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_patterns_type ON patterns (pattern_type)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_patterns_confidence ON patterns (confidence)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_patterns_effectiveness ON patterns (effectiveness_score)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_patterns_file_path ON patterns (file_path)")
        
        # Indexes for relationships table
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_relationships_source ON pattern_relationships (source_pattern_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_relationships_target ON pattern_relationships (target_pattern_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_relationships_type ON pattern_relationships (relationship_type)")
        
        # Indexes for effectiveness table
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_effectiveness_pattern ON pattern_effectiveness (pattern_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_effectiveness_score ON pattern_effectiveness (effectiveness_score)")
        
        # Indexes for usage history table
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_usage_pattern ON usage_history (pattern_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_usage_date ON usage_history (used_at)")
        
        self.db_connection.commit()
    
    async def store_pattern(self, pattern: Dict[str, Any]) -> bool:
        """Store a new coding pattern"""
        try:
            # Validate pattern structure
            if not self._validate_pattern(pattern):
                logger.warning(f"Invalid pattern structure: {pattern.get('pattern_id', 'unknown')}")
                return False
            
            # Check if pattern already exists
            existing = await self.get_pattern(pattern['pattern_id'])
            if existing:
                # Update existing pattern
                return await self._update_pattern(pattern)
            else:
                # Insert new pattern
                return await self._insert_pattern(pattern)
                
        except Exception as e:
            logger.error(f"Error storing pattern: {str(e)}")
            return False
    
    async def _insert_pattern(self, pattern: Dict[str, Any]) -> bool:
        """Insert a new pattern into the database"""
        try:
            cursor = self.db_connection.cursor()
            
            # Prepare data for insertion
            now = datetime.now().isoformat()
            pattern_data = {
                'pattern_id': pattern['pattern_id'],
                'pattern_type': pattern['pattern_type'],
                'pattern_name': pattern['pattern_name'],
                'description': pattern.get('description', ''),
                'confidence': pattern['confidence'],
                'file_path': pattern.get('file_path', ''),
                'line_numbers': json.dumps(pattern.get('line_numbers', [])),
                'pattern_data': json.dumps(pattern.get('pattern_data', {})),
                'detected_at': pattern.get('detected_at', now),
                'effectiveness_score': pattern.get('effectiveness_score', 0.0),
                'usage_count': 0,
                'success_count': 0,
                'failure_count': 0,
                'last_used': None,
                'created_at': now,
                'updated_at': now
            }
            
            # Insert pattern
            cursor.execute("""
                INSERT INTO patterns (
                    pattern_id, pattern_type, pattern_name, description, confidence,
                    file_path, line_numbers, pattern_data, detected_at, effectiveness_score,
                    usage_count, success_count, failure_count, last_used, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                pattern_data['pattern_id'], pattern_data['pattern_type'], pattern_data['pattern_name'],
                pattern_data['description'], pattern_data['confidence'], pattern_data['file_path'],
                pattern_data['line_numbers'], pattern_data['pattern_data'], pattern_data['detected_at'],
                pattern_data['effectiveness_score'], pattern_data['usage_count'], pattern_data['success_count'],
                pattern_data['failure_count'], pattern_data['last_used'], pattern_data['created_at'],
                pattern_data['updated_at']
            ))
            
            self.db_connection.commit()
            
            # Update cache
            self._update_cache(pattern['pattern_id'], pattern_data)
            
            logger.info(f"✅ Pattern stored successfully: {pattern['pattern_id']}")
            return True
            
        except Exception as e:
            logger.error(f"Error inserting pattern: {str(e)}")
            self.db_connection.rollback()
            return False
    
    async def _update_pattern(self, pattern: Dict[str, Any]) -> bool:
        """Update an existing pattern in the database"""
        try:
            cursor = self.db_connection.cursor()
            
            # Prepare update data
            now = datetime.now().isoformat()
            update_data = {
                'pattern_name': pattern.get('pattern_name'),
                'description': pattern.get('description'),
                'confidence': pattern.get('confidence'),
                'file_path': pattern.get('file_path'),
                'line_numbers': json.dumps(pattern.get('line_numbers', [])),
                'pattern_data': json.dumps(pattern.get('pattern_data', {})),
                'detected_at': pattern.get('detected_at'),
                'effectiveness_score': pattern.get('effectiveness_score'),
                'updated_at': now
            }
            
            # Update pattern
            cursor.execute("""
                UPDATE patterns SET
                    pattern_name = ?, description = ?, confidence = ?, file_path = ?,
                    line_numbers = ?, pattern_data = ?, detected_at = ?, effectiveness_score = ?,
                    updated_at = ?
                WHERE pattern_id = ?
            """, (
                update_data['pattern_name'], update_data['description'], update_data['confidence'],
                update_data['file_path'], update_data['line_numbers'], update_data['pattern_data'],
                update_data['detected_at'], update_data['effectiveness_score'], update_data['updated_at'],
                pattern['pattern_id']
            ))
            
            self.db_connection.commit()
            
            # Update cache
            self._update_cache(pattern['pattern_id'], update_data)
            
            logger.info(f"✅ Pattern updated successfully: {pattern['pattern_id']}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating pattern: {str(e)}")
            self.db_connection.rollback()
            return False
    
    async def get_pattern(self, pattern_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a pattern by ID"""
        try:
            # Check cache first
            if pattern_id in self.pattern_cache:
                self.cache_stats["hits"] += 1
                return self.pattern_cache[pattern_id]
            
            self.cache_stats["misses"] += 1
            
            # Query database
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT * FROM patterns WHERE pattern_id = ?", (pattern_id,))
            row = cursor.fetchone()
            
            if row:
                pattern_data = self._row_to_dict(row)
                # Update cache
                self._update_cache(pattern_id, pattern_data)
                return pattern_data
            
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving pattern {pattern_id}: {str(e)}")
            return None
    
    async def find_similar(self, context: Dict[str, Any], limit: int = 10) -> List[Dict[str, Any]]:
        """Find patterns similar to current context"""
        try:
            # Extract context features for similarity matching
            context_features = self._extract_context_features(context)
            
            # Query database for similar patterns
            similar_patterns = await self._query_similar_patterns(context_features, limit)
            
            # Rank by similarity score
            ranked_patterns = self._rank_by_similarity(similar_patterns, context_features)
            
            return ranked_patterns[:limit]
            
        except Exception as e:
            logger.error(f"Error finding similar patterns: {str(e)}")
            return []
    
    async def _query_similar_patterns(self, context_features: Dict[str, Any], limit: int) -> List[Dict[str, Any]]:
        """Query database for patterns similar to context features"""
        try:
            cursor = self.db_connection.cursor()
            
            # Build similarity query based on context features
            query_parts = []
            params = []
            
            if 'pattern_type' in context_features:
                query_parts.append("pattern_type = ?")
                params.append(context_features['pattern_type'])
            
            if 'file_path' in context_features:
                query_parts.append("file_path LIKE ?")
                params.append(f"%{context_features['file_path']}%")
            
            if 'confidence_threshold' in context_features:
                query_parts.append("confidence >= ?")
                params.append(context_features['confidence_threshold'])
            
            # Build final query
            if query_parts:
                where_clause = " AND ".join(query_parts)
                query = f"""
                    SELECT * FROM patterns 
                    WHERE {where_clause}
                    ORDER BY effectiveness_score DESC, confidence DESC
                    LIMIT ?
                """
                params.append(limit)
            else:
                # Fallback to general query
                query = """
                    SELECT * FROM patterns 
                    ORDER BY effectiveness_score DESC, confidence DESC
                    LIMIT ?
                """
                params.append(limit)
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            # Convert rows to dictionaries
            patterns = []
            for row in rows:
                pattern_data = self._row_to_dict(row)
                patterns.append(pattern_data)
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error querying similar patterns: {str(e)}")
            return []
    
    def _extract_context_features(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Extract relevant features from context for similarity matching"""
        features = {}
        
        # Extract pattern type if available
        if 'pattern_type' in context:
            features['pattern_type'] = context['pattern_type']
        
        # Extract file path information
        if 'file_path' in context:
            features['file_path'] = context['file_path']
        
        # Extract confidence threshold
        if 'confidence_threshold' in context:
            features['confidence_threshold'] = context['confidence_threshold']
        else:
            features['confidence_threshold'] = 0.5  # Default threshold
        
        # Extract pattern data features
        if 'pattern_data' in context:
            pattern_data = context['pattern_data']
            if isinstance(pattern_data, dict):
                # Extract key features from pattern data
                if 'language' in pattern_data:
                    features['language'] = pattern_data['language']
                if 'complexity' in pattern_data:
                    features['complexity'] = pattern_data['complexity']
        
        return features
    
    def _rank_by_similarity(self, patterns: List[Dict[str, Any]], context_features: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Rank patterns by similarity to context features"""
        try:
            # Calculate similarity scores for each pattern
            scored_patterns = []
            
            for pattern in patterns:
                similarity_score = self._calculate_similarity_score(pattern, context_features)
                scored_patterns.append({
                    'pattern': pattern,
                    'similarity_score': similarity_score
                })
            
            # Sort by similarity score (descending)
            scored_patterns.sort(key=lambda x: x['similarity_score'], reverse=True)
            
            # Return patterns with scores
            return [item['pattern'] for item in scored_patterns]
            
        except Exception as e:
            logger.error(f"Error ranking patterns by similarity: {str(e)}")
            return patterns  # Return original order if ranking fails
    
    def _calculate_similarity_score(self, pattern: Dict[str, Any], context_features: Dict[str, Any]) -> float:
        """Calculate similarity score between pattern and context features"""
        try:
            score = 0.0
            max_score = 0.0
            
            # Pattern type similarity (30% weight)
            if 'pattern_type' in context_features and 'pattern_type' in pattern:
                if context_features['pattern_type'] == pattern['pattern_type']:
                    score += 0.3
                max_score += 0.3
            
            # File path similarity (20% weight)
            if 'file_path' in context_features and 'file_path' in pattern:
                if context_features['file_path'] in pattern['file_path'] or pattern['file_path'] in context_features['file_path']:
                    score += 0.2
                max_score += 0.2
            
            # Confidence score (25% weight)
            if 'confidence_threshold' in context_features and 'confidence' in pattern:
                if pattern['confidence'] >= context_features['confidence_threshold']:
                    score += 0.25
                max_score += 0.25
            
            # Effectiveness score (25% weight)
            if 'effectiveness_score' in pattern:
                score += 0.25 * pattern['effectiveness_score']
                max_score += 0.25
            
            # Normalize score
            if max_score > 0:
                return score / max_score
            else:
                return 0.0
                
        except Exception as e:
            logger.error(f"Error calculating similarity score: {str(e)}")
            return 0.0
    
    async def update_pattern_effectiveness(self, pattern_id: str, effectiveness: Dict[str, Any]):
        """Update pattern effectiveness metrics"""
        try:
            cursor = self.db_connection.cursor()
            
            # Extract effectiveness data
            success = effectiveness.get('success', False)
            user_feedback = effectiveness.get('user_feedback', None)
            context_hash = effectiveness.get('context_hash', '')
            
            # Update pattern usage statistics
            if success:
                cursor.execute("""
                    UPDATE patterns SET
                        usage_count = usage_count + 1,
                        success_count = success_count + 1,
                        last_used = ?,
                        updated_at = ?
                    WHERE pattern_id = ?
                """, (datetime.now().isoformat(), datetime.now().isoformat(), pattern_id))
            else:
                cursor.execute("""
                    UPDATE patterns SET
                        usage_count = usage_count + 1,
                        failure_count = failure_count + 1,
                        last_used = ?,
                        updated_at = ?
                    WHERE pattern_id = ?
                """, (datetime.now().isoformat(), datetime.now().isoformat(), pattern_id))
            
            # Calculate new effectiveness score
            cursor.execute("""
                SELECT usage_count, success_count, failure_count 
                FROM patterns WHERE pattern_id = ?
            """, (pattern_id,))
            row = cursor.fetchone()
            
            if row:
                usage_count = row['usage_count']
                success_count = row['success_count']
                failure_count = row['failure_count']
                
                if usage_count > 0:
                    success_rate = success_count / usage_count
                    # Simple effectiveness formula - can be enhanced
                    effectiveness_score = success_rate * 0.7 + (user_feedback / 5.0 if user_feedback else 0.5) * 0.3
                    
                    # Update effectiveness score
                    cursor.execute("""
                        UPDATE patterns SET
                            effectiveness_score = ?,
                            updated_at = ?
                        WHERE pattern_id = ?
                    """, (effectiveness_score, datetime.now().isoformat(), pattern_id))
            
            # Record effectiveness measurement
            effectiveness_id = f"eff_{pattern_id}_{datetime.now().timestamp()}"
            cursor.execute("""
                INSERT INTO pattern_effectiveness (
                    effectiveness_id, pattern_id, effectiveness_score, success_rate,
                    usage_count, measured_at, context_hash
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                effectiveness_id, pattern_id, effectiveness_score, success_rate,
                usage_count, datetime.now().isoformat(), context_hash
            ))
            
            # Record usage history
            usage_id = f"usage_{pattern_id}_{datetime.now().timestamp()}"
            cursor.execute("""
                INSERT INTO usage_history (
                    usage_id, pattern_id, used_at, context_hash, success, user_feedback, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                usage_id, pattern_id, datetime.now().isoformat(), context_hash,
                success, user_feedback, effectiveness.get('notes', '')
            ))
            
            self.db_connection.commit()
            
            # Update cache
            if pattern_id in self.pattern_cache:
                self.pattern_cache[pattern_id]['effectiveness_score'] = effectiveness_score
                self.pattern_cache[pattern_id]['usage_count'] = usage_count
                self.pattern_cache[pattern_id]['success_count'] = success_count
                self.pattern_cache[pattern_id]['failure_count'] = failure_count
                self.pattern_cache[pattern_id]['last_used'] = datetime.now().isoformat()
            
            logger.info(f"✅ Pattern effectiveness updated: {pattern_id}")
            
        except Exception as e:
            logger.error(f"Error updating pattern effectiveness: {str(e)}")
            self.db_connection.rollback()
    
    async def get_pattern_statistics(self) -> Dict[str, Any]:
        """Get overall pattern database statistics"""
        try:
            cursor = self.db_connection.cursor()
            
            # Total patterns by type
            cursor.execute("""
                SELECT pattern_type, COUNT(*) as count 
                FROM patterns 
                GROUP BY pattern_type
            """)
            type_counts = {row['pattern_type']: row['count'] for row in cursor.fetchall()}
            
            # Average effectiveness by type
            cursor.execute("""
                SELECT pattern_type, AVG(effectiveness_score) as avg_effectiveness
                FROM patterns 
                GROUP BY pattern_type
            """)
            avg_effectiveness = {row['pattern_type']: row['avg_effectiveness'] for row in cursor.fetchall()}
            
            # Total usage statistics
            cursor.execute("""
                SELECT 
                    SUM(usage_count) as total_usage,
                    SUM(success_count) as total_success,
                    SUM(failure_count) as total_failure
                FROM patterns
            """)
            usage_stats = cursor.fetchone()
            
            # Cache statistics
            cache_stats = {
                "hits": self.cache_stats["hits"],
                "misses": self.cache_stats["misses"],
                "hit_rate": self.cache_stats["hits"] / (self.cache_stats["hits"] + self.cache_stats["misses"]) if (self.cache_stats["hits"] + self.cache_stats["misses"]) > 0 else 0,
                "size": self.cache_stats["size"],
                "max_size": self.cache_stats["max_size"]
            }
            
            return {
                "success": True,
                "total_patterns": sum(type_counts.values()),
                "patterns_by_type": type_counts,
                "average_effectiveness_by_type": avg_effectiveness,
                "usage_statistics": {
                    "total_usage": usage_stats['total_usage'] or 0,
                    "total_success": usage_stats['total_success'] or 0,
                    "total_failure": usage_stats['total_failure'] or 0,
                    "success_rate": (usage_stats['total_success'] or 0) / (usage_stats['total_usage'] or 1)
                },
                "cache_statistics": cache_stats,
                "database_size": Path(self.db_path).stat().st_size if Path(self.db_path).exists() else 0
            }
            
        except Exception as e:
            logger.error(f"Error getting pattern statistics: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _validate_pattern(self, pattern: Dict[str, Any]) -> bool:
        """Validate pattern structure before storage"""
        required_fields = ['pattern_id', 'pattern_type', 'pattern_name', 'confidence']
        
        for field in required_fields:
            if field not in pattern:
                logger.warning(f"Missing required field: {field}")
                return False
        
        # Validate data types
        if not isinstance(pattern['pattern_id'], str) or not pattern['pattern_id']:
            logger.warning("pattern_id must be non-empty string")
            return False
        
        if not isinstance(pattern['confidence'], (int, float)) or not (0 <= pattern['confidence'] <= 1):
            logger.warning("confidence must be float between 0 and 1")
            return False
        
        return True
    
    def _row_to_dict(self, row) -> Dict[str, Any]:
        """Convert database row to dictionary"""
        try:
            data = dict(row)
            
            # Parse JSON fields
            if 'line_numbers' in data and data['line_numbers']:
                try:
                    data['line_numbers'] = json.loads(data['line_numbers'])
                except json.JSONDecodeError:
                    data['line_numbers'] = []
            
            if 'pattern_data' in data and data['pattern_data']:
                try:
                    data['pattern_data'] = json.loads(data['pattern_data'])
                except json.JSONDecodeError:
                    data['pattern_data'] = {}
            
            return data
            
        except Exception as e:
            logger.error(f"Error converting row to dict: {str(e)}")
            return {}
    
    def _update_cache(self, pattern_id: str, pattern_data: Dict[str, Any]):
        """Update pattern cache"""
        try:
            # Check cache size limit
            if len(self.pattern_cache) >= self.cache_stats["max_size"]:
                # Remove oldest entries (simple LRU)
                oldest_keys = sorted(self.pattern_cache.keys(), key=lambda k: self.pattern_cache[k].get('updated_at', ''))[:100]
                for key in oldest_keys:
                    del self.pattern_cache[key]
                    self.cache_stats["size"] -= 1
            
            # Add/update pattern in cache
            self.pattern_cache[pattern_id] = pattern_data
            self.cache_stats["size"] += 1
            
        except Exception as e:
            logger.error(f"Error updating cache: {str(e)}")
    
    def clear_cache(self):
        """Clear the pattern cache"""
        self.pattern_cache.clear()
        self.relationship_cache.clear()
        self.cache_stats["size"] = 0
        logger.info("✅ Pattern cache cleared")
    
    def close(self):
        """Close database connection"""
        if self.db_connection:
            self.db_connection.close()
            logger.info("✅ Pattern database connection closed")

# Example usage and testing
async def main():
    """Example usage of the PatternDatabase"""
    db = PatternDatabase("test_patterns.db")
    
    try:
        # Create some test patterns
        test_patterns = [
            {
                "pattern_id": "test_style_1",
                "pattern_type": "code_style",
                "pattern_name": "Consistent Naming",
                "description": "Uses consistent snake_case naming",
                "confidence": 0.9,
                "file_path": "test_file.py",
                "line_numbers": [1, 5, 10],
                "pattern_data": {"naming_convention": "snake_case", "consistency": 0.95},
                "detected_at": datetime.now().isoformat(),
                "effectiveness_score": 0.8
            },
            {
                "pattern_id": "test_arch_1",
                "pattern_type": "architecture",
                "pattern_name": "MVC Pattern",
                "description": "Follows Model-View-Controller architecture",
                "confidence": 0.85,
                "file_path": "project/",
                "line_numbers": [],
                "pattern_data": {"architecture": "MVC", "layers": ["models", "views", "controllers"]},
                "detected_at": datetime.now().isoformat(),
                "effectiveness_score": 0.9
            }
        ]
        
        # Store patterns
        print("📝 Storing test patterns...")
        for pattern in test_patterns:
            success = await db.store_pattern(pattern)
            print(f"  {'✅' if success else '❌'} {pattern['pattern_name']}")
        
        # Retrieve patterns
        print("\n🔍 Retrieving patterns...")
        for pattern in test_patterns:
            retrieved = await db.get_pattern(pattern['pattern_id'])
            if retrieved:
                print(f"  ✅ {retrieved['pattern_name']} - Confidence: {retrieved['confidence']}")
            else:
                print(f"  ❌ Failed to retrieve {pattern['pattern_id']}")
        
        # Find similar patterns
        print("\n🔍 Finding similar patterns...")
        context = {
            "pattern_type": "code_style",
            "confidence_threshold": 0.8
        }
        similar = await db.find_similar(context, limit=5)
        print(f"  Found {len(similar)} similar patterns")
        
        # Update effectiveness
        print("\n📊 Updating pattern effectiveness...")
        await db.update_pattern_effectiveness("test_style_1", {
            "success": True,
            "user_feedback": 4,
            "context_hash": "test_context_123"
        })
        
        # Get statistics
        print("\n📈 Getting database statistics...")
        stats = await db.get_pattern_statistics()
        if stats.get("success"):
            print(f"  Total patterns: {stats['total_patterns']}")
            print(f"  Cache hit rate: {stats['cache_statistics']['hit_rate']:.2%}")
            print(f"  Database size: {stats['database_size']} bytes")
        else:
            print(f"  ❌ Failed to get statistics: {stats.get('error')}")
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
    
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(main())
