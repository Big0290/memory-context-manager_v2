#!/usr/bin/env python3
"""
Health check endpoint for Docker container
"""
import sys
import time
from pathlib import Path

def check_health():
    """Simple health check"""
    try:
        # Check if brain memory store exists
        memory_store = Path("/app/brain_memory_store")
        if not memory_store.exists():
            return False
        
        # Check if main modules can be imported
        sys.path.insert(0, "/app/src")
        sys.path.insert(0, "/app")
        
        from plugin_manager import PluginManager
        return True
        
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

if __name__ == "__main__":
    if check_health():
        print("Health check passed")
        sys.exit(0)
    else:
        print("Health check failed")
        sys.exit(1)