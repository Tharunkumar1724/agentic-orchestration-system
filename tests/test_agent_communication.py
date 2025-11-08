import asyncio
import uuid
from app.storage import save, load, delete
from app.services.orchestrator import run_workflow


def test_agent_to_agent_communication():
    """Test workflow with multiple agents communicating with each other."""
    # Clean up
    for item_id in ["t_search", "a_researcher", "a_writer", "w_communication"]:
        try:
            for kind in ["tools", "agents", "workflows"]:
                delete(kind, item_id)
        except Exception:
            pass

    # Create a websearch tool
    tool = {"id": "t_search", "name": "web-search", "type": "websearch", "config": {}}
    save("tools", "t_search", tool)

    # Create researcher agent
    agent1 = {
        "id": "a_researcher",
        "name": "researcher",
        "type": "zero_shot",
        "llm_config": {},
        "tools": ["t_search"]
    }
    save("agents", "a_researcher", agent1)

    # Create writer agent (receives context from researcher)
    agent2 = {
        "id": "a_writer",
        "name": "writer",
        "type": "react",
        "llm_config": {},
        "tools": []
    }
    save("agents", "a_writer", agent2)

    # Create workflow: researcher -> writer (sequential communication)
    workflow = {
        "id": "w_communication",
        "name": "agent-communication-test",
        "entrypoint": {
            "id": "root",
            "type": "sequence",
            "children": [
                {
                    "id": "research",
                    "type": "agent",
                    "ref": "a_researcher",
                    "inputs": {"prompt": "Research the benefits of LangGraph for agentic workflows"}
                },
                {
                    "id": "write",
                    "type": "agent",
                    "ref": "a_writer",
                    "inputs": {"prompt": "Write a summary based on the research findings"}
                }
            ]
        }
    }
    save("workflows", "w_communication", workflow)

    # Run workflow
    res = asyncio.get_event_loop().run_until_complete(
        run_workflow(workflow, run_id=str(uuid.uuid4()))
    )

    # Assertions
    assert res["status"] == "success", f"Workflow failed: {res.get('error')}"
    assert "result" in res
    assert "meta" in res
    
    # Check communication log exists
    assert "communication_log" in res["meta"]
    assert len(res["meta"]["communication_log"]) > 0, "No communication logged"
    
    # Check both agents were involved
    assert "agents_used" in res["meta"]
    assert "a_researcher" in res["meta"]["agents_used"]
    assert "a_writer" in res["meta"]["agents_used"]
    
    # Check results contain agent outputs
    assert "research" in res["result"]
    assert "write" in res["result"]
    assert "llm" in res["result"]["research"]
    assert "llm" in res["result"]["write"]
    
    # Check context preservation
    assert "context_size" in res["result"]["research"]
    assert "context_size" in res["result"]["write"]
    
    print(f"✓ Agent communication test passed!")
    print(f"  - Communication log entries: {len(res['meta']['communication_log'])}")
    print(f"  - Agents used: {res['meta']['agents_used']}")
    print(f"  - Researcher context size: {res['result']['research']['context_size']}")
    print(f"  - Writer context size: {res['result']['write']['context_size']}")


if __name__ == "__main__":
    test_agent_to_agent_communication()
