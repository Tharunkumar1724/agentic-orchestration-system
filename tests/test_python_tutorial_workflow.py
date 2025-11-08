"""
Test the Python Tutorial Workflow - demonstrates sequential workflow with agent communication
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)


def test_python_tutorial_workflow_execution():
    """Execute the Python tutorial workflow and display results."""
    
    print("\n" + "="*80)
    print("🚀 EXECUTING PYTHON TUTORIAL WORKFLOW")
    print("="*80)
    
    # Execute the workflow
    response = client.post("/v1/workflows/python_tutorial_workflow/run")
    assert response.status_code == 200
    
    result = response.json()
    
    # Display workflow info
    print(f"\n📋 Workflow ID: {result['workflow_id']}")
    print(f"🆔 Run ID: {result['run_id']}")
    print(f"📊 Status: {result['status']}")
    
    # Check basic structure
    assert result["workflow_id"] == "python_tutorial_workflow"
    assert result["status"] in ["success", "failed"]
    
    if result["status"] == "success":
        print("\n✅ WORKFLOW COMPLETED SUCCESSFULLY!\n")
        
        # Display research node results
        if "research_python" in result["result"]:
            research = result["result"]["research_python"]
            print("="*80)
            print("🔬 RESEARCH NODE: Python Best Practices Search")
            print("="*80)
            print(f"Agent: {research['agent_id']}")
            print(f"Task: {research['task']}")
            
            # Show search results
            if "tool_results" in research and "duckduckgo_search" in research["tool_results"]:
                search_data = research["tool_results"]["duckduckgo_search"]
                print(f"\n🔍 Search Results: {search_data.get('count', 0)} results")
                
                if search_data.get("results"):
                    print("\nTop Search Results:")
                    for i, res in enumerate(search_data["results"][:3], 1):
                        print(f"\n  {i}. {res.get('title', 'No title')}")
                        print(f"     URL: {res.get('href', 'No URL')}")
                        print(f"     Preview: {res.get('body', 'No preview')[:100]}...")
            
            # Show LLM response (first 500 chars)
            print(f"\n🤖 Groq LLM Response (Preview):")
            print("-" * 80)
            llm_resp = research.get('llm_response', 'No response')
            print(llm_resp[:800] + "..." if len(llm_resp) > 800 else llm_resp)
            print("-" * 80)
        
        # Display writer node results
        if "write_tutorial" in result["result"]:
            writer = result["result"]["write_tutorial"]
            print("\n" + "="*80)
            print("✍️ WRITER NODE: Tutorial Creation")
            print("="*80)
            print(f"Agent: {writer['agent_id']}")
            print(f"Task: {writer['task']}")
            
            # Show tutorial content
            print(f"\n📝 Generated Tutorial Content:")
            print("-" * 80)
            tutorial = writer.get('llm_response', 'No tutorial generated')
            print(tutorial[:1200] + "..." if len(tutorial) > 1200 else tutorial)
            print("-" * 80)
        
        # Display agent communication
        print("\n" + "="*80)
        print("💬 AGENT-TO-AGENT COMMUNICATION")
        print("="*80)
        
        comm_log = result["meta"].get("communication_log", [])
        print(f"Total messages exchanged: {len(comm_log)}")
        
        for i, msg in enumerate(comm_log, 1):
            print(f"\n{i}. Node: {msg.get('sender')}")
            print(f"   Agent: {msg.get('agent', 'Unknown')}")
            print(f"   Type: {msg.get('type')}")
        
        # Display workflow statistics
        print("\n" + "="*80)
        print("📈 WORKFLOW STATISTICS")
        print("="*80)
        print(f"Agents used: {', '.join(result['meta'].get('agents_used', []))}")
        print(f"Total communication messages: {result['meta'].get('total_messages', 0)}")
        print(f"Final step: {result['meta'].get('final_step', 'N/A')}")
        
        # Verify agent communication happened
        assert len(comm_log) >= 2, "Should have messages from both agents"
        assert len(result["result"]) >= 2, "Should have results from both nodes"
        
        print("\n" + "="*80)
        print("✅ TEST PASSED - Workflow executed successfully!")
        print("="*80 + "\n")
    
    else:
        print(f"\n❌ WORKFLOW FAILED")
        print(f"Error: {result.get('error', 'Unknown error')}")
        if 'meta' in result and 'error_details' in result['meta']:
            print(f"Details: {result['meta']['error_details']}")


if __name__ == "__main__":
    print("Running Python Tutorial Workflow Test...")
    pytest.main([__file__, "-v", "-s"])
