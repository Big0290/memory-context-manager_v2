# 🧠 Cursor MCP Configuration for Enhanced AI Brain

## 📋 Configuration Files

### `mcp.json` - Basic Configuration

This is the main MCP configuration file that Cursor will use by default.

### `mcp-enhanced.json` - Enhanced Configuration

This configuration includes multiple MCP servers for different AI brain capabilities.

## 🚀 How to Use

### 1. **Basic MCP Server** (Recommended)

Use `mcp.json` for the main AI brain connection:

- **Server**: `memory-context-manager-v2`
- **Capabilities**: Complete AI brain with enhanced thinking, dreaming, and background processing

### 2. **Enhanced MCP Servers**

Use `mcp-enhanced.json` for specialized capabilities:

- **Enhanced Thinking System**: Background process integration and iteration analysis
- **Enhanced Dream System**: Context injection optimization and memory consolidation

## 🔧 Setup Instructions

1. **Ensure Docker is running** with our containers:

   ```bash
   docker-compose up -d
   ```

2. **Cursor will automatically detect** the MCP configuration

3. **Test the connection** by asking Cursor to use our AI brain tools

## 🧠 Available AI Brain Tools

- **`think`** - Enhanced thinking with background processing analysis
- **`dream`** - Enhanced dreaming with context injection optimization
- **`remember`** - Enhanced memory formation
- **`analyze_system_optimization`** - Comprehensive system analysis
- **`get_dream_analysis`** - Dream system analysis and insights

## 🆘 Troubleshooting

If the MCP connection fails:

1. Check that Docker containers are running
2. Verify the container name is `memory_mcp_server`
3. Ensure the MCP server is accessible

## 📚 Documentation

For more details about our enhanced AI brain capabilities, see the `docs/` directory.
