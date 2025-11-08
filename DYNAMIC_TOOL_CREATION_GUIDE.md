# Dynamic Tool Creation Guide

## Overview

The Dynamic Tool Creation system allows you to create tools on-the-fly without manually writing YAML files. This is perfect for:

- **Rapid prototyping** - Create and test tools instantly
- **User-generated tools** - Let users define custom integrations
- **Programmatic tool management** - Generate tools based on runtime conditions
- **Template-based workflows** - Use predefined patterns for common tasks

---

## Quick Start

### 1. Create a DuckDuckGo Search Tool (Simplest)

```bash
curl -X POST http://localhost:8000/tools/dynamic/duckduckgo \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Web Search",
    "max_results": 5,
    "region": "us-en"
  }'
```

**Python:**
```python
import requests

response = requests.post("http://localhost:8000/tools/dynamic/duckduckgo", json={
    "name": "My Web Search",
    "max_results": 5,
    "region": "us-en"
})

tool = response.json()
print(f"Created tool: {tool['tool']['id']}")
```

---

### 2. Create from Template

```bash
curl -X POST http://localhost:8000/tools/dynamic/from-template \
  -H "Content-Type: application/json" \
  -d '{
    "template": "duckduckgo_search",
    "name": "News Search",
    "config_overrides": {
      "max_results": 10,
      "timelimit": "d"
    }
  }'
```

---

### 3. Create Custom Tool

```python
import requests

custom_tool = {
    "name": "GitHub API",
    "type": "api",
    "config": {
        "url": "https://api.github.com",
        "method": "GET",
        "headers": {
            "Accept": "application/vnd.github.v3+json"
        }
    },
    "input_schema": {
        "type": "object",
        "properties": {
            "endpoint": {"type": "string"}
        }
    }
}

response = requests.post(
    "http://localhost:8000/tools/dynamic/custom",
    json=custom_tool
)
```

---

## Available Templates

### List Templates

```bash
curl http://localhost:8000/tools/dynamic/templates
```

**Response:**
```json
{
  "templates": [
    {
      "template": "duckduckgo_search",
      "type": "websearch",
      "description": "Template for duckduckgo search tools"
    },
    {
      "template": "api_rest",
      "type": "api",
      "description": "Template for api rest tools"
    },
    ...
  ]
}
```

### Get Template Schema

```bash
curl http://localhost:8000/tools/dynamic/templates/duckduckgo_search
```

---

## Tool Templates Reference

### 1. DuckDuckGo Search (`duckduckgo_search`)

**Purpose:** Web search using DuckDuckGo

**Config Options:**
- `max_results` (int): Number of results (default: 5)
- `region` (string): Region code (default: "wt-wt")
- `safesearch` (string): "strict", "moderate", or "off"
- `timelimit` (string): "d" (day), "w" (week), "m" (month), null (all time)

**Example:**
```json
{
  "template": "duckduckgo_search",
  "name": "Academic Search",
  "config_overrides": {
    "max_results": 15,
    "safesearch": "strict"
  }
}
```

---

### 2. REST API (`api_rest`)

**Purpose:** Make HTTP API calls

**Config Options:**
- `url` (string): Base URL
- `method` (string): GET, POST, PUT, DELETE, PATCH
- `headers` (object): HTTP headers
- `timeout` (float): Request timeout in seconds

**Example:**
```json
{
  "template": "api_rest",
  "name": "Weather API",
  "config_overrides": {
    "url": "https://api.weather.gov",
    "headers": {"User-Agent": "MyApp/1.0"}
  }
}
```

---

### 3. GraphQL API (`api_graphql`)

**Purpose:** Execute GraphQL queries

**Config Options:**
- `url` (string): GraphQL endpoint
- `timeout` (float): Request timeout
- `headers` (object): HTTP headers

**Example:**
```json
{
  "template": "api_graphql",
  "name": "GitHub GraphQL",
  "config_overrides": {
    "url": "https://api.github.com/graphql",
    "headers": {
      "Authorization": "Bearer YOUR_TOKEN"
    }
  }
}
```

---

### 4. File Reader (`file_reader`)

**Purpose:** Read files from disk

