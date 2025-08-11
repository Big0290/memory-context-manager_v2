# 🛠️ Tools and Workflows Guide

## Overview

Memory Context Manager v2 provides a comprehensive suite of tools organized into several categories. This guide explains each tool, its purpose, and how to use it effectively.

## 🧠 Core Brain Interface Tools

### 1. **brain_info**

**Purpose**: Get comprehensive information about the brain interface and available capabilities
**Workflow**:

```
User Request → brain_info() → Returns brain capabilities, status, and configuration
```

**Use Case**: Initial setup, debugging, understanding system capabilities

### 2. **ai_chat_with_memory**

**Purpose**: Enhanced AI chat with persistent memory and context awareness
**Workflow**:

```
User Message → Memory Context Retrieval → AI Processing → Response Generation → Memory Storage → Response Return
```

**Parameters**:

- `user_message`: The user's input message
- `ai_model_name`: AI model to use (default: "assistant")
  **Use Case**: Main conversation interface with memory persistence

### 3. **quick_memory_chat**

**Purpose**: Fast, lightweight chat without full memory processing
**Workflow**:

```
User Message → Quick AI Processing → Response Return
```

**Use Case**: Simple questions, quick responses, when full memory context isn't needed

## 🔌 Plugin Management Tools

### 4. **list_plugins**

**Purpose**: List all loaded plugins and their information
**Workflow**:

```
Request → Plugin Registry Scan → Plugin List Generation → Return Plugin Details
```

**Use Case**: System administration, debugging, understanding available functionality

### 5. **reload_plugin**

**Purpose**: Reload a specific plugin by name
**Workflow**:

```
Plugin Name → Plugin Unload → Plugin Reload → Status Return
```

**Use Case**: Development, plugin updates, troubleshooting

### 6. **server_status**

**Purpose**: Get server status and statistics
**Workflow**:

```
Request → System Status Check → Statistics Collection → Status Report Return
```

**Use Case**: Monitoring, health checks, performance analysis

## 🧠 Memory and Context Tools

### 7. **store_memory**

**Purpose**: Store information in persistent memory
**Workflow**:

```
Key + Value + Tags → Memory Storage → Persistence → Success Confirmation
```

**Parameters**:

- `key`: Unique identifier for the memory
- `value`: Information to store
- `tags`: Optional categorization tags
  **Use Case**: Saving important information, user preferences, conversation context

### 8. **retrieve_memory**

**Purpose**: Retrieve information from memory by key
**Workflow**:

```
Key → Memory Lookup → Value Retrieval → Return Stored Information
```

**Use Case**: Accessing saved information, retrieving context, user preferences

### 9. **search_memory**

**Purpose**: Search memory entries by keyword
**Workflow**:

```
Keyword → Memory Search → Pattern Matching → Relevant Results Return
```

**Use Case**: Finding related information, context discovery, knowledge retrieval

### 10. **add_context**

**Purpose**: Add context information to conversation history
**Workflow**:

```
Context + Type → Context Storage → History Update → Confirmation
```

**Use Case**: Building conversation context, maintaining session state

### 11. **get_context_summary**

**Purpose**: Get a summary of recent conversation context
**Workflow**:

```
Count Parameter → Context Retrieval → Summary Generation → Context Summary Return
```

**Use Case**: Understanding conversation flow, context review, session management

### 12. **clear_memory**

**Purpose**: Clear all memory entries
**Workflow**:

```
Confirmation → Memory Clear → Storage Reset → Confirmation Return
```

**Use Case**: Privacy, fresh start, debugging

## 📁 File Operations Tools

### 13. **read_file**

**Purpose**: Read the contents of a file
**Workflow**:

```
File Path → File Existence Check → Content Reading → Content Return
```

**Use Case**: Reading configuration files, documents, code files

### 14. **write_file**

**Purpose**: Write content to a file
**Workflow**:

```
File Path + Content → Directory Creation (if needed) → File Writing → Success Confirmation
```

