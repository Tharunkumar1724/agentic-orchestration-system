# Tool Orchestration Architecture

## Overview

The Tool Orchestration system is a comprehensive, enterprise-level architecture for managing and executing diverse tool types across the agentic application. It provides advanced features including multiple execution strategies, retry mechanisms, fallback handling, and detailed execution tracking.

## Architecture Components

### Backend (Python)

#### Core Module: `tool_orchestrator.py`

Located in `app/services/tool_orchestrator.py`, this module provides the foundation for all tool operations.

**Key Classes:**

1. **ToolType (Enum)**
   ```python
   class ToolType(Enum):
       WEBSEARCH = "websearch"
       API = "api"
       CODE = "code"
       DATABASE = "database"
       FILE = "file"
       PYTHON = "python"
       SHELL = "shell"
       HTTP = "http"
       GRAPHQL = "graphql"
       CUSTOM = "custom"
   ```

2. **ToolExecutionStrategy (Enum)**
   ```python
   class ToolExecutionStrategy(Enum):
       SEQUENTIAL = "sequential"   # One at a time, pass results between
       PARALLEL = "parallel"       # All at once, independent
       CONDITIONAL = "conditional" # Based on conditions
       RETRY = "retry"            # With automatic retries
       FALLBACK = "fallback"      # Try alternatives on failure
   ```

3. **ToolResult (Class)**
   - Standardized response format for all tools
   - Fields: `success`, `data`, `error`, `metadata`, `execution_time`, `timestamp`
   - Provides `to_dict()` for serialization

4. **ToolOrchestrator (Class)**
   - Main orchestration engine
   - Handles all tool types with dedicated handlers
   - Implements all execution strategies
   - Tracks execution history and statistics

### Tool Type Handlers

Each tool type has a dedicated async handler method:

#### 1. Web Search (`_handle_websearch`)
- **Integration**: DuckDuckGo Search (DDGS)
- **Features**: 
  - Region-specific search
  - SafeSearch controls
  - Time-limited results
  - Configurable result count
- **Response**: List of search results with title, URL, snippet

#### 2. API (`_handle_api`)
- **Methods**: GET, POST, PUT, DELETE, PATCH
- **Features**:
  - Custom headers support
  - Request/response timeout
  - JSON/form data handling
  - Authentication headers
- **Response**: Status code, response body, headers

#### 3. HTTP (`_handle_http`)
- **Similar to API** but with enhanced HTTP-specific features
- **Additional**: Cookie management, redirect handling

#### 4. GraphQL (`_handle_graphql`)
- **Features**:
  - Query and mutation support
  - Variable handling
  - Error parsing
- **Response**: GraphQL data and errors

#### 5. Code Execution (`_handle_code`)
- **Safety**: Sandboxed execution environment
- **Languages**: Python (default), extensible to others
- **Features**: Timeout controls, output capture
- **Response**: Execution output and exit code

#### 6. Python Scripts (`_handle_python`)
- **Execution**: Via subprocess
- **Features**:
  - Script file or inline code
  - Environment variables
  - Working directory control
- **Response**: stdout, stderr, return code

#### 7. Shell Commands (`_handle_shell`)
- **Platform**: Cross-platform support
- **Features**:
  - Command chaining
  - Environment variables
  - Working directory
- **Response**: Command output

#### 8. Database (`_handle_database`)
- **Support**: PostgreSQL, MySQL, SQLite (extensible)
- **Features**:
  - Connection pooling
  - Parameterized queries
  - Transaction support
- **Response**: Query results or affected rows

#### 9. File Operations (`_handle_file`)
- **Operations**: Read, write, append, delete, list
- **Features**:
  - Path validation
  - Encoding support
  - Binary/text modes
- **Response**: File content or operation status

#### 10. Custom Tools (`_handle_custom`)
- **Extensibility**: Plugin architecture
- **Features**:
  - Dynamic tool loading
  - Custom validation
  - Flexible I/O
- **Response**: Tool-specific format

### Execution Strategies

#### 1. Sequential Execution
```python
async def _execute_sequential(self, tools, inputs, context)
```
- **Use Case**: Tools with dependencies on previous results
- **Behavior**: Executes tools one at a time in order
- **Context Passing**: Each tool receives results from previous tool
- **Best For**: Workflows where output of one tool feeds into next

**Example Flow:**
```
Tool 1 (Search) → Results → Tool 2 (Analyze) → Results → Tool 3 (Summarize)
```

