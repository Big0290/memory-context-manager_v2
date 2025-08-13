#!/usr/bin/env python3
"""
Web Crawler MCP Tools - Integration with Memory Context Manager v2
Provides MCP tools for web crawling, learning bit extraction, and content management
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import sqlite3
import os

from web_crawler.engine.web_crawler_engine import WebCrawler, CrawlConfig, LearningBit, BackgroundCrawlerManager
from integration import SymbioticIntegrationBridge
from web_crawler.discovery.extensive_search_engine import MultiSiteDiscoveryEngine, DiscoveryConfig
from web_crawler.search.search_engine_integration import SearchEngineIntegration, SearchEngineConfig

logger = logging.getLogger(__name__)

class WebCrawlerMCPTools:
    """MCP tools for web crawling and learning bit management"""
    
    def __init__(self, db_path: str):
        """Initialize MCP tools with web crawler"""
        self.crawler = WebCrawler(db_path)
        self.background_manager = BackgroundCrawlerManager(db_path)
        self.symbiotic_bridge = SymbioticIntegrationBridge(db_path)
        self.extensive_search_engine = MultiSiteDiscoveryEngine(db_path)
        
        # Initialize search engine integration
        search_config = SearchEngineConfig(
            google_custom_search_api_key=os.getenv('GOOGLE_CUSTOM_SEARCH_API_KEY', ''),
            google_custom_search_engine_id=os.getenv('GOOGLE_CUSTOM_SEARCH_ENGINE_ID', ''),
            bing_search_api_key=os.getenv('BING_SEARCH_API_KEY', '')
        )
        self.search_engine_integration = SearchEngineIntegration(db_path, search_config)
        
        logger.info("✅ Web crawler MCP tools initialized with background manager, symbiotic bridge, extensive search engine, and search engine integration")
        self.active_crawls: Dict[str, Dict[str, Any]] = {}
    
    async def crawl_website(
        self,
        url: str,
        max_pages: int = 50,
        max_depth: int = 3,
        follow_links: bool = True,
        crawl_delay: float = 1.0,
        respect_robots: bool = True
    ) -> Dict[str, Any]:
        """
        🕷️ Crawl a website and extract learning bits
        
        Crawls a website starting from the given URL, extracts structured learning content,
        categorizes it precisely, and stores it in the memory system for future reference.
        
        Args:
            url: Starting URL for the crawl
            max_pages: Maximum number of pages to crawl
            max_depth: Maximum depth for link following
            follow_links: Whether to follow discovered links
            crawl_delay: Delay between requests in seconds
            respect_robots: Whether to respect robots.txt
        
        Returns:
            Crawl session results with statistics
        """
        try:
            logger.info(f"🕷️ Starting website crawl: {url}")
            
            # Create crawler configuration
            config = CrawlConfig(
                max_depth=max_depth,
                crawl_delay=crawl_delay,
                respect_robots_txt=respect_robots,
                follow_links=follow_links
            )
            
            # Initialize crawler
            self.crawler = WebCrawler(self.db_path, config)
            
            # Start crawl session
            crawl_id = f"crawl_{int(datetime.now().timestamp())}"
            self.active_crawls[crawl_id] = {
                'url': url,
                'start_time': datetime.now(),
                'status': 'running',
                'config': config.__dict__
            }
            
            # Perform the crawl
            result = await self.crawler.crawl_website(url, max_pages)
            
            # Update session status
            self.active_crawls[crawl_id]['status'] = 'completed'
            self.active_crawls[crawl_id]['end_time'] = datetime.now()
            self.active_crawls[crawl_id]['result'] = result
            
            # Get learning bit count
            learning_bits = await self.crawler.get_learning_bits(limit=1000)
            total_bits = len(learning_bits)
            
            logger.info(f"✅ Website crawl completed: {result['total_pages']} pages, {total_bits} learning bits")
            
            return {
                "success": True,
                "crawl_id": crawl_id,
                "url": url,
                "total_pages_crawled": result['total_pages'],
                "total_learning_bits_extracted": total_bits,
                "crawl_duration_seconds": result.get('duration', 0),
                "status": "completed",
                "message": f"Successfully crawled {url} and extracted {total_bits} learning bits"
            }
            
        except Exception as e:
            logger.error(f"❌ Website crawl failed: {e}")
            if 'crawl_id' in locals() and crawl_id in self.active_crawls:
                self.active_crawls[crawl_id]['status'] = 'failed'
                self.active_crawls[crawl_id]['error'] = str(e)
            
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to crawl website: {e}"
            }
    
    async def get_learning_bits(
        self,
        category: Optional[str] = None,
        subcategory: Optional[str] = None,
        content_type: Optional[str] = None,
        complexity_level: Optional[str] = None,
        min_importance: float = 0.0,
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        📚 Retrieve learning bits from the crawled content database
        
        Retrieves and filters learning bits based on various criteria including
        category, subcategory, content type, complexity, and importance score.
        
        Args:
            category: Filter by main category (programming, api, tutorial, etc.)
            subcategory: Filter by subcategory (python, javascript, etc.)
            content_type: Filter by content type (concept, example, definition, etc.)
            complexity_level: Filter by complexity (beginner, intermediate, advanced)
            min_importance: Minimum importance score (0.0 to 1.0)
            limit: Maximum number of results to return
        
        Returns:
            List of learning bits matching the criteria
        """
        try:
            if not self.crawler:
                self.crawler = WebCrawler(self.db_path)
            
            # Get learning bits from database
            learning_bits = await self.crawler.get_learning_bits(
                category=category,
                subcategory=subcategory,
                content_type=content_type,
                limit=limit * 2  # Get more to filter by importance
            )
            
            # Filter by importance and complexity if specified
            filtered_bits = []
            for bit in learning_bits:
                if bit.get('importance_score', 0) >= min_importance:
                    if complexity_level is None or bit.get('complexity_level') == complexity_level:
                        filtered_bits.append(bit)
            
            # Limit results
            filtered_bits = filtered_bits[:limit]
            
            # Prepare response
            response = {
                "success": True,
                "total_found": len(filtered_bits),
                "filters_applied": {
                    "category": category,
                    "subcategory": subcategory,
                    "content_type": content_type,
                    "complexity_level": complexity_level,
                    "min_importance": min_importance
                },
                "learning_bits": []
            }
            
            # Format learning bits for response
            for bit in filtered_bits:
                formatted_bit = {
                    "id": bit.get('id'),
                    "content_type": bit.get('content_type'),
                    "category": bit.get('category'),
                    "subcategory": bit.get('subcategory'),
                    "content": bit.get('content', '')[:500] + "..." if len(bit.get('content', '')) > 500 else bit.get('content', ''),
                    "context": bit.get('context', '')[:200] + "..." if len(bit.get('context', '')) > 200 else bit.get('context', ''),
                    "importance_score": bit.get('importance_score'),
                    "confidence_score": bit.get('confidence_score'),
                    "complexity_level": bit.get('complexity_level'),
                    "source_url": bit.get('source_url'),
                    "tags": bit.get('tags', []),
                    "extracted_at": bit.get('extracted_at'),
                    "reference_count": bit.get('reference_count', 0)
                }
                response["learning_bits"].append(formatted_bit)
            
            logger.info(f"📚 Retrieved {len(filtered_bits)} learning bits")
            return response
            
        except Exception as e:
            logger.error(f"❌ Failed to retrieve learning bits: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to retrieve learning bits: {e}"
            }
    
    async def search_learning_bits(
        self,
        query: str,
        category: Optional[str] = None,
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        🔍 Search learning bits by content and context
        
        Performs semantic search through all extracted learning bits to find
        relevant content based on the search query.
        
        Args:
            query: Search query string
            category: Optional category filter
            limit: Maximum number of results to return
        
        Returns:
            Search results with relevance scoring
        """
        try:
            if not self.crawler:
                self.crawler = WebCrawler(self.db_path)
            
            # Perform search
            search_results = await self.crawler.search_learning_bits(query, limit=limit * 2)
            
            # Filter by category if specified
            if category:
                search_results = [bit for bit in search_results if bit.get('category') == category]
            
            # Limit results
            search_results = search_results[:limit]
            
            # Calculate relevance scores (simple keyword matching for now)
            for bit in search_results:
                content_lower = bit.get('content', '').lower()
                query_lower = query.lower()
                
                # Simple relevance scoring
                relevance = 0.0
                for word in query_lower.split():
                    if word in content_lower:
                        relevance += 0.1
                
                # Boost by importance and confidence
                relevance += (bit.get('importance_score', 0.5) * 0.3)
                relevance += (bit.get('confidence_score', 0.8) * 0.2)
                
                bit['relevance_score'] = min(1.0, relevance)
            
            # Sort by relevance
            search_results.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
            
            # Format response
            response = {
                "success": True,
                "query": query,
                "total_results": len(search_results),
                "category_filter": category,
                "results": []
            }
            
            for bit in search_results:
                formatted_result = {
                    "id": bit.get('id'),
                    "content_type": bit.get('content_type'),
                    "category": bit.get('category'),
                    "subcategory": bit.get('subcategory'),
                    "content": bit.get('content', '')[:400] + "..." if len(bit.get('content', '')) > 400 else bit.get('content', ''),
                    "context": bit.get('context', '')[:200] + "..." if len(bit.get('context', '')) > 200 else bit.get('context', ''),
                    "relevance_score": bit.get('relevance_score'),
                    "importance_score": bit.get('importance_score'),
                    "source_url": bit.get('source_url'),
                    "tags": bit.get('tags', [])
                }
                response["results"].append(formatted_result)
            
            logger.info(f"🔍 Search for '{query}' returned {len(search_results)} results")
            return response
            
        except Exception as e:
            logger.error(f"❌ Search failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Search failed: {e}"
            }
    
    async def get_crawl_status(self, crawl_id: Optional[str] = None) -> Dict[str, Any]:
        """
        📊 Get status of web crawling operations
        
        Returns the status of active or completed crawl sessions,
        including progress, statistics, and any errors encountered.
        
        Args:
            crawl_id: Specific crawl session ID, or None for all sessions
        
        Returns:
            Crawl session status information
        """
        try:
            if crawl_id:
                if crawl_id in self.active_crawls:
                    return {
                        "success": True,
                        "crawl_id": crawl_id,
                        "status": self.active_crawls[crawl_id]
                    }
                else:
                    return {
                        "success": False,
                        "error": "Crawl ID not found",
                        "message": f"Crawl session {crawl_id} not found"
                    }
            else:
                # Return all crawl sessions
                return {
                    "success": True,
                    "total_active_crawls": len([c for c in self.active_crawls.values() if c.get('status') == 'running']),
                    "total_completed_crawls": len([c for c in self.active_crawls.values() if c.get('status') == 'completed']),
                    "total_failed_crawls": len([c for c in self.active_crawls.values() if c.get('status') == 'failed']),
                    "crawl_sessions": self.active_crawls
                }
                
        except Exception as e:
            logger.error(f"❌ Failed to get crawl status: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to get crawl status: {e}"
            }
    
    async def get_learning_statistics(self) -> Dict[str, Any]:
        """
        📈 Get comprehensive statistics about extracted learning content
        
        Provides detailed statistics about the learning bits database including
        counts by category, content type, complexity, and usage patterns.
        
        Returns:
            Comprehensive learning content statistics
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get total counts
                cursor.execute("SELECT COUNT(*) FROM learning_bits")
                total_bits = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM crawled_pages")
                total_pages = cursor.fetchone()[0]
                
                # Get counts by category
                cursor.execute("""
                    SELECT category, COUNT(*) as count 
                    FROM learning_bits 
                    GROUP BY category 
                    ORDER BY count DESC
                """)
                category_counts = dict(cursor.fetchall())
                
                # Get counts by content type
                cursor.execute("""
                    SELECT content_type, COUNT(*) as count 
                    FROM learning_bits 
                    GROUP BY content_type 
                    ORDER BY count DESC
                """)
                content_type_counts = dict(cursor.fetchall())
                
                # Get counts by complexity
                cursor.execute("""
                    SELECT complexity_level, COUNT(*) as count 
                    FROM learning_bits 
                    GROUP BY complexity_level 
                    ORDER BY count DESC
                """)
                complexity_counts = dict(cursor.fetchall())
                
                # Get top domains
                cursor.execute("""
                    SELECT cp.domain, COUNT(lb.id) as bit_count 
                    FROM learning_bits lb
                    JOIN crawled_pages cp ON lb.page_id = cp.id
                    GROUP BY cp.domain 
                    ORDER BY bit_count DESC 
                    LIMIT 10
                """)
                top_domains = dict(cursor.fetchall())
                
                # Get average importance and confidence
                cursor.execute("""
                    SELECT 
                        AVG(importance_score) as avg_importance,
                        AVG(confidence_score) as avg_confidence,
                        AVG(reference_count) as avg_references
                    FROM learning_bits
                """)
                avg_stats = cursor.fetchone()
                
                # Get recent activity
                cursor.execute("""
                    SELECT COUNT(*) FROM learning_bits 
                    WHERE created_at >= datetime('now', '-7 days')
                """)
                recent_bits = cursor.fetchone()[0]
                
                return {
                    "success": True,
                    "total_learning_bits": total_bits,
                    "total_crawled_pages": total_pages,
                    "category_distribution": category_counts,
                    "content_type_distribution": content_type_counts,
                    "complexity_distribution": complexity_counts,
                    "top_source_domains": top_domains,
                    "average_scores": {
                        "importance": round(avg_stats[0] or 0, 3),
                        "confidence": round(avg_stats[1] or 0, 3),
                        "references": round(avg_stats[2] or 0, 1)
                    },
                    "recent_activity": {
                        "bits_last_7_days": recent_bits
                    },
                    "database_info": {
                        "path": self.db_path,
                        "last_updated": datetime.now().isoformat()
                    }
                }
                
        except Exception as e:
            logger.error(f"❌ Failed to get learning statistics: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to get learning statistics: {e}"
            }
    
    async def add_categorization_rule(
        self,
        rule_name: str,
        rule_type: str,
        pattern: str,
        category: str,
        subcategory: Optional[str] = None,
        confidence_boost: float = 0.1,
        priority: int = 5
    ) -> Dict[str, Any]:
        """
        ⚙️ Add a new categorization rule for learning bit classification
        
        Creates custom rules for automatically categorizing learning bits
        based on patterns, keywords, or structural elements.
        
        Args:
            rule_name: Unique name for the rule
            rule_type: Type of rule (keyword, pattern, structure, semantic)
            pattern: The pattern or keyword to match
            category: Main category to assign
            subcategory: Optional subcategory
            confidence_boost: Confidence score boost when rule matches
            priority: Rule priority (1=highest, 10=lowest)
        
        Returns:
            Result of rule creation
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if rule already exists
                cursor.execute(
                    "SELECT id FROM categorization_rules WHERE rule_name = ?",
                    (rule_name,)
                )
                
                if cursor.fetchone():
                    return {
                        "success": False,
                        "error": "Rule name already exists",
                        "message": f"Rule '{rule_name}' already exists"
                    }
                
                # Insert new rule
                cursor.execute("""
                    INSERT INTO categorization_rules 
                    (rule_name, rule_type, pattern, category, subcategory, 
                     confidence_boost, priority, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (rule_name, rule_type, pattern, category, subcategory,
                      confidence_boost, priority, True))
                
                conn.commit()
                
                logger.info(f"✅ Added categorization rule: {rule_name}")
                
                return {
                    "success": True,
                    "rule_name": rule_name,
                    "rule_id": cursor.lastrowid,
                    "message": f"Successfully added categorization rule '{rule_name}'"
                }
                
        except Exception as e:
            logger.error(f"❌ Failed to add categorization rule: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to add categorization rule: {e}"
            }
    
    async def get_categorization_rules(self) -> Dict[str, Any]:
        """
        📋 Get all active categorization rules
        
        Returns the list of all active categorization rules used for
        automatically classifying learning bits.
        
        Returns:
            List of categorization rules with their configurations
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT rule_name, rule_type, pattern, category, subcategory,
                           confidence_boost, priority, is_active, created_at
                    FROM categorization_rules
                    ORDER BY priority ASC, created_at DESC
                """)
                
                rules = []
                for row in cursor.fetchall():
                    rule = {
                        "rule_name": row[0],
                        "rule_type": row[1],
                        "pattern": row[2],
                        "category": row[3],
                        "subcategory": row[4],
                        "confidence_boost": row[5],
                        "priority": row[6],
                        "is_active": bool(row[7]),
                        "created_at": row[8]
                    }
                    rules.append(rule)
                
                return {
                    "success": True,
                    "total_rules": len(rules),
                    "active_rules": len([r for r in rules if r['is_active']]),
                    "rules": rules
                }
                
        except Exception as e:
            logger.error(f"❌ Failed to get categorization rules: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to get categorization rules: {e}"
            }
    
    async def get_comprehensive_learning_report(self) -> Dict[str, Any]:
        """Get comprehensive learning coverage report"""
        try:
            report = await self.crawler.get_comprehensive_learning_report()
            return {
                "success": True,
                "report": report,
                "message": "Comprehensive learning report generated successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to generate comprehensive learning report"
            }
    
    async def start_background_crawl(self, job_id: str, start_url: str, config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Start a background crawl job"""
        try:
            result = await self.background_manager.start_background_crawl(job_id, start_url, config)
            return {
                "success": True,
                "result": result,
                "message": "Background crawl job initiated"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to start background crawl"
            }
    
    async def get_background_crawl_status(self, job_id: str = None) -> Dict[str, Any]:
        """Get status of background crawls"""
        try:
            status = self.background_manager.get_crawl_status(job_id)
            return {
                "success": True,
                "status": status,
                "message": "Background crawl status retrieved"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to get background crawl status"
            }
    
    async def stop_background_crawl(self, job_id: str) -> Dict[str, Any]:
        """Stop an active background crawl"""
        try:
            result = self.background_manager.stop_crawl(job_id)
            return {
                "success": True,
                "result": result,
                "message": "Background crawl stop requested"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to stop background crawl"
            }
    
    async def get_learning_evolution_report(self) -> Dict[str, Any]:
        """Get comprehensive learning evolution report"""
        try:
            # Get learning evolution from crawler
            evolution = self.crawler.learning_evolution
            
            # Get intelligent processor insights
            processor_insights = {
                'total_patterns': len(self.crawler.intelligent_processor.learning_patterns),
                'pattern_breakdown': {},
                'quality_metrics': {}
            }
            
            # Analyze patterns
            for pattern_key, pattern_data in self.crawler.intelligent_processor.learning_patterns.items():
                processor_insights['pattern_breakdown'][pattern_key] = {
                    'success_count': pattern_data['success_count'],
                    'avg_importance': pattern_data['avg_importance'],
                    'avg_confidence': pattern_data['avg_confidence']
                }
            
            # Get recent learning bits for quality analysis
            recent_bits = await self.crawler.get_learning_bits(limit=100)
            if recent_bits:
                avg_importance = sum(bit['importance_score'] for bit in recent_bits) / len(recent_bits)
                avg_confidence = sum(bit['confidence_score'] for bit in recent_bits) / len(recent_bits)
                processor_insights['quality_metrics'] = {
                    'avg_importance': avg_importance,
                    'avg_confidence': avg_confidence,
                    'total_recent_bits': len(recent_bits)
                }
            
            report = {
                'learning_evolution': evolution,
                'processor_insights': processor_insights,
                'system_health': {
                    'total_extractions': evolution['total_extractions'],
                    'success_rate': (evolution['successful_extractions'] / evolution['total_extractions'] * 100) if evolution['total_extractions'] > 0 else 0,
                    'quality_improvements': evolution['quality_improvements'],
                    'pattern_discoveries': evolution['pattern_discoveries']
                }
            }
            
            return {
                "success": True,
                "report": report,
                "message": "Learning evolution report generated successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to generate learning evolution report"
            }
    
    async def establish_symbiotic_integration(self) -> Dict[str, Any]:
        """Establish symbiotic integration between all systems"""
        try:
            result = await self.symbiotic_bridge.establish_symbiotic_connections()
            return {
                "success": True,
                "result": result,
                "message": "Symbiotic integration established successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to establish symbiotic integration"
            }
    
    async def get_symbiotic_status(self) -> Dict[str, Any]:
        """Get current symbiotic integration status"""
        try:
            status = await self.symbiotic_bridge.get_symbiotic_status()
            return {
                "success": True,
                "status": status,
                "message": "Symbiotic status retrieved successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to get symbiotic status"
            }
    
    async def trigger_symbiotic_learning_cycle(self) -> Dict[str, Any]:
        """Trigger a complete symbiotic learning cycle"""
        try:
            result = await self.symbiotic_bridge.trigger_symbiotic_learning_cycle()
            return {
                "success": True,
                "result": result,
                "message": "Symbiotic learning cycle triggered successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to trigger symbiotic learning cycle"
            }
    
    async def start_multi_site_discovery(self, seed_urls: List[str], discovery_depth: int = None) -> Dict[str, Any]:
        """Start a multi-site discovery session to find related websites"""
        try:
            result = await self.extensive_search_engine.start_discovery_session(seed_urls, discovery_depth)
            return {
                "success": True,
                "result": result,
                "message": "Multi-site discovery session initiated successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to start multi-site discovery"
            }
    
    async def get_discovery_status(self) -> Dict[str, Any]:
        """Get current multi-site discovery status and metrics"""
        try:
            status = await self.extensive_search_engine.get_discovery_status()
            return {
                "success": True,
                "status": status,
                "message": "Discovery status retrieved successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to get discovery status"
            }
    
    async def stop_discovery_session(self, session_id: str) -> Dict[str, Any]:
        """Stop an active multi-site discovery session"""
        try:
            result = await self.extensive_search_engine.stop_discovery_session(session_id)
            return {
                "success": True,
                "result": result,
                "message": "Discovery session stop requested"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to stop discovery session"
            }
    
    async def get_discovered_sites_report(self) -> Dict[str, Any]:
        """Get comprehensive report on discovered sites and relationships"""
        try:
            # Get discovered sites from database
            with sqlite3.connect(self.extensive_search_engine.db_path) as conn:
                cursor = conn.cursor()
                
                # Get discovered sites summary
                cursor.execute("""
                    SELECT content_type, COUNT(*) as count, AVG(relevance_score) as avg_relevance
                    FROM discovered_sites
                    GROUP BY content_type
                    ORDER BY count DESC
                """)
                content_type_summary = cursor.fetchall()
                
                # Get domain relationships
                cursor.execute("""
                    SELECT source_domain, target_domain, relationship_type, relationship_strength
                    FROM domain_relationships
                    ORDER BY relationship_strength DESC
                    LIMIT 20
                """)
                domain_relationships = cursor.fetchall()
                
                # Get cross references
                cursor.execute("""
                    SELECT relationship_type, COUNT(*) as count, AVG(relationship_strength) as avg_strength
                    FROM cross_references
                    GROUP BY relationship_type
                    ORDER BY count DESC
                """)
                cross_references_summary = cursor.fetchall()
                
                # Get discovery metrics
                discovery_metrics = self.extensive_search_engine.discovery_metrics
                
                report = {
                    'discovery_metrics': discovery_metrics,
                    'content_type_distribution': [
                        {
                            'type': row[0],
                            'count': row[1],
                            'avg_relevance': row[2]
                        } for row in content_type_summary
                    ],
                    'domain_relationships': [
                        {
                            'source': row[0],
                            'target': row[1],
                            'type': row[2],
                            'strength': row[3]
                        } for row in domain_relationships
                    ],
                    'cross_references_summary': [
                        {
                            'type': row[0],
                            'count': row[1],
                            'avg_strength': row[2]
                        } for row in cross_references_summary
                    ]
                }
                
                return {
                    "success": True,
                    "report": report,
                    "message": "Discovered sites report generated successfully"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to generate discovered sites report"
            }
    
    async def perform_multi_engine_search(self, query: str, max_results: int = None, 
                                        engines: List[str] = None) -> Dict[str, Any]:
        """Perform search across multiple search engines (Google, Bing)"""
        try:
            results = await self.search_engine_integration.perform_multi_engine_search(
                query, max_results, engines
            )
            
            # Convert results to serializable format
            serializable_results = []
            for result in results:
                serializable_results.append({
                    'result_id': result.result_id,
                    'title': result.title,
                    'url': result.url,
                    'description': result.description,
                    'source_engine': result.source_engine,
                    'relevance_score': result.relevance_score,
                    'content_type': result.content_type,
                    'domain': result.domain,
                    'search_query': result.search_query,
                    'result_rank': result.result_rank,
                    'metadata': result.metadata,
                    'discovered_at': result.discovered_at.isoformat()
                })
            
            return {
                "success": True,
                "results": serializable_results,
                "total_results": len(serializable_results),
                "query": query,
                "engines_used": engines or ['google', 'bing'],
                "message": f"Multi-engine search completed with {len(serializable_results)} results"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to perform multi-engine search"
            }
    
    async def get_search_engine_metrics(self) -> Dict[str, Any]:
        """Get search engine performance metrics and status"""
        try:
            metrics = await self.search_engine_integration.get_search_metrics()
            return {
                "success": True,
                "metrics": metrics,
                "message": "Search engine metrics retrieved successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to get search engine metrics"
            }
    
    async def search_and_discover_content(self, query: str, max_results: int = 20) -> Dict[str, Any]:
        """Combined search and discovery - search engines + multi-site discovery"""
        try:
            logger.info(f"🔍 Starting combined search and discovery for: '{query}'")
            
            # Step 1: Search engines
            search_results = await self.search_engine_integration.perform_multi_engine_search(
                query, max_results // 2
            )
            
            # Step 2: Extract URLs from search results for discovery
            search_urls = [result.url for result in search_results]
            
            # Step 3: Start multi-site discovery with search results
            discovery_result = await self.extensive_search_engine.start_discovery_session(
                search_urls, discovery_depth=1
            )
            
            # Step 4: Get discovery status
            discovery_status = await self.extensive_search_engine.get_discovery_status()
            
            combined_result = {
                'search_results': len(search_results),
                'discovery_session': discovery_result.get('session_id'),
                'discovery_status': discovery_status,
                'total_sources': len(search_results) + discovery_status.get('discovered_sites_count', 0),
                'query': query,
                'search_engines_used': ['google', 'bing'],
                'discovery_method': 'search_engine_enhanced'
            }
            
            return {
                "success": True,
                "result": combined_result,
                "message": f"Combined search and discovery completed for '{query}'"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to perform combined search and discovery"
            }
    
    def register_tools(self, mcp_server):
        """Register all web crawler MCP tools with the MCP server"""
        # This method can be used to register tools with an MCP server
        # For now, the tools are available as instance methods
        logger.info("✅ Web crawler MCP tools available as instance methods")
        # Register comprehensive learning report tool
        mcp_server.add_tool(
            "get_comprehensive_learning_report",
            "Get comprehensive learning coverage and analysis report",
            self.get_comprehensive_learning_report
        )
        
        # Register background crawler tools
        mcp_server.add_tool(
            "start_background_crawl",
            "Start a background crawl job that runs without user interruption",
            self.start_background_crawl
        )
        
        mcp_server.add_tool(
            "get_background_crawl_status",
            "Get status of background crawls and queue",
            self.get_background_crawl_status
        )
        
        mcp_server.add_tool(
            "stop_background_crawl",
            "Stop an active background crawl job",
            self.stop_background_crawl
        )
        
        # Register learning evolution tool
        mcp_server.add_tool(
            "get_learning_evolution_report",
            "Get comprehensive report on learning evolution and intelligent processor insights",
            self.get_learning_evolution_report
        )
        
        # Register symbiotic integration tools
        mcp_server.add_tool(
            "establish_symbiotic_integration",
            "Establish symbiotic integration between web crawler and all learning/processing systems",
            self.establish_symbiotic_integration
        )
        
        mcp_server.add_tool(
            "get_symbiotic_status",
            "Get current symbiotic integration status between all systems",
            self.get_symbiotic_status
        )
        
        mcp_server.add_tool(
            "trigger_symbiotic_learning_cycle",
            "Trigger a complete symbiotic learning cycle across all integrated systems",
            self.trigger_symbiotic_learning_cycle
        )
        
        # Register extensive search tools
        mcp_server.add_tool(
            "start_multi_site_discovery",
            "Start a multi-site discovery session to find related websites across domains",
            self.start_multi_site_discovery
        )
        
        mcp_server.add_tool(
            "get_discovery_status",
            "Get current multi-site discovery status and metrics",
            self.get_discovery_status
        )
        
        mcp_server.add_tool(
            "stop_discovery_session",
            "Stop an active multi-site discovery session",
            self.stop_discovery_session
        )
        
        mcp_server.add_tool(
            "get_discovered_sites_report",
            "Get comprehensive report on discovered sites and cross-domain relationships",
            self.get_discovered_sites_report
        )
        
        # Register search engine integration tools
        mcp_server.add_tool(
            "perform_multi_engine_search",
            "Perform search across multiple search engines (Google, Bing) for enhanced content discovery",
            self.perform_multi_engine_search
        )
        
        mcp_server.add_tool(
            "get_search_engine_metrics",
            "Get search engine performance metrics and API status",
            self.get_search_engine_metrics
        )
        
        mcp_server.add_tool(
            "search_and_discover_content",
            "Combined search and discovery - search engines + multi-site discovery for comprehensive content finding",
            self.search_and_discover_content
        )
        return mcp_server

# Example usage
if __name__ == "__main__":
    # This module is designed to be imported and used by the MCP server
    print("Web Crawler MCP Tools - Import this module to register web crawling tools")
