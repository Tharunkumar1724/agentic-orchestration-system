# Workflow-to-Workflow Communication System

## Overview
The Solutions feature now supports AI-powered workflow-to-workflow communication using Gemini 1.5 Pro for intelligent context transfer and live execution visualization.

## Features

### 1. **KAG (Knowledge-Aided Generation)**
- **Gemini 1.5 Pro Integration**: Uses Google's Gemini API for reasoning and fact extraction
- **Automatic Fact Extraction**: Extracts key insights from workflow outputs
- **Conversation Memory**: Maintains context across workflow executions
- **Intelligent Handoff**: AI determines what information to pass between workflows

### 2. **Live Visualization**
- **Real-time Updates**: WebSocket connection for instant status updates
- **Visual Workflow Chain**: See each workflow execute in sequence
- **Animated Transitions**: Visual handoff indicators between workflows
- **KAG Analysis Display**: Shows AI-extracted facts and summaries

### 3. **Solution Execution**
- **Sequential Workflow Execution**: Workflows run in the order specified
- **Context Transfer**: Each workflow receives insights from previous workflows
- **Comprehensive Summary**: Final summary combining all workflow results

## Architecture

### Backend Components

#### 1. Gemini Client (`app/services/gemini_client.py`)
```python
from app.services.gemini_client import get_gemini_client

client = get_gemini_client()
result = client.extract_facts(workflow_output, context)
```

**Functions:**
- `generate(prompt)`: Generate content using Gemini 1.5 Pro
- `extract_facts(output, context)`: Extract facts and create summary
- `summarize_conversation(messages)`: Create conversation summary
- `reason_about_handoff(source, target)`: Generate handoff instructions

#### 2. KAG Service (`app/services/kag_service.py`)
```python
from app.services.kag_service import invoke_kag

result = invoke_kag(
    workflow_output=output,
    workflow_name="Data Analysis",
    solution_id="solution_123",
    workflow_id="workflow_456",
    context="Additional context"
)
```

**Returns:**
```json
{
  "summary": "Concise summary of workflow output",
  "facts": ["fact1", "fact2", "fact3"],
  "reasoning": "AI analysis and insights",
  "memory_stored": true,
  "context_available": true
}
```

#### 3. Conversation Memory
Stores workflow execution history and context for the entire solution:
```python
from app.services.kag_service import get_conversation_memory

memory = get_conversation_memory()
memories = memory.get_memories(solution_id)
context = memory.get_solution_context(solution_id)
```

### API Endpoints

#### POST `/api/workflows/{workflow_id}/run`
Execute workflow with solution context:
```json
{
  "query": "Execute task",
  "format": "structured",
  "solution_id": "solution_123",
  "previous_workflow_id": "workflow_abc"
}
```

**Response includes KAG data:**
```json
{
  "workflow_id": "workflow_456",
  "run_id": "run_789",
  "status": "completed",
  "results": [...],
  "kag": {
    "summary": "...",
    "facts": [...],
    "reasoning": "...",
    "memory_stored": true
  }
}
```

#### POST `/api/workflows/communicate`
Prepare handoff between workflows:
```json
{
  "source_workflow_id": "workflow_1",
  "target_workflow_id": "workflow_2",
  "solution_id": "solution_123",
  "target_task": "Optional task description"
}
```

#### GET `/api/workflows/solution/{solution_id}/summary`
Get comprehensive solution summary:
```json
{
  "total_workflows": 3,
  "summaries": [
    {
      "workflow_name": "Data Collection",
      "summary": "...",
      "timestamp": "2025-11-09T..."
    }
  ],
  "combined_facts": ["fact1", "fact2", ...],
  "overall_context": "AI-generated overall summary"
}
```

#### DELETE `/api/workflows/solution/{solution_id}/memory`
Clear conversation memory for a solution.

#### WebSocket `/api/workflows/ws/{client_id}`
Real-time execution updates:
- `workflow_start`: Workflow begins execution
- `workflow_kag`: KAG analysis completed
- `workflow_handoff`: Context transferred to next workflow
- `workflow_complete`: Workflow finished
- `workflow_communication`: General communication events

### Frontend Components

#### 1. SolutionsExecutor (`frontend/src/components/SolutionsExecutor.js`)
Main component for managing and executing solutions:
- Create/edit/delete solutions
- Execute solutions with live visualization
- WebSocket integration for real-time updates
- Display AI-generated summaries and facts

#### 2. WorkflowCommunicationVisualizer (`frontend/src/components/WorkflowCommunicationVisualizer.js`)
Live visualization component:
- Visual workflow chain with status indicators
- Animated handoff displays
- KAG analysis results
- Execution statistics

## Usage Guide

### 1. Create a Solution
1. Navigate to **Solutions** page
2. Click **Create Solution**
3. Enter name and description
4. Select workflows to include (they will execute in order)
5. Click **Create**

