import sys
import os
import asyncio

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.storage import load
from app.services.orchestrator import run_workflow
import json

async def test_workflow():
    print("=" * 60)
    print("Testing Sequential Workflow with Research Agent + Web Search")
    print("=" * 60)
    
    # Load workflow
    workflow_def = load("workflows", "test-sequential-workflow")
    if not workflow_def:
        print("ERROR: Could not load workflow")
        return
    
    print(f"\n[OK] Loaded workflow: {workflow_def.get('name')}")
    print(f"  Type: {workflow_def.get('type')}")
    print(f"  Nodes: {len(workflow_def.get('nodes', []))}")
    
    # Load agent
    agent_def = load("agents", "researcher-agent")
    if agent_def:
        print(f"[OK] Loaded agent: {agent_def.get('name')}")
        print(f"  Tools: {agent_def.get('tools', [])}")
    
    # Run workflow
    print("\n" + "=" * 60)
    print("EXECUTING WORKFLOW...")
    print("=" * 60 + "\n")
    
    try:
        result = await run_workflow(workflow_def)
        
        print("\n" + "=" * 60)
        print("WORKFLOW RESULTS")
        print("=" * 60)
        print(f"\nStatus: {result.get('status')}")
        print(f"Run ID: {result.get('run_id')}")
        
        if result.get('steps'):
            print(f"\n[STEPS] Execution Steps ({len(result['steps'])} total):\n")
            for i, step in enumerate(result['steps'], 1):
                print(f"Step {i}: {step.get('node_id', 'unknown')}")
                print(f"  Agent: {step.get('agent', 'unknown')}")
                print(f"  Task: {step.get('task', 'N/A')[:80]}...")
                print(f"  Status: {step.get('status', 'unknown')}")
                if step.get('tool_calls'):
                    print(f"  Tools Used: {', '.join(step['tool_calls'])}")
                if step.get('output'):
                    output = step['output'][:300]
                    print(f"  Output: {output}...")
                print()
        
        if result.get('final_output'):
            print(f"\n[OUTPUT] Final Output:\n")
            print(result['final_output'][:500])
            print("\n" + "=" * 60)
        
        # Save result
        with open('test_workflow_result.json', 'w') as f:
            json.dump(result, f, indent=2, default=str)
        print("\n[OK] Full results saved to: test_workflow_result.json")
        
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_workflow())