**Config Options:**
- `encoding` (string): File encoding (default: "utf-8")
- `safe_path_check` (bool): Validate file paths

**Example:**
```json
{
  "template": "file_reader",
  "name": "Config Reader",
  "config_overrides": {
    "encoding": "utf-8"
  }
}
```

---

### 5. File Writer (`file_writer`)

**Purpose:** Write files to disk

**Config Options:**
- `encoding` (string): File encoding
- `create_dirs` (bool): Create parent directories if needed

**Example:**
```json
{
  "template": "file_writer",
  "name": "Report Writer",
  "config_overrides": {
    "create_dirs": true
  }
}
```

---

## Batch Creation

Create multiple tools at once:

```python
import requests

batch_request = {
    "tools": [
        {
            "template": "duckduckgo_search",
            "name": "Quick Search",
            "config": {"max_results": 3}
        },
        {
            "template": "duckduckgo_search",
            "name": "Deep Search",
            "config": {"max_results": 15}
        },
        {
            "template": "api_rest",
            "name": "GitHub API",
            "config": {
                "url": "https://api.github.com",
                "headers": {"Accept": "application/vnd.github.v3+json"}
            }
        }
    ],
    "save_to_disk": true
}

response = requests.post(
    "http://localhost:8000/tools/dynamic/batch",
    json=batch_request
)

print(f"Created {response.json()['count']} tools")
```

---

## Tool Recipes

Predefined suites of related tools:

### Available Recipes

```bash
curl http://localhost:8000/tools/dynamic/recipes
```

### Create from Recipe

```bash
# Create web search suite (3 tools)
curl -X POST http://localhost:8000/tools/dynamic/recipes/web_search

# Create API tools suite (2 tools)
curl -X POST http://localhost:8000/tools/dynamic/recipes/api_tools

# Create file operations suite (2 tools)
curl -X POST http://localhost:8000/tools/dynamic/recipes/file_operations
```

---

## Using Dynamic Tools in Agents

### 1. Create Tool
```python
# Create a search tool
response = requests.post("http://localhost:8000/tools/dynamic/duckduckgo", json={
    "name": "AI Research Search",
    "max_results": 10
})
tool_id = response.json()["tool"]["id"]
```

### 2. Create Agent with Tool
```python
# Create agent using the tool
agent = {
    "id": "researcher_agent",
    "name": "Research Agent",
    "type": "react",
    "llm_config": {
        "provider": "groq",
        "model": "llama-3.1-70b-versatile"
    },
    "tools": [tool_id]  # Use the dynamic tool
}

requests.post("http://localhost:8000/agents/", json=agent)
```

### 3. Create Workflow
```python
# Create workflow using the agent
workflow = {
    "id": "research_workflow",
    "name": "Research Workflow",
    "type": "sequence",
    "nodes": [
        {
            "id": "search",
            "agent_ref": "researcher_agent",
            "task": "Research AI trends in 2025"
        }
    ]
}

requests.post("http://localhost:8000/workflows/", json=workflow)
```

### 4. Execute
```python
# Run the workflow
response = requests.post(
    "http://localhost:8000/workflows/research_workflow/execute",
    json={"parameters": {}}
)
```

---

## Advanced: Custom Tool Schema

For complete control, define everything:

```python
custom_tool = {
    "name": "Slack Notifier",
    "type": "api",
    "description": "Send messages to Slack",
    "config": {
        "url": "https://slack.com/api/chat.postMessage",
        "method": "POST",
        "headers": {
            "Authorization": "Bearer xoxb-your-token",
            "Content-Type": "application/json"
        },
        "timeout": 5.0
    },
    "input_schema": {
        "type": "object",
        "properties": {
            "channel": {
                "type": "string",
                "description": "Channel ID or name"
            },
            "text": {
                "type": "string",
                "description": "Message text"
            },
            "thread_ts": {
                "type": "string",
                "description": "Thread timestamp (optional)"
            }
        },
        "required": ["channel", "text"]
    },
    "output_schema": {
        "type": "object",
        "properties": {
            "ok": {"type": "boolean"},
            "channel": {"type": "string"},
            "ts": {"type": "string"},
            "message": {"type": "object"}
        }
    },
    "save_to_disk": true
}

response = requests.post(
    "http://localhost:8000/tools/dynamic/custom",
    json=custom_tool
)
```

