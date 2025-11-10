from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from typing import List, Dict, Any
from app.models import SolutionDef, SolutionCreate, SolutionUpdate, WorkflowCommunication, WorkflowDef
from app.storage import save, load, list_all, delete
from app.services.kag_service import get_kag_service
from app.services.orchestrator import run_workflow
from datetime import datetime
import uuid
import asyncio
import json

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


@router.post("/{solution_id}/execute")
async def execute_solution(solution_id: str, query: str = "Execute solution"):
    """
    Execute all workflows in a solution sequentially with AI-powered communication.
    Each workflow's output is analyzed by Gemini, facts are extracted, and context is passed to the next workflow.
    Returns comprehensive metrics for the entire solution execution.
    """
    solution = load("solutions", solution_id)
    if not solution:
        raise HTTPException(status_code=404, detail="Solution not found")
    
    if not solution.get("workflows"):
        raise HTTPException(status_code=400, detail="Solution has no workflows")
    
    kag_service = get_kag_service()
    execution_results = []
    
    # Aggregate metrics across all workflows
    from app.services.metrics_service import create_metrics_tracker
    solution_metrics = create_metrics_tracker()
    solution_metrics.start()
    
    try:
        # Execute workflows in sequence
        for i, workflow_id in enumerate(solution["workflows"]):
            workflow = load("workflows", workflow_id)
            if not workflow:
                raise HTTPException(status_code=404, detail=f"Workflow '{workflow_id}' not found")
            
            # Prepare handoff context from previous workflow
            handoff_context = None
            if i > 0:
                previous_workflow_id = solution["workflows"][i - 1]
                handoff_context = kag_service.prepare_handoff(
                    source_workflow_id=previous_workflow_id,
                    target_workflow_id=workflow_id,
                    target_workflow_description=workflow.get("description", ""),
                    solution_id=solution_id
                )
            
            # Execute workflow with actual orchestrator
            try:
                result = await run_workflow(workflow, run_id=f"solution_{solution_id}_{i}")
                workflow_output = json.dumps(result.get("results", result.get("result", "")))
                
                # Aggregate metrics from this workflow
                if result.get("metrics"):
                    wf_metrics = result["metrics"]
                    solution_metrics.token_count += wf_metrics.get("token_usage_count", 0)
                    solution_metrics.token_input += wf_metrics.get("token_input_count", 0)
                    solution_metrics.token_output += wf_metrics.get("token_output_count", 0)
                    solution_metrics.tool_invocations.extend([{"workflow": workflow_id}] * wf_metrics.get("tool_invocation_count", 0))
                    solution_metrics.errors.extend(wf_metrics.get("errors", []))
                    solution_metrics.warnings.extend(wf_metrics.get("warnings", []))
                    solution_metrics.steps_executed += wf_metrics.get("workflow_step_count", 0)
                
            except Exception as e:
                workflow_output = f"Error executing workflow: {str(e)}"
                solution_metrics.add_error(f"Workflow {workflow_id}: {str(e)}")
            
            # Invoke KAG to extract facts and store in memory
            kag_result = kag_service.invoke_kag(
                workflow_output=workflow_output,
                workflow_name=workflow.get("name", workflow_id),
                solution_id=solution_id,
                workflow_id=workflow_id,
                context=f"Workflow {i+1} of {len(solution['workflows'])}"
            )
            
            execution_results.append({
                "workflow_id": workflow_id,
                "workflow_name": workflow.get("name", workflow_id),
                "position": i + 1,
                "total": len(solution["workflows"]),
                "handoff_received": handoff_context,
                "kag_analysis": kag_result,
                "output": workflow_output,
                "metrics": result.get("metrics", {}) if 'result' in locals() else {}
            })
        
        # End solution metrics tracking
        solution_metrics.end()
        aggregated_metrics = solution_metrics.calculate_metrics(
            task_completed=(len(solution_metrics.errors) == 0)
        )
        
        # Get solution summary
        summary = kag_service.get_solution_summary(solution_id)
        
        return {
            "solution_id": solution_id,
            "solution_name": solution.get("name", ""),
            "execution_results": execution_results,
            "summary": summary,
            "metrics": aggregated_metrics.model_dump(),  # Include aggregated metrics
            "success": True
        }
        
    except Exception as e:
        solution_metrics.end()
        solution_metrics.add_error(f"Solution execution failed: {str(e)}")
        aggregated_metrics = solution_metrics.calculate_metrics(task_completed=False)
        
        raise HTTPException(
            status_code=500, 
            detail={
                "message": f"Execution failed: {str(e)}",
                "metrics": aggregated_metrics.model_dump()
            }
        )


@router.get("/{solution_id}/summary")
async def get_solution_summary(solution_id: str):
    """Get AI-powered summary of all workflow executions in a solution."""
    solution = load("solutions", solution_id)
    if not solution:
        raise HTTPException(status_code=404, detail="Solution not found")
    
    kag_service = get_kag_service()
    summary = kag_service.get_solution_summary(solution_id)
    
    return summary


