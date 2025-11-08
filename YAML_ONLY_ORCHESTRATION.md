# YAML-Only Tool Orchestration System

## Overview
Create and orchestrate tools entirely through YAML files - no Python code required!

---

## 🎯 How It Works

1. **Define tools** in YAML files in `config/tools/`
2. **Reference tools** in agent YAML files
3. **Orchestrate in workflows** - the system handles everything
4. **Execute** - tools run automatically based on YAML config

---

## 📝 Step 1: Define Tools in YAML

### DuckDuckGo Search Tool
**File: `config/tools/web_search.yaml`**
```yaml
id: web_search
name: Web Search Tool
type: websearch
config:
  engine: duckduckgo
  max_results: 5
  region: wt-wt
  safesearch: moderate
  timelimit: null
description: "General web search using DuckDuckGo"
version: v1
```

### News Search Tool
**File: `config/tools/news_search.yaml`**
```yaml
id: news_search
name: Recent News Search
type: websearch
config:
  engine: duckduckgo
  max_results: 10
  region: wt-wt
  safesearch: moderate
  timelimit: d  # Last day only
description: "Search for recent news articles"
version: v1
```

### Academic Search Tool
**File: `config/tools/academic_search.yaml`**
```yaml
id: academic_search
name: Academic Research Search
type: websearch
config:
  engine: duckduckgo
  max_results: 15
  region: wt-wt
  safesearch: strict
  timelimit: null
description: "Search for academic and research content"
version: v1
```

### API Tool Example
**File: `config/tools/github_api.yaml`**
```yaml
id: github_api
name: GitHub API Tool
type: api
config:
  url: https://api.github.com
  method: GET
  headers:
    Accept: application/vnd.github.v3+json
    User-Agent: AgenticApp/1.0
  timeout: 10.0
description: "Access GitHub API"
version: v1
```

---

## 📝 Step 2: Define Agents in YAML

**File: `config/agents/web_researcher.yaml`**
```yaml
id: web_researcher
name: Web Research Agent
type: react
llm_config:
  provider: groq
  model: llama-3.1-70b-versatile
  temperature: 0.3
  max_tokens: 2000
tools:
  - web_search  # Reference the tool by ID
  - news_search
description: "Agent that searches the web for information"
version: v1
```

**File: `config/agents/academic_researcher.yaml`**
```yaml
id: academic_researcher
name: Academic Research Agent
type: react
llm_config:
  provider: groq
  model: llama-3.1-70b-versatile
  temperature: 0.2
  max_tokens: 2500
tools:
  - academic_search
  - web_search
description: "Agent specialized in academic research"
version: v1
```

---

## 📝 Step 3: Define Workflows in YAML

### Simple Search Workflow
**File: `config/workflows/simple_search.yaml`**
```yaml
id: simple_search
name: Simple Web Search
description: "Execute a web search task"
type: sequence
nodes:
  - id: search_step
    agent_ref: web_researcher
    task: "Search for information about ${parameters.topic}"
version: v1
```

### Multi-Agent Research Workflow
**File: `config/workflows/comprehensive_research.yaml`**
```yaml
id: comprehensive_research
name: Comprehensive Research Workflow
description: "Multi-step research using different search tools"
type: sequence
nodes:
  # Step 1: General web search
  - id: web_search
    agent_ref: web_researcher
    task: "Search for general information about ${parameters.topic}"
  
  # Step 2: News search
  - id: news_search
    agent_ref: web_researcher
    task: "Find recent news about ${parameters.topic}"
    receives_from:
      - web_search
  
  # Step 3: Academic search
  - id: academic_search
    agent_ref: academic_researcher
    task: "Find academic papers and research about ${parameters.topic}"
    receives_from:
      - web_search
      - news_search
version: v1
```

### Parallel Search Workflow
**File: `config/workflows/parallel_search.yaml`**
```yaml
id: parallel_search
name: Parallel Multi-Source Search
description: "Search multiple sources simultaneously"
type: parallel
nodes:
  # All these run at the same time
  - id: general_search
    agent_ref: web_researcher
    task: "Search web for ${parameters.topic}"
  
  - id: news_search
    agent_ref: web_researcher
    task: "Search news for ${parameters.topic}"
  
  - id: academic_search
    agent_ref: academic_researcher
    task: "Search academic sources for ${parameters.topic}"
version: v1
```

### Router Workflow (Conditional)
**File: `config/workflows/smart_search.yaml`**
```yaml
id: smart_search
name: Smart Search Router
description: "Routes to appropriate search based on query type"
type: router
routing_logic: topic_based
nodes:
  - id: news_path
    agent_ref: web_researcher
    task: "Search for news about ${parameters.topic}"
    condition: "news|current events|latest"
  
  - id: academic_path
    agent_ref: academic_researcher
    task: "Search academic sources for ${parameters.topic}"
    condition: "research|paper|study|academic"
  
  - id: general_path
    agent_ref: web_researcher
    task: "General search for ${parameters.topic}"
    condition: "default"
version: v1
```

