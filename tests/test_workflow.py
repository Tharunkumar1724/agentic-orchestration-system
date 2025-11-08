import asyncio
import uuid
from app.storage import save, load, delete
from app.services.orchestrator import run_workflow


def test_simple_sequence_workflow():
    # Clean up any previous
    try:
        delete("tools", "t1")
        delete("agents", "a1")
        delete("workflows", "w1")
    except Exception:
        pass

    # Create a simple tool
    tool = {"id": "t1", "name": "searcher", "type": "websearch", "config": {}}
    save("tools", "t1", tool)

    # Create an agent that uses the tool
    agent = {"id": "a1", "name": "q-agent", "type": "zero_shot", "llm_config": {}, "tools": ["t1"]}
    save("agents", "a1", agent)

    # Define a sequence workflow: agent -> tool
    workflow = {
        "id": "w1",
        "name": "seq1",
        "entrypoint": {
            "id": "root",
            "type": "sequence",
            "children": [
                {"id": "n1", "type": "agent", "ref": "a1", "inputs": {"prompt": "Find info about LangChain"}},
                {"id": "n2", "type": "tool", "ref": "t1", "inputs": {"q": "LangChain library"}}
            ]
        }
    }
    save("workflows", "w1", workflow)

    # Run workflow
    res = asyncio.get_event_loop().run_until_complete(run_workflow(workflow, run_id=str(uuid.uuid4())))
    assert res["status"] == "success"
    assert "result" in res
    # Basic checks
    assert "n1" in res["result"] and "llm" in res["result"]["n1"]
    assert "n2" in res["result"] and "search_results" in res["result"]["n2"]
