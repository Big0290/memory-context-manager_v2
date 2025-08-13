#!/usr/bin/env python3
"""
Web Crawler Engine - Comprehensive web content ingestion for Memory Context Manager v2
Fetches, parses, categorizes, and stores web content as structured learning bits
"""

import asyncio
import aiohttp
import hashlib
import json
import logging
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Set, Tuple, Union
from urllib.parse import urljoin, urlparse, urlunparse
from dataclasses import dataclass, asdict
import sqlite3
from bs4 import BeautifulSoup
import trafilatura
from trafilatura.settings import use_config

logger = logging.getLogger(__name__)

@dataclass
class CrawlConfig:
    """Configuration for web crawling operations"""
    max_depth: int = 3
    max_pages_per_domain: int = 100
    crawl_delay: float = 1.0
    timeout: int = 30
    max_retries: int = 3
    user_agent: str = "Memory-Context-Manager-v2/1.0 (Educational Research Bot)"
    respect_robots_txt: bool = True
    follow_links: bool = True
    extract_images: bool = False
    extract_code: bool = True
    extract_tables: bool = True
    min_content_length: int = 100
    max_content_length: int = 50000

@dataclass
class LearningBit:
    """A structured learning unit extracted from web content"""
    content_hash: str
    content_type: str  # 'concept', 'example', 'definition', 'procedure', 'warning', 'tip'
    category: str  # 'programming', 'api', 'tutorial', 'reference', 'best_practice'
    subcategory: str  # 'python', 'javascript', 'web_development', 'database'
    content: str
    context: str
    importance_score: float
    confidence_score: float
    source_url: str
    tags: List[str]
    complexity_level: str
    language: str = 'en'

@dataclass
class CrawledPage:
    """Information about a crawled web page"""
    url: str
    title: str
    content: str
    html_content: str
    status_code: int
    response_time_ms: int
    crawl_depth: int
    parent_url: Optional[str]
    domain: str
    path: str
    metadata: Dict[str, Any]

class ContentAnalyzer:
    """Analyzes and categorizes web content for learning extraction"""
    
    def __init__(self):
        # Content type detection patterns
        self.content_patterns = {
            'concept': [
                r'\b(?:concept|idea|principle|theory|approach|methodology)\b',
                r'\b(?:what is|definition of|meaning of)\b',
                r'\b(?:introduction to|overview of|basics of)\b',
                r'\b(?:understanding|learning about|exploring)\b',
                r'\b(?:fundamental|essential|core|basic)\b',
                r'\b(?:key concept|main idea|central principle)\b'
            ],
            'example': [
                r'\b(?:example|sample|instance|case|demonstration)\b',
                r'\b(?:for example|e\.g\.|such as|like)\b',
                r'```[\s\S]*?```',  # Code blocks
                r'<code>[\s\S]*?</code>',
                r'\b(?:here\'s how|this shows|demonstrates)\b',
                r'\b(?:sample code|code example|working example)\b',
                r'\b(?:practical example|real-world example)\b'
            ],
            'definition': [
                r'\b(?:define|definition|means|refers to|is a)\b',
                r'\b(?:consists of|composed of|made up of)\b',
                r'\b(?:characterized by|distinguished by)\b',
                r'\b(?:describes|explains|clarifies)\b',
                r'\b(?:represents|signifies|denotes)\b',
                r'\b(?:type of|kind of|form of)\b'
            ],
            'procedure': [
                r'\b(?:step|procedure|process|method|algorithm)\b',
                r'\b(?:how to|steps to|procedure for)\b',
                r'\b(?:first|second|third|next|finally)\b',
                r'\b(?:1\.|2\.|3\.|step \d+)\b',
                r'\b(?:follow these|complete these|execute)\b',
                r'\b(?:workflow|sequence|order of operations)\b',
                r'\b(?:installation|setup|configuration)\b'
            ],
            'warning': [
                r'\b(?:warning|caution|danger|important|note)\b',
                r'\b(?:be careful|avoid|don\'t|never)\b',
                r'⚠️|🚨|💡|📝|❗',
                r'\b(?:critical|essential|must|should)\b',
                r'\b(?:limitation|restriction|constraint)\b',
                r'\b(?:deprecated|obsolete|legacy)\b'
            ],
            'tip': [
                r'\b(?:tip|hint|suggestion|recommendation|best practice)\b',
                r'\b(?:pro tip|expert tip|useful tip)\b',
                r'💡|💭|✨|🎯',
                r'\b(?:advice|guidance|insight)\b',
                r'\b(?:optimization|improvement|enhancement)\b',
                r'\b(?:trick|shortcut|efficiency)\b'
            ],
            'reference': [
                r'\b(?:reference|documentation|manual|specification)\b',
                r'\b(?:syntax|parameters|return|examples)\b',
                r'\b(?:table|list|index|glossary)\b',
                r'\b(?:see|check|look at|refer to)\b',
                r'\b(?:api reference|function reference|class reference)\b',
                r'\b(?:properties|methods|attributes|events)\b'
            ],
            'tutorial': [
                r'\b(?:tutorial|guide|how-to|walkthrough|lesson)\b',
                r'\b(?:learn|teaching|instruction|step-by-step)\b',
                r'\b(?:beginner|intermediate|advanced|expert)\b',
                r'\b(?:getting started|setup|installation)\b',
                r'\b(?:hands-on|practical|exercise)\b',
                r'\b(?:course|curriculum|syllabus)\b'
            ],
            'comparison': [
                r'\b(?:compare|comparison|difference|versus|vs)\b',
                r'\b(?:similar to|different from|unlike)\b',
                r'\b(?:advantages|disadvantages|pros|cons)\b',
                r'\b(?:better than|worse than|same as)\b',
                r'\b(?:trade-off|tradeoff|balance)\b'
            ],
            'troubleshooting': [
                r'\b(?:troubleshoot|troubleshooting|problem|issue|error)\b',
                r'\b(?:fix|solution|resolve|debug)\b',
                r'\b(?:common problems|frequently asked|faq)\b',
                r'\b(?:error message|exception|crash)\b',
                r'\b(?:diagnose|identify|locate)\b'
            ]
        }
        
        # Category detection patterns
        self.category_patterns = {
            'programming': [
                r'\b(?:code|programming|development|software|coding)\b',
                r'\b(?:function|class|method|variable|algorithm)\b',
                r'\b(?:python|javascript|java|c\+\+|go|rust)\b',
                r'```[\s\S]*?```',  # Code blocks
                r'<code>[\s\S]*?</code>'
            ],
            'api': [
                r'\b(?:api|endpoint|request|response|http)\b',
                r'\b(?:rest|graphql|soap|websocket)\b',
                r'\b(?:authentication|authorization|token)\b',
                r'\b(?:get|post|put|delete|patch)\b'
            ],
            'tutorial': [
                r'\b(?:tutorial|guide|how-to|walkthrough|lesson)\b',
                r'\b(?:learn|teaching|instruction|step-by-step)\b',
                r'\b(?:beginner|intermediate|advanced|expert)\b'
            ],
            'reference': [
                r'\b(?:reference|documentation|manual|specification)\b',
                r'\b(?:syntax|parameters|return|examples)\b',
                r'\b(?:table|list|index|glossary)\b'
            ],
            'best_practice': [
                r'\b(?:best practice|recommendation|guideline)\b',
                r'\b(?:do\'s and don\'ts|tips and tricks)\b',
                r'\b(?:efficient|optimized|performance|security)\b'
            ]
        }
        
        # Subcategory detection patterns
        self.subcategory_patterns = {
            'python': [r'\bpython\b', r'\bpy\b', r'\.py\b', r'pip\b', r'pypi\b'],
            'javascript': [r'\bjavascript\b', r'\bjs\b', r'\.js\b', r'node\b', r'npm\b'],
            'web_development': [r'\bweb\b', r'\bhtml\b', r'\bcss\b', r'\bfrontend\b', r'\bbackend\b'],
            'database': [r'\bdatabase\b', r'\bsql\b', r'\bmysql\b', r'\bpostgresql\b', r'\bmongodb\b'],
            'devops': [r'\bdevops\b', r'\bci/cd\b', r'\bdocker\b', r'\bkubernetes\b', r'\bterraform\b'],
            'machine_learning': [r'\bml\b', r'\bai\b', r'\bartificial intelligence\b', r'\bneural network\b'],
            'cybersecurity': [r'\bsecurity\b', r'\bcybersecurity\b', r'\bencryption\b', r'\bauthentication\b']
        }
        
        # Complexity detection patterns
        self.complexity_patterns = {
            'beginner': [
                r'\b(?:beginner|basic|simple|easy|introductory)\b',
                r'\b(?:first time|new to|getting started)\b',
                r'\b(?:fundamental|essential|core)\b'
            ],
            'intermediate': [
                r'\b(?:intermediate|moderate|medium|standard)\b',
                r'\b(?:advanced beginner|some experience)\b',
                r'\b(?:practical|hands-on|real-world)\b'
            ],
            'advanced': [
                r'\b(?:advanced|expert|professional|senior)\b',
                r'\b(?:complex|sophisticated|optimization)\b',
                r'\b(?:enterprise|production|scalable)\b'
            ]
        }

    def analyze_content(self, content: str, url: str) -> Dict[str, Any]:
        """Analyze content and return categorization results"""
        content_lower = content.lower()
        url_lower = url.lower()
        
        # Detect content types
        detected_types = []
        for content_type, patterns in self.content_patterns.items():
            for pattern in patterns:
                if re.search(pattern, content_lower, re.IGNORECASE):
                    detected_types.append(content_type)
                    break
        
        # Detect categories
        detected_categories = []
        for category, patterns in self.category_patterns.items():
            for pattern in patterns:
                if re.search(pattern, content_lower, re.IGNORECASE):
                    detected_categories.append(category)
                    break
        
        # Detect subcategories
        detected_subcategories = []
        for subcategory, patterns in self.subcategory_patterns.items():
            for pattern in patterns:
                if re.search(pattern, content_lower, re.IGNORECASE) or re.search(pattern, url_lower, re.IGNORECASE):
                    detected_subcategories.append(subcategory)
                    break
        
        # Detect complexity
        complexity = 'moderate'  # default
        for comp_level, patterns in self.complexity_patterns.items():
            for pattern in patterns:
                if re.search(pattern, content_lower, re.IGNORECASE):
                    complexity = comp_level
                    break
        
        # Calculate importance score based on content characteristics
        importance_score = self._calculate_importance(content, detected_types, detected_categories)
        
        # Calculate confidence score based on pattern matches
        confidence_score = self._calculate_confidence(detected_types, detected_categories, detected_subcategories)
        
        return {
            'content_types': detected_types,
            'categories': detected_categories,
            'subcategories': detected_subcategories,
            'complexity': complexity,
            'importance_score': importance_score,
            'confidence_score': confidence_score
        }
    
    def _calculate_importance(self, content: str, content_types: List[str], categories: List[str]) -> float:
        """Calculate importance score based on content characteristics"""
        score = 0.5  # base score
        
        # Content length factor
        if len(content) > 1000:
            score += 0.1
        if len(content) > 5000:
            score += 0.1
        
        # Content type factor
        if 'concept' in content_types:
            score += 0.15
        if 'definition' in content_types:
            score += 0.1
        if 'example' in content_types:
            score += 0.05
        
        # Category factor
        if 'programming' in categories:
            score += 0.1
        if 'api' in categories:
            score += 0.1
        if 'best_practice' in categories:
            score += 0.15
        
        return min(1.0, score)
    
    def _calculate_confidence(self, content_types: List[str], categories: List[str], subcategories: List[str]) -> float:
        """Calculate confidence score based on pattern matches"""
        score = 0.5  # base score
        
        # More specific patterns increase confidence
        if len(content_types) > 0:
            score += 0.2
        if len(categories) > 0:
            score += 0.2
        if len(subcategories) > 0:
            score += 0.1
        
        return min(1.0, score)

