# Workflow Output Formatting - Visual Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                         WORKFLOW EXECUTION                          │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    LangGraph Orchestrator                           │
│  • Runs agents in sequence/parallel                                │
│  • Executes tools                                                   │
│  • Manages state and communication                                  │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         RAW RESULT                                  │
│  {                                                                  │
│    "result": {                                                      │
│      "node-1": {                                                    │
│        "agent_id": "...",                                           │
│        "agent_name": "...",                                         │
│        "llm_response": "...",                                       │
│        "tool_results": {...deeply nested...}                        │
│      }                                                              │
│    },                                                               │
│    "meta": {                                                        │
│      "communication_log": [...duplicates...],                       │
│      "shared_state": {...more data...}                             │
│    }                                                                │
│  }                                                                  │
│                                                                     │
│  Size: ~5KB | Readable: ❌ | Duplicates: Yes                       │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                    format_output=True (default)
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     OUTPUT FORMATTER                                │
│                                                                     │
│  1. Extract essential data                                         │
│  2. Remove duplicates                                              │
│  3. Clean structure                                                │
│  4. Add summary                                                    │
│  5. Organize metadata                                              │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    │              │              │
                    ▼              ▼              ▼
         ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
         │  STRUCTURED  │ │   COMPACT    │ │     TEXT     │
         │   (default)  │ │   (minimal)  │ │   (report)   │
         └──────────────┘ └──────────────┘ └──────────────┘
                │                 │                 │
                ▼                 ▼                 ▼
         ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
         │ • Summary    │ │ • Workflow   │ │ Formatted    │
         │ • Results    │ │   ID         │ │ text report  │
         │ • Metadata   │ │ • Status     │ │ with boxes   │
         │              │ │ • Responses  │ │ and lines    │
         │ ~1KB         │ │ ~500 bytes   │ │ ~2KB         │
         │ Readable: ✅  │ │ Readable: ✅  │ │ Readable: ✅✅ │
         └──────────────┘ └──────────────┘ └──────────────┘

                          ┌──────────────┐
                          │     RAW      │
                          │  (debug)     │
                          └──────────────┘
                                 │
                                 ▼
                          ┌──────────────┐
                          │ Original     │
                          │ nested JSON  │
                          │ ~5KB         │
                          │ Readable: ❌  │
                          └──────────────┘

═══════════════════════════════════════════════════════════════════════

                         FORMAT SELECTION

API Request:
  POST /workflows/{id}/run?format=structured  ← Default
  POST /workflows/{id}/run?format=compact
  POST /workflows/{id}/run?format=text
  POST /workflows/{id}/run?format=raw

Python Code:
  result = await orchestrator.run_workflow(workflow)  ← Structured
  result = await orchestrator.run_workflow(workflow, format_output=False)  ← Raw

═══════════════════════════════════════════════════════════════════════

                      EXAMPLE: STRUCTURED OUTPUT

{
  "workflow_id": "research-workflow",
  "run_id": "abc-123",
  "status": "success",
  "timestamp": "2025-11-08T12:00:00",
  "summary": "Workflow completed successfully. Executed 2 node(s).",
  "results": {
    "node-1": {
      "node_id": "node-1",
      "agent": "Research Agent",
      "task": "Search for AI news",
      "response": "Here are the latest developments...",
      "tools_executed": [
        {
          "tool": "web-search-tool",
          "status": "success",
          "summary": "Found 5 results"
        }
      ]
    },
    "node-2": {
      "node_id": "node-2",
      "agent": "Analysis Agent",
      "task": "Analyze findings",
      "response": "Based on the research...",
      "tools_executed": []
    }
  },
  "metadata": {
    "total_nodes": 2,
    "agents_used": ["researcher-agent"],
    "execution_steps": 2
  }
}

═══════════════════════════════════════════════════════════════════════

                         SIZE COMPARISON

Before (Raw):     ████████████████████  5,120 bytes
After (Struct):   ████                  1,024 bytes  (80% reduction!)
After (Compact):  ██                      512 bytes  (90% reduction!)

═══════════════════════════════════════════════════════════════════════

                            BENEFITS