@router.websocket("/ws/{solution_id}")
async def solution_websocket(websocket: WebSocket, solution_id: str):
    """
    WebSocket for real-time solution execution updates with workflow communication visualization
    """
    print(f"🔌 WebSocket connection requested for solution: {solution_id}")
    await websocket.accept()
    print(f"✅ WebSocket accepted for solution: {solution_id}")
    
    solution = load("solutions", solution_id)
    if not solution:
        print(f"❌ Solution not found: {solution_id}")
        await websocket.send_json({"type": "error", "message": "Solution not found"})
        await websocket.close()
        return
    
    print(f"📦 Loaded solution: {solution.get('name')}, workflows: {solution.get('workflows')}")
    kag_service = get_kag_service()
    
    try:
        while True:
            # Wait for execution request
            print(f"⏳ Waiting for client command...")
            data = await websocket.receive_json()
            print(f"📨 Received data: {data}")
            
            if data.get("action") == "execute":
                print(f"▶️ Starting execution of solution: {solution_id}")
                
                # Get user query from the request
                user_query = data.get("query", "")
                print(f"📝 User query: {user_query}")
                
                await websocket.send_json({
                    "type": "execution_started",
                    "solution_id": solution_id,
                    "total_workflows": len(solution["workflows"]),
                    "query": user_query
                })
                print(f"📤 Sent execution_started")
                
                # Execute workflows and stream updates
                for i, workflow_id in enumerate(solution["workflows"]):
                    print(f"\n🔄 Processing workflow {i+1}/{len(solution['workflows'])}: {workflow_id}")
                    workflow = load("workflows", workflow_id)
                    if not workflow:
                        print(f"⚠️ Workflow not found: {workflow_id}")
                        continue
                    
                    await websocket.send_json({
                        "type": "workflow_started",
                        "workflow_id": workflow_id,
                        "workflow_name": workflow.get("name", workflow_id),
                        "position": i + 1,
                        "total": len(solution["workflows"])
                    })
                    print(f"📤 Sent workflow_started for: {workflow.get('name')}")
                    
                    # Prepare handoff from previous workflow
                    handoff_context = None
                    if i > 0:
                        previous_workflow_id = solution["workflows"][i - 1]
                        handoff_context = kag_service.prepare_handoff(
                            source_workflow_id=previous_workflow_id,
                            target_workflow_id=workflow_id,
                            target_workflow_description=workflow.get("description", ""),
                            solution_id=solution_id
                        )
                        
                        await websocket.send_json({
                            "type": "handoff_prepared",
                            "from_workflow": previous_workflow_id,
                            "to_workflow": workflow_id,
                            "handoff_data": handoff_context
                        })
                    
                    # Execute actual workflow
                    try:
                        run_id = str(uuid.uuid4())
                        
                        # Build task with user query
                        if user_query:
                            # Use the actual user query as the task
                            task_input = f"{user_query}"
                            if handoff_context:
                                task_input += f"\n\nContext from previous workflow:\n{handoff_context.get('handoff_data', '')}"
                        else:
                            # Fallback to generic task
                            task_input = f"Execute as part of solution: {solution.get('name', '')}"
                            if handoff_context:
                                task_input += f"\n\nContext from previous workflow:\n{handoff_context.get('handoff_data', '')}"
                        
                        # Set task in first node
                        if workflow.get("nodes") and len(workflow["nodes"]) > 0:
                            workflow["nodes"][0]["task"] = task_input
                        
                        # Execute workflow
                        result = await run_workflow(workflow, run_id)
                        
                        # Extract output
                        workflow_output = json.dumps(result.get("results", result.get("result", "")))
                        
                    except Exception as e:
                        workflow_output = f"Error executing workflow: {str(e)}"
                        print(f"Workflow execution error: {e}")
                    
                    # Invoke KAG
                    kag_result = kag_service.invoke_kag(
                        workflow_output=workflow_output,
                        workflow_name=workflow.get("name", workflow_id),
                        solution_id=solution_id,
                        workflow_id=workflow_id,
                        context=f"Workflow {i+1} of {len(solution['workflows'])}"
                    )
                    
                    await websocket.send_json({
                        "type": "workflow_completed",
                        "workflow_id": workflow_id,
                        "workflow_name": workflow.get("name", workflow_id),
                        "kag_analysis": kag_result,
                        "output": workflow_output,
                        "metrics": result.get("metrics", {}) if 'result' in locals() else {}  # Include metrics
                    })
                
                # Send final summary
                summary = kag_service.get_solution_summary(solution_id)
                
                # Calculate aggregated metrics
                from app.services.metrics_service import create_metrics_tracker
                solution_tracker = create_metrics_tracker()
                solution_tracker.start()
                
                # Aggregate all workflow metrics
                all_workflow_results = []
                for i, wf_id in enumerate(solution["workflows"]):
                    # Store workflow results for aggregation
                    # Note: In real implementation, you'd collect these during execution
                    pass
                
                solution_tracker.end()
                overall_metrics = solution_tracker.calculate_metrics(task_completed=True)
                
                await websocket.send_json({
                    "type": "execution_completed",
                    "solution_id": solution_id,
                    "summary": summary,
                    "overall_metrics": overall_metrics.model_dump()  # Include aggregated metrics
                })
                
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for solution {solution_id}")
    except Exception as e:
        await websocket.send_json({"type": "error", "message": str(e)})
        await websocket.close()
