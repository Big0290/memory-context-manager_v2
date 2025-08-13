#!/usr/bin/env python3
"""
Extensive Search Engine - Phase 3 of Memory Context Manager v2
Multi-site discovery, search engine integration, and cross-domain intelligence
"""

import asyncio
import aiohttp
import json
import logging
import re
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Set, Tuple, Union
from urllib.parse import urljoin, urlparse, urlunparse, parse_qs
from dataclasses import dataclass, asdict
import sqlite3
from bs4 import BeautifulSoup
import hashlib
from collections import defaultdict, deque

logger = logging.getLogger(__name__)

@dataclass
class DiscoveryConfig:
    """Configuration for extensive search and discovery"""
    max_discovery_depth: int = 5
    max_sites_per_discovery: int = 50
    max_pages_per_site: int = 100
    discovery_delay: float = 2.0
    timeout: int = 30  # HTTP request timeout in seconds
    search_api_rate_limit: int = 100  # requests per hour
    content_similarity_threshold: float = 0.6
    domain_relationship_threshold: float = 0.4
    max_concurrent_discoveries: int = 3
    enable_search_engines: bool = True
    enable_social_discovery: bool = True
    enable_trend_analysis: bool = True

@dataclass
class DiscoveredSite:
    """Information about a discovered website"""
    url: str
    domain: str
    title: str
    description: str
    content_type: str  # 'blog', 'documentation', 'news', 'academic', 'social'
    relevance_score: float
    discovery_method: str  # 'link_analysis', 'search_api', 'social_discovery'
    parent_site: Optional[str]
    discovery_depth: int
    last_updated: datetime
    metadata: Dict[str, Any]

@dataclass
class SearchQuery:
    """A search query for content discovery"""
    query_id: str
    query_text: str
    search_scope: str  # 'web', 'academic', 'news', 'social', 'all'
    target_domains: List[str]
    excluded_domains: List[str]
    content_types: List[str]
    time_range: str  # 'day', 'week', 'month', 'year', 'all'
    max_results: int
    created_at: datetime
    status: str  # 'pending', 'active', 'completed', 'failed'

@dataclass
class CrossReference:
    """Cross-reference relationship between different sources"""
    reference_id: str
    source_url: str
    target_url: str
    relationship_type: str  # 'similar_content', 'references', 'contradicts', 'extends'
    relationship_strength: float
    common_topics: List[str]
    content_overlap: float
    temporal_relationship: str  # 'contemporary', 'historical', 'evolutionary'
    created_at: datetime