#### 2. Parallel Execution
```python
async def _execute_parallel(self, tools, inputs, context)
```
- **Use Case**: Independent tools that can run simultaneously
- **Behavior**: Uses `asyncio.gather()` to run all tools concurrently
- **Performance**: Significantly faster for independent operations
- **Best For**: Multiple searches, API calls, or data fetches

**Example Flow:**
```
Tool 1 (Search A) ┐
Tool 2 (Search B) ├─> All execute simultaneously → Combined results
Tool 3 (API Call) ┘
```

#### 3. Conditional Execution
```python
async def _execute_conditional(self, tools, inputs, context)
```
- **Use Case**: Dynamic execution based on conditions
- **Behavior**: Evaluates conditions before executing each tool
- **Conditions**: Based on previous results or context
- **Best For**: Adaptive workflows with branching logic

**Example Flow:**
```
Tool 1 → If success → Tool 2A
      → If failure → Tool 2B
```

#### 4. Retry Execution
```python
async def _execute_with_retry(self, tools, inputs, context)
```
- **Use Case**: Unreliable tools or network operations
- **Behavior**: Automatically retries failed tools with exponential backoff
- **Configuration**: Max retries, backoff multiplier
- **Best For**: API calls, web searches, external services

**Example Flow:**
```
Tool Execute → Fail → Wait 1s → Retry → Fail → Wait 2s → Retry → Success
```

#### 5. Fallback Execution
```python
async def _execute_with_fallback(self, tools, inputs, context)
```
- **Use Case**: Critical operations that must succeed
- **Behavior**: Tries alternative tools if primary fails
- **Chain**: Ordered list of fallback tools
- **Best For**: Mission-critical operations with backup options

**Example Flow:**
```
Primary Tool → Fail → Fallback 1 → Fail → Fallback 2 → Success
```

### Integration with Main Orchestrator

The tool orchestrator is integrated into `orchestrator.py`:

```python
from app.services.tool_orchestrator import (
    tool_orchestrator,
    ToolExecutionStrategy
)

async def run_agent(self, agent_def, task, state):
    # ... agent setup ...
    
    # Determine execution strategy from agent config
    execution_strategy = agent_def.get("tool_execution_strategy", "sequential")
    strategy_map = {
        "sequential": ToolExecutionStrategy.SEQUENTIAL,
        "parallel": ToolExecutionStrategy.PARALLEL,
        "conditional": ToolExecutionStrategy.CONDITIONAL,
        "retry": ToolExecutionStrategy.RETRY,
        "fallback": ToolExecutionStrategy.FALLBACK
    }
    strategy = strategy_map.get(execution_strategy, ToolExecutionStrategy.SEQUENTIAL)
    
    # Execute tools using orchestrator
    results = await tool_orchestrator.execute_tools(
        tools_to_execute,
        tool_inputs,
        execution_context,
        strategy
    )
```

## Frontend (React)

### Component: `ToolOrchestration.js`

Located in `frontend/src/components/ToolOrchestration.js`

**Features:**
1. **Tool Type Visualization**
   - Icons and colors for each tool type
   - Tool type selection interface
   - Visual indicators for active tools

2. **Execution Strategy Selector**
   - Cards for each strategy
   - Detailed descriptions
   - Visual feedback on selection

3. **Execution History Viewer**
   - Real-time execution tracking
   - Success/failure indicators
   - Execution time display
   - Retry count visualization
   - Error message display
   - Result preview

4. **Statistics Dashboard**
   - Total executions
   - Success/failure rates
   - Average execution time
   - Tool usage patterns

### Tool Type Icons and Colors

```javascript
const TOOL_TYPES = {
  websearch: { icon: Globe, color: 'blue', label: 'Web Search' },
  api: { icon: Network, color: 'green', label: 'API Call' },
  http: { icon: Zap, color: 'purple', label: 'HTTP Request' },
  graphql: { icon: GitBranch, color: 'pink', label: 'GraphQL' },
  code: { icon: Code, color: 'yellow', label: 'Code Execution' },
  python: { icon: Terminal, color: 'cyan', label: 'Python Script' },
  shell: { icon: Terminal, color: 'gray', label: 'Shell Command' },
  database: { icon: Database, color: 'indigo', label: 'Database Query' },
  file: { icon: FileText, color: 'orange', label: 'File Operation' },
  custom: { icon: Wrench, color: 'red', label: 'Custom Tool' }
};
```

