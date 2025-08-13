#!/usr/bin/env python3
"""
Search Engine Integration - Phase 3B of Memory Context Manager v2
Google Custom Search API and Bing Web Search API integration for enhanced discovery
"""

import asyncio
import aiohttp
import json
import logging
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
import os
import base64
import hmac
import hashlib
import urllib.parse

logger = logging.getLogger(__name__)

@dataclass
class SearchEngineConfig:
    """Configuration for search engine integration"""
    google_custom_search_api_key: str = ""
    google_custom_search_engine_id: str = ""
    bing_search_api_key: str = ""
    bing_search_endpoint: str = "https://api.bing.microsoft.com/v7.0/search"
    search_rate_limit: int = 100  # requests per hour
    max_results_per_query: int = 50
    result_filtering_threshold: float = 0.6
    enable_google_search: bool = True
    enable_bing_search: bool = True
    enable_duplicate_filtering: bool = True
    enable_relevance_scoring: bool = True

@dataclass
class SearchResult:
    """A search result from any search engine"""
    result_id: str
    title: str
    url: str
    description: str
    source_engine: str  # 'google', 'bing', 'combined'
    relevance_score: float
    content_type: str
    domain: str
    search_query: str
    result_rank: int
    metadata: Dict[str, Any]
    discovered_at: datetime

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
    search_engines: List[str]  # ['google', 'bing']
    created_at: datetime
    status: str  # 'pending', 'active', 'completed', 'failed'

class GoogleCustomSearchAPI:
    """Google Custom Search API integration"""
    
    def __init__(self, api_key: str, engine_id: str):
        self.api_key = api_key
        self.engine_id = engine_id
        self.base_url = "https://www.googleapis.com/customsearch/v1"
        self.rate_limit_remaining = 100
        self.rate_limit_reset = datetime.now() + timedelta(hours=1)
    
    async def search(self, query: str, max_results: int = 10) -> List[SearchResult]:
        """Perform Google Custom Search"""
        try:
            if not self.api_key or not self.engine_id:
                logger.warning("⚠️ Google Custom Search not configured")
                return []
            
            if self.rate_limit_remaining <= 0:
                logger.warning("⚠️ Google API rate limit reached")
                return []
            
            # Prepare search parameters
            params = {
                'key': self.api_key,
                'cx': self.engine_id,
                'q': query,
                'num': min(max_results, 10),  # Google limit is 10 per request
                'start': 1
            }
            
            # Perform search
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params) as response:
                    if response.status != 200:
                        logger.error(f"❌ Google search failed: {response.status}")
                        return []
                    
                    data = await response.json()
                    
                    # Update rate limit info
                    if 'quotaLimit' in data.get('queries', {}).get('request', [{}])[0]:
                        self.rate_limit_remaining = data['queries']['request'][0]['quotaLimit']
                    
                    # Parse results
                    results = []
                    if 'items' in data:
                        for i, item in enumerate(data['items']):
                            result = SearchResult(
                                result_id=f"google_{hashlib.md5(item['link'].encode()).hexdigest()}",
                                title=item.get('title', ''),
                                url=item['link'],
                                description=item.get('snippet', ''),
                                source_engine='google',
                                relevance_score=self._calculate_google_relevance(item, i),
                                content_type=self._determine_content_type(item),
                                domain=urlparse(item['link']).netloc,
                                search_query=query,
                                result_rank=i + 1,
                                metadata={
                                    'displayLink': item.get('displayLink', ''),
                                    'formattedUrl': item.get('formattedUrl', ''),
                                    'pagemap': item.get('pagemap', {}),
                                    'queries': data.get('queries', {})
                                },
                                discovered_at=datetime.now()
                            )
                            results.append(result)
                    
                    logger.info(f"✅ Google search completed: {len(results)} results for '{query}'")
                    return results
                    
        except Exception as e:
            logger.error(f"❌ Google search error: {e}")
            return []
    
    def _calculate_google_relevance(self, item: Dict[str, Any], rank: int) -> float:
        """Calculate relevance score for Google search result"""
        score = 0.0
        
        # Rank-based scoring (Google ranks by relevance)
        if rank == 0:
            score += 0.4
        elif rank < 3:
            score += 0.3
        elif rank < 5:
            score += 0.2
        else:
            score += 0.1
        
        # Title quality
        title = item.get('title', '')
        if len(title) > 10 and len(title) < 100:
            score += 0.2
        
        # Description quality
        snippet = item.get('snippet', '')
        if len(snippet) > 20:
            score += 0.2
        
        # URL quality
        url = item.get('link', '')
        if not url.endswith(('.pdf', '.doc', '.txt')):
            score += 0.1
        
        # Domain quality
        domain = urlparse(url).netloc
        if domain and '.' in domain:
            score += 0.1
        
        return min(score, 1.0)
    
    def _determine_content_type(self, item: Dict[str, Any]) -> str:
        """Determine content type from Google search result"""
        url = item.get('link', '').lower()
        title = item.get('title', '').lower()
        snippet = item.get('snippet', '').lower()
        
        # Documentation sites
        if any(term in url for term in ['docs', 'documentation', 'api', 'reference']):
            return 'documentation'
        
        # Blog sites
        if any(term in url for term in ['blog', 'post', 'article', 'news']):
            return 'blog'
        
        # Academic sites
        if any(term in url for term in ['edu', 'academic', 'research', 'paper', 'journal']):
            return 'academic'
        
        # Social media
        if any(term in url for term in ['twitter', 'facebook', 'linkedin', 'reddit']):
            return 'social'
        
        # News sites
        if any(term in title or term in snippet for term in ['news', 'breaking', 'latest']):
            return 'news'
        
        return 'general'

