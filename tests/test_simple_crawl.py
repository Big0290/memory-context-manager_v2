#!/usr/bin/env python3
"""
Simple test for web crawler text extraction
"""

import asyncio
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from web_crawler_engine import WebCrawler

async def test_simple_crawl():
    """Test crawling a simple HTML page"""
    print("🧪 Testing Simple Web Crawl")
    print("=" * 40)
    
    try:
        # Initialize crawler
        crawler = WebCrawler('brain_memory_store/brain.db')
        
        # Test with a simple HTML page
        test_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Page</title>
        </head>
        <body>
            <h1>Python Programming</h1>
            <p>This is a test page about Python programming concepts.</p>
            <p>Python is a high-level programming language that emphasizes code readability.</p>
            <h2>Key Concepts</h2>
            <ul>
                <li>Variables and data types</li>
                <li>Functions and methods</li>
                <li>Classes and objects</li>
                <li>Modules and packages</li>
            </ul>
            <h2>Example Code</h2>
            <pre><code>
def hello_world():
    print("Hello, World!")
    
class Calculator:
    def add(self, a, b):
        return a + b
            </code></pre>
        </body>
        </html>
        """
        
        print("Testing text extraction from HTML...")
        
        # Test text extraction
        extracted_text = crawler._extract_text_content(test_html)
        print(f"Extracted text length: {len(extracted_text)}")
        print(f"First 200 chars: {extracted_text[:200]}...")
        
        # Test title extraction
        title = crawler._extract_title(test_html)
        print(f"Extracted title: {title}")
        
        # Test learning bit extraction
        print("\nTesting learning bit extraction...")
        learning_bits = await crawler._extract_learning_bits(extracted_text, "http://test.com", 1)
        print(f"Found {len(learning_bits)} learning bits")
        
        for i, bit in enumerate(learning_bits):
            print(f"\n{i+1}. Type: {bit.content_type}")
            print(f"   Category: {bit.category}")
            print(f"   Subcategory: {bit.subcategory}")
            print(f"   Content: {bit.content[:100]}...")
            print(f"   Importance: {bit.importance_score:.2f}")
            print(f"   Confidence: {bit.confidence_score:.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_simple_crawl())
    if success:
        print("\n✅ Simple crawl test completed successfully!")
    else:
        print("\n❌ Simple crawl test failed!")
