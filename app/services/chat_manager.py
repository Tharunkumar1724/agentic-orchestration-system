"""Chat session management for continuous conversations with workflows."""
import uuid
import yaml
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional, List
from app.models import ChatSession, ChatMessage


# Chat sessions are stored in data/chat_sessions
CHAT_BASE = Path(__file__).resolve().parent.parent.parent / "data" / "chat_sessions"
CHAT_BASE.mkdir(parents=True, exist_ok=True)


def _session_path(session_id: str) -> Path:
    """Get path for a session file."""
    return CHAT_BASE / f"{session_id}.yaml"


def create_session(workflow_id: str, initial_message: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None, solution_id: Optional[str] = None) -> ChatSession:
    """Create a new chat session."""
    session_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    
    messages = []
    if initial_message:
        messages.append(ChatMessage(
            role="user",
            content=initial_message,
            timestamp=now,
            metadata={}
        ))
    
    session = ChatSession(
        session_id=session_id,
        workflow_id=workflow_id,
        solution_id=solution_id,
        created_at=now,
        updated_at=now,
        messages=messages,
        state={},
        conversation_memory={},
        workflow_history=[workflow_id] if workflow_id else [],
        metadata=metadata or {}
    )
    
    # Save session
    with _session_path(session_id).open("w", encoding="utf-8") as f:
        yaml.safe_dump(session.model_dump(), f, default_flow_style=False, sort_keys=False)
    
    return session


def get_session(session_id: str) -> Optional[ChatSession]:
    """Get a chat session by ID."""
    path = _session_path(session_id)
    if not path.exists():
        return None
    
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        return ChatSession(**data)


def update_session(session: ChatSession) -> ChatSession:
    """Update a chat session."""
    session.updated_at = datetime.now(timezone.utc).isoformat()
    
    with _session_path(session.session_id).open("w", encoding="utf-8") as f:
        yaml.safe_dump(session.model_dump(), f, default_flow_style=False, sort_keys=False)
    
    return session


def add_message(session_id: str, role: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> Optional[ChatSession]:
    """Add a message to a chat session."""
    session = get_session(session_id)
    if not session:
        return None
    
    message = ChatMessage(
        role=role,
        content=content,
        timestamp=datetime.now(timezone.utc).isoformat(),
        metadata=metadata or {}
    )
    
    session.messages.append(message)
    return update_session(session)


def list_sessions(workflow_id: Optional[str] = None) -> List[ChatSession]:
    """List all chat sessions, optionally filtered by workflow_id."""
    sessions = []
    
    for path in CHAT_BASE.glob("*.yaml"):
        try:
            with path.open("r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                session = ChatSession(**data)
                if workflow_id is None or session.workflow_id == workflow_id:
                    sessions.append(session)
        except Exception:
            continue
    
    return sorted(sessions, key=lambda s: s.updated_at, reverse=True)


def delete_session(session_id: str) -> bool:
    """Delete a chat session."""
    path = _session_path(session_id)
    if path.exists():
        path.unlink()
        return True
    return False
