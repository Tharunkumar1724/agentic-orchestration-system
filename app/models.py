from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
import enum


class ToolType(str, enum.Enum):
    api = "api"
    code = "code"
    websearch = "websearch"


class ToolDef(BaseModel):
    id: str
    name: str
    type: ToolType
    config: Dict[str, Any] = Field(default_factory=dict)
    version: Optional[str] = "v1"


class AgentType(str, enum.Enum):
    zero_shot = "zero_shot"
    react = "react"
    custom = "custom"


class AgentDef(BaseModel):
    id: str
    name: str
    type: AgentType
    llm_config: Dict[str, Any] = Field(default_factory=dict)
    tools: List[str] = Field(default_factory=list)
    use_kag: bool = False
    communication: Dict[str, Any] = Field(default_factory=dict)  # Communication settings
    version: Optional[str] = "v1"


class WorkflowNode(BaseModel):
    id: str
    agent_ref: Optional[str] = None  # Reference to agent
    task: Optional[str] = None  # Task description
    tools: List[str] = Field(default_factory=list)  # Tool IDs attached to this agent node
    dependencies: List[str] = Field(default_factory=list)  # Node IDs this node depends on
    receives_from: List[str] = Field(default_factory=list)  # Agent IDs to receive messages from (legacy)
    sends_to: List[str] = Field(default_factory=list)  # Agent IDs to send messages to (legacy)


class WorkflowDef(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    type: str = "sequence"  # 'sequence', 'parallel', or 'router'
    nodes: List[WorkflowNode] = Field(default_factory=list)
    version: Optional[str] = "v1"


class SolutionDef(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    workflows: List[str] = Field(default_factory=list)  # Workflow IDs
    workflow_memory: Dict[str, Any] = Field(default_factory=dict)  # Shared memory across workflows
    communication_config: Dict[str, Any] = Field(default_factory=dict)  # Inter-workflow communication settings
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    version: Optional[str] = "v1"


class SolutionCreate(BaseModel):
    """Request to create a new solution."""
    id: Optional[str] = None  # Auto-generated if not provided
    name: str
    description: Optional[str] = None
    workflows: List[str] = Field(default_factory=list)
    communication_config: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SolutionUpdate(BaseModel):
    """Request to update a solution."""
    name: Optional[str] = None
    description: Optional[str] = None
    workflows: Optional[List[str]] = None
    communication_config: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


class WorkflowCommunication(BaseModel):
    """Inter-workflow communication event."""
    from_workflow_id: str
    to_workflow_id: str
    message_type: str  # 'data', 'command', 'query', 'response'
    payload: Dict[str, Any]
    timestamp: str
    solution_id: Optional[str] = None


class RunResult(BaseModel):
    workflow_id: str
    run_id: str
    status: str
    result: Any
    meta: Dict[str, Any] = Field(default_factory=dict)


class ChatMessage(BaseModel):
    """A single chat message in a conversation."""
    role: str  # "user" or "assistant"
    content: str
    timestamp: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ChatSession(BaseModel):
    """Chat session for continuous conversation with a workflow."""
    session_id: str
    workflow_id: str
    solution_id: Optional[str] = None  # Solution context
    created_at: str
    updated_at: str
    messages: List[ChatMessage] = Field(default_factory=list)
    state: Dict[str, Any] = Field(default_factory=dict)  # Persistent workflow state
    conversation_memory: Dict[str, Any] = Field(default_factory=dict)  # Transferable memory buffer
    workflow_history: List[str] = Field(default_factory=list)  # Track workflow switches
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ChatSessionCreate(BaseModel):
    """Request to create a new chat session."""
    workflow_id: Optional[str] = None
    solution_id: Optional[str] = None
    name: Optional[str] = None
    initial_message: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ChatMessageRequest(BaseModel):
    """Request to send a message in a chat session."""
    message: str
    stream: bool = False


class WorkflowSwitchRequest(BaseModel):
    """Request to switch to a different workflow within the same solution."""
    new_workflow_id: str
    transfer_memory: bool = True  # Whether to transfer conversation memory
    reason: Optional[str] = None  # Why switching workflows
