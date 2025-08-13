#!/usr/bin/env python3
"""
Test Web Crawler - Demonstration of comprehensive web crawling capabilities
Tests the web crawler engine, MCP tools, and learning bit extraction
"""

import asyncio
import json
import logging
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from web_crawler_engine import WebCrawler, CrawlConfig
from web_crawler_mcp_tools import WebCrawlerMCPTools

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_basic_crawling():
    """Test basic web crawling functionality"""
    print("\n🕷️ Testing Basic Web Crawling")
    print("=" * 50)
    
    try:
        # Initialize crawler
        crawler = WebCrawler('brain_memory_store/brain.db')
        
        # Test crawling a simple documentation page
        test_url = "https://docs.python.org/3/tutorial/"
        
        print(f"Starting crawl of: {test_url}")
        result = await crawler.crawl_website(test_url, max_pages=5)
        
        print(f"✅ Crawl completed successfully!")
        print(f"   Pages crawled: {result['total_pages']}")
        print(f"   Duration: {result.get('duration', 0):.1f} seconds")
        
        return result
        
    except Exception as e:
        print(f"❌ Basic crawling test failed: {e}")
        return None

async def test_learning_bit_extraction():
    """Test learning bit extraction and categorization"""
    print("\n📚 Testing Learning Bit Extraction")
    print("=" * 50)
    
    try:
        crawler = WebCrawler('brain_memory_store/brain.db')
        
        # Get learning bits by category
        print("Retrieving programming-related learning bits...")
        programming_bits = await crawler.get_learning_bits(
            category='programming',
            limit=10
        )
        
        print(f"✅ Found {len(programming_bits)} programming learning bits")
        
        if programming_bits:
            print("\nSample learning bits:")
            for i, bit in enumerate(programming_bits[:3]):
                print(f"\n{i+1}. {bit.get('content_type', 'unknown')} - {bit.get('category', 'unknown')}")
                print(f"   Content: {bit.get('content', '')[:100]}...")
                print(f"   Importance: {bit.get('importance_score', 0):.2f}")
                print(f"   Confidence: {bit.get('confidence_score', 0):.2f}")
        
        return programming_bits
        
    except Exception as e:
        print(f"❌ Learning bit extraction test failed: {e}")
        return None

async def test_search_functionality():
    """Test search functionality"""
    print("\n🔍 Testing Search Functionality")
    print("=" * 50)
    
    try:
        crawler = WebCrawler('brain_memory_store/brain.db')
        
        # Search for specific terms
        search_terms = ['function', 'class', 'import']
        
        for term in search_terms:
            print(f"\nSearching for: '{term}'")
            results = await crawler.search_learning_bits(term, limit=5)
            
            print(f"   Found {len(results)} results")
            
            if results:
                top_result = results[0]
                print(f"   Top result: {top_result.get('content', '')[:80]}...")
                print(f"   Relevance: {top_result.get('relevance_score', 0):.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Search functionality test failed: {e}")
        return False

async def test_mcp_tools():
    """Test MCP tool integration"""
    print("\n🔧 Testing MCP Tool Integration")
    print("=" * 50)
    
    try:
        # Initialize MCP tools
        mcp_tools = WebCrawlerMCPTools('brain_memory_store/brain.db')
        
        # Test learning statistics
        print("Getting learning statistics...")
        stats = await mcp_tools.get_learning_statistics()
        
        if stats.get('success'):
            print(f"✅ Statistics retrieved successfully!")
            print(f"   Total learning bits: {stats.get('total_learning_bits', 0)}")
            print(f"   Total crawled pages: {stats.get('total_crawled_pages', 0)}")
            
            # Show category distribution
            categories = stats.get('category_distribution', {})
            if categories:
                print(f"   Category distribution:")
                for category, count in list(categories.items())[:5]:
                    print(f"     {category}: {count}")
        else:
            print(f"⚠️ Statistics retrieval failed: {stats.get('error', 'Unknown error')}")
        
        return stats
        
    except Exception as e:
        print(f"❌ MCP tools test failed: {e}")
        return None

