from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import agents, tools, workflows, solutions, chat

app = FastAPI(title="Agentic Orchestrator", version="0.1.0")

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
