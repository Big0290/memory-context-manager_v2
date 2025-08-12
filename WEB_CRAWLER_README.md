# 🕷️ Web Crawler Engine for Memory Context Manager v2

A comprehensive web crawling and content ingestion system that automatically extracts, categorizes, and stores learning bits from web content for optimal context injection and cross-referencing.

## 🎯 **Overview**

The Web Crawler Engine transforms the Memory Context Manager from a text-only learning system into a comprehensive web content ingestion platform. It can:

- **Fetch web pages** with proper HTTP handling and robots.txt respect
- **Extract clean text content** using advanced HTML parsing
- **Categorize learning bits** with precise pattern matching and AI analysis
- **Store structured data** in an enhanced SQLite database
- **Enable cross-referencing** between related concepts and content
- **Provide MCP tools** for seamless integration with Cursor and other MCP clients

## 🏗️ **Architecture**

### **Core Components**

1. **WebCrawler** - Main crawling engine with async HTTP client
2. **ContentAnalyzer** - Intelligent content categorization and analysis
3. **Database Schema** - Enhanced storage for crawled content and learning bits
4. **MCP Tools** - Integration with Memory Context Manager v2
5. **Categorization Rules** - Customizable classification system

### **Data Flow**

```
🌐 Website → 🕷️ WebCrawler → 📄 ContentExtraction → 🧠 ContentAnalysis → 💾 DatabaseStorage → 🔍 MCPTools
```

## 🚀 **Features**

### **Advanced Web Crawling**

- **Async HTTP requests** with configurable timeouts and delays
- **Robots.txt compliance** and domain rate limiting
- **Link discovery** and intelligent crawling depth control
- **Error handling** and retry mechanisms
- **Session management** for efficient crawling

### **Intelligent Content Processing**

- **HTML parsing** with BeautifulSoup and Trafilatura
- **Text extraction** optimized for documentation and tutorials
- **Content chunking** into meaningful learning units
- **Context preservation** with surrounding content
- **Language detection** and support

### **Precise Categorization**

- **Content type detection**: concept, example, definition, procedure, warning, tip
- **Category classification**: programming, API, tutorial, reference, best practice
- **Subcategory identification**: Python, JavaScript, web development, database, etc.
- **Complexity assessment**: beginner, intermediate, advanced
- **Importance scoring** based on content characteristics
- **Confidence scoring** based on pattern matches

### **Enhanced Database Storage**

- **Crawled pages** with metadata and response information
- **Learning bits** with precise categorization and scoring
- **Cross-references** between related content
- **Crawl sessions** with statistics and configuration
- **Categorization rules** for custom classification

### **MCP Tool Integration**

- **crawl_website** - Start comprehensive website crawling
- **get_learning_bits** - Retrieve categorized learning content
- **search_learning_bits** - Semantic search through extracted content
- **get_crawl_status** - Monitor crawling operations
- **get_learning_statistics** - Comprehensive content analytics
- **add_categorization_rule** - Custom classification rules

## 📦 **Installation**

### **Dependencies**

```bash
# Install required packages
pip install aiohttp beautifulsoup4 trafilatura

# Or use the requirements file
pip install -r requirements_web_crawler.txt
```

### **Database Setup**

The web crawler automatically initializes its database schema when first used:

```python
from web_crawler_engine import WebCrawler

# Initialize crawler (creates tables automatically)
crawler = WebCrawler('brain_memory_store/brain.db')
```

## 🎮 **Usage Examples**

### **Basic Website Crawling**

```python
import asyncio
from web_crawler_engine import WebCrawler

async def crawl_docs():
    # Initialize crawler
    crawler = WebCrawler('brain_memory_store/brain.db')

    # Crawl Python documentation
    result = await crawler.crawl_website(
        start_url="https://docs.python.org/3/",
        max_pages=50,
        max_depth=3
    )

    print(f"Crawled {result['total_pages']} pages")
    print(f"Duration: {result.get('duration', 0):.1f} seconds")

# Run the crawler
asyncio.run(crawl_docs())
```

### **Learning Bit Retrieval**

