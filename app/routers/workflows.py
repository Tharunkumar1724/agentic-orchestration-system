from fastapi import APIRouter, HTTPException
from app.models import WorkflowDef, RunResult
from app.storage import save, load, list_all, delete
from app.services.orchestrator import run_workflow
from typing import List, Optional
from pydantic import BaseModel
import uuid

router = APIRouter()


class RunRequest(BaseModel):
    query: Optional[str] = None


@router.post("/", response_model=WorkflowDef)
async def create_workflow(w: WorkflowDef):
    if load("workflows", w.id):
        raise HTTPException(status_code=400, detail="Workflow exists")
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
async def run_workflow_endpoint(workflow_id: str, request: RunRequest = RunRequest()):
    data = load("workflows", workflow_id)
    if not data:
        raise HTTPException(status_code=404, detail="Workflow not found")
    run_id = str(uuid.uuid4())
    
    # Pass query to workflow if provided
    if request.query:
        # Inject query into first node's task
        if data.get("nodes") and len(data["nodes"]) > 0:
            data["nodes"][0]["task"] = request.query
    
    result = await run_workflow(data, run_id)
    save("runs", run_id, result)
    return result
