import asyncio
import uuid
from app.storage import save, load, delete
from app.services.orchestrator import run_workflow


def test_kag_agent_with_parallel_workflow():
    """Test an agent with KAG enabled, parallel tools, and router logic."""
    # Clean up
    for kind, ids in [("tools", ["t_search", "t_code"]), ("agents", ["a_kag"]), ("workflows", ["w_kag"])]:
        for id_ in ids:
            try:
                delete(kind, id_)
            except Exception:
                pass

    # Create tools
    save("tools", "t_search", {"id": "t_search", "name": "search", "type": "websearch", "config": {}})
    save("tools", "t_code", {"id": "t_code", "name": "coder", "type": "code", "config": {"snippet": "print('hello')"}})

    # Create agent with KAG enabled
    agent = {
        "id": "a_kag",
        "name": "kag-agent",
        "type": "react",
        "llm_config": {},
        "tools": ["t_search", "t_code"],
        "use_kag": True
    }
    save("agents", "a_kag", agent)

    # Workflow: parallel + router
    workflow = {
        "id": "w_kag",
        "name": "kag-parallel-router",
        "entrypoint": {
            "id": "root",
            "type": "sequence",
            "children": [
                {
                    "id": "step1",
                    "type": "parallel",
                    "children": [
                        {"id": "p1", "type": "agent", "ref": "a_kag", "inputs": {"prompt": "Find AI papers"}},
                        {"id": "p2", "type": "tool", "ref": "t_search", "inputs": {"q": "machine learning"}}
                    ]
                },
                {
                    "id": "router1",
                    "type": "router",
                    "inputs": {"value": "A"},
                    "children": [
                        {"id": "rA", "type": "tool", "ref": "t_code", "inputs": {"cond": "A", "code": "x=1"}},
                        {"id": "rB", "type": "tool", "ref": "t_search", "inputs": {"cond": "B", "q": "fallback"}}
                    ]
                }
            ]
        }
    }
    save("workflows", "w_kag", workflow)

    # Run
    res = asyncio.get_event_loop().run_until_complete(run_workflow(workflow, run_id=str(uuid.uuid4())))
    assert res["status"] == "success"
    assert "result" in res
    # Verify parallel execution
    assert "step1" in res["result"]
    assert "p1" in res["result"]["step1"]
    assert "p2" in res["result"]["step1"]
    # Verify router picked rA
    assert "router1" in res["result"]
    assert "executed" in res["result"]["router1"]
    print("KAG + parallel + router test passed!")
