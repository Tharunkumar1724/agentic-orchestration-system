Agentic AI orchestration backend

This project provides a FastAPI backend that allows dynamic creation of tools, agents, workflows, and solutions. Workflows can be defined in YAML and executed (sequential, parallel, router). The system stores definitions and run outputs as JSON.

Key points
- Versioned FastAPI API (/v1)
- CRUD for tools, agents, workflows, solutions
- **🆕 Dynamic Tool Creation System** - Create tools on-the-fly without YAML files
- Dynamic creation of agents and tools (api, code, websearch types)
- **🔍 DuckDuckGo Web Search** - Built-in web search capabilities
- Workflow runner with sequential/parallel/router patterns
- Agent-to-agent communication with context preservation
- Context window management across multi-turn conversations
- YAML orchestration support
- Save outputs as JSON
- Pluggable LLM layer: configured to use Groq LLM (llama-3.1-8b-instant). Provide the API key via environment variable `GROQ_API_KEY`.

LLM provider configuration

The project supports multiple LLM providers. By default the provider is `groq`. You can switch to Anthropic Claude (Sonnet 4.5) by setting environment variables:

```
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=<your-anthropic-key>
ANTHROPIC_MODEL=claude-sonnet-4.5
```

Agent-to-agent communication

Workflows automatically maintain context and enable agent-to-agent communication:
- Each agent has its own LLM client with persistent conversation history
- Agents can see messages from previous agents in the workflow
- Communication log is saved in workflow run results under `meta.communication_log`
- Shared state allows agents to access outputs from earlier steps

The current HTTP calls in `app/services/llm_client.py` use the real Groq API (OpenAI-compatible endpoint). For production with Anthropic, use their official SDK and adapt response parsing.

Local quickstart
1. Create a virtualenv and install dependencies:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and set `GROQ_API_KEY` if you want to use the real Groq model.

3. Start the server:

```powershell
uvicorn app.main:app --reload --port 8000
```

4. Use the OpenAPI UI at http://localhost:8000/docs to create tools/agents/workflows and run them.

## 🆕 Dynamic Tool Creation

Create tools programmatically without writing YAML files:

**Quick Start:**
```bash
python quickstart_dynamic_tools.py
```

**Using Python Client:**
```python
from agentic_tool_client import AgenticToolClient

client = AgenticToolClient()

# Create a DuckDuckGo search tool
tool = client.create_duckduckgo_search(
    name="My Web Search",
    max_results=5,
    region="us-en"
)

# Use in an agent
agent = {
    "id": "researcher",
    "name": "Research Agent",
    "type": "react",
    "llm_config": {"provider": "groq", "model": "llama-3.1-70b-versatile"},
    "tools": [tool["tool"]["id"]]
}
```

**Available Resources:**
- 📚 **Guide**: `DYNAMIC_TOOL_CREATION_GUIDE.md` - Complete documentation
- 🎯 **Examples**: `DYNAMIC_TOOL_EXAMPLES.md` - YAML configuration examples
- 🚀 **Quick Reference**: `DYNAMIC_TOOLS_README.md` - API reference
- 📝 **Implementation**: `DYNAMIC_TOOLS_IMPLEMENTATION.md` - Technical details
- 🧪 **Tests**: Run `python test_dynamic_tools.py`
- 💻 **Interactive CLI**: Run `python interactive_tool_creator.py`
- 🎬 **Full Example**: Run `python example_complete_workflow.py`

**11 Tool Templates Available:**
- DuckDuckGo Search, REST API, GraphQL, Web Scraper
- Database (SQL), File Reader, File Writer
- Python Executor, Shell Command, HTTP Request, Custom

Notes
- This is a backend-only prototype. The LLM integration will attempt to use Groq if an API key is present, otherwise a mock LLM is used for safe offline testing.
- See `tests/test_workflow.py` for an example flow test.

````
```

4. Use the OpenAPI UI at http://localhost:8000/docs to create tools/agents/workflows and run them.

Notes
- This is a backend-only prototype. The LLM integration will attempt to use Groq if an API key is present, otherwise a mock LLM is used for safe offline testing.
- See `tests/test_workflow.py` for an example flow test.
