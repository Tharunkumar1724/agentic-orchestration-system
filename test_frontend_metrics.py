"""Test metrics display in frontend-compatible format."""
import httpx
import json
import asyncio

async def create_test_solution():
    """Create a test solution with workflows."""
    async with httpx.AsyncClient(follow_redirects=True, timeout=60.0) as client:
        # Get available workflows
        wf_resp = await client.get('http://localhost:8000/workflows')
        workflows = wf_resp.json()
        
        if not workflows:
            print("No workflows found!")
            return None
        
        # Create solution
        solution_data = {
            "id": "metrics_test_solution",
            "name": "Metrics Test Solution",
            "description": "Solution for testing metrics display",
            "workflows": [workflows[0]["id"]]
        }
        
        resp = await client.post('http://localhost:8000/solutions', json=solution_data)
        if resp.status_code == 200:
            print(f"✅ Created solution: {solution_data['id']}")
            return solution_data['id']
        else:
            print(f"❌ Failed to create solution: {resp.text}")
            return None

async def test_solution_metrics(solution_id):
    """Test solution execution metrics."""
    async with httpx.AsyncClient(follow_redirects=True, timeout=120.0) as client:
        print(f"\n🚀 Executing solution: {solution_id}")
        
        resp = await client.post(
            f'http://localhost:8000/solutions/{solution_id}/execute',
            params={'query': 'test solution metrics display'}
        )
        
        if resp.status_code == 200:
            result = resp.json()
            print("\n" + "="*80)
            print("SOLUTION RESPONSE STRUCTURE:")
            print("="*80)
            print(f"Response keys: {list(result.keys())}")
            
            if 'metrics' in result:
                print("\n✅ SOLUTION AGGREGATED METRICS FOUND!")
                metrics = result['metrics']
                print(f"\nLatency: {metrics.get('latency_ms')} ms")
                print(f"Token Usage: {metrics.get('token_usage_count')}")
                print(f"Accuracy: {metrics.get('accuracy')}%")
                print(f"Response Quality: {metrics.get('response_quality')}%")
                print(f"Task Completion: {metrics.get('task_completion_rate')}%")
            else:
                print("\n❌ NO AGGREGATED METRICS FOUND IN SOLUTION RESPONSE!")
            
            # Check individual workflow metrics
            if 'execution_results' in result:
                print(f"\n📊 Checking {len(result['execution_results'])} workflow results...")
                for i, wf_result in enumerate(result['execution_results']):
                    wf_name = wf_result.get('workflow_name', 'Unknown')
                    print(f"\n  Workflow {i+1}: {wf_name}")
                    print(f"  Keys: {list(wf_result.keys())}")
                    
                    if 'metrics' in wf_result:
                        print(f"  ✅ Has individual metrics")
                        wf_metrics = wf_result['metrics']
                        print(f"     - Latency: {wf_metrics.get('latency_ms')} ms")
                        print(f"     - Tokens: {wf_metrics.get('token_usage_count')}")
                    else:
                        print(f"  ❌ Missing individual metrics")
            
            return True
        else:
            print(f"❌ Solution execution failed: {resp.status_code} - {resp.text}")
            return False

async def main():
    print("="*80)
    print("METRICS DISPLAY TEST FOR FRONTEND")
    print("="*80)
    
    # Create test solution
    solution_id = await create_test_solution()
    
    if solution_id:
        # Test solution execution
        await test_solution_metrics(solution_id)
    else:
        print("Skipping solution test - no solution created")

if __name__ == "__main__":
    asyncio.run(main())