**Use Case**: Creating files, saving data, writing logs

### 15. **list_directory**

**Purpose**: List files and directories in a path
**Workflow**:

```
Directory Path → Path Validation → Directory Scanning → File List Return
```

**Use Case**: File system navigation, project exploration, directory management

### 16. **file_exists**

**Purpose**: Check if a file or directory exists
**Workflow**:

```
Path → Existence Check → Boolean Result Return
```

**Use Case**: File validation, conditional operations, error prevention

## 💻 System Information Tools

### 17. **get_system_info**

**Purpose**: Get general system information
**Workflow**:

```
Request → Platform Detection → System Info Collection → System Details Return
```

**Use Case**: System diagnostics, environment understanding, troubleshooting

### 18. **get_resource_usage**

**Purpose**: Get current system resource usage
**Workflow**:

```
Request → Resource Monitoring → Metrics Collection → Resource Report Return
```

**Use Case**: Performance monitoring, capacity planning, system health checks

### 19. **get_python_info**

**Purpose**: Get Python interpreter information
**Workflow**:

```
Request → Python Environment Check → Version/Path Info → Python Details Return
```

**Use Case**: Environment verification, dependency checking, debugging

### 20. **get_environment_vars**

**Purpose**: Get environment variables (filtered for security)
**Workflow**:

```
Request → Environment Scan → Variable Filtering → Safe Variables Return
```

**Use Case**: Configuration checking, environment debugging, security auditing

## 🧠 Cognitive Brain Plugin Tools

### 21. **think**

**Purpose**: Think and respond with memory and context
**Workflow**:

```
Message + Context → Memory Retrieval → Cognitive Processing → Thoughtful Response
```

**Use Case**: Deep thinking, problem solving, context-aware responses

### 22. **remember**

**Purpose**: Store important information with emotional weight
**Workflow**:

```
Information + Importance → Emotional Tagging → Memory Storage → Confirmation
```

**Use Case**: Learning, experience storage, important information retention

### 23. **recall**

**Purpose**: Search through memories and past experiences
**Workflow**:

```
Query + Depth → Memory Search → Pattern Matching → Relevant Memories Return
```

**Use Case**: Knowledge retrieval, experience recall, context building

### 24. **reflect**

**Purpose**: Engage in self-reflection and metacognition
**Workflow**:

```
Topic → Self-Analysis → Pattern Recognition → Reflection Results
```

**Use Case**: Learning improvement, self-awareness, performance analysis

### 25. **consciousness_check**

**Purpose**: Check current state of consciousness and awareness
**Workflow**:

```
Request → State Assessment → Awareness Check → Consciousness Report
```

**Use Case**: System health, cognitive state monitoring, debugging

### 26. **learn_from**

**Purpose**: Learn from text content or documents
**Workflow**:

```
Source + Lesson Type → Content Processing → Knowledge Extraction → Learning Confirmation
```

**Use Case**: Knowledge acquisition, document processing, continuous learning

### 27. **dream**

**Purpose**: Background processing and memory consolidation
**Workflow**:

```
Request → Background Processing → Memory Consolidation → Processing Status
```

**Use Case**: Memory optimization, background learning, system maintenance

## 🎯 Cursor Integration Tools

### 28. **get_cursor_context**

**Purpose**: Get comprehensive context for Cursor conversations
**Workflow**:

```
Request → Context Retrieval → User Info + History → Context Summary Return
```

**Use Case**: Cursor IDE integration, conversation continuity, user context

### 29. **track_cursor_conversation**

**Purpose**: Track Cursor conversation for learning and context
**Workflow**:

```
User Message + Assistant Response → Conversation Storage → Learning Update → Tracking Confirmation
```

**Use Case**: Conversation history, learning from interactions, context building

### 30. **cursor_auto_inject_context**

**Purpose**: Auto-inject relevant context for new Cursor conversations
**Workflow**:

```
Request → Context Analysis → Relevant Info Selection → Context Injection
```

**Use Case**: Seamless conversation flow, automatic context provision

## 🔍 Analysis and Monitoring Tools

### 31. **get_function_call_history**

**Purpose**: Get comprehensive function call history with traceability
**Workflow**:

```
Limit + Function Name → History Retrieval → Call Analysis → History Report
```

**Use Case**: Debugging, performance analysis, usage tracking

### 32. **get_session_statistics**

**Purpose**: Get comprehensive session statistics and performance metrics
**Workflow**:

```
Request → Statistics Collection → Metric Analysis → Performance Report
```

**Use Case**: Performance monitoring, usage analytics, system optimization

### 33. **search_function_calls**

**Purpose**: Search function calls by content, context, or parameters
**Workflow**:

```
Search Term + Limit → Function Call Search → Pattern Matching → Search Results
```

**Use Case**: Debugging, usage analysis, pattern recognition

### 34. **get_comprehensive_system_status**

**Purpose**: Get complete system status overview
**Workflow**:

```
Request → System Scan → Status Collection → Comprehensive Report
```

**Use Case**: System health checks, troubleshooting, performance monitoring

## 🧪 Testing and Validation Tools

### 35. **test_llm_connection**

**Purpose**: Test connection to the Ollama LLM service
**Workflow**:

```
Request → Connection Test → Service Validation → Connection Status Return
```

**Use Case**: System validation, troubleshooting, health checks

### 36. **test_memory_system**

**Purpose**: Test the memory system with sample conversations
**Workflow**:

```
Request → Sample Data Generation → Memory Operations Test → Test Results Return
```

**Use Case**: System testing, validation, debugging

### 37. **list_available_models**

**Purpose**: List available LLM models from Ollama
**Workflow**:

```
Request → Model Discovery → Model List Generation → Available Models Return
```

**Use Case**: Model selection, system configuration, capability discovery

## 🔄 Tool Workflow Patterns

### Basic Tool Usage Pattern

```
1. Tool Selection → 2. Parameter Preparation → 3. Tool Execution → 4. Result Processing → 5. Action/Response
```

### Memory-Enhanced Workflow

```
1. Context Retrieval → 2. Tool Execution → 3. Memory Storage → 4. Response Generation → 5. Learning Update
```

### Error Handling Workflow

```
1. Tool Execution → 2. Error Detection → 3. Error Logging → 4. Fallback Response → 5. User Notification
```

### Performance Monitoring Workflow

```
1. Tool Execution Start → 2. Performance Metrics Collection → 3. Tool Execution End → 4. Metrics Storage → 5. Performance Analysis
```

## 🎯 Best Practices for Tool Usage

### 1. **Tool Selection**

- Choose the most specific tool for your task
- Use memory tools for persistent information
- Leverage cognitive tools for complex thinking tasks

### 2. **Parameter Optimization**

- Provide clear, specific parameters
- Use appropriate data types
- Include relevant context when available

### 3. **Error Handling**

- Always check for errors in tool responses
- Implement fallback strategies
- Log errors for debugging

### 4. **Performance Considerations**

- Use lightweight tools for simple tasks
- Batch operations when possible
- Monitor tool execution times

### 5. **Memory Management**

- Store important information persistently
- Use tags for organization
- Clean up unnecessary data regularly

## 🚀 Advanced Tool Combinations

### Conversation Enhancement

```
get_cursor_context() → ai_chat_with_memory() → track_cursor_conversation()
```

### Problem Solving

```
think() → search_memory() → learn_from() → remember()
```

### System Monitoring

```
get_system_info() → get_resource_usage() → get_comprehensive_system_status()
```

### File Management

```
list_directory() → file_exists() → read_file() → write_file()
```

---

**💡 Pro Tip**: The tools are designed to work together seamlessly. Combine them to create powerful workflows that leverage the full capabilities of the Memory Context Manager v2 system.