class BingWebSearchAPI:
    """Bing Web Search API integration"""
    
    def __init__(self, api_key: str, endpoint: str = None):
        self.api_key = api_key
        self.endpoint = endpoint or "https://api.bing.microsoft.com/v7.0/search"
        self.rate_limit_remaining = 100
        self.rate_limit_reset = datetime.now() + timedelta(hours=1)
    
    async def search(self, query: str, max_results: int = 10) -> List[SearchResult]:
        """Perform Bing Web Search"""
        try:
            if not self.api_key:
                logger.warning("⚠️ Bing Web Search not configured")
                return []
            
            if self.rate_limit_remaining <= 0:
                logger.warning("⚠️ Bing API rate limit reached")
                return []
            
            # Prepare headers
            headers = {
                'Ocp-Apim-Subscription-Key': self.api_key,
                'Accept': 'application/json'
            }
            
            # Prepare search parameters
            params = {
                'q': query,
                'count': min(max_results, 50),  # Bing limit is 50 per request
                'offset': 0,
                'mkt': 'en-US',
                'safesearch': 'Moderate'
            }
            
            # Perform search
            async with aiohttp.ClientSession() as session:
                async with session.get(self.endpoint, headers=headers, params=params) as response:
                    if response.status != 200:
                        logger.error(f"❌ Bing search failed: {response.status}")
                        return []
                    
                    data = await response.json()
                    
                    # Parse results
                    results = []
                    if 'webPages' in data and 'value' in data['webPages']:
                        for i, item in enumerate(data['webPages']['value']):
                            result = SearchResult(
                                result_id=f"bing_{hashlib.md5(item['url'].encode()).hexdigest()}",
                                title=item.get('name', ''),
                                url=item['url'],
                                description=item.get('snippet', ''),
                                source_engine='bing',
                                relevance_score=self._calculate_bing_relevance(item, i),
                                content_type=self._determine_content_type(item),
                                domain=urlparse(item['url']).netloc,
                                search_query=query,
                                result_rank=i + 1,
                                metadata={
                                    'displayUrl': item.get('displayUrl', ''),
                                    'dateLastCrawled': item.get('dateLastCrawled', ''),
                                    'language': item.get('language', ''),
                                    'isFamilyFriendly': item.get('isFamilyFriendly', False)
                                },
                                discovered_at=datetime.now()
                            )
                            results.append(results)
                    
                    logger.info(f"✅ Bing search completed: {len(results)} results for '{query}'")
                    return results
                    
        except Exception as e:
            logger.error(f"❌ Bing search error: {e}")
            return []
    
    def _calculate_bing_relevance(self, item: Dict[str, Any], rank: int) -> float:
        """Calculate relevance score for Bing search result"""
        score = 0.0
        
        # Rank-based scoring (Bing ranks by relevance)
        if rank == 0:
            score += 0.4
        elif rank < 3:
            score += 0.3
        elif rank < 5:
            score += 0.2
        else:
            score += 0.1
        
        # Title quality
        title = item.get('name', '')
        if len(title) > 10 and len(title) < 100:
            score += 0.2
        
        # Description quality
        snippet = item.get('snippet', '')
        if len(snippet) > 20:
            score += 0.2
        
        # URL quality
        url = item.get('url', '')
        if not url.endswith(('.pdf', '.doc', '.txt')):
            score += 0.1
        
        # Domain quality
        domain = urlparse(url).netloc
        if domain and '.' in domain:
            score += 0.1
        
        return min(score, 1.0)
    
    def _determine_content_type(self, item: Dict[str, Any]) -> str:
        """Determine content type from Bing search result"""
        url = item.get('url', '').lower()
        title = item.get('name', '').lower()
        snippet = item.get('snippet', '').lower()
        
        # Documentation sites
        if any(term in url for term in ['docs', 'documentation', 'api', 'reference']):
            return 'documentation'
        
        # Blog sites
        if any(term in url for term in ['blog', 'post', 'article', 'news']):
            return 'blog'
        
        # Academic sites
        if any(term in url for term in ['edu', 'academic', 'research', 'paper', 'journal']):
            return 'academic'
        
        # Social media
        if any(term in url for term in ['twitter', 'facebook', 'linkedin', 'reddit']):
            return 'social'
        
        # News sites
        if any(term in title or term in snippet for term in ['news', 'breaking', 'latest']):
            return 'news'
        
        return 'general'

