# KAG (Knowledge-Aided Generation) with LangGraph

## 🎯 Overview

The KAG (Knowledge-Aided Generation) service is a sophisticated workflow intelligence system built with **LangGraph** that extracts facts, generates summaries, and manages memory across multi-workflow solutions.

## 🏗️ Architecture

### LangGraph State Machine

The KAG service implements a 4-node sequential workflow using LangGraph:

```
START → Retrieve Context → Extract Facts → Generate Summary → Store Memory → END
```

### State Schema

```python
class KAGState(TypedDict):
    workflow_output: str        # Input workflow execution result
    workflow_name: str          # Name of the workflow
    solution_id: str            # ID of parent solution
    workflow_id: str            # Unique workflow identifier
    context: str                # Additional context
    previous_context: str       # Retrieved historical context
    facts: List[str]            # Extracted facts
    summary: str                # Generated summary
    reasoning: str              # LLM reasoning
    memory_stored: bool         # Storage confirmation
    error: Optional[str]        # Error handling
```

## 🔄 Workflow Nodes

### Node 1: Retrieve Context
**Purpose:** Load previous workflow outputs from memory

**Operations:**
- Get solution context from ConversationMemory
- Build full context with historical data
- Combine with current workflow context

**State Updates:**
- `previous_context`: Historical workflow summaries
- `context`: Full context for LLM processing

### Node 2: Extract Facts
**Purpose:** Analyze workflow output using Gemini AI

**Operations:**
- Send output + context to Gemini
- Extract key facts and insights
- Generate reasoning explanation

**State Updates:**
- `facts`: List of extracted facts
- `reasoning`: LLM reasoning process

### Node 3: Generate Summary
**Purpose:** Create concise summary from facts

**Operations:**
- Use Gemini to synthesize facts
- Generate 2-3 sentence summary
- Fallback to basic summary if needed

**State Updates:**
- `summary`: Concise workflow summary

### Node 4: Store Memory
**Purpose:** Persist results for future workflows

**Operations:**
- Create memory entry with facts/summary/reasoning
- Store in ConversationMemory
- Mark storage success

**State Updates:**
- `memory_stored`: Storage confirmation flag

## 🚀 Usage

### Basic Invocation

```python
from app.services.kag_service import get_kag_service

service = get_kag_service()

result = service.invoke_kag(
    workflow_output="Analysis complete. Found 3 key insights...",
    workflow_name="Market Analysis",
    solution_id="solution_001",
    workflow_id="workflow_001",
    context="Q3 business metrics"
)

print(result["summary"])    # Summary of workflow
print(result["facts"])      # Extracted facts
print(result["reasoning"])  # LLM reasoning
```

### Multi-Workflow Context

```python
# Workflow 1
service.invoke_kag(
    workflow_output="Collected 10,000 customer records",
    workflow_name="Data Collection",
    solution_id="solution_001",
    workflow_id="wf_001",
    context="Initial data gathering"
)

# Workflow 2 (has context from Workflow 1)
result = service.invoke_kag(
    workflow_output="Analysis reveals 3 customer segments",
    workflow_name="Data Analysis",
    solution_id="solution_001",
    workflow_id="wf_002",
    context="Analyzing collected data"
)

# result["context_available"] == True
```

### Workflow Handoff

```python
# Prepare handoff from one workflow to next
handoff = service.prepare_handoff(
    source_workflow_id="research_wf",
    target_workflow_id="planning_wf",
    target_workflow_description="Create business plan",
    solution_id="solution_001"
)

print(handoff["handoff_data"])  # Structured data for next workflow
print(handoff["facts"])         # Relevant facts
print(handoff["relevance"])     # Why facts matter
```

### Solution Summary

```python
# Get comprehensive summary of all workflows
summary = service.get_solution_summary("solution_001")

print(summary["total_workflows"])   # Number of workflows
print(summary["combined_facts"])    # All facts
print(summary["overall_context"])   # LLM-generated summary
print(summary["summaries"])         # Individual workflow summaries
```

## 🧪 Testing

### Run All Tests

```powershell
python test_kag_langgraph.py
```

### Test Coverage

1. **Basic KAG Invocation** - Single workflow processing
2. **Multi-Workflow Context** - Context preservation across 3 workflows
3. **Handoff Preparation** - Workflow-to-workflow data transfer
4. **Solution Summary** - Aggregated summary generation
5. **Memory Management** - Memory storage and cleanup
6. **Error Handling** - Empty/long output handling
7. **LangGraph State Transitions** - Verify state machine
8. **Singleton Pattern** - Service instance management

### Expected Output

```
✅ PASS  Basic KAG Invocation
✅ PASS  Multi-Workflow Context
✅ PASS  Handoff Preparation
✅ PASS  Solution Summary
✅ PASS  Memory Management
✅ PASS  Error Handling
✅ PASS  LangGraph State Transitions
✅ PASS  Singleton Pattern

Total Tests: 8
✅ Passed: 8
❌ Failed: 0
Success Rate: 100.0%
```

## 📊 Visualization

```powershell
python visualize_kag_graph.py
```

Shows ASCII diagram of the LangGraph state machine with all nodes and edges.

## 🎨 Features

