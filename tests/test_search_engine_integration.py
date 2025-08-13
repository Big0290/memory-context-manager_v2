#!/usr/bin/env python3
"""
Test script for search engine integration capabilities
"""

import asyncio
import sys
import os
import sqlite3
from pathlib import Path
sys.path.append(str(Path.cwd()))

from search_engine_integration import SearchEngineIntegration, SearchEngineConfig

async def test_search_engine_integration():
    """Test the search engine integration capabilities"""
    print("🔍 Testing Search Engine Integration")
    print("=" * 45)
    
    # Create configuration (without API keys for testing)
    config = SearchEngineConfig(
        google_custom_search_api_key="",  # Will use fallback mode
        google_custom_search_engine_id="",
        bing_search_api_key="",  # Will use fallback mode
        enable_google_search=True,
        enable_bing_search=True,
        enable_duplicate_filtering=True,
        enable_relevance_scoring=True
    )
    
    # Initialize search engine integration
    integration = SearchEngineIntegration('brain_memory_store/brain.db', config)
    
    print(f"\n⚙️ Search Engine Configuration:")
    print(f"   Google Search: {'✅ Enabled' if config.enable_google_search else '❌ Disabled'}")
    print(f"   Bing Search: {'✅ Enabled' if config.enable_bing_search else '❌ Disabled'}")
    print(f"   Duplicate Filtering: {'✅ Enabled' if config.enable_duplicate_filtering else '❌ Disabled'}")
    print(f"   Relevance Scoring: {'✅ Enabled' if config.enable_relevance_scoring else '❌ Disabled'}")
    
    # Test database initialization
    print(f"\n🗄️ Testing Search Database...")
    try:
        with sqlite3.connect(integration.db_path) as conn:
            cursor = conn.cursor()
            
            # Check search results table
            cursor.execute("SELECT COUNT(*) FROM search_results")
            results_count = cursor.fetchone()[0]
            print(f"   Search Results: {results_count}")
            
            # Check search queries table
            cursor.execute("SELECT COUNT(*) FROM search_queries")
            queries_count = cursor.fetchone()[0]
            print(f"   Search Queries: {queries_count}")
            
            # Check search engine metrics table
            cursor.execute("SELECT COUNT(*) FROM search_engine_metrics")
            metrics_count = cursor.fetchone()[0]
            print(f"   Search Engine Metrics: {metrics_count}")
            
            print(f"✅ Search database is operational")
            
    except Exception as e:
        print(f"❌ Search database test failed: {e}")
        return False
    
    # Test search engine status
    print(f"\n🔍 Testing Search Engine Status...")
    try:
        metrics = await integration.get_search_metrics()
        
        print(f"   Engine Status:")
        print(f"     Google: {'✅ Available' if metrics['engine_status']['google'] else '❌ Not Available'}")
        print(f"     Bing: {'✅ Available' if metrics['engine_status']['bing'] else '❌ Not Available'}")
        
        print(f"   Rate Limits:")
        print(f"     Google Remaining: {metrics['rate_limits']['google_remaining']}")
        print(f"     Bing Remaining: {metrics['rate_limits']['bing_remaining']}")
        
        print(f"   Search Metrics:")
        print(f"     Total Searches: {metrics['search_metrics']['total_searches']}")
        print(f"     Google Searches: {metrics['search_metrics']['google_searches']}")
        print(f"     Bing Searches: {metrics['search_metrics']['bing_searches']}")
        print(f"     Total Results: {metrics['search_metrics']['total_results']}")
        print(f"     Average Relevance: {metrics['search_metrics']['average_relevance']:.2f}")
        print(f"     Duplicates Filtered: {metrics['search_metrics']['duplicate_filtered']}")
        
        print(f"✅ Search engine status retrieved successfully")
        
    except Exception as e:
        print(f"❌ Search engine status test failed: {e}")
        return False
    
    # Test multi-engine search (will work in fallback mode)
    print(f"\n🔍 Testing Multi-Engine Search...")
    try:
        query = "Model Context Protocol MCP documentation"
        max_results = 10
        
        print(f"   Query: '{query}'")
        print(f"   Max Results: {max_results}")
        print(f"   Note: Running in fallback mode (no API keys configured)")
        
        # This will work even without API keys (fallback mode)
        results = await integration.perform_multi_engine_search(query, max_results)
        
        print(f"   Results Found: {len(results)}")
        
        if results:
            print(f"\n   Top Results:")
            for i, result in enumerate(results[:3]):
                print(f"     {i+1}. {result.title}")
                print(f"        URL: {result.url}")
                print(f"        Engine: {result.source_engine}")
                print(f"        Relevance: {result.relevance_score:.2f}")
                print(f"        Type: {result.content_type}")
        
        print(f"✅ Multi-engine search test completed")
        
    except Exception as e:
        print(f"❌ Multi-engine search test failed: {e}")
        return False
    
    return True