## Usage Examples

### Agent Configuration with Tool Strategy

```yaml
id: "research-agent"
name: "Research Agent"
type: "zero_shot"
system_prompt: "You are a research assistant"
tool_execution_strategy: "parallel"  # Use parallel execution
tools:
  - "websearch-google"
  - "websearch-academic"
  - "api-wikipedia"
```

### Custom Tool Definition

```yaml
id: "custom-analyzer"
name: "Data Analyzer"
type: "custom"
config:
  handler: "analyze_data"
  timeout: 30
  retry_count: 3
```

### Conditional Execution Example

```yaml
tool_execution_strategy: "conditional"
tools:
  - id: "check-cache"
    type: "database"
    condition: "always"
  - id: "fetch-api"
    type: "api"
    condition: "if_cache_miss"
  - id: "process-data"
    type: "python"
    condition: "if_data_found"
```

### Fallback Chain Example

```yaml
tool_execution_strategy: "fallback"
tools:
  - id: "primary-search"
    type: "websearch"
    config:
      engine: "google"
  - id: "backup-search"
    type: "websearch"
    config:
      engine: "duckduckgo"
  - id: "tertiary-search"
    type: "api"
    config:
      url: "https://api.search.example.com"
```

## Execution Flow

### Complete Tool Execution Lifecycle

```
1. Agent Receives Task
   ↓
2. Load Agent Configuration
   ↓
3. Determine Execution Strategy
   ↓
4. Collect Tools to Execute
   ↓
5. ToolOrchestrator.execute_tools()
   ↓
6. Strategy-Specific Execution
   - Sequential: One by one
   - Parallel: All at once
   - Conditional: Evaluate conditions
   - Retry: With backoff
   - Fallback: Try alternatives
   ↓
7. Tool-Specific Handler
   - _handle_websearch()
   - _handle_api()
   - etc.
   ↓
8. Collect Results
   ↓
9. Build ToolResult Objects
   ↓
10. Update Execution History
   ↓
11. Return Results to Agent
   ↓
12. Agent Processes Results
   ↓
13. Update Frontend Visualization
```

## Error Handling

### Tool-Level Errors
- Caught in individual handlers
- Returned as ToolResult with `success=False`
- Error message in `error` field
- Metadata includes error type and traceback

### Strategy-Level Errors
- Retry strategy: Automatic retry with backoff
- Fallback strategy: Try next tool in chain
- Conditional strategy: Skip failed conditions
- All strategies: Log errors, continue execution

### System-Level Errors
- Logged to execution history
- Returned to frontend for display
- Agent receives error notification
- Workflow continues with partial results

## Performance Considerations

### Parallel Execution
- **Speedup**: N tools execute in time of slowest tool
- **Resource Usage**: Higher memory and CPU during execution
- **Best Practice**: Use for I/O-bound operations

### Sequential Execution
- **Reliability**: Easy to debug, predictable
- **Resource Usage**: Minimal, one tool at a time
- **Best Practice**: Use for dependent operations

### Retry Strategy
- **Exponential Backoff**: 1s, 2s, 4s, 8s, etc.
- **Max Retries**: Configurable (default: 3)
- **Best Practice**: Use for network operations

## Monitoring and Analytics

### Execution History
- Every tool execution is recorded
- Includes: tool_id, success, error, execution_time, timestamp
- Accessible via `tool_orchestrator.execution_history`

### Statistics
```python
stats = tool_orchestrator.get_execution_stats()
# Returns:
# {
#   "total_executions": 150,
#   "successful_executions": 142,
#   "failed_executions": 8,
#   "average_execution_time": 1.234,
#   "tool_type_usage": {
#     "websearch": 50,
#     "api": 45,
#     "code": 30,
#     ...
#   }
# }
```

### Frontend Visualization
- Real-time execution tracking
- Visual indicators for success/failure
- Execution time graphs
- Tool usage patterns

## Extension Points

### Adding New Tool Types

1. **Add to ToolType enum:**
```python
class ToolType(Enum):
    # ... existing types ...
    MY_NEW_TOOL = "my_new_tool"
```

2. **Create handler method:**
```python
async def _handle_my_new_tool(self, tool_def, inputs, context):
    # Implementation
    return ToolResult(
        success=True,
        data={"result": "data"},
        metadata={"tool_type": "my_new_tool"}
    )
```

