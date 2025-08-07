#!/usr/bin/env python3
"""
Simple MCP Setup for Cursor Integration
"""

import json
import os
import sys
import platform
from pathlib import Path


def create_mcp_config():
    """Create MCP configuration for Cursor"""
    project_root = Path(__file__).parent.absolute()
    config_dir = project_root / ".cursor"
    config_file = config_dir / "mcp.json"
    
    # Create configuration
    config = {
        "mcpServers": {
            "memory-context-manager": {
                "command": "uv",
                "args": ["run", "python", "main.py"],
                "cwd": str(project_root),
                "env": {
                    "PYTHONPATH": str(project_root)
                }
            }
        }
    }
    
    # Create directory and write config
    config_dir.mkdir(exist_ok=True)
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    return config_file


def main():
    """Main setup function"""
    print("🚀 Memory Context Manager - MCP Setup")
    print("=" * 40)
    
    print(f"OS: {platform.system()}")
    print(f"Project: {Path(__file__).parent.name}")
    
    try:
        config_file = create_mcp_config()
        print(f"\n✅ Created MCP configuration: {config_file}")
        
        print("\n📋 Next steps:")
        print("1. Restart Cursor IDE")
        print("2. Go to Settings → Features → Model Context Protocol")  
        print("3. Verify 'memory-context-manager' appears as Connected")
        print("4. Available tools: 16 total (file ops, memory, system info)")
        
        print(f"\n🔧 Configuration file: {config_file}")
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()