```python
# Get programming concepts
programming_bits = await crawler.get_learning_bits(
    category='programming',
    subcategory='python',
    content_type='concept',
    complexity_level='beginner',
    min_importance=0.7,
    limit=20
)

for bit in programming_bits:
    print(f"📚 {bit['content_type']}: {bit['content'][:100]}...")
    print(f"   Importance: {bit['importance_score']:.2f}")
    print(f"   Confidence: {bit['confidence_score']:.2f}")
```

### **Content Search**

```python
# Search for specific concepts
search_results = await crawler.search_learning_bits(
    query="async function",
    category='programming',
    limit=10
)

for result in search_results:
    print(f"🔍 {result['content'][:80]}...")
    print(f"   Relevance: {result['relevance_score']:.2f}")
    print(f"   Source: {result['source_url']}")
```

### **MCP Tool Usage**

```python
from web_crawler_mcp_tools import WebCrawlerMCPTools

# Initialize MCP tools
mcp_tools = WebCrawlerMCPTools('brain_memory_store/brain.db')

# Crawl website via MCP
crawl_result = await mcp_tools.crawl_website(
    url="https://docs.python.org/3/",
    max_pages=25,
    follow_links=True,
    crawl_delay=1.0
)

# Get learning statistics
stats = await mcp_tools.get_learning_statistics()
print(f"Total learning bits: {stats['total_learning_bits']}")
```

## ⚙️ **Configuration**

### **CrawlConfig Options**

```python
from web_crawler_engine import CrawlConfig

config = CrawlConfig(
    max_depth=3,                    # Maximum link following depth
    max_pages_per_domain=100,       # Pages per domain limit
    crawl_delay=1.0,               # Delay between requests (seconds)
    timeout=30,                    # HTTP request timeout
    max_retries=3,                 # Retry attempts for failed requests
    user_agent="Custom Bot/1.0",   # Custom user agent string
    respect_robots_txt=True,        # Respect robots.txt files
    follow_links=True,              # Follow discovered links
    extract_code=True,              # Extract code blocks
    min_content_length=100,         # Minimum content length to process
    max_content_length=50000        # Maximum content length to process
)
```

### **Custom Categorization Rules**

```python
# Add custom classification rule
await mcp_tools.add_categorization_rule(
    rule_name="docker_patterns",
    rule_type="pattern",
    pattern="docker\\s+(?:run|build|compose)",
    category="devops",
    subcategory="docker",
    confidence_boost=0.3,
    priority=2
)
```

## 📊 **Database Schema**

### **Core Tables**

- **`crawled_pages`** - Web pages with metadata and content
- **`learning_bits`** - Extracted learning units with categorization
- **`learning_relationships`** - Cross-references between content
- **`crawl_queue`** - URL discovery and crawling management
- **`crawl_sessions`** - Crawling operation tracking
- **`categorization_rules`** - Custom classification patterns

### **Key Fields**

- **Content categorization**: type, category, subcategory, complexity
- **Quality scoring**: importance_score, confidence_score
- **Usage tracking**: reference_count, last_referenced
- **Source tracking**: source_url, page_id, extracted_at
- **Cross-referencing**: cross_references, relationships

## 🔍 **Content Analysis**

### **Automatic Detection**

The system automatically detects:

- **Content types** based on linguistic patterns
- **Categories** from technical terminology and context
- **Subcategories** from programming languages and frameworks
- **Complexity levels** from difficulty indicators
- **Importance scores** from content characteristics

### **Pattern Matching**

Uses regex patterns for:

- Function definitions and code blocks
- API endpoints and HTTP methods
- Tutorial steps and procedures
- Warning and caution statements
- Best practice recommendations

## 🚦 **Performance & Scalability**

### **Optimization Features**

- **Async HTTP requests** for concurrent crawling
- **Connection pooling** and session reuse
- **Intelligent delays** to respect rate limits
- **Content filtering** to avoid low-quality pages
- **Database indexing** for fast queries

### **Resource Management**

- **Configurable limits** for pages and depth
- **Memory-efficient** content processing
- **Automatic cleanup** of temporary data
- **Progress tracking** for long operations

## 🧪 **Testing**

### **Run Test Suite**

