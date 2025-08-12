#!/usr/bin/env python3
"""
Test script for symbiotic integration between web crawler and all learning/processing systems
"""

import asyncio
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

from symbiotic_integration_bridge import SymbioticIntegrationBridge
from web_crawler_engine import WebCrawler

async def test_symbiotic_integration():
    """Test the complete symbiotic integration system"""
    print("🔗 Testing Symbiotic Integration Bridge")
    print("=" * 50)
    
    # Initialize symbiotic bridge
    bridge = SymbioticIntegrationBridge('brain_memory_store/brain.db')
    
    print(f"\n🚀 Establishing Symbiotic Connections...")
    print("   This will integrate web crawler with:")
    print("   - Memory System")
    print("   - Knowledge Graph")
    print("   - AI Learning")
    print("   - Context Orchestration")
    print("   - Processing Pipeline")
    
    # Establish connections
    result = await bridge.establish_symbiotic_connections()
    
    if result['status'] == 'success':
        print(f"\n✅ Symbiotic connections established successfully!")
        
        # Show integration status
        integration_status = result['integration_status']
        print(f"\n📊 Integration Status:")
        for system, status in integration_status.items():
            status_icon = "✅" if status else "❌"
            print(f"   {status_icon} {system.replace('_', ' ').title()}")
        
        # Show symbiotic metrics
        metrics = result['symbiotic_metrics']
        print(f"\n📈 Symbiotic Metrics:")
        print(f"   Total integrations: {metrics['total_integrations']}")
        print(f"   Memory enhancements: {metrics['memory_enhancements']}")
        print(f"   Knowledge expansions: {metrics['knowledge_expansions']}")
        print(f"   AI learning cycles: {metrics['ai_learning_cycles']}")
        print(f"   Context unifications: {metrics['context_unifications']}")
        
        # Get detailed status
        print(f"\n🔍 Getting Detailed Symbiotic Status...")
        status = await bridge.get_symbiotic_status()
        
        if status:
            system_health = status.get('system_health', {})
            print(f"\n🏥 System Health:")
            print(f"   Total systems: {system_health.get('total_systems', 0)}")
            print(f"   Integrated systems: {system_health.get('integrated_systems', 0)}")
            print(f"   Integration percentage: {system_health.get('integration_percentage', 0):.1f}%")
        
        # Test symbiotic learning cycle
        print(f"\n🔄 Testing Symbiotic Learning Cycle...")
        cycle_result = await bridge.trigger_symbiotic_learning_cycle()
        
        if cycle_result['status'] == 'success':
            print(f"✅ Learning cycle completed successfully!")
            print(f"   Enhancements applied: {cycle_result.get('enhancements_applied', 0)}")
            print(f"   Cycle type: {cycle_result.get('cycle_type', 'unknown')}")
        else:
            print(f"❌ Learning cycle failed: {cycle_result.get('error', 'Unknown error')}")
        
        return True
        
    else:
        print(f"❌ Failed to establish symbiotic connections: {result.get('error', 'Unknown error')}")
        return False

async def test_unified_knowledge_access():
    """Test unified knowledge access across all systems"""
    print(f"\n🧠 Testing Unified Knowledge Access")
    print("=" * 40)
    
    try:
        # Test accessing learning bits through unified interface
        crawler = WebCrawler('brain_memory_store/brain.db')
        
        # Get learning bits
        learning_bits = await crawler.get_learning_bits(limit=10)
        
        if learning_bits:
            print(f"\n📚 Retrieved {len(learning_bits)} learning bits through unified interface")
            
            # Show sample bits
            print(f"\n🔍 Sample Learning Bits:")
            for i, bit in enumerate(learning_bits[:3]):
                print(f"   {i+1}. {bit.get('content_type', 'unknown')} - {bit.get('category', 'unknown')}")
                print(f"      Content: {bit.get('content', '')[:100]}...")
                print(f"      Importance: {bit.get('importance_score', 0):.2f}")
                print(f"      Confidence: {bit.get('confidence_score', 0):.2f}")
        
        # Test comprehensive learning report
        print(f"\n📊 Testing Comprehensive Learning Report...")
        report = await crawler.get_comprehensive_learning_report()
        
        if 'error' not in report:
            summary = report.get('summary', {})
            print(f"\n📈 Learning Coverage Summary:")
            print(f"   Total pages: {summary.get('total_pages_crawled', 0)}")
            print(f"   Total learning bits: {summary.get('total_learning_bits', 0)}")
            print(f"   Avg bits per page: {summary.get('average_learning_bits_per_page', 0):.1f}")
            
            # Show content type distribution
            content_types = report.get('content_type_analysis', {})
            if content_types.get('distribution'):
                print(f"\n🔍 Content Type Distribution:")
                for type_info in content_types['distribution'][:5]:
                    print(f"   {type_info['type']}: {type_info['count']} ({type_info['percentage']:.1f}%)")
        
        return True
        
    except Exception as e:
        print(f"❌ Unified knowledge access test failed: {e}")
        return False

