"""
End-to-end integration test demonstrating full CRUD + workflow execution
"""
import asyncio
import uuid
from app.storage import save, load, delete, list_all
from app.services.orchestrator import run_workflow


def test_complete_workflow_lifecycle():
    """Complete test: create tools, agents, workflow, run it, verify JSON output."""
    
    # Clean slate
    for kind in ["tools", "agents", "workflows"]:
        items = list_all(kind)
        for item in items:
            delete(kind, item["id"])
    
    # Clean runs separately (different structure)
    runs = list_all("runs")
    for run in runs:
        if "run_id" in run:
            delete("runs", run["run_id"])
    
    # 1. Create tools
    tools = [
        {"id": "search_t", "name": "search", "type": "websearch", "config": {}},
        {"id": "code_t", "name": "coder", "type": "code", "config": {"snippet": "x=42"}},
        {"id": "api_t", "name": "api", "type": "api", "config": {"url": "https://httpbin.org/get"}}
    ]
    for t in tools:
        save("tools", t["id"], t)
    
    # 2. Create agents
    agents = [
        {
            "id": "agent_react",
            "name": "React Agent",
            "type": "react",
            "llm_config": {"temp": 0.7},
            "tools": ["search_t", "code_t"],
            "use_kag": False
        },
        {
            "id": "agent_kag",
            "name": "KAG Agent",
            "type": "zero_shot",
            "llm_config": {},
            "tools": ["api_t"],
            "use_kag": True
        }
    ]
    for a in agents:
        save("agents", a["id"], a)
    
    # 3. Create workflow with seq + parallel + router
    workflow = {
        "id": "wf_complete",
        "name": "Complete Test Workflow",
        "version": "v1",
        "entrypoint": {
            "id": "root",
            "type": "sequence",
            "children": [
                {
                    "id": "seq_step1",
                    "type": "agent",
                    "ref": "agent_react",
                    "inputs": {"prompt": "Analyze data"}
                },
                {
                    "id": "parallel_step",
                    "type": "parallel",
                    "children": [
                        {"id": "par1", "type": "tool", "ref": "search_t", "inputs": {"q": "AI"}},
                        {"id": "par2", "type": "agent", "ref": "agent_kag", "inputs": {"prompt": "Summarize"}},
                        {"id": "par3", "type": "tool", "ref": "code_t", "inputs": {"code": "print(123)"}}
                    ]
                },
                {
                    "id": "router_step",
                    "type": "router",
                    "inputs": {"value": "route1"},
                    "children": [
                        {"id": "r1", "type": "tool", "ref": "api_t", "inputs": {"cond": "route1"}},
                        {"id": "r2", "type": "tool", "ref": "search_t", "inputs": {"cond": "route2", "q": "backup"}}
                    ]
                }
            ]
        }
    }
    save("workflows", workflow["id"], workflow)
    
    # 4. Run workflow
    run_id = str(uuid.uuid4())
    result = asyncio.get_event_loop().run_until_complete(run_workflow(workflow, run_id))
    
    # Save the run result (mimics what the API endpoint does)
    save("runs", run_id, result)
    
    # 5. Verify result
    assert result["status"] == "success"
    assert result["workflow_id"] == "wf_complete"
    assert result["run_id"] == run_id
    
    # Check sequential step
    assert "seq_step1" in result["result"]
    assert "llm" in result["result"]["seq_step1"]
    
    # Check parallel step
    assert "parallel_step" in result["result"]
    assert "par1" in result["result"]["parallel_step"]
    assert "par2" in result["result"]["parallel_step"]
    assert "par3" in result["result"]["parallel_step"]
    
    # Check router step
    assert "router_step" in result["result"]
    
    # 6. Verify JSON save
    saved_run = load("runs", run_id)
    assert saved_run is not None
    assert saved_run["status"] == "success"
    
    # 7. List all
    all_tools = list_all("tools")
    all_agents = list_all("agents")
    all_workflows = list_all("workflows")
    assert len(all_tools) == 3
    assert len(all_agents) == 2
    assert len(all_workflows) == 1
    
    print("✅ Complete workflow lifecycle test passed!")
    print(f"   - Created {len(all_tools)} tools")
    print(f"   - Created {len(all_agents)} agents")
    print(f"   - Created {len(all_workflows)} workflows")
    print(f"   - Executed workflow with sequential, parallel, and router nodes")
    print(f"   - Verified JSON output saved to data/runs/{run_id}.json")
