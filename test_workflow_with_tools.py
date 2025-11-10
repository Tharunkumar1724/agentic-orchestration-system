"""
Test Workflow Execution with Tools
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_workflow_with_tools():
    """Test workflow execution that uses tools"""
    
    print("="*70)
    print("WORKFLOW EXECUTION WITH TOOLS - TEST")
    print("="*70)
    print()
    
    # Test the 'retest' workflow which uses both tools
    workflow_id = "retest"
    
    print(f"Testing Workflow: {workflow_id}")
    print("-" * 70)
    
    # Execute workflow
    response = requests.post(
        f"{BASE_URL}/workflows/{workflow_id}/run",
        json={"query": "Analyze AAPL stock performance"}
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        
        print(f"\n✅ Workflow Executed Successfully")
        print(f"\nWorkflow ID: {data.get('workflow_id')}")
        print(f"Status: {data.get('status')}")
        
        # Check if we have results
        results = data.get('results') or data.get('result', {})
        if results:
            print(f"\n📊 Results:")
            for key, value in results.items():
                print(f"\nNode: {key}")
                if isinstance(value, dict):
                    # Check for tool execution results
                    if value.get('tools_executed'):
                        print(f"  Tools Executed: {len(value['tools_executed'])}")
                        for tool in value['tools_executed']:
                            print(f"    - {tool.get('tool', 'unknown')}: {tool.get('summary', 'N/A')[:100]}")
                    
                    if value.get('response'):
                        print(f"  Response: {str(value['response'])[:200]}...")
                else:
                    print(f"  {str(value)[:200]}...")
        
        # Check metrics
        if data.get('metrics'):
            metrics = data['metrics']
            print(f"\n📈 Metrics:")
            print(f"  Token Usage: {metrics.get('token_usage_count', 0)}")
            print(f"  Tool Invocations: {metrics.get('tool_invocation_count', 0)}")
            print(f"  Tool Success Rate: {metrics.get('tool_success_rate', 0)}%")
            print(f"  Execution Time: {metrics.get('latency_ms', 0):.0f}ms")
        
        # Check for communication log
        meta = data.get('meta', {})
        if meta.get('communication_log'):
            print(f"\n💬 Communication Log: {len(meta['communication_log'])} messages")
    
    else:
        print(f"\n❌ Workflow Execution Failed")
        try:
            error_data = response.json()
            print(f"Error: {error_data.get('detail', 'Unknown error')}")
        except:
            print(f"Error: {response.text[:200]}")
    
    print("\n" + "="*70)
    print("TEST COMPLETE")
    print("="*70)

if __name__ == "__main__":
    test_workflow_with_tools()
