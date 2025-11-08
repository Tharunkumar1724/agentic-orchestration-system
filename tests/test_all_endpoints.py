"""Comprehensive test suite for all API endpoints."""
import pytest
import asyncio
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient
from app.main import app
from app.storage import save, load, delete, list_all

client = TestClient(app)


class TestHealthEndpoint:
    """Test health check endpoint."""
    
    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestToolsEndpoints:
    """Test all tools CRUD endpoints."""
    
    def setup_method(self):
        """Clean up before each test."""
        try:
            delete("tools", "test_tool")
        except:
            pass
    
    def test_create_tool(self):
        """Test POST /v1/tools/"""
        tool_data = {
            "id": "test_tool",
            "name": "Test Tool",
            "type": "websearch",
            "config": {"max_results": 5},
            "version": "v1"
        }
        response = client.post("/v1/tools/", json=tool_data)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "test_tool"
        assert data["type"] == "websearch"
    
    def test_get_tool(self):
        """Test GET /v1/tools/{tool_id}"""
        # First create a tool
        tool_data = {
            "id": "test_tool",
            "name": "Test Tool",
            "type": "api",
            "config": {},
            "version": "v1"
        }
        client.post("/v1/tools/", json=tool_data)
        
        # Now get it
        response = client.get("/v1/tools/test_tool")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "test_tool"
    
    def test_list_tools(self):
        """Test GET /v1/tools/"""
        response = client.get("/v1/tools/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_update_tool(self):
        """Test PUT /v1/tools/{tool_id}"""
        tool_data = {
            "id": "test_tool",
            "name": "Updated Tool",
            "type": "code",
            "config": {"snippet": "print('test')"},
            "version": "v1"
        }
        response = client.put("/v1/tools/test_tool", json=tool_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Tool"
    
    def test_delete_tool(self):
        """Test DELETE /v1/tools/{tool_id}"""
        # Create first
        tool_data = {
            "id": "test_tool",
            "name": "Test Tool",
            "type": "websearch",
            "config": {},
            "version": "v1"
        }
        client.post("/v1/tools/", json=tool_data)
        
        # Delete
        response = client.delete("/v1/tools/test_tool")
        assert response.status_code == 200
        data = response.json()
        assert data["deleted"] == True


class TestAgentsEndpoints:
    """Test all agents CRUD endpoints."""
    
    def setup_method(self):
        """Clean up before each test."""
        try:
            delete("agents", "test_agent")
        except:
            pass
    
    def test_create_agent(self):
        """Test POST /v1/agents/"""
        agent_data = {
            "id": "test_agent",
            "name": "Test Agent",
            "type": "zero_shot",
            "llm_config": {},
            "tools": [],
            "use_kag": False,
            "version": "v1"
        }
        response = client.post("/v1/agents/", json=agent_data)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "test_agent"
        assert data["type"] == "zero_shot"
    
    def test_get_agent(self):
        """Test GET /v1/agents/{agent_id}"""
        agent_data = {
            "id": "test_agent",
            "name": "Test Agent",
            "type": "react",
            "llm_config": {},
            "tools": ["search_tool"],
            "use_kag": False,
            "version": "v1"
        }
        client.post("/v1/agents/", json=agent_data)
        
        response = client.get("/v1/agents/test_agent")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "test_agent"
        assert data["tools"] == ["search_tool"]
    
    def test_list_agents(self):
        """Test GET /v1/agents/"""
        response = client.get("/v1/agents/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_update_agent(self):
        """Test PUT /v1/agents/{agent_id}"""
        agent_data = {
            "id": "test_agent",
            "name": "Updated Agent",
            "type": "custom",
            "llm_config": {"temp": 0.9},
            "tools": [],
            "use_kag": True,
            "version": "v1"
        }
        response = client.put("/v1/agents/test_agent", json=agent_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Agent"
        assert data["use_kag"] == True
    
    def test_delete_agent(self):
        """Test DELETE /v1/agents/{agent_id}"""
        agent_data = {
            "id": "test_agent",
            "name": "Test Agent",
            "type": "zero_shot",
            "llm_config": {},
            "tools": [],
            "use_kag": False,
            "version": "v1"
        }
        client.post("/v1/agents/", json=agent_data)
        
        response = client.delete("/v1/agents/test_agent")
        assert response.status_code == 200
        data = response.json()
        assert data["deleted"] == True


class TestWorkflowsEndpoints:
    """Test all workflows CRUD endpoints."""
    
    def setup_method(self):
        """Clean up before each test."""
        try:
            delete("workflows", "test_workflow")
        except:
            pass
    
    def test_create_workflow(self):
        """Test POST /v1/workflows/"""
        workflow_data = {
            "id": "test_workflow",
            "name": "Test Workflow",
            "version": "v1",
            "type": "sequence",
            "nodes": [
                {
                    "id": "step1",
                    "type": "agent",
                    "agent_ref": "test_agent",
                    "inputs": {"prompt": "test"}
                }
            ]
        }
        response = client.post("/v1/workflows/", json=workflow_data)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "test_workflow"
        assert data["type"] == "sequence"
    
    def test_get_workflow(self):
        """Test GET /v1/workflows/{workflow_id}"""
        workflow_data = {
            "id": "test_workflow",
            "name": "Test Workflow",
            "version": "v1",
            "type": "parallel",
            "nodes": []
        }
        client.post("/v1/workflows/", json=workflow_data)
        
        response = client.get("/v1/workflows/test_workflow")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "test_workflow"
    
    def test_list_workflows(self):
        """Test GET /v1/workflows/"""
        response = client.get("/v1/workflows/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_update_workflow(self):
        """Test PUT /v1/workflows/{workflow_id}"""
        workflow_data = {
            "id": "test_workflow",
            "name": "Updated Workflow",
            "version": "v2",
            "type": "sequence",
            "nodes": []
        }
        response = client.put("/v1/workflows/test_workflow", json=workflow_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Workflow"
    
    def test_delete_workflow(self):
        """Test DELETE /v1/workflows/{workflow_id}"""
        workflow_data = {
            "id": "test_workflow",
            "name": "Test Workflow",
            "version": "v1",
            "type": "sequence",
            "nodes": []
        }
        client.post("/v1/workflows/", json=workflow_data)
        
        response = client.delete("/v1/workflows/test_workflow")
        assert response.status_code == 200
        data = response.json()
        assert data["deleted"] == True


class TestSolutionsEndpoints:
    """Test all solutions CRUD endpoints."""
    
    def setup_method(self):
        """Clean up before each test."""
        try:
            delete("solutions", "test_solution")
        except:
            pass
    
    def test_create_solution(self):
        """Test POST /v1/solutions/"""
        solution_data = {
            "id": "test_solution",
            "name": "Test Solution",
            "workflows": ["workflow1", "workflow2"],
            "version": "v1"
        }
        response = client.post("/v1/solutions/", json=solution_data)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "test_solution"
        assert len(data["workflows"]) == 2
    
    def test_get_solution(self):
        """Test GET /v1/solutions/{solution_id}"""
        solution_data = {
            "id": "test_solution",
            "name": "Test Solution",
            "workflows": [],
            "version": "v1"
        }
        client.post("/v1/solutions/", json=solution_data)
        
        response = client.get("/v1/solutions/test_solution")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "test_solution"
    
    def test_list_solutions(self):
        """Test GET /v1/solutions/"""
        response = client.get("/v1/solutions/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_update_solution(self):
        """Test PUT /v1/solutions/{solution_id}"""
        solution_data = {
            "id": "test_solution",
            "name": "Updated Solution",
            "workflows": ["new_workflow"],
            "version": "v2"
        }
        response = client.put("/v1/solutions/test_solution", json=solution_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Solution"
    
    def test_delete_solution(self):
        """Test DELETE /v1/solutions/{solution_id}"""
        solution_data = {
            "id": "test_solution",
            "name": "Test Solution",
            "workflows": [],
            "version": "v1"
        }
        client.post("/v1/solutions/", json=solution_data)
        
        response = client.delete("/v1/solutions/test_solution")
        assert response.status_code == 200
        data = response.json()
        assert data["deleted"] == True


class TestWorkflowExecution:
    """Test workflow execution endpoint."""
    
    def setup_method(self):
        """Set up test data."""
        # Clean up
        for item in ["exec_tool", "exec_agent", "exec_workflow"]:
            try:
                delete("tools", item)
                delete("agents", item)
                delete("workflows", item)
            except:
                pass
    
    def test_run_simple_workflow(self):
        """Test POST /v1/workflows/{workflow_id}/run"""
        # Create tool
        tool_data = {
            "id": "exec_tool",
            "name": "Exec Tool",
            "type": "websearch",
            "config": {},
            "version": "v1"
        }
        client.post("/v1/tools/", json=tool_data)
        
        # Create agent
        agent_data = {
            "id": "exec_agent",
            "name": "Exec Agent",
            "type": "zero_shot",
            "llm_config": {},
            "tools": ["exec_tool"],
            "use_kag": False,
            "version": "v1"
        }
        client.post("/v1/agents/", json=agent_data)
        
        # Create workflow
        workflow_data = {
            "id": "exec_workflow",
            "name": "Exec Workflow",
            "version": "v1",
            "type": "sequence",
            "nodes": [
                {
                    "id": "step1",
                    "type": "agent",
                    "agent_ref": "exec_agent",
                    "inputs": {"prompt": "Test execution"}
                }
            ]
        }
        client.post("/v1/workflows/", json=workflow_data)
        
        # Run workflow
        response = client.post("/v1/workflows/exec_workflow/run")
        assert response.status_code == 200
        data = response.json()
        assert "workflow_id" in data
        assert "run_id" in data
        assert "status" in data
        assert "result" in data
        assert "meta" in data
        assert isinstance(data["meta"], dict)
        assert "communication_log" in data["meta"]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
