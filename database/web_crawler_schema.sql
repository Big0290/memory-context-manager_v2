-- Web Crawler Database Schema for Memory Context Manager v2
-- Enhanced schema for comprehensive web crawling and knowledge extraction

-- Table for storing crawled web pages
CREATE TABLE IF NOT EXISTS crawled_pages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT UNIQUE NOT NULL,
    title TEXT,
    content TEXT NOT NULL,
    html_content TEXT,
    content_type TEXT DEFAULT 'text/html',
    status_code INTEGER,
    response_time_ms INTEGER,
    last_crawled TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    crawl_depth INTEGER DEFAULT 0,
    parent_url TEXT,
    domain TEXT,
    path TEXT,
    metadata TEXT, -- JSON blob for headers, robots.txt info, etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for extracted learning bits with precise categorization
CREATE TABLE IF NOT EXISTS learning_bits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    page_id INTEGER,
    content_hash TEXT UNIQUE NOT NULL,
    content_type TEXT NOT NULL, -- 'concept', 'example', 'definition', 'procedure', 'warning', 'tip'
    category TEXT NOT NULL, -- 'programming', 'api', 'tutorial', 'reference', 'best_practice'
    subcategory TEXT, -- 'python', 'javascript', 'web_development', 'database'
    content TEXT NOT NULL,
    context TEXT, -- surrounding context for better understanding
    importance_score REAL DEFAULT 0.5,
    confidence_score REAL DEFAULT 0.8,
    source_url TEXT,
    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_referenced TIMESTAMP,
    reference_count INTEGER DEFAULT 0,
    cross_references TEXT, -- JSON array of related learning bit IDs
    tags TEXT, -- JSON array of tags for precise categorization
    emotional_weight TEXT DEFAULT 'medium',
    complexity_level TEXT DEFAULT 'moderate',
    language TEXT DEFAULT 'en',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (page_id) REFERENCES crawled_pages(id)
);

-- Table for semantic relationships between learning bits
CREATE TABLE IF NOT EXISTS learning_relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_bit_id INTEGER NOT NULL,
    target_bit_id INTEGER NOT NULL,
    relationship_type TEXT NOT NULL, -- 'prerequisite', 'related', 'implements', 'extends', 'similar', 'opposite'
    strength REAL DEFAULT 0.5,
    bidirectional BOOLEAN DEFAULT FALSE,
    metadata TEXT, -- JSON blob for relationship context
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (source_bit_id) REFERENCES learning_bits(id),
    FOREIGN KEY (target_bit_id) REFERENCES learning_bits(id)
);

-- Table for crawling queue and discovered URLs
CREATE TABLE IF NOT EXISTS crawl_queue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT UNIQUE NOT NULL,
    priority INTEGER DEFAULT 5, -- 1=highest, 10=lowest
    status TEXT DEFAULT 'pending', -- 'pending', 'crawling', 'completed', 'failed', 'skipped'
    discovered_from TEXT, -- URL that led to this discovery
    depth_level INTEGER DEFAULT 0,
    domain TEXT,
    estimated_importance REAL DEFAULT 0.5,
    last_attempt TIMESTAMP,
    retry_count INTEGER DEFAULT 0,
    max_retries INTEGER DEFAULT 3,
    robots_txt_allowed BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for domain-specific crawling rules and settings
CREATE TABLE IF NOT EXISTS domain_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain TEXT UNIQUE NOT NULL,
    robots_txt TEXT,
    crawl_delay REAL DEFAULT 1.0,
    max_depth INTEGER DEFAULT 3,
    allowed_paths TEXT, -- JSON array of allowed path patterns
    blocked_paths TEXT, -- JSON array of blocked path patterns
    content_filters TEXT, -- JSON array of content filtering rules
    priority_boost REAL DEFAULT 1.0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for crawling sessions and statistics
CREATE TABLE IF NOT EXISTS crawl_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_name TEXT NOT NULL,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP,
    status TEXT DEFAULT 'running', -- 'running', 'completed', 'paused', 'stopped'
    total_urls_discovered INTEGER DEFAULT 0,
    total_pages_crawled INTEGER DEFAULT 0,
    total_learning_bits_extracted INTEGER DEFAULT 0,
    total_relationships_found INTEGER DEFAULT 0,
    errors_encountered INTEGER DEFAULT 0,
    configuration TEXT, -- JSON blob for crawl configuration
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for content categorization patterns and rules
CREATE TABLE IF NOT EXISTS categorization_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_name TEXT UNIQUE NOT NULL,
    rule_type TEXT NOT NULL, -- 'keyword', 'pattern', 'structure', 'semantic'
    pattern TEXT NOT NULL, -- regex pattern or keyword list
    category TEXT NOT NULL,
    subcategory TEXT,
    confidence_boost REAL DEFAULT 0.1,
    priority INTEGER DEFAULT 5,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for optimal performance
CREATE INDEX IF NOT EXISTS idx_crawled_pages_url ON crawled_pages(url);
CREATE INDEX IF NOT EXISTS idx_crawled_pages_domain ON crawled_pages(domain);
CREATE INDEX IF NOT EXISTS idx_crawled_pages_last_crawled ON crawled_pages(last_crawled);
CREATE INDEX IF NOT EXISTS idx_learning_bits_category ON learning_bits(category);
CREATE INDEX IF NOT EXISTS idx_learning_bits_subcategory ON learning_bits(subcategory);
CREATE INDEX IF NOT EXISTS idx_learning_bits_content_type ON learning_bits(content_type);
CREATE INDEX IF NOT EXISTS idx_learning_bits_importance ON learning_bits(importance_score);
CREATE INDEX IF NOT EXISTS idx_learning_bits_tags ON learning_bits(tags);
CREATE INDEX IF NOT EXISTS idx_crawl_queue_status ON crawl_queue(status);
CREATE INDEX IF NOT EXISTS idx_crawl_queue_priority ON crawl_queue(priority);
CREATE INDEX IF NOT EXISTS idx_crawl_queue_domain ON crawl_queue(domain);
CREATE INDEX IF NOT EXISTS idx_learning_relationships_source ON learning_relationships(source_bit_id);
CREATE INDEX IF NOT EXISTS idx_learning_relationships_target ON learning_relationships(target_bit_id);
CREATE INDEX IF NOT EXISTS idx_learning_relationships_type ON learning_relationships(relationship_type);
