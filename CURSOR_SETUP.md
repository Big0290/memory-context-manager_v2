# Cursor MCP Integration Guide

This guide will help you integrate the Memory Context Manager with Cursor IDE.

## 🚀 Quick Start

1. **Install Dependencies**
   ```bash
   uv add "mcp[cli]>=1.0.0" "pydantic>=2.0.0" "typing-extensions>=4.0.0" "psutil>=5.9.0"
   ```

2. **Run Setup**
   ```bash
   uv run python setup_mcp.py
   ```

3. **Restart Cursor IDE**

4. **Verify Integration**
   - Go to Cursor Settings → Features → Model Context Protocol
   - Look for "memory-context-manager" in the server list
   - Status should show as "Connected"

## 🔧 Configuration Files Created

### Project-Level Configuration
- **Location**: `.cursor/mcp.json` in your project root
- **Scope**: Only this project will have access to the MCP server

### Global Configuration  
- **Location**: `~/.cursor/mcp.json` in your home directory
- **Scope**: All Cursor projects will have access to the MCP server

### Generated Files
- **Launch Script**: `launch_mcp_server.sh` (Linux/macOS) or `launch_mcp_server.bat` (Windows)
- **Configuration**: Automatically detects UV, Python paths, and sets environment variables

## 🛠 Available Tools in Cursor

Once configured, these tools will be available in Cursor chat:

### File Operations
- `read_file` - Read file contents
- `write_file` - Write content to files
- `list_directory` - List directory contents
- `file_exists` - Check file existence

### Memory & Context Management
- `store_memory` - Store information persistently
- `retrieve_memory` - Get stored information
- `search_memory` - Search through stored memories
- `add_context` - Add conversation context
- `get_context_summary` - Get recent context summary
- `clear_memory` - Clear stored memories

### System Information
- `get_system_info` - System details
- `get_resource_usage` - CPU, memory, disk usage
- `get_python_info` - Python environment info
- `get_environment_vars` - Environment variables

### Server Management
- `list_plugins` - Show loaded plugins
- `server_status` - Server statistics
- `reload_plugin` - Reload specific plugins

## 🔍 Troubleshooting

### Server Not Appearing in Cursor

1. **Check Configuration File**
   ```bash
   # Verify the config file exists and is valid JSON
   cat .cursor/mcp.json
   ```

2. **Test Server Manually**
   ```bash
   # Test if the server starts correctly
   ./launch_mcp_server.sh
   # or
   uv run python main.py
   ```

3. **Check Cursor MCP Logs**
   - In Cursor: View → Output → Select "MCP Logs" from dropdown
   - Look for connection errors or server startup issues

### Server Shows as Disconnected

1. **Verify Dependencies**
   ```bash
   uv run python test_server.py
   ```

2. **Check File Paths**
   - Ensure the `cwd` path in `mcp.json` is correct
   - Verify `main.py` exists at the specified location

3. **Environment Issues**
   - Check if UV is installed: `which uv`
   - Check Python version: `python3 --version`
   - Verify virtual environment is activated

### Tools Not Working

1. **Check Plugin Loading**
   - Run `uv run python test_server.py`
   - Verify all plugins load successfully

2. **Permission Issues**
   - Ensure the server has read/write access to necessary directories
   - Check if plugins directory exists and contains plugin files

3. **Port Conflicts**
   - MCP uses stdin/stdout, no port conflicts should occur
   - If issues persist, check for other MCP servers with similar names

## 🔄 Manual Configuration

If automatic setup fails, create `.cursor/mcp.json` manually:

```json
{
  "mcpServers": {
    "memory-context-manager": {
      "command": "uv",
      "args": ["run", "python", "main.py"],
      "cwd": "/absolute/path/to/memory-context-manager_v2",
      "env": {
        "PYTHONPATH": "/absolute/path/to/memory-context-manager_v2",
        "MCP_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

**Replace the paths with your actual project directory!**

## 📱 Different Platforms

### macOS
- Config location: `~/.cursor/mcp.json`
- Use: `python3` or `uv`

### Windows  
- Config location: `%USERPROFILE%\.cursor\mcp.json`
- Use: `python`, `py`, or `uv`

### Linux
- Config location: `~/.cursor/mcp.json` 
- Use: `python3` or `uv`

## 🧪 Testing Your Setup

1. **Server Test**
   ```bash
   uv run python test_server.py
   ```

2. **Manual Server Start**
   ```bash
   uv run python main.py
   # Should start and wait for MCP protocol messages
   ```

3. **Configuration Test**
   ```bash
   uv run python setup_mcp.py
   # Will create the configuration automatically
   ```

## 🆘 Getting Help

If you're still having issues:

1. Check the main `README.md` for detailed documentation
2. Verify all dependencies are correctly installed
3. Test each plugin independently using `test_server.py`
4. Check Cursor's MCP logs for specific error messages
5. Ensure you're using a supported Cursor version with MCP support

## 🎯 Success Indicators

You'll know everything is working when:
- ✅ Cursor shows "memory-context-manager" as Connected in MCP settings
- ✅ You can see "Available Tools" in Cursor chat that include your server's tools
- ✅ Cursor can successfully call tools like `server_status` or `list_plugins`
- ✅ The server responds to tool calls with expected data

Happy coding! 🚀