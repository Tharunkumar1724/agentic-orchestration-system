import sys
import os
import asyncio
import httpx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_api_workflow_save():
    print("Testing workflow save via API...\n")
    
    workflow_data = {
        "id": "test-api-workflow",
        "name": "Test API Workflow",
        "description": "Testing workflow save to data folder",
        "type": "sequence",
        "nodes": [
            {
                "id": "node-1",
                "agent_ref": "researcher-agent",
                "task": "Test task 1",
                "dependencies": []
            },
            {
                "id": "node-2",
                "agent_ref": "researcher-agent",
                "task": "Test task 2",
                "dependencies": ["node-1"]
            }
        ]
    }
    
    async with httpx.AsyncClient() as client:
        # Create workflow
        print(f"Creating workflow: {workflow_data['name']}")
        response = await client.post("http://localhost:8000/workflows/", json=workflow_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}\n")
        
        # Check data folder
        data_path = os.path.join('data', 'workflows', 'test-api-workflow.json')
        if os.path.exists(data_path):
            print(f"✅ Workflow saved to data folder: {data_path}")
            with open(data_path, 'r') as f:
                import json
                data = json.load(f)
                print(f"   Nodes: {len(data.get('nodes', []))}")
        else:
            print(f"❌ Workflow NOT found in data folder")
        
        # Check config folder
        config_path = os.path.join('config', 'workflows', 'test-api-workflow.yaml')
        if os.path.exists(config_path):
            print(f"✅ Workflow saved to config folder: {config_path}")
        else:
            print(f"❌ Workflow NOT found in config folder")

if __name__ == "__main__":
    asyncio.run(test_api_workflow_save())
