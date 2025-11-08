# 🚀 PERFECT TOOL YAML ARCHITECTURE - QUICK START

## ✅ STATUS: BOTH SERVERS RUNNING

### 🌐 Access Points
- **Frontend (React)**: http://localhost:3000
- **Backend (FastAPI)**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## 📁 Files Created

### 1️⃣ **PERFECT_TOOL_ARCHITECTURE.yaml**
**Location**: `c:\Sorry\agentic_app\config\tools\PERFECT_TOOL_ARCHITECTURE.yaml`

**Complete Reference Template** with:
- ✅ All configuration options
- ✅ Input/Output schemas
- ✅ API integration (frontend & backend)
- ✅ Error handling & retry logic
- ✅ Security & authentication
- ✅ Caching & performance
- ✅ Monitoring & logging
- ✅ Complete examples

### 2️⃣ **perfect_duckduckgo_search.yaml**
**Location**: `c:\Sorry\agentic_app\config\tools\perfect_duckduckgo_search.yaml`

**Production-Ready Web Search Tool**:
- DuckDuckGo integration
- Regional search (wt-wt, us-en, uk-en, etc.)
- Time filters (day, week, month, year)
- Safe search (strict, moderate, off)
- Caching & rate limiting

### 3️⃣ **perfect_api_tool.yaml**
**Location**: `c:\Sorry\agentic_app\config\tools\perfect_api_tool.yaml`

**Generic REST API Caller**:
- All HTTP methods (GET, POST, PUT, DELETE, PATCH)
- Multiple auth types (Bearer, API Key, Basic)
- Custom headers & parameters
- Request/response handling

### 4️⃣ **perfect_github_api.yaml**
**Location**: `c:\Sorry\agentic_app\config\tools\perfect_github_api.yaml`

**GitHub API Integration**:
- Repository management
- Issue tracking
- Pull requests
- Code search

### 5️⃣ **PERFECT_TOOL_ARCHITECTURE_GUIDE.md**
**Location**: `c:\Sorry\agentic_app\PERFECT_TOOL_ARCHITECTURE_GUIDE.md`

**Complete Documentation** with:
- Architecture overview
- Backend API endpoints
- Frontend integration
- Security & authentication
- Performance optimization
- Testing examples
- Best practices

---

## 🎯 YAML Tool Architecture Structure

```yaml
# Basic Info
id: unique_tool_id
name: "Tool Display Name"
type: api|websearch|code|file|database|llm
description: "What the tool does"
version: v1

# Configuration
config:
  api:
    base_url: "https://api.example.com"
    endpoint: "/resource"
    method: GET|POST|PUT|DELETE|PATCH
    auth:
      type: bearer|api_key|basic|none
      token: "${ENV_VAR}"
    headers:
      Content-Type: "application/json"
    timeout: 30
    retry_attempts: 3

# What tool accepts
input_schema:
  type: object
  properties:
    param_name:
      type: string|integer|boolean|object|array
      description: "Parameter description"
      default: value
  required: [required_param]

# What tool returns
output_schema:
  type: object
  properties:
    success:
      type: boolean
    data:
      type: object
    metadata:
      type: object

# API Integration
api_integration:
  backend:
    base_url: "http://localhost:8000"
    endpoints:
      create: { path: "/tools", method: POST }
      get: { path: "/tools/{tool_id}", method: GET }
      list: { path: "/tools", method: GET }
      update: { path: "/tools/{tool_id}", method: PUT }
      delete: { path: "/tools/{tool_id}", method: DELETE }
  
  frontend:
    service_functions:
      - name: "getAll"
        endpoint: "/tools"
        method: "GET"

# Error Handling
error_handling:
  retry:
    enabled: true
    max_attempts: 3
    strategy: exponential_backoff
  validation:
    validate_input: true
    validate_output: true

# Execution
execution:
  async_enabled: true
  cache:
    enabled: true
    ttl_seconds: 3600
  monitoring:
    enabled: true
  logging:
    enabled: true
    log_level: INFO

# Examples
examples:
  - name: "Example Usage"
    input:
      param: "value"
    expected_output:
      success: true
```

---

## 🔌 Backend API Endpoints

### Tool Management
```
GET    /tools              - List all tools
GET    /tools/{id}         - Get specific tool
POST   /tools              - Create new tool
PUT    /tools/{id}         - Update tool
DELETE /tools/{id}         - Delete tool
```

### Dynamic Tool Creation
```
GET    /tools/dynamic/templates              - List available templates
GET    /tools/dynamic/templates/{name}       - Get template schema
POST   /tools/dynamic/from-template          - Create from template
POST   /tools/dynamic/custom                 - Create custom tool
POST   /tools/dynamic/duckduckgo             - Quick DuckDuckGo tool
POST   /tools/dynamic/batch                  - Batch create tools
GET    /tools/dynamic/recipes                - List recipes
POST   /tools/dynamic/recipes/{name}         - Create from recipe
```

---

## 💻 Frontend Integration

### API Service (JavaScript)
```javascript
import { toolsAPI } from './services/api';

// Get all tools
const tools = await toolsAPI.getAll();

// Get specific tool
const tool = await toolsAPI.getById('duckduckgo_web_search');

// Create tool
const newTool = await toolsAPI.create({
  id: 'my_tool',
  name: 'My Tool',
  type: 'api',
  config: { /* ... */ }
});

// Update tool
await toolsAPI.update('my_tool', updatedData);

// Delete tool
await toolsAPI.delete('my_tool');
```

