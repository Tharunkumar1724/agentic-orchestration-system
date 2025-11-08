# 🚀 Dynamic Tools - Getting Started

## ⚡ Quick Start (30 seconds)

```bash
# 1. Start backend
python run.py

# 2. Create your first tool
python quickstart_dynamic_tools.py
```

---

## 📝 Create a Tool (3 Ways)

### Python (Easiest)
```python
from agentic_tool_client import AgenticToolClient

client = AgenticToolClient()
tool = client.create_duckduckgo_search("My Search", max_results=5)
print(f"Tool ID: {tool['tool']['id']}")
```

### cURL
```bash
curl -X POST http://localhost:8000/tools/dynamic/duckduckgo \
  -H "Content-Type: application/json" \
  -d '{"name": "My Search", "max_results": 5}'
```

### Interactive CLI
```bash
python interactive_tool_creator.py
```

---

## 🎯 Use in Workflow

```python
import requests

# 1. Create tool
tool = client.create_duckduckgo_search("Research Tool", max_results=10)
tool_id = tool["tool"]["id"]

# 2. Create agent with tool
agent = {
    "id": "researcher",
    "name": "Research Agent",
    "type": "react",
    "llm_config": {"provider": "groq", "model": "llama-3.1-70b-versatile"},
    "tools": [tool_id]  # ← Your dynamic tool!
}
requests.post("http://localhost:8000/agents/", json=agent)

# 3. Create workflow
workflow = {
    "id": "research_workflow",
    "name": "Research Workflow",
    "type": "sequence",
    "nodes": [{"id": "search", "agent_ref": "researcher", "task": "Research AI"}]
}
requests.post("http://localhost:8000/workflows/", json=workflow)

# 4. Execute
requests.post("http://localhost:8000/workflows/research_workflow/execute")
```

---

## 📚 Learn More

| Resource | Purpose |
|----------|---------|
| `quickstart_dynamic_tools.py` | Verify setup |
| `test_dynamic_tools.py` | See all features |
| `example_complete_workflow.py` | Full example |
| `interactive_tool_creator.py` | No-code creation |
| `DYNAMIC_TOOL_CREATION_GUIDE.md` | Complete docs |

---

## 🔍 DuckDuckGo Options

```python
client.create_duckduckgo_search(
    name="My Tool",
    max_results=5,      # 1-100
    region="us-en",     # wt-wt, us-en, uk-en, de-de, etc.
    safesearch="moderate",  # strict, moderate, off
    timelimit="d"      # d (day), w (week), m (month), None (all)
)
```

---

## 🛠️ Available Templates

- `duckduckgo_search` - Web search
- `api_rest` - REST API
- `api_graphql` - GraphQL
- `web_scraper` - Scraping
- `database_sql` - SQL queries
- `file_reader` - Read files
- `file_writer` - Write files
- `python_executor` - Python code
- `shell_command` - Shell commands
- `http_request` - HTTP requests
- `custom` - Fully custom

---

## 💡 Common Patterns

### Multi-regional search
```python
for region in ["us-en", "uk-en", "de-de"]:
    client.create_duckduckgo_search(f"{region} Search", region=region)
```

### Time-based news
```python
client.create_duckduckgo_search("Today", timelimit="d")
client.create_duckduckgo_search("This Week", timelimit="w")
```

### Batch creation
```python
client.batch_create([
    {"template": "duckduckgo_search", "name": "Quick", "config": {"max_results": 3}},
    {"template": "duckduckgo_search", "name": "Deep", "config": {"max_results": 15}}
])
```

---

## ✅ What You Get

✅ Create tools in 1 line of code  
✅ 11 different tool types  
✅ Automatic YAML generation  
✅ Works with existing agents/workflows  
✅ Python client, REST API, CLI  
✅ Comprehensive documentation  

---

**Ready? Run:** `python quickstart_dynamic_tools.py`
