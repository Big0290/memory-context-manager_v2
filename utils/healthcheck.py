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
            print("Brain memory store not found")
            return False
        
        # Check if the server is running by looking for the brain interface
        brain_interface = Path("/app/brain_interface.py")
        if not brain_interface.exists():
            print("Brain interface not found")
            return False
        
        # Check if the context analyzer module exists
        context_analyzer = Path("/app/plugins/cognitive_brain_plugin/modules/context_analyzer.py")
        if not context_analyzer.exists():
            print("Context analyzer module not found")
            return False
        
        print("All required components found")
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