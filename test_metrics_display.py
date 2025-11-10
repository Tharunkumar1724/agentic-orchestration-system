"""Quick test to check metrics in workflow response."""
import httpx
import json
import asyncio

async def test_workflow():
    async with httpx.AsyncClient(follow_redirects=True, timeout=60.0) as client:
        print("Testing workflow execution...")
        resp = await client.post(
            'http://localhost:8000/workflows/retest/run',
            json={'query': 'test metrics display'}
        )
        
        if resp.status_code == 200:
            result = resp.json()
            print("\n" + "="*80)
            print("WORKFLOW RESPONSE STRUCTURE:")
            print("="*80)
            print(f"Response keys: {list(result.keys())}")
            
            if 'metrics' in result:
                print("\n✅ METRICS FOUND!")
                print(json.dumps(result['metrics'], indent=2))
            else:
                print("\n❌ NO METRICS FOUND!")
                print("\nFull response:")
                print(json.dumps(result, indent=2))
        else:
            print(f"Error: {resp.status_code} - {resp.text}")

async def test_solution():
    async with httpx.AsyncClient(follow_redirects=True, timeout=120.0) as client:
        print("\n\nTesting solution execution...")
        resp = await client.post(
            'http://localhost:8000/solutions/test_sol/execute',
            params={'query': 'test solution metrics'}
        )
        
        if resp.status_code == 200:
            result = resp.json()
            print("\n" + "="*80)
            print("SOLUTION RESPONSE STRUCTURE:")
            print("="*80)
            print(f"Response keys: {list(result.keys())}")
            
            if 'metrics' in result:
                print("\n✅ METRICS FOUND!")
                print(json.dumps(result['metrics'], indent=2))
            else:
                print("\n❌ NO METRICS FOUND!")
                
            # Check workflow results
            if 'execution_results' in result:
                for i, wf_result in enumerate(result['execution_results']):
                    print(f"\n--- Workflow {i+1} result keys: {list(wf_result.keys())}")
                    if 'metrics' in wf_result:
                        print(f"✅ Workflow {i+1} has metrics")
                    else:
                        print(f"❌ Workflow {i+1} missing metrics")
        else:
            print(f"Error: {resp.status_code} - {resp.text}")

async def main():
    await test_workflow()
    await test_solution()

if __name__ == "__main__":
    asyncio.run(main())
