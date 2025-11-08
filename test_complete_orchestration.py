import sys
import os
import asyncio

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.storage import load
from app.services.orchestrator import run_workflow
import json

async def test_complete_orchestration():
    print("=" * 70)
    print("COMPLETE ORCHESTRATION TEST")
    print("=" * 70)
    
    # Test 1: Load workflow
    print("\n[1] Loading workflow...")
    workflow_def = load("workflows", "ai-research-workflow")
    if not workflow_def:
        print("❌ ERROR: Could not load workflow")
        return
    print(f"✅ Loaded: {workflow_def.get('name')}")
    print(f"   Nodes: {len(workflow_def.get('nodes', []))}")
    
    # Test 2: Load agent
    print("\n[2] Loading agent...")
    agent_def = load("agents", "researcher-agent")
    if not agent_def:
        print("❌ ERROR: Could not load agent")
        return
    print(f"✅ Loaded: {agent_def.get('name')}")
    print(f"   Type: {agent_def.get('type')}")
    print(f"   Tools: {agent_def.get('tools', [])}")
    
    # Test 3: Load tool
    print("\n[3] Loading tool...")
    tool_def = load("tools", "web-search-tool")
    if not tool_def:
        print("❌ ERROR: Could not load tool")
        return
    print(f"✅ Loaded: {tool_def.get('name')}")
    print(f"   Type: {tool_def.get('type')}")
    print(f"   Config: {tool_def.get('config', {})}")
    
    # Test 4: Execute workflow
    print("\n" + "=" * 70)
    print("EXECUTING WORKFLOW...")
    print("=" * 70 + "\n")
    
    try:
        result = await run_workflow(workflow_def)
        
        print("\n" + "=" * 70)
        print("RESULTS")
        print("=" * 70)
        print(f"\n✅ Status: {result.get('status')}")
        print(f"   Run ID: {result.get('run_id')}")
        print(f"   Workflow: {result.get('workflow_id')}")
        
        # Print execution details
        if result.get('result'):
            print(f"\n📋 Node Results:")
            for node_id, node_result in result['result'].items():
                print(f"\n  {node_id}:")
                print(f"    Agent: {node_result.get('agent_name', 'N/A')}")
                print(f"    Tools Used: {node_result.get('tools_used', [])}")
                
                if node_result.get('tool_results'):
                    print(f"    Tool Results:")
                    for tool_id, tool_res in node_result['tool_results'].items():
                        if tool_res.get('results'):
                            print(f"      {tool_id}: {len(tool_res['results'])} search results")
                        elif tool_res.get('error'):
                            print(f"      {tool_id}: ERROR - {tool_res['error']}")
                
                llm_output = node_result.get('llm_response', '')[:200]
                print(f"    LLM Output: {llm_output}...")
        
        # Save result
        result_file = 'test_complete_orchestration_result.json'
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, default=str)
        print(f"\n✅ Full results saved to: {result_file}")
        
        # Test 5: Verify workflow saved to data folder
        print("\n[5] Checking data folder...")
        data_workflows_path = os.path.join('data', 'workflows')
        if os.path.exists(data_workflows_path):
            files = os.listdir(data_workflows_path)
            print(f"✅ Data folder exists with {len(files)} workflow(s)")
            for f in files[:5]:
                print(f"   - {f}")
        else:
            print("❌ Data workflows folder not found")
        
        print("\n" + "=" * 70)
        print("TEST COMPLETE")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_complete_orchestration())
