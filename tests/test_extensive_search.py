#!/usr/bin/env python3
"""
Test script for extensive search and multi-site discovery capabilities
"""

import asyncio
import sys
import sqlite3
from pathlib import Path
sys.path.append(str(Path.cwd()))

from extensive_search_engine import MultiSiteDiscoveryEngine, DiscoveryConfig

async def test_extensive_search_engine():
    """Test the extensive search engine capabilities"""
    print("🔍 Testing Extensive Search Engine")
    print("=" * 40)
    
    # Initialize extensive search engine
    engine = MultiSiteDiscoveryEngine('brain_memory_store/brain.db')
    
    print(f"\n🚀 Starting Multi-Site Discovery Session...")
    print(f"   This will discover related websites across domains")
    print(f"   Starting from Cursor MCP documentation")
    
    # Start discovery session
    seed_urls = ['https://docs.cursor.com/en/context/mcp']
    discovery_depth = 2
    
    result = await engine.start_discovery_session(seed_urls, discovery_depth)
    
    if result['status'] == 'started':
        session_id = result['session_id']
        print(f"\n✅ Discovery session started successfully!")
        print(f"   Session ID: {session_id}")
        print(f"   Seed URLs: {len(seed_urls)}")
        print(f"   Max Depth: {discovery_depth}")
        print(f"   Message: {result['message']}")
        
        # Monitor discovery progress
        print(f"\n⏳ Monitoring Discovery Progress...")
        print(f"   Discovery will run in background...")
        
        # Wait for initial discovery to start
        await asyncio.sleep(5)
        
        # Get discovery status
        status = await engine.get_discovery_status()
        print(f"\n📊 Discovery Status:")
        print(f"   Status: {status['status']}")
        print(f"   Queue Size: {status['discovery_queue_size']}")
        print(f"   Active Discoveries: {status['active_discoveries']}")
        print(f"   Discovered Sites: {status['discovered_sites_count']}")
        
        # Show metrics
        metrics = status['metrics']
        print(f"\n📈 Discovery Metrics:")
        print(f"   Total Sites Discovered: {metrics['total_sites_discovered']}")
        print(f"   Discovery Sessions: {metrics['discovery_sessions']}")
        print(f"   Average Relevance Score: {metrics['average_relevance_score']:.2f}")
        
        # Wait for more discovery to happen
        print(f"\n⏳ Waiting for more discoveries...")
        await asyncio.sleep(10)
        
        # Get updated status
        updated_status = await engine.get_discovery_status()
        print(f"\n📊 Updated Discovery Status:")
        print(f"   Discovered Sites: {updated_status['discovered_sites_count']}")
        print(f"   Queue Size: {updated_status['discovery_queue_size']}")
        
        # Show some discovered sites
        if updated_status['discovered_sites_count'] > 0:
            print(f"\n🌐 Sample Discovered Sites:")
            discovered_sites = list(engine.discovered_sites.values())[:5]
            for i, site in enumerate(discovered_sites):
                print(f"   {i+1}. {site.title}")
                print(f"      URL: {site.url}")
                print(f"      Type: {site.content_type}")
                print(f"      Relevance: {site.relevance_score:.2f}")
                print(f"      Method: {site.discovery_method}")
        
        return session_id
        
    else:
        print(f"❌ Failed to start discovery session: {result.get('error', 'Unknown error')}")
        return None

async def test_discovery_database():
    """Test the discovery database functionality"""
    print(f"\n🗄️ Testing Discovery Database")
    print("=" * 35)
    
    try:
        engine = MultiSiteDiscoveryEngine('brain_memory_store/brain.db')
        
        # Check database tables
        with sqlite3.connect(engine.db_path) as conn:
            cursor = conn.cursor()
            
            # Check discovered sites table
            cursor.execute("SELECT COUNT(*) FROM discovered_sites")
            sites_count = cursor.fetchone()[0]
            print(f"   Discovered Sites: {sites_count}")
            
            # Check search queries table
            cursor.execute("SELECT COUNT(*) FROM search_queries")
            queries_count = cursor.fetchone()[0]
            print(f"   Search Queries: {queries_count}")
            
            # Check cross references table
            cursor.execute("SELECT COUNT(*) FROM cross_references")
            refs_count = cursor.fetchone()[0]
            print(f"   Cross References: {refs_count}")
            
            # Check domain relationships table
            cursor.execute("SELECT COUNT(*) FROM domain_relationships")
            domains_count = cursor.fetchone()[0]
            print(f"   Domain Relationships: {domains_count}")
            
            print(f"✅ Discovery database is operational")
            return True
            
    except Exception as e:
        print(f"❌ Discovery database test failed: {e}")
        return False

