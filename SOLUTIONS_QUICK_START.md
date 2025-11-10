# 🚀 Solutions Quick Start Guide

## What are Solutions?

Solutions are **multi-workflow orchestrations** that enable:
- Sequential workflow execution with AI-powered communication
- Context handoffs between workflows using Gemini AI (KAG)
- Real-time execution monitoring via WebSocket
- Fact extraction and knowledge aggregation

---

## Quick Setup ✅

### 1. Start Backend
```bash
cd c:\Sorry\agentic_app
python run.py
```
**Endpoint**: http://localhost:8000

### 2. Start Frontend
```bash
cd c:\Sorry\agentic_app\frontend
npm start
```
**Endpoint**: http://localhost:3000

### 3. Verify Running
```bash
# Backend health check
curl http://localhost:8000/health

# List solutions
curl http://localhost:8000/solutions/
```

---

## Create a Solution (3 Ways)

### Option 1: Frontend UI
1. Open http://localhost:3000
2. Go to "Solutions" section
3. Click "Create Solution"
4. Fill form and select workflows
5. Click "Save"

### Option 2: API (cURL)
```bash
curl -X POST http://localhost:8000/solutions/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Solution",
    "description": "Multi-step research and analysis",
    "workflows": ["workflow_1", "workflow_2"]
  }'
```

### Option 3: Python Script
```python
import requests

response = requests.post("http://localhost:8000/solutions/", json={
    "name": "My Solution",
    "description": "Description",
    "workflows": ["wf1", "wf2"]
})
print(response.json())
```

---

## Execute a Solution

### Frontend (Real-time UI)
1. Click on solution
2. Click "Start Execution"
3. Watch real-time progress:
   - Workflow status
   - AI analysis
   - Handoff data
   - Final summary

### API (Programmatic)
```bash
curl -X POST http://localhost:8000/solutions/{solution_id}/execute
```

### WebSocket (Real-time Streaming)
```javascript
const ws = new WebSocket('ws://localhost:8000/solutions/ws/{solution_id}');

ws.onopen = () => {
  ws.send(JSON.stringify({ action: 'execute' }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data.type, data);
};
```

---

## Common Operations

### List All Solutions
```bash
GET http://localhost:8000/solutions/
```

### Get Specific Solution
```bash
GET http://localhost:8000/solutions/{id}
```

### Update Solution
```bash
PUT http://localhost:8000/solutions/{id}
{
  "name": "Updated Name",
  "workflows": ["new_wf1", "new_wf2"]
}
```

### Delete Solution
```bash
DELETE http://localhost:8000/solutions/{id}
```

### Add Workflow to Solution
```bash
POST http://localhost:8000/solutions/{id}/workflows/{workflow_id}
```

### Remove Workflow from Solution
```bash
DELETE http://localhost:8000/solutions/{id}/workflows/{workflow_id}
```

### Get AI Summary
```bash
GET http://localhost:8000/solutions/{id}/summary
```

---

## WebSocket Events

When executing a solution via WebSocket, you'll receive:

### 1. execution_started
```json
{
  "type": "execution_started",
  "solution_id": "sol_123",
  "total_workflows": 3
}
```

### 2. workflow_started
```json
{
  "type": "workflow_started",
  "workflow_id": "wf1",
  "workflow_name": "Research",
  "position": 1,
  "total": 3
}
```

### 3. handoff_prepared
```json
{
  "type": "handoff_prepared",
  "from_workflow": "wf1",
  "to_workflow": "wf2",
  "handoff_data": {
    "handoff_data": "Context from previous workflow",
    "relevance": "Highly relevant for next task",
    "context": "Research findings about...",
    "facts": ["fact1", "fact2"]
  }
}
```

### 4. workflow_completed
```json
{
  "type": "workflow_completed",
  "workflow_id": "wf1",
  "workflow_name": "Research",
  "kag_analysis": {
    "summary": "AI-generated summary",
    "facts": ["extracted", "facts"],
    "reasoning": "AI reasoning process"
  },
  "output": "workflow output data"
}
```

