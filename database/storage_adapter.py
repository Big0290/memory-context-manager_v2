"""
Storage Adapter - Provides seamless backward compatibility
Existing plugins continue to work with JSON files, but data is actually stored in SQLite
"""

import json
import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from .brain_db import get_brain_db

logger = logging.getLogger(__name__)

class JSONCompatibilityAdapter:
    """
    Provides JSON file interface while using SQLite backend
    Existing plugins work unchanged - they think they're reading/writing JSON
    """
    
    def __init__(self):
        self.db = get_brain_db()
        
    def read_json_file(self, file_path: str) -> Dict[str, Any]:
        """
        Read JSON file - routes to appropriate database method
        Existing code: json.load(open('memory_store.json'))
        Now works with: adapter.read_json_file('memory_store.json') 
        """
        filename = Path(file_path).name
        
        if filename == "memory_store.json":
            return self.db.get_memory_store()
        
        elif filename == "brain_state.json":
            return self.db.get_brain_state()
            
        elif filename == "identities.json":
            return self.db.get_identity_profiles()
        
        else:
            # For unknown files, fallback to actual JSON file
            try:
                if os.path.exists(file_path):
                    with open(file_path, 'r') as f:
                        return json.load(f)
                else:
                    return {}
            except Exception as e:
                logger.warning(f"Failed to read {file_path}: {e}")
                return {}
    
    def write_json_file(self, file_path: str, data: Dict[str, Any]) -> bool:
        """
        Write JSON file - routes to appropriate database method
        Existing code: json.dump(data, open('memory_store.json', 'w'))
        Now works with: adapter.write_json_file('memory_store.json', data)
        """
        filename = Path(file_path).name
        
        try:
            if filename == "memory_store.json":
                return self._write_memory_store(data)
                
            elif filename == "brain_state.json":
                return self.db.update_brain_state(data)
                
            elif filename == "identities.json":
                return self._write_identities(data)
            
            else:
                # For unknown files, write actual JSON file
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, 'w') as f:
                    json.dump(data, f, indent=2)
                return True
                
        except Exception as e:
            logger.error(f"Failed to write {file_path}: {e}")
            return False
    
    def _write_memory_store(self, data: Dict[str, Any]) -> bool:
        """Write memory store data to database"""
        memory_store = data.get("memory_store", {})
        
        for key, item_data in memory_store.items():
            self.db.set_memory_item(
                key=key,
                value=item_data.get("value", ""),
                tags=item_data.get("tags", []),
                emotional_weight=item_data.get("emotional_weight", "medium")
            )
        
        # Handle context history
        context_history = data.get("context_history", [])
        for context in context_history:
            self.db.add_context_history(context)
            
        return True
    
    def _write_identities(self, data: Dict[str, Any]) -> bool:
        """Write identity data to database"""
        identities = data.get("identities", [])
        
        for identity in identities:
            self.db.update_identity_profile(
                identity_id=identity.get("id", "default"),
                profile_data=identity
            )
            
        return True

    def file_exists(self, file_path: str) -> bool:
        """Check if file exists (for compatibility)"""
        filename = Path(file_path).name
        
        # These "files" always exist in database
        if filename in ["memory_store.json", "brain_state.json", "identities.json"]:
            return True
        
        return os.path.exists(file_path)

# Global adapter instance
_storage_adapter = None

def get_storage_adapter() -> JSONCompatibilityAdapter:
    """Get global storage adapter instance"""
    global _storage_adapter
    if _storage_adapter is None:
        _storage_adapter = JSONCompatibilityAdapter()
    return _storage_adapter

# Monkey patch functions to maintain compatibility
def patch_json_operations():
    """
    Patch common JSON operations to use database backend
    This makes existing plugins work without code changes
    """
    import builtins
    import json
    
    original_open = builtins.open
    original_json_load = json.load
    original_json_dump = json.dump
    
    adapter = get_storage_adapter()
    
    # Track which files are being accessed for JSON operations
    _json_file_handles = {}
    
    def patched_open(file_path, mode='r', *args, **kwargs):
        """Patched open function that intercepts JSON file operations"""
        path_str = str(file_path)
        filename = Path(path_str).name
        
        # Check if this is one of our JSON files
        if filename in ["memory_store.json", "brain_state.json", "identities.json"]:
            if 'r' in mode:
                # Return a fake file handle for reading
                class FakeReadHandle:
                    def __init__(self, data):
                        self.data = data
                        self.closed = False
                    
                    def read(self):
                        return json.dumps(self.data)
                    
                    def close(self):
                        self.closed = True
                    
                    def __enter__(self):
                        return self
                    
                    def __exit__(self, *args):
                        self.close()
                
                data = adapter.read_json_file(path_str)
                return FakeReadHandle(data)
            
            elif 'w' in mode:
                # Return a fake file handle for writing
                class FakeWriteHandle:
                    def __init__(self, file_path):
                        self.file_path = file_path
                        self.content = ""
                        self.closed = False
                    
                    def write(self, content):
                        self.content += content
                    
                    def close(self):
                        if not self.closed and self.content:
                            try:
                                data = json.loads(self.content)
                                adapter.write_json_file(self.file_path, data)
                            except:
                                pass
                        self.closed = True
                    
                    def __enter__(self):
                        return self
                    
                    def __exit__(self, *args):
                        self.close()
                
                return FakeWriteHandle(path_str)
        
        # For non-JSON files, use original open
        return original_open(file_path, mode, *args, **kwargs)
    
    def patched_json_load(fp):
        """Patched json.load that works with our fake file handles"""
        if hasattr(fp, 'file_path'):
            # This is one of our fake handles
            return adapter.read_json_file(fp.file_path)
        elif hasattr(fp, 'data'):
            # This is our fake read handle
            return fp.data
        else:
            # Regular file handle
            return original_json_load(fp)
    
    def patched_json_dump(obj, fp, *args, **kwargs):
        """Patched json.dump that works with our fake file handles"""
        if hasattr(fp, 'file_path'):
            # This is one of our fake write handles
            adapter.write_json_file(fp.file_path, obj)
        elif hasattr(fp, 'write'):
            # Check if this might be a file we should intercept
            if hasattr(fp, 'name'):
                filename = Path(fp.name).name
                if filename in ["memory_store.json", "brain_state.json", "identities.json"]:
                    adapter.write_json_file(fp.name, obj)
                    return
            
            # Regular file handle or fake handle
            fp.write(json.dumps(obj, *args, **kwargs))
        else:
            # Fallback to original
            original_json_dump(obj, fp, *args, **kwargs)
    
    # Apply patches
    builtins.open = patched_open
    json.load = patched_json_load
    json.dump = patched_json_dump
    
    logger.info("🔧 JSON operations patched for database compatibility")