# Cognitive Brain Plugin

A sophisticated brain-inspired plugin for MCP (Model Context Protocol) servers that provides intelligent memory management, contextual analysis, emotional weighting, and self-reflective learning capabilities.

## 🧠 Overview

This plugin replicates human brain structure and cognitive processes using a modular architecture. It provides identity-aware persistent memory, contextual reflection, learning from experience, and emotional tagging capabilities.

## 🏗️ Architecture

### Core Modules

1. **FrontalModule** (Prefrontal Cortex)
   - Executive functions and reasoning
   - Task planning and decision making
   - Working memory management
   - Context switching

2. **MemoryCore** (Hippocampus) 
   - Long-term memory storage and retrieval
   - Memory consolidation
   - Association creation
   - Contextual recall

3. **EmotionTagger** (Amygdala)
   - Emotional weight assessment
   - Importance scoring
   - Priority tagging
   - Emotional context switching

4. **Router** (Thalamus)
   - Input routing to appropriate modules
   - Load balancing and priority management
   - Adaptive routing learning

5. **SelfReflector** (Meta-cognition)
   - Pattern analysis and learning
   - Performance review
   - Improvement planning
   - Self-awareness

6. **SyncBridge** (Corpus Callosum)
   - Multi-agent synchronization
   - Context sharing with privacy controls
   - Collaborative memory formation

### Data Structures

- **MemoryChunk**: Core memory unit with content, emotional weight, and associations
- **BrainState**: Current cognitive state and activity levels
- **IdentityProfile**: Identity-aware context management
- **TaskContext**: Task and goal tracking
- **ReflectionEntry**: Self-reflection and learning records

## 🚀 Features

### ✨ Key Capabilities

- **Identity-Aware Memory**: Contextual memory tied to specific identities/personas
- **Emotional Weighting**: Automatic importance assessment (Critical, Important, Novel, Positive, Negative, Routine)
- **Contextual Reflection**: Learning from past experiences and decisions
- **Pattern Recognition**: Automatic identification of behavioral and decision patterns
- **Self-Awareness**: Introspection about reasoning processes and performance
- **Multi-Agent Sync**: Secure sharing and collaboration between AI agents
- **Adaptive Learning**: Continuous improvement based on outcomes

### 🔧 Advanced Features

- **Debug Mode**: Detailed introspection and thought process tracking
- **Memory Consolidation**: Automatic strengthening of important memories
- **Association Networks**: Intelligent linking of related memories
- **Priority Queuing**: Smart task and request prioritization
- **Load Balancing**: Efficient resource allocation across modules
- **Conflict Resolution**: Handling of contradictory information

## 📦 Installation

1. **Copy Plugin Files**
   ```bash
   cp -r plugins/cognitive_brain_plugin/ /path/to/your/mcp/server/plugins/
   ```

2. **Install Dependencies**
   ```bash
   pip install pydantic typing-extensions
   ```

3. **Configure Storage Directory**
   ```python
   plugin_config = {
       "storage_dir": "brain_memory_store",
       "auto_analyze": True,
       "debug_mode": False,
       "memory_threshold": 100
   }
   ```

## 🎯 Usage

### Basic Integration

```python
from plugins.cognitive_brain_plugin.plugin import create_plugin

# Create plugin instance
brain_plugin = create_plugin({
    "storage_dir": "my_brain_storage",
    "auto_analyze": True,
    "debug_mode": True
})

# Initialize with MCP server
success = brain_plugin.initialize(mcp_server)
```

### Available Tools

Once integrated, the plugin provides these MCP tools:

#### `brain_analyze`
Analyze content for emotional weight and importance:
```python
result = await mcp_server.call_tool("brain_analyze", 
    content="We have a critical security vulnerability that needs immediate attention",
    context_type="incident"
)
# Returns: emotional analysis, importance scores, recommended priority
```

#### `brain_remember`
Store content in brain memory:
```python
result = await mcp_server.call_tool("brain_remember",
    content="Successfully implemented new authentication system",
    tags=["security", "implementation", "success"],
    emotional_weight="positive"
)
```

#### `brain_recall`
Search and retrieve memories:
```python
result = await mcp_server.call_tool("brain_recall",
    query="authentication security",
    limit=10
)
# Returns: relevant memories with similarity scores
```

#### `brain_reflect`
Trigger reflection and learning:
```python
result = await mcp_server.call_tool("brain_reflect",
    focus_areas=["memories", "decisions", "patterns"],
    period_hours=24
)
# Returns: insights, patterns identified, improvement suggestions
```

#### `brain_status`
Get current brain system status:
```python
result = await mcp_server.call_tool("brain_status")
# Returns: module activity levels, brain state, statistics
```

#### `brain_debug`
Control debug mode and get detailed information:
```python
result = await mcp_server.call_tool("brain_debug", enable=True)
# Returns: debug information, recent activities, thought processes
```

## 🔄 Automatic Processing

The plugin can automatically:

- **Analyze incoming requests** for emotional significance
- **Store important interactions** in memory
- **Learn from request/response patterns**
- **Trigger reflection** after significant events
- **Consolidate memories** during quiet periods
- **Route complex requests** to appropriate modules

## 📊 Configuration Options

```python
config = {
    "storage_dir": "brain_memory_store",     # Memory storage location
    "auto_analyze": True,                    # Auto-analyze content
    "debug_mode": False,                     # Enable detailed logging
    "memory_threshold": 100,                 # Min content length to analyze
    "consolidation_interval": 3600,          # Memory consolidation interval (seconds)
    "max_working_memory": 7,                 # Working memory capacity (Miller's rule)
    "reflection_interval": 21600,            # Auto-reflection interval (seconds)
    "emotional_baseline": 0.5,               # Emotional assessment baseline
    "learning_rate": 0.1,                    # Adaptation learning rate
}
```

## 🌐 Multi-Agent Scenarios

The plugin supports sophisticated multi-agent scenarios:

### Agent Registration
```python
# Register another agent
await brain_plugin.integration._process_with_module("sync_bridge", {
    "type": "agent_registration",
    "agent_id": "assistant_002",
    "agent_info": {
        "name": "Code Assistant",
        "type": "coding",
        "capabilities": ["code_review", "debugging"]
    },
    "permissions": ["read_memories", "context_share"]
})
```

### Context Sharing
```python
# Share context with other agents
await brain_plugin.integration._process_with_module("sync_bridge", {
    "type": "context_share",
    "target_agents": ["assistant_002", "assistant_003"],
    "context_data": {"current_project": "authentication_system"},
    "sharing_level": "metadata_only"  # or "memory_only", "full_context"
})
```

## 🛠️ Development

### Extending the Plugin

Add new modules by extending `BrainModule`:

```python
from plugins.cognitive_brain_plugin.core.brain_core import BrainModule

class CustomModule(BrainModule):
    def __init__(self, storage_adapter):
        super().__init__("custom_module", storage_adapter)
    
    def process(self, input_data, brain_state):
        # Custom processing logic
        return {"processed": True}
```

Register with brain:
```python
brain.register_module("custom_module", CustomModule(storage_adapter))
```

### Custom Storage Adapters

Implement `MemoryStorageAdapter` for different storage backends:

```python
from plugins.cognitive_brain_plugin.adapters.memory_adapter import MemoryStorageAdapter

class DatabaseStorageAdapter(MemoryStorageAdapter):
    def __init__(self, db_connection):
        self.db = db_connection
    
    def store_memory_chunk(self, chunk):
        # Store to database
        pass
```

## 📈 Performance

### Memory Usage
- **Working Memory**: Limited to 7±2 items (configurable)
- **Long-term Storage**: JSON file-based (configurable to database)
- **Consolidation**: Automatic background processing
- **Cleanup**: Automatic management of memory size

### Processing Speed
- **Analysis**: O(n) where n is content length
- **Retrieval**: O(log n) with indexing
- **Association**: O(k) where k is keyword count
- **Reflection**: Background processing, non-blocking

## 🔐 Privacy and Security

### Privacy Controls
- **Data Anonymization**: Configurable content anonymization
- **Access Permissions**: Fine-grained agent permissions
- **Identity Isolation**: Memory separation by identity
- **Sharing Controls**: Selective context sharing

### Security Features
- **Input Validation**: All inputs validated and sanitized
- **Storage Encryption**: Optional encrypted storage
- **Audit Logging**: Detailed operation logging
- **Memory Isolation**: Secure memory boundaries

## 🧪 Testing

Run the example demonstration:
```bash
python examples/brain_plugin_example.py
```

This will demonstrate:
- Content analysis and emotional weighting
- Memory storage and retrieval
- Pattern recognition and reflection
- Multi-module coordination
- Debug capabilities

## 🐛 Troubleshooting

### Common Issues

1. **Memory Storage Errors**
   - Check storage directory permissions
   - Verify disk space availability
   - Review configuration settings

2. **Module Loading Issues**
   - Ensure all dependencies installed
   - Check Python path configuration
   - Verify module import statements

3. **Performance Issues**
   - Monitor working memory usage
   - Adjust consolidation intervals
   - Enable debug mode for analysis

### Debug Mode

Enable comprehensive debugging:
```python
result = await mcp_server.call_tool("brain_debug", enable=True)
```

This provides:
- Recent activity logs
- Memory usage statistics
- Module performance metrics
- Thought process traces

## 🤝 Contributing

1. Follow the existing module architecture
2. Add comprehensive error handling
3. Include debug information in new modules
4. Update documentation and examples
5. Test with various scenarios

## 📄 License

This plugin is provided as part of the MCP ecosystem. Please refer to your MCP server license for terms of use.

## 🔗 Related Resources

- [MCP Server Documentation](link-to-mcp-docs)
- [Brain-Computer Interface Research](link-to-research)
- [Cognitive Architecture Papers](link-to-papers)
- [Memory Consolidation Studies](link-to-studies)

---

*Built with 🧠 for intelligent MCP server enhancement*