class SearchEngineIntegration:
    """Main search engine integration orchestrator"""
    
    def __init__(self, db_path: str, config: SearchEngineConfig = None):
        self.db_path = db_path
        self.config = config or SearchEngineConfig()
        self.google_search = None
        self.bing_search = None
        
        # Initialize search engines
        self._init_search_engines()
        
        # Initialize database
        self._init_search_database()
        
        # Search metrics
        self.search_metrics = {
            'total_searches': 0,
            'google_searches': 0,
            'bing_searches': 0,
            'total_results': 0,
            'average_relevance': 0.0,
            'duplicate_filtered': 0
        }
    
    def _init_search_engines(self):
        """Initialize search engine APIs"""
        # Check Google Custom Search API
        if self.config.enable_google_search and self.config.google_custom_search_api_key:
            if len(self.config.google_custom_search_api_key) > 20:  # Basic validation
                self.google_search = GoogleCustomSearchAPI(
                    self.config.google_custom_search_api_key,
                    self.config.google_custom_search_engine_id
                )
                logger.info("✅ Google Custom Search API initialized successfully")
                logger.info(f"   API Key: {self.config.google_custom_search_api_key[:10]}...")
                logger.info(f"   Engine ID: {self.config.google_custom_search_engine_id}")
            else:
                logger.warning("⚠️ Google API key appears to be invalid (too short)")
        else:
            logger.warning("⚠️ Google Custom Search API not configured")
        
        # Check Bing Web Search API
        if self.config.enable_bing_search and self.config.bing_search_api_key:
            if len(self.config.bing_search_api_key) > 20:  # Basic validation
                self.bing_search = BingWebSearchAPI(self.config.bing_search_api_key)
                logger.info("✅ Bing Web Search API initialized successfully")
                logger.info(f"   API Key: {self.config.bing_search_api_key[:10]}...")
            else:
                logger.warning("⚠️ Bing API key appears to be invalid (too short)")
        else:
            logger.warning("⚠️ Bing Web Search API not configured")
        
        # Summary of available engines
        available_engines = []
        if self.google_search:
            available_engines.append("Google")
        if self.bing_search:
            available_engines.append("Bing")
        
        if available_engines:
            logger.info(f"🚀 Search engines available: {', '.join(available_engines)}")
        else:
            logger.warning("⚠️ No search engines configured - using fallback methods only")
            logger.info("💡 To enable search engines, set the appropriate API keys in environment variables")
            logger.info("   GOOGLE_CUSTOM_SEARCH_API_KEY and GOOGLE_CUSTOM_SEARCH_ENGINE_ID")
            logger.info("   BING_SEARCH_API_KEY")
    
    def _init_search_database(self):
        """Initialize search database tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create search results table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS search_results (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        result_id TEXT UNIQUE,
                        title TEXT,
                        url TEXT UNIQUE,
                        description TEXT,
                        source_engine TEXT,
                        relevance_score REAL,
                        content_type TEXT,
                        domain TEXT,
                        search_query TEXT,
                        result_rank INTEGER,
                        metadata TEXT,
                        discovered_at TIMESTAMP,
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
                        search_engines TEXT,
                        created_at TIMESTAMP,
                        status TEXT
                    )
                """)
                
                # Create search engine metrics table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS search_engine_metrics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        engine_name TEXT,
                        searches_performed INTEGER,
                        results_found INTEGER,
                        average_relevance REAL,
                        rate_limit_remaining INTEGER,
                        last_used TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create indices for performance
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_search_results_url ON search_results (url)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_search_results_query ON search_results (search_query)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_search_results_relevance ON search_results (relevance_score)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_search_results_engine ON search_results (source_engine)")
                
                conn.commit()
                logger.info("✅ Search database initialized successfully")
                
        except Exception as e:
            logger.error(f"❌ Failed to initialize search database: {e}")
            raise
    
    async def perform_multi_engine_search(self, query: str, max_results: int = None, 
                                        engines: List[str] = None) -> List[SearchResult]:
        """Perform search across multiple search engines"""
        try:
            max_results = max_results or self.config.max_results_per_query
            engines = engines or ['google', 'bing']
            
            logger.info(f"🔍 Performing multi-engine search: '{query}' (max: {max_results})")
            
            all_results = []
            
            # Google search
            if 'google' in engines and self.google_search:
                logger.info("🔍 Searching Google...")
                google_results = await self.google_search.search(query, max_results)
                all_results.extend(google_results)
                self.search_metrics['google_searches'] += 1
            
            # Bing search
            if 'bing' in engines and self.bing_search:
                logger.info("🔍 Searching Bing...")
                bing_results = await self.bing_search.search(query, max_results)
                all_results.extend(bing_results)
                self.search_metrics['bing_searches'] += 1
            
            # Update metrics
            self.search_metrics['total_searches'] += 1
            self.search_metrics['total_results'] += len(all_results)
            
            # Filter and deduplicate results
            if self.config.enable_duplicate_filtering:
                filtered_results = self._filter_duplicate_results(all_results)
                self.search_metrics['duplicate_filtered'] += len(all_results) - len(filtered_results)
                all_results = filtered_results
            
            # Score and rank results
            if self.config.enable_relevance_scoring:
                all_results = self._enhance_relevance_scoring(all_results)
            
            # Sort by relevance
            all_results.sort(key=lambda x: x.relevance_score, reverse=True)
            
            # Limit results
            final_results = all_results[:max_results]
            
            # Store results in database
            await self._store_search_results(final_results)
            
            # Update average relevance
            if final_results:
                self.search_metrics['average_relevance'] = (
                    (self.search_metrics['average_relevance'] * 
                     (self.search_metrics['total_searches'] - 1) + 
                     sum(r.relevance_score for r in final_results) / len(final_results)) / 
                    self.search_metrics['total_searches']
                )
            
            logger.info(f"✅ Multi-engine search completed: {len(final_results)} results")
            return final_results
            
        except Exception as e:
            logger.error(f"❌ Multi-engine search failed: {e}")
            return []
    
    def _filter_duplicate_results(self, results: List[SearchResult]) -> List[SearchResult]:
        """Filter out duplicate results based on URL and content similarity"""
        seen_urls = set()
        filtered_results = []
        
        for result in results:
            # Normalize URL
            normalized_url = self._normalize_url(result.url)
            
            if normalized_url not in seen_urls:
                seen_urls.add(normalized_url)
                filtered_results.append(result)
        
        return filtered_results
    
    def _normalize_url(self, url: str) -> str:
        """Normalize URL for duplicate detection"""
        parsed = urlparse(url)
        
        # Remove common tracking parameters
        query_params = parse_qs(parsed.query)
        filtered_params = {k: v for k, v in query_params.items() 
                          if k not in ['utm_source', 'utm_medium', 'utm_campaign', 'ref']}
        
        # Rebuild URL without tracking parameters
        clean_query = '&'.join([f"{k}={v[0]}" for k, v in filtered_params.items()])
        
        return urlunparse((
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            clean_query,
            parsed.fragment
        ))
    
    def _enhance_relevance_scoring(self, results: List[SearchResult]) -> List[SearchResult]:
        """Enhance relevance scoring based on multiple factors"""
        for result in results:
            # Base score from search engine
            base_score = result.relevance_score
            
            # Content type bonus
            if result.content_type == 'documentation':
                base_score += 0.1
            elif result.content_type == 'academic':
                base_score += 0.1
            
            # Domain quality bonus
            domain = result.domain
            if domain.endswith('.edu'):
                base_score += 0.1
            elif domain.endswith('.org'):
                base_score += 0.05
            
            # Title quality bonus
            title = result.title
            if len(title) > 20 and len(title) < 80:
                base_score += 0.05
            
            # Cap at 1.0
            result.relevance_score = min(base_score, 1.0)
        
        return results
    
    async def _store_search_results(self, results: List[SearchResult]):
        """Store search results in database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                for result in results:
                    cursor.execute("""
                        INSERT OR REPLACE INTO search_results 
                        (result_id, title, url, description, source_engine, relevance_score,
                         content_type, domain, search_query, result_rank, metadata, discovered_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        result.result_id, result.title, result.url, result.description,
                        result.source_engine, result.relevance_score, result.content_type,
                        result.domain, result.search_query, result.result_rank,
                        json.dumps(result.metadata), result.discovered_at
                    ))
                
                conn.commit()
                
        except Exception as e:
            logger.error(f"❌ Failed to store search results: {e}")
    
    async def get_search_metrics(self) -> Dict[str, Any]:
        """Get search engine performance metrics"""
        return {
            'search_metrics': self.search_metrics,
            'engine_status': {
                'google': self.google_search is not None,
                'bing': self.bing_search is not None
            },
            'rate_limits': {
                'google_remaining': self.google_search.rate_limit_remaining if self.google_search else 0,
                'bing_remaining': self.bing_search.rate_limit_remaining if self.bing_search else 0
            }
        }

# Example usage
async def main():
    """Test the search engine integration"""
    # Load configuration from environment or config file
    config = SearchEngineConfig(
        google_custom_search_api_key=os.getenv('GOOGLE_CUSTOM_SEARCH_API_KEY', ''),
        google_custom_search_engine_id=os.getenv('GOOGLE_CUSTOM_SEARCH_ENGINE_ID', ''),
        bing_search_api_key=os.getenv('BING_SEARCH_API_KEY', '')
    )
    
    integration = SearchEngineIntegration('brain_memory_store/brain.db', config)
    
    # Perform search
    results = await integration.perform_multi_engine_search(
        query="Model Context Protocol MCP documentation",
        max_results=20
    )
    
    print(f"Search completed: {len(results)} results")
    
    # Show top results
    for i, result in enumerate(results[:5]):
        print(f"{i+1}. {result.title}")
        print(f"   URL: {result.url}")
        print(f"   Relevance: {result.relevance_score:.2f}")
        print(f"   Engine: {result.source_engine}")

if __name__ == "__main__":
    asyncio.run(main())
