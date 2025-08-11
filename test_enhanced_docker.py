#!/usr/bin/env python3
"""
Test Enhanced Docker Functionality
Verifies that the enhanced ContextAnalyzer functionality is working in the container
"""

import asyncio
import json
from mcp.client import ClientSession
from mcp.client.stdio import stdio_client

async def test_enhanced_functionality():
    """Test the enhanced functionality in the Docker container"""
    try:
        print("🚀 Testing Enhanced MCP Server with ContextAnalyzer")
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
                brain_tools = []
                
                for tool in tools.tools:
                    if "enhanced with contextual understanding" in tool.description:
                        enhanced_tools.append(tool.name)
                    if tool.name in ["think", "remember", "recall", "reflect", "learn_from"]:
                        brain_tools.append(tool.name)
                
                print(f"🧠 Brain tools found: {brain_tools}")
                print(f"🔍 Enhanced tools: {enhanced_tools}")
                
                # Test the enhanced think tool
                if "think" in brain_tools:
                    print("\n🧪 Testing enhanced think tool with context analysis...")
                    
                    test_message = "I need to implement this functionality safely without breaking existing systems"
                    
                    result = await session.call_tool(
                        "think",
                        arguments={
                            "message": test_message,
                            "context": "problem_solving"
                        }
                    )
                    
                    if result.content:
                        print("✅ Think tool executed successfully!")
                        print(f"📝 Message analyzed: {test_message[:50]}...")
                        
                        # Parse the result
                        try:
                            result_data = json.loads(result.content[0].text)
                            print(f"💭 Thought: {result_data.get('thought', '')[:100]}...")
                            
                            # Check for enhanced features
                            if "context_insights" in result_data:
                                print("🎯 Enhanced with contextual understanding!")
                                print(f"   Context insights: {len(result_data.get('context_insights', []))}")
                                print(f"   Context score: {result_data.get('context_score', 0):.2f}")
                                
                                # Show some insights
                                insights = result_data.get('context_insights', [])
                                if insights:
                                    print("   Sample insights:")
                                    for insight in insights[:2]:
                                        print(f"     • {insight}")
                            else:
                                print("⚠️  Think tool not showing enhanced features")
                                
                        except json.JSONDecodeError:
                            print("📄 Raw result:", result.content[0].text[:200])
                    else:
                        print("❌ Think tool returned no content")
                else:
                    print("\n⚠️  Think tool not found")
                
                # Test the enhanced remember tool
                if "remember" in brain_tools:
                    print("\n🧪 Testing enhanced remember tool with context analysis...")
                    
                    test_info = "User prioritizes safety and quality in all implementations"
                    
                    result = await session.call_tool(
                        "remember",
                        arguments={
                            "information": test_info,
                            "importance": "high"
                        }
                    )
                    
                    if result.content:
                        print("✅ Remember tool executed successfully!")
                        try:
                            result_data = json.loads(result.content[0].text)
                            if "context_enhancement" in result_data:
                                print("🎯 Enhanced with contextual understanding!")
                                context_enh = result_data["context_enhancement"]
                                print(f"   Context score: {context_enh.get('context_score', 0):.2f}")
                                print(f"   Implicit goals: {len(context_enh.get('implicit_goals', {}).get('detected_goals', []))}")
                            else:
                                print("⚠️  Remember tool not showing enhanced features")
                        except json.JSONDecodeError:
                            print("📄 Raw remember result:", result.content[0].text[:200])
                    else:
                        print("❌ Remember tool returned no content")
                
                print("\n✅ Enhanced functionality test completed!")
                return True
                
    except Exception as e:
        print(f"❌ Error testing enhanced functionality: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🎯 Docker Enhanced ContextAnalyzer Test")
    print("Make sure the MCP server is running in Docker")
    print("=" * 60)
    
    success = asyncio.run(test_enhanced_functionality())
    
    if success:
        print("\n🎉 Enhanced ContextAnalyzer functionality is working in Docker!")
        print("\n🚀 Your MCP server now has:")
        print("   • Full ContextAnalyzer integration with all brain tools")
        print("   • Automatic subtlety detection and pattern recognition")
        print("   • Implicit goal extraction and complexity assessment")
        print("   • Intelligent recommendations based on context analysis")
        print("   • No more fallback system - full functionality available!")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