3. **Add to execute_tool() dispatch:**
```python
elif tool_type == ToolType.MY_NEW_TOOL:
    return await self._handle_my_new_tool(tool_def, inputs, context)
```

4. **Update frontend tool types:**
```javascript
const TOOL_TYPES = {
  // ... existing types ...
  my_new_tool: { icon: MyIcon, color: 'teal', label: 'My New Tool' }
};
```

### Adding New Execution Strategies

1. **Add to ToolExecutionStrategy enum:**
```python
class ToolExecutionStrategy(Enum):
    # ... existing strategies ...
    MY_STRATEGY = "my_strategy"
```

2. **Implement strategy method:**
```python
async def _execute_my_strategy(self, tools, inputs, context):
    # Implementation
    results = []
    # ... custom logic ...
    return results
```

3. **Add to execute_tools() dispatch:**
```python
elif strategy == ToolExecutionStrategy.MY_STRATEGY:
    return await self._execute_my_strategy(tools, inputs, context)
```

4. **Update frontend strategies:**
```javascript
const EXECUTION_STRATEGIES = [
  // ... existing strategies ...
  {
    id: 'my_strategy',
    name: 'My Strategy',
    description: 'Custom execution strategy',
    icon: MyIcon,
    color: 'teal'
  }
];
```

## Best Practices

### Tool Configuration
- Always specify timeout values
- Use appropriate execution strategy
- Configure retry counts for unreliable tools
- Set up fallback chains for critical operations

### Error Handling
- Always check `ToolResult.success` before using data
- Log errors for debugging
- Provide meaningful error messages
- Use fallback strategies for resilience

### Performance
- Use parallel execution for independent tools
- Implement caching for expensive operations
- Set reasonable timeouts
- Monitor execution times and optimize slow tools

### Security
- Validate all inputs before execution
- Sanitize shell commands
- Use parameterized database queries
- Restrict file system access
- Implement rate limiting for external APIs

## Testing

### Unit Tests
```python
# Test individual tool handlers
async def test_websearch_handler():
    result = await tool_orchestrator._handle_websearch(
        {"type": "websearch", "config": {"max_results": 5}},
        {"query": "test query"},
        {}
    )
    assert result.success
    assert len(result.data["results"]) > 0
```

### Integration Tests
```python
# Test execution strategies
async def test_parallel_execution():
    tools = [
        {"id": "tool1", "type": "websearch"},
        {"id": "tool2", "type": "api"}
    ]
    results = await tool_orchestrator.execute_tools(
        tools,
        {"query": "test"},
        {},
        ToolExecutionStrategy.PARALLEL
    )
    assert len(results) == 2
```

### End-to-End Tests
```python
# Test complete workflow with tools
async def test_agent_with_tools():
    workflow = load_workflow("test-workflow")
    result = await orchestrator.execute_workflow(workflow, {"task": "test task"})
    assert result["status"] == "completed"
```

## Troubleshooting

### Common Issues

**Issue**: Tools timing out
- **Solution**: Increase timeout in tool config
- **Check**: Network connectivity, API rate limits

**Issue**: Parallel execution slower than sequential
- **Solution**: Use sequential for CPU-bound tasks
- **Explanation**: Parallel is best for I/O-bound operations

**Issue**: Retry strategy not working
- **Solution**: Check error types are retriable
- **Configuration**: Adjust max_retries and backoff settings

**Issue**: Tools not showing in frontend
- **Solution**: Verify tool type in TOOL_TYPES constant
- **Check**: API response format matches expected structure

## Future Enhancements

1. **Advanced Caching**
   - Result caching with TTL
   - Distributed cache support
   - Cache invalidation strategies

2. **Tool Composition**
   - Composite tools from multiple tools
   - Tool pipelines
   - Reusable tool templates

3. **Enhanced Monitoring**
   - Real-time metrics dashboard
   - Alert system for failures
   - Performance analytics

4. **Security Features**
   - Tool access control
   - Rate limiting per tool
   - Audit logging

5. **AI-Powered Optimization**
   - Automatic strategy selection
   - Tool recommendation
   - Performance prediction

## Conclusion

The Tool Orchestration Architecture provides a robust, scalable foundation for managing diverse tool types in the agentic application. With support for 10 tool types, 5 execution strategies, comprehensive error handling, and detailed monitoring, it enables complex, reliable workflows while maintaining simplicity and extensibility.
