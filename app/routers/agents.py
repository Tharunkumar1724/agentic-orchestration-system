from fastapi import APIRouter, HTTPException
from app.models import AgentDef
from app.storage import save, load, list_all, delete
from typing import List

router = APIRouter()


@router.post("/", response_model=AgentDef)
async def create_agent(agent: AgentDef):
    # Generate ID if not provided or empty
    if not agent.id or agent.id.strip() == "":
        import uuid
        agent.id = f"agent_{uuid.uuid4().hex[:8]}"
    
    # Check if agent already exists
    existing = load("agents", agent.id)
    if existing:
        raise HTTPException(
            status_code=400, 
            detail=f"Agent with ID '{agent.id}' already exists. Use PUT to update or choose a different ID."
        )
    
    save("agents", agent.id, agent.model_dump())
    return agent


@router.get("/{agent_id}", response_model=AgentDef)
async def get_agent(agent_id: str):
    data = load("agents", agent_id)
    if not data:
        raise HTTPException(status_code=404, detail="Agent not found")
    return data


@router.get("/", response_model=List[AgentDef])
async def list_agents():
    return list_all("agents")


@router.put("/{agent_id}", response_model=AgentDef)
async def update_agent(agent_id: str, agent: AgentDef):
    save("agents", agent_id, agent.model_dump())
    return agent


@router.delete("/{agent_id}")
async def delete_agent(agent_id: str):
    ok = delete("agents", agent_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"deleted": True}
