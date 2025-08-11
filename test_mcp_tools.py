#!/usr/bin/env python3
"""
🧪 Simple MCP Tools Test

Tests if the MCP server is working and has enhanced tools available.
"""

import subprocess
import time

def test_mcp_server():
    """Test if MCP server is responding"""
    print("🧪 Testing MCP Server...")
    
    # Check if server is running
    try:
        result = subprocess.run(
            ["docker-compose", "ps", "memory_mcp_server"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if "Up" in result.stdout:
            print("✅ MCP Server is running")
            
            # Check server logs for enhanced tools
            print("🔍 Checking server logs for enhanced tools...")
            
            logs_result = subprocess.run(
                ["docker-compose", "logs", "memory_mcp_server"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if "Enhanced Tool Registry: 12 tools" in logs_result.stdout:
                print("✅ Enhanced Tool Registry found with 12 tools")
                
                # Check for specific enhanced tools
                enhanced_tools = [
                    "think_deeply", "reflect_enhanced", "remember_important",
                    "recall_intelligently", "forget_selectively", "understand_deeply",
                    "detect_patterns", "assess_complexity", "code_analyze",
                    "debug_intelligently", "refactor_safely", "analyze_context_comprehensive"
                ]
                
                found_tools = []
                for tool in enhanced_tools:
                    if tool in logs_result.stdout:
                        found_tools.append(tool)
                
                print(f"✅ Found {len(found_tools)} enhanced tools:")
                for tool in found_tools:
                    print(f"   - {tool}")
                
                if len(found_tools) == 12:
                    print("🎉 All 12 enhanced tools are available!")
                    return True
                else:
                    print(f"⚠️ Only {len(found_tools)}/12 enhanced tools found")
                    return False
            else:
                print("❌ Enhanced Tool Registry not found in logs")
                return False
        else:
            print("❌ MCP Server is not running")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Timeout checking MCP server")
        return False
    except Exception as e:
        print(f"❌ Error testing MCP server: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🚀 MCP Enhanced Tools Test")
    print("=" * 50)
    
    success = test_mcp_server()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 SUCCESS: MCP server has all enhanced tools!")
        print("💡 The tools are already registered and available.")
        print("🔧 You can now use them in Cursor!")
    else:
        print("❌ FAILED: MCP server is not working properly")
        print("🔧 Check the server logs for errors")

if __name__ == "__main__":
    main()