---

## Configuration Files

Tools created dynamically are saved to `config/tools/` as YAML files:

```yaml
# config/tools/duckduckgo_search_abc123.yaml
id: duckduckgo_search_abc123
name: My Web Search
description: DuckDuckGo web search tool
type: websearch
config:
  engine: duckduckgo
  max_results: 5
  region: us-en
  safesearch: moderate
  timelimit: null
input_schema:
  type: object
  properties:
    query:
      type: string
      description: Search query
  required:
    - query
output_schema:
  type: object
  properties:
    results:
      type: array
    query:
      type: string
    count:
      type: integer
version: v1
created_at: '2025-11-07T10:30:00'
template: duckduckgo_search
```

---

## API Reference

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tools/dynamic/templates` | List all templates |
| GET | `/tools/dynamic/templates/{name}` | Get template schema |
| POST | `/tools/dynamic/from-template` | Create from template |
| POST | `/tools/dynamic/custom` | Create custom tool |
| POST | `/tools/dynamic/duckduckgo` | Quick DuckDuckGo tool |
| POST | `/tools/dynamic/batch` | Batch create tools |
| GET | `/tools/dynamic/recipes` | List recipes |
| POST | `/tools/dynamic/recipes/{name}` | Create from recipe |

---

## Testing

Run the comprehensive test suite:

```bash
# Start backend first
python run.py

# In another terminal, run tests
python test_dynamic_tools.py
```

---

## Examples

### Example 1: Multi-Regional Search

```python
regions = ["us-en", "uk-en", "de-de", "fr-fr"]
tools = []

for region in regions:
    response = requests.post("http://localhost:8000/tools/dynamic/duckduckgo", json={
        "name": f"Search {region.upper()}",
        "region": region,
        "max_results": 5
    })
    tools.append(response.json()["tool"]["id"])

# Now use tools in parallel workflow
workflow = {
    "id": "multi_region_search",
    "name": "Multi-Region Search",
    "execution_strategy": "parallel",
    "tools": tools
}
```

### Example 2: Time-Based News Search

```python
timeframes = {
    "today": "d",
    "this_week": "w",
    "this_month": "m"
}

for name, limit in timeframes.items():
    requests.post("http://localhost:8000/tools/dynamic/duckduckgo", json={
        "name": f"News - {name.title()}",
        "timelimit": limit,
        "max_results": 8
    })
```

### Example 3: API Integration Suite

```python
apis = [
    {"name": "GitHub", "url": "https://api.github.com"},
    {"name": "GitLab", "url": "https://gitlab.com/api/v4"},
    {"name": "Bitbucket", "url": "https://api.bitbucket.org/2.0"}
]

batch_request = {
    "tools": [
        {
            "template": "api_rest",
            "name": f"{api['name']} API",
            "config": {"url": api["url"]}
        }
        for api in apis
    ]
}

requests.post("http://localhost:8000/tools/dynamic/batch", json=batch_request)
```

---

## Best Practices

1. **Use Templates** - Start with templates for common tool types
2. **Name Descriptively** - Give tools clear, specific names
3. **Set Appropriate Limits** - Configure max_results, timeouts appropriately
4. **Validate Inputs** - Use input_schema to validate tool parameters
5. **Handle Errors** - Tools should fail gracefully with clear errors
6. **Document Config** - Use descriptions to explain config options
7. **Test Incrementally** - Test tools individually before using in workflows
8. **Version Tools** - Keep track of tool versions for reproducibility

---

## Troubleshooting

### Tool not executing
- Verify tool type is supported
- Check config values are valid
- Ensure required inputs are provided

### DuckDuckGo search failing
- Verify network connectivity
- Check region code is valid
- Try reducing max_results

### API tool errors
- Validate URL is accessible
- Check headers/auth tokens
- Verify timeout is sufficient

---

## Next Steps

1. ✅ Create your first dynamic tool
2. ✅ Test it individually
3. ✅ Integrate into an agent
4. ✅ Build a workflow
5. ✅ Execute and monitor

For more examples, see `DYNAMIC_TOOL_EXAMPLES.md`
