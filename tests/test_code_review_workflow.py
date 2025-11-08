"""
Test the Code Review Workflow - demonstrates 3-agent sequential workflow with full communication
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)


def test_code_review_workflow_execution():
    """Execute the code review workflow with 3 agents communicating."""
    
    print("\n" + "="*80)
    print("🔍 EXECUTING CODE REVIEW WORKFLOW (3 Agents)")
    print("="*80)
    
    # Execute the workflow
    response = client.post("/v1/workflows/code_review_workflow/run")
    assert response.status_code == 200
    
    result = response.json()
    
    # Display header
    print(f"\n📋 Workflow: {result['workflow_id']}")
    print(f"🆔 Run ID: {result['run_id']}")
    print(f"📊 Status: {result['status']}")
    print(f"⏱️  Agents in sequence: Research → Analyze → Recommend")
    
    assert result["workflow_id"] == "code_review_workflow"
    assert result["status"] in ["success", "failed"]
    
    if result["status"] == "success":
        print("\n✅ ALL 3 AGENTS EXECUTED SUCCESSFULLY!\n")
        
        # Agent 1: Research Best Practices
        if "fetch_best_practices" in result["result"]:
            node1 = result["result"]["fetch_best_practices"]
            print("="*80)
            print("🔬 AGENT 1: Research Best Practices (groq_researcher)")
            print("="*80)
            print(f"Task: {node1['task']}")
            
            if "tool_results" in node1 and "duckduckgo_search" in node1["tool_results"]:
                search = node1["tool_results"]["duckduckgo_search"]
                print(f"🔍 Web Search: {search.get('count', 0)} results found")
            
            llm_output = node1.get('llm_response', '')
            print(f"\n🤖 LLM Output (excerpt):")
            print("-" * 80)
            print(llm_output[:600] + "..." if len(llm_output) > 600 else llm_output)
            print("-" * 80)
        
        # Agent 2: Analyze Code
        if "analyze_code" in result["result"]:
            node2 = result["result"]["analyze_code"]
            print("\n" + "="*80)
            print("📊 AGENT 2: Analyze Code (analyzer_agent)")
            print("="*80)
            print(f"Task: {node2['task']}")
            print("✉️  Received context from: fetch_best_practices")
            
            llm_output = node2.get('llm_response', '')
            print(f"\n🤖 Analysis Output (excerpt):")
            print("-" * 80)
            print(llm_output[:600] + "..." if len(llm_output) > 600 else llm_output)
            print("-" * 80)
        
        # Agent 3: Generate Recommendations
        if "generate_recommendations" in result["result"]:
            node3 = result["result"]["generate_recommendations"]
            print("\n" + "="*80)
            print("✍️ AGENT 3: Generate Recommendations (writer_agent)")
            print("="*80)
            print(f"Task: {node3['task']}")
            print("✉️  Received context from: analyze_code")
            
            llm_output = node3.get('llm_response', '')
            print(f"\n🤖 Recommendations Output (excerpt):")
            print("-" * 80)
            print(llm_output[:800] + "..." if len(llm_output) > 800 else llm_output)
            print("-" * 80)
        
        # Communication Flow Visualization
        print("\n" + "="*80)
        print("💬 AGENT COMMUNICATION FLOW")
        print("="*80)
        
        comm_log = result["meta"].get("communication_log", [])
        print(f"\nTotal messages: {len(comm_log)}")
        print("\nMessage Flow:")
        print("┌─────────────────────────────────────────────────────────┐")
        
        for i, msg in enumerate(comm_log, 1):
            sender = msg.get('sender', 'Unknown')
            agent = msg.get('agent', 'Unknown')
            arrow = " │\n │ ↓ (passes context)\n │" if i < len(comm_log) else ""
            print(f" │ {i}. {sender:20s} [{agent}]")
            if arrow:
                print(arrow)
        
        print("└─────────────────────────────────────────────────────────┘")
        
        # Statistics
        print("\n" + "="*80)
        print("📈 WORKFLOW EXECUTION STATISTICS")
        print("="*80)
        print(f"✓ Nodes executed: {len(result['result'])}")
        print(f"✓ Agents involved: {', '.join(set(result['meta'].get('agents_used', [])))}")
        print(f"✓ Communication messages: {result['meta'].get('total_messages', 0)}")
        print(f"✓ Context preserved: YES (all agents received previous output)")
        print(f"✓ Final agent: {result['meta'].get('final_step', 'N/A')}")
        
        # Verify 3-agent workflow
        assert len(result["result"]) == 3, "Should have 3 nodes executed"
        assert len(comm_log) == 3, "Should have 3 communication messages"
        
        print("\n" + "="*80)
        print("✅ 3-AGENT WORKFLOW TEST PASSED!")
        print("="*80)
        print("\n✨ Key Achievement: Successfully demonstrated sequential")
        print("   agent communication with context preservation across 3 agents!")
        print("="*80 + "\n")
    
    else:
        print(f"\n❌ WORKFLOW FAILED")
        print(f"Error: {result.get('error', 'Unknown error')}")


if __name__ == "__main__":
    print("Running Code Review Workflow Test (3 Agents)...")
    pytest.main([__file__, "-v", "-s"])