### 2. Execute a Solution
1. Click the **Execute** button on a solution card
2. Watch live visualization as workflows run
3. See AI-extracted facts and summaries for each workflow
4. View final comprehensive summary

### 3. View Results
After execution completes:
- **Overall Summary**: AI-generated summary of all workflows
- **Facts Extracted**: Key insights from all workflows
- **Individual Summaries**: Per-workflow analysis

## Example Workflow

### Stock Analysis Solution
```yaml
Solution: "Market Intelligence"
Workflows:
  1. Stock Data Collection (stock_prediction_tool)
  2. News Research (duckduckgo_search)
  3. Analysis & Recommendation

Execution Flow:
  Step 1: Collect stock data → Extract: prices, trends, volume
  Step 2: Research news → Receives stock context → Extract: sentiment, events
  Step 3: Analyze → Receives all context → Generate recommendation
```

### What Happens During Execution:

1. **Workflow 1 Executes**
   - Fetches stock data
   - Gemini extracts facts: "Stock price increased 5%", "High volume"
   - Stores in conversation memory

2. **Handoff to Workflow 2**
   - Gemini analyzes what's relevant
   - Passes context: "Research news for stock showing 5% increase"
   - Workflow 2 receives enhanced context

3. **Workflow 2 Executes**
   - Searches news with stock context
   - Gemini extracts facts: "Positive earnings report", "New product launch"
   - Combines with previous memory

4. **Handoff to Workflow 3**
   - Full context from both workflows
   - Workflow 3 generates informed recommendation

5. **Final Summary**
   - Gemini creates overall summary
   - Combines all facts and insights
   - Provides comprehensive analysis

## Configuration

### Environment Variables
```env
# Required for Gemini integration
GEMINI_API_KEY=your-gemini-api-key-here

# Existing configuration
GROQ_API_KEY=your-groq-api-key-here
```

### Gemini Settings
- **Model**: gemini-1.5-pro
- **Temperature**: 0.3 (fact extraction), 0.5 (summaries), 0.6 (handoff reasoning)
- **Max Tokens**: 2048
- **Timeout**: 30 seconds

## Best Practices

### 1. Workflow Organization
- Order workflows logically (data collection → analysis → action)
- Each workflow should have a clear, focused task
- Use descriptive workflow names and descriptions

### 2. Context Usage
- First workflow: Receives initial query
- Subsequent workflows: Receive previous context + new query
- Use Gemini to filter and focus relevant information

### 3. Error Handling
- Each workflow executes independently
- Failures don't block subsequent workflows
- Check individual workflow results in visualization

### 4. Performance
- Gemini API calls add ~1-2 seconds per workflow
- WebSocket provides instant UI updates
- Memory stores lightweight summaries, not full outputs

## Troubleshooting

### WebSocket Not Connecting
- Check backend is running on port 8000
- Verify browser console for connection errors
- Ensure no firewall blocking WebSocket

### Gemini API Errors
- Verify API key is correct in `.env`
- Check rate limits (Gemini 1.5 Pro has generous limits)
- Review backend logs for detailed error messages

### Memory Not Persisting
- Memory is in-memory only (resets on backend restart)
- Use `/memory` endpoint to clear if needed
- Each solution has isolated memory

## Advanced Features

### Custom Handoff Logic
Modify `gemini_client.py` `reason_about_handoff()` to customize how context is transferred.

### Fact Filtering
Update `extract_facts()` prompt to focus on specific types of information.

### Visualization Customization
Edit `WorkflowCommunicationVisualizer.js` to change colors, animations, or layout.

## Technical Details

### Memory Structure
```python
{
  "solution_id:workflow_id": [
    {
      "workflow_id": "...",
      "workflow_name": "...",
      "summary": "...",
      "facts": [...],
      "reasoning": "...",
      "timestamp": "2025-11-09T..."
    }
  ]
}
```

### WebSocket Message Format
```json
{
  "type": "workflow_kag",
  "solution_id": "solution_123",
  "workflow_id": "workflow_456",
  "run_id": "run_789",
  "summary": "...",
  "facts": [...]
}
```

## Future Enhancements
- [ ] Persistent memory storage (database)
- [ ] Workflow branching based on AI decisions
- [ ] Multi-model support (GPT-4, Claude, etc.)
- [ ] Custom KAG templates per solution type
- [ ] Export execution reports
- [ ] Workflow dependency graphs

## API Reference Summary

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/workflows/{id}/run` | POST | Execute workflow with KAG |
| `/api/workflows/communicate` | POST | Prepare workflow handoff |
| `/api/workflows/solution/{id}/summary` | GET | Get solution summary |
| `/api/workflows/solution/{id}/memory` | DELETE | Clear solution memory |
| `/api/workflows/ws/{client_id}` | WebSocket | Live updates |

## Support
For issues or questions:
1. Check backend logs: `Receive-Job -Id <job_id> -Keep`
2. Check browser console for frontend errors
3. Verify Gemini API key is valid
4. Test individual workflows before creating solutions
