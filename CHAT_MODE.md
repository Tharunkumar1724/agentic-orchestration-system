# Chat Mode Documentation

## Overview

**Chat Mode** enables continuous, context-aware conversations with any workflow. Instead of one-off executions, you can have multi-turn dialogues where the workflow remembers previous messages and maintains state across interactions - just like a chatbot!

## Key Features

✅ **Persistent Sessions** - Each conversation is saved with a unique session ID  
✅ **Context Preservation** - Workflows remember previous messages and responses  
✅ **State Management** - Full workflow state is maintained across turns  
✅ **Multi-Turn Conversations** - Have back-and-forth dialogues naturally  
✅ **Session History** - Retrieve full conversation history anytime  
✅ **Multiple Sessions** - Run multiple parallel conversations with different workflows  

## API Endpoints

### 1. Create Chat Session
```http
POST /v1/chat/sessions
```

**Request Body:**
```json
{
  "workflow_id": "ai_research_workflow",
  "initial_message": "Hello! Can you help me learn Python?",
  "metadata": {
    "user": "john_doe",
    "source": "web_app"
  }
}
```

**Response:**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "workflow_id": "ai_research_workflow",
  "created_at": "2025-11-05T10:30:00",
  "updated_at": "2025-11-05T10:30:05",
  "messages": [
    {
      "role": "user",
      "content": "Hello! Can you help me learn Python?",
      "timestamp": "2025-11-05T10:30:00"
    },
    {
      "role": "assistant",
      "content": "Of course! I'd be happy to help...",
      "timestamp": "2025-11-05T10:30:05"
    }
  ],
  "state": {},
  "metadata": {"user": "john_doe"}
}
```

### 2. Send Message
```http
POST /v1/chat/sessions/{session_id}/message
```

**Request Body:**
```json
{
  "message": "What are the best practices for Python functions?",
  "stream": false
}
```

**Response:** Returns updated session with new messages

### 3. Get Session History
```http
GET /v1/chat/sessions/{session_id}
```

**Response:** Full session object with all messages

### 4. List Sessions
```http
GET /v1/chat/sessions
GET /v1/chat/sessions?workflow_id=ai_research_workflow
```

**Response:** Array of all sessions, optionally filtered by workflow

### 5. Clear Session History
```http
POST /v1/chat/sessions/{session_id}/clear
```

Clears all messages but keeps the session active.

### 6. Delete Session
```http
DELETE /v1/chat/sessions/{session_id}
```

Permanently deletes the session.

## Usage Examples

### Example 1: Python Learning Chat

```python
import requests

BASE_URL = "http://localhost:8000/v1"

# Create session
response = requests.post(f"{BASE_URL}/chat/sessions", json={
    "workflow_id": "ai_research_workflow",
    "initial_message": "I want to learn Python"
})
session = response.json()
session_id = session['session_id']

# Continue conversation
response = requests.post(
    f"{BASE_URL}/chat/sessions/{session_id}/message",
    json={"message": "What are the basics I should start with?"}
)
print(response.json()['messages'][-1]['content'])

# Ask follow-up (context is preserved!)
response = requests.post(
    f"{BASE_URL}/chat/sessions/{session_id}/message",
    json={"message": "Can you give me an example?"}
)
print(response.json()['messages'][-1]['content'])
```

### Example 2: Code Review Chat

```python
# Start code review session
response = requests.post(f"{BASE_URL}/chat/sessions", json={
    "workflow_id": "code_review_workflow",
    "initial_message": "Review this: def add(a, b): return a + b"
})
session_id = response.json()['session_id']

# Ask for improvements
requests.post(
    f"{BASE_URL}/chat/sessions/{session_id}/message",
    json={"message": "What specific improvements would you suggest?"}
)

# Ask follow-up
requests.post(
    f"{BASE_URL}/chat/sessions/{session_id}/message",
    json={"message": "How would I add type hints?"}
)
```

### Example 3: Using cURL

```bash
# Create session
curl -X POST http://localhost:8000/v1/chat/sessions \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_id": "ai_research_workflow",
    "initial_message": "Tell me about LangGraph"
  }'

# Send message (replace SESSION_ID)
curl -X POST http://localhost:8000/v1/chat/sessions/SESSION_ID/message \
  -H "Content-Type: application/json" \
  -d '{"message": "How does it compare to LangChain?"}'

# Get history
curl http://localhost:8000/v1/chat/sessions/SESSION_ID
```

## Interactive Demo

Run the interactive chat demo:

```bash
python chat_demo.py
```

This provides a command-line interface to:
- Select any workflow
- Have a natural conversation
- View conversation history
- See context preservation in action

## How It Works

### 1. State Preservation

Each session maintains a `WorkflowState` object that includes:
- **messages**: Full conversation history
- **shared_data**: Data shared between agents
- **agents_used**: Which agents have been invoked
- **results**: Results from each workflow execution
- **error**: Any error state

### 2. Context Flow

```
User Message 1 → Workflow → Assistant Response 1
                  ↓
              [STATE SAVED]
                  ↓
