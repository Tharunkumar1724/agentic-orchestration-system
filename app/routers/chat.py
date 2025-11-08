"""Chat mode router for continuous conversations with workflows."""
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.models import ChatSession, ChatSessionCreate, ChatMessageRequest, ChatMessage, WorkflowSwitchRequest
from app.services import chat_manager
from app.services.orchestrator import orchestrator
from app.services.solution_service import solution_service
from app.storage import load
from datetime import datetime

router = APIRouter()


@router.post("/sessions", response_model=ChatSession)
async def create_chat_session(request: ChatSessionCreate):
    """Create a new chat session for a workflow or solution.
    
    This allows you to have a continuous conversation with a workflow,
    maintaining context across multiple message exchanges.
    If a solution_id is provided, the session can switch between workflows
    within that solution while maintaining memory.
    """
    # Verify workflow exists if provided
    if request.workflow_id:
        workflow = load("workflows", request.workflow_id)
        if not workflow:
            raise HTTPException(status_code=404, detail=f"Workflow {request.workflow_id} not found")
    
    # Verify solution exists if provided
    solution_data = None
    if request.solution_id:
        solution_data = load("solutions", request.solution_id)
        if not solution_data:
            raise HTTPException(status_code=404, detail=f"Solution {request.solution_id} not found")
        
        # Initialize solution runtime
        solution_service.initialize_solution_runtime(request.solution_id, solution_data)
        
        # If no workflow specified, use first workflow in solution
        if not request.workflow_id and solution_data.get("workflows"):
            request.workflow_id = solution_data["workflows"][0]
    
    # Create session
    session = chat_manager.create_session(
        workflow_id=request.workflow_id or "general-chat",
        initial_message=request.initial_message,
        metadata=request.metadata or {}
    )
    
    # Add solution context
    if request.solution_id:
        session.solution_id = request.solution_id
        session.workflow_history = [request.workflow_id] if request.workflow_id else []
        session.metadata["solution_name"] = solution_data.get("name", "")
        session.metadata["available_workflows"] = solution_data.get("workflows", [])
    
    # Set session name if provided
    if request.name:
        session.metadata["name"] = request.name
    
    # If there's an initial message and a workflow, process it
    if request.initial_message and request.workflow_id:
        workflow = load("workflows", request.workflow_id)
        # Run workflow with the initial message
        result = await orchestrator.run_workflow(workflow, initial_state=session.state)
        
        # Update session state
        session.state = result.get("state", {})
        
        # Update solution memory if in solution context
        if session.solution_id:
            solution_service.update_shared_memory(
                session.solution_id,
                request.workflow_id,
                {"conversation_context": session.conversation_memory}
            )
        
        # Add assistant response
        assistant_content = str(result.get("result", {}))
        session = chat_manager.add_message(
            session.session_id,
            role="assistant",
            content=assistant_content,
            metadata={"run_id": result.get("run_id"), "status": result.get("status")}
        )
    
    return session


@router.get("/sessions", response_model=List[ChatSession])
async def list_chat_sessions(workflow_id: Optional[str] = None):
    """List all chat sessions, optionally filtered by workflow_id."""
    return chat_manager.list_sessions(workflow_id=workflow_id)


@router.get("/sessions/{session_id}", response_model=ChatSession)
async def get_chat_session(session_id: str):
    """Get a specific chat session with full message history."""
    session = chat_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
    return session


@router.post("/sessions/{session_id}/message", response_model=ChatSession)
async def send_message(session_id: str, request: ChatMessageRequest):
    """Send a message to a chat session and get the workflow's response.
    
    This maintains context from previous messages in the session.
    """
    # Get session
    session = chat_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
    
    # Get workflow
    workflow = load("workflows", session.workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail=f"Workflow {session.workflow_id} not found")
    
    # Add user message
    session = chat_manager.add_message(
        session_id,
        role="user",
        content=request.message
    )
    
    # Prepare workflow state with conversation history
    # Add user's new message to the state
    if not session.state:
        session.state = {
            "messages": [],
            "shared_data": {},
            "agents_used": [],
            "current_step": "",
            "results": {},
            "error": None
        }
    
    # Add user message to workflow state
    session.state["messages"].append({
        "sender": "user",
        "content": request.message,
        "type": "user_message"
    })
    
    # Run workflow with preserved state
    try:
        result = await orchestrator.run_workflow(workflow, initial_state=session.state)
    except Exception as e:
        error_msg = str(e)
        if "getaddrinfo failed" in error_msg or "ConnectError" in error_msg:
            last_response = "I'm currently unable to connect to the AI service. This could be due to:\n\n1. Network connectivity issues\n2. The API service being temporarily unavailable\n3. API key configuration problems\n\nYour message was: \"" + request.message + "\"\n\nPlease check the backend logs or try again in a moment."
        else:
            last_response = f"I encountered an error processing your request: {error_msg[:200]}"
        
        # Add error response
        session = chat_manager.add_message(
            session_id,
            role="assistant",
            content=last_response,
            metadata={"error": error_msg, "status": "error"}
        )
        return session
    
    # Update session state with new workflow state
    session.state = result.get("state", session.state)
    
    # Extract response from last agent result
    workflow_results = result.get("result", {})
    
    # Get the last node's response
    last_response = ""
    if workflow_results:
        last_node_key = list(workflow_results.keys())[-1] if workflow_results else None
        if last_node_key:
            last_node_result = workflow_results[last_node_key]
            last_response = last_node_result.get("llm_response", str(last_node_result))
    
    if not last_response:
        last_response = str(workflow_results)
    
    # Add assistant response
    session = chat_manager.add_message(
        session_id,
        role="assistant",
        content=last_response,
        metadata={
            "run_id": result.get("run_id"),
            "status": result.get("status"),
            "agents_used": result.get("meta", {}).get("agents_used", [])
        }
    )
    
    return session


