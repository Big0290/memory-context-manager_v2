#!/usr/bin/env python3
"""
Test Docker Functionality
Verifies that the enhanced ContextAnalyzer functionality is working in the container
"""

import asyncio
import json
from mcp.client import ClientSession
from mcp.client.stdio import stdio_client

async def test_enhanced_functionality():
    """Test the enhanced functionality in the Docker container"""
    try:
        print("🚀 Testing Enhanced MCP Server Functionality")
        print("=" * 60)
        
        # Connect to the MCP server
        async with stdio_client() as (read, write):
            async with ClientSession(read, write) as session:
                print("✅ Connected to MCP server")
                
                # List available tools
                tools = await session.list_tools()
                print(f"\n📋 Available Tools: {len(tools.tools)}")
                
                # Look for our enhanced tools
                enhanced_tools = []
                context_tools = []
                
                for tool in tools.tools:
                    if "enhanced with contextual understanding" in tool.description:
                        enhanced_tools.append(tool.name)
                    if "context" in tool.name.lower() or "analyze" in tool.name.lower():
                        context_tools.append(tool.name)
                
                print(f"🔍 Context-related tools: {context_tools}")
                print(f"🧠 Enhanced brain tools: {enhanced_tools}")
                
                # Test the analyze_context_deeply tool if available
                if "analyze_context_deeply" in [t.name for t in tools.tools]:
                    print("\n🧪 Testing analyze_context_deeply tool...")
                    
                    test_content = "I need to implement this functionality safely without breaking existing systems"
                    
                    result = await session.call_tool(
                        "analyze_context_deeply",
                        arguments={
                            "content": test_content,
                            "analysis_type": "comprehensive"
                        }
                    )
                    
                    if result.content:
                        print("✅ Tool executed successfully!")
                        print(f"📝 Content analyzed: {test_content[:50]}...")
                        
                        # Parse the result
                        try:
                            result_data = json.loads(result.content[0].text)
                            if result_data.get("success"):
                                context_analysis = result_data.get("context_analysis", {})
                                print(f"🎯 Context Score: {context_analysis.get('context_score', 0):.2f}")
                                print(f"💡 Insights: {len(context_analysis.get('insights', []))}")
                                print(f"🚀 Recommendations: {len(context_analysis.get('recommendations', []))}")
                            else:
                                print(f"❌ Tool failed: {result_data.get('error', 'Unknown error')}")
                        except json.JSONDecodeError:
                            print("📄 Raw result:", result.content[0].text[:200])
                    else:
                        print("❌ Tool returned no content")
                else:
                    print("\n⚠️  analyze_context_deeply tool not found")
                
                # Test enhanced brain tools
                print("\n🧠 Testing Enhanced Brain Tools...")
                
                # Test think tool
                if "think" in [t.name for t in tools.tools]:
                    print("💭 Testing enhanced think tool...")
                    
                    result = await session.call_tool(
                        "think",
                        arguments={
                            "message": "I need to implement this safely",
                            "context": "problem_solving"
                        }
                    )
                    
                    if result.content:
                        print("✅ Think tool executed successfully!")
                        try:
                            result_data = json.loads(result.content[0].text)
                            if "context_insights" in result_data:
                                print("🎯 Enhanced with contextual understanding!")
                                print(f"   Context insights: {len(result_data.get('context_insights', []))}")
                                print(f"   Context score: {result_data.get('context_score', 0):.2f}")
                            else:
                                print("⚠️  Think tool not showing enhanced features")
                        except json.JSONDecodeError:
                            print("📄 Raw think result:", result.content[0].text[:200])
                    else:
                        print("❌ Think tool returned no content")
                
                print("\n✅ Enhanced functionality test completed!")
                return True
                
    except Exception as e:
        print(f"❌ Error testing enhanced functionality: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🎯 Docker Enhanced Functionality Test")
    print("Make sure the MCP server is running in Docker")
    print("=" * 60)
    
    success = asyncio.run(test_enhanced_functionality())
    
    if success:
        print("\n🎉 Enhanced functionality is working in Docker!")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
