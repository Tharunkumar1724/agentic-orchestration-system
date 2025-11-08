# API Usage Examples

## Starting the Server

```powershell
cd c:\Sorry\agentic_app
C:/Users/HAI/AppData/Local/Programs/Python/Python313/python.exe -m uvicorn app.main:app --reload --port 8000
```

Visit http://localhost:8000/docs for the interactive API documentation.

## Example 1: Create a WebSearch Tool

```bash
curl -X POST http://localhost:8000/v1/tools/ \
  -H "Content-Type: application/json" \
  -d '{
    "id": "websearch_1",
    "name": "DuckDuckGo Search",
    "type": "websearch",
    "config": {},
    "version": "v1"
  }'
```

## Example 2: Create a Code Execution Tool

```bash
curl -X POST http://localhost:8000/v1/tools/ \
  -H "Content-Type: application/json" \
  -d '{
    "id": "code_1",
    "name": "Python Executor",
    "type": "code",
    "config": {"snippet": "print(\"Hello from code tool\")"},
    "version": "v1"
  }'
```

## Example 3: Create an API Call Tool

```bash
curl -X POST http://localhost:8000/v1/tools/ \
  -H "Content-Type: application/json" \
  -d '{
    "id": "api_1",
    "name": "Weather API",
    "type": "api",
    "config": {"url": "https://api.weather.com/data"},
    "version": "v1"
  }'
```

## Example 4: Create a React Agent with Tools and KAG

```bash
curl -X POST http://localhost:8000/v1/agents/ \
  -H "Content-Type: application/json" \
  -d '{
    "id": "agent_1",
    "name": "Research Agent",
    "type": "react",
    "llm_config": {"temperature": 0.7},
    "tools": ["websearch_1", "code_1"],
    "use_kag": true,
    "version": "v1"
  }'
```

## Example 5: Create a Zero-Shot Agent

```bash
curl -X POST http://localhost:8000/v1/agents/ \
  -H "Content-Type: application/json" \
  -d '{
    "id": "agent_2",
    "name": "Summary Agent",
    "type": "zero_shot",
    "llm_config": {},
    "tools": [],
    "use_kag": false,
    "version": "v1"
  }'
```

## Example 6: Create a Sequential Workflow

```bash
curl -X POST http://localhost:8000/v1/workflows/ \
  -H "Content-Type: application/json" \
  -d '{
    "id": "workflow_1",
    "name": "Sequential Research Flow",
    "version": "v1",
    "entrypoint": {
      "id": "root",
      "type": "sequence",
      "children": [
        {
          "id": "step1",
          "type": "agent",
          "ref": "agent_1",
          "inputs": {"prompt": "Research AI trends"}
        },
        {
          "id": "step2",
          "type": "tool",
          "ref": "websearch_1",
          "inputs": {"q": "AI research 2025"}
        }
      ]
    }
  }'
```

## Example 7: Create a Parallel Workflow

```bash
curl -X POST http://localhost:8000/v1/workflows/ \
  -H "Content-Type: application/json" \
  -d '{
    "id": "workflow_2",
    "name": "Parallel Execution",
    "version": "v1",
    "entrypoint": {
      "id": "root",
      "type": "parallel",
      "children": [
        {
          "id": "p1",
          "type": "tool",
          "ref": "websearch_1",
          "inputs": {"q": "topic A"}
        },
        {
          "id": "p2",
          "type": "tool",
          "ref": "code_1",
          "inputs": {"code": "print(\"parallel execution\")"}
        }
      ]
    }
  }'
```

## Example 8: Create a Router Workflow

```bash
curl -X POST http://localhost:8000/v1/workflows/ \
  -H "Content-Type: application/json" \
  -d '{
    "id": "workflow_3",
    "name": "Router Flow",
    "version": "v1",
    "entrypoint": {
      "id": "root",
      "type": "router",
      "inputs": {"value": "A"},
      "children": [
        {
          "id": "routeA",
          "type": "agent",
          "ref": "agent_1",
          "inputs": {"cond": "A", "prompt": "Handle case A"}
        },
        {
          "id": "routeB",
          "type": "agent",
          "ref": "agent_2",
          "inputs": {"cond": "B", "prompt": "Handle case B"}
        }
      ]
    }
  }'
```

## Example 9: Run a Workflow

```bash
curl -X POST http://localhost:8000/v1/workflows/workflow_1/run
```

The response will include:
- `workflow_id`: ID of the workflow
- `run_id`: Unique ID for this execution
- `status`: "success" or "failed"
- `result`: The execution results (JSON)

Results are automatically saved to `data/runs/{run_id}.json`

## Example 10: List All Resources

```bash
# List all tools
curl http://localhost:8000/v1/tools/

# List all agents
curl http://localhost:8000/v1/agents/

# List all workflows
curl http://localhost:8000/v1/workflows/

# List all solutions
curl http://localhost:8000/v1/solutions/
```

## Example 11: Update an Agent

```bash
curl -X PUT http://localhost:8000/v1/agents/agent_1 \
  -H "Content-Type: application/json" \
  -d '{
    "id": "agent_1",
    "name": "Updated Research Agent",
    "type": "react",
    "llm_config": {"temperature": 0.9},
    "tools": ["websearch_1", "code_1", "api_1"],
    "use_kag": true,
    "version": "v1"
  }'
```

## Example 12: Delete Resources

```bash
curl -X DELETE http://localhost:8000/v1/tools/websearch_1
curl -X DELETE http://localhost:8000/v1/agents/agent_1
curl -X DELETE http://localhost:8000/v1/workflows/workflow_1
```

## Agent Types Available
- `zero_shot`: Simple one-shot LLM call
- `react`: Reasoning + Acting pattern with tool usage
- `custom`: Custom agent logic

## Tool Types Available
- `websearch`: Web search (e.g., DuckDuckGo)
- `api`: HTTP API calls
- `code`: Execute code snippets

## Workflow Node Types
- `sequence`: Execute children in order
- `parallel`: Execute children concurrently
- `router`: Conditional branching based on input value
- `agent`: Execute an agent
- `tool`: Execute a tool

## KAG (Knowledge-Agent) Support
Set `use_kag: true` on any agent to enable knowledge retrieval augmentation. The system will prepend relevant context to prompts before LLM calls.
