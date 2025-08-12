#!/usr/bin/env python3
"""
Debug script to test learning bit extraction process
"""

import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

from web_crawler_engine import WebCrawler, ContentAnalyzer

async def debug_learning_bits():
    """Debug the learning bit extraction process"""
    print("🔍 Debugging Learning Bit Extraction")
    print("=" * 50)
    
    # Test content analysis directly
    analyzer = ContentAnalyzer()
    
    # Test content from our crawled page
    test_content = """
Connect external tools and data sources to Cursor using MCP
stdout
or serve an HTTP endpoint - Python, JavaScript, Go, etc.
| Transport | Execution environment | Deployment | Users | Input | Auth |
|---|---|---|---|---|---|
stdio | Local | Cursor manages | Single user | Shell command | Manual |
SSE | Local/Remote | Deploy as server | Multiple users | URL to an SSE endpoint | OAuth |
Streamable HTTP | Local/Remote | Deploy as server | Multiple users | URL to an HTTP endpoint | OAuth |
"""
    
    print('Testing content analysis...')
    analysis = analyzer.analyze_content(test_content, 'https://docs.cursor.com/en/context/mcp')
    print(f'Analysis result: {analysis}')
    
    # Test content chunking
    crawler = WebCrawler('brain_memory_store/brain.db')
    chunks = crawler._split_content_into_chunks(test_content)
    print(f'\nContent chunks: {len(chunks)}')
    for i, chunk in enumerate(chunks):
        print(f'Chunk {i+1}: {chunk[:100]}...')
    
    # Test learning bit extraction
    print('\nTesting learning bit extraction...')
    learning_bits = await crawler._extract_learning_bits(test_content, 'https://docs.cursor.com/en/context/mcp', 1)
    print(f'Learning bits extracted: {len(learning_bits)}')
    
    if learning_bits:
        for i, bit in enumerate(learning_bits):
            print(f'\nLearning Bit {i+1}:')
            print(f'  Type: {bit.content_type}')
            print(f'  Category: {bit.category}')
            print(f'  Subcategory: {bit.subcategory}')
            print(f'  Content: {bit.content[:100]}...')
            print(f'  Importance: {bit.importance_score}')
            print(f'  Confidence: {bit.confidence_score}')
            print(f'  Tags: {bit.tags}')
    
    return learning_bits

if __name__ == "__main__":
    import asyncio
    result = asyncio.run(debug_learning_bits())
    print(f"\n🎯 Debug complete. Found {len(result) if result else 0} learning bits.")
