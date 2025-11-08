# Dynamic Tool Configuration Examples

## 1. DuckDuckGo Web Search Tools

### Basic Search
```yaml
id: duckduckgo_basic
name: Basic Web Search
type: websearch
config:
  engine: duckduckgo
  max_results: 5
  region: wt-wt
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
      items:
        type: object
        properties:
          title: { type: string }
          url: { type: string }
          snippet: { type: string }
    query: { type: string }
    count: { type: integer }
```

### News Search (Last 24 Hours)
```yaml
id: duckduckgo_news
name: Recent News Search
type: websearch
config:
  engine: duckduckgo
  max_results: 10
  region: wt-wt
  safesearch: moderate
  timelimit: d  # d=day, w=week, m=month
```

### Academic Search
```yaml
id: duckduckgo_academic
name: Academic Research Search
type: websearch
config:
  engine: duckduckgo
  max_results: 15
  region: wt-wt
  safesearch: strict
  timelimit: null
description: "Search for academic papers and research"
```

## 2. API Tools

### REST API Tool
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
input_schema:
  type: object
  properties:
    endpoint:
      type: string
      description: API endpoint (e.g., /users/username)
    params:
      type: object
```

### GraphQL API Tool
```yaml
id: graphql_api
name: GraphQL Query Tool
type: graphql
config:
  url: https://api.example.com/graphql
  timeout: 15.0
  headers:
    Content-Type: application/json
input_schema:
  type: object
  properties:
    query:
      type: string
      description: GraphQL query
    variables:
      type: object
  required:
    - query
```

## 3. File Operations

### File Reader
```yaml
id: file_reader
name: Text File Reader
type: file
config:
  operation: read
  encoding: utf-8
  safe_path_check: true
input_schema:
  type: object
  properties:
    path:
      type: string
    encoding:
      type: string
      default: utf-8
  required:
    - path
```

### File Writer
```yaml
id: file_writer
name: Text File Writer
type: file
config:
  operation: write
  encoding: utf-8
  create_dirs: true
input_schema:
  type: object
  properties:
    path: { type: string }
    content: { type: string }
    mode:
      type: string
      enum: [write, append]
      default: write
  required:
    - path
    - content
```

## 4. Python Execution

```yaml
id: python_executor
name: Python Code Runner
type: python
config:
  sandbox: true
  timeout: 30
  allowed_imports:
    - math
    - json
    - datetime
    - requests
input_schema:
  type: object
  properties:
    code:
      type: string
      description: Python code to execute
    timeout:
      type: number
      default: 30
  required:
    - code
```

## 5. Database Tools

### SQL Query Tool
```yaml
id: postgres_query
name: PostgreSQL Query Tool
type: database
config:
  db_type: postgresql
  connection_string: postgresql://user:pass@localhost/dbname
  safe_mode: true
  read_only: true
input_schema:
  type: object
  properties:
    query:
      type: string
    params:
      type: array
  required:
    - query
```

## 6. Agent Configuration Using Dynamic Tools

```yaml
# agents/researcher_with_tools.yaml
id: researcher_v2
name: Advanced Research Agent
type: react
llm_config:
  provider: groq
  model: llama-3.1-70b-versatile
  temperature: 0.3
  max_tokens: 2000
tools:
  - duckduckgo_basic      # Basic search
  - duckduckgo_news       # News search
  - duckduckgo_academic   # Academic search
  - github_api            # For code research
  - file_writer           # To save findings
workflow:
  - step: search_web
    tool: duckduckgo_basic
    input_mapping:
      query: "${task}"
  - step: search_news
    tool: duckduckgo_news
    input_mapping:
      query: "${task}"
    condition: if_previous_success
  - step: save_results
    tool: file_writer
    input_mapping:
      path: results/${run_id}.md
      content: "${results}"
```

## 7. Pipeline with Dynamic Tools

```yaml
# workflows/research_pipeline.yaml
id: ai_research_pipeline
name: AI Research Pipeline
type: sequence
nodes:
  - id: broad_search
    agent_ref: researcher_v2
    task: "Search for ${topic}"
    
  - id: deep_dive
    agent_ref: researcher_v2
    task: "Analyze findings from broad_search"
    receives_from: [broad_search]
    
  - id: code_search
    agent_ref: researcher_v2
    task: "Find code examples for ${topic}"
    tools:
      - github_api
    
  - id: compile_report
    agent_ref: writer_agent
    task: "Write comprehensive report"
    receives_from: [broad_search, deep_dive, code_search]
```

## 8. Conditional Tool Execution

```yaml
# Workflow with fallback tools
id: resilient_search
name: Resilient Search Workflow
type: sequence
nodes:
  - id: primary_search
    tool: duckduckgo_basic
    input:
      query: "${query}"
    fallback:
      tool: duckduckgo_news
      condition: if_previous_failure
  
  - id: verify_results
    tool: custom_validator
    input:
      data: "${primary_search.results}"
    retry:
      max_attempts: 3
      backoff: exponential
```

## 9. Parallel Tool Execution

```yaml
# Execute multiple searches in parallel
id: parallel_research
name: Multi-Source Research
execution_strategy: parallel
nodes:
  - id: web_search
    tool: duckduckgo_basic
    input:
      query: "${query}"
  
  - id: news_search
    tool: duckduckgo_news
    input:
      query: "${query}"
  
  - id: academic_search
    tool: duckduckgo_academic
    input:
      query: "${query}"
  
  - id: merge_results
    tool: custom_merger
    input:
      sources:
        - "${web_search.results}"
        - "${news_search.results}"
        - "${academic_search.results}"
    depends_on: [web_search, news_search, academic_search]
```

## 10. Tool Orchestration Example

```yaml
# Complete orchestration with multiple tool types
id: comprehensive_pipeline
name: Comprehensive Analysis Pipeline
description: "Full research, analysis, and reporting pipeline"

tools:
  - duckduckgo_basic
  - github_api
  - python_executor
  - file_writer

execution_strategy: sequential

steps:
  - name: research
    tool: duckduckgo_basic
    config:
      max_results: 10
    input:
      query: "${parameters.topic}"
    output: research_data
  
  - name: fetch_code
    tool: github_api
    config:
      endpoint: /search/repositories
    input:
      params:
        q: "${parameters.topic}"
        sort: stars
    output: code_repos
  
  - name: analyze
    tool: python_executor
    input:
      code: |
        import json
        data = ${research_data}
        repos = ${code_repos}
        # Analysis logic
        result = {"summary": "...", "insights": [...]}
        print(json.dumps(result))
    output: analysis
  
  - name: save_report
    tool: file_writer
    input:
      path: reports/${run_id}_report.md
      content: |
        # Research Report: ${parameters.topic}
        
        ## Web Research
        ${research_data}
        
        ## Code Examples
        ${code_repos}
        
        ## Analysis
        ${analysis}
```
