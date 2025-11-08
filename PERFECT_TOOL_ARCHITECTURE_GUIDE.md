# Perfect Tool YAML Architecture Guide

## 📚 Overview

This guide provides the complete YAML architecture for creating tools that work seamlessly with both frontend and backend APIs.

## 🏗️ Architecture Files Created

### 1. **PERFECT_TOOL_ARCHITECTURE.yaml**
Complete reference template with all possible configurations:
- ✅ Full input/output schemas
- ✅ API integration (backend & frontend)
- ✅ Error handling & retry logic
- ✅ Security & authentication
- ✅ Caching & performance
- ✅ Monitoring & logging
- ✅ Examples & documentation

### 2. **perfect_duckduckgo_search.yaml**
Production-ready web search tool:
- DuckDuckGo integration
- Regional & time filters
- Safe search options
- Full API endpoints

### 3. **perfect_api_tool.yaml**
Generic REST API caller:
- Support for all HTTP methods
- Authentication options
- Custom headers & params
- Request/response handling

### 4. **perfect_github_api.yaml**
GitHub API integration:
- Repository management
- Issue tracking
- Pull requests
- Code search

## 🔧 Core Architecture Components

### 1. Basic Identification
```yaml
id: tool_unique_id
name: "Tool Display Name"
type: api|websearch|code|file|database|llm
description: "Tool description"
version: v1
```

### 2. Configuration
```yaml
config:
  api:
    base_url: "https://api.example.com"
    endpoint: "/resource"
    method: GET|POST|PUT|DELETE|PATCH
    
    auth:
      type: bearer|api_key|basic|oauth2|none
      token: "${ENV_VAR}"
    
    headers:
      Content-Type: "application/json"
    
    timeout: 30
    retry_attempts: 3
```

### 3. Input Schema
```yaml
input_schema:
  type: object
  properties:
    param_name:
      type: string|integer|boolean|object|array
      description: "Parameter description"
      minimum: 1  # for integers
      maxLength: 500  # for strings
      enum: [option1, option2]  # for enums
      default: value
  
  required:
    - required_param
```

### 4. Output Schema
```yaml
output_schema:
  type: object
  properties:
    success:
      type: boolean
    
    data:
      type: object
      properties:
        results:
          type: array
          items:
            type: object
    
    metadata:
      type: object
      properties:
        execution_time_ms:
          type: integer
```

### 5. API Integration
```yaml
api_integration:
  backend:
    base_url: "http://localhost:8000"
    endpoints:
      create:
        path: "/tools"
        method: POST
      get:
        path: "/tools/{tool_id}"
        method: GET
      list:
        path: "/tools"
        method: GET
      update:
        path: "/tools/{tool_id}"
        method: PUT
      delete:
        path: "/tools/{tool_id}"
        method: DELETE
  
  frontend:
    service_functions:
      - name: "getAll"
        endpoint: "/tools"
        method: "GET"
        returns: "Array<ToolDef>"
```

## 🌐 Backend API Endpoints

### Tool Management
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/tools` | GET | List all tools |
| `/tools/{id}` | GET | Get tool by ID |
| `/tools` | POST | Create new tool |
| `/tools/{id}` | PUT | Update tool |
| `/tools/{id}` | DELETE | Delete tool |

### Dynamic Tool Creation
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/tools/dynamic/templates` | GET | List templates |
| `/tools/dynamic/from-template` | POST | Create from template |
| `/tools/dynamic/custom` | POST | Create custom tool |
| `/tools/dynamic/duckduckgo` | POST | Quick DuckDuckGo tool |
| `/tools/dynamic/batch` | POST | Batch create tools |

## 💻 Frontend Integration

### Using the API Service
```javascript
import { toolsAPI } from './services/api';

// Get all tools
const tools = await toolsAPI.getAll();

// Get specific tool
const tool = await toolsAPI.getById('duckduckgo_web_search');

// Create new tool
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
      } catch (error) {
        console.error('Error fetching tools:', error);
      } finally {
        setLoading(false);
      }
    }
    fetchTools();
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      {tools.map(tool => (
        <div key={tool.id}>
          <h3>{tool.name}</h3>
          <p>{tool.description}</p>
        </div>
      ))}
    </div>
  );
}
```

## 🔐 Security & Authentication