---

## 📝 Step 4: Tool Orchestration Patterns

### Pattern 1: Sequential Tool Execution
**File: `config/workflows/sequential_tools.yaml`**
```yaml
id: sequential_tools
name: Sequential Tool Execution
type: sequence
nodes:
  - id: step1
    tool_ref: web_search  # Direct tool reference
    input:
      query: "${parameters.query}"
    output: web_results
  
  - id: step2
    tool_ref: news_search
    input:
      query: "${parameters.query}"
    output: news_results
  
  - id: step3
    tool_ref: academic_search
    input:
      query: "${parameters.query} based on ${web_results}"
    output: academic_results
```

### Pattern 2: Parallel Tool Execution
**File: `config/workflows/parallel_tools.yaml`**
```yaml
id: parallel_tools
name: Parallel Tool Execution
type: parallel
execution_strategy: parallel
nodes:
  - id: search_us
    tool_ref: web_search
    config_override:
      region: us-en
    input:
      query: "${parameters.query}"
  
  - id: search_uk
    tool_ref: web_search
    config_override:
      region: uk-en
    input:
      query: "${parameters.query}"
  
  - id: search_de
    tool_ref: web_search
    config_override:
      region: de-de
    input:
      query: "${parameters.query}"
```

### Pattern 3: Conditional Tool Execution
**File: `config/workflows/conditional_tools.yaml`**
```yaml
id: conditional_tools
name: Conditional Tool Execution
type: sequence
nodes:
  - id: primary_search
    tool_ref: web_search
    input:
      query: "${parameters.query}"
    retry_on_failure: true
    max_retries: 3
  
  - id: fallback_search
    tool_ref: news_search
    input:
      query: "${parameters.query}"
    condition: if_previous_failure
  
  - id: enhancement_search
    tool_ref: academic_search
    input:
      query: "${parameters.query}"
    condition: if_previous_success
```

### Pattern 4: Tool Chain with Transformation
**File: `config/workflows/tool_chain.yaml`**
```yaml
id: tool_chain
name: Tool Chain with Data Flow
type: sequence
nodes:
  # Search for initial data
  - id: initial_search
    tool_ref: web_search
    input:
      query: "${parameters.topic}"
    output_mapping:
      results: search_results
  
  # Process/analyze results
  - id: analyze
    agent_ref: web_researcher
    task: "Analyze these search results: ${search_results}"
    output_mapping:
      analysis: analysis_output
  
  # Deep dive based on analysis
  - id: deep_search
    tool_ref: academic_search
    input:
      query: "Deep dive into: ${analysis_output.key_topics}"
    output_mapping:
      results: final_results
```

---

## 📝 Step 5: Advanced Tool Configurations

### Multi-Regional Search Suite
**File: `config/tool_suites/global_search.yaml`**
```yaml
suite_id: global_search
name: Global Search Suite
description: "Search tools for different regions"
tools:
  - id: search_us
    name: US Search
    type: websearch
    config:
      engine: duckduckgo
      max_results: 5
      region: us-en
      safesearch: moderate
  
  - id: search_uk
    name: UK Search
    type: websearch
    config:
      engine: duckduckgo
      max_results: 5
      region: uk-en
      safesearch: moderate
  
  - id: search_germany
    name: Germany Search
    type: websearch
    config:
      engine: duckduckgo
      max_results: 5
      region: de-de
      safesearch: moderate
  
  - id: search_france
    name: France Search
    type: websearch
    config:
      engine: duckduckgo
      max_results: 5
      region: fr-fr
      safesearch: moderate
```

### Time-Based News Suite
**File: `config/tool_suites/news_suite.yaml`**
```yaml
suite_id: news_suite
name: Time-Based News Suite
description: "News search tools for different timeframes"
tools:
  - id: news_today
    name: Today's News
    type: websearch
    config:
      engine: duckduckgo
      max_results: 8
      region: wt-wt
      safesearch: moderate
      timelimit: d
  
  - id: news_week
    name: This Week's News
    type: websearch
    config:
      engine: duckduckgo
      max_results: 10
      region: wt-wt
      safesearch: moderate
      timelimit: w
  
  - id: news_month
    name: This Month's News
    type: websearch
    config:
      engine: duckduckgo
      max_results: 12
      region: wt-wt
      safesearch: moderate
      timelimit: m
```

---

## 🚀 Usage (Pure YAML)

### 1. Load and Execute via API (No Python Coding)