### ✅ Sequential Workflow Execution
- LangGraph manages state transitions
- Each node processes sequentially
- Clean separation of concerns

### ✅ Context Preservation
- Memory persists across workflows
- Previous outputs inform current processing
- Solution-wide intelligence

### ✅ Gemini AI Integration
- Fact extraction from unstructured text
- Reasoning generation
- Summary creation
- Handoff analysis

### ✅ Error Handling
- Each node handles errors gracefully
- State includes error field
- Fallback mechanisms for LLM failures

### ✅ Singleton Pattern
- Global service instance
- Shared memory across calls
- Efficient resource usage

## 🔧 Configuration

### Environment Variables

```env
GEMINI_API_KEY=your-gemini-api-key-here
```

### Dependencies

```
langgraph>=0.2.0
langchain>=0.1.0
langchain-core>=0.1.0
```

## 📈 Performance

### Metrics

- **Average Processing Time**: ~2-5 seconds per workflow
- **Memory Usage**: O(n) where n = number of workflows
- **Context Preservation**: 100% across workflows
- **Fact Extraction Accuracy**: Depends on Gemini model

### Optimization Tips

1. **Batch Processing**: Process multiple workflows in solution
2. **Context Limits**: Truncate very long outputs to 500 chars
3. **Memory Cleanup**: Clear solution memory when done
4. **Caching**: Singleton pattern reduces initialization overhead

## 🔍 API Reference

### KAGService

#### `invoke_kag(workflow_output, workflow_name, solution_id, workflow_id, context="")`

Main entry point for KAG processing.

**Parameters:**
- `workflow_output` (str): Raw workflow execution result
- `workflow_name` (str): Name of the workflow
- `solution_id` (str): Parent solution identifier
- `workflow_id` (str): Unique workflow identifier
- `context` (str): Additional context (optional)

**Returns:**
```python
{
    "summary": str,              # Concise workflow summary
    "facts": List[str],          # Extracted facts
    "reasoning": str,            # LLM reasoning
    "memory_stored": bool,       # Storage confirmation
    "context_available": bool    # Previous context exists
}
```

#### `prepare_handoff(source_workflow_id, target_workflow_id, target_workflow_description, solution_id)`

Prepare data handoff between workflows.

**Returns:**
```python
{
    "handoff_data": str,         # Structured handoff data
    "relevance": str,            # Why data matters
    "facts": List[str],          # Relevant facts
    "source_summary": str        # Source workflow summary
}
```

#### `get_solution_summary(solution_id)`

Get aggregated summary of all workflows.

**Returns:**
```python
{
    "total_workflows": int,      # Workflow count
    "summaries": List[Dict],     # Individual summaries
    "combined_facts": List[str], # All facts
    "overall_context": str       # LLM summary
}
```

#### `clear_solution_memory(solution_id)`

Clear all memory for a solution.

### ConversationMemory

#### `add_memory(solution_id, workflow_id, memory)`

Store workflow memory.

#### `get_memories(solution_id, workflow_id=None)`

Retrieve memories for solution or specific workflow.

#### `get_solution_context(solution_id)`

Get formatted context string for solution.

#### `clear_solution(solution_id)`

Clear all memories for solution.

## 🐛 Troubleshooting

### Issue: "GEMINI_API_KEY not found"
**Solution:** Set environment variable in `.env` file

### Issue: Facts array is empty
**Solution:** Ensure workflow output has meaningful content

### Issue: Context not preserved
**Solution:** Use same `solution_id` across workflows

### Issue: Memory grows too large
**Solution:** Call `clear_solution_memory()` when done

## 🚀 Advanced Usage

### Custom LLM Provider

Modify `gemini_client.py` to use different LLM:

```python
# app/services/kag_service.py
from .your_llm_client import get_your_llm_client

class KAGService:
    def __init__(self):
        self.llm_client = get_your_llm_client()
        # ... rest of code
```

### Parallel Processing

For independent workflows, process in parallel:

```python
from concurrent.futures import ThreadPoolExecutor

workflows = [...]

with ThreadPoolExecutor(max_workers=3) as executor:
    results = executor.map(
        lambda w: service.invoke_kag(
            w["output"], w["name"], solution_id, w["id"]
        ),
        workflows
    )
```

### Custom State Fields

Extend `KAGState` for domain-specific needs:

```python
class CustomKAGState(KAGState):
    custom_field: str
    domain_data: Dict[str, Any]
```

## 📝 Best Practices

1. ✅ **Use Descriptive Names**: Clear workflow names improve summaries
2. ✅ **Provide Context**: Include relevant context for better fact extraction
3. ✅ **Clean Up Memory**: Call `clear_solution_memory()` when done
4. ✅ **Handle Errors**: Check for `error` field in results
5. ✅ **Singleton Pattern**: Use `get_kag_service()` not `KAGService()`
6. ✅ **Test Thoroughly**: Run `test_kag_langgraph.py` after changes

## 🎓 Examples

See `test_kag_langgraph.py` for comprehensive examples of:
- Basic invocation
- Multi-workflow chains
- Handoff preparation
- Solution summaries
- Memory management

## 📄 License

Part of the Agentic Orchestration System - MIT License

---

**Built with LangGraph 🦜🔗 and Gemini AI 🤖**
