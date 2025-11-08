"""
Interactive Chat Mode Demo - Talk to your workflow like a chatbot!

Usage:
    python chat_demo.py
"""
import requests
import json
from datetime import datetime


BASE_URL = "http://localhost:8000/v1"


def print_message(role: str, content: str):
    """Pretty print a chat message."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    if role == "user":
        print(f"\n[{timestamp}] 👤 YOU:")
        print(f"  {content}")
    else:
        print(f"\n[{timestamp}] 🤖 ASSISTANT:")
        print(f"  {content}")


def create_session(workflow_id: str, initial_message: str = None):
    """Create a new chat session."""
    response = requests.post(f"{BASE_URL}/chat/sessions", json={
        "workflow_id": workflow_id,
        "initial_message": initial_message
    })
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error creating session: {response.text}")
        return None


def send_message(session_id: str, message: str):
    """Send a message to the chat session."""
    response = requests.post(f"{BASE_URL}/chat/sessions/{session_id}/message", json={
        "message": message
    })
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error sending message: {response.text}")
        return None


def list_workflows():
    """List available workflows."""
    response = requests.get(f"{BASE_URL}/workflows/")
    if response.status_code == 200:
        return response.json()
    return []


def main():
    print("="*80)
    print("🤖 WORKFLOW CHAT MODE - Interactive Demo")
    print("="*80)
    print("\nThis lets you have a continuous conversation with any workflow!")
    print("Context is preserved across all your messages.\n")
    
    # List available workflows
    print("\n📋 Available Workflows:")
    print("-"*80)
    workflows = list_workflows()
    
    if not workflows:
        print("❌ No workflows found! Please start the server first.")
        return
    
    for i, wf in enumerate(workflows, 1):
        print(f"{i}. {wf['id']}")
        print(f"   Name: {wf['name']}")
        print(f"   Type: {wf['type']}")
        print(f"   Nodes: {len(wf.get('nodes', []))}")
        print()
    
    # Select workflow
    try:
        choice = int(input("Select workflow (enter number): ")) - 1
        workflow_id = workflows[choice]['id']
        print(f"\n✓ Selected: {workflows[choice]['name']}")
    except (ValueError, IndexError):
        print("Invalid choice!")
        return
    
    # Create session
    print("\n" + "="*80)
    print("🚀 Starting Chat Session")
    print("="*80)
    
    initial = input("\n💬 Your first message (or press Enter to skip): ").strip()
    
    session = create_session(workflow_id, initial or None)
    
    if not session:
        print("Failed to create session!")
        return
    
    session_id = session['session_id']
    print(f"\n✓ Session created: {session_id[:8]}...")
    
    # Show initial exchange if there was one
    if initial:
        for msg in session['messages']:
            print_message(msg['role'], msg['content'])
    
    # Interactive chat loop
    print("\n" + "="*80)
    print("💬 Chat Mode Active - Type 'quit' to exit, 'history' to see all messages")
    print("="*80)
    
    while True:
        try:
            user_input = input("\n👤 YOU: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if user_input.lower() == 'history':
                # Get full history
                response = requests.get(f"{BASE_URL}/chat/sessions/{session_id}")
                if response.status_code == 200:
                    history = response.json()
                    print("\n" + "="*80)
                    print(f"📜 CONVERSATION HISTORY ({len(history['messages'])} messages)")
                    print("="*80)
                    for msg in history['messages']:
                        print_message(msg['role'], msg['content'][:300] + "..." if len(msg['content']) > 300 else msg['content'])
                continue
            
            # Send message
            session = send_message(session_id, user_input)
            
            if not session:
                print("Failed to send message!")
                continue
            
            # Show assistant response
            latest = session['messages'][-1]
            print_message(latest['role'], latest['content'])
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
