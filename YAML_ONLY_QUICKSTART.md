# YAML-Only Tool Orchestration - Quick Start

## 🎯 No Python Code Required!

Everything is configured through YAML files. Just edit YAML and execute via simple API calls.

---

## ✅ What's Already Created For You

### Tools (6 ready-to-use search tools)
- `config/tools/web_search_general.yaml` - General web search
- `config/tools/news_search_recent.yaml` - Recent news (24h)
- `config/tools/news_weekly.yaml` - Weekly news
- `config/tools/academic_search_tool.yaml` - Academic research
- `config/tools/search_us_region.yaml` - US regional search
- `config/tools/search_uk_region.yaml` - UK regional search

### Agent (1 pre-configured agent)
- `config/agents/comprehensive_researcher.yaml` - Uses all 3 main search tools

### Workflows (3 ready-to-use workflows)
- `config/workflows/simple_web_search_workflow.yaml` - Single search
- `config/workflows/multi_source_research.yaml` - Sequential: web → news → academic
- `config/workflows/parallel_region_search.yaml` - Parallel: US + UK search

---

## 🚀 How to Use (No Python!)

### Method 1: Direct API Call (cURL)

```bash
# Execute simple search
curl -X POST http://localhost:8000/workflows/simple_web_search_workflow/execute \
  -H "Content-Type: application/json" \
  -d '{"parameters": {"topic": "artificial intelligence"}}'

# Execute multi-source research
curl -X POST http://localhost:8000/workflows/multi_source_research/execute \
  -H "Content-Type: application/json" \
  -d '{"parameters": {"topic": "climate change"}}'

# Execute parallel regional search
curl -X POST http://localhost:8000/workflows/parallel_region_search/execute \
  -H "Content-Type: application/json" \
  -d '{"parameters": {"topic": "technology trends"}}'
```

### Method 2: Using PowerShell (Windows)

```powershell
# Execute workflow
$body = @{
    parameters = @{
        topic = "artificial intelligence"
    }
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/workflows/simple_web_search_workflow/execute" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

### Method 3: Using HTTP File (VS Code REST Client)

Create a file `api_calls.http`:

```http
### Execute Simple Search
POST http://localhost:8000/workflows/simple_web_search_workflow/execute
Content-Type: application/json

{
  "parameters": {
    "topic": "artificial intelligence"
  }
}

### Execute Multi-Source Research
POST http://localhost:8000/workflows/multi_source_research/execute
Content-Type: application/json

{
  "parameters": {
    "topic": "climate change"
  }
}
```

---

## 📝 Create Your Own Tools (Pure YAML)

### Example: Create a Custom Search Tool

**File: `config/tools/my_custom_search.yaml`**
```yaml
id: my_custom_search
name: My Custom Search
type: websearch
config:
  engine: duckduckgo
  max_results: 8            # How many results (1-100)
  region: us-en             # Region: wt-wt, us-en, uk-en, de-de, fr-fr
  safesearch: moderate      # strict, moderate, or off
  timelimit: w              # d (day), w (week), m (month), null (all time)
description: "My custom search configuration"
version: v1
```

That's it! The tool is ready to use.

---

## 📝 Create Your Own Agent (Pure YAML)

**File: `config/agents/my_researcher.yaml`**
```yaml
id: my_researcher
name: My Research Agent
type: react
llm_config:
  provider: groq
  model: llama-3.1-70b-versatile
  temperature: 0.3
  max_tokens: 2000
tools:
  - my_custom_search     # Reference your tool by ID
  - web_search_general   # Or use existing tools
  - news_search_recent
description: "My custom research agent"
version: v1
```

---

## 📝 Create Your Own Workflow (Pure YAML)

**File: `config/workflows/my_research_workflow.yaml`**
```yaml
id: my_research_workflow
name: My Research Workflow
description: "My custom research workflow"
type: sequence
nodes:
  - id: step1
    agent_ref: my_researcher  # Reference your agent
    task: "Research ${parameters.topic}"
version: v1
```

---

## 🔄 Workflow Types

### Sequential (one after another)
```yaml
type: sequence
nodes:
  - id: step1
    agent_ref: agent1
    task: "First task"
  
  - id: step2
    agent_ref: agent2
    task: "Second task, using results from step1"
    receives_from:
      - step1
```

### Parallel (all at once)
```yaml
type: parallel
nodes:
  - id: task_a
    agent_ref: agent1
    task: "Task A"
  
  - id: task_b
    agent_ref: agent2
    task: "Task B (runs simultaneously with A)"
```

### Router (conditional)
```yaml
type: router
nodes:
  - id: option1
    agent_ref: agent1
    task: "If news topic"
    condition: "news"
  
  - id: option2
    agent_ref: agent2
    task: "If academic topic"
    condition: "academic"
