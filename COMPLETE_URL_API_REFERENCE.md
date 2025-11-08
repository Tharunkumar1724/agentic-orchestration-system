# 🌐 Complete URL & API Reference

## 🚀 Application URLs

### Frontend (React)
```
Main Application:     http://localhost:3000
Dashboard:            http://localhost:3000/
Agents:               http://localhost:3000/#agents
Tools:                http://localhost:3000/#tools
Workflows:            http://localhost:3000/#workflows
Solutions:            http://localhost:3000/#solutions
Chat:                 http://localhost:3000/#chat
```

### Backend (FastAPI)
```
API Base:             http://localhost:8000
API Documentation:    http://localhost:8000/docs
Alternative Docs:     http://localhost:8000/redoc
Health Check:         http://localhost:8000/health
OpenAPI Schema:       http://localhost:8000/openapi.json
```

---

## 🔌 Complete API Endpoints

### 🏥 Health & Info
```
GET  /health                     - Health check endpoint
```

### 🛠️ Tools API

#### Basic CRUD
```
GET    /tools                    - List all tools
GET    /tools/{tool_id}          - Get specific tool by ID
POST   /tools                    - Create new tool
PUT    /tools/{tool_id}          - Update existing tool
DELETE /tools/{tool_id}          - Delete tool
```

**Request Body (POST/PUT)**:
```json
{
  "id": "tool_unique_id",
  "name": "Tool Name",
  "type": "api|websearch|code|file|database|llm",
  "config": {
    "api": {
      "base_url": "https://api.example.com",
      "endpoint": "/resource",
      "method": "GET",
      "auth": {
        "type": "bearer",
        "token": "${API_TOKEN}"
      }
    }
  },
  "version": "v1"
}
```

**Response**:
```json
{
  "id": "tool_unique_id",
  "name": "Tool Name",
  "type": "api",
  "config": { ... },
  "version": "v1"
}
```

#### Dynamic Tool Creation
```
GET    /tools/dynamic/templates
       - List all available tool templates
       Response: { "templates": ["duckduckgo_search", "api_call", ...] }

GET    /tools/dynamic/templates/{template_name}
       - Get schema for specific template
       Response: Template configuration schema

POST   /tools/dynamic/from-template
       - Create tool from template
       Body: {
         "template": "duckduckgo_search",
         "name": "My Search Tool",
         "description": "Custom search tool",
         "config_overrides": { ... },
         "save_to_disk": true
       }
       Response: {
         "success": true,
         "tool": { ... },
         "message": "Tool created successfully"
       }

POST   /tools/dynamic/custom
       - Create completely custom tool
       Body: {
         "name": "Custom Tool",
         "type": "api",
         "config": { ... },
         "input_schema": { ... },
         "output_schema": { ... },
         "save_to_disk": true
       }

POST   /tools/dynamic/duckduckgo
       - Quick create DuckDuckGo search tool
       Body: {
         "name": "Quick Search",
         "max_results": 10,
         "region": "us-en",
         "safesearch": "moderate",
         "timelimit": null
       }

POST   /tools/dynamic/batch
       - Create multiple tools at once
       Body: {
         "tools": [
           { "template": "duckduckgo_search", "name": "Tool 1" },
           { "template": "api_call", "name": "Tool 2" }
         ],
         "save_to_disk": true
       }

GET    /tools/dynamic/recipes
       - List available tool recipes
       Response: {
         "recipes": [
           {
             "name": "web_search",
             "description": "Suite of search tools",
             "tool_count": 3
           }
         ]
       }

POST   /tools/dynamic/recipes/{recipe_name}
       - Create tools from recipe
       Recipe names: web_search, api_tools, file_operations
```

### 🤖 Agents API
```
GET    /agents                   - List all agents
GET    /agents/{agent_id}        - Get specific agent
POST   /agents                   - Create new agent
PUT    /agents/{agent_id}        - Update agent
DELETE /agents/{agent_id}        - Delete agent
```

**Request Body**:
```json
{
  "id": "agent_unique_id",
  "name": "Agent Name",
  "type": "zero_shot|react|custom",
  "llm_config": {
    "model": "llama-3.1-70b-versatile",
    "temperature": 0.7
  },
  "tools": ["tool_id_1", "tool_id_2"],
  "use_kag": false,
  "version": "v1"
}
```

