from fastapi import APIRouter, HTTPException, Query, WebSocket, WebSocketDisconnect
from app.models import WorkflowDef, RunResult
from app.storage import save, load, list_all, delete
from app.services.orchestrator import run_workflow
from app.services.output_formatter import output_formatter
from app.services.kag_service import get_kag_service, invoke_kag
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import uuid
import json
import asyncio

router = APIRouter()

# WebSocket connection manager for live updates
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
    
    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
    
    async def send_message(self, message: dict, client_id: str):
        if client_id in self.active_connections:
            try:
                await self.active_connections[client_id].send_json(message)
            except:
                self.disconnect(client_id)
    
    async def broadcast(self, message: dict):
        disconnected = []
        for client_id, connection in self.active_connections.items():
            try:
                await connection.send_json(message)
            except:
                disconnected.append(client_id)
        
        for client_id in disconnected:
            self.disconnect(client_id)

manager = ConnectionManager()


class RunRequest(BaseModel):
    query: Optional[str] = None
    format: Optional[str] = "structured"  # Options: "structured", "compact", "raw", "text"
    solution_id: Optional[str] = None  # For workflow communication
    previous_workflow_id: Optional[str] = None  # For handoff


class CommunicateRequest(BaseModel):
    source_workflow_id: str
    target_workflow_id: str
    solution_id: str
    target_task: Optional[str] = None


@router.post("/", response_model=WorkflowDef)
async def create_workflow(w: WorkflowDef):
    # Generate ID if not provided or empty
    if not w.id or w.id.strip() == "":
        w.id = f"workflow_{uuid.uuid4().hex[:8]}"
    
    # Check if workflow already exists
    existing = load("workflows", w.id)
    if existing:
        raise HTTPException(
            status_code=400, 
            detail=f"Workflow with ID '{w.id}' already exists. Use PUT to update or choose a different ID."
        )
    
    save("workflows", w.id, w.model_dump())
    return w


@router.get("/", response_model=List[WorkflowDef])
async def list_workflows():
    return list_all("workflows")


@router.get("/runs", response_model=List[dict])
async def list_runs():
    """List all workflow runs"""
    return list_all("runs")


@router.get("/runs/{run_id}")
async def get_run(run_id: str):
    """Get a specific workflow run result"""
    data = load("runs", run_id)
    if not data:
        raise HTTPException(status_code=404, detail="Run not found")
    return data


@router.get("/{workflow_id}", response_model=WorkflowDef)
async def get_workflow(workflow_id: str):
    data = load("workflows", workflow_id)
    if not data:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return data


@router.put("/{workflow_id}", response_model=WorkflowDef)
async def update_workflow(workflow_id: str, w: WorkflowDef):
    save("workflows", workflow_id, w.model_dump())
    return w


