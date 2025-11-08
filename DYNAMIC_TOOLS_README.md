# Dynamic Tool Creation System

> **Create, configure, and deploy tools on-the-fly without writing YAML files**

## 🎯 What is This?

The Dynamic Tool Creation System allows you to create and configure tools programmatically using:
- **REST API endpoints** - Create tools via HTTP requests
- **Python client library** - Fluent, easy-to-use Python interface
- **Template system** - Predefined patterns for common tool types
- **Recipe collections** - Pre-configured tool suites for specific use cases

## ⚡ Quick Start

### 1. Start the Backend

```bash
python run.py
```

### 2. Create Your First Tool

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

print(f"Created tool: {tool['tool']['id']}")
```

**Using cURL:**
```bash
curl -X POST http://localhost:8000/tools/dynamic/duckduckgo \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Web Search",
    "max_results": 5
  }'
```

### 3. Use Tool in a Workflow

```python
import requests

# Create agent with the tool
agent = {
    "id": "researcher",
    "name": "Research Agent",
    "type": "react",
    "llm_config": {"provider": "groq", "model": "llama-3.1-70b-versatile"},
    "tools": [tool["tool"]["id"]]
}

requests.post("http://localhost:8000/agents/", json=agent)
```

## 📚 Features

### ✅ Template-Based Creation
- 11 pre-built templates (DuckDuckGo, API, GraphQL, Files, Python, etc.)
- Override default configurations
- Consistent schema validation

### ✅ Fully Custom Tools
- Define your own tool types
- Custom input/output schemas
- Complete control over configuration

### ✅ Batch Operations
- Create multiple tools at once
- Predefined recipe suites
- Parallel tool deployment

### ✅ Fluent Python Client
- Builder pattern for easy configuration
- Type hints and autocomplete
- Clean, readable API

### ✅ Persistent Storage
- Automatically saved as YAML files
- Version controlled
- Reusable across workflows

## 🛠️ Available Templates

| Template | Type | Use Case |
|----------|------|----------|
| `duckduckgo_search` | websearch | Web search queries |
| `api_rest` | api | REST API calls |
| `api_graphql` | graphql | GraphQL queries |
| `web_scraper` | http | Extract data from websites |
| `database_sql` | database | SQL queries |
| `file_reader` | file | Read files |
| `file_writer` | file | Write files |
| `python_executor` | python | Execute Python code |
| `shell_command` | shell | Run shell commands |
| `http_request` | http | Generic HTTP requests |
| `custom` | custom | Fully custom tools |

## 📖 Examples

### Example 1: Multi-Regional Search Tools

```python
from agentic_tool_client import AgenticToolClient, SearchToolBuilder

client = AgenticToolClient()

# Create search tools for different regions
regions = {
    "US": "us-en",
    "UK": "uk-en",
    "Germany": "de-de",
    "France": "fr-fr"
}

tools = []
for name, region in regions.items():
    tool = (
        SearchToolBuilder(client)
        .with_name(f"{name} Web Search")
        .with_region(region)
        .with_max_results(5)
        .build()
    )
    tools.append(tool["tool"]["id"])

print(f"Created {len(tools)} regional search tools")
```

### Example 2: API Integration Suite

```python
from agentic_tool_client import AgenticToolClient, APIToolBuilder

client = AgenticToolClient()

# GitHub API
github = (
    APIToolBuilder(client)
    .with_name("GitHub API")
    .with_url("https://api.github.com")
    .with_header("Accept", "application/vnd.github.v3+json")
    .build()
)

# Weather API
weather = (
    APIToolBuilder(client)
    .with_name("Weather API")
    .with_url("https://api.weather.gov")
    .with_header("User-Agent", "MyApp/1.0")
    .with_timeout(15.0)
    .build()
)
```

### Example 3: Time-Based News Search

```python
client = AgenticToolClient()

# Create tools for different time ranges
timeframes = {
    "Today's News": "d",
    "This Week": "w",
    "This Month": "m"
}

for name, limit in timeframes.items():
    client.create_duckduckgo_search(
        name=name,
        timelimit=limit,
        max_results=8
    )
```

### Example 4: Complete Research Pipeline

```python
from agentic_tool_client import AgenticToolClient, SearchToolBuilder
import requests

client = AgenticToolClient()

# Step 1: Create specialized search tool
search_tool = (
    SearchToolBuilder(client)
    .with_name("AI Research Search")
    .with_max_results(10)
    .moderate_search()
    .build()
)

# Step 2: Create agent
agent = {
    "id": "ai_researcher",
    "name": "AI Research Agent",
    "type": "react",
    "llm_config": {
        "provider": "groq",
        "model": "llama-3.1-70b-versatile"
    },
    "tools": [search_tool["tool"]["id"]]
}
requests.post("http://localhost:8000/agents/", json=agent)

# Step 3: Create workflow
workflow = {
    "id": "research_pipeline",
    "name": "Research Pipeline",
    "type": "sequence",
    "nodes": [
        {
            "id": "search",
            "agent_ref": "ai_researcher",
            "task": "Research transformer neural networks"
        }
    ]
}
requests.post("http://localhost:8000/workflows/", json=workflow)

# Step 4: Execute
result = requests.post(
    "http://localhost:8000/workflows/research_pipeline/execute",
    json={"parameters": {}}
)
print(result.json())
```

## 🔌 API Reference

### REST Endpoints

#### List Templates
```http
GET /tools/dynamic/templates
```

#### Get Template Schema
```http
GET /tools/dynamic/templates/{template_name}
```

#### Create from Template
```http
POST /tools/dynamic/from-template
Content-Type: application/json

