# Agentic AI System - Quick Start Guide

## What's Been Implemented

### Core Features
1. **FastAPI Backend** (versioned v1 APIs)
   - CRUD operations for Tools, Agents, Workflows, Solutions
   - Workflow execution endpoint with JSON output
   - Health check endpoint

2. **Dynamic Tool Creation** (3 types)
   - `api`: HTTP API calls
   - `code`: Code snippet execution
   - `websearch`: Web search (DuckDuckGo-like simulation)

3. **Dynamic Agent Creation**
   - Agent types: `zero_shot`, `react`, `custom`
   - Each agent can have multiple tools
   - Per-agent LLM context window management
   - Agent-to-agent communication via shared context

4. **Workflow Orchestration**
   - Sequential execution
   - Parallel execution
   - Router-based conditional execution
   - YAML configuration support
   - Full communication logging

5. **LLM Integration**
   - Groq API (llama-3.1-8b-instant) with your API key pre-configured
   - Anthropic Claude Sonnet 4.5 support (configurable)
   - Context window preservation across multi-turn conversations
   - Automatic message history management (last 20 messages)

6. **Agent-to-Agent Communication**
   - Workflow context shared across all agents
   - Message passing between agents and tools
   - Communication log saved in workflow run results
   - Shared state for data exchange

## Quick Start

### 1. Start the Server

```powershell
cd c:\Sorry\agentic_app
uvicorn app.main:app --reload --port 8000
```

### 2. Open API Documentation
Visit: http://localhost:8000/docs

### 3. Create a Tool (Example: Web Search)

**POST** `/v1/tools/`
```json
{
  "id": "search_tool",
  "name": "Web Search",
  "type": "websearch",
  "config": {},
  "version": "v1"
}
```

### 4. Create an Agent

**POST** `/v1/agents/`
```json
{
  "id": "researcher",
  "name": "Research Agent",
  "type": "zero_shot",
  "llm_config": {},
  "tools": ["search_tool"],
  "use_kag": false,
  "version": "v1"
}
```

### 5. Create a Workflow

**POST** `/v1/workflows/`
```json
{
  "id": "research_workflow",
  "name": "Research Workflow",
  "entrypoint": {
    "id": "root",
    "type": "sequence",
    "children": [
      {
        "id": "step1",
        "type": "agent",
        "ref": "researcher",
        "inputs": {
          "prompt": "Research AI agent frameworks"
        }
      }
    ]
  },
  "version": "v1"
}
```

### 6. Run the Workflow

**POST** `/v1/workflows/research_workflow/run`

Response includes:
```json
{
  "workflow_id": "research_workflow",
  "run_id": "...",
  "status": "success",
  "result": { ... },
  "meta": {
    "communication_log": [ ... ],
    "shared_state": { ... },
    "agents_used": ["researcher"],
    "total_messages": 8
  }
}
```

## Advanced Examples

### Multi-Agent Workflow with Communication

```json
{
  "id": "multi_agent",
  "name": "Multi-Agent Collaboration",
  "entrypoint": {
    "id": "root",
    "type": "sequence",
    "children": [
      {
        "id": "research",
        "type": "agent",
        "ref": "researcher",
        "inputs": {"prompt": "Find info about LangGraph"}
      },
      {
        "id": "write",
        "type": "agent",
        "ref": "writer",
        "inputs": {"prompt": "Summarize the research findings"}
      }
    ]
  }
}
```

The `writer` agent automatically receives context from the `researcher` agent's output!

### Parallel Execution

```json
{
  "id": "parallel_research",
  "name": "Parallel Research",
  "entrypoint": {
    "id": "root",
    "type": "parallel",
    "children": [
      {
        "id": "search1",
        "type": "tool",
        "ref": "search_tool",
        "inputs": {"q": "AI agents"}
      },
      {
        "id": "search2",
        "type": "tool",
        "ref": "search_tool",
        "inputs": {"q": "LangChain"}
      }
    ]
  }
}
```

### Router-Based Conditional Flow

```json
{
  "id": "router_example",
  "name": "Conditional Router",
  "entrypoint": {
    "id": "root",
    "type": "router",
    "inputs": {"value": "route-A"},
    "children": [
      {
        "id": "optionA",
        "type": "agent",
        "ref": "agent_a",
        "inputs": {"cond": "route-A", "prompt": "Execute A"}
      },
      {
        "id": "optionB",
        "type": "agent",
        "ref": "agent_b",
        "inputs": {"cond": "route-B", "prompt": "Execute B"}
      }
    ]
  }
}
```

