import os
import sys
import platform
import psutil
from datetime import datetime
from typing import List, Dict, Any

# Add parent and src directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)
sys.path.insert(0, os.path.join(parent_dir, 'src'))

from plugin_interface import BasePlugin, PluginMetadata, ToolDefinition


class SystemInfoPlugin(BasePlugin):
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="system_info",
            version="1.0.0",
            description="Plugin for getting system information and metrics",
            author="Memory Context Manager",
            dependencies=["psutil"]
        )
    
    def get_tools(self) -> List[ToolDefinition]:
        return [
            ToolDefinition(
                name="get_system_info",
                description="Get general system information",
                handler=self.get_system_info
            ),
            ToolDefinition(
                name="get_resource_usage",
                description="Get current system resource usage",
                handler=self.get_resource_usage
            ),
            ToolDefinition(
                name="get_python_info",
                description="Get Python interpreter information",
                handler=self.get_python_info
            ),
            ToolDefinition(
                name="get_environment_vars",
                description="Get environment variables (filtered for security)",
                handler=self.get_environment_vars
            )
        ]
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get general system information"""
        try:
            return {
                "platform": {
                    "system": platform.system(),
                    "release": platform.release(),
                    "version": platform.version(),
                    "machine": platform.machine(),
                    "processor": platform.processor(),
                    "architecture": platform.architecture(),
                    "platform": platform.platform()
                },
                "hostname": platform.node(),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": f"Error getting system info: {str(e)}"}
    
    def get_resource_usage(self) -> Dict[str, Any]:
        """Get current system resource usage"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                "cpu": {
                    "percent_used": cpu_percent,
                    "count": psutil.cpu_count(),
                    "count_logical": psutil.cpu_count(logical=True)
                },
                "memory": {
                    "total": memory.total,
                    "available": memory.available,
                    "percent_used": memory.percent,
                    "used": memory.used,
                    "free": memory.free
                },
                "disk": {
                    "total": disk.total,
                    "used": disk.used,
                    "free": disk.free,
                    "percent_used": (disk.used / disk.total) * 100
                },
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": f"Error getting resource usage: {str(e)}"}
    
    def get_python_info(self) -> Dict[str, Any]:
        """Get Python interpreter information"""
        try:
            return {
                "version": sys.version,
                "version_info": {
                    "major": sys.version_info.major,
                    "minor": sys.version_info.minor,
                    "micro": sys.version_info.micro,
                    "releaselevel": sys.version_info.releaselevel,
                    "serial": sys.version_info.serial
                },
                "executable": sys.executable,
                "platform": sys.platform,
                "implementation": {
                    "name": sys.implementation.name,
                    "version": sys.implementation.version,
                    "cache_tag": sys.implementation.cache_tag
                },
                "path": sys.path[:5],  # First 5 paths only
                "modules_count": len(sys.modules),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": f"Error getting Python info: {str(e)}"}
    
    def get_environment_vars(self, filter_sensitive: bool = True) -> Dict[str, Any]:
        """Get environment variables (filtered for security)"""
        try:
            sensitive_patterns = [
                'password', 'secret', 'key', 'token', 'auth', 'credential',
                'api_key', 'private', 'ssh', 'cert', 'ssl'
            ]
            
            env_vars = {}
            filtered_count = 0
            
            for key, value in os.environ.items():
                if filter_sensitive:
                    key_lower = key.lower()
                    if any(pattern in key_lower for pattern in sensitive_patterns):
                        filtered_count += 1
                        continue
                
                env_vars[key] = value
            
            return {
                "environment_variables": env_vars,
                "total_count": len(os.environ),
                "filtered_count": filtered_count if filter_sensitive else 0,
                "showing_count": len(env_vars),
                "filtered_sensitive": filter_sensitive,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": f"Error getting environment variables: {str(e)}"}