from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from app.models import SolutionDef, SolutionCreate, SolutionUpdate, WorkflowCommunication, WorkflowDef
from app.storage import save, load, list_all, delete
from datetime import datetime
import uuid

router = APIRouter()


@router.post("/", response_model=SolutionDef)
async def create_solution(s: SolutionCreate):
    """Create a new solution with optional workflows."""
    solution_id = s.id or f"solution_{uuid.uuid4().hex[:8]}"
    
    # Check if solution already exists
    if load("solutions", solution_id):
        raise HTTPException(status_code=400, detail="Solution already exists")
    
    # Verify all workflows exist
    for workflow_id in s.workflows:
        if not load("workflows", workflow_id):
            raise HTTPException(status_code=404, detail=f"Workflow '{workflow_id}' not found")
    
    now = datetime.utcnow().isoformat()
    solution = SolutionDef(
        id=solution_id,
        name=s.name,
        description=s.description,
        workflows=s.workflows,
        workflow_memory={},
        communication_config=s.communication_config,
        metadata=s.metadata,
        created_at=now,
        updated_at=now,
        version="v1"
    )
    
    save("solutions", solution_id, solution.model_dump())
    return solution


@router.get("/{solution_id}", response_model=SolutionDef)
async def get_solution(solution_id: str):
    """Get a specific solution by ID."""
    data = load("solutions", solution_id)
    if not data:
        raise HTTPException(status_code=404, detail="Solution not found")
    return data


@router.get("/", response_model=List[SolutionDef])
async def list_solutions():
    """List all solutions."""
    return list_all("solutions")


@router.put("/{solution_id}", response_model=SolutionDef)
async def update_solution(solution_id: str, update: SolutionUpdate):
    """Update an existing solution."""
    existing = load("solutions", solution_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Solution not found")
    
    # Verify all workflows exist if updating workflows
    if update.workflows is not None:
        for workflow_id in update.workflows:
            if not load("workflows", workflow_id):
                raise HTTPException(status_code=404, detail=f"Workflow '{workflow_id}' not found")
    
    # Update fields
    if update.name is not None:
        existing["name"] = update.name
    if update.description is not None:
        existing["description"] = update.description
    if update.workflows is not None:
        existing["workflows"] = update.workflows
    if update.communication_config is not None:
        existing["communication_config"] = update.communication_config
    if update.metadata is not None:
        existing["metadata"].update(update.metadata)
    
    existing["updated_at"] = datetime.utcnow().isoformat()
    
    save("solutions", solution_id, existing)
    return existing


@router.delete("/{solution_id}")
async def delete_solution(solution_id: str):
    """Delete a solution."""
    ok = delete("solutions", solution_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Solution not found")
    return {"deleted": True}


@router.post("/{solution_id}/workflows/{workflow_id}")
async def add_workflow_to_solution(solution_id: str, workflow_id: str):
    """Add a workflow to a solution."""
    solution = load("solutions", solution_id)
    if not solution:
        raise HTTPException(status_code=404, detail="Solution not found")
    
    workflow = load("workflows", workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    if workflow_id not in solution["workflows"]:
        solution["workflows"].append(workflow_id)
        solution["updated_at"] = datetime.utcnow().isoformat()
        save("solutions", solution_id, solution)
    
    return {"message": f"Workflow '{workflow_id}' added to solution '{solution_id}'", "solution": solution}


@router.delete("/{solution_id}/workflows/{workflow_id}")
async def remove_workflow_from_solution(solution_id: str, workflow_id: str):
    """Remove a workflow from a solution."""
    solution = load("solutions", solution_id)
    if not solution:
        raise HTTPException(status_code=404, detail="Solution not found")
    
    if workflow_id in solution["workflows"]:
        solution["workflows"].remove(workflow_id)
        solution["updated_at"] = datetime.utcnow().isoformat()
        save("solutions", solution_id, solution)
    
    return {"message": f"Workflow '{workflow_id}' removed from solution '{solution_id}'", "solution": solution}


@router.get("/{solution_id}/workflows", response_model=List[WorkflowDef])
async def get_solution_workflows(solution_id: str):
    """Get all workflows in a solution."""
    solution = load("solutions", solution_id)
    if not solution:
        raise HTTPException(status_code=404, detail="Solution not found")
    
    workflows = []
    for workflow_id in solution["workflows"]:
        workflow = load("workflows", workflow_id)
        if workflow:
            workflows.append(workflow)
    
    return workflows


@router.post("/{solution_id}/communicate")
async def send_workflow_communication(solution_id: str, comm: WorkflowCommunication):
    """Send communication between workflows in a solution."""
    solution = load("solutions", solution_id)
    if not solution:
        raise HTTPException(status_code=404, detail="Solution not found")
    
    # Verify workflows are in solution
    if comm.from_workflow_id not in solution["workflows"]:
        raise HTTPException(status_code=400, detail=f"Workflow '{comm.from_workflow_id}' not in solution")
    if comm.to_workflow_id not in solution["workflows"]:
        raise HTTPException(status_code=400, detail=f"Workflow '{comm.to_workflow_id}' not in solution")
    
    # Store communication in solution memory
    if "communication_log" not in solution["workflow_memory"]:
        solution["workflow_memory"]["communication_log"] = []
    
    solution["workflow_memory"]["communication_log"].append(comm.model_dump())
    solution["updated_at"] = datetime.utcnow().isoformat()
    save("solutions", solution_id, solution)
    
    return {"message": "Communication sent", "communication": comm}


@router.get("/{solution_id}/communications")
async def get_solution_communications(solution_id: str):
    """Get all inter-workflow communications in a solution."""
    solution = load("solutions", solution_id)
    if not solution:
        raise HTTPException(status_code=404, detail="Solution not found")
    
    return solution.get("workflow_memory", {}).get("communication_log", [])