User Message 2 → Workflow (with previous state) → Assistant Response 2
                  ↓
              [STATE UPDATED]
                  ↓
User Message 3 → Workflow (with all previous context) → Response 3
```

### 3. Agent Context

When you send a message:
1. Previous conversation is loaded from session
2. User's new message is added to workflow state
3. Workflow executes with full context
4. Agents can see previous messages via `state["messages"]`
5. Response is added to session and returned

## Benefits

### vs. Regular Workflow Execution

| Feature | Regular Execution | Chat Mode |
|---------|------------------|-----------|
| Context | One-time only | Persistent across turns |
| State | Lost after execution | Saved and restored |
| Conversations | Not possible | Natural multi-turn dialogues |
| History | Not stored | Full history available |
| Use Case | Batch processing | Interactive assistance |

## Use Cases

### 1. **AI Assistant**
Create an AI assistant that remembers the entire conversation:
```python
session = create_session("ai_research_workflow", "I'm learning Python")
send_message(session_id, "What should I learn first?")
send_message(session_id, "Can you explain that more?")  # Remembers context!
```

### 2. **Code Review Bot**
Iterative code review with back-and-forth refinement:
```python
session = create_session("code_review_workflow", "Review my code: ...")
send_message(session_id, "What about performance?")
send_message(session_id, "How can I optimize it?")
```

### 3. **Research Assistant**
Guided research with follow-up questions:
```python
session = create_session("ai_research_workflow", "Tell me about AI")
send_message(session_id, "What about neural networks?")
send_message(session_id, "Give me examples")
```

### 4. **Tutorial Generator**
Interactive tutorial creation with clarifications:
```python
session = create_session("python_tutorial_workflow", "Create Python tutorial")
send_message(session_id, "Make it more detailed")
send_message(session_id, "Add more examples")
```

## Testing

Run the comprehensive test suite:

```bash
# Run all chat mode tests
pytest tests/test_chat_mode.py -v -s

# Run specific test
pytest tests/test_chat_mode.py::test_chat_mode_continuous_conversation -v -s
```

Tests cover:
- ✅ Multi-turn conversations
- ✅ Context preservation
- ✅ Session management
- ✅ History retrieval
- ✅ Session filtering
- ✅ Clear and delete operations

## Architecture

### Components

1. **ChatSession Model** (`app/models.py`)
   - Defines session structure
   - Messages, state, metadata

2. **Chat Manager** (`app/services/chat_manager.py`)
   - Session CRUD operations
   - Storage management
   - Session listing and filtering

3. **Chat Router** (`app/routers/chat.py`)
   - API endpoints
   - Request/response handling
   - Workflow orchestration

4. **Enhanced Orchestrator** (`app/services/orchestrator.py`)
   - Supports `initial_state` parameter
   - Preserves and returns full state
   - Context injection for agents

### Data Flow

```
Client Request
    ↓
Chat Router (chat.py)
    ↓
Chat Manager (chat_manager.py) - Load/Save session
    ↓
Orchestrator (orchestrator.py) - Execute with state
    ↓
LangGraph - Process with context
    ↓
Agents - See previous messages
    ↓
Results - Saved to session
    ↓
Response to Client
```

## Storage

Sessions are stored in `data/chat_sessions/` as YAML files:

```yaml
session_id: "550e8400-e29b-41d4-a716-446655440000"
workflow_id: "ai_research_workflow"
created_at: "2025-11-05T10:30:00"
updated_at: "2025-11-05T10:35:00"
messages:
  - role: "user"
    content: "Hello!"
    timestamp: "2025-11-05T10:30:00"
  - role: "assistant"
    content: "Hi! How can I help?"
    timestamp: "2025-11-05T10:30:05"
state:
  messages: [...]
  shared_data: {...}
  results: {...}
```

## Best Practices

### 1. Session Management
- Create new sessions for distinct conversations
- Reuse sessions for related follow-ups
- Clear history when switching topics
- Delete old sessions periodically

### 2. Message Design
- Be specific in initial messages
- Reference previous context naturally
- Use follow-ups to refine responses

### 3. Error Handling
- Check response status codes
- Handle session not found (404)
- Validate workflow exists before creating session

### 4. Performance
- Avoid extremely long conversations (state grows)
- Clear history periodically for long-running sessions
- Use session filtering to find specific conversations

## Troubleshooting

### Session not found
```python
response = requests.get(f"/v1/chat/sessions/{session_id}")
if response.status_code == 404:
    print("Session expired or deleted")
```

### Workflow doesn't maintain context
- Check that workflow state is being preserved
- Verify agents are reading from `state["messages"]`
- Ensure initial_state is passed to orchestrator

### Large response sizes
- Limit conversation history shown to client
- Clear old messages periodically
- Use pagination for history retrieval

## Future Enhancements

Potential improvements:
- [ ] Streaming responses (SSE)
- [ ] Session expiration/TTL
- [ ] Conversation summarization
- [ ] Multi-user sessions
- [ ] Session search/filtering
- [ ] Export conversations
- [ ] Conversation analytics

---

🎉 **You now have full chatbot capabilities for any workflow!**