```

---

## 🎨 DuckDuckGo Configuration Options

### Max Results
```yaml
config:
  max_results: 5    # Options: 1-100
```

### Region
```yaml
config:
  region: us-en     # Options: wt-wt (global), us-en, uk-en, de-de, fr-fr, etc.
```

### Safety Level
```yaml
config:
  safesearch: moderate    # Options: strict, moderate, off
```

### Time Range
```yaml
config:
  timelimit: d     # Options: d (day), w (week), m (month), null (all time)
```

---

## 📋 Complete Example: AI Research

### 1. Create Tool
**`config/tools/ai_search.yaml`**
```yaml
id: ai_search
name: AI Search Tool
type: websearch
config:
  engine: duckduckgo
  max_results: 10
  region: wt-wt
  safesearch: moderate
  timelimit: null
```

### 2. Create Agent
**`config/agents/ai_researcher.yaml`**
```yaml
id: ai_researcher
name: AI Research Agent
type: react
llm_config:
  provider: groq
  model: llama-3.1-70b-versatile
tools:
  - ai_search
```

### 3. Create Workflow
**`config/workflows/ai_research.yaml`**
```yaml
id: ai_research
name: AI Research Workflow
type: sequence
nodes:
  - id: research
    agent_ref: ai_researcher
    task: "Research ${parameters.topic}"
```

### 4. Execute (No Python!)
```bash
curl -X POST http://localhost:8000/workflows/ai_research/execute \
  -H "Content-Type: application/json" \
  -d '{"parameters": {"topic": "transformer neural networks"}}'
```

---

## 🎯 Ready-Made Examples You Can Use Now

### Example 1: Simple Search
```bash
curl -X POST http://localhost:8000/workflows/simple_web_search_workflow/execute \
  -H "Content-Type: application/json" \
  -d '{"parameters": {"topic": "python programming"}}'
```

### Example 2: Comprehensive Research
```bash
curl -X POST http://localhost:8000/workflows/multi_source_research/execute \
  -H "Content-Type: application/json" \
  -d '{"parameters": {"topic": "renewable energy"}}'
```

### Example 3: Multi-Region Search
```bash
curl -X POST http://localhost:8000/workflows/parallel_region_search/execute \
  -H "Content-Type: application/json" \
  -d '{"parameters": {"topic": "electric vehicles"}}'
```

---

## 📁 File Organization

```
config/
├── tools/              ← Define your search tools here
│   ├── web_search_general.yaml
│   ├── news_search_recent.yaml
│   └── YOUR_TOOL.yaml
│
├── agents/             ← Define your agents here
│   ├── comprehensive_researcher.yaml
│   └── YOUR_AGENT.yaml
│
└── workflows/          ← Define your workflows here
    ├── simple_web_search_workflow.yaml
    ├── multi_source_research.yaml
    └── YOUR_WORKFLOW.yaml
```

---

## ✅ Workflow: Edit YAML → Execute → Done

```
1. Edit/Create YAML file
   ↓
2. Save file
   ↓
3. Execute via API call (curl/PowerShell/HTTP)
   ↓
4. Get results
```

**No Python code at any step!**

---

## 🎓 Tool Template (Copy & Modify)

```yaml
id: YOUR_TOOL_ID          # Unique ID (no spaces)
name: Your Tool Name      # Human-readable name
type: websearch           # Type: websearch, api, code, etc.
config:
  engine: duckduckgo      # Always duckduckgo for search
  max_results: 5          # 1-100
  region: wt-wt           # wt-wt, us-en, uk-en, de-de, fr-fr
  safesearch: moderate    # strict, moderate, off
  timelimit: null         # d, w, m, or null
description: "What this tool does"
version: v1
```

---

## 🎓 Agent Template (Copy & Modify)

```yaml
id: YOUR_AGENT_ID
name: Your Agent Name
type: react
llm_config:
  provider: groq
  model: llama-3.1-70b-versatile
  temperature: 0.3
  max_tokens: 2000
tools:
  - tool_id_1
  - tool_id_2
description: "What this agent does"
version: v1
```

---

## 🎓 Workflow Template (Copy & Modify)

```yaml
id: YOUR_WORKFLOW_ID
name: Your Workflow Name
description: "What this workflow does"
type: sequence  # or: parallel, router
nodes:
  - id: step1
    agent_ref: YOUR_AGENT_ID
    task: "Task description with ${parameters.topic}"
version: v1
```

---

## 🚀 Start Using Now

1. **Start backend**: `python run.py`
2. **Choose a workflow** from `config/workflows/`
3. **Execute via API** (see examples above)
4. **Get results**!

**No Python coding required - just YAML configuration!**
