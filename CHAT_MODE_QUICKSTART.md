# 🤖 Chat Mode - Quick Start Guide

## What is Chat Mode?

Chat Mode transforms any workflow into an **interactive chatbot** with **persistent conversations**. Instead of one-off executions, you can have **multi-turn dialogues** where the workflow remembers previous messages and maintains context across interactions.

## Quick Example

```python
import requests

BASE = "http://localhost:8000/v1"

# Create a chat session
session = requests.post(f"{BASE}/chat/sessions", json={
    "workflow_id": "ai_research_workflow",
    "initial_message": "I want to learn Python"
}).json()

session_id = session['session_id']

# Continue the conversation - context is preserved!
response = requests.post(
    f"{BASE}/chat/sessions/{session_id}/message",
    json={"message": "What are the basics?"}
).json()

print(response['messages'][-1]['content'])

# Ask follow-up - it remembers everything!
response = requests.post(
    f"{BASE}/chat/sessions/{session_id}/message",
    json={"message": "Can you give me an example?"}
).json()

print(response['messages'][-1]['content'])
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/chat/sessions` | POST | Create new chat session |
| `/v1/chat/sessions` | GET | List all sessions |
| `/v1/chat/sessions/{id}` | GET | Get session with full history |
| `/v1/chat/sessions/{id}/message` | POST | Send message to session |
| `/v1/chat/sessions/{id}/clear` | POST | Clear message history |
| `/v1/chat/sessions/{id}` | DELETE | Delete session |

## Interactive Demo

Run the interactive CLI demo:

```bash
python chat_demo.py
```

This lets you:
- 📋 Select any workflow
- 💬 Have natural back-and-forth conversations
- 📜 View full conversation history
- ✨ Experience context preservation in action

## Key Features

✅ **Persistent Sessions** - Each conversation saved with unique ID  
✅ **Context Preservation** - Workflows remember all previous messages  
✅ **State Management** - Full workflow state maintained across turns  
✅ **Multi-Turn Conversations** - Natural back-and-forth dialogues  
✅ **Session History** - Retrieve full conversation anytime  
✅ **Multiple Sessions** - Run parallel conversations with different workflows  

## Use Cases

### 1. AI Learning Assistant
```python
# Student asks questions, gets guided learning
session = create_session("ai_research_workflow", "Teach me Python")
send_message(session_id, "What should I learn first?")
send_message(session_id, "Can you explain that more?")  # Remembers context!
```

### 2. Code Review Bot
```python
# Iterative code improvement
session = create_session("code_review_workflow", "Review this code: ...")
send_message(session_id, "What about performance?")
send_message(session_id, "Show me how to optimize it")
```

### 3. Research Assistant
```python
# Guided research with follow-ups
session = create_session("ai_research_workflow", "Research AI trends")
send_message(session_id, "What about neural networks?")
send_message(session_id, "Give me specific examples")
```

## Testing

All 6 chat mode tests passing! ✅

```bash
# Run all chat tests
pytest tests/test_chat_mode.py -v

# Tests include:
# ✅ Multi-turn conversations
# ✅ Context preservation
# ✅ Session listing/filtering
# ✅ History retrieval
# ✅ Clear and delete operations
```

## How It Works

1. **Create Session** → Initial state created
2. **Send Message** → User message added to state
3. **Workflow Executes** → With full conversation context
4. **Response Generated** → Based on all previous messages
5. **State Saved** → Ready for next turn
6. **Repeat** → Continuous conversation!

```
User: "I want to learn Python"
  ↓
Assistant: "Great! Let's start with the basics..."
  ↓ [STATE SAVED]
User: "What about functions?"
  ↓ [Workflow sees previous context]
Assistant: "Based on what we discussed, here's how functions work..."
  ↓ [STATE UPDATED]
User: "Show me an example"
  ↓ [Full context available]
Assistant: "Here's an example building on our previous discussion..."
```

## Storage

Sessions stored in `data/chat_sessions/`:
- Each session = one YAML file
- Contains full message history
- Preserves workflow state
- Includes metadata

## Documentation

📚 **Full Documentation**: See `CHAT_MODE.md` for:
- Complete API reference
- Detailed usage examples
- Architecture overview
- Best practices
- Troubleshooting

## Benefits vs. Regular Execution

| Feature | Regular Execution | Chat Mode |
|---------|------------------|-----------|
| Context | One-time only | Persistent ✅ |
| State | Lost after execution | Saved ✅ |
| Conversations | Not possible | Natural dialogues ✅ |
| History | Not stored | Full history ✅ |
| Use Case | Batch processing | Interactive assistance ✅ |

---

**🎉 Your workflows are now chatbots!** Start conversations with any workflow and maintain context across unlimited turns!
