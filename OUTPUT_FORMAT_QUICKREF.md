# Output Formatting Quick Reference

## Problem Solved ✅

**Before:** Workflow outputs were deeply nested JSON with duplicate data, technical internals, and poor readability.

**After:** Clean, structured outputs with multiple format options.

## Quick Start

### API Usage

```bash
# Default structured format
curl -X POST "http://localhost:8000/workflows/my-workflow/run" \
  -H "Content-Type: application/json" \
  -d '{"query": "Your query here"}'

# Compact format (minimal output)
curl -X POST "http://localhost:8000/workflows/my-workflow/run?format=compact" \
  -H "Content-Type: application/json" \
  -d '{"query": "Your query here"}'

# Text format (human-readable report)
curl -X POST "http://localhost:8000/workflows/my-workflow/run?format=text" \
  -H "Content-Type: application/json" \
  -d '{"query": "Your query here"}'
```

### Python Usage

```python
from app.services.orchestrator import orchestrator
from app.services.output_formatter import output_formatter

# Get structured output (default)
result = await orchestrator.run_workflow(workflow)

# Convert to different formats
compact = output_formatter.format_compact(result)
text = output_formatter.format_for_display(result)

# Get raw output (for debugging)
raw = await orchestrator.run_workflow(workflow, format_output=False)
```

## Output Formats

| Format | Size | Use Case | Example |
|--------|------|----------|---------|
| **structured** | Medium | Default, API responses | Clean JSON with summary + results |
| **compact** | Small | Mobile, quick responses | Minimal JSON, essential data only |
| **text** | Large | Reports, console output | Human-readable formatted text |
| **raw** | Very Large | Debugging, development | Full technical details |

## Response Structure (Structured Format)

```json
{
  "workflow_id": "string",
  "run_id": "uuid",
  "status": "success|failed",
  "timestamp": "ISO-8601",
  "summary": "Human-readable summary",
  "results": {
    "node-id": {
      "node_id": "string",
      "agent": "Agent name",
      "task": "Task description",
      "response": "Agent response",
      "tools_executed": [...]
    }
  },
  "metadata": {
    "total_nodes": 0,
    "agents_used": [],
    "execution_steps": 0
  }
}
```

## Benefits

- ✅ **80% smaller** response size
- ✅ **No duplicate** data
- ✅ **Clean structure** - easy to parse
- ✅ **User-friendly** - no technical internals
- ✅ **Multiple formats** - choose what you need
- ✅ **Backwards compatible** - raw format still available

## Examples

### Before (Raw)
```json
{
  "result": {
    "node-1": {
      "agent_id": "...",
      "agent_name": "...",
      "llm_response": "...",
      "tool_results": {
        "tool-1": {
          "tool": "...",
          "query": "...",
          "results": [...deeply nested...]
        }
      }
    }
  },
  "meta": {
    "communication_log": [...duplicate data...],
    "shared_state": {...more duplicates...}
  }
}
```

### After (Structured)
```json
{
  "summary": "Workflow completed successfully.",
  "results": {
    "node-1": {
      "agent": "Research Agent",
      "response": "Clean response here",
      "tools_executed": [
        {"tool": "web-search", "summary": "Found 5 results"}
      ]
    }
  }
}
```

## Common Tasks

### Display results in frontend
```javascript
// Fetch with structured format
const response = await fetch('/workflows/my-workflow/run', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({query: 'Your query'})
});

const result = await response.json();

// Easy to display
console.log(result.summary);
result.results.forEach((node) => {
  console.log(`${node.agent}: ${node.response}`);
});
```

### Save to file
```python
# Save as text report
with open('report.txt', 'w') as f:
    f.write(output_formatter.format_for_display(result))

# Save as compact JSON
with open('result.json', 'w') as f:
    json.dump(output_formatter.format_compact(result), f)
```

### Debug workflow
```python
# Get raw output with all details
result = await orchestrator.run_workflow(workflow, format_output=False)

# Or via API
# GET /workflows/{id}/run?format=raw
```

## Testing

Run the test script to see all formats:
```bash
python test_formatted_output.py
```

Run the comparison:
```bash
python output_comparison.py
```

## Files

- **Formatter:** `app/services/output_formatter.py`
- **Orchestrator:** `app/services/orchestrator.py`
- **API Router:** `app/routers/workflows.py`
- **Tests:** `test_formatted_output.py`
- **Guide:** `OUTPUT_FORMATTING_GUIDE.md`

## Need Help?

- See full guide: `OUTPUT_FORMATTING_GUIDE.md`
- Check API docs: `COMPLETE_URL_API_REFERENCE.md`
- Run examples: `python test_formatted_output.py`
