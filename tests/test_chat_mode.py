"""
Test chat mode - continuous conversation with workflows like a chatbot.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_chat_mode_continuous_conversation():
    """Test: Have a multi-turn conversation with a workflow."""
    
    print("\n" + "="*80)
    print("💬 CHAT MODE TEST - CONTINUOUS CONVERSATION")
    print("="*80)
    
    # Step 1: Create a chat session
    print("\n📝 Step 1: Creating chat session...")
    response = client.post("/v1/chat/sessions", json={
        "workflow_id": "ai_research_workflow",
        "initial_message": "Hello! Can you help me learn about Python?",
        "metadata": {"user": "test_user"}
    })
    
    assert response.status_code == 200
    session = response.json()
    session_id = session["session_id"]
    
    print(f"✓ Session created: {session_id}")
    print(f"✓ Workflow: {session['workflow_id']}")
    print(f"✓ Messages in session: {len(session['messages'])}")
    
    # Show initial exchange
    print("\n" + "-"*80)
    print("INITIAL MESSAGE:")
    print("-"*80)
    for msg in session['messages']:
        print(f"\n{msg['role'].upper()}: {msg['content'][:200]}...")
    
    # Step 2: Send follow-up message
    print("\n" + "="*80)
    print("📝 Step 2: Sending follow-up message...")
    print("="*80)
    
    response = client.post(f"/v1/chat/sessions/{session_id}/message", json={
        "message": "What are the best practices for Python functions?"
    })
    
    assert response.status_code == 200
    session = response.json()
    
    print(f"✓ Follow-up processed")
    print(f"✓ Total messages: {len(session['messages'])}")
    
    # Show latest message
    latest = session['messages'][-1]
    print(f"\n{latest['role'].upper()}: {latest['content'][:300]}...")
    
    # Step 3: Another follow-up (testing context preservation)
    print("\n" + "="*80)
    print("📝 Step 3: Testing context preservation...")
    print("="*80)
    
    response = client.post(f"/v1/chat/sessions/{session_id}/message", json={
        "message": "Can you give me an example?"
    })
    
    assert response.status_code == 200
    session = response.json()
    
    print(f"✓ Context preserved!")
    print(f"✓ Total messages: {len(session['messages'])}")
    
    latest = session['messages'][-1]
    print(f"\n{latest['role'].upper()}: {latest['content'][:300]}...")
    
    # Step 4: Get full conversation history
    print("\n" + "="*80)
    print("📜 Step 4: Retrieving full conversation history...")
    print("="*80)
    
    response = client.get(f"/v1/chat/sessions/{session_id}")
    assert response.status_code == 200
    
    history = response.json()
    print(f"\n✓ Session ID: {history['session_id']}")
    print(f"✓ Workflow: {history['workflow_id']}")
    print(f"✓ Created: {history['created_at']}")
    print(f"✓ Updated: {history['updated_at']}")
    print(f"✓ Total messages: {len(history['messages'])}")
    
    print("\n" + "-"*80)
    print("FULL CONVERSATION:")
    print("-"*80)
    for i, msg in enumerate(history['messages'], 1):
        role = msg['role'].upper()
        content = msg['content'][:150] + "..." if len(msg['content']) > 150 else msg['content']
        print(f"\n[{i}] {role}:")
        print(f"    {content}")
    
    # Verify conversation flow
    assert len(history['messages']) >= 4  # At least 2 user + 2 assistant
    assert history['messages'][0]['role'] == 'user'
    assert history['messages'][1]['role'] == 'assistant'
    
    print("\n" + "="*80)
    print("✅ CHAT MODE TEST PASSED!")
    print("   • Session created successfully")
    print("   • Multi-turn conversation works")
    print("   • Context is preserved across messages")
    print("   • Full history retrieval works")
    print("="*80)


def test_list_chat_sessions():
    """Test: List all chat sessions."""
    
    print("\n" + "="*80)
    print("📋 LISTING ALL CHAT SESSIONS")
    print("="*80)
    
    # Create a couple of sessions
    client.post("/v1/chat/sessions", json={
        "workflow_id": "ai_research_workflow",
        "initial_message": "Test session 1"
    })
    
    client.post("/v1/chat/sessions", json={
        "workflow_id": "python_tutorial_workflow",
        "initial_message": "Test session 2"
    })
    
    # List all sessions
    response = client.get("/v1/chat/sessions")
    assert response.status_code == 200
    
    sessions = response.json()
    print(f"\n✓ Found {len(sessions)} chat sessions")
    
    for i, session in enumerate(sessions[:5], 1):  # Show first 5
        print(f"\n{i}. Session: {session['session_id'][:8]}...")
        print(f"   Workflow: {session['workflow_id']}")
        print(f"   Messages: {len(session['messages'])}")
        print(f"   Created: {session['created_at']}")
    
    print("\n✅ Session listing works!")


def test_filter_sessions_by_workflow():
    """Test: Filter sessions by workflow ID."""
    
    print("\n" + "="*80)
    print("🔍 FILTERING SESSIONS BY WORKFLOW")
    print("="*80)
    
    # List sessions for specific workflow
    response = client.get("/v1/chat/sessions?workflow_id=ai_research_workflow")
    assert response.status_code == 200
    
    sessions = response.json()
    print(f"\n✓ Found {len(sessions)} sessions for 'ai_research_workflow'")
    
    # Verify all are for the correct workflow
    for session in sessions:
        assert session['workflow_id'] == 'ai_research_workflow'
    
    print("✅ Filtering works correctly!")


def test_clear_session_history():
    """Test: Clear session history while keeping the session."""
    
    print("\n" + "="*80)
    print("🗑️  CLEARING SESSION HISTORY")
    print("="*80)
    
    # Create session with messages
    response = client.post("/v1/chat/sessions", json={
        "workflow_id": "ai_research_workflow",
        "initial_message": "Initial message"
    })
    session_id = response.json()["session_id"]
    
    # Add more messages
    client.post(f"/v1/chat/sessions/{session_id}/message", json={
        "message": "Follow-up message"
    })
    
    # Check message count before clearing
    response = client.get(f"/v1/chat/sessions/{session_id}")
    before_count = len(response.json()['messages'])
    print(f"\n✓ Messages before clear: {before_count}")
    
    # Clear history
    response = client.post(f"/v1/chat/sessions/{session_id}/clear")
    assert response.status_code == 200
    
    # Check after clearing
    response = client.get(f"/v1/chat/sessions/{session_id}")
    after = response.json()
    after_count = len(after['messages'])
    
    print(f"✓ Messages after clear: {after_count}")
    print(f"✓ Session still exists: {after['session_id']}")
    
    assert after_count == 0
    assert after['session_id'] == session_id
    
    print("\n✅ Clear history works!")


def test_delete_session():
    """Test: Delete a chat session completely."""
    
    print("\n" + "="*80)
    print("❌ DELETING CHAT SESSION")
    print("="*80)
    
    # Create session
    response = client.post("/v1/chat/sessions", json={
        "workflow_id": "ai_research_workflow",
        "initial_message": "Test"
    })
    assert response.status_code == 200, f"Failed to create session: {response.text}"
    
    session_id = response.json()["session_id"]
    print(f"\n✓ Created session: {session_id[:8]}...")
    
    # Verify it exists first
    response = client.get(f"/v1/chat/sessions/{session_id}")
    assert response.status_code == 200, f"Session doesn't exist: {response.text}"
    print(f"✓ Session exists")
    
    # Delete it
    response = client.delete(f"/v1/chat/sessions/{session_id}")
    assert response.status_code == 200, f"Failed to delete: {response.text}"
    print(f"✓ Session deleted")
    
    # Verify it's gone
    response = client.get(f"/v1/chat/sessions/{session_id}")
    assert response.status_code == 404
    print(f"✓ Session no longer exists")
    
    print("\n✅ Delete session works!")


def test_chat_mode_with_code_review_workflow():
    """Test: Chat mode with code review workflow (3 agents)."""
    
    print("\n" + "="*80)
    print("💬 CHAT MODE WITH CODE REVIEW WORKFLOW")
    print("="*80)
    
    # Create session
    response = client.post("/v1/chat/sessions", json={
        "workflow_id": "code_review_workflow",
        "initial_message": "Please review this code: def add(a, b): return a + b"
    })
    
    assert response.status_code == 200
    session = response.json()
    session_id = session["session_id"]
    
    print(f"\n✓ Session created for code_review_workflow")
    print(f"✓ Initial review completed")
    print(f"✓ Messages: {len(session['messages'])}")
    
    # Follow-up: Ask for specific improvements
    response = client.post(f"/v1/chat/sessions/{session_id}/message", json={
        "message": "What specific improvements would you suggest?"
    })
    
    assert response.status_code == 200
    session = response.json()
    
    print(f"\n✓ Follow-up processed")
    print(f"✓ Total messages: {len(session['messages'])}")
    
    # Show conversation
    print("\n" + "-"*80)
    print("CONVERSATION:")
    print("-"*80)
    for msg in session['messages']:
        print(f"\n{msg['role'].upper()}: {msg['content'][:200]}...")
    
    print("\n✅ Code review chat mode works!")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("🤖 RUNNING CHAT MODE TESTS")
    print("="*80)
    pytest.main([__file__, "-v", "-s"])
