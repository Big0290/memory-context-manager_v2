import os
from pathlib import Path
from typing import List, Dict, Any
import sys
import json

# Add parent and src directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)
sys.path.insert(0, os.path.join(parent_dir, 'src'))

from plugin_interface import BasePlugin, PluginMetadata, ToolDefinition


class FileOperationsPlugin(BasePlugin):
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="file_operations",
            version="1.0.0",
            description="Plugin for file system operations",
            author="Memory Context Manager",
        )
    
    def get_tools(self) -> List[ToolDefinition]:
        return [
            ToolDefinition(
                name="read_file",
                description="Read the contents of a file",
                handler=self.read_file
            ),
            ToolDefinition(
                name="write_file",
                description="Write content to a file",
                handler=self.write_file
            ),
            ToolDefinition(
                name="list_directory",
                description="List files and directories in a path",
                handler=self.list_directory
            ),
            ToolDefinition(
                name="file_exists",
                description="Check if a file or directory exists",
                handler=self.file_exists
            )
        ]
    
    def read_file(self, file_path: str) -> str:
        """Read the contents of a file"""
        try:
            path = Path(file_path)
            if not path.exists():
                return f"Error: File {file_path} does not exist"
            
            if not path.is_file():
                return f"Error: {file_path} is not a file"
            
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    def write_file(self, file_path: str, content: str, create_dirs: bool = True) -> str:
        """Write content to a file"""
        try:
            path = Path(file_path)
            
            if create_dirs:
                path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return f"Successfully wrote to {file_path}"
        except Exception as e:
            return f"Error writing file: {str(e)}"
    
    def list_directory(self, directory_path: str) -> Dict[str, Any]:
        """List files and directories in a path"""
        try:
            path = Path(directory_path)
            
            if not path.exists():
                return {"error": f"Directory {directory_path} does not exist"}
            
            if not path.is_dir():
                return {"error": f"{directory_path} is not a directory"}
            
            items = {
                "files": [],
                "directories": [],
                "path": str(path.absolute())
            }
            
            for item in path.iterdir():
                if item.is_file():
                    items["files"].append({
                        "name": item.name,
                        "size": item.stat().st_size,
                        "modified": item.stat().st_mtime
                    })
                elif item.is_dir():
                    items["directories"].append({
                        "name": item.name,
                        "modified": item.stat().st_mtime
                    })
            
            return items
        except Exception as e:
            return {"error": f"Error listing directory: {str(e)}"}
    
    def file_exists(self, path: str) -> Dict[str, Any]:
        """Check if a file or directory exists"""
        try:
            file_path = Path(path)
            exists = file_path.exists()
            
            result = {
                "path": path,
                "exists": exists
            }
            
            if exists:
                result.update({
                    "is_file": file_path.is_file(),
                    "is_directory": file_path.is_dir(),
                    "absolute_path": str(file_path.absolute()),
                    "size": file_path.stat().st_size if file_path.is_file() else None
                })
            
            return result
        except Exception as e:
            return {"error": f"Error checking file existence: {str(e)}"}