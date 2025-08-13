#!/usr/bin/env python3
"""
Test Environment Requirements Checker
Installs missing dependencies and creates mock modules for testing
"""

import sys
import subprocess
import importlib
from types import ModuleType

def install_and_mock_dependencies():
    """Install or mock required dependencies for testing"""
    
    # List of required packages with fallback mocks
    requirements = {
        'aiohttp': create_aiohttp_mock,
        'aiosqlite': create_aiosqlite_mock, 
        'psutil': None,  # Should install normally
        'requests': None,
        'beautifulsoup4': create_bs4_mock,
        'pydantic': create_pydantic_mock,
        'trafilatura': create_trafilatura_mock
    }
    
    print("🔧 Setting up test environment dependencies...")
    
    for package, mock_creator in requirements.items():
        package_import = package.replace('-', '_').replace('4', '')
        
        try:
            # Try to import the package
            importlib.import_module(package_import)
            print(f"✅ {package}: Already available")
            
        except ImportError:
            # Try to install it
            try:
                print(f"⬇️ Installing {package}...")
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", 
                    package, "--quiet", "--user"
                ])
                importlib.import_module(package_import)
                print(f"✅ {package}: Installed successfully")
                
            except (subprocess.CalledProcessError, ImportError):
                # If installation fails, create mock
                if mock_creator:
                    mock_module = mock_creator()
                    sys.modules[package_import] = mock_module
                    print(f"🔧 {package}: Mock module created")
                else:
                    print(f"❌ {package}: Installation failed, no mock available")

def create_aiohttp_mock():
    """Create mock aiohttp module for testing"""
    mock = ModuleType('aiohttp')
    
    class MockClientSession:
        async def __aenter__(self):
            return self
        async def __aexit__(self, *args):
            pass
        async def get(self, url, **kwargs):
            return MockResponse()
        async def post(self, url, **kwargs):
            return MockResponse()
    
    class MockResponse:
        def __init__(self):
            self.status = 200
        async def json(self):
            return {"mock": "response"}
        async def text(self):
            return "mock response"
            
    mock.ClientSession = MockClientSession
    return mock

def create_aiosqlite_mock():
    """Create mock aiosqlite module for testing"""
    mock = ModuleType('aiosqlite')
    
    def connect(database):
        class MockConnection:
            async def __aenter__(self):
                return self
            async def __aexit__(self, *args):
                pass
            async def execute(self, sql, params=None):
                return MockCursor()
            async def commit(self):
                pass
        return MockConnection()
    
    class MockCursor:
        async def fetchone(self):
            return None
        async def fetchall(self):
            return []
    
    mock.connect = connect
    return mock

def create_pydantic_mock():
    """Create mock pydantic module for testing"""
    mock = ModuleType('pydantic')
    
    class BaseModel:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
                
        def dict(self):
            return {}
            
        def json(self):
            return "{}"
    
    mock.BaseModel = BaseModel
    return mock

def create_bs4_mock():
    """Create mock BeautifulSoup4 module for testing"""
    mock = ModuleType('bs4')
    
    class BeautifulSoup:
        def __init__(self, markup="", features="html.parser"):
            self.markup = markup
            
        def find(self, *args, **kwargs):
            return None
            
        def find_all(self, *args, **kwargs):
            return []
            
        def get_text(self):
            return "mock text"
    
    mock.BeautifulSoup = BeautifulSoup
    
    # Also create the 'bs4' alias for beautifulsoup4
    sys.modules['bs4'] = mock
    return mock

def create_trafilatura_mock():
    """Create mock trafilatura module for testing"""
    mock = ModuleType('trafilatura')
    
    def extract(downloaded, **kwargs):
        return "mock extracted text"
    
    def fetch_url(url, **kwargs):
        return f"mock content from {url}"
    
    mock.extract = extract
    mock.fetch_url = fetch_url
    return mock

if __name__ == "__main__":
    install_and_mock_dependencies()
    print("✅ Test environment setup complete")