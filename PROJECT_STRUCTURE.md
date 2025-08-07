# Memory Context Manager v2 - Project Structure

## 🎯 Core Files

```
memory-context-manager_v2/
├── main.py                    # Main MCP server entry point
├── setup_mcp.py              # Cursor integration setup
├── pyproject.toml            # Dependencies and project config
├── uv.lock                   # Dependency lock file
├── src/                      # Core source code
│   ├── __init__.py
│   ├── plugin_interface.py   # Plugin system interface
│   └── plugin_manager.py     # Plugin loading and management
├── plugins/                  # Extensible plugins
│   ├── __init__.py
│   ├── file_operations_plugin.py    # File system operations
│   ├── memory_context_plugin.py     # Memory and context management
│   └── system_info_plugin.py        # System information tools
├── .cursor/                  # Cursor IDE configuration
│   └── mcp.json             # MCP server configuration
├── README.md                # Main documentation
└── CURSOR_SETUP.md         # Cursor integration guide
```

## 🚀 Getting Started

### 1. Install Dependencies
```bash
uv add "mcp[cli]>=1.0.0" "pydantic>=2.0.0" "typing-extensions>=4.0.0" "psutil>=5.9.0"
```

### 2. Setup for Cursor
```bash
uv run python setup_mcp.py
```

### 3. Test Server
```bash
uv run python main.py
```

## 🧩 Plugin System

### Core Components
- **Plugin Interface**: `src/plugin_interface.py` - Defines plugin contracts
- **Plugin Manager**: `src/plugin_manager.py` - Handles plugin loading and lifecycle
- **Main Server**: `main.py` - FastMCP server with plugin integration

### Available Plugins
1. **File Operations** - read_file, write_file, list_directory, file_exists
2. **Memory Context** - store_memory, retrieve_memory, search_memory, context management
3. **System Info** - get_system_info, get_resource_usage, get_python_info, get_environment_vars

### Server Management Tools
- **list_plugins** - Show all loaded plugins
- **server_status** - Get server statistics

## 📊 Server Capabilities

- **Total Tools**: 16 (14 from plugins + 2 core)
- **Resources**: 2 (memory_entries, context_history)
- **Plugins**: 3 independent, extensible plugins
- **Transport**: stdin/stdout for maximum reliability

## 🔧 Configuration

The server uses a simple, clean configuration:
```json
{
  "mcpServers": {
    "memory-context-manager": {
      "command": "uv",
      "args": ["run", "python", "main.py"],
      "cwd": "/path/to/project",
      "env": {
        "PYTHONPATH": "/path/to/project"
      }
    }
  }
}
```

## ✨ Key Features

- **Extensible**: Easy to add new plugins
- **Independent**: Each plugin operates separately
- **Reliable**: Uses official MCP SDK with stdio transport
- **Clean**: Minimal, focused codebase
- **Production Ready**: Proper error handling and logging

## 🎉 Success Indicators

When working correctly in Cursor:
- ✅ "memory-context-manager" shows as Connected (green)
- ✅ 16 tools available in Cursor chat
- ✅ All plugin functionality accessible
- ✅ Persistent memory and context management
- ✅ File operations and system information tools