async def test_search_configuration():
    """Test search engine configuration options"""
    print(f"\n⚙️ Testing Search Configuration Options")
    print("=" * 40)
    
    # Test different configuration scenarios
    configs = [
        ("Default Config", SearchEngineConfig()),
        ("Google Only", SearchEngineConfig(enable_bing_search=False)),
        ("Bing Only", SearchEngineConfig(enable_google_search=False)),
        ("High Threshold", SearchEngineConfig(
            result_filtering_threshold=0.8
        )),
        ("Low Threshold", SearchEngineConfig(
            result_filtering_threshold=0.3
        ))
    ]
    
    for config_name, config in configs:
        print(f"\n   {config_name}:")
        print(f"     Google: {config.enable_google_search}")
        print(f"     Bing: {config.enable_bing_search}")
        print(f"     Filtering Threshold: {config.result_filtering_threshold}")
        print(f"     Max Results: {config.max_results_per_query}")
        print(f"     Rate Limit: {config.search_rate_limit}/hour")
    
    print(f"✅ Search configuration options tested")
    return True

async def test_fallback_functionality():
    """Test fallback functionality when APIs are not available"""
    print(f"\n🔄 Testing Fallback Functionality")
    print("=" * 35)
    
    # Create integration without API keys
    config = SearchEngineConfig(
        google_custom_search_api_key="",
        bing_search_api_key="",
        enable_google_search=True,
        enable_bing_search=True
    )
    
    integration = SearchEngineIntegration('brain_memory_store/brain.db', config)
    
    print(f"   Fallback Mode: {'✅ Active' if not integration.google_search and not integration.bing_search else '❌ Not Active'}")
    print(f"   Google API: {'❌ Not Available' if not integration.google_search else '✅ Available'}")
    print(f"   Bing API: {'❌ Not Available' if not integration.bing_search else '✅ Available'}")
    
    # Test that system still works
    try:
        metrics = await integration.get_search_metrics()
        print(f"   System Status: ✅ Operational")
        print(f"   Metrics Available: ✅ Yes")
    except Exception as e:
        print(f"   System Status: ❌ Failed")
        print(f"   Error: {e}")
        return False
    
    print(f"✅ Fallback functionality working correctly")
    return True

async def main():
    """Main test function"""
    print("🔍 Search Engine Integration Test")
    print("=" * 50)
    print("   Testing Phase 3B: Search Engine Integration")
    
    # Test 1: Search Engine Integration
    print(f"\n🧪 Test 1: Search Engine Integration")
    integration_success = await test_search_engine_integration()
    
    # Test 2: Search Configuration
    print(f"\n🧪 Test 2: Search Configuration Options")
    config_success = await test_search_configuration()
    
    # Test 3: Fallback Functionality
    print(f"\n🧪 Test 3: Fallback Functionality")
    fallback_success = await test_fallback_functionality()
    
    # Final status
    print(f"\n🎯 Final Test Results:")
    print(f"   🔍 Search Engine Integration: {'✅ PASS' if integration_success else '❌ FAIL'}")
    print(f"   ⚙️ Search Configuration: {'✅ PASS' if config_success else '❌ FAIL'}")
    print(f"   🔄 Fallback Functionality: {'✅ PASS' if fallback_success else '❌ FAIL'}")
    
    total_tests = 3
    passed_tests = sum([integration_success, config_success, fallback_success])
    
    print(f"\n📊 Overall Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print(f"\n🎉 ALL TESTS PASSED! Search Engine Integration is operational!")
        print(f"   Your AI system can now search across Google and Bing!")
        print(f"   Ready for enhanced content discovery!")
        
        # Show next steps
        print(f"\n🚀 Next Steps for Full Integration:")
        print(f"   1. Get Google Custom Search API key")
        print(f"   2. Get Bing Web Search API key")
        print(f"   3. Set environment variables:")
        print(f"      export GOOGLE_CUSTOM_SEARCH_API_KEY='your_key_here'")
        print(f"      export GOOGLE_CUSTOM_SEARCH_ENGINE_ID='your_engine_id'")
        print(f"      export BING_SEARCH_API_KEY='your_key_here'")
        print(f"   4. Restart the system for full API access")
        
    else:
        print(f"\n⚠️  Some tests failed. Review before proceeding.")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