@router.delete("/{workflow_id}")
async def delete_workflow(workflow_id: str):
    ok = delete("workflows", workflow_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return {"deleted": True}


@router.post("/{workflow_id}/run", response_model=RunResult)
async def run_workflow_endpoint(
    workflow_id: str, 
    request: RunRequest = RunRequest(),
    format: Optional[str] = Query("structured", description="Output format: structured, compact, raw, text")
):
    """
    Execute a workflow and return formatted results with KAG integration.
    
    Args:
        workflow_id: ID of the workflow to run
        request: Run request with optional query, format, and solution context
        format: Output format (structured, compact, raw, text)
    """
    data = load("workflows", workflow_id)
    if not data:
        raise HTTPException(status_code=404, detail="Workflow not found")
    run_id = str(uuid.uuid4())
    
    # Handle workflow-to-workflow communication
    context_data = None
    if request.solution_id and request.previous_workflow_id:
        kag_service = get_kag_service()
        handoff = kag_service.prepare_handoff(
            source_workflow_id=request.previous_workflow_id,
            target_workflow_id=workflow_id,
            target_workflow_description=data.get("description", ""),
            solution_id=request.solution_id
        )
        context_data = handoff
        
        # Broadcast handoff event
        await manager.broadcast({
            "type": "workflow_handoff",
            "solution_id": request.solution_id,
            "from": request.previous_workflow_id,
            "to": workflow_id,
            "data": handoff
        })
    
    # Pass query to workflow if provided
    task_input = request.query
    if context_data:
        # Combine query with handoff context
        task_input = f"{request.query}\n\nContext from previous workflow:\n{context_data.get('handoff_data', '')}" if request.query else context_data.get('handoff_data', '')
    
    if task_input and data.get("nodes") and len(data["nodes"]) > 0:
        data["nodes"][0]["task"] = task_input
    
    # Broadcast workflow start
    if request.solution_id:
        await manager.broadcast({
            "type": "workflow_start",
            "solution_id": request.solution_id,
            "workflow_id": workflow_id,
            "run_id": run_id
        })
    
    # Use format from request body or query parameter
    output_format = request.format or format
    
    # Execute workflow with formatting preference
    result = await run_workflow(data, run_id)
    
    # Invoke KAG to extract facts and create memory
    if request.solution_id:
        workflow_name = data.get("name", workflow_id)
        raw_output = json.dumps(result.get("results", result.get("result", "")))
        
        kag_result = invoke_kag(
            workflow_output=raw_output,
            workflow_name=workflow_name,
            solution_id=request.solution_id,
            workflow_id=workflow_id,
            context=data.get("description", "")
        )
        
        # Add KAG data to result
        result["kag"] = kag_result
        
        # Broadcast KAG completion
        await manager.broadcast({
            "type": "workflow_kag",
            "solution_id": request.solution_id,
            "workflow_id": workflow_id,
            "run_id": run_id,
            "summary": kag_result.get("summary"),
            "facts": kag_result.get("facts", [])
        })
    
    # Apply additional formatting based on request
    if output_format == "compact":
        result = output_formatter.format_compact(result)
    elif output_format == "text":
        text_output = output_formatter.format_for_display(result)
        result = {
            "workflow_id": result.get("workflow_id"),
            "run_id": result.get("run_id"),
            "status": result.get("status"),
            "output": text_output
        }
    elif output_format == "raw":
        # Return raw unformatted result
        result = result.get("_raw", result)
    # "structured" is default and already applied by run_workflow
    
    # Broadcast workflow completion
    if request.solution_id:
        await manager.broadcast({
            "type": "workflow_complete",
            "solution_id": request.solution_id,
            "workflow_id": workflow_id,
            "run_id": run_id,
            "status": result.get("status")
        })
    
    # Save the result
    save("runs", run_id, result)
    return result


@router.post("/communicate", response_model=Dict[str, Any])
async def communicate_workflows(request: CommunicateRequest):
    """
    Facilitate communication between two workflows using KAG.
    
    This endpoint prepares the handoff data from source to target workflow.
    """
    kag_service = get_kag_service()
    
    # Load target workflow to get description
    target_data = load("workflows", request.target_workflow_id)
    if not target_data:
        raise HTTPException(status_code=404, detail="Target workflow not found")
    
    target_description = request.target_task or target_data.get("description", "")
    
    # Prepare handoff
    handoff_data = kag_service.prepare_handoff(
        source_workflow_id=request.source_workflow_id,
        target_workflow_id=request.target_workflow_id,
        target_workflow_description=target_description,
        solution_id=request.solution_id
    )
    
    # Broadcast communication event
    await manager.broadcast({
        "type": "workflow_communication",
        "solution_id": request.solution_id,
        "from": request.source_workflow_id,
        "to": request.target_workflow_id,
        "handoff": handoff_data
    })
    
    return {
        "success": True,
        "handoff_data": handoff_data,
        "source_workflow_id": request.source_workflow_id,
        "target_workflow_id": request.target_workflow_id
    }


@router.get("/solution/{solution_id}/summary")
async def get_solution_summary(solution_id: str):
    """Get comprehensive summary of all workflows in a solution"""
    kag_service = get_kag_service()
    summary = kag_service.get_solution_summary(solution_id)
    return summary


@router.delete("/solution/{solution_id}/memory")
async def clear_solution_memory(solution_id: str):
    """Clear conversation memory for a solution"""
    kag_service = get_kag_service()
    kag_service.clear_solution_memory(solution_id)
    return {"success": True, "message": "Solution memory cleared"}


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """
    WebSocket endpoint for real-time workflow execution updates
    
    Clients connect with a unique client_id and receive:
    - workflow_start: When a workflow begins execution
    - workflow_kag: When KAG analysis completes
    - workflow_handoff: When data is handed off between workflows
    - workflow_complete: When a workflow finishes
    - workflow_communication: General communication events
    """
    await manager.connect(websocket, client_id)
    try:
        while True:
            # Keep connection alive and handle any incoming messages
            data = await websocket.receive_text()
            # Echo back or process client messages if needed
            await websocket.send_json({"type": "ping", "message": "connected"})
    except WebSocketDisconnect:
        manager.disconnect(client_id)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(client_id)