### 🔄 Workflows API
```
GET    /workflows                - List all workflows
GET    /workflows/{workflow_id}  - Get specific workflow
POST   /workflows                - Create new workflow
PUT    /workflows/{workflow_id}  - Update workflow
DELETE /workflows/{workflow_id}  - Delete workflow
POST   /workflows/{workflow_id}/run
       - Execute workflow
       Body: { "input": "User input text" }

GET    /workflows/runs           - List all workflow runs
GET    /workflows/runs/{run_id}  - Get specific run result
```

**Workflow Structure**:
```json
{
  "id": "workflow_unique_id",
  "name": "Workflow Name",
  "description": "What this workflow does",
  "type": "sequence|parallel|router",
  "nodes": [
    {
      "id": "node_1",
      "agent_ref": "agent_id",
      "task": "Task description",
      "receives_from": [],
      "sends_to": ["node_2"]
    }
  ],
  "version": "v1"
}
```

**Run Response**:
```json
{
  "workflow_id": "workflow_id",
  "run_id": "unique_run_id",
  "status": "completed|running|failed",
  "result": { ... },
  "meta": {
    "execution_time": 1.234,
    "timestamp": "2025-11-07T12:00:00Z"
  }
}
```

### 📦 Solutions API
```
GET    /solutions                - List all solutions (alias for runs)
GET    /solutions/{solution_id}  - Get specific solution
```

### 💬 Chat API
```
GET    /chat/sessions            - List all chat sessions
GET    /chat/sessions/{session_id}
       - Get specific chat session with full message history

POST   /chat/sessions
       - Create new chat session
       Body: {
         "workflow_id": "workflow_id",  // optional
         "name": "Session Name",         // optional
         "initial_message": "Hi there",  // optional
         "metadata": {}                  // optional
       }
       Response: {
         "session_id": "unique_id",
         "workflow_id": "workflow_id",
         "created_at": "2025-11-07T12:00:00Z",
         "messages": [],
         "state": {}
       }

POST   /chat/sessions/{session_id}/message
       - Send message to chat session
       Body: {
         "message": "Your message here",
         "stream": false
       }
       Response: {
         "role": "assistant",
         "content": "Response from workflow",
         "timestamp": "2025-11-07T12:00:00Z",
         "metadata": {}
       }

DELETE /chat/sessions/{session_id}
       - Delete chat session
```

---

## 🔗 Frontend API Integration

### Service File Location
```
File: c:\Sorry\agentic_app\frontend\src\services\api.js
```

### Available Functions

#### Tools API
```javascript
import { toolsAPI } from './services/api';

// List all tools
const response = await toolsAPI.getAll();
// Returns: { data: [ToolDef, ToolDef, ...] }

// Get specific tool
const tool = await toolsAPI.getById('tool_id');
// Returns: { data: ToolDef }

// Create tool
const newTool = await toolsAPI.create({
  id: 'my_tool',
  name: 'My Tool',
  type: 'api',
  config: {}
});
// Returns: { data: ToolDef }

// Update tool
const updated = await toolsAPI.update('tool_id', toolData);
// Returns: { data: ToolDef }

// Delete tool
await toolsAPI.delete('tool_id');
// Returns: { data: { deleted: true } }
```

#### Agents API
```javascript
import { agentsAPI } from './services/api';

const agents = await agentsAPI.getAll();
const agent = await agentsAPI.getById('agent_id');
const newAgent = await agentsAPI.create(agentData);
const updated = await agentsAPI.update('agent_id', agentData);
await agentsAPI.delete('agent_id');
```

#### Workflows API
```javascript
import { workflowsAPI } from './services/api';

const workflows = await workflowsAPI.getAll();
const workflow = await workflowsAPI.getById('workflow_id');
const newWorkflow = await workflowsAPI.create(workflowData);
const updated = await workflowsAPI.update('workflow_id', workflowData);
await workflowsAPI.delete('workflow_id');

// Execute workflow
const result = await workflowsAPI.run('workflow_id', {
  input: "Execute this task"
});
// Returns: { 
//   data: {
//     workflow_id: "...",
//     run_id: "...",
//     status: "completed",
//     result: { ... }
//   }
// }
```

#### Chat API
```javascript
import { chatAPI } from './services/api';

// Get all sessions
const sessions = await chatAPI.getSessions();

// Get specific session
const session = await chatAPI.getSession('session_id');

// Create new session
const newSession = await chatAPI.createSession({
  workflow_id: 'workflow_id',
  name: 'My Chat',
  initial_message: 'Hello'
});

// Send message
const response = await chatAPI.sendMessage('session_id', 'Your message');

// Delete session
await chatAPI.deleteSession('session_id');
```

