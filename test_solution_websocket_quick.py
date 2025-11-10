"""
Quick test to verify WebSocket connection for solution execution
"""
import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://localhost:8000/solutions/ws/test_solution_001"
    
    print(f"🔌 Connecting to {uri}...")
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connected to WebSocket!")
            
            # Send execute command
            print("📤 Sending execute command...")
            await websocket.send(json.dumps({"action": "execute"}))
            
            # Receive messages
            print("📥 Waiting for messages...\n")
            
            message_count = 0
            async for message in websocket:
                data = json.loads(message)
                message_count += 1
                
                msg_type = data.get("type", "unknown")
                print(f"[{message_count}] Type: {msg_type}")
                
                if msg_type == "execution_started":
                    print(f"    ▶️ Execution started for solution: {data.get('solution_id')}")
                    print(f"    Total workflows: {data.get('total_workflows')}")
                
                elif msg_type == "workflow_started":
                    print(f"    🔄 Workflow {data.get('position')}/{data.get('total')}: {data.get('workflow_name')}")
                
                elif msg_type == "handoff_prepared":
                    print(f"    🤝 Handoff: {data.get('from_workflow')} → {data.get('to_workflow')}")
                
                elif msg_type == "workflow_completed":
                    print(f"    ✅ Workflow completed: {data.get('workflow_name')}")
                    kag = data.get('kag_analysis', {})
                    if kag:
                        print(f"        Summary: {kag.get('summary', '')[:80]}...")
                
                elif msg_type == "execution_completed":
                    print(f"    🎉 Execution complete!")
                    summary = data.get('summary', {})
                    print(f"        Total workflows: {summary.get('total_workflows', 0)}")
                    print(f"        Overall context available: {bool(summary.get('overall_context'))}")
                    break
                
                elif msg_type == "error":
                    print(f"    ❌ Error: {data.get('message')}")
                    break
                
                print()
            
            print(f"\n📊 Received {message_count} messages total")
            print("✅ WebSocket test completed successfully!")
            
    except Exception as e:
        print(f"❌ WebSocket error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("SOLUTION WEBSOCKET TEST")
    print("=" * 60)
    print()
    
    success = asyncio.run(test_websocket())
    exit(0 if success else 1)
