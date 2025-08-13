#!/usr/bin/env python3
"""
Check Symbiotic Integration Status
"""

import asyncio
import json
from symbiotic_integration_bridge import SymbioticIntegrationBridge

async def main():
    """Check symbiotic integration status"""
    try:
        bridge = SymbioticIntegrationBridge('brain_memory_store/brain.db')
        result = await bridge.get_symbiotic_status()
        
        print("🔗 SYMBIOTIC INTEGRATION STATUS:")
        print("=" * 50)
        print(json.dumps(result, indent=2, default=str))
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