class IntelligentLearningProcessor:
    """Intelligent processor that adapts learning extraction based on content patterns"""
    
    def __init__(self):
        self.learning_patterns = {}  # Track successful patterns
        self.content_quality_metrics = {}  # Track content quality
        self.adaptive_thresholds = {
            'min_chunk_length': 30,
            'max_chunk_length': 1000,
            'importance_boost_threshold': 0.7,
            'confidence_boost_threshold': 0.8
        }
        self.learning_history = []  # Track learning evolution
    
    def adapt_extraction_strategy(self, content: str, url: str, previous_results: List[LearningBit]) -> Dict[str, Any]:
        """Adapt extraction strategy based on content analysis and previous results"""
        strategy = {
            'chunk_size': 'adaptive',
            'content_focus': 'balanced',
            'quality_threshold': 'standard',
            'extraction_method': 'pattern_based'
        }
        
        # Analyze content characteristics
        content_length = len(content)
        content_complexity = self._analyze_content_complexity(content)
        
        # Adjust strategy based on content characteristics
        if content_length > 10000:
            strategy['chunk_size'] = 'large'
            strategy['content_focus'] = 'comprehensive'
        elif content_length < 2000:
            strategy['chunk_size'] = 'small'
            strategy['content_focus'] = 'focused'
        
        if content_complexity > 0.8:
            strategy['quality_threshold'] = 'high'
            strategy['extraction_method'] = 'semantic_based'
        
        # Learn from previous results
        if previous_results:
            avg_importance = sum(bit.importance_score for bit in previous_results) / len(previous_results)
            if avg_importance < 0.5:
                strategy['quality_threshold'] = 'strict'
                strategy['extraction_method'] = 'quality_focused'
        
        return strategy
    
    def _analyze_content_complexity(self, content: str) -> float:
        """Analyze content complexity based on various factors"""
        complexity_score = 0.0
        
        # Factor 1: Technical terms
        technical_terms = ['api', 'function', 'class', 'method', 'algorithm', 'protocol', 'interface']
        tech_count = sum(1 for term in technical_terms if term.lower() in content.lower())
        complexity_score += min(tech_count / 10.0, 0.3)
        
        # Factor 2: Code blocks
        code_blocks = content.count('```') / 2
        complexity_score += min(code_blocks / 5.0, 0.2)
        
        # Factor 3: Structured content
        structured_indicators = ['•', '-', '*', '1.', '2.', '3.', '|', '---']
        structure_count = sum(content.count(indicator) for indicator in structured_indicators)
        complexity_score += min(structure_count / 50.0, 0.2)
        
        # Factor 4: Content density
        words = content.split()
        if words:
            avg_word_length = sum(len(word) for word in words) / len(words)
            complexity_score += min(avg_word_length / 10.0, 0.3)
        
        return min(complexity_score, 1.0)
    
    def update_learning_patterns(self, successful_bits: List[LearningBit], failed_attempts: List[str]):
        """Update learning patterns based on successful and failed extractions"""
        for bit in successful_bits:
            pattern_key = f"{bit.content_type}_{bit.category}"
            if pattern_key not in self.learning_patterns:
                self.learning_patterns[pattern_key] = {
                    'success_count': 0,
                    'avg_importance': 0.0,
                    'avg_confidence': 0.0,
                    'content_lengths': []
                }
            
            pattern = self.learning_patterns[pattern_key]
            pattern['success_count'] += 1
            pattern['avg_importance'] = (pattern['avg_importance'] * (pattern['success_count'] - 1) + bit.importance_score) / pattern['success_count']
            pattern['avg_confidence'] = (pattern['avg_confidence'] * (pattern['success_count'] - 1) + bit.confidence_score) / pattern['success_count']
            pattern['content_lengths'].append(len(bit.content))
    
    def get_optimized_extraction_params(self, content_type: str, category: str) -> Dict[str, Any]:
        """Get optimized extraction parameters based on learned patterns"""
        pattern_key = f"{content_type}_{category}"
        if pattern_key in self.learning_patterns:
            pattern = self.learning_patterns[pattern_key]
            return {
                'min_chunk_length': max(20, int(sum(pattern['content_lengths']) / len(pattern['content_lengths']) * 0.3)),
                'importance_threshold': pattern['avg_importance'] * 0.8,
                'confidence_threshold': pattern['avg_confidence'] * 0.8
            }
        
        return self.adaptive_thresholds

