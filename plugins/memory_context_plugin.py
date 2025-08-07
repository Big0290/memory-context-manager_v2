import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

# Add parent and src directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)
sys.path.insert(0, os.path.join(parent_dir, 'src'))

from plugin_interface import BasePlugin, PluginMetadata, ToolDefinition, ResourceDefinition


class MemoryContextPlugin(BasePlugin):
    def __init__(self):
        super().__init__()
        self.memory_store = {}
        self.context_history = []
        self.memory_file = Path("memory_store.json")
    
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="memory_context",
            version="1.0.0",
            description="Plugin for managing conversation context and memory",
            author="Memory Context Manager",
        )
    
    def _setup(self):
        self.load_memory()
    
    def _teardown(self):
        self.save_memory()
    
    def get_tools(self) -> List[ToolDefinition]:
        return [
            ToolDefinition(
                name="store_memory",
                description="Store information in persistent memory",
                handler=self.store_memory
            ),
            ToolDefinition(
                name="retrieve_memory",
                description="Retrieve information from memory by key",
                handler=self.retrieve_memory
            ),
            ToolDefinition(
                name="search_memory",
                description="Search memory entries by keyword",
                handler=self.search_memory
            ),
            ToolDefinition(
                name="add_context",
                description="Add context information to the conversation history",
                handler=self.add_context
            ),
            ToolDefinition(
                name="get_context_summary",
                description="Get a summary of recent conversation context",
                handler=self.get_context_summary
            ),
            ToolDefinition(
                name="clear_memory",
                description="Clear all memory entries",
                handler=self.clear_memory
            )
        ]
    
    def get_resources(self) -> List[ResourceDefinition]:
        return [
            ResourceDefinition(
                name="memory_entries",
                uri_template="memory://entries/{key}",
                description="Access memory entries by key",
                handler=self.get_memory_resource
            ),
            ResourceDefinition(
                name="context_history",
                uri_template="context://history/{count}",
                description="Access recent context history",
                handler=self.get_context_resource
            )
        ]
    
    def store_memory(self, key: str, value: str, tags: Optional[List[str]] = None) -> str:
        """Store information in persistent memory"""
        try:
            self.memory_store[key] = {
                "value": value,
                "timestamp": datetime.now().isoformat(),
                "tags": tags or []
            }
            self.save_memory()
            return f"Successfully stored memory entry: {key}"
        except Exception as e:
            return f"Error storing memory: {str(e)}"
    
    def retrieve_memory(self, key: str) -> Dict[str, Any]:
        """Retrieve information from memory by key"""
        try:
            if key in self.memory_store:
                return {
                    "key": key,
                    "found": True,
                    **self.memory_store[key]
                }
            else:
                return {
                    "key": key,
                    "found": False,
                    "message": f"No memory entry found for key: {key}"
                }
        except Exception as e:
            return {"error": f"Error retrieving memory: {str(e)}"}
    
    def search_memory(self, keyword: str) -> Dict[str, Any]:
        """Search memory entries by keyword"""
        try:
            matches = []
            keyword_lower = keyword.lower()
            
            for key, entry in self.memory_store.items():
                if (keyword_lower in key.lower() or
                    keyword_lower in entry["value"].lower() or
                    any(keyword_lower in tag.lower() for tag in entry["tags"])):
                    matches.append({
                        "key": key,
                        "value": entry["value"],
                        "timestamp": entry["timestamp"],
                        "tags": entry["tags"]
                    })
            
            return {
                "keyword": keyword,
                "matches": matches,
                "count": len(matches)
            }
        except Exception as e:
            return {"error": f"Error searching memory: {str(e)}"}
    
    def add_context(self, context: str, context_type: str = "general") -> str:
        """Add context information to the conversation history"""
        try:
            context_entry = {
                "content": context,
                "type": context_type,
                "timestamp": datetime.now().isoformat()
            }
            
            self.context_history.append(context_entry)
            
            if len(self.context_history) > 100:
                self.context_history = self.context_history[-100:]
            
            return f"Successfully added context entry of type: {context_type}"
        except Exception as e:
            return f"Error adding context: {str(e)}"
    
    def get_context_summary(self, count: int = 10) -> Dict[str, Any]:
        """Get a summary of recent conversation context"""
        try:
            recent_context = self.context_history[-count:] if self.context_history else []
            
            return {
                "recent_entries": recent_context,
                "count": len(recent_context),
                "total_entries": len(self.context_history)
            }
        except Exception as e:
            return {"error": f"Error getting context summary: {str(e)}"}
    
    def clear_memory(self, confirm: bool = False) -> str:
        """Clear all memory entries"""
        try:
            if not confirm:
                return "Warning: This will clear all memory entries. Call with confirm=True to proceed."
            
            self.memory_store.clear()
            self.context_history.clear()
            self.save_memory()
            
            return "Successfully cleared all memory entries and context history"
        except Exception as e:
            return f"Error clearing memory: {str(e)}"
    
    def get_memory_resource(self, key: str) -> Dict[str, Any]:
        """Resource handler for memory entries"""
        return self.retrieve_memory(key)
    
    def get_context_resource(self, count: str) -> Dict[str, Any]:
        """Resource handler for context history"""
        try:
            count_int = int(count)
            return self.get_context_summary(count_int)
        except ValueError:
            return {"error": "Invalid count parameter"}
    
    def load_memory(self):
        """Load memory from persistent storage"""
        try:
            if self.memory_file.exists():
                with open(self.memory_file, 'r') as f:
                    data = json.load(f)
                    self.memory_store = data.get("memory_store", {})
                    self.context_history = data.get("context_history", [])
        except Exception as e:
            print(f"Warning: Could not load memory file: {e}")
            self.memory_store = {}
            self.context_history = []
    
    def save_memory(self):
        """Save memory to persistent storage"""
        try:
            data = {
                "memory_store": self.memory_store,
                "context_history": self.context_history,
                "last_updated": datetime.now().isoformat()
            }
            with open(self.memory_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save memory file: {e}")