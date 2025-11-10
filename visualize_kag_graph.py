"""
Visualize KAG LangGraph Workflow
Generate a visual representation of the KAG state machine
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.services.kag_service import KAGService


def visualize_kag_graph():
    """Generate and display KAG workflow graph"""
    print("\n🎨 KAG LangGraph Workflow Visualization\n")
    print("=" * 80)
    
    service = KAGService()
    
    # Print ASCII diagram
    print("""
    KAG WORKFLOW GRAPH (LangGraph State Machine)
    
    ┌─────────────────────────────────────────────────────────────────┐
    │                         START                                   │
    └───────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
    ┌─────────────────────────────────────────────────────────────────┐
    │                  NODE 1: Retrieve Context                       │
    │  - Get previous workflow outputs from memory                    │
    │  - Build full context with historical data                      │
    │  - State: previous_context, context                             │
    └───────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
    ┌─────────────────────────────────────────────────────────────────┐
    │                  NODE 2: Extract Facts                          │
    │  - Use Gemini to analyze workflow output                        │
    │  - Extract key facts and insights                               │
    │  - State: facts, reasoning                                      │
    └───────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
    ┌─────────────────────────────────────────────────────────────────┐
    │                  NODE 3: Generate Summary                       │
    │  - Create concise summary from facts                            │
    │  - Use LLM for natural language generation                      │
    │  - State: summary                                               │
    └───────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
    ┌─────────────────────────────────────────────────────────────────┐
    │                  NODE 4: Store Memory                           │
    │  - Persist facts, summary, reasoning to memory                  │
    │  - Enable context for future workflows                          │
    │  - State: memory_stored                                         │
    └───────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
    ┌─────────────────────────────────────────────────────────────────┐
    │                          END                                    │
    │  Returns: {summary, facts, reasoning, memory_stored}            │
    └─────────────────────────────────────────────────────────────────┘
    
    STATE SCHEMA:
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    - workflow_output: str        # Input workflow execution result
    - workflow_name: str          # Name of the workflow
    - solution_id: str            # ID of parent solution
    - workflow_id: str            # Unique workflow identifier
    - context: str                # Additional context
    - previous_context: str       # Retrieved historical context
    - facts: List[str]            # Extracted facts
    - summary: str                # Generated summary
    - reasoning: str              # LLM reasoning
    - memory_stored: bool         # Storage confirmation
    - error: Optional[str]        # Error handling
    
    FEATURES:
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ✅ Sequential workflow execution with LangGraph
    ✅ State management across 4 processing nodes
    ✅ Gemini AI integration for fact extraction
    ✅ Context preservation across multiple workflows
    ✅ Memory management for solution-wide intelligence
    ✅ Error handling at each node
    ✅ Singleton pattern for service instance
    """)
    
    print("=" * 80)
    print("\n📊 Graph Statistics:")
    print(f"  - Total Nodes: 4")
    print(f"  - State Fields: 11")
    print(f"  - Edges: 4 (sequential)")
    print(f"  - Error Handling: Enabled at each node")
    print(f"  - Memory Backend: In-memory ConversationMemory")
    print(f"  - LLM Provider: Gemini")
    
    print("\n✅ Graph compiled and ready for execution")
    print("\n💡 Usage:")
    print("  from app.services.kag_service import get_kag_service")
    print("  service = get_kag_service()")
    print("  result = service.invoke_kag(output, name, solution_id, workflow_id)")
    print()


if __name__ == "__main__":
    visualize_kag_graph()
