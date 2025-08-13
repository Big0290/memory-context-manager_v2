#!/usr/bin/env python3
"""
Test script for enhanced web crawler with multi-depth navigation
"""

import asyncio
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

from web_crawler_engine import WebCrawler

async def test_enhanced_crawler():
    """Test the enhanced web crawler capabilities"""
    print("🧪 Testing Enhanced Web Crawler with Multi-Depth Navigation")
    print("=" * 65)
    
    # Initialize enhanced crawler
    crawler = WebCrawler('brain_memory_store/brain.db')
    
    # Test enhanced crawling with depth navigation
    print("\n🚀 Starting enhanced crawl of Cursor MCP documentation...")
    print("   Target: Multi-depth crawling with intelligent link prioritization")
    
    result = await crawler.crawl_website(
        start_url='https://docs.cursor.com/en/context/mcp',
        max_pages=10,  # Increased page limit
        max_depth=3    # Multi-depth crawling
    )
    
    print(f"\n📊 Enhanced Crawl Results:")
    print(f"   Pages crawled: {result.get('total_pages', 0)}")
    print(f"   Learning bits: {result.get('total_learning_bits', 0)}")
    print(f"   Max depth reached: {result.get('crawl_depth_reached', 0)}")
    print(f"   Duration: {result.get('duration', 0):.1f}s")
    
    if result.get('domains_crawled'):
        print(f"   Domains: {', '.join(result['domains_crawled'])}")
    
    if result.get('subjects_discovered'):
        print(f"   Subjects discovered: {len(result['subjects_discovered'])}")
        print(f"   Subject types: {', '.join(result['subjects_discovered'][:5])}")
    
    if result.get('categories_found'):
        print(f"   Categories found: {len(result['categories_found'])}")
        print(f"   Sample categories: {', '.join(result['categories_found'][:5])}")
    
    # Generate comprehensive learning report
    print(f"\n📈 Generating Comprehensive Learning Report...")
    report = await crawler.get_comprehensive_learning_report()
    
    if 'error' not in report:
        summary = report.get('summary', {})
        print(f"\n📚 Learning Coverage Summary:")
        print(f"   Total pages: {summary.get('total_pages_crawled', 0)}")
        print(f"   Total learning bits: {summary.get('total_learning_bits', 0)}")
        print(f"   Avg bits per page: {summary.get('average_learning_bits_per_page', 0):.1f}")
        
        # Content type analysis
        content_types = report.get('content_type_analysis', {})
        if content_types.get('distribution'):
            print(f"\n🔍 Content Type Distribution:")
            for type_info in content_types['distribution'][:5]:  # Top 5
                print(f"   {type_info['type']}: {type_info['count']} ({type_info['percentage']:.1f}%)")
        
        # Category analysis
        categories = report.get('category_analysis', {})
        if categories.get('distribution'):
            print(f"\n📂 Category Distribution:")
            for cat_info in categories['distribution'][:5]:  # Top 5
                print(f"   {cat_info['category']}: {cat_info['count']} ({cat_info['percentage']:.1f}%)")
        
        # Top learning bits
        top_bits = report.get('top_learning_bits', [])
        if top_bits:
            print(f"\n⭐ Top Learning Bits by Importance:")
            for i, bit in enumerate(top_bits[:3]):  # Top 3
                print(f"   {i+1}. {bit['content_type']} - {bit['category']} (Score: {bit['importance_score']:.2f})")
                print(f"      Content: {bit['content'][:100]}...")
        
        # Domain coverage
        domains = report.get('domain_coverage', {})
        if domains.get('domains'):
            print(f"\n🌐 Domain Coverage:")
            for domain_info in domains['domains']:
                print(f"   {domain_info['domain']}: {domain_info['pages_crawled']} pages, {domain_info['learning_bits']} bits")
    
    else:
        print(f"❌ Failed to generate report: {report['error']}")
    
    return result, report

if __name__ == "__main__":
    print("Starting enhanced web crawler test...")
    result, report = asyncio.run(test_enhanced_crawler())
    print(f"\n🎯 Enhanced crawler test complete!")
    print(f"   Final status: {result.get('total_pages', 0)} pages, {result.get('total_learning_bits', 0)} learning bits")