---

## 🧪 Testing Examples

### Using cURL

#### Create a Tool
```bash
curl -X POST http://localhost:8000/tools \
  -H "Content-Type: application/json" \
  -d '{
    "id": "test_search",
    "name": "Test Search",
    "type": "websearch",
    "config": {
      "search": {
        "engine": "duckduckgo",
        "max_results": 10
      }
    }
  }'
```

#### Create Tool from Template
```bash
curl -X POST http://localhost:8000/tools/dynamic/from-template \
  -H "Content-Type: application/json" \
  -d '{
    "template": "duckduckgo_search",
    "name": "My Search Tool",
    "save_to_disk": true
  }'
```

#### Run a Workflow
```bash
curl -X POST http://localhost:8000/workflows/my_workflow/run \
  -H "Content-Type: application/json" \
  -d '{
    "input": "Search for artificial intelligence"
  }'
```

#### Create Chat Session
```bash
curl -X POST http://localhost:8000/chat/sessions \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_id": "my_workflow",
    "name": "Test Chat"
  }'
```

#### Send Chat Message
```bash
curl -X POST http://localhost:8000/chat/sessions/SESSION_ID/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, how are you?"
  }'
```

### Using JavaScript (Fetch)

```javascript
// Create tool
const createTool = async () => {
  const response = await fetch('http://localhost:8000/tools', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      id: 'test_tool',
      name: 'Test Tool',
      type: 'api',
      config: {}
    })
  });
  return await response.json();
};

// Get all tools
const getAllTools = async () => {
  const response = await fetch('http://localhost:8000/tools');
  return await response.json();
};

// Run workflow
const runWorkflow = async (workflowId, input) => {
  const response = await fetch(
    `http://localhost:8000/workflows/${workflowId}/run`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ input })
    }
  );
  return await response.json();
};
```

### Using Python (requests)

```python
import requests

# Create tool
response = requests.post(
    'http://localhost:8000/tools',
    json={
        'id': 'test_tool',
        'name': 'Test Tool',
        'type': 'api',
        'config': {}
    }
)
print(response.json())

# Get all tools
response = requests.get('http://localhost:8000/tools')
tools = response.json()

# Run workflow
response = requests.post(
    'http://localhost:8000/workflows/my_workflow/run',
    json={'input': 'Process this'}
)
result = response.json()
```

---

## 📊 Response Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Invalid request data |
| 404 | Not Found | Resource not found |
| 422 | Validation Error | Request validation failed |
| 500 | Server Error | Internal server error |

---

## 🔒 CORS Configuration

Current CORS settings (in `app/main.py`):
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # Allow all origins
    allow_credentials=True,        # Allow credentials
    allow_methods=["*"],           # Allow all methods
    allow_headers=["*"],           # Allow all headers
)
```

**Production**: Change `allow_origins=["*"]` to specific domains:
```python
allow_origins=[
    "http://localhost:3000",
    "https://yourdomain.com"
]
```

---

## 🎯 Environment Variables

Create a `.env` file for sensitive data:

```env
# API Keys
GITHUB_TOKEN=your_github_token_here
OPENWEATHER_API_KEY=your_weather_key_here
GROQ_API_KEY=your_groq_key_here

# Database
DATABASE_URL=postgresql://user:pass@localhost/db

# Application
API_BASE_URL=http://localhost:8000
REACT_APP_API_URL=http://localhost:8000
```

Access in YAML tools:
```yaml
config:
  api:
    auth:
      token: "${GITHUB_TOKEN}"
```

---

## 📱 WebSocket Support (Future)

For streaming responses and real-time updates:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};

ws.send(JSON.stringify({
  type: 'chat',
  message: 'Hello'
}));
```

---

## 🚀 Deployment URLs

When deploying to production:

```yaml
# Frontend
Production URL:       https://app.yourdomain.com
Staging URL:          https://staging.yourdomain.com

# Backend
Production API:       https://api.yourdomain.com
Staging API:          https://api-staging.yourdomain.com

# Update in frontend .env
REACT_APP_API_URL=https://api.yourdomain.com
```

---

**Last Updated**: November 7, 2025
**Backend**: http://localhost:8000 ✅
**Frontend**: http://localhost:3000 ✅
