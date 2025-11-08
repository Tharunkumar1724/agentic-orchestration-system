# Quick Reference Guide

## Start Server
```powershell
.\start.ps1
```
Server runs at: http://localhost:8000
API Docs: http://localhost:8000/docs

## Run Tests
```powershell
pytest tests/ -v
```

## Common Operations

### 1. Create WebSearch Tool
```bash
curl -X POST http://localhost:8000/v1/tools/ -H "Content-Type: application/json" -d '{"id":"search1","name":"Search","type":"websearch","config":{}}'
```

### 2. Create React Agent with Tool
```bash
curl -X POST http://localhost:8000/v1/agents/ -H "Content-Type: application/json" -d '{"id":"agent1","name":"Agent","type":"react","tools":["search1"],"use_kag":true}'
```

### 3. Create Sequential Workflow
```bash
curl -X POST http://localhost:8000/v1/workflows/ -H "Content-Type: application/json" -d '{"id":"wf1","name":"Flow","entrypoint":{"id":"root","type":"sequence","children":[{"id":"s1","type":"agent","ref":"agent1","inputs":{"prompt":"test"}}]}}'
```

### 4. Run Workflow
```bash
curl -X POST http://localhost:8000/v1/workflows/wf1/run
```

### 5. List Resources
```bash
curl http://localhost:8000/v1/tools/
curl http://localhost:8000/v1/agents/
curl http://localhost:8000/v1/workflows/
```

## Tool Types
- `websearch` - Web search
- `code` - Python execution
- `api` - HTTP calls

## Agent Types
- `zero_shot` - Simple LLM
- `react` - Reasoning + tools
- `custom` - Custom logic

## Workflow Patterns
- `sequence` - Sequential execution
- `parallel` - Concurrent execution  
- `router` - Conditional branching

## Key Files
- `data/` - JSON storage
- `data/runs/` - Workflow results
- `tests/` - Test suite
- `API_EXAMPLES.md` - Full examples
- `README.md` - Complete docs

## Troubleshooting

**Server won't start?**
```powershell
$env:PYTHONPATH="c:\Sorry\agentic_app"
python -m uvicorn app.main:app --port 8000
```

**Tests failing?**
```powershell
pytest tests/test_workflow.py -v -s
```

**Check data saved?**
```powershell
ls data/tools/
ls data/agents/
ls data/workflows/
ls data/runs/
```