{
  "template": "duckduckgo_search",
  "name": "My Tool",
  "config_overrides": {"max_results": 10}
}
```

#### Quick DuckDuckGo Tool
```http
POST /tools/dynamic/duckduckgo
Content-Type: application/json

{
  "name": "Search Tool",
  "max_results": 5,
  "region": "wt-wt"
}
```

#### Custom Tool
```http
POST /tools/dynamic/custom
Content-Type: application/json

{
  "name": "My Custom Tool",
  "type": "api",
  "config": {...},
  "input_schema": {...}
}
```

#### Batch Create
```http
POST /tools/dynamic/batch
Content-Type: application/json

{
  "tools": [...],
  "save_to_disk": true
}
```

#### List Recipes
```http
GET /tools/dynamic/recipes
```

#### Create from Recipe
```http
POST /tools/dynamic/recipes/{recipe_name}
```

### Python Client Methods

```python
client = AgenticToolClient("http://localhost:8000")

# Templates
client.list_templates()
client.get_template_schema("duckduckgo_search")

# Creation
client.create_from_template(template, name, config_overrides)
client.create_duckduckgo_search(name, max_results, region)
client.create_api_tool(name, url, method, headers)
client.create_custom_tool(name, type, config, schemas)

# Batch
client.batch_create(tool_specs)

# Recipes
client.list_recipes()
client.create_from_recipe(recipe_name)

# Management
client.get_tool(tool_id)
client.list_tools()
client.delete_tool(tool_id)
```

## 🧪 Testing

### Run All Tests
```bash
python test_dynamic_tools.py
```

### Run Complete Example
```bash
python example_complete_workflow.py
```

## 📁 File Structure

```
agentic_app/
├── app/
│   ├── routers/
│   │   └── tools.py              # Enhanced with dynamic endpoints
│   └── services/
│       └── dynamic_tool_generator.py  # Core generator logic
├── config/
│   └── tools/                    # Auto-generated YAML files
│       ├── duckduckgo_search_abc123.yaml
│       └── api_rest_def456.yaml
├── agentic_tool_client.py        # Python client library
├── test_dynamic_tools.py         # Comprehensive tests
├── example_complete_workflow.py  # Full example
├── DYNAMIC_TOOL_CREATION_GUIDE.md
└── DYNAMIC_TOOL_EXAMPLES.md
```

## 🎨 Builder Pattern Examples

### Search Tool Builder

```python
tool = (
    SearchToolBuilder(client)
    .with_name("Advanced Search")
    .with_max_results(15)
    .with_region("us-en")
    .strict_search()
    .recent_week()
    .with_description("Strict search for recent content")
    .build()
)
```

### API Tool Builder

```python
tool = (
    APIToolBuilder(client)
    .with_name("Slack Bot")
    .with_url("https://slack.com/api/chat.postMessage")
    .post()
    .with_auth_token("xoxb-your-token")
    .with_timeout(10.0)
    .build()
)
```

## 🔄 Integration with Existing System

Dynamic tools integrate seamlessly with:
- ✅ Agents (via `tools` array)
- ✅ Workflows (tool execution nodes)
- ✅ Chat Mode (tool calling)
- ✅ Tool Orchestrator (all execution strategies)

## 🌟 Best Practices

1. **Use Templates First** - Start with templates before going custom
2. **Name Descriptively** - Clear names make tools easier to find
3. **Set Appropriate Limits** - Configure timeouts, max_results appropriately
4. **Validate Schemas** - Use input_schema to validate parameters
5. **Test Individually** - Test tools before integrating into workflows
6. **Version Control** - Track tool YAML files in git
7. **Document Config** - Add descriptions for complex tools

## 🚀 Advanced Usage

### Conditional Tool Creation

```python
def create_search_tools(topic):
    """Create topic-specific search tools"""
    client = AgenticToolClient()
    
    tools = []
    
    # General search
    general = client.create_duckduckgo_search(
        name=f"{topic} Search",
        max_results=10
    )
    tools.append(general)
    
    # News search
    news = client.create_duckduckgo_search(
        name=f"{topic} News",
        max_results=5,
        timelimit="w"
    )
    tools.append(news)
    
    return [t["tool"]["id"] for t in tools]

# Usage
ai_tools = create_search_tools("AI Research")
bio_tools = create_search_tools("Biotechnology")
```

### Dynamic Workflow Generation

```python
def create_research_workflow(topic, tool_ids):
    """Generate workflow for a research topic"""
    
    workflow = {
        "id": f"research_{topic.lower().replace(' ', '_')}",
        "name": f"{topic} Research Workflow",
        "type": "parallel",
        "nodes": [
            {
                "id": f"search_{i}",
                "tool_ref": tool_id,
                "task": f"Search for {topic}"
            }
            for i, tool_id in enumerate(tool_ids)
        ]
    }
    
    return requests.post(
        "http://localhost:8000/workflows/",
        json=workflow
    )
```

## 📝 License

Part of the AgenticApp project.

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional tool templates
- More recipe collections
- Enhanced validation
- Tool versioning system
- Tool marketplace/sharing

## 📞 Support

- **Documentation**: See `DYNAMIC_TOOL_CREATION_GUIDE.md`
- **Examples**: See `DYNAMIC_TOOL_EXAMPLES.md`
- **Issues**: Report bugs or request features

---

**Happy Tool Creating! 🛠️✨**
