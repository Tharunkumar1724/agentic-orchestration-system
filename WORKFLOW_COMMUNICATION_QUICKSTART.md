# Quick Start: Workflow Communication in Solutions

## What's New?
✅ AI-powered workflow-to-workflow communication using Gemini 1.5 Pro  
✅ Live visualization of workflow execution  
✅ Automatic fact extraction and context transfer  
✅ Conversation memory across workflow chains  
✅ Dark-themed beautiful UI with animations  

## Prerequisites
- Backend running on `http://localhost:8000`
- Frontend running on `http://localhost:3000`
- Gemini API key configured (add to .env file)

## 5-Minute Demo

### Step 1: Access Solutions
1. Open frontend: `http://localhost:3000`
2. Click **Solutions** in the sidebar

### Step 2: Create a Solution
1. Click **Create Solution**
2. Fill in:
   - **Name**: "Market Analysis"
   - **Description**: "Analyze stock market with AI"
   - **Workflows**: Select existing workflows (e.g., retest workflow)
3. Click **Create**

### Step 3: Execute Solution
1. Find your solution in the list
2. Click the green **Execute** button
3. Watch the magic happen! ✨

### Step 4: Observe Live Visualization
You'll see:
- 🔵 **Blue glow**: Workflow currently executing
- 🟢 **Green glow**: Workflow completed
- 🟣 **Purple boxes**: AI-extracted facts and summaries
- ⚡ **Animated arrows**: Context transfer between workflows
- 📊 **Statistics**: Real-time execution progress

### Step 5: View Results
After execution completes:
- **Overall Summary**: AI-generated comprehensive analysis
- **Total Facts**: All insights extracted across workflows
- **Individual Summaries**: Per-workflow AI analysis

## Example Solution: Stock Analysis

### Setup
```
Solution Name: "Stock Market Intelligence"
Workflows:
  1. Stock Analysis Workflow (with stock_prediction_tool)
  2. Research Workflow (with duckduckgo_search)
```

### What Happens:
1. **Workflow 1**: Fetches stock data
   - Gemini extracts: "AAPL price: $180", "Volume increased 20%"
   - Stores in memory

2. **Handoff** → Gemini analyzes and passes relevant context

3. **Workflow 2**: Searches news with stock context
   - Receives: "Research news about AAPL showing 20% volume increase"
   - Gemini extracts: "New iPhone launch", "Strong earnings report"

4. **Final Summary**: Combines all insights
   - "AAPL showing strong momentum with new product launch and high trading volume"

## Key Features

### 🧠 AI-Powered (Gemini 1.5 Pro)
- Extracts key facts from workflow outputs
- Creates concise summaries
- Intelligently determines what context to pass
- Generates comprehensive final analysis

### ⚡ Real-Time Updates
- WebSocket connection for instant updates
- No page refresh needed
- See exactly what's happening as it happens

### 🎨 Beautiful Dark UI
- Consistent with your existing theme
- Smooth animations and transitions
- Visual indicators for every state
- Professional gradient buttons with glowing shadows

### 💾 Conversation Memory
- Maintains context across entire solution
- Each workflow builds on previous insights
- Clear solution memory when needed

## API Examples

### Execute Workflow with Context
```bash
curl -X POST http://localhost:8000/api/workflows/retest/run \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Analyze AAPL stock",
    "format": "structured",
    "solution_id": "my_solution",
    "previous_workflow_id": "previous_workflow"
  }'
```

### Get Solution Summary
```bash
curl http://localhost:8000/api/workflows/solution/my_solution/summary
```

### Clear Solution Memory
```bash
curl -X DELETE http://localhost:8000/api/workflows/solution/my_solution/memory
```

## WebSocket Connection (JavaScript)
```javascript
const ws = new WebSocket('ws://localhost:8000/api/workflows/ws/client_123');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  if (data.type === 'workflow_kag') {
    console.log('AI Analysis:', data.summary);
    console.log('Facts:', data.facts);
  }
};
```

## Troubleshooting

### Backend not starting?
```powershell
# Stop existing
Stop-Job -Id 7 -ErrorAction SilentlyContinue
Remove-Job -Id 7 -ErrorAction SilentlyContinue

# Start fresh
Start-Job -ScriptBlock { 
  cd c:\Sorry\agentic_app
  $env:PYTHONPATH = "c:\Sorry\agentic_app"
  python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 
}
```

### Check backend status
```powershell
# View logs
Get-Job -Id 7 | Receive-Job -Keep

# Test endpoint
curl http://localhost:8000/health
```

### Frontend not updating?
1. Refresh browser: `Ctrl + F5`
2. Check console for errors: `F12`
3. Verify WebSocket connection in Network tab

### Gemini API errors?
- Check `.env` file has correct API key
- Verify internet connection
- Check backend logs for specific error

## Files Created/Modified

### Backend
- ✅ `app/services/gemini_client.py` - Gemini API integration
- ✅ `app/services/kag_service.py` - Knowledge-Aided Generation
- ✅ `app/routers/workflows.py` - Enhanced with communication endpoints
- ✅ `.env` - Added Gemini API key

### Frontend
- ✅ `frontend/src/components/SolutionsExecutor.js` - Main execution UI
- ✅ `frontend/src/components/WorkflowCommunicationVisualizer.js` - Live visualization
- ✅ `frontend/src/App.js` - Updated routing

### Documentation
- ✅ `WORKFLOW_COMMUNICATION_GUIDE.md` - Complete reference
- ✅ `WORKFLOW_COMMUNICATION_QUICKSTART.md` - This file

## Next Steps

1. **Test the feature**:
   - Create a solution with 2-3 workflows
   - Execute and watch the visualization
   - Check the AI-generated summaries

2. **Explore the code**:
   - See how Gemini extracts facts
   - Modify prompts for your use case
   - Customize visualization colors

3. **Build complex solutions**:
   - Chain multiple workflows
   - Use different tools in each workflow
   - Let AI handle the context transfer

## Tips for Best Results

### Workflow Design
- Give each workflow a clear, focused task
- Use descriptive names and descriptions
- Order workflows logically (collect → analyze → act)

### Query Optimization
- Be specific in your queries
- Include relevant context
- Let AI extract the key information

### Visualization
- Execute during development to see the flow
- Use it to debug workflow interactions
- Share with stakeholders for demos

## Support & Resources

- **Full Documentation**: `WORKFLOW_COMMUNICATION_GUIDE.md`
- **Backend Code**: `app/services/` and `app/routers/workflows.py`
- **Frontend Code**: `frontend/src/components/SolutionsExecutor.js`
- **API Testing**: Use the included `api_requests.http` file

## Enjoy! 🚀

You now have an AI-powered workflow orchestration system with:
- Intelligent context transfer
- Beautiful live visualization
- Comprehensive analysis
- Professional UI

Start creating solutions and watch the AI connect your workflows! ✨
