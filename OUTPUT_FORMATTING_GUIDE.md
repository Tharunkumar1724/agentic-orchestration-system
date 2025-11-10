# Workflow Output Formatting Guide

## Overview

The workflow execution system now provides **structured, clean output formatting** instead of raw nested JSON. You can choose from multiple output formats based on your needs.

## Output Formats

### 1. **Structured Format** (Default)
Clean, organized output with summary, results, and metadata.

**Best for:** Most use cases, API responses, frontend display

**Structure:**
```json
{
  "workflow_id": "my-workflow",
  "run_id": "abc-123",
  "status": "success",
  "timestamp": "2025-11-08T12:00:00",
  "summary": "Workflow completed successfully. Executed 2 node(s).",
  "results": {
    "node-1": {
      "node_id": "node-1",
      "agent": "Research Agent",
      "task": "Search for latest AI news",
      "response": "Here are the latest developments...",
      "tools_executed": [
        {
          "tool": "web-search-tool",
          "status": "success",
          "summary": "Found 5 results"
        }
      ]
    }
  },
  "metadata": {
    "total_nodes": 2,
    "agents_used": ["researcher-agent"],
    "execution_steps": 2
  }
}
```

### 2. **Compact Format**
Minimal output with only essential information.

**Best for:** Mobile apps, quick responses, bandwidth-limited scenarios

**Structure:**
```json
{
  "workflow_id": "my-workflow",
  "run_id": "abc-123",
  "status": "success",
  "summary": "Workflow completed successfully. Executed 2 node(s).",
  "node_responses": {
    "node-1": {
      "agent": "Research Agent",
      "response": "Here are the latest developments..."
    }
  }
}
```

### 3. **Text Format**
Human-readable report format.

**Best for:** Console output, reports, documentation, emails

**Example:**
```
================================================================================
WORKFLOW EXECUTION REPORT
================================================================================
Workflow ID: my-workflow
Run ID: abc-123
Status: SUCCESS
Timestamp: 2025-11-08T12:00:00

SUMMARY
--------------------------------------------------------------------------------
Workflow completed successfully. Executed 2 node(s).

DETAILED RESULTS
--------------------------------------------------------------------------------

[node-1]
  Agent: Research Agent
  Task: Search for latest AI news
  Response:
    Here are the latest developments in AI...
    
  Tools Used:
    - web-search-tool: Found 5 results

EXECUTION METADATA
--------------------------------------------------------------------------------
Total Nodes: 2
Agents Used: researcher-agent
Execution Steps: 2
================================================================================
```

### 4. **Raw Format**
Unformatted output with all technical details.

**Best for:** Debugging, development, advanced analysis

**Note:** This is the original format with full nested structures, communication logs, and internal state.

## Usage

### Via API

#### Using Query Parameter
```bash
# Structured format (default)
POST /workflows/{workflow_id}/run?format=structured

# Compact format
POST /workflows/{workflow_id}/run?format=compact

# Text format
POST /workflows/{workflow_id}/run?format=text

# Raw format
POST /workflows/{workflow_id}/run?format=raw
```

#### Using Request Body
```bash
curl -X POST "http://localhost:8000/workflows/my-workflow/run" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Tell me about AI",
    "format": "compact"
  }'
```

### Via Python

```python
from app.services.orchestrator import orchestrator
from app.services.output_formatter import output_formatter

# Run with formatted output (default)
result = await orchestrator.run_workflow(workflow, format_output=True)

# Run without formatting (raw)
result = await orchestrator.run_workflow(workflow, format_output=False)

# Convert to different formats
compact = output_formatter.format_compact(result)
text = output_formatter.format_for_display(result)
```

## Format Comparison

| Feature | Structured | Compact | Text | Raw |
|---------|-----------|---------|------|-----|
| **Size** | Medium | Small | Large | Very Large |
| **Readability** | High | Medium | Very High | Low |
| **Detail** | Medium | Low | High | Very High |
| **Best For** | API/Frontend | Mobile/Quick | Reports/Console | Debugging |
| **Technical Info** | Minimal | None | Some | All |