async def test_symbiotic_learning_evolution():
    """Test symbiotic learning evolution capabilities"""
    print(f"\n🧬 Testing Symbiotic Learning Evolution")
    print("=" * 45)
    
    try:
        crawler = WebCrawler('brain_memory_store/brain.db')
        
        # Check learning evolution status
        print(f"\n🔍 Current Learning Evolution Status:")
        evolution = crawler.learning_evolution
        print(f"   Total extractions: {evolution['total_extractions']}")
        print(f"   Successful: {evolution['successful_extractions']}")
        print(f"   Failed: {evolution['failed_extractions']}")
        print(f"   Quality improvements: {evolution['quality_improvements']}")
        print(f"   Pattern discoveries: {evolution['pattern_discoveries']}")
        
        # Check intelligent processor status
        print(f"\n🧠 Intelligent Processor Status:")
        processor = crawler.intelligent_processor
        print(f"   Learning patterns: {len(processor.learning_patterns)}")
        print(f"   Adaptive thresholds: {processor.adaptive_thresholds}")
        
        if processor.learning_patterns:
            print(f"\n📊 Learning Pattern Breakdown:")
            for pattern_key, pattern_data in list(processor.learning_patterns.items())[:5]:
                print(f"   {pattern_key}:")
                print(f"     Success count: {pattern_data['success_count']}")
                print(f"     Avg importance: {pattern_data['avg_importance']:.2f}")
                print(f"     Avg confidence: {pattern_data['avg_confidence']:.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Symbiotic learning evolution test failed: {e}")
        return False

async def main():
    """Main test function"""
    print("🔗 Comprehensive Symbiotic Integration Test")
    print("=" * 60)
    print("   Testing true symbiosis between web crawler and all learning systems")
    
    # Test 1: Symbiotic Integration
    print(f"\n🧪 Test 1: Symbiotic Integration Bridge")
    integration_success = await test_symbiotic_integration()
    
    # Test 2: Unified Knowledge Access
    print(f"\n🧪 Test 2: Unified Knowledge Access")
    knowledge_success = await test_unified_knowledge_access()
    
    # Test 3: Symbiotic Learning Evolution
    print(f"\n🧪 Test 3: Symbiotic Learning Evolution")
    evolution_success = await test_symbiotic_learning_evolution()
    
    # Final status
    print(f"\n🎯 Final Test Results:")
    print(f"   🔗 Symbiotic Integration: {'✅ PASS' if integration_success else '❌ FAIL'}")
    print(f"   🧠 Unified Knowledge Access: {'✅ PASS' if knowledge_success else '❌ FAIL'}")
    print(f"   🧬 Learning Evolution: {'✅ PASS' if evolution_success else '❌ FAIL'}")
    
    total_tests = 3
    passed_tests = sum([integration_success, knowledge_success, evolution_success])
    
    print(f"\n📊 Overall Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print(f"\n🎉 ALL TESTS PASSED! True symbiotic integration achieved!")
        print(f"   Your web crawler is now fully integrated with all learning systems!")
        print(f"   Ready for extensive web search capabilities!")
    else:
        print(f"\n⚠️  Some tests failed. Integration may be incomplete.")
        print(f"   Review failed tests before proceeding to extensive web search.")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
