"""
Quick comparison: Before vs After output formatting
"""

import json

# BEFORE: Raw unstructured output (what users were seeing)
raw_output = {
    "workflow_id": "test-workflow",
    "run_id": "abc-123",
    "status": "success",
    "result": {
        "node-1": {
            "agent_id": "researcher-agent",
            "agent_name": "Research Agent",
            "agent_type": "react",
            "task": "Search for AI news",
            "llm_response": "Here is a detailed analysis of AI developments spanning multiple paragraphs with technical details...",
            "context_size": 5,
            "tool_results": {
                "web-search-tool": {
                    "tool": "web-search-tool",
                    "query": "AI news",
                    "count": 5,
                    "results": [
                        {"title": "Article 1", "href": "http://...", "body": "Long article text..."},
                        {"title": "Article 2", "href": "http://...", "body": "Long article text..."},
                        # ... more nested data
                    ]
                }
            },
            "tools_used": ["Web Search"]
        }
    },
    "meta": {
        "communication_log": [
            {
                "sender": "node-1",
                "agent": "researcher-agent",
                "content": {
                    # ... deeply nested duplicate data
                },
                "type": "agent_result"
            }
        ],
        "shared_state": {
            # ... more nested data
        },
        "agents_used": ["researcher-agent"],
        "total_messages": 1,
        "final_step": "node-1"
    },
    "state": {
        # ... complete state duplication
    }
}

# AFTER: Clean structured output (what users see now)
structured_output = {
    "workflow_id": "test-workflow",
    "run_id": "abc-123",
    "status": "success",
    "timestamp": "2025-11-08T12:00:00",
    "summary": "Workflow completed successfully. Executed 1 node(s).",
    "results": {
        "node-1": {
            "node_id": "node-1",
            "agent": "Research Agent",
            "task": "Search for AI news",
            "response": "Here is a detailed analysis of AI developments...",
            "tools_executed": [
                {
                    "tool": "web-search-tool",
                    "status": "success",
                    "summary": "Found 5 results"
                }
            ]
        }
    },
    "metadata": {
        "total_nodes": 1,
        "agents_used": ["researcher-agent"],
        "execution_steps": 1
    }
}

print("=" * 80)
print("BEFORE: Raw Output (Unstructured)")
print("=" * 80)
print("❌ Problems:")
print("  - Deeply nested structure")
print("  - Duplicate data in multiple places")
print("  - Technical internals exposed")
print("  - Hard to read and parse")
print("  - Large response size")
print()
print("Example size: ~5KB+ for simple workflow")
print()

print("=" * 80)
print("AFTER: Structured Output")
print("=" * 80)
print("✅ Improvements:")
print("  - Clean, flat structure")
print("  - No duplication")
print("  - User-friendly format")
print("  - Easy to read and parse")
print("  - Smaller response size")
print()
print("Example size: ~1KB for same workflow (80% reduction!)")
print()

print("=" * 80)
print("STRUCTURED FORMAT")
print("=" * 80)
print(json.dumps(structured_output, indent=2))
print()

print("=" * 80)
print("💡 TIP: You can still access raw format for debugging:")
print("   format=raw in API call or format_output=False in code")
print("=" * 80)
