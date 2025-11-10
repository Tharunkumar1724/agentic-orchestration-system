from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import agents, tools, workflows, solutions, chat
from dotenv import load_dotenv
import yaml
import os
from pathlib import Path
from app.storage import save

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Agentic Orchestrator", version="0.1.0")


@app.on_event("startup")
async def startup_event():
    """Load configuration from YAML files on startup"""
    print("🚀 Loading configuration from YAML files...")
    
    # Load tools
    tools_dir = Path("config/tools")
    if tools_dir.exists():
        loaded_count = 0
        for yaml_file in tools_dir.glob("*.yaml"):
            try:
                with open(yaml_file, 'r') as f:
                    tool_data = yaml.safe_load(f)
                    tool_id = tool_data.get('id')
                    
                    if tool_id:
                        save("tools", tool_id, tool_data)
                        loaded_count += 1
                        print(f"  ✅ Loaded tool: {tool_id}")
                    else:
                        print(f"  ⚠️ Skipped {yaml_file.name} (no id)")
            except Exception as e:
                print(f"  ❌ Failed to load {yaml_file.name}: {e}")
        
        print(f"✅ Loaded {loaded_count} tools")
    else:
        print(f"⚠️ Tools directory not found: {tools_dir}")
    
    # Load agents
    agents_dir = Path("config/agents")
    if agents_dir.exists():
        loaded_count = 0
        for yaml_file in agents_dir.glob("*.yaml"):
            try:
                with open(yaml_file, 'r') as f:
                    agent_data = yaml.safe_load(f)
                    agent_id = agent_data.get('id')
                    
                    if agent_id:
                        save("agents", agent_id, agent_data)
                        loaded_count += 1
                    else:
                        print(f"  ⚠️ Skipped {yaml_file.name} (no id)")
            except Exception as e:
                print(f"  ❌ Failed to load {yaml_file.name}: {e}")
        
        print(f"✅ Loaded {loaded_count} agents")
    else:
        print(f"⚠️ Agents directory not found: {agents_dir}")
    
    # Load workflows
    workflows_dir = Path("config/workflows")
    if workflows_dir.exists():
        loaded_count = 0
        for yaml_file in workflows_dir.glob("*.yaml"):
            try:
                with open(yaml_file, 'r') as f:
                    workflow_data = yaml.safe_load(f)
                    workflow_id = workflow_data.get('id')
                    
                    if workflow_id:
                        save("workflows", workflow_id, workflow_data)
                        loaded_count += 1
                    else:
                        print(f"  ⚠️ Skipped {yaml_file.name} (no id)")
            except Exception as e:
                print(f"  ❌ Failed to load {yaml_file.name}: {e}")
        
        print(f"✅ Loaded {loaded_count} workflows")
    else:
        print(f"⚠️ Workflows directory not found: {workflows_dir}")
    
    # Load solutions
    solutions_dir = Path("config/solutions")
    if solutions_dir.exists():
        loaded_count = 0
        for yaml_file in solutions_dir.glob("*.yaml"):
            try:
                with open(yaml_file, 'r') as f:
                    solution_data = yaml.safe_load(f)
                    solution_id = solution_data.get('id')
                    
                    if solution_id:
                        save("solutions", solution_id, solution_data)
                        loaded_count += 1
                    else:
                        print(f"  ⚠️ Skipped {yaml_file.name} (no id)")
            except Exception as e:
                print(f"  ❌ Failed to load {yaml_file.name}: {e}")
        
        print(f"✅ Loaded {loaded_count} solutions")
    else:
        print(f"⚠️ Solutions directory not found: {solutions_dir}")
    
    print("✅ Configuration loading complete!")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers without /v1 prefix for frontend compatibility
app.include_router(agents.router, prefix="/agents", tags=["agents"])
app.include_router(tools.router, prefix="/tools", tags=["tools"])
app.include_router(workflows.router, prefix="/workflows", tags=["workflows"])
app.include_router(solutions.router, prefix="/solutions", tags=["solutions"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])

# Also include versioned routes for backward compatibility
app.include_router(agents.router, prefix="/v1/agents", tags=["agents-v1"])
app.include_router(tools.router, prefix="/v1/tools", tags=["tools-v1"])
app.include_router(workflows.router, prefix="/v1/workflows", tags=["workflows-v1"])
app.include_router(solutions.router, prefix="/v1/solutions", tags=["solutions-v1"])
app.include_router(chat.router, prefix="/v1/chat", tags=["chat-v1"])

@app.get("/health")
async def health():
    return {"status": "ok"}