```bash
# Create workflow from YAML
curl -X POST http://localhost:8000/workflows/load-from-yaml \
  -H "Content-Type: application/json" \
  -d '{"yaml_file": "config/workflows/comprehensive_research.yaml"}'

# Execute workflow
curl -X POST http://localhost:8000/workflows/comprehensive_research/execute \
  -H "Content-Type: application/json" \
  -d '{"parameters": {"topic": "AI transformers"}}'
```

### 2. Via Configuration File

**File: `config/executions/my_research.yaml`**
```yaml
execution_id: my_research_001
workflow: comprehensive_research
parameters:
  topic: "Latest developments in AI"
  depth: comprehensive
options:
  save_results: true
  output_format: json
  output_path: results/my_research_001.json
```

Execute:
```bash
curl -X POST http://localhost:8000/executions/run \
  -H "Content-Type: application/json" \
  -d '{"config_file": "config/executions/my_research.yaml"}'
```

---

## 📋 Complete Example: AI Research Pipeline

### Tools (YAML Files)
**`config/tools/ai_web_search.yaml`**
```yaml
id: ai_web_search
name: AI Web Search
type: websearch
config:
  engine: duckduckgo
  max_results: 10
  region: wt-wt
  safesearch: moderate
```

**`config/tools/ai_news_search.yaml`**
```yaml
id: ai_news_search
name: AI News Search
type: websearch
config:
  engine: duckduckgo
  max_results: 8
  region: wt-wt
  safesearch: moderate
  timelimit: w
```

**`config/tools/ai_paper_search.yaml`**
```yaml
id: ai_paper_search
name: AI Paper Search
type: websearch
config:
  engine: duckduckgo
  max_results: 15
  region: wt-wt
  safesearch: strict
```

### Agent (YAML File)
**`config/agents/ai_researcher.yaml`**
```yaml
id: ai_researcher
name: AI Research Agent
type: react
llm_config:
  provider: groq
  model: llama-3.1-70b-versatile
  temperature: 0.3
tools:
  - ai_web_search
  - ai_news_search
  - ai_paper_search
```

### Workflow (YAML File)
**`config/workflows/ai_research_pipeline.yaml`**
```yaml
id: ai_research_pipeline
name: AI Research Pipeline
type: sequence
nodes:
  - id: web_research
    agent_ref: ai_researcher
    task: "Search web for ${parameters.ai_topic}"
    tools:
      - ai_web_search
  
  - id: news_research
    agent_ref: ai_researcher
    task: "Find recent news about ${parameters.ai_topic}"
    tools:
      - ai_news_search
    receives_from:
      - web_research
  
  - id: paper_research
    agent_ref: ai_researcher
    task: "Find academic papers about ${parameters.ai_topic}"
    tools:
      - ai_paper_search
    receives_from:
      - web_research
      - news_research
```

### Execution Config (YAML File)
**`config/executions/ai_research.yaml`**
```yaml
execution_id: ai_research_transformers
workflow: ai_research_pipeline
parameters:
  ai_topic: "Transformer neural networks in 2025"
options:
  save_results: true
  output_format: markdown
  output_path: results/ai_research_transformers.md
```

---

## 🎯 Key Principles (No Python Code)

✅ **Tools** → Defined in YAML files (`config/tools/`)  
✅ **Agents** → Defined in YAML files (`config/agents/`)  
✅ **Workflows** → Defined in YAML files (`config/workflows/`)  
✅ **Execution** → Configured in YAML files (`config/executions/`)  
✅ **Orchestration** → Backend handles everything automatically  

**You never write Python code - just YAML configurations!**

---

## 📁 Directory Structure

```
config/
├── tools/
│   ├── web_search.yaml
│   ├── news_search.yaml
│   ├── academic_search.yaml
│   ├── github_api.yaml
│   └── ...
├── agents/
│   ├── web_researcher.yaml
│   ├── academic_researcher.yaml
│   └── ...
├── workflows/
│   ├── simple_search.yaml
│   ├── comprehensive_research.yaml
│   ├── parallel_search.yaml
│   └── ...
├── executions/
│   ├── my_research.yaml
│   ├── ai_research.yaml
│   └── ...
└── tool_suites/
    ├── global_search.yaml
    ├── news_suite.yaml
    └── ...
```

---

## 🔄 Execution Flow (All YAML)

```
1. Define Tool (YAML)
   ↓
2. Define Agent (YAML, references tool)
   ↓
3. Define Workflow (YAML, references agent)
   ↓
4. Define Execution (YAML, references workflow)
   ↓
5. Submit to API (simple curl/HTTP request)
   ↓
6. Backend orchestrates everything
   ↓
7. Results saved automatically
```

**No Python code at any step!**