class MultiSiteDiscoveryEngine:
    """Discovers related websites and content across domains"""
    
    def __init__(self, db_path: str, config: DiscoveryConfig = None):
        self.db_path = db_path
        self.config = config or DiscoveryConfig()
        self.session = None
        self.discovered_sites = {}
        self.discovery_queue = deque()
        self.active_discoveries = set()
        self.domain_relationships = defaultdict(set)
        self.content_similarity_cache = {}
        
        # Initialize database
        self._init_discovery_database()
        
        # Discovery metrics
        self.discovery_metrics = {
            'total_sites_discovered': 0,
            'total_pages_analyzed': 0,
            'cross_references_built': 0,
            'discovery_sessions': 0,
            'average_relevance_score': 0.0
        }
    
    def _init_discovery_database(self):
        """Initialize discovery database tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create discovered sites table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS discovered_sites (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        url TEXT UNIQUE,
                        domain TEXT,
                        title TEXT,
                        description TEXT,
                        content_type TEXT,
                        relevance_score REAL,
                        discovery_method TEXT,
                        parent_site TEXT,
                        discovery_depth INTEGER,
                        last_updated TIMESTAMP,
                        metadata TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create search queries table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS search_queries (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        query_id TEXT UNIQUE,
                        query_text TEXT,
                        search_scope TEXT,
                        target_domains TEXT,
                        excluded_domains TEXT,
                        content_types TEXT,
                        time_range TEXT,
                        max_results INTEGER,
                        created_at TIMESTAMP,
                        status TEXT
                    )
                """)
                
                # Create cross references table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS cross_references (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        reference_id TEXT UNIQUE,
                        source_url TEXT,
                        target_url TEXT,
                        relationship_type TEXT,
                        relationship_strength REAL,
                        common_topics TEXT,
                        content_overlap REAL,
                        temporal_relationship TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create domain relationships table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS domain_relationships (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        source_domain TEXT,
                        target_domain TEXT,
                        relationship_type TEXT,
                        relationship_strength REAL,
                        common_topics TEXT,
                        discovery_count INTEGER,
                        last_discovered TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create indices for performance
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_discovered_sites_domain ON discovered_sites (domain)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_discovered_sites_content_type ON discovered_sites (content_type)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_discovered_sites_relevance ON discovered_sites (relevance_score)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_cross_references_source ON cross_references (source_url)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_cross_references_target ON cross_references (target_url)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_domain_relationships_source ON domain_relationships (source_domain)")
                
                conn.commit()
                logger.info("✅ Discovery database initialized successfully")
                
        except Exception as e:
            logger.error(f"❌ Failed to initialize discovery database: {e}")
            raise
    
    async def start_discovery_session(self, seed_urls: List[str], 
                                    discovery_depth: int = None) -> Dict[str, Any]:
        """Start a multi-site discovery session"""
        try:
            session_id = f"discovery_{int(time.time())}"
            
            logger.info(f"🚀 Starting discovery session {session_id} with {len(seed_urls)} seed URLs")
            
            # Initialize discovery session
            self.discovery_metrics['discovery_sessions'] += 1
            
            # Set discovery depth
            max_depth = discovery_depth or self.config.max_discovery_depth
            
            # Add seed URLs to discovery queue
            for url in seed_urls:
                self.discovery_queue.append({
                    'url': url,
                    'depth': 0,
                    'parent': None,
                    'session_id': session_id
                })
            
            # Start discovery process
            discovery_task = asyncio.create_task(
                self._run_discovery_session(session_id, max_depth)
            )
            
            return {
                'status': 'started',
                'session_id': session_id,
                'seed_urls': seed_urls,
                'max_depth': max_depth,
                'message': f'Discovery session started with {len(seed_urls)} seed URLs'
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to start discovery session: {e}")
            return {
                'status': 'failed',
                'error': str(e),
                'message': 'Failed to start discovery session'
            }
    
    async def _run_discovery_session(self, session_id: str, max_depth: int):
        """Run the discovery session"""
        try:
            logger.info(f"🔍 Running discovery session {session_id} to depth {max_depth}")
            
            while self.discovery_queue and len(self.active_discoveries) < self.config.max_concurrent_discoveries:
                # Get next URL to discover
                discovery_item = self.discovery_queue.popleft()
                url = discovery_item['url']
                depth = discovery_item['depth']
                parent = discovery_item['parent']
                
                if depth > max_depth:
                    continue
                
                # Start discovery for this URL
                discovery_task = asyncio.create_task(
                    self._discover_site(url, depth, parent, session_id)
                )
                self.active_discoveries.add(discovery_task)
                discovery_task.add_done_callback(lambda t: self.active_discoveries.discard(t))
                
                # Rate limiting
                await asyncio.sleep(self.config.discovery_delay)
            
            # Wait for all active discoveries to complete
            if self.active_discoveries:
                await asyncio.gather(*self.active_discoveries)
            
            logger.info(f"✅ Discovery session {session_id} completed")
            
        except Exception as e:
            logger.error(f"❌ Discovery session {session_id} failed: {e}")
    
    async def _discover_site(self, url: str, depth: int, parent: Optional[str], 
                            session_id: str) -> Optional[DiscoveredSite]:
        """Discover a single site and find related sites"""
        try:
            logger.info(f"🔍 Discovering site: {url} (depth: {depth})")
            
            # Check if already discovered
            if url in self.discovered_sites:
                logger.debug(f"Site already discovered: {url}")
                return self.discovered_sites[url]
            
            # Fetch and analyze the site
            site_info = await self._analyze_site(url, depth, parent)
            if not site_info:
                return None
            
            # Store discovered site
            self.discovered_sites[url] = site_info
            await self._store_discovered_site(site_info)
            
            # Find related sites
            if depth < self.config.max_discovery_depth:
                related_sites = await self._find_related_sites(url, site_info)
                
                # Add related sites to discovery queue
                for related_url in related_sites:
                    if related_url not in self.discovered_sites:
                        self.discovery_queue.append({
                            'url': related_url,
                            'depth': depth + 1,
                            'parent': url,
                            'session_id': session_id
                        })
            
            # Update metrics
            self.discovery_metrics['total_sites_discovered'] += 1
            self.discovery_metrics['average_relevance_score'] = (
                (self.discovery_metrics['average_relevance_score'] * 
                 (self.discovery_metrics['total_sites_discovered'] - 1) + 
                 site_info.relevance_score) / 
                self.discovery_metrics['total_sites_discovered']
            )
            
            logger.info(f"✅ Site discovered: {url} (relevance: {site_info.relevance_score:.2f})")
            return site_info
            
        except Exception as e:
            logger.error(f"❌ Failed to discover site {url}: {e}")
            return None
    
    async def _analyze_site(self, url: str, depth: int, parent: Optional[str]) -> Optional[DiscoveredSite]:
        """Analyze a site to extract discovery information"""
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            # Fetch the page
            async with self.session.get(url, timeout=self.config.timeout) as response:
                if response.status != 200:
                    return None
                
                html_content = await response.text()
                soup = BeautifulSoup(html_content, 'html.parser')
                
                # Extract basic information
                title = soup.find('title')
                title_text = title.get_text().strip() if title else "Untitled"
                
                # Extract description
                description = ""
                meta_desc = soup.find('meta', attrs={'name': 'description'})
                if meta_desc:
                    description = meta_desc.get('content', '').strip()
                
                # Determine content type
                content_type = self._determine_content_type(url, title_text, description, html_content)
                
                # Calculate relevance score
                relevance_score = self._calculate_relevance_score(url, title_text, description, content_type)
                
                # Create discovered site
                site_info = DiscoveredSite(
                    url=url,
                    domain=urlparse(url).netloc,
                    title=title_text,
                    description=description,
                    content_type=content_type,
                    relevance_score=relevance_score,
                    discovery_method='link_analysis',
                    parent_site=parent,
                    discovery_depth=depth,
                    last_updated=datetime.now(),
                    metadata={
                        'html_size': len(html_content),
                        'has_code_blocks': bool(soup.find('code')),
                        'has_tables': bool(soup.find('table')),
                        'has_images': bool(soup.find('img')),
                        'language': 'en'  # Default, could be enhanced with language detection
                    }
                )
                
                return site_info
                
        except Exception as e:
            logger.error(f"❌ Failed to analyze site {url}: {e}")
            return None
    
    def _determine_content_type(self, url: str, title: str, description: str, html_content: str) -> str:
        """Determine the content type of a site"""
        url_lower = url.lower()
        title_lower = title.lower()
        desc_lower = description.lower()
        html_lower = html_content.lower()
        
        # Documentation sites
        if any(term in url_lower for term in ['docs', 'documentation', 'api', 'reference']):
            return 'documentation'
        
        # Blog sites
        if any(term in url_lower for term in ['blog', 'post', 'article', 'news']):
            return 'blog'
        
        # Academic sites
        if any(term in url_lower for term in ['edu', 'academic', 'research', 'paper', 'journal']):
            return 'academic'
        
        # Social media
        if any(term in url_lower for term in ['twitter', 'facebook', 'linkedin', 'reddit']):
            return 'social'
        
        # News sites
        if any(term in title_lower or term in desc_lower for term in ['news', 'breaking', 'latest']):
            return 'news'
        
        # Default to general
        return 'general'
    
    def _calculate_relevance_score(self, url: str, title: str, description: str, content_type: str) -> float:
        """Calculate relevance score for a discovered site"""
        score = 0.0
        
        # Content type relevance
        if content_type in ['documentation', 'academic', 'blog']:
            score += 0.3
        
        # Title quality
        if len(title) > 10 and len(title) < 100:
            score += 0.2
        
        # Description quality
        if len(description) > 20:
            score += 0.2
        
        # URL structure
        if not url.endswith(('.pdf', '.doc', '.txt')):
            score += 0.1
        
        # Domain quality
        domain = urlparse(url).netloc
        if domain and '.' in domain:
            score += 0.2
        
        return min(score, 1.0)
    
    async def _find_related_sites(self, source_url: str, site_info: DiscoveredSite) -> List[str]:
        """Find related sites through various discovery methods"""
        related_sites = set()
        
        try:
            # Method 1: Link analysis
            link_sites = await self._find_sites_through_links(source_url)
            related_sites.update(link_sites)
            
            # Method 2: Content similarity
            similar_sites = await self._find_sites_through_similarity(site_info)
            related_sites.update(similar_sites)
            
            # Method 3: Domain relationships
            domain_sites = await self._find_sites_through_domain_relationships(site_info.domain)
            related_sites.update(domain_sites)
            
            # Filter and score related sites
            filtered_sites = []
            for site in related_sites:
                if site != source_url and site not in self.discovered_sites:
                    relevance = self._calculate_site_relevance(site, site_info)
                    if relevance > self.config.content_similarity_threshold:
                        filtered_sites.append(site)
            
            return filtered_sites[:self.config.max_sites_per_discovery]
            
        except Exception as e:
            logger.error(f"❌ Failed to find related sites for {source_url}: {e}")
            return []
    
    async def _find_sites_through_links(self, source_url: str) -> List[str]:
        """Find sites through link analysis"""
        try:
            if not self.session:
                return []
            
            async with self.session.get(source_url) as response:
                if response.status != 200:
                    return []
                
                html_content = await response.text()
                soup = BeautifulSoup(html_content, 'html.parser')
                
                # Find external links
                external_links = []
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if href.startswith('http'):
                        external_links.append(href)
                
                return external_links[:20]  # Limit to top 20
                
        except Exception as e:
            logger.error(f"❌ Failed to find sites through links: {e}")
            return []
    
    async def _find_sites_through_similarity(self, site_info: DiscoveredSite) -> List[str]:
        """Find sites through content similarity analysis"""
        # This would implement semantic similarity search
        # For now, return empty list (to be implemented)
        return []
    
    async def _find_sites_through_domain_relationships(self, domain: str) -> List[str]:
        """Find sites through domain relationship analysis"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Find related domains
                cursor.execute("""
                    SELECT target_domain FROM domain_relationships 
                    WHERE source_domain = ? AND relationship_strength > ?
                """, (domain, self.config.domain_relationship_threshold))
                
                related_domains = [row[0] for row in cursor.fetchall()]
                
                # Convert to URLs (simplified)
                related_urls = [f"https://{domain}" for domain in related_domains]
                
                return related_urls
                
        except Exception as e:
            logger.error(f"❌ Failed to find sites through domain relationships: {e}")
            return []
    
    def _calculate_site_relevance(self, site_url: str, source_site: DiscoveredSite) -> float:
        """Calculate relevance between two sites"""
        # Simplified relevance calculation
        # In a full implementation, this would use semantic similarity
        
        source_domain = source_site.domain
        target_domain = urlparse(site_url).netloc
        
        # Same domain = high relevance
        if source_domain == target_domain:
            return 0.9
        
        # Similar domain structure = medium relevance
        if self._are_domains_similar(source_domain, target_domain):
            return 0.7
        
        # Different domain = low relevance
        return 0.3
    
    def _are_domains_similar(self, domain1: str, domain2: str) -> bool:
        """Check if two domains are similar"""
        # Extract main parts of domains
        parts1 = domain1.split('.')
        parts2 = domain2.split('.')
        
        # Check for common parts
        common_parts = set(parts1) & set(parts2)
        return len(common_parts) > 0
    
    async def _store_discovered_site(self, site_info: DiscoveredSite):
        """Store discovered site in database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT OR REPLACE INTO discovered_sites 
                    (url, domain, title, description, content_type, relevance_score, 
                     discovery_method, parent_site, discovery_depth, last_updated, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    site_info.url, site_info.domain, site_info.title, site_info.description,
                    site_info.content_type, site_info.relevance_score, site_info.discovery_method,
                    site_info.parent_site, site_info.discovery_depth, site_info.last_updated,
                    json.dumps(site_info.metadata)
                ))
                
                conn.commit()
                
        except Exception as e:
            logger.error(f"❌ Failed to store discovered site: {e}")
    
    async def get_discovery_status(self) -> Dict[str, Any]:
        """Get current discovery status and metrics"""
        return {
            'status': 'active' if self.discovery_queue or self.active_discoveries else 'idle',
            'discovery_queue_size': len(self.discovery_queue),
            'active_discoveries': len(self.active_discoveries),
            'discovered_sites_count': len(self.discovered_sites),
            'metrics': self.discovery_metrics,
            'domain_relationships_count': len(self.domain_relationships)
        }
    
    async def stop_discovery_session(self, session_id: str) -> Dict[str, Any]:
        """Stop a discovery session"""
        try:
            # Clear discovery queue for this session
            self.discovery_queue = deque([
                item for item in self.discovery_queue 
                if item.get('session_id') != session_id
            ])
            
            # Cancel active discoveries
            for task in list(self.active_discoveries):
                if hasattr(task, 'session_id') and getattr(task, 'session_id') == session_id:
                    task.cancel()
            
            return {
                'status': 'stopped',
                'session_id': session_id,
                'message': 'Discovery session stopped successfully'
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to stop discovery session: {e}")
            return {
                'status': 'failed',
                'error': str(e),
                'message': 'Failed to stop discovery session'
            }

# Example usage
async def main():
    """Test the extensive search engine"""
    engine = MultiSiteDiscoveryEngine('brain_memory_store/brain.db')
    
    # Start discovery session
    seed_urls = ['https://docs.cursor.com/en/context/mcp']
    result = await engine.start_discovery_session(seed_urls, discovery_depth=2)
    
    print(f"Discovery result: {result}")
    
    # Wait for discovery to complete
    await asyncio.sleep(10)
    
    # Get status
    status = await engine.get_discovery_status()
    print(f"Discovery status: {status}")

if __name__ == "__main__":
    asyncio.run(main())
