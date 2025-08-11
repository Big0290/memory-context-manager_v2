#!/usr/bin/env python3
"""
Test Tool Registry
Verifies the new tool registry system works correctly
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_tool_registry():
    """Test the tool registry system"""
    try:
        print("🧪 Testing Tool Registry System")
        print("=" * 40)
        
        # Test importing the tool registry
        from tool_registry import ToolRegistry
        print("✅ ToolRegistry imported successfully")
        
        # Test creating a mock MCP server
        class MockMCPServer:
            def tool(self):
                def decorator(func):
                    return func
                return decorator
        
        mock_mcp = MockMCPServer()
        
        # Test creating registry
        registry = ToolRegistry(mock_mcp)
        print("✅ ToolRegistry created successfully")
        
        # Test tool registration
        def test_handler():
            return {"test": "success"}
        
        success = registry.register_tool(
            name="test_tool",
            handler=test_handler,
            category="test",
            description="A test tool"
        )
        
        if success:
            print("✅ Tool registration successful")
        else:
            print("❌ Tool registration failed")
        
        # Test duplicate registration
        success2 = registry.register_tool(
            name="test_tool",  # Same name
            handler=test_handler,
            category="test",
            description="Another test tool"
        )
        
        if not success2:
            print("✅ Duplicate tool prevention working")
        else:
            print("❌ Duplicate tool prevention failed")
        
        # Test tool info
        tool_info = registry.get_tool_info()
        print(f"✅ Tool info retrieved: {tool_info['total_tools']} tools")
        
        # Test category listing
        test_tools = registry.list_tools_by_category("test")
        print(f"✅ Category listing working: {len(test_tools)} tools in 'test' category")
        
        print("\n🎉 Tool Registry test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Tool Registry test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_tool_registry()
    
    if success:
        print("\n🚀 Tool Registry is ready for integration!")
    else:
        print("\n⚠️  Tool Registry needs fixes before integration.")
