# Solution Types - Quick Start Guide

## 🚀 Quick Overview

You can now create solutions with two different communication strategies:

| Mode | Strategy | Best For |
|------|----------|----------|
| 💡 **Normal** | KAG + Conversational Buffer | General workflows, fact extraction |
| 🔬 **Research** | Agentic RAG | Advanced retrieval, deep context |

---

## 📖 Create Your First Solution

### Option 1: Normal Mode (Default)

**Use when**: You need standard workflow communication with fact extraction.

```javascript
// Frontend (React)
const solution = {
  name: "Stock Analysis",
  solution_type: "normal",  // KAG + Buffer
  workflows: ["research", "analysis", "report"]
}
```

**What happens**:
- ✅ Each workflow output analyzed by Gemini
- ✅ Facts extracted automatically
- ✅ Facts + buffer passed to next workflow
- ✅ Fast and efficient

### Option 2: Research Mode

**Use when**: You need intelligent retrieval and deep context awareness.

```javascript
// Frontend (React)
const solution = {
  name: "Deep Market Research",
  solution_type: "research",  // Agentic RAG
  workflows: ["data_collection", "analysis", "insights"]
}
```

**What happens**:
- ✅ Agent memory initialized at each workflow start
- ✅ RAG retrieves relevant context from previous workflows
- ✅ Intelligent handoffs with summarization
- ✅ Perfect for research-intensive tasks

---

## 🎨 Using the UI

### Step 1: Create Solution

1. Go to **Solutions** page
2. Click **Create Solution**
3. Fill in basic info:
   - Name: e.g., "Stock Analysis"
   - Description: What this solution does

### Step 2: Choose Solution Type

You'll see two cards:

```
┌─────────────────────────┐  ┌─────────────────────────┐
│ ✓ Normal                │  │   Research              │
│ 💡 KAG + Buffer         │  │   🔬 Agentic RAG        │
│                         │  │                         │
│ Best for general        │  │ Advanced retrieval with │
│ workflows with fact     │  │ agent memory            │
│ extraction              │  │ initialization          │
└─────────────────────────┘  └─────────────────────────┘
```

**Click the one that fits your needs!**

### Step 3: Add Workflows

- Select workflows from the list
- They'll execute in order
- Context passes automatically

### Step 4: Execute

1. Click the chat icon on your solution
2. Type your query (e.g., "Analyze AAPL stock")
3. Watch the workflows execute with the chosen strategy!

---

## 🔍 How to Tell Which Mode is Active

### In Solution List

Look for the badge next to the solution name:
- 💡 **Normal (KAG+Buffer)** - Green badge
- 🔬 **Research (Agentic RAG)** - Purple badge

### In Chat Interface

The header shows the mode:
```
🧠 My Research Solution  [🔬 Research Mode (Agentic RAG)]
```

During execution, you'll see:
```
🚀 Starting execution of 3 workflows using 🔬 Agentic RAG...
```

For Research mode, you'll also see:
```
🧠 Agent memory initialized for node_xyz with RAG context
```

---

## 💡 Decision Guide

### Choose Normal Mode When:

- ✅ You have standard data processing workflows
- ✅ Fact extraction is sufficient
- ✅ Workflows are relatively independent
- ✅ Speed is important
- ✅ Simple context transfer is enough

**Example Use Cases**:
- Stock price analysis
- Data aggregation pipelines
- Report generation
- Simple multi-step processes

### Choose Research Mode When:

- ✅ Workflows need deep context from previous steps
- ✅ You're doing research-intensive work
- ✅ Intelligent retrieval is important
- ✅ Context complexity is high
- ✅ You want agent memory at node start

**Example Use Cases**:
- Market research with multiple data sources
- Academic research workflows
- Complex financial analysis
- Multi-source data correlation
- Long-running analytical pipelines

---

## 🔧 API Quick Reference

### Create Normal Solution

```python
import requests

response = requests.post("http://localhost:8000/solutions/", json={
    "name": "My Normal Solution",
    "description": "Uses KAG for communication",
    "solution_type": "normal",
    "workflows": ["workflow1", "workflow2"]
})
```

### Create Research Solution

```python
import requests

response = requests.post("http://localhost:8000/solutions/", json={
    "name": "My Research Solution",
    "description": "Uses Agentic RAG for communication",
    "solution_type": "research",
    "workflows": ["workflow1", "workflow2"]
})
```

### Update Existing Solution Type

```python
import requests

response = requests.put(
    "http://localhost:8000/solutions/solution_123",
    json={"solution_type": "research"}
)
```

---

## 🎯 Common Questions

### Q: Can I change the solution type after creation?

**A**: Yes! Edit the solution and change the type. Next execution will use the new strategy.

### Q: What happens to existing solutions?

**A**: They default to "normal" mode for backward compatibility.

### Q: Is Research mode slower?

**A**: Slightly, due to RAG retrieval, but the deep context often makes up for it with better results.

### Q: Can I mix modes in a solution?

**A**: No, each solution uses one mode for all its workflows. Create separate solutions if you need different modes.

### Q: Do I need to change my workflows?

**A**: No! The same workflows work with both modes. The difference is in how they communicate.

---

## 🧪 Try It Now!

### Quick Test

1. **Start the backend**:
   ```bash
   python -m uvicorn app.main:app --reload --port 8000
   ```

2. **Start the frontend**:
   ```bash
   cd frontend && npm start
   ```

3. **Create two solutions**:
   - One Normal mode
   - One Research mode
   - Use the same workflows in both

4. **Execute both with the same query**

5. **Compare the execution**:
   - Normal: Fast, fact-based handoffs
   - Research: RAG retrieval, agent memory

---

## 📊 What to Expect

### Normal Mode Execution

```
🚀 Starting execution using 💡 KAG + Conversational Buffer...
⚡ Executing: Research Workflow
✅ Research Workflow completed!
🤝 Transferring context: research → analysis
⚡ Executing: Analysis Workflow
✅ Analysis Workflow completed!
🎉 All workflows completed!
```

### Research Mode Execution

```
🚀 Starting execution using 🔬 Agentic RAG...
⚡ Executing: Research Workflow
🧠 Agent memory initialized with RAG context
✅ Research Workflow completed!
🤝 Intelligent handoff prepared with retrieval
⚡ Executing: Analysis Workflow
🧠 Agent memory initialized with RAG context
✅ Analysis Workflow completed!
🎉 All workflows completed!
```

---

## ✅ Checklist

Before using solution types, make sure:

- [ ] Backend is running
- [ ] Frontend is running
- [ ] You have at least 2 workflows created
- [ ] You understand the difference between modes
- [ ] You've chosen the right mode for your use case

---

## 🎓 Learn More

For detailed technical information, see:
- `SOLUTION_TYPES_IMPLEMENTATION.md` - Full implementation details
- `KAG_LANGGRAPH_GUIDE.md` - How KAG works
- `SOLUTION_SYSTEM_COMPLETE.md` - Solution system overview

---

**Ready to create intelligent multi-workflow solutions? Let's go! 🚀**