✅ Smaller response size (faster loading)
✅ No duplicate data (efficient)
✅ Clean structure (easy to parse)
✅ User-friendly (better UX)
✅ Multiple formats (flexible)
✅ Backwards compatible (no breaking changes)

═══════════════════════════════════════════════════════════════════════
```

## Data Flow Diagram

```
USER REQUEST
     │
     ▼
┌─────────────────┐
│  API Endpoint   │  /workflows/{id}/run?format=compact
└─────────────────┘
     │
     ▼
┌─────────────────┐
│   Orchestrator  │  Executes workflow
└─────────────────┘
     │
     ▼
┌─────────────────┐
│   Raw Result    │  Nested JSON, duplicates, 5KB
└─────────────────┘
     │
     ▼ (format_output=True)
┌─────────────────┐
│Output Formatter │  Transforms and cleans
└─────────────────┘
     │
     ▼
┌─────────────────┐
│Structured Result│  Clean JSON, 1KB
└─────────────────┘
     │
     ▼
┌─────────────────┐
│ USER RESPONSE   │  Easy to use!
└─────────────────┘
```

## Component Interaction

```
┌──────────────────────────────────────────────────────────┐
│                    FastAPI Router                        │
│                (workflows.py)                            │
│                                                          │
│  • Receives request with format parameter                │
│  • Calls orchestrator                                    │
│  • Applies format transformation                         │
│  • Returns formatted result                              │
└──────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────┐
│                   Orchestrator                           │
│               (orchestrator.py)                          │
│                                                          │
│  • Builds workflow graph                                 │
│  • Executes agents and tools                             │
│  • Collects raw results                                  │
│  • Calls formatter if requested                          │
└──────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────┐
│                Output Formatter                          │
│             (output_formatter.py)                        │
│                                                          │
│  Methods:                                                │
│  • format_workflow_result() → Structured                 │
│  • format_compact() → Compact                            │
│  • format_for_display() → Text                           │
└──────────────────────────────────────────────────────────┘
```

## Format Decision Tree

```
                    Format Parameter?
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
    structured          compact            text
         │                 │                 │
         ▼                 ▼                 ▼
    Clean JSON       Minimal JSON      Text Report
    Medium size       Small size       Large size
    Default           Mobile            Console
```

## Before vs After Visualization

```
BEFORE (Raw):
┌─────────────────────────────────────────┐
│ result                                  │
│  ├─ node-1                              │
│  │   ├─ agent_id: "..."                │
│  │   ├─ agent_name: "..."              │
│  │   ├─ agent_type: "..."              │
│  │   ├─ task: "..."                    │
│  │   ├─ llm_response: "..."            │
│  │   ├─ context_size: 5                │
│  │   └─ tool_results                   │
│  │       └─ web-search-tool            │
│  │           ├─ tool: "..."            │
│  │           ├─ query: "..."           │
│  │           └─ results: [...]         │
│  └─ node-2 (similar nesting)           │
│                                         │
│ meta                                    │
│  ├─ communication_log: [...]           │
│  ├─ shared_state: {...}                │
│  ├─ agents_used: [...]                 │
│  └─ total_messages: 2                  │
│                                         │
│ state (duplicate of everything)        │
└─────────────────────────────────────────┘
Size: 5KB | Depth: 5 levels | Duplicates: Yes

AFTER (Structured):
┌─────────────────────────────────────────┐
│ workflow_id: "..."                      │
│ run_id: "..."                           │
│ status: "success"                       │
│ summary: "Completed successfully"       │
│                                         │
│ results                                 │
│  ├─ node-1                              │
│  │   ├─ agent: "Research Agent"        │
│  │   ├─ response: "..."                │
│  │   └─ tools_executed: [...]          │
│  └─ node-2 (same structure)             │
│                                         │
│ metadata                                │
│  ├─ total_nodes: 2                     │
│  ├─ agents_used: [...]                 │
│  └─ execution_steps: 2                 │
└─────────────────────────────────────────┘
Size: 1KB | Depth: 2 levels | Duplicates: No
```
