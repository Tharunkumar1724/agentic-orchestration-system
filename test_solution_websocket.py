"""
Test WebSocket connection for solution execution
"""
import asyncio
import websockets
import json

async def test_solution_websocket():
    solution_id = "sol"  # The actual solution ID
    uri = f"ws://localhost:8000/solutions/ws/{solution_id}"
    
    print(f"Connecting to: {uri}")
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connected!")
            
            # Send execute command
            await websocket.send(json.dumps({"action": "execute"}))
            print("📤 Sent execute command")
            
            # Receive messages
            while True:
                try:
                    message = await asyncio.wait_for(websocket.recv(), timeout=30.0)
                    data = json.loads(message)
                    
                    msg_type = data.get("type", "unknown")
                    print(f"\n📨 Received: {msg_type}")
                    
                    if msg_type == "execution_started":
                        print(f"   Starting {data.get('total_workflows')} workflows...")
                    
                    elif msg_type == "workflow_started":
                        print(f"   ▶️  {data.get('workflow_name')} ({data.get('position')}/{data.get('total')})")
                    
                    elif msg_type == "handoff_prepared":
                        print(f"   🔄 Handoff prepared")
                        print(f"      Data: {json.dumps(data.get('handoff_data', {}), indent=2)[:200]}...")
                    
                    elif msg_type == "workflow_completed":
                        print(f"   ✅ {data.get('workflow_name')} completed")
                        kag = data.get('kag_analysis', {})
                        print(f"      Summary: {kag.get('summary', 'N/A')[:100]}...")
                        print(f"      Facts: {len(kag.get('facts', []))} extracted")
                    
                    elif msg_type == "execution_completed":
                        print(f"\n✅ Solution execution complete!")
                        summary = data.get('summary', {})
                        print(f"   Total workflows: {summary.get('total_workflows', 0)}")
                        print(f"   Total facts: {len(summary.get('combined_facts', []))}")
                        break
                    
                    elif msg_type == "error":
                        print(f"   ❌ Error: {data.get('message')}")
                        break
                        
                except asyncio.TimeoutError:
                    print("⏰ Timeout waiting for message")
                    break
                    
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Testing Solution WebSocket Execution\n")
    asyncio.run(test_solution_websocket())