class WebCrawler:
    """Main web crawler class for fetching and processing web content"""
    
    def __init__(self, db_path: str):
        """Initialize the web crawler"""
        self.db_path = db_path
        self.config = CrawlConfig()
        self.content_analyzer = ContentAnalyzer()
        self.intelligent_processor = IntelligentLearningProcessor()
        self.session = None
        self.crawl_queue = []
        self.crawled_urls = set()
        self.url_depths = {}
        self.url_priorities = {}
        self.domain_delays = {}
        
        # Initialize database
        self._init_database()
        
        # Learning evolution tracking
        self.learning_evolution = {
            'total_extractions': 0,
            'successful_extractions': 0,
            'failed_extractions': 0,
            'quality_improvements': 0,
            'pattern_discoveries': 0
        }
    
    def _init_database(self):
        """Initialize the web crawler database tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Read and execute the schema
                schema_path = Path(__file__).parent / 'database' / 'web_crawler_schema.sql'
                if schema_path.exists():
                    with open(schema_path, 'r') as f:
                        schema_sql = f.read()
                        conn.executescript(schema_sql)
                        conn.commit()
                        logger.info("✅ Web crawler database schema initialized")
                else:
                    logger.warning("⚠️ Schema file not found, creating basic tables")
                    self._create_basic_tables(conn)
        except Exception as e:
            logger.error(f"❌ Database initialization failed: {e}")
            raise
    
    def _create_basic_tables(self, conn: sqlite3.Connection):
        """Create basic tables if schema file is not available"""
        basic_tables = [
            """CREATE TABLE IF NOT EXISTS crawled_pages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE NOT NULL,
                title TEXT,
                content TEXT NOT NULL,
                html_content TEXT,
                status_code INTEGER,
                response_time_ms INTEGER,
                last_crawled TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                crawl_depth INTEGER DEFAULT 0,
                parent_url TEXT,
                domain TEXT,
                path TEXT,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",
            """CREATE TABLE IF NOT EXISTS learning_bits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                page_id INTEGER,
                content_hash TEXT UNIQUE NOT NULL,
                content_type TEXT NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT,
                content TEXT NOT NULL,
                context TEXT,
                importance_score REAL DEFAULT 0.5,
                confidence_score REAL DEFAULT 0.8,
                source_url TEXT,
                tags TEXT,
                complexity_level TEXT DEFAULT 'moderate',
                language TEXT DEFAULT 'en',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (page_id) REFERENCES crawled_pages(id)
            )"""
        ]
        
        for table_sql in basic_tables:
            conn.execute(table_sql)
        conn.commit()
    
    async def start_session(self):
        """Start the aiohttp session"""
        if self.session is None:
            timeout = aiohttp.ClientTimeout(total=self.config.timeout)
            self.session = aiohttp.ClientSession(
                timeout=timeout,
                headers={'User-Agent': self.config.user_agent}
            )
            logger.info("🚀 Web crawler session started")
    
    async def stop_session(self):
        """Stop the aiohttp session"""
        if self.session:
            await self.session.close()
            self.session = None
            logger.info("🛑 Web crawler session stopped")
    
    async def crawl_url(self, url: str, depth: int = 0, parent_url: Optional[str] = None) -> Optional[CrawledPage]:
        """Crawl a single URL and extract content"""
        if url in self.crawled_urls:
            return None
        
        try:
            start_time = time.time()
            
            # Respect robots.txt and domain delays
            domain = urlparse(url).netloc
            if not await self._can_crawl_domain(domain, url):
                logger.info(f"⏭️ Skipping {url} (robots.txt or delay)")
                return None
            
            # Fetch the page
            async with self.session.get(url) as response:
                response_time = int((time.time() - start_time) * 1000)
                
                if response.status != 200:
                    logger.warning(f"⚠️ HTTP {response.status} for {url}")
                    return None
                
                # Get content
                html_content = await response.text()
                
                # Extract clean text content
                content = self._extract_text_content(html_content)
                
                if len(content) < self.config.min_content_length:
                    logger.info(f"📝 Content too short for {url} ({len(content)} chars)")
                    return None
                
                # Parse title
                title = self._extract_title(html_content)
                
                # Store in database
                page_id = await self._store_crawled_page(
                    url, title, content, html_content, response.status, 
                    response_time, depth, parent_url, domain
                )
                
                # Extract learning bits
                learning_bits = await self._extract_learning_bits(content, url, page_id)
                
                # Store learning bits
                for bit in learning_bits:
                    await self._store_learning_bit(bit, page_id)
                
                # Mark as crawled
                self.crawled_urls.add(url)
                
                # Update domain delay
                self.domain_delays[domain] = time.time()
                
                logger.info(f"✅ Crawled {url} -> {len(learning_bits)} learning bits")
                
                return CrawledPage(
                    url=url,
                    title=title,
                    content=content,
                    html_content=html_content,
                    status_code=response.status,
                    response_time_ms=response_time,
                    crawl_depth=depth,
                    parent_url=parent_url,
                    domain=domain,
                    path=urlparse(url).path,
                    metadata={'headers': dict(response.headers)}
                )
                
        except Exception as e:
            logger.error(f"❌ Error crawling {url}: {e}")
            return None
    
    def _extract_text_content(self, html_content: str) -> str:
        """Extract clean text content from HTML"""
        try:
            # Use trafilatura for better text extraction
            extracted_text = trafilatura.extract(html_content)
            if extracted_text:
                return extracted_text.strip()
            
            # Fallback to BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text
            
        except Exception as e:
            logger.warning(f"⚠️ Text extraction failed: {e}")
            # Fallback to BeautifulSoup only
            try:
                soup = BeautifulSoup(html_content, 'html.parser')
                
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()
                
                # Get text
                text = soup.get_text()
                
                # Clean up whitespace
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = ' '.join(chunk for chunk in chunks if chunk)
                
                return text
            except Exception as fallback_error:
                logger.error(f"❌ Fallback text extraction also failed: {fallback_error}")
                return ""
    
    def _extract_title(self, html_content: str) -> str:
        """Extract page title from HTML"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            title_tag = soup.find('title')
            if title_tag:
                return title_tag.get_text().strip()
            
            # Fallback to h1
            h1_tag = soup.find('h1')
            if h1_tag:
                return h1_tag.get_text().strip()
            
            return "Untitled"
            
        except Exception:
            return "Untitled"
    
    async def _can_crawl_domain(self, domain: str, url: str) -> bool:
        """Check if we can crawl a domain based on robots.txt and delays"""
        if not self.config.respect_robots_txt:
            return True
        
        # Check domain delay
        if domain in self.domain_delays:
            time_since_last = time.time() - self.domain_delays[domain]
            if time_since_last < self.config.crawl_delay:
                return False
        
        # TODO: Implement robots.txt checking
        # For now, just respect delays
        return True
    
    async def _store_crawled_page(self, url: str, title: str, content: str, 
                                 html_content: str, status_code: int, 
                                 response_time: int, depth: int, 
                                 parent_url: Optional[str], domain: str) -> int:
        """Store crawled page in database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if page already exists
                cursor.execute(
                    "SELECT id FROM crawled_pages WHERE url = ?",
                    (url,)
                )
                existing = cursor.fetchone()
                
                if existing:
                    # Update existing page
                    cursor.execute("""
                        UPDATE crawled_pages 
                        SET title = ?, content = ?, html_content = ?, 
                            status_code = ?, response_time_ms = ?, 
                            last_crawled = CURRENT_TIMESTAMP, crawl_depth = ?,
                            parent_url = ?, domain = ?, path = ?, metadata = ?
                        WHERE url = ?
                    """, (title, content, html_content, status_code, response_time,
                          depth, parent_url, domain, urlparse(url).path,
                          json.dumps({'headers': {}}), url))
                    return existing[0]
                else:
                    # Insert new page
                    cursor.execute("""
                        INSERT INTO crawled_pages 
                        (url, title, content, html_content, status_code, 
                         response_time_ms, crawl_depth, parent_url, domain, path, metadata)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (url, title, content, html_content, status_code,
                          response_time, depth, parent_url, domain, urlparse(url).path,
                          json.dumps({'headers': {}})))
                    
                    return cursor.lastrowid
                    
        except Exception as e:
            logger.error(f"❌ Failed to store crawled page: {e}")
            raise
    
    async def _get_page_id_from_url(self, url: str) -> int:
        """Get the page ID from the database using the URL"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM crawled_pages WHERE url = ?", (url,))
                result = cursor.fetchone()
                if result:
                    return result[0]
                else:
                    logger.warning(f"⚠️ Page ID not found for URL: {url}")
                    return 0
        except Exception as e:
            logger.error(f"❌ Failed to get page ID for {url}: {e}")
            return 0
    
    async def _extract_learning_bits(self, content: str, url: str, page_id: int) -> List[LearningBit]:
        """Extract learning bits from content with intelligent adaptive processing"""
        learning_bits = []
        failed_attempts = []
        
        # Get previous learning results for this domain to adapt strategy
        previous_results = await self._get_previous_learning_bits_for_domain(url)
        
        # Get adaptive extraction strategy
        strategy = self.intelligent_processor.adapt_extraction_strategy(content, url, previous_results)
        
        # Split content into chunks based on strategy
        chunks = self._split_content_into_chunks_adaptive(content, strategy)
        
        for chunk in chunks:
            try:
                # Apply adaptive chunk filtering
                if not self._meets_adaptive_criteria(chunk, strategy):
                    continue
                
                # Analyze chunk with enhanced analysis
                analysis = self.content_analyzer.analyze_content(chunk, url)
                
                # Apply intelligent filtering based on learned patterns
                if not self._passes_intelligent_filtering(chunk, analysis, strategy):
                    failed_attempts.append(f"Filtered out: {chunk[:50]}...")
                    continue
                
                # Create learning bit with enhanced processing
                learning_bit = await self._create_enhanced_learning_bit(chunk, analysis, url, page_id)
                
                if learning_bit:
                    learning_bits.append(learning_bit)
                    self.learning_evolution['successful_extractions'] += 1
                else:
                    failed_attempts.append(f"Failed to create: {chunk[:50]}...")
                    self.learning_evolution['failed_extractions'] += 1
                
            except Exception as e:
                failed_attempts.append(f"Error processing: {str(e)}")
                self.learning_evolution['failed_extractions'] += 1
                logger.warning(f"⚠️ Error processing chunk: {e}")
        
        # Update learning patterns and evolution
        if learning_bits:
            self.intelligent_processor.update_learning_patterns(learning_bits, failed_attempts)
            self._update_learning_evolution(learning_bits, failed_attempts)
        
        self.learning_evolution['total_extractions'] += len(chunks)
        
        logger.info(f"🧠 Intelligent extraction: {len(learning_bits)} learning bits from {len(chunks)} chunks")
        if failed_attempts:
            logger.debug(f"📝 Failed attempts: {len(failed_attempts)}")
        
        return learning_bits
    
    def _split_content_into_chunks_adaptive(self, content: str, strategy: Dict[str, Any]) -> List[str]:
        """Split content into chunks using adaptive strategy"""
        if strategy['chunk_size'] == 'large':
            # Larger chunks for comprehensive content
            chunks = re.split(r'\n\s*\n\s*\n', content)  # Triple newlines
        elif strategy['chunk_size'] == 'small':
            # Smaller chunks for focused content
            chunks = re.split(r'[.!?]\s+', content)  # Sentence-based
        else:
            # Adaptive chunking
            chunks = self._split_content_into_chunks(content)
        
        # Apply strategy-based filtering
        filtered_chunks = []
        for chunk in chunks:
            chunk = chunk.strip()
            if len(chunk) >= strategy.get('min_chunk_length', 30):
                if strategy['content_focus'] == 'comprehensive' or len(chunk) <= strategy.get('max_chunk_length', 1000):
                    filtered_chunks.append(chunk)
        
        return filtered_chunks
    
    def _meets_adaptive_criteria(self, chunk: str, strategy: Dict[str, Any]) -> bool:
        """Check if chunk meets adaptive criteria"""
        # Basic length check
        if len(chunk.strip()) < strategy.get('min_chunk_length', 30):
            return False
        
        # Quality threshold check
        if strategy['quality_threshold'] == 'strict':
            # More stringent quality checks
            if len(chunk.split()) < 10:  # Must have minimum words
                return False
            if chunk.count(' ') < 5:  # Must have proper spacing
                return False
        
        return True
    
    def _passes_intelligent_filtering(self, chunk: str, analysis: Dict[str, Any], strategy: Dict[str, Any]) -> bool:
        """Apply intelligent filtering based on learned patterns"""
        # Basic category requirement
        if not analysis['categories']:
            return False
        
        # Get optimized parameters for this content type/category
        if analysis['content_types'] and analysis['categories']:
            content_type = analysis['content_types'][0]
            category = analysis['categories'][0]
            optimized_params = self.intelligent_processor.get_optimized_extraction_params(content_type, category)
            
            # Apply learned thresholds
            if analysis['importance_score'] < optimized_params.get('importance_threshold', 0.3):
                return False
            if analysis['confidence_score'] < optimized_params.get('confidence_threshold', 0.4):
                return False
        
        return True
    
    async def _create_enhanced_learning_bit(self, chunk: str, analysis: Dict[str, Any], url: str, page_id: int) -> Optional[LearningBit]:
        """Create enhanced learning bit with intelligent processing"""
        try:
            content_hash = hashlib.md5(chunk.encode()).hexdigest()
            
            # Get surrounding context
            context = self._get_chunk_context([chunk], chunk)
            
            # Create enhanced tags
            tags = self._create_enhanced_tags(chunk, analysis, url)
            
            # Determine content type with enhanced inference
            content_type = self._infer_enhanced_content_type(chunk, analysis, url)
            
            # Calculate enhanced scores
            importance_score = self._calculate_enhanced_importance(chunk, analysis, url)
            confidence_score = self._calculate_enhanced_confidence(chunk, analysis)
            
            # Apply learning-based quality improvements
            if self._should_apply_quality_improvement(analysis):
                importance_score = min(1.0, importance_score * 1.1)
                confidence_score = min(1.0, confidence_score * 1.05)
                self.learning_evolution['quality_improvements'] += 1
            
            learning_bit = LearningBit(
                content_hash=content_hash,
                content_type=content_type,
                category=analysis['categories'][0] if analysis['categories'] else 'general',
                subcategory=analysis['subcategories'][0] if analysis['subcategories'] else None,
                content=chunk.strip(),
                context=context,
                importance_score=importance_score,
                confidence_score=confidence_score,
                source_url=url,
                tags=tags,
                complexity_level=analysis['complexity']
            )
            
            return learning_bit
            
        except Exception as e:
            logger.error(f"❌ Failed to create learning bit: {e}")
            return None
    
    def _create_enhanced_tags(self, chunk: str, analysis: Dict[str, Any], url: str) -> List[str]:
        """Create enhanced tags with intelligent analysis"""
        tags = []
        tags.extend(analysis['content_types'])
        tags.extend(analysis['categories'])
        tags.extend(analysis['subcategories'])
        
        # Add intelligent tags based on content analysis
        chunk_lower = chunk.lower()
        
        # Technical complexity tags
        if any(term in chunk_lower for term in ['api', 'endpoint', 'request']):
            tags.append('technical')
        if any(term in chunk_lower for term in ['tutorial', 'guide', 'how-to']):
            tags.append('educational')
        if any(term in chunk_lower for term in ['example', 'sample', 'demo']):
            tags.append('practical')
        
        # URL-based tags
        url_lower = url.lower()
        if '/api/' in url_lower:
            tags.append('api_documentation')
        if '/tutorial/' in url_lower:
            tags.append('tutorial_content')
        if '/reference/' in url_lower:
            tags.append('reference_material')
        
        return list(set(tags))  # Remove duplicates
    
    def _infer_enhanced_content_type(self, chunk: str, analysis: Dict[str, Any], url: str) -> str:
        """Enhanced content type inference with learning-based improvements"""
        # Use existing inference logic
        base_type = self._infer_content_type(chunk, analysis, url)
        
        # Apply learning-based improvements
        if base_type == 'concept' and 'api' in analysis['categories']:
            # API concepts are often better categorized as definitions
            return 'definition'
        elif base_type == 'concept' and 'tutorial' in analysis['categories']:
            # Tutorial concepts are often better categorized as procedures
            return 'procedure'
        
        return base_type
    
    def _should_apply_quality_improvement(self, analysis: Dict[str, Any]) -> bool:
        """Determine if quality improvement should be applied"""
        # Apply improvements to high-quality content
        if analysis['importance_score'] > 0.7 and analysis['confidence_score'] > 0.7:
            return True
        
        # Apply improvements to technical content
        if 'api' in analysis['categories'] or 'programming' in analysis['categories']:
            return True
        
        return False
    
    def _update_learning_evolution(self, learning_bits: List[LearningBit], failed_attempts: List[str]):
        """Update learning evolution metrics"""
        if learning_bits:
            # Check for new pattern discoveries
            new_patterns = set()
            for bit in learning_bits:
                pattern = f"{bit.content_type}_{bit.category}"
                if pattern not in self.intelligent_processor.learning_patterns:
                    new_patterns.add(pattern)
            
            if new_patterns:
                self.learning_evolution['pattern_discoveries'] += len(new_patterns)
                logger.info(f"🔍 Discovered {len(new_patterns)} new learning patterns: {', '.join(new_patterns)}")
    
    async def _get_previous_learning_bits_for_domain(self, url: str) -> List[LearningBit]:
        """Get previous learning bits from the same domain for adaptive learning"""
        try:
            domain = urlparse(url).netloc
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT lb.content_type, lb.category, lb.importance_score, lb.confidence_score
                    FROM learning_bits lb
                    JOIN crawled_pages cp ON lb.page_id = cp.id
                    WHERE cp.domain = ?
                    ORDER BY lb.created_at DESC
                    LIMIT 50
                """, (domain,))
                
                results = cursor.fetchall()
                # Convert to LearningBit objects for compatibility
                learning_bits = []
                for row in results:
                    # Create minimal LearningBit object for analysis
                    bit = type('LearningBit', (), {
                        'content_type': row[0],
                        'category': row[1],
                        'importance_score': row[2],
                        'confidence_score': row[3]
                    })()
                    learning_bits.append(bit)
                
                return learning_bits
                
        except Exception as e:
            logger.warning(f"⚠️ Could not retrieve previous learning bits: {e}")
            return []
    
    def _infer_content_type(self, chunk: str, analysis: Dict[str, Any], url: str) -> str:
        """Enhanced content type inference based on multiple factors"""
        chunk_lower = chunk.lower()
        url_lower = url.lower()
        
        # Check for specific patterns in the chunk
        if any(pattern in chunk_lower for pattern in ['```', '<code>', 'function', 'class', 'method']):
            return 'example'
        
        if any(pattern in chunk_lower for pattern in ['error', 'exception', 'problem', 'issue', 'fix']):
            return 'troubleshooting'
        
        if any(pattern in chunk_lower for pattern in ['vs', 'versus', 'difference', 'compare', 'similar']):
            return 'comparison'
        
        if any(pattern in chunk_lower for pattern in ['step', 'procedure', 'how to', 'follow']):
            return 'procedure'
        
        if any(pattern in chunk_lower for pattern in ['warning', 'caution', 'important', 'note']):
            return 'warning'
        
        if any(pattern in chunk_lower for pattern in ['tip', 'hint', 'recommendation', 'best practice']):
            return 'tip'
        
        # Check URL patterns
        if any(pattern in url_lower for pattern in ['/api/', '/reference/', '/docs/']):
            return 'reference'
        
        if any(pattern in url_lower for pattern in ['/tutorial/', '/guide/', '/how-to/']):
            return 'tutorial'
        
        if any(pattern in url_lower for pattern in ['/examples/', '/samples/']):
            return 'example'
        
        # Default based on categories
        if 'reference' in analysis['categories']:
            return 'reference'
        elif 'tutorial' in analysis['categories']:
            return 'tutorial'
        elif 'api' in analysis['categories']:
            return 'definition'
        elif 'best_practice' in analysis['categories']:
            return 'tip'
        
        return 'concept'
    
    def _calculate_enhanced_importance(self, chunk: str, analysis: Dict[str, Any], url: str) -> float:
        """Calculate enhanced importance score based on multiple factors"""
        base_score = analysis['importance_score']
        
        # Factor 1: Content length (longer content often more important)
        length_factor = min(len(chunk) / 500.0, 0.3)  # Max 0.3 boost
        
        # Factor 2: URL depth (deeper pages often more specific/important)
        url_depth = len([p for p in urlparse(url).path.split('/') if p])
        depth_factor = min(url_depth * 0.05, 0.2)  # Max 0.2 boost
        
        # Factor 3: Content type boost
        type_boost = 0.0
        if analysis['content_types']:
            content_type = analysis['content_types'][0]
            if content_type in ['definition', 'concept']:
                type_boost = 0.1  # Core concepts are important
            elif content_type in ['example', 'tutorial']:
                type_boost = 0.15  # Practical examples are very important
            elif content_type in ['warning', 'troubleshooting']:
                type_boost = 0.2  # Critical information
        
        # Factor 4: Category boost
        category_boost = 0.0
        if 'api' in analysis['categories']:
            category_boost = 0.1  # API docs are important
        if 'best_practice' in analysis['categories']:
            category_boost = 0.15  # Best practices are valuable
        
        # Calculate final score
        final_score = base_score + length_factor + depth_factor + type_boost + category_boost
        return min(1.0, max(0.1, final_score))
    
    def _calculate_enhanced_confidence(self, chunk: str, analysis: Dict[str, Any]) -> float:
        """Calculate enhanced confidence score based on content quality"""
        base_confidence = analysis['confidence_score']
        
        # Factor 1: Content clarity (shorter, focused content is clearer)
        clarity_factor = 0.0
        if 50 <= len(chunk) <= 300:  # Optimal length range
            clarity_factor = 0.1
        elif len(chunk) > 500:  # Very long content might be less clear
            clarity_factor = -0.05
        
        # Factor 2: Pattern match strength
        pattern_strength = 0.0
        if len(analysis['content_types']) > 0:
            pattern_strength = 0.1  # Strong pattern matches
        if len(analysis['categories']) > 1:
            pattern_strength += 0.05  # Multiple category matches
        
        # Factor 3: Content structure
        structure_factor = 0.0
        if any(char in chunk for char in ['•', '-', '*', '1.', '2.', '3.']):
            structure_factor = 0.05  # Structured content
        
        # Calculate final confidence
        final_confidence = base_confidence + clarity_factor + pattern_strength + structure_factor
        return min(1.0, max(0.1, final_confidence))

    def _split_content_into_chunks(self, content: str) -> List[str]:
        """Split content into meaningful chunks"""
        # Split by double newlines (paragraphs)
        chunks = re.split(r'\n\s*\n', content)
        
        # Further split very long chunks
        final_chunks = []
        for chunk in chunks:
            if len(chunk) > 1000:
                # Split by sentences for very long chunks
                sentences = re.split(r'[.!?]+', chunk)
                final_chunks.extend([s.strip() for s in sentences if len(s.strip()) > 50])
            else:
                final_chunks.append(chunk.strip())
        
        return [c for c in final_chunks if len(c.strip()) > 0]
    
    def _get_chunk_context(self, chunks: List[str], target_chunk: str) -> str:
        """Get surrounding context for a chunk"""
        try:
            chunk_index = chunks.index(target_chunk)
            
            # Get previous and next chunks
            context_chunks = []
            
            if chunk_index > 0:
                context_chunks.append(chunks[chunk_index - 1][:200] + "...")
            
            if chunk_index < len(chunks) - 1:
                context_chunks.append("..." + chunks[chunk_index + 1][:200])
            
            return " | ".join(context_chunks) if context_chunks else ""
            
        except ValueError:
            return ""
    
    async def _store_learning_bit(self, learning_bit: LearningBit, page_id: int):
        """Store learning bit in database with cross-reference generation"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if learning bit already exists
                cursor.execute(
                    "SELECT id FROM learning_bits WHERE content_hash = ?",
                    (learning_bit.content_hash,)
                )
                
                existing_bit = cursor.fetchone()
                
                if existing_bit:
                    # Update existing bit
                    cursor.execute("""
                        UPDATE learning_bits 
                        SET reference_count = reference_count + 1,
                            last_referenced = CURRENT_TIMESTAMP,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE content_hash = ?
                    """, (learning_bit.content_hash,))
                    bit_id = existing_bit[0]
                else:
                    # Insert new bit
                    cursor.execute("""
                        INSERT INTO learning_bits 
                        (page_id, content_hash, content_type, category, subcategory,
                         content, context, importance_score, confidence_score,
                         source_url, tags, complexity_level, language)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (page_id, learning_bit.content_hash, learning_bit.content_type,
                          learning_bit.category, learning_bit.subcategory, learning_bit.content,
                          learning_bit.context, learning_bit.importance_score,
                          learning_bit.confidence_score, learning_bit.source_url,
                          json.dumps(learning_bit.tags), learning_bit.complexity_level,
                          learning_bit.language))
                    
                    bit_id = cursor.lastrowid
                
                # Generate cross-references for new or updated learning bits
                await self._generate_cross_references(cursor, learning_bit, bit_id)
                
                conn.commit()
                logger.info(f"✅ Learning bit stored with cross-references: {bit_id}")
                    
        except Exception as e:
            logger.error(f"❌ Failed to store learning bit: {e}")
            raise
    
    async def _generate_cross_references(self, cursor, learning_bit: LearningBit, bit_id: int):
        """Generate cross-references between learning bits for enhanced context injection"""
        try:
            # 1. Find similar content by category and content type
            cursor.execute("""
                SELECT id, content, content_type, category, importance_score, confidence_score
                FROM learning_bits 
                WHERE id != ? AND category = ? AND content_type = ?
                ORDER BY importance_score DESC, confidence_score DESC
                LIMIT 5
            """, (bit_id, learning_bit.category, learning_bit.content_type))
            
            similar_bits = cursor.fetchall()
            
            # 2. Find related content by category (different content type)
            cursor.execute("""
                SELECT id, content, content_type, category, importance_score, confidence_score
                FROM learning_bits 
                WHERE id != ? AND category = ? AND content_type != ?
                ORDER BY importance_score DESC, confidence_score DESC
                LIMIT 3
            """, (bit_id, learning_bit.category, learning_bit.content_type))
            
            related_bits = cursor.fetchall()
            
            # 3. Find prerequisite content (lower complexity, same category)
            cursor.execute("""
                SELECT id, content, content_type, category, importance_score, confidence_score
                FROM learning_bits 
                WHERE id != ? AND category = ? AND complexity_level = 'beginner'
                ORDER BY importance_score DESC, confidence_score DESC
                LIMIT 2
            """, (bit_id, learning_bit.category))
            
            prerequisite_bits = cursor.fetchall()
            
            # 4. Create cross-references
            all_related = similar_bits + related_bits + prerequisite_bits
            
            for related_bit in all_related:
                related_id, related_content, related_type, related_category, related_importance, related_confidence = related_bit
                
                # Calculate relationship strength based on similarity
                relationship_strength = self._calculate_relationship_strength(
                    learning_bit, related_type, related_category, related_importance, related_confidence
                )
                
                # Only create cross-reference if strength is above threshold
                if relationship_strength > 0.3:
                    # Create cross-reference entry
                    cursor.execute("""
                        INSERT OR IGNORE INTO cross_references 
                        (source_bit_id, target_bit_id, source_type, target_type, 
                         relationship_type, strength, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                    """, (bit_id, related_id, learning_bit.content_type, related_type, 
                          'related', relationship_strength))
                    
                    # Create reverse cross-reference for bidirectional relationships
                    cursor.execute("""
                        INSERT OR IGNORE INTO cross_references 
                        (source_bit_id, target_bit_id, source_type, target_type, 
                         relationship_type, strength, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                    """, (related_id, bit_id, related_type, learning_bit.content_type, 
                          'related', relationship_strength))
            
            logger.info(f"✅ Generated cross-references for learning bit {bit_id}")
            
        except Exception as e:
            logger.error(f"❌ Failed to generate cross-references: {e}")
            # Don't raise - cross-references are optional
    
    def _calculate_relationship_strength(self, learning_bit: LearningBit, 
                                      related_type: str, related_category: str, 
                                      related_importance: float, related_confidence: float) -> float:
        """Calculate relationship strength between learning bits"""
        strength = 0.0
        
        # Base strength from importance and confidence
        strength += (learning_bit.importance_score + related_importance) * 0.3
        strength += (learning_bit.confidence_score + related_confidence) * 0.3
        
        # Category similarity bonus
        if learning_bit.category == related_category:
            strength += 0.2
        
        # Content type compatibility
        if learning_bit.content_type == related_type:
            strength += 0.1
        elif self._are_content_types_compatible(learning_bit.content_type, related_type):
            strength += 0.05
        
        # Subcategory bonus
        if learning_bit.subcategory and learning_bit.subcategory == related_category:
            strength += 0.1
        
        return min(1.0, strength)
    
    def _are_content_types_compatible(self, type1: str, type2: str) -> bool:
        """Check if two content types are compatible for relationships"""
        compatible_pairs = [
            ('concept', 'definition'),
            ('example', 'concept'),
            ('procedure', 'concept'),
            ('tutorial', 'example'),
            ('reference', 'concept'),
            ('tip', 'procedure'),
            ('warning', 'procedure'),
            ('troubleshooting', 'procedure')
        ]
        
        return (type1, type2) in compatible_pairs or (type2, type1) in compatible_pairs
    
    async def crawl_website(self, start_url: str, max_pages: int = 50, max_depth: int = 3) -> Dict[str, Any]:
        """Crawl a website starting from a URL with enhanced navigation"""
        logger.info(f"🚀 Starting enhanced website crawl: {start_url}")
        
        # Initialize crawl session
        crawl_session = {
            'start_url': start_url,
            'start_time': datetime.now(),
            'total_pages': 0,
            'total_learning_bits': 0,
            'crawl_depth_reached': 0,
            'domains_crawled': set(),
            'subjects_discovered': set(),
            'categories_found': set(),
            'errors': [],
            'crawl_paths': []
        }
        
        try:
            await self.start_session()
            
            # Initialize crawl queue with priority system
            self.crawl_queue = []
            self.crawled_urls = set()
            self.url_depths = {start_url: 0}  # Track depth for each URL
            self.url_priorities = {start_url: 1.0}  # Priority scoring
            
            # Add start URL to queue (don't mark as crawled yet)
            self.crawl_queue.append(start_url)
            
            page_count = 0
            current_depth = 0
            
            while self.crawl_queue and page_count < max_pages:
                # Get next URL with highest priority
                next_url = self._get_next_priority_url()
                if not next_url:
                    break
                
                current_depth = self.url_depths.get(next_url, 0)
                
                # Skip if we've reached max depth
                if current_depth >= max_depth:
                    logger.info(f"⏭️ Skipping {next_url} - max depth {max_depth} reached")
                    continue
                
                # Skip if already crawled (but allow start URL to be crawled)
                if next_url in self.crawled_urls and next_url != start_url:
                    logger.debug(f"⏭️ Skipping already crawled URL: {next_url}")
                    continue
                
                logger.info(f"🕷️ Crawling {next_url} (depth {current_depth}, priority {self.url_priorities.get(next_url, 0):.2f})")
                
                try:
                    # Crawl the page
                    crawled_page = await self.crawl_url(next_url, depth=current_depth)
                    
                    if crawled_page:
                        page_count += 1
                        crawl_session['total_pages'] = page_count
                        crawl_session['crawl_depth_reached'] = max(crawl_session['crawl_depth_reached'], current_depth)
                        
                        # Mark URL as successfully crawled
                        self.crawled_urls.add(next_url)
                        
                        # Track domain
                        domain = urlparse(next_url).netloc
                        crawl_session['domains_crawled'].add(domain)
                        
                        # Get the page ID from the database for learning bit storage
                        page_id = await self._get_page_id_from_url(next_url)
                        
                        # Extract and analyze learning bits
                        learning_bits = await self._extract_learning_bits(
                            crawled_page.content, next_url, page_id
                        )
                        
                        # Track subjects and categories discovered
                        for bit in learning_bits:
                            crawl_session['subjects_discovered'].add(bit.content_type)
                            crawl_session['categories_found'].add(bit.category)
                            if bit.subcategory:
                                crawl_session['categories_found'].add(f"{bit.category}:{bit.subcategory}")
                        
                        # Enhanced link discovery and prioritization
                        if current_depth < max_depth - 1:
                            new_links = self._discover_and_prioritize_links(
                                crawled_page.html_content, next_url, current_depth + 1
                            )
                            
                            # Add new links to queue with calculated priorities
                            for link, priority in new_links.items():
                                if link not in self.crawled_urls and link not in self.url_depths:
                                    self.crawl_queue.append(link)
                                    self.url_depths[link] = current_depth + 1
                                    self.url_priorities[link] = priority
                                    logger.debug(f"🔗 Added link: {link} (depth {current_depth + 1}, priority {priority:.2f})")
                        
                        # Log progress with enhanced metrics
                        if page_count % 5 == 0:
                            logger.info(f"📊 Crawled {page_count} pages, depth {current_depth}, queue: {len(self.crawl_queue)}, subjects: {len(crawl_session['subjects_discovered'])}")
                    
                    # Respect crawl delay
                    await asyncio.sleep(self.config.crawl_delay)
                
                except Exception as e:
                    error_msg = f"❌ Failed to crawl {next_url}: {e}"
                    logger.error(error_msg)
                    crawl_session['errors'].append(error_msg)
            
            # Final statistics
            crawl_session['end_time'] = datetime.now()
            crawl_session['duration'] = (crawl_session['end_time'] - crawl_session['start_time']).total_seconds()
            
            # Count total learning bits extracted
            total_learning_bits = 0
            try:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT COUNT(*) FROM learning_bits")
                    total_learning_bits = cursor.fetchone()[0]
            except Exception as e:
                logger.warning(f"⚠️ Could not count learning bits: {e}")
            
            crawl_session['total_learning_bits'] = total_learning_bits
            
            # Convert sets to lists for JSON serialization
            crawl_session['domains_crawled'] = list(crawl_session['domains_crawled'])
            crawl_session['subjects_discovered'] = list(crawl_session['subjects_discovered'])
            crawl_session['categories_found'] = list(crawl_session['categories_found'])
            
            logger.info(f"🎉 Enhanced website crawl completed: {page_count} pages, {total_learning_bits} learning bits, depth {crawl_session['crawl_depth_reached']} in {crawl_session['duration']:.1f}s")
            logger.info(f"📚 Discovered {len(crawl_session['subjects_discovered'])} subjects and {len(crawl_session['categories_found'])} categories")
            
            return crawl_session
            
        finally:
            await self.stop_session()
    
    def _extract_links(self, html_content: str, base_url: str) -> List[str]:
        """Extract links from HTML content"""
        links = []
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            for link in soup.find_all('a', href=True):
                href = link['href']
                
                # Convert relative URLs to absolute
                absolute_url = urljoin(base_url, href)
                
                # Filter out non-HTTP URLs and anchors
                if (absolute_url.startswith('http') and 
                    '#' not in absolute_url and 
                    'mailto:' not in absolute_url and
                    'tel:' not in absolute_url):
                    links.append(absolute_url)
            
            return links
            
        except Exception as e:
            logger.warning(f"⚠️ Link extraction failed: {e}")
            return []
    
    async def get_learning_bits(self, category: Optional[str] = None, 
                               subcategory: Optional[str] = None,
                               content_type: Optional[str] = None,
                               limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieve learning bits from database with filtering"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                query = """
                    SELECT lb.*, cp.url as page_url, cp.title as page_title
                    FROM learning_bits lb
                    JOIN crawled_pages cp ON lb.page_id = cp.id
                    WHERE 1=1
                """
                params = []
                
                if category:
                    query += " AND lb.category = ?"
                    params.append(category)
                
                if subcategory:
                    query += " AND lb.subcategory = ?"
                    params.append(subcategory)
                
                if content_type:
                    query += " AND lb.content_type = ?"
                    params.append(content_type)
                
                query += " ORDER BY lb.importance_score DESC, lb.confidence_score DESC"
                query += " LIMIT ?"
                params.append(limit)
                
                cursor.execute(query, params)
                rows = cursor.fetchall()
                
                # Convert to list of dictionaries
                columns = [description[0] for description in cursor.description]
                learning_bits = []
                
                for row in rows:
                    bit_dict = dict(zip(columns, row))
                    # Parse JSON fields
                    if bit_dict.get('tags'):
                        bit_dict['tags'] = json.loads(bit_dict['tags'])
                    learning_bits.append(bit_dict)
                
                return learning_bits
                
        except Exception as e:
            logger.error(f"❌ Failed to retrieve learning bits: {e}")
            return []
    
    async def search_learning_bits(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Search learning bits by content"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                search_query = """
                    SELECT lb.*, cp.url as page_url, cp.title as page_title
                    FROM learning_bits lb
                    JOIN crawled_pages cp ON lb.page_id = cp.id
                    WHERE lb.content LIKE ? OR lb.context LIKE ?
                    ORDER BY lb.importance_score DESC, lb.confidence_score DESC
                    LIMIT ?
                """
                
                search_term = f"%{query}%"
                cursor.execute(search_query, (search_term, search_term, limit))
                rows = cursor.fetchall()
                
                # Convert to list of dictionaries
                columns = [description[0] for description in cursor.description]
                learning_bits = []
                
                for row in rows:
                    bit_dict = dict(zip(columns, row))
                    # Parse JSON fields
                    if bit_dict.get('tags'):
                        bit_dict['tags'] = json.loads(bit_dict['tags'])
                    learning_bits.append(bit_dict)
                
                return learning_bits
                
        except Exception as e:
            logger.error(f"❌ Failed to search learning bits: {e}")
            return []

    def _get_next_priority_url(self) -> Optional[str]:
        """Get the next URL with highest priority from the queue"""
        if not self.crawl_queue:
            return None
        
        # Sort queue by priority (highest first)
        self.crawl_queue.sort(key=lambda url: self.url_priorities.get(url, 0), reverse=True)
        
        # Get highest priority URL (don't mark as crawled yet)
        next_url = self.crawl_queue.pop(0)
        
        return next_url
    
    def _discover_and_prioritize_links(self, html_content: str, base_url: str, target_depth: int) -> Dict[str, float]:
        """Discover links and calculate their priority scores"""
        links_with_priorities = {}
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            for link in soup.find_all('a', href=True):
                href = link['href']
                
                # Convert relative URLs to absolute
                absolute_url = urljoin(base_url, href)
                
                # Filter out non-HTTP URLs and anchors
                if (absolute_url.startswith('http') and 
                    '#' not in absolute_url and 
                    'mailto:' not in absolute_url and
                    'tel:' not in absolute_url):
                    
                    # Calculate priority score based on multiple factors
                    priority = self._calculate_link_priority(link, absolute_url, base_url, target_depth)
                    
                    if priority > 0.1:  # Only include relevant links
                        links_with_priorities[absolute_url] = priority
            
            return links_with_priorities
            
        except Exception as e:
            logger.warning(f"⚠️ Link discovery failed: {e}")
            return {}
    
    def _calculate_link_priority(self, link_element, absolute_url: str, base_url: str, target_depth: int) -> float:
        """Calculate priority score for a discovered link"""
        priority = 0.5  # Base priority
        
        try:
            # Factor 1: Link text relevance
            link_text = link_element.get_text(strip=True).lower()
            if link_text:
                # Check if link text contains relevant keywords
                relevant_keywords = ['guide', 'tutorial', 'documentation', 'api', 'reference', 
                                   'examples', 'getting started', 'how to', 'best practices']
                for keyword in relevant_keywords:
                    if keyword in link_text:
                        priority += 0.3
                        break
            
            # Factor 2: URL path relevance
            url_path = urlparse(absolute_url).path.lower()
            if url_path:
                # Prefer deeper paths (more specific content)
                path_depth = len([p for p in url_path.split('/') if p])
                priority += min(path_depth * 0.1, 0.3)
                
                # Prefer paths with relevant keywords
                path_keywords = ['docs', 'guide', 'tutorial', 'api', 'examples', 'reference']
                for keyword in path_keywords:
                    if keyword in url_path:
                        priority += 0.2
                        break
            
            # Factor 3: Same domain preference
            base_domain = urlparse(base_url).netloc
            link_domain = urlparse(absolute_url).netloc
            if base_domain == link_domain:
                priority += 0.2  # Prefer same domain
            
            # Factor 4: Depth-based priority adjustment
            if target_depth == 1:
                priority += 0.1  # Slight preference for first level
            elif target_depth > 2:
                priority -= 0.1  # Slight penalty for very deep links
            
            # Factor 5: Link element attributes
            if link_element.get('title'):
                title = link_element['title'].lower()
                if any(keyword in title for keyword in ['guide', 'tutorial', 'documentation']):
                    priority += 0.2
            
            # Factor 6: Avoid common non-content paths
            avoid_paths = ['/login', '/signup', '/contact', '/about', '/privacy', '/terms']
            if any(avoid_path in absolute_url.lower() for avoid_path in avoid_paths):
                priority -= 0.3
            
            # Ensure priority is within bounds
            priority = max(0.1, min(1.0, priority))
            
            return priority
            
        except Exception as e:
            logger.debug(f"⚠️ Priority calculation failed for {absolute_url}: {e}")
            return 0.5  # Return base priority on error

    async def get_comprehensive_learning_report(self) -> Dict[str, Any]:
        """Generate comprehensive report on learning coverage and discoveries"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get overall statistics
                cursor.execute("SELECT COUNT(*) FROM crawled_pages")
                total_pages = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM learning_bits")
                total_learning_bits = cursor.fetchone()[0]
                
                # Get content type distribution
                cursor.execute("""
                    SELECT content_type, COUNT(*) as count, 
                           AVG(importance_score) as avg_importance,
                           AVG(confidence_score) as avg_confidence
                    FROM learning_bits 
                    GROUP BY content_type 
                    ORDER BY count DESC
                """)
                content_type_stats = cursor.fetchall()
                
                # Get category distribution
                cursor.execute("""
                    SELECT category, COUNT(*) as count,
                           AVG(importance_score) as avg_importance,
                           AVG(confidence_score) as avg_confidence
                    FROM learning_bits 
                    GROUP BY category 
                    ORDER BY count DESC
                """)
                category_stats = cursor.fetchall()
                
                # Get subcategory distribution
                cursor.execute("""
                    SELECT subcategory, COUNT(*) as count,
                           AVG(importance_score) as avg_importance,
                           AVG(confidence_score) as avg_confidence
                    FROM learning_bits 
                    WHERE subcategory IS NOT NULL
                    GROUP BY subcategory 
                    ORDER BY count DESC
                """)
                subcategory_stats = cursor.fetchall()
                
                # Get domain coverage
                cursor.execute("""
                    SELECT cp.domain, COUNT(DISTINCT cp.id) as pages,
                           COUNT(lb.id) as learning_bits,
                           AVG(lb.importance_score) as avg_importance
                    FROM crawled_pages cp
                    LEFT JOIN learning_bits lb ON cp.id = lb.page_id
                    GROUP BY cp.domain
                    ORDER BY learning_bits DESC
                """)
                domain_stats = cursor.fetchall()
                
                # Get top learning bits by importance
                cursor.execute("""
                    SELECT lb.content_type, lb.category, lb.subcategory, 
                           lb.content, lb.importance_score, lb.confidence_score,
                           cp.url as source_url
                    FROM learning_bits lb
                    JOIN crawled_pages cp ON lb.page_id = cp.id
                    ORDER BY lb.importance_score DESC, lb.confidence_score DESC
                    LIMIT 10
                """)
                top_learning_bits = cursor.fetchall()
                
                # Get learning bit growth over time
                cursor.execute("""
                    SELECT DATE(lb.created_at) as date, COUNT(*) as count
                    FROM learning_bits lb
                    WHERE lb.created_at IS NOT NULL
                    GROUP BY DATE(lb.created_at)
                    ORDER BY date DESC
                    LIMIT 30
                """)
                learning_growth = cursor.fetchall()
                
                # Compile comprehensive report
                report = {
                    'summary': {
                        'total_pages_crawled': total_pages,
                        'total_learning_bits': total_learning_bits,
                        'average_learning_bits_per_page': total_learning_bits / total_pages if total_pages > 0 else 0,
                        'report_generated_at': datetime.now().isoformat()
                    },
                    'content_type_analysis': {
                        'distribution': [
                            {
                                'type': row[0],
                                'count': row[1],
                                'percentage': (row[1] / total_learning_bits * 100) if total_learning_bits > 0 else 0,
                                'avg_importance': row[2],
                                'avg_confidence': row[3]
                            }
                            for row in content_type_stats
                        ],
                        'total_types_discovered': len(content_type_stats)
                    },
                    'category_analysis': {
                        'distribution': [
                            {
                                'category': row[0],
                                'count': row[1],
                                'percentage': (row[1] / total_learning_bits * 100) if total_learning_bits > 0 else 0,
                                'avg_importance': row[2],
                                'avg_confidence': row[3]
                            }
                            for row in category_stats
                        ],
                        'total_categories_discovered': len(category_stats)
                    },
                    'subcategory_analysis': {
                        'distribution': [
                            {
                                'subcategory': row[0],
                                'count': row[1],
                                'percentage': (row[1] / total_learning_bits * 100) if total_learning_bits > 0 else 0,
                                'avg_importance': row[2],
                                'avg_confidence': row[3]
                            }
                            for row in subcategory_stats
                        ],
                        'total_subcategories_discovered': len(subcategory_stats)
                    },
                    'domain_coverage': {
                        'domains': [
                            {
                                'domain': row[0],
                                'pages_crawled': row[1],
                                'learning_bits': row[2],
                                'avg_importance': row[3]
                            }
                            for row in domain_stats
                        ],
                        'total_domains': len(domain_stats)
                    },
                    'top_learning_bits': [
                        {
                            'content_type': row[0],
                            'category': row[1],
                            'subcategory': row[2],
                            'content': row[3][:200] + '...' if len(row[3]) > 200 else row[3],
                            'importance_score': row[4],
                            'confidence_score': row[5],
                            'source_url': row[6]
                        }
                        for row in top_learning_bits
                    ],
                    'learning_growth': [
                        {
                            'date': row[0],
                            'new_learning_bits': row[1]
                        }
                        for row in learning_growth
                    ],
                    'insights': {
                        'most_common_content_type': content_type_stats[0][0] if content_type_stats else 'None',
                        'most_common_category': category_stats[0][0] if category_stats else 'None',
                        'highest_importance_content': top_learning_bits[0][0] if top_learning_bits else 'None',
                        'coverage_efficiency': (total_learning_bits / total_pages) if total_pages > 0 else 0
                    }
                }
                
                return report
                
        except Exception as e:
            logger.error(f"❌ Failed to generate comprehensive learning report: {e}")
            return {'error': str(e)}

class BackgroundCrawlerManager:
    """Manages background crawling operations without user interruption"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.active_crawls = {}  # Track active crawl sessions
        self.crawl_queue = []    # Queue of pending crawl jobs
        self.crawl_history = []  # History of completed crawls
        self.background_tasks = set()  # Active background tasks
        self.crawl_configs = {}  # Crawl configurations per job
        self.auto_restart = True  # Auto-restart failed crawls
        self.max_concurrent_crawls = 3  # Limit concurrent crawls
        
    async def start_background_crawl(self, job_id: str, start_url: str, 
                                   config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Start a background crawl job"""
        if len(self.active_crawls) >= self.max_concurrent_crawls:
            # Queue the job
            self.crawl_queue.append({
                'job_id': job_id,
                'start_url': start_url,
                'config': config or {},
                'queued_at': datetime.now(),
                'priority': config.get('priority', 'normal') if config else 'normal'
            })
            return {
                'status': 'queued',
                'job_id': job_id,
                'message': f'Crawl job queued. {len(self.crawl_queue)} jobs ahead.',
                'estimated_start': self._estimate_start_time(len(self.crawl_queue))
            }
        
        # Start the crawl immediately
        return await self._execute_crawl_job(job_id, start_url, config or {})
    
    async def _execute_crawl_job(self, job_id: str, start_url: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a crawl job in the background"""
        try:
            # Initialize crawler with job-specific config
            crawler_config = CrawlConfig()
            if config:
                if 'max_pages' in config:
                    crawler_config.max_pages = config['max_pages']
                if 'crawl_delay' in config:
                    crawler_config.crawl_delay = config['crawl_delay']
                if 'max_depth' in config:
                    crawler_config.max_depth = config['max_depth']
            
            crawler = WebCrawler(self.db_path)
            crawler.config = crawler_config
            
            # Track active crawl
            self.active_crawls[job_id] = {
                'start_time': datetime.now(),
                'start_url': start_url,
                'config': config,
                'status': 'running',
                'progress': {'pages_crawled': 0, 'learning_bits': 0},
                'crawler': crawler
            }
            
            # Start background task
            task = asyncio.create_task(self._run_background_crawl(job_id, crawler, start_url, config))
            self.background_tasks.add(task)
            task.add_done_callback(lambda t: self.background_tasks.discard(t))
            
            return {
                'status': 'started',
                'job_id': job_id,
                'message': 'Background crawl started successfully',
                'estimated_duration': self._estimate_duration(config)
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to start background crawl {job_id}: {e}")
            return {
                'status': 'failed',
                'job_id': job_id,
                'error': str(e),
                'message': 'Failed to start background crawl'
            }
    
    async def _run_background_crawl(self, job_id: str, crawler: WebCrawler, 
                                  start_url: str, config: Dict[str, Any]):
        """Run the actual crawl in the background"""
        try:
            logger.info(f"🚀 Starting background crawl {job_id} for {start_url}")
            
            # Execute the crawl
            result = await crawler.crawl_website(
                start_url=start_url,
                max_pages=config.get('max_pages', 50),
                max_depth=config.get('max_depth', 3)
            )
            
            # Update crawl status
            self.active_crawls[job_id]['status'] = 'completed'
            self.active_crawls[job_id]['result'] = result
            self.active_crawls[job_id]['end_time'] = datetime.now()
            
            # Add to history
            self.crawl_history.append({
                'job_id': job_id,
                'start_url': start_url,
                'config': config,
                'result': result,
                'start_time': self.active_crawls[job_id]['start_time'],
                'end_time': self.active_crawls[job_id]['end_time']
            })
            
            # Remove from active crawls
            del self.active_crawls[job_id]
            
            # Process next queued job
            await self._process_next_queued_job()
            
            logger.info(f"✅ Background crawl {job_id} completed successfully")
            
        except Exception as e:
            logger.error(f"❌ Background crawl {job_id} failed: {e}")
            
            # Update status
            if job_id in self.active_crawls:
                self.active_crawls[job_id]['status'] = 'failed'
                self.active_crawls[job_id]['error'] = str(e)
                self.active_crawls[job_id]['end_time'] = datetime.now()
            
            # Auto-restart if enabled
            if self.auto_restart and job_id in self.active_crawls:
                logger.info(f"🔄 Auto-restarting failed crawl {job_id}")
                await asyncio.sleep(5)  # Wait before restart
                await self._execute_crawl_job(job_id, start_url, config)
    
    async def _process_next_queued_job(self):
        """Process the next job in the queue"""
        if self.crawl_queue and len(self.active_crawls) < self.max_concurrent_crawls:
            # Sort by priority and queued time
            self.crawl_queue.sort(key=lambda job: (
                {'high': 0, 'normal': 1, 'low': 2}.get(job['priority'], 1),
                job['queued_at']
            ))
            
            next_job = self.crawl_queue.pop(0)
            await self._execute_crawl_job(
                next_job['job_id'],
                next_job['start_url'],
                next_job['config']
            )
    
    def get_crawl_status(self, job_id: str = None) -> Dict[str, Any]:
        """Get status of crawls"""
        if job_id:
            if job_id in self.active_crawls:
                return {
                    'job_id': job_id,
                    'status': 'active',
                    'details': self.active_crawls[job_id]
                }
            else:
                # Check history
                for crawl in self.crawl_history:
                    if crawl['job_id'] == job_id:
                        return {
                            'job_id': job_id,
                            'status': 'completed',
                            'details': crawl
                        }
                return {'job_id': job_id, 'status': 'not_found'}
        
        # Return overall status
        return {
            'active_crawls': len(self.active_crawls),
            'queued_jobs': len(self.crawl_queue),
            'completed_crawls': len(self.crawl_history),
            'max_concurrent': self.max_concurrent_crawls,
            'active_jobs': list(self.active_crawls.keys()),
            'queued_jobs': [job['job_id'] for job in self.crawl_queue]
        }
    
    def stop_crawl(self, job_id: str) -> Dict[str, Any]:
        """Stop an active crawl"""
        if job_id in self.active_crawls:
            crawl_info = self.active_crawls[job_id]
            crawl_info['status'] = 'stopped'
            crawl_info['end_time'] = datetime.now()
            
            # Cancel background task if possible
            # Note: This is a simplified approach - in production you'd want more robust task cancellation
            
            return {
                'status': 'stopped',
                'job_id': job_id,
                'message': 'Crawl stopped successfully'
            }
        
        return {
            'status': 'not_found',
            'job_id': job_id,
            'message': 'Crawl job not found'
        }
    
    def _estimate_start_time(self, queue_position: int) -> str:
        """Estimate when a queued job will start"""
        if queue_position == 0:
            return "immediately"
        
        # Rough estimate: 5 minutes per job ahead
        estimated_minutes = queue_position * 5
        if estimated_minutes < 60:
            return f"in {estimated_minutes} minutes"
        else:
            hours = estimated_minutes // 60
            minutes = estimated_minutes % 60
            return f"in {hours}h {minutes}m"
    
    def _estimate_duration(self, config: Dict[str, Any]) -> str:
        """Estimate crawl duration based on configuration"""
        max_pages = config.get('max_pages', 50)
        max_depth = config.get('max_depth', 3)
        crawl_delay = config.get('crawl_delay', 1.0)
        
        # Rough estimate: 2 seconds per page + delays
        estimated_seconds = max_pages * (2 + crawl_delay)
        
        if estimated_seconds < 60:
            return f"{estimated_seconds} seconds"
        elif estimated_seconds < 3600:
            minutes = estimated_seconds // 60
            return f"{minutes} minutes"
        else:
            hours = estimated_seconds // 3600
            minutes = (estimated_seconds % 3600) // 60
            return f"{hours}h {minutes}m"

# Example usage and testing
async def main():
    """Example usage of the web crawler"""
    # Initialize crawler
    crawler = WebCrawler('brain_memory_store/brain.db')
    
    # Crawl a website
    result = await crawler.crawl_website('https://docs.python.org/3/', max_pages=10)
    print(f"Crawl result: {result}")
    
    # Get learning bits
    bits = await crawler.get_learning_bits(category='programming', limit=5)
    print(f"Found {len(bits)} learning bits")
    
    # Search learning bits
    search_results = await crawler.search_learning_bits('function', limit=5)
    print(f"Search found {len(search_results)} results")

if __name__ == "__main__":
    asyncio.run(main())