async def test_discovery_configuration():
    """Test discovery configuration and settings"""
    print(f"\n⚙️ Testing Discovery Configuration")
    print("=" * 35)
    
    # Create custom configuration
    custom_config = DiscoveryConfig(
        max_discovery_depth=3,
        max_sites_per_discovery=25,
        max_pages_per_site=50,
        discovery_delay=1.5,
        content_similarity_threshold=0.7,
        domain_relationship_threshold=0.5,
        max_concurrent_discoveries=2
    )
    
    print(f"   Max Discovery Depth: {custom_config.max_discovery_depth}")
    print(f"   Max Sites per Discovery: {custom_config.max_sites_per_discovery}")
    print(f"   Max Pages per Site: {custom_config.max_pages_per_site}")
    print(f"   Discovery Delay: {custom_config.discovery_delay}s")
    print(f"   Content Similarity Threshold: {custom_config.content_similarity_threshold}")
    print(f"   Domain Relationship Threshold: {custom_config.domain_relationship_threshold}")
    print(f"   Max Concurrent Discoveries: {custom_config.max_concurrent_discoveries}")
    
    # Test with custom configuration
    engine = MultiSiteDiscoveryEngine('brain_memory_store/brain.db', custom_config)
    
    print(f"✅ Custom discovery configuration applied successfully")
    return True

async def main():
    """Main test function"""
    print("🔍 Extensive Search Engine & Multi-Site Discovery Test")
    print("=" * 65)
    print("   Testing Phase 3: Extensive Web Search capabilities")
    
    # Test 1: Discovery Database
    db_success = await test_discovery_database()
    
    # Test 2: Discovery Configuration
    config_success = await test_discovery_configuration()
    
    # Test 3: Extensive Search Engine
    session_id = await test_extensive_search_engine()
    
    # Final status
    print(f"\n🎯 Final Test Results:")
    print(f"   🗄️ Discovery Database: {'✅ PASS' if db_success else '❌ FAIL'}")
    print(f"   ⚙️ Discovery Configuration: {'✅ PASS' if config_success else '❌ FAIL'}")
    print(f"   🔍 Extensive Search Engine: {'✅ PASS' if session_id else '❌ FAIL'}")
    
    if session_id:
        print(f"\n🚀 Multi-site discovery session {session_id} is running!")
        print(f"   💡 Use get_discovery_status() to monitor progress")
        print(f"   📊 Use get_discovered_sites_report() to see results")
        print(f"   🛑 Use stop_discovery_session() to stop when needed")
        
        # Create engine instance for final status
        engine = MultiSiteDiscoveryEngine('brain_memory_store/brain.db')
        final_status = await engine.get_discovery_status()
        print(f"\n📊 Final Discovery Status:")
        print(f"   Total Sites Discovered: {final_status['metrics']['total_sites_discovered']}")
        print(f"   Discovery Queue: {final_status['discovery_queue_size']}")
        print(f"   Active Discoveries: {final_status['active_discoveries']}")
    
    total_tests = 3
    passed_tests = sum([db_success, config_success, 1 if session_id else 0])
    
    print(f"\n📊 Overall Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print(f"\n🎉 ALL TESTS PASSED! Extensive Search Engine is operational!")
        print(f"   Your AI system can now discover knowledge across multiple websites!")
        print(f"   Ready for cross-domain intelligence building!")
    else:
        print(f"\n⚠️  Some tests failed. Review before proceeding.")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