### API Key Authentication
```yaml
config:
  api:
    auth:
      type: api_key
      token: "${API_KEY}"
      header: "X-API-Key"
```

### Bearer Token
```yaml
config:
  api:
    auth:
      type: bearer
      token: "${ACCESS_TOKEN}"
      header: "Authorization"
      prefix: "Bearer"
```

### Basic Authentication
```yaml
config:
  api:
    auth:
      type: basic
      username: "${USERNAME}"
      password: "${PASSWORD}"
```

## ⚡ Performance & Optimization

### Caching
```yaml
execution:
  cache:
    enabled: true
    ttl_seconds: 3600
    strategy: lru
```

### Rate Limiting
```yaml
config:
  api:
    rate_limit:
      requests_per_second: 10
      requests_per_minute: 100
      requests_per_hour: 1000
```

### Retry Logic
```yaml
error_handling:
  retry:
    enabled: true
    max_attempts: 3
    strategy: exponential_backoff
    base_delay: 1.0
    max_delay: 30.0
```

## 📊 Monitoring & Logging

```yaml
execution:
  monitoring:
    enabled: true
    collect_metrics: true
    metrics:
      - execution_time
      - success_rate
      - error_rate
      - cache_hit_rate
  
  logging:
    enabled: true
    log_level: INFO
    log_format: json
```

## 🧪 Testing Examples

### Simple Tool Test
```yaml
examples:
  - name: "Basic Usage"
    input:
      query: "test query"
    expected_output:
      success: true
      data:
        results: []
```

### Error Handling Test
```yaml
examples:
  - name: "Error Handling"
    input:
      query: ""  # Invalid
    expected_output:
      success: false
      error:
        code: "4001"
        message: "Missing Required Parameter"
```

## 🚀 Quick Start

### 1. Create a Tool YAML File
```bash
# Copy the template
cp config/tools/PERFECT_TOOL_ARCHITECTURE.yaml config/tools/my_tool.yaml

# Edit with your configuration
# Set: id, name, type, config, input_schema, output_schema
```

### 2. Start Backend
```bash
# Windows PowerShell
.\start_backend.ps1

# Or manually
uvicorn app.main:app --reload --port 8000
```

### 3. Start Frontend
```bash
# Windows PowerShell
.\start_dashboard.ps1

# Or manually
cd frontend
npm install
npm start
```

### 4. Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📝 Tool Types Reference

### API Tool (`type: api`)
- External REST API calls
- OAuth/API key authentication
- Custom headers & parameters

### Web Search Tool (`type: websearch`)
- DuckDuckGo, Google, Bing
- Region & time filters
- Safe search options

### Code Tool (`type: code`)
- Execute Python/JavaScript
- Sandboxed environment
- Timeout & memory limits

### File Tool (`type: file`)
- Read/write files
- Path restrictions
- Size limits

### Database Tool (`type: database`)
- SQL/NoSQL queries
- Connection pooling
- Transaction support

### LLM Tool (`type: llm`)
- OpenAI, Anthropic, Groq
- Streaming support
- Token management

## 🎯 Best Practices

1. **Always validate input/output** - Use proper schemas
2. **Handle errors gracefully** - Implement retry logic
3. **Cache when possible** - Reduce API calls
4. **Monitor performance** - Track metrics
5. **Secure credentials** - Use environment variables
6. **Document everything** - Add examples & descriptions
7. **Test thoroughly** - Include unit & integration tests
8. **Version your tools** - Track changes in changelog

## 📖 Additional Resources

- **API Documentation**: http://localhost:8000/docs
- **Frontend Guide**: See COMPLETE_FRONTEND_GUIDE.md
- **Dynamic Tools**: See DYNAMIC_TOOLS_COMPLETE.md
- **Testing Guide**: See TESTING_GUIDE.md

## 🆘 Troubleshooting

### Tool Not Appearing in Frontend
1. Check tool YAML syntax
2. Verify tool is saved in `config/tools/`
3. Restart backend server
4. Check browser console for errors

### API Connection Issues
1. Verify backend is running on port 8000
2. Check CORS settings in `app/main.py`
3. Ensure API_BASE_URL is correct in frontend

### Authentication Errors
1. Verify environment variables are set
2. Check token format and expiration
3. Review auth configuration in YAML

---

**Created**: November 7, 2025
**Version**: 1.0.0
**Status**: Production Ready ✅