async def test_categorization_rules():
    """Test categorization rule management"""
    print("\n⚙️ Testing Categorization Rules")
    print("=" * 50)
    
    try:
        mcp_tools = WebCrawlerMCPTools('brain_memory_store/brain.db')
        
        # Add a test categorization rule
        print("Adding test categorization rule...")
        rule_result = await mcp_tools.add_categorization_rule(
            rule_name="test_python_function",
            rule_type="keyword",
            pattern="def\\s+\\w+\\s*\\(",
            category="programming",
            subcategory="python",
            confidence_boost=0.2,
            priority=3
        )
        
        if rule_result.get('success'):
            print(f"✅ Rule added successfully: {rule_result.get('rule_name')}")
        else:
            print(f"⚠️ Rule addition failed: {rule_result.get('error', 'Unknown error')}")
        
        # Get all rules
        print("\nRetrieving all categorization rules...")
        rules = await mcp_tools.get_categorization_rules()
        
        if rules.get('success'):
            print(f"✅ Retrieved {rules.get('total_rules', 0)} rules")
            for rule in rules.get('rules', [])[:3]:
                print(f"   - {rule['rule_name']}: {rule['rule_type']} -> {rule['category']}")
        else:
            print(f"⚠️ Rules retrieval failed: {rules.get('error', 'Unknown error')}")
        
        return rules
        
    except Exception as e:
        print(f"❌ Categorization rules test failed: {e}")
        return None

async def test_website_crawl():
    """Test full website crawling with MCP tools"""
    print("\n🌐 Testing Full Website Crawl")
    print("=" * 50)
    
    try:
        mcp_tools = WebCrawlerMCPTools('brain_memory_store/brain.db')
        
        # Test crawling a small documentation site
        test_url = "https://httpbin.org/html"  # Simple test page
        
        print(f"Starting crawl of: {test_url}")
        crawl_result = await mcp_tools.crawl_website(
            url=test_url,
            max_pages=3,
            max_depth=2,
            follow_links=False,  # Don't follow links for test
            crawl_delay=0.5
        )
        
        if crawl_result.get('success'):
            print(f"✅ Website crawl completed successfully!")
            print(f"   Pages crawled: {crawl_result.get('total_pages_crawled', 0)}")
            print(f"   Learning bits extracted: {crawl_result.get('total_learning_bits_extracted', 0)}")
            print(f"   Duration: {crawl_result.get('crawl_duration_seconds', 0):.1f} seconds")
        else:
            print(f"⚠️ Website crawl failed: {crawl_result.get('error', 'Unknown error')}")
        
        return crawl_result
        
    except Exception as e:
        print(f"❌ Full website crawl test failed: {e}")
        return None

async def run_comprehensive_test():
    """Run all tests comprehensively"""
    print("🚀 Starting Comprehensive Web Crawler Tests")
    print("=" * 60)
    
    test_results = {}
    
    # Test 1: Basic crawling
    test_results['basic_crawling'] = await test_basic_crawling()
    
    # Test 2: Learning bit extraction
    test_results['learning_bits'] = await test_learning_bit_extraction()
    
    # Test 3: Search functionality
    test_results['search'] = await test_search_functionality()
    
    # Test 4: MCP tools
    test_results['mcp_tools'] = await test_mcp_tools()
    
    # Test 5: Categorization rules
    test_results['categorization_rules'] = await test_categorization_rules()
    
    # Test 6: Full website crawl
    test_results['website_crawl'] = await test_website_crawl()
    
    # Summary
    print("\n📊 Test Results Summary")
    print("=" * 60)
    
    successful_tests = 0
    total_tests = len(test_results)
    
    for test_name, result in test_results.items():
        if result is not None and (isinstance(result, bool) and result) or (isinstance(result, dict) and result.get('success', False)):
            print(f"✅ {test_name}: PASSED")
            successful_tests += 1
        else:
            print(f"❌ {test_name}: FAILED")
    
    print(f"\n🎯 Overall Result: {successful_tests}/{total_tests} tests passed")
    
    if successful_tests == total_tests:
        print("🎉 All tests passed! Web crawler is working correctly.")
    else:
        print("⚠️ Some tests failed. Check the logs for details.")
    
    return test_results

def main():
    """Main test runner"""
    print("🕷️ Web Crawler Test Suite")
    print("Testing comprehensive web crawling capabilities for Memory Context Manager v2")
    
    try:
        # Run tests
        results = asyncio.run(run_comprehensive_test())
        
        # Save results to file
        with open('web_crawler_test_results.json', 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n📄 Test results saved to: web_crawler_test_results.json")
        
    except KeyboardInterrupt:
        print("\n⏹️ Tests interrupted by user")
    except Exception as e:
        print(f"\n💥 Test suite failed with error: {e}")
        logger.exception("Test suite error")

if __name__ == "__main__":
    main()