@router.delete("/sessions/{session_id}")
async def delete_chat_session(session_id: str):
    """Delete a chat session."""
    success = chat_manager.delete_session(session_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
    return {"message": f"Session {session_id} deleted"}


@router.post("/sessions/{session_id}/clear")
async def clear_session_history(session_id: str):
    """Clear message history but keep the session."""
    session = chat_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
    
    session.messages = []
    session.state = {}
    return chat_manager.update_session(session)


@router.post("/sessions/{session_id}/switch-workflow", response_model=ChatSession)
async def switch_workflow(session_id: str, request: WorkflowSwitchRequest):
    """Switch to a different workflow within the same solution, transferring memory."""
    session = chat_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
    
    # Verify session has a solution context
    if not session.solution_id:
        raise HTTPException(
            status_code=400,
            detail="Cannot switch workflows - session is not part of a solution"
        )
    
    # Verify new workflow exists
    new_workflow = load("workflows", request.new_workflow_id)
    if not new_workflow:
        raise HTTPException(status_code=404, detail=f"Workflow {request.new_workflow_id} not found")
    
    # Verify new workflow is in the solution
    solution = load("solutions", session.solution_id)
    if request.new_workflow_id not in solution.get("workflows", []):
        raise HTTPException(
            status_code=400,
            detail=f"Workflow {request.new_workflow_id} is not in solution {session.solution_id}"
        )
    
    old_workflow_id = session.workflow_id
    
    # Transfer memory if requested
    if request.transfer_memory:
        # Prepare memory to transfer
        memory_to_transfer = {
            "conversation_context": session.conversation_memory,
            "session_data": session.state,
            "message_history": [
                {"role": msg.role, "content": msg.content, "timestamp": msg.timestamp}
                for msg in session.messages[-10:]  # Last 10 messages for context
            ]
        }
        
        # Transfer using solution service
        transferred = solution_service.transfer_memory_between_workflows(
            session.solution_id,
            old_workflow_id,
            request.new_workflow_id,
            memory_to_transfer
        )
        
        # Update session conversation memory
        session.conversation_memory.update(transferred)
    
    # Update session
    session.workflow_id = request.new_workflow_id
    session.workflow_history.append(request.new_workflow_id)
    session.updated_at = datetime.utcnow().isoformat()
    
    # Add system message about the switch
    switch_message = f"Switched from workflow '{old_workflow_id}' to '{request.new_workflow_id}'"
    if request.reason:
        switch_message += f". Reason: {request.reason}"
    
    session = chat_manager.add_message(
        session_id,
        role="assistant",
        content=switch_message,
        metadata={
            "system_event": "workflow_switch",
            "old_workflow": old_workflow_id,
            "new_workflow": request.new_workflow_id,
            "memory_transferred": request.transfer_memory
        }
    )
    
    return session


@router.get("/sessions/{session_id}/solution-context")
async def get_solution_context(session_id: str):
    """Get the solution context for a chat session, including available workflows."""
    session = chat_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
    
    if not session.solution_id:
        return {
            "has_solution": False,
            "message": "Session is not part of a solution"
        }
    
    # Get solution data
    solution = load("solutions", session.solution_id)
    if not solution:
        return {
            "has_solution": False,
            "error": "Solution not found"
        }
    
    # Get workflow details
    available_workflows = []
    for wf_id in solution.get("workflows", []):
        wf = load("workflows", wf_id)
        if wf:
            available_workflows.append({
                "id": wf_id,
                "name": wf.get("name", wf_id),
                "description": wf.get("description", ""),
                "is_current": wf_id == session.workflow_id
            })
    
    # Get communication blueprint
    blueprint = solution_service.get_communication_blueprint(session.solution_id)
    
    return {
        "has_solution": True,
        "solution_id": session.solution_id,
        "solution_name": solution.get("name", ""),
        "current_workflow": session.workflow_id,
        "available_workflows": available_workflows,
        "workflow_history": session.workflow_history,
        "communication_blueprint": blueprint,
        "shared_memory_size": len(str(solution.get("workflow_memory", {})))
    }


@router.get("/sessions/{session_id}/blueprint")
async def get_session_blueprint(session_id: str):
    """Get the real-time blueprint showing workflow structure and communication."""
    session = chat_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
    
    # Get current workflow
    workflow = load("workflows", session.workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail=f"Workflow {session.workflow_id} not found")
    
    blueprint = {
        "workflow": {
            "id": workflow["id"],
            "name": workflow.get("name", ""),
            "type": workflow.get("type", "sequence"),
            "nodes": workflow.get("nodes", [])
        },
        "session_state": {
            "message_count": len(session.messages),
            "agents_used": session.state.get("agents_used", []),
            "current_step": session.state.get("current_step", ""),
        }
    }
    
    # Add solution context if available
    if session.solution_id:
        blueprint["solution_context"] = solution_service.get_communication_blueprint(session.solution_id)
    
    return blueprint
