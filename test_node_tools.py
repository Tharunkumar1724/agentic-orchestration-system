"""Test if workflow nodes are using their tools correctly."""
import asyncio
from app.storage import load
from app.services.orchestrator import run_workflow

async def test_node_tools():
    # Load the test workflow
    workflow = load("workflows", "test_workflow_tools")
    print(f"Workflow: {workflow['name']}")
    print(f"Nodes: {len(workflow['nodes'])}")
    
    for node in workflow['nodes']:
        print(f"\nNode {node['id']}:")
        print(f"  Agent: {node['agent_ref']}")
        print(f"  Tools: {node.get('tools', [])}")
    
    # Run the workflow
    print("\n" + "="*50)
    print("Running workflow...")
    print("="*50 + "\n")
    
    result = await run_workflow(workflow, "test_run_123")
    
    print("\n" + "="*50)
    print("Results:")
    print("="*50)
    
    for node_id, node_result in result.get("result", {}).items():
        print(f"\nNode {node_id}:")
        print(f"  Tools used: {node_result.get('tools_used', [])}")
        print(f"  Tool results: {list(node_result.get('tool_results', {}).keys())}")

if __name__ == "__main__":
    asyncio.run(test_node_tools())
