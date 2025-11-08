# Tools Persistence Fix - Complete Documentation

## Problem Summary
Tools were not being saved/persisted in workflows on both frontend and backend. When users dragged tools onto agent nodes in the workflow canvas and saved the workflow, the tools were lost after reload.

## Root Cause Analysis

### Backend Issue
The `WorkflowNode` model in `app/models.py` was missing critical fields:
1. **Missing `tools` field** - Tools attached to agent nodes were not being stored
2. **Missing `dependencies` field** - Frontend sends `dependencies` array, but backend only had `receives_from`/`sends_to`

### Frontend Issue
The frontend correctly:
- Allowed dragging tools onto agent nodes
- Set `node.data.tools` array when tools were dropped
- Sent `dependencies` array in the save payload

But the backend silently dropped these fields because they weren't in the Pydantic model.

## Solution Implemented

### 1. Updated `WorkflowNode` Model (app/models.py)

**Before:**
```python
class WorkflowNode(BaseModel):
    id: str
    agent_ref: Optional[str] = None
    task: Optional[str] = None
    receives_from: List[str] = Field(default_factory=list)
    sends_to: List[str] = Field(default_factory=list)
```

**After:**
```python
class WorkflowNode(BaseModel):
    id: str
    agent_ref: Optional[str] = None
    task: Optional[str] = None
    tools: List[str] = Field(default_factory=list)  # ✅ NEW: Tool IDs attached to this agent node
    dependencies: List[str] = Field(default_factory=list)  # ✅ NEW: Node IDs this node depends on
    receives_from: List[str] = Field(default_factory=list)  # Legacy support
    sends_to: List[str] = Field(default_factory=list)  # Legacy support
```

### 2. Enhanced Frontend Drag & Drop (frontend/src/components/Workflows.js)

Added fallback detection for tool drops in case DOM structure changes:
- Primary method: Query DOM for `[data-id="..."]` attribute
- Fallback method: Use React Flow coordinates with position-based hit testing

Added debug logging to help diagnose issues:
- Logs all API responses (workflows, agents, tools)
- Shows tools count in console
- Clears state on error for better empty-state messages

## Verification & Testing

### Backend API Test
```powershell
# Create workflow with tools
$body = '{
  "id":"test_workflow_tools",
  "name":"Test Tools Workflow", 
  "nodes":[{
    "id":"node1",
    "agent_ref":"researcher-agent",
    "task":"Test task",
    "tools":["duckduckgo_search","rest_api_caller"],
    "dependencies":[]
  }]
}'
Invoke-RestMethod -Uri 'http://localhost:8000/workflows' -Method Post -Body $body -ContentType 'application/json'

# Retrieve and verify tools persisted
Invoke-RestMethod -Uri 'http://localhost:8000/workflows/test_workflow_tools' -Method Get
```

**Result:** ✅ Tools correctly saved and retrieved from both API and YAML file

### YAML File Verification
File: `config/workflows/test_workflow_tools.yaml`
```yaml
nodes:
- id: node1
  agent_ref: researcher-agent
  task: Test task
  tools:
  - duckduckgo_search
  - rest_api_caller
  dependencies: []
```

**Result:** ✅ Tools array persisted correctly in YAML

## How to Test in UI

1. **Open Frontend** (http://localhost:3000)
2. **Navigate to Workflows** section
3. **Create New Workflow**
4. **Drag an Agent** from sidebar to canvas (creates agent node)
5. **Drag a Tool** (e.g., DuckDuckGo Search) onto the agent node
6. **Verify Tool Badge** appears on the agent node showing tool attached
7. **Save Workflow** with a name
8. **Reload Page** (F5)
9. **Open the Workflow** for editing
10. **Verify Tools** are still attached to the agent nodes

**Expected Result:** Tools should appear as badges on agent nodes after reload.

## Browser DevTools Debugging

Open Console (F12) and look for:
```
fetchData: tools response: {...}
fetchData: set tools count -> 16
```

This confirms:
- Tools are being fetched from backend
- Number of tools available for drag & drop

## Files Changed

1. **app/models.py**
   - Added `tools: List[str]` field to `WorkflowNode`
   - Added `dependencies: List[str]` field to `WorkflowNode`

2. **frontend/src/components/Workflows.js**
   - Added debug logging to `fetchData()`
   - Enhanced `onDrop()` with fallback node detection
   - Added error handling to clear state on fetch failure

3. **run.py**
   - Changed `reload=False` to `reload=True` for development

## Backend Restart Required

After updating the model, the backend must be restarted:
```powershell
cd c:\Sorry\agentic_app
python run.py
```

## Known Issues & Future Improvements

### Current State
✅ Tools persist in backend (API + YAML)  
✅ Frontend can attach tools via drag & drop  
✅ Tools are included in save payload  
⚠️ Need to verify frontend displays tools after reload (UI test pending)

### Potential Improvements
1. **Visual Feedback**: Add animation when tool is successfully attached
2. **Tool Details**: Show tool description/config on hover
3. **Remove Tools**: Add X button to remove tools from agents
4. **Validation**: Warn if agent doesn't support certain tool types
5. **Tool Limits**: Optionally limit number of tools per agent

## Related Files to Review

- `app/services/orchestrator.py` - How tools are executed during workflow runs
- `app/routers/tools.py` - Tool CRUD operations
- `config/tools/*.yaml` - Available tool definitions
- `frontend/src/components/WorkflowBlueprint.js` - Execution visualization

## API Endpoints Reference

- `POST /workflows` - Create workflow (now accepts `tools` and `dependencies`)
- `GET /workflows/{id}` - Get workflow (now returns `tools` and `dependencies`)
- `PUT /workflows/{id}` - Update workflow (now saves `tools` and `dependencies`)
- `GET /tools` - List all available tools for drag & drop

## Troubleshooting

### Tools Not Showing in Sidebar
1. Check browser console for fetch errors
2. Verify `GET /tools` returns 200 with array
3. Check `REACT_APP_API_URL` environment variable

### Tools Not Attaching on Drop
1. Check console for drop event errors
2. Verify React Flow canvas has `onDrop` and `onDragOver` handlers
3. Try the fallback detection (should log warnings if it activates)

### Tools Lost After Save
1. Verify backend has been restarted after model update
2. Check workflow YAML file directly in `config/workflows/`
3. Test via API directly (see Backend API Test section)

## Next Steps

1. ✅ Backend model updated
2. ✅ Backend tested via API
3. ✅ YAML persistence verified
4. ⏳ Frontend UI test (manual verification needed)
5. ⏳ End-to-end integration test
6. ⏳ Update user documentation

---

**Fixed:** November 8, 2025  
**Issue:** Tools not persisting in workflows  
**Status:** Backend ✅ | Frontend UI verification pending ⏳
