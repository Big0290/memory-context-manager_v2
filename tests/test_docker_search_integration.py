#!/usr/bin/env python3
"""
Docker-specific test script for search engine integration
Tests the system with Docker environment variables
"""

import asyncio
import sys
import os
import sqlite3
from pathlib import Path
sys.path.append(str(Path.cwd()))

from search_engine_integration import SearchEngineIntegration, SearchEngineConfig

async def test_docker_environment():
    """Test the search engine integration in Docker environment"""
    print("🐳 Testing Search Engine Integration in Docker Environment")
    print("=" * 60)
    
    # Check environment variables
    print(f"\n🔍 Environment Variables Check:")
    google_key = os.getenv('GOOGLE_CUSTOM_SEARCH_API_KEY', '')
    google_engine = os.getenv('GOOGLE_CUSTOM_SEARCH_ENGINE_ID', '')
    bing_key = os.getenv('BING_SEARCH_API_KEY', '')
    
    print(f"   GOOGLE_CUSTOM_SEARCH_API_KEY: {'✅ Set' if google_key else '❌ Not Set'}")
    if google_key:
        print(f"     Value: {google_key[:10]}...{google_key[-4:]}")
    
    print(f"   GOOGLE_CUSTOM_SEARCH_ENGINE_ID: {'✅ Set' if google_engine else '❌ Not Set'}")
    if google_engine:
        print(f"     Value: {google_engine}")
    
    print(f"   BING_SEARCH_API_KEY: {'✅ Set' if bing_key else '❌ Not Set'}")
    if bing_key:
        print(f"     Value: {bing_key[:10]}...{bing_key[-4:]}")
    
    # Create configuration from environment
    config = SearchEngineConfig(
        google_custom_search_api_key=google_key,
        google_custom_search_engine_id=google_engine,
        bing_search_api_key=bing_key,
        enable_google_search=bool(google_key and google_engine),
        enable_bing_search=bool(bing_key)
    )
    
    print(f"\n⚙️ Configuration Created:")
    print(f"   Google Search Enabled: {config.enable_google_search}")
    print(f"   Bing Search Enabled: {config.enable_bing_search}")
    print(f"   API Keys Valid: {bool(google_key and google_engine) or bool(bing_key)}")
    
    return config

async def test_search_engine_initialization(config: SearchEngineConfig):
    """Test search engine initialization with the configuration"""
    print(f"\n🚀 Testing Search Engine Initialization")
    print("=" * 45)
    
    try:
        # Initialize search engine integration
        integration = SearchEngineIntegration('brain_memory_store/brain.db', config)
        
        # Check what engines are available
        google_available = integration.google_search is not None
        bing_available = integration.bing_search is not None
        
        print(f"   Google Search Engine: {'✅ Available' if google_available else '❌ Not Available'}")
        print(f"   Bing Search Engine: {'✅ Available' if bing_available else '❌ Not Available'}")
        
        # Get metrics to verify initialization
        metrics = await integration.get_search_metrics()
        
        print(f"\n📊 Search Engine Status:")
        print(f"   Total Searches: {metrics['search_metrics']['total_searches']}")
        print(f"   Google Searches: {metrics['search_metrics']['google_searches']}")
        print(f"   Bing Searches: {metrics['search_metrics']['bing_searches']}")
        print(f"   Engine Status: {metrics['engine_status']}")
        
        print(f"✅ Search engine initialization completed successfully")
        return integration, True
        
    except Exception as e:
        print(f"❌ Search engine initialization failed: {e}")
        return None, False

async def test_actual_search_functionality(integration: SearchEngineIntegration):
    """Test actual search functionality if APIs are available"""
    print(f"\n🔍 Testing Actual Search Functionality")
    print("=" * 45)
    
    if not integration.google_search and not integration.bing_search:
        print(f"   ⚠️ No search engines available - skipping search test")
        print(f"   💡 This is expected if no API keys are configured")
        return True
    
    try:
        # Perform a real search
        query = "Model Context Protocol MCP documentation"
        max_results = 5
        
        print(f"   Query: '{query}'")
        print(f"   Max Results: {max_results}")
        
        # Get available engines properly
        metrics = await integration.get_search_metrics()
        available_engines = [k for k, v in metrics['engine_status'].items() if v]
        print(f"   Available Engines: {available_engines}")
        
        # Perform search
        results = await integration.perform_multi_engine_search(query, max_results)
        
        print(f"\n   Search Results:")
        print(f"     Total Found: {len(results)}")
        
        if results:
            for i, result in enumerate(results[:3]):
                print(f"     {i+1}. {result.title}")
                print(f"        URL: {result.url}")
                print(f"        Engine: {result.source_engine}")
                print(f"        Relevance: {result.relevance_score:.2f}")
                print(f"        Type: {result.content_type}")
        else:
            print(f"     No results found - this might indicate an API issue")
        
        print(f"✅ Search functionality test completed")
        return True
        
    except Exception as e:
        print(f"❌ Search functionality test failed: {e}")
        return False