## Examples

### Example 1: Running with Structured Output

**Request:**
```bash
curl -X POST "http://localhost:8000/workflows/research-workflow/run" \
  -H "Content-Type: application/json" \
  -d '{"query": "Latest developments in quantum computing"}'
```

**Response:**
```json
{
  "workflow_id": "research-workflow",
  "run_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "success",
  "timestamp": "2025-11-08T14:30:00",
  "summary": "Workflow completed successfully. Executed 2 node(s).",
  "results": {
    "research-node": {
      "node_id": "research-node",
      "agent": "Research Agent",
      "task": "Latest developments in quantum computing",
      "response": "Recent breakthroughs in quantum computing include...",
      "tools_executed": [
        {
          "tool": "web-search-tool",
          "status": "success",
          "summary": "Found 5 results"
        }
      ]
    },
    "analysis-node": {
      "node_id": "analysis-node",
      "agent": "Analysis Agent",
      "task": "Analyze research findings",
      "response": "Based on the research, key insights are...",
      "tools_executed": []
    }
  },
  "metadata": {
    "total_nodes": 2,
    "agents_used": ["researcher-agent"],
    "execution_steps": 2
  }
}
```

### Example 2: Text Format for Console

```python
import asyncio
from app.services.orchestrator import orchestrator
from app.services.output_formatter import output_formatter
from app.storage import load

async def run_and_print():
    workflow = load("workflows", "my-workflow")
    result = await orchestrator.run_workflow(workflow)
    
    # Print as formatted text
    print(output_formatter.format_for_display(result))

asyncio.run(run_and_print())
```

## Benefits

✅ **Clean Output**: No more deeply nested JSON with technical internals
✅ **Flexible**: Choose the format that fits your use case
✅ **User-Friendly**: Easy to read and understand
✅ **Backwards Compatible**: Raw format still available for debugging
✅ **Efficient**: Compact format reduces bandwidth usage
✅ **Professional**: Text format perfect for reports and documentation

## Migration from Old Format

If you have existing code expecting the old raw format:

```python
# Old way (still works)
result = await run_workflow(workflow)
# result has deeply nested structure

# New way - get structured output
result = await run_workflow(workflow)
# result is clean and structured

# To get old format
result = await orchestrator.run_workflow(workflow, format_output=False)
# OR via API
GET /workflows/{id}/run?format=raw
```

## Customization

You can customize the formatter by modifying `app/services/output_formatter.py`:

```python
from app.services.output_formatter import OutputFormatter

class CustomFormatter(OutputFormatter):
    @staticmethod
    def _extract_response(node_result):
        # Your custom logic
        pass

# Use your custom formatter
output_formatter = CustomFormatter()
```

## Troubleshooting

### Output still showing raw format
- Check that `format_output=True` is set (default)
- Verify API request includes correct `format` parameter
- Ensure you're using the latest version of the orchestrator

### Missing data in compact format
- Compact format intentionally excludes technical details
- Use "structured" or "raw" format for complete data

### Text format too long
- Text format is verbose by design
- Use "compact" or "structured" for shorter output

## Best Practices

1. **Default to Structured**: Use structured format for most API responses
2. **Compact for Mobile**: Use compact format for mobile or bandwidth-limited clients
3. **Text for Humans**: Use text format when humans will read the output directly
4. **Raw for Debug**: Only use raw format when debugging or analyzing internals
5. **Store Formatted**: Save the formatted result, access raw via `_raw` key if needed

## Related

- [Workflow Execution Guide](WORKFLOW_EXECUTION.md)
- [API Reference](COMPLETE_URL_API_REFERENCE.md)
- [Output Formatter Source](../app/services/output_formatter.py)
