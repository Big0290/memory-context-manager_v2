#!/usr/bin/env python3
"""
Test script for enhanced learning process and background operation
"""

import asyncio
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

from web_crawler_engine import WebCrawler, BackgroundCrawlerManager

async def test_enhanced_learning():
    """Test the enhanced learning process with intelligent processor"""
    print("🧠 Testing Enhanced Learning Process")
    print("=" * 45)
    
    # Initialize enhanced crawler
    crawler = WebCrawler('brain_memory_store/brain.db')
    
    print(f"\n🔍 Current Learning Evolution Status:")
    evolution = crawler.learning_evolution
    print(f"  Total extractions: {evolution['total_extractions']}")
    print(f"  Successful: {evolution['successful_extractions']}")
    print(f"  Failed: {evolution['failed_extractions']}")
    print(f"  Quality improvements: {evolution['quality_improvements']}")
    print(f"  Pattern discoveries: {evolution['pattern_discoveries']}")
    
    print(f"\n🧠 Intelligent Processor Status:")
    processor = crawler.intelligent_processor
    print(f"  Learning patterns: {len(processor.learning_patterns)}")
    print(f"  Adaptive thresholds: {processor.adaptive_thresholds}")
    
    if processor.learning_patterns:
        print(f"\n📊 Learning Pattern Breakdown:")
        for pattern_key, pattern_data in list(processor.learning_patterns.items())[:5]:
            print(f"  {pattern_key}:")
            print(f"    Success count: {pattern_data['success_count']}")
            print(f"    Avg importance: {pattern_data['avg_importance']:.2f}")
            print(f"    Avg confidence: {pattern_data['avg_confidence']:.2f}")
    
    return crawler

async def test_background_operation():
    """Test the background crawler operation"""
    print(f"\n🚀 Testing Background Crawler Operation")
    print("=" * 50)
    
    # Initialize background manager
    background_manager = BackgroundCrawlerManager('brain_memory_store/brain.db')
    
    print(f"\n📊 Background Manager Status:")
    status = background_manager.get_crawl_status()
    print(f"  Active crawls: {status['active_crawls']}")
    print(f"  Queued jobs: {status['queued_jobs']}")
    print(f"  Completed crawls: {status['completed_crawls']}")
    print(f"  Max concurrent: {status['max_concurrent']}")
    
    # Test starting a background crawl
    print(f"\n🎯 Starting Background Crawl Job...")
    job_id = "test_enhanced_learning_001"
    config = {
        'max_pages': 5,
        'max_depth': 2,
        'crawl_delay': 0.5,
        'priority': 'high'
    }
    
    result = await background_manager.start_background_crawl(
        job_id=job_id,
        start_url='https://docs.cursor.com/en/context/mcp',
        config=config
    )
    
    print(f"  Job ID: {job_id}")
    print(f"  Status: {result['status']}")
    print(f"  Message: {result['message']}")
    
    if result['status'] == 'started':
        print(f"  Estimated duration: {result['estimated_duration']}")
    elif result['status'] == 'queued':
        print(f"  Estimated start: {result['estimated_start']}")
    
    # Wait a moment and check status
    print(f"\n⏳ Waiting 3 seconds to check progress...")
    await asyncio.sleep(3)
    
    status = background_manager.get_crawl_status(job_id)
    print(f"  Job status: {status['status']}")
    if status['status'] == 'active':
        print(f"  Start time: {status['details']['start_time']}")
        print(f"  Configuration: {status['details']['config']}")
    
    # Get overall status
    overall_status = background_manager.get_crawl_status()
    print(f"\n📊 Updated Background Manager Status:")
    print(f"  Active crawls: {overall_status['active_crawls']}")
    print(f"  Queued jobs: {overall_status['queued_jobs']}")
    
    return background_manager, job_id

async def test_learning_evolution_report():
    """Test the learning evolution reporting"""
    print(f"\n📈 Testing Learning Evolution Reporting")
    print("=" * 45)
    
    crawler = WebCrawler('brain_memory_store/brain.db')
    
    # Get comprehensive learning report
    print(f"\n📊 Generating Learning Evolution Report...")
    report = await crawler.get_comprehensive_learning_report()
    
    if 'error' not in report:
        summary = report.get('summary', {})
        print(f"\n📚 Learning Coverage Summary:")
        print(f"  Total pages: {summary.get('total_pages_crawled', 0)}")
        print(f"  Total learning bits: {summary.get('total_learning_bits', 0)}")
        print(f"  Avg bits per page: {summary.get('average_learning_bits_per_page', 0):.1f}")
        
        # Content type analysis
        content_types = report.get('content_type_analysis', {})
        if content_types.get('distribution'):
            print(f"\n🔍 Content Type Distribution:")
            for type_info in content_types['distribution'][:5]:
                print(f"  {type_info['type']}: {type_info['count']} ({type_info['percentage']:.1f}%)")
        
        # Category analysis
        categories = report.get('category_analysis', {})
        if categories.get('distribution'):
            print(f"\n📂 Category Distribution:")
            for cat_info in categories['distribution'][:5]:
                print(f"  {cat_info['category']}: {cat_info['count']} ({cat_info['percentage']:.1f}%)")
        
        # Top learning bits
        top_bits = report.get('top_learning_bits', [])
        if top_bits:
            print(f"\n⭐ Top Learning Bits by Importance:")
            for i, bit in enumerate(top_bits[:3]):
                print(f"  {i+1}. {bit['content_type']} - {bit['category']} (Score: {bit['importance_score']:.2f})")
                print(f"      Content: {bit['content'][:80]}...")
    
    else:
        print(f"❌ Failed to generate report: {report['error']}")
    
    return report

async def main():
    """Main test function"""
    print("🧪 Enhanced Learning Process & Background Operation Test")
    print("=" * 65)
    
    # Test 1: Enhanced Learning Process
    crawler = await test_enhanced_learning()
    
    # Test 2: Background Operation
    background_manager, job_id = await test_background_operation()
    
    # Test 3: Learning Evolution Report
    report = await test_learning_evolution_report()
    
    # Final status check
    print(f"\n🎯 Final Status Check:")
    final_status = background_manager.get_crawl_status(job_id)
    print(f"  Background job {job_id}: {final_status['status']}")
    
    if final_status['status'] == 'active':
        print(f"  ⚠️  Job still running - you can continue using the system!")
        print(f"  💡 Use get_background_crawl_status() to monitor progress")
        print(f"  🛑 Use stop_background_crawl() to stop when needed")
    
    print(f"\n🎉 Enhanced learning and background operation test complete!")
    print(f"   The system is now ready for autonomous operation!")

if __name__ == "__main__":
    asyncio.run(main())
