import importlib
import importlib.util
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Type, Any
import logging
from plugin_interface import PluginInterface, ToolDefinition, ResourceDefinition, PromptDefinition

logger = logging.getLogger(__name__)


class PluginRegistry:
    def __init__(self):
        self.plugins: Dict[str, PluginInterface] = {}
        self.tools: Dict[str, ToolDefinition] = {}
        self.resources: Dict[str, ResourceDefinition] = {}
        self.prompts: Dict[str, PromptDefinition] = {}
    
    def register_plugin(self, plugin: PluginInterface) -> None:
        plugin_name = plugin.metadata.name
        if plugin_name in self.plugins:
            logger.warning(f"Plugin {plugin_name} already registered, skipping")
            return
        
        self.plugins[plugin_name] = plugin
        
        for tool in plugin.get_tools():
            if tool.name in self.tools:
                logger.warning(f"Tool {tool.name} from plugin {plugin_name} conflicts with existing tool")
                continue
            self.tools[tool.name] = tool
        
        for resource in plugin.get_resources():
            if resource.name in self.resources:
                logger.warning(f"Resource {resource.name} from plugin {plugin_name} conflicts with existing resource")
                continue
            self.resources[resource.name] = resource
        
        for prompt in plugin.get_prompts():
            if prompt.name in self.prompts:
                logger.warning(f"Prompt {prompt.name} from plugin {plugin_name} conflicts with existing prompt")
                continue
            self.prompts[prompt.name] = prompt
        
        logger.info(f"Registered plugin: {plugin_name}")
    
    def unregister_plugin(self, plugin_name: str) -> None:
        if plugin_name not in self.plugins:
            return
        
        plugin = self.plugins[plugin_name]
        
        for tool in plugin.get_tools():
            self.tools.pop(tool.name, None)
        
        for resource in plugin.get_resources():
            self.resources.pop(resource.name, None)
        
        for prompt in plugin.get_prompts():
            self.prompts.pop(prompt.name, None)
        
        self.plugins.pop(plugin_name)
        logger.info(f"Unregistered plugin: {plugin_name}")
    
    def get_plugin(self, name: str) -> Optional[PluginInterface]:
        return self.plugins.get(name)
    
    def list_plugins(self) -> List[str]:
        return list(self.plugins.keys())


class PluginManager:
    def __init__(self, plugin_dirs: Optional[List[str]] = None):
        self.registry = PluginRegistry()
        self.plugin_dirs = plugin_dirs or ["plugins"]
        self._loaded_modules: Dict[str, Any] = {}
    
    def load_plugins_from_directory(self, directory: str) -> None:
        plugin_dir = Path(directory)
        if not plugin_dir.exists() or not plugin_dir.is_dir():
            logger.warning(f"Plugin directory does not exist: {directory}")
            return
        
        for file_path in plugin_dir.glob("*.py"):
            if file_path.name.startswith("_"):
                continue
            
            try:
                self._load_plugin_from_file(file_path)
            except Exception as e:
                logger.error(f"Failed to load plugin from {file_path}: {e}")
    
    def _load_plugin_from_file(self, file_path: Path) -> None:
        module_name = f"plugin_{file_path.stem}"
        
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Cannot load module from {file_path}")
        
        module = importlib.util.module_from_spec(spec)
        self._loaded_modules[module_name] = module
        
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        
        plugin_classes = [
            getattr(module, attr) for attr in dir(module)
            if (isinstance(getattr(module, attr), type) and
                issubclass(getattr(module, attr), PluginInterface) and
                getattr(module, attr) != PluginInterface)
        ]
        
        for plugin_class in plugin_classes:
            try:
                plugin_instance = plugin_class()
                plugin_instance.initialize()
                self.registry.register_plugin(plugin_instance)
                logger.info(f"Loaded plugin: {plugin_instance.metadata.name}")
            except Exception as e:
                logger.error(f"Failed to initialize plugin {plugin_class.__name__}: {e}")
    
    def load_all_plugins(self) -> None:
        for directory in self.plugin_dirs:
            self.load_plugins_from_directory(directory)
    
    def unload_plugin(self, plugin_name: str) -> None:
        plugin = self.registry.get_plugin(plugin_name)
        if plugin:
            try:
                plugin.cleanup()
            except Exception as e:
                logger.error(f"Error cleaning up plugin {plugin_name}: {e}")
            
            self.registry.unregister_plugin(plugin_name)
    
    def reload_plugin(self, plugin_name: str) -> None:
        self.unload_plugin(plugin_name)
        self.load_all_plugins()
    
    def shutdown(self) -> None:
        for plugin_name in list(self.registry.plugins.keys()):
            plugin = self.registry.plugins[plugin_name]
            try:
                plugin.on_server_shutdown()
                plugin.cleanup()
            except Exception as e:
                logger.error(f"Error shutting down plugin {plugin_name}: {e}")
        
        self.registry.plugins.clear()
        self.registry.tools.clear()
        self.registry.resources.clear()
        self.registry.prompts.clear()
    
    def startup_plugins(self) -> None:
        for plugin in self.registry.plugins.values():
            try:
                plugin.on_server_startup()
            except Exception as e:
                logger.error(f"Error starting up plugin {plugin.metadata.name}: {e}")