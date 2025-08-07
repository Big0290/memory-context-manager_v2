from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Callable
from pydantic import BaseModel


class PluginMetadata(BaseModel):
    name: str
    version: str
    description: str
    author: Optional[str] = None
    dependencies: List[str] = []


class ToolDefinition(BaseModel):
    name: str
    description: str
    handler: Callable
    parameters: Dict[str, Any] = {}


class ResourceDefinition(BaseModel):
    name: str
    uri_template: str
    description: str
    handler: Callable


class PromptDefinition(BaseModel):
    name: str
    description: str
    handler: Callable
    arguments: List[str] = []


class PluginInterface(ABC):
    @property
    @abstractmethod
    def metadata(self) -> PluginMetadata:
        pass
    
    @abstractmethod
    def initialize(self) -> None:
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        pass
    
    def get_tools(self) -> List[ToolDefinition]:
        return []
    
    def get_resources(self) -> List[ResourceDefinition]:
        return []
    
    def get_prompts(self) -> List[PromptDefinition]:
        return []
    
    def on_server_startup(self) -> None:
        pass
    
    def on_server_shutdown(self) -> None:
        pass


class BasePlugin(PluginInterface):
    def __init__(self):
        self._initialized = False
    
    def initialize(self) -> None:
        if self._initialized:
            return
        self._initialized = True
        self._setup()
    
    def cleanup(self) -> None:
        if not self._initialized:
            return
        self._teardown()
        self._initialized = False
    
    def _setup(self) -> None:
        pass
    
    def _teardown(self) -> None:
        pass
    
    @property
    def is_initialized(self) -> bool:
        return self._initialized