## LLM Configuration

### Using Groq (Default - Pre-configured)
Set up with your API key in `.env`:
```
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
```

### Switching to Claude Sonnet 4.5
Create `.env` file:
```
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=your-key-here
ANTHROPIC_MODEL=claude-sonnet-4.5
```

## Key Features Explained

### Context Window Management
- Each agent maintains its own conversation history
- Last 20 messages preserved automatically
- Context passed between sequential agents
- LLM sees full conversation history

### Communication Log
Every workflow run saves:
- Messages between agents
- Tool execution start/end
- Agent start/end with prompts
- Shared state updates

Access via: `workflow_result["meta"]["communication_log"]`

### Dynamic Tool Types

#### API Tool
```json
{
  "id": "api_tool",
  "type": "api",
  "config": {
    "url": "https://api.example.com/endpoint"
  }
}
```

#### Code Tool
```json
{
  "id": "code_tool",
  "type": "code",
  "config": {
    "snippet": "print('Hello from code tool')"
  }
}
```

#### WebSearch Tool
```json
{
  "id": "search",
  "type": "websearch",
  "config": {}
}
```

## Files Structure

```
c:\Sorry\agentic_app\
├── app\
│   ├── main.py              # FastAPI app entry
│   ├── models.py            # Pydantic models
│   ├── storage.py           # JSON file persistence
│   ├── routers\
│   │   ├── agents.py        # Agent CRUD
│   │   ├── tools.py         # Tool CRUD
│   │   ├── workflows.py     # Workflow CRUD & run
│   │   └── solutions.py     # Solution CRUD
│   ├── services\
│   │   ├── llm_client.py    # LLM integration (Groq/Claude)
│   │   └── orchestrator.py  # Workflow runner
│   └── utils\
│       └── yaml_utils.py    # YAML parser
├── data\                    # JSON storage
│   ├── agents\
│   ├── tools\
│   ├── workflows\
│   ├── solutions\
│   └── runs\
├── tests\
│   ├── test_workflow.py
│   └── test_agent_communication.py
├── requirements.txt
└── README.md
```

## Testing

Run the test suite:
```powershell
cd c:\Sorry\agentic_app
pytest tests/
```

Or run individual tests:
```powershell
python tests/test_workflow.py
python tests/test_agent_communication.py
```

## Next Steps / TODOs

1. **KAG Integration**: Add knowledge-augmented generation toggle for agents
2. **More Tool Types**: Add database, file system, email tools
3. **Authentication**: Add API key auth for production
4. **Workflow Monitoring**: Add real-time status updates
5. **Result Caching**: Cache workflow results for repeated runs

## Troubleshooting

### Import Errors
Make sure PYTHONPATH is set:
```powershell
$env:PYTHONPATH="c:\Sorry\agentic_app"
```

### LLM Timeout
Increase timeout in `llm_client.py`:
```python
async with httpx.AsyncClient(timeout=120.0) as client:
```

### Context Too Large
Reduce `max_context_messages` in `LLMClient`:
```python
self.max_context_messages = 10  # Reduced from 20
```

## API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/v1/agents/` | Create agent |
| GET | `/v1/agents/{id}` | Get agent |
| GET | `/v1/agents/` | List all agents |
| PUT | `/v1/agents/{id}` | Update agent |
| DELETE | `/v1/agents/{id}` | Delete agent |
| POST | `/v1/tools/` | Create tool |
| GET | `/v1/tools/{id}` | Get tool |
| GET | `/v1/tools/` | List all tools |
| PUT | `/v1/tools/{id}` | Update tool |
| DELETE | `/v1/tools/{id}` | Delete tool |
| POST | `/v1/workflows/` | Create workflow |
| GET | `/v1/workflows/{id}` | Get workflow |
| GET | `/v1/workflows/` | List all workflows |
| PUT | `/v1/workflows/{id}` | Update workflow |
| DELETE | `/v1/workflows/{id}` | Delete workflow |
| **POST** | **`/v1/workflows/{id}/run`** | **Run workflow** |
| POST | `/v1/solutions/` | Create solution |
| GET | `/v1/solutions/{id}` | Get solution |
| GET | `/v1/solutions/` | List all solutions |

## Support

For issues or questions:
1. Check the `/docs` endpoint for interactive API documentation
2. Review `communication_log` in workflow results for debugging
3. Enable verbose logging in `llm_client.py` for LLM debugging

---

**System Status**: ✅ Fully operational with Groq LLM integration, agent-to-agent communication, and complete CRUD APIs.