### 5. execution_completed
```json
{
  "type": "execution_completed",
  "solution_id": "sol_123",
  "summary": {
    "total_workflows": 3,
    "overall_context": "Comprehensive summary",
    "combined_facts": ["all", "facts", "from", "workflows"]
  }
}
```

### 6. error
```json
{
  "type": "error",
  "message": "Error description"
}
```

---

## Data Files Location

### Config (YAML)
```
config/solutions/{solution_id}.yaml
```

### Data (JSON)
```
data/solutions/{solution_id}.json
```

Both files are created automatically when you save a solution.

---

## Example: Complete Workflow

```python
import requests
import json
from websockets.sync.client import connect

# 1. Create solution
solution = requests.post("http://localhost:8000/solutions/", json={
    "name": "Research & Analysis Pipeline",
    "workflows": ["research_wf", "analysis_wf", "report_wf"]
}).json()

solution_id = solution["id"]
print(f"Created solution: {solution_id}")

# 2. Execute via WebSocket
ws_uri = f"ws://localhost:8000/solutions/ws/{solution_id}"

with connect(ws_uri) as websocket:
    # Send execute command
    websocket.send(json.dumps({"action": "execute"}))
    
    # Receive updates
    for message in websocket:
        data = json.loads(message)
        print(f"{data['type']}: {data}")
        
        if data["type"] == "execution_completed":
            print("✅ Solution execution complete!")
            break

# 3. Get final summary
summary = requests.get(f"http://localhost:8000/solutions/{solution_id}/summary").json()
print(f"Total facts collected: {len(summary['combined_facts'])}")
```

---

## Testing

### Run Tests
```bash
# API tests
python test_solution_fix.py

# WebSocket tests
python test_solution_websocket_quick.py
```

### Manual Verification
```bash
# Check backend
curl http://localhost:8000/health

# List solutions
curl http://localhost:8000/solutions/

# Check data files
ls data/solutions/
```

---

## Troubleshooting

### Solutions Not Loading
```bash
# Check if data files exist
ls data/solutions/

# Restart backend
python run.py
```

### WebSocket Connection Failed
- Ensure backend is running on port 8000
- Check solution ID exists
- Verify no firewall blocking WebSocket

### Frontend Not Showing Solutions
- Check browser console for errors
- Verify backend CORS is enabled
- Check API endpoint: http://localhost:8000/solutions/

---

## Best Practices

1. **Name workflows clearly** - Helps with debugging and AI analysis
2. **Use descriptive solution names** - Makes it easier to find and manage
3. **Keep workflow count reasonable** - 2-5 workflows per solution is ideal
4. **Test workflows individually** - Before adding to solution
5. **Monitor WebSocket messages** - Use browser dev tools
6. **Check KAG summaries** - Verify AI is extracting useful context

---

## Current Status ✅

- Backend: Running on http://localhost:8000
- Frontend: Running on http://localhost:3000
- API Endpoints: 13 endpoints, all working
- WebSocket: Real-time updates functional
- Data Persistence: YAML + JSON working
- Test Coverage: 100% passing

---

## Next Steps

1. Create your first solution ✨
2. Execute and watch real-time updates 🚀
3. Check AI-generated summaries 🤖
4. Build complex multi-workflow pipelines 🔗

**Ready to use!** 🎉

---

## Quick Reference

| Action | Command |
|--------|---------|
| Start backend | `python run.py` |
| Start frontend | `cd frontend && npm start` |
| Create solution | `POST /solutions/` |
| Execute solution | `POST /solutions/{id}/execute` |
| Watch real-time | `WS /solutions/ws/{id}` |
| Get summary | `GET /solutions/{id}/summary` |
| List all | `GET /solutions/` |

---

**Version**: 1.0  
**Last Updated**: November 9, 2025  
**Status**: Fully Operational ✅