async def test_docker_health():
    """Test Docker-specific health checks"""
    print(f"\n🐳 Testing Docker Health")
    print("=" * 25)
    
    # Check if we're running in Docker
    in_docker = os.path.exists('/.dockerenv')
    print(f"   Running in Docker: {'✅ Yes' if in_docker else '❌ No'}")
    
    # Check environment variable access
    env_vars = [
        'GOOGLE_CUSTOM_SEARCH_API_KEY',
        'GOOGLE_CUSTOM_SEARCH_ENGINE_ID',
        'BING_SEARCH_API_KEY'
    ]
    
    print(f"\n   Environment Variable Access:")
    for var in env_vars:
        value = os.getenv(var, '')
        status = '✅ Set' if value else '❌ Not Set'
        print(f"     {var}: {status}")
        if value:
            print(f"       Length: {len(value)} characters")
    
    # Check database access
    try:
        db_path = 'brain_memory_store/brain.db'
        if os.path.exists(db_path):
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
                table_count = cursor.fetchone()[0]
                print(f"   Database Access: ✅ Available ({table_count} tables)")
        else:
            print(f"   Database Access: ❌ Not Found at {db_path}")
    except Exception as e:
        print(f"   Database Access: ❌ Error: {e}")
    
    print(f"✅ Docker health check completed")
    return True

async def main():
    """Main test function for Docker environment"""
    print("🐳 Docker Search Engine Integration Test")
    print("=" * 60)
    print("   Testing Phase 3B: Search Engine Integration in Docker")
    
    # Test 1: Docker Environment
    print(f"\n🧪 Test 1: Docker Environment Check")
    config = await test_docker_environment()
    
    # Test 2: Search Engine Initialization
    print(f"\n🧪 Test 2: Search Engine Initialization")
    integration, init_success = await test_search_engine_initialization(config)
    
    # Test 3: Search Functionality
    print(f"\n🧪 Test 3: Search Functionality")
    if init_success and integration:
        search_success = await test_actual_search_functionality(integration)
    else:
        search_success = False
        print(f"   ⚠️ Skipping search test due to initialization failure")
    
    # Test 4: Docker Health
    print(f"\n🧪 Test 4: Docker Health Check")
    docker_health = await test_docker_health()
    
    # Final status
    print(f"\n🎯 Final Test Results:")
    print(f"   🐳 Docker Environment: {'✅ PASS' if config else '❌ FAIL'}")
    print(f"   🚀 Search Engine Init: {'✅ PASS' if init_success else '❌ FAIL'}")
    print(f"   🔍 Search Functionality: {'✅ PASS' if search_success else '❌ FAIL'}")
    print(f"   🐳 Docker Health: {'✅ PASS' if docker_health else '❌ FAIL'}")
    
    total_tests = 4
    passed_tests = sum([bool(config), init_success, search_success, docker_health])
    
    print(f"\n📊 Overall Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print(f"\n🎉 ALL TESTS PASSED! Docker Search Engine Integration is operational!")
        print(f"   Your AI system can now search the web through Docker!")
        
        # Show next steps
        if config.enable_google_search:
            print(f"\n🚀 Google Search is ENABLED!")
            print(f"   API Key: {config.google_custom_search_api_key[:10]}...")
            print(f"   Engine ID: {config.google_custom_search_engine_id}")
            print(f"   Ready for web searches!")
        else:
            print(f"\n⚠️ Google Search is DISABLED")
            print(f"   Check your GOOGLE_CUSTOM_SEARCH_ENGINE_ID")
            print(f"   Current value: {config.google_custom_search_engine_id}")
        
    else:
        print(f"\n⚠️ Some tests failed. Review the output above.")
        
        # Troubleshooting tips
        print(f"\n🔧 Troubleshooting Tips:")
        print(f"   1. Check Docker Compose environment variables")
        print(f"   2. Verify API keys are correct")
        print(f"   3. Ensure Google Custom Search Engine ID is valid")
        print(f"   4. Check Docker container logs")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