### React Component Example
```javascript
import React, { useState, useEffect } from 'react';
import { toolsAPI } from '../services/api';

function ToolsList() {
  const [tools, setTools] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchTools() {
      try {
        const response = await toolsAPI.getAll();
        setTools(response.data);
      } finally {
        setLoading(false);
      }
    }
    fetchTools();
  }, []);

  return (
    <div>
      {tools.map(tool => (
        <div key={tool.id}>
          <h3>{tool.name}</h3>
          <p>{tool.description}</p>
          <span>Type: {tool.type}</span>
        </div>
      ))}
    </div>
  );
}
```

---

## 🔐 Authentication Types

### 1. Bearer Token
```yaml
config:
  api:
    auth:
      type: bearer
      token: "${ACCESS_TOKEN}"
      header: "Authorization"
      prefix: "Bearer"
```

### 2. API Key
```yaml
config:
  api:
    auth:
      type: api_key
      token: "${API_KEY}"
      header: "X-API-Key"
```

### 3. Basic Auth
```yaml
config:
  api:
    auth:
      type: basic
      username: "${USERNAME}"
      password: "${PASSWORD}"
```

---

## 📊 Tool Types Reference

| Type | Description | Example |
|------|-------------|---------|
| `api` | REST API calls | GitHub, Weather API |
| `websearch` | Web search engines | DuckDuckGo, Google |
| `code` | Code execution | Python, JavaScript |
| `file` | File operations | Read, Write, Delete |
| `database` | Database queries | PostgreSQL, MongoDB |
| `llm` | LLM integration | OpenAI, Groq, Anthropic |

---

## 🧪 Testing Your Tool

### 1. Test via API Docs
1. Open http://localhost:8000/docs
2. Find `/tools` POST endpoint
3. Click "Try it out"
4. Paste your tool YAML as JSON
5. Execute

### 2. Test via Frontend
1. Open http://localhost:3000
2. Navigate to "Tools" section
3. Click "Create Tool"
4. Fill in the form
5. Save and test

### 3. Test via cURL
```bash
# Create tool
curl -X POST http://localhost:8000/tools \
  -H "Content-Type: application/json" \
  -d '{
    "id": "test_tool",
    "name": "Test Tool",
    "type": "api",
    "config": {}
  }'

# Get all tools
curl http://localhost:8000/tools

# Get specific tool
curl http://localhost:8000/tools/test_tool
```

---

## 🎨 Example: Creating a Weather Tool

```yaml
id: weather_api
name: "Weather API"
type: api
description: "Get weather information for any location"
version: v1

config:
  api:
    base_url: "https://api.openweathermap.org/data/2.5"
    endpoint: "/weather"
    method: GET
    auth:
      type: api_key
      token: "${OPENWEATHER_API_KEY}"
    headers:
      Accept: "application/json"
    timeout: 30

input_schema:
  type: object
  properties:
    city:
      type: string
      description: "City name"
    country:
      type: string
      description: "Country code (optional)"
      default: "US"
  required: [city]

output_schema:
  type: object
  properties:
    success:
      type: boolean
    data:
      type: object
      properties:
        temperature:
          type: number
        description:
          type: string
        humidity:
          type: number

api_integration:
  backend:
    base_url: "http://localhost:8000"
    endpoints:
      create:
        path: "/tools"
        method: POST

execution:
  async_enabled: true
  cache:
    enabled: true
    ttl_seconds: 1800  # Cache for 30 minutes
```

---

## 📚 Next Steps

1. **Explore the Templates**
   - Open `PERFECT_TOOL_ARCHITECTURE.yaml`
   - Review all available options
   - Copy sections you need

2. **Create Your First Tool**
   - Copy `perfect_api_tool.yaml`
   - Customize for your API
   - Save to `config/tools/`

3. **Test in Frontend**
   - Open http://localhost:3000
   - Navigate to Tools
   - See your tool listed

4. **Read the Full Guide**
   - Open `PERFECT_TOOL_ARCHITECTURE_GUIDE.md`
   - Learn best practices
   - See advanced examples

---

## 🆘 Quick Troubleshooting

### Backend not starting?
```bash
cd c:\Sorry\agentic_app
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend not loading?
```bash
cd c:\Sorry\agentic_app\frontend
npm install
npm start
```

### Tool not appearing?
1. Check YAML syntax
2. Verify file location: `config/tools/`
3. Restart backend: `Ctrl+C` then restart
4. Refresh browser: `F5`

### API errors?
1. Check backend logs in terminal
2. Open http://localhost:8000/docs
3. Test endpoint directly
4. Verify CORS settings

---

## 📞 Resources

- **API Docs**: http://localhost:8000/docs
- **Frontend**: http://localhost:3000
- **Architecture Guide**: `PERFECT_TOOL_ARCHITECTURE_GUIDE.md`
- **Examples**: `config/tools/perfect_*.yaml`

---

**Status**: ✅ Production Ready
**Servers**: ✅ Backend Running | ✅ Frontend Running
**Created**: November 7, 2025

**Happy Building! 🚀**