```bash
# Execute comprehensive tests
python test_web_crawler.py

# Test specific components
python -c "
import asyncio
from test_web_crawler import test_basic_crawling
asyncio.run(test_basic_crawling())
"
```

### **Test Coverage**

- ✅ Basic web crawling functionality
- ✅ Learning bit extraction and categorization
- ✅ Search and retrieval operations
- ✅ MCP tool integration
- ✅ Categorization rule management
- ✅ Full website crawling workflows

## 🔧 **Integration**

### **With Memory Context Manager v2**

```python
# In your main MCP server
from web_crawler_mcp_tools import WebCrawlerMCPTools

# Register web crawler tools
web_crawler_tools = WebCrawlerMCPTools('brain_memory_store/brain.db')
web_crawler_tools.register_tools(mcp_server)
```

### **With Cursor IDE**

The web crawler tools are automatically available through the MCP server:

```python
# Use in Cursor chat
await crawl_website(
    url="https://docs.python.org/3/",
    max_pages=20,
    follow_links=True
)

# Search for specific content
await search_learning_bits(
    query="async programming",
    category="programming"
)
```

## 📈 **Analytics & Monitoring**

### **Learning Statistics**

```python
stats = await mcp_tools.get_learning_statistics()

print(f"📊 Learning Content Analytics:")
print(f"   Total bits: {stats['total_learning_bits']}")
print(f"   Categories: {stats['category_distribution']}")
print(f"   Top domains: {stats['top_source_domains']}")
print(f"   Recent activity: {stats['recent_activity']}")
```

### **Crawl Monitoring**

```python
status = await mcp_tools.get_crawl_status()

print(f"🕷️ Crawl Operations:")
print(f"   Active: {status['total_active_crawls']}")
print(f"   Completed: {status['total_completed_crawls']}")
print(f"   Failed: {status['total_failed_crawls']}")
```

## 🚨 **Best Practices**

### **Responsible Crawling**

- **Respect robots.txt** and rate limits
- **Use appropriate delays** between requests
- **Limit crawl depth** and page counts
- **Monitor resource usage** during operations
- **Handle errors gracefully** with retry logic

### **Content Quality**

- **Filter low-quality content** with minimum length requirements
- **Use multiple extraction methods** for better text quality
- **Validate categorization** with confidence thresholds
- **Regularly review** and update categorization rules

### **Performance Optimization**

- **Batch database operations** for better throughput
- **Use connection pooling** for database access
- **Implement caching** for frequently accessed content
- **Monitor memory usage** during large crawls

## 🔮 **Future Enhancements**

### **Planned Features**

- **Semantic analysis** with LLM integration
- **Image content extraction** and OCR
- **Multi-language support** for international content
- **Advanced relationship mapping** with graph databases
- **Real-time crawling** with webhook notifications
- **Distributed crawling** across multiple nodes

### **AI Integration**

- **LLM-powered categorization** for better accuracy
- **Content summarization** for long articles
- **Semantic similarity** for better cross-referencing
- **Automatic tag generation** from content analysis

## 🤝 **Contributing**

### **Development Setup**

```bash
# Clone the repository
git clone <repository-url>
cd memory-context-manager_v2

# Install dependencies
pip install -r requirements_web_crawler.txt

# Run tests
python test_web_crawler.py
```

### **Code Style**

- Follow PEP 8 guidelines
- Use type hints throughout
- Add comprehensive docstrings
- Include error handling
- Write unit tests for new features

## 📄 **License**

This web crawler engine is part of the Memory Context Manager v2 project and follows the same licensing terms.

## 🆘 **Support**

### **Common Issues**

1. **Import errors**: Ensure all dependencies are installed
2. **Database errors**: Check file permissions and SQLite installation
3. **Network errors**: Verify internet connectivity and firewall settings
4. **Memory issues**: Reduce max_pages or implement pagination

### **Getting Help**

- Check the test suite for examples
- Review the database schema for data structure
- Examine logs for detailed error information
- Use the MCP tools for debugging and monitoring

---

**🎉 The Web Crawler Engine transforms your Memory Context Manager into a comprehensive knowledge ingestion system, enabling truly intelligent context injection and cross-referencing across all your learning content!**
