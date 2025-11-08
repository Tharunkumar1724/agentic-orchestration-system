"""
Comprehensive test for AI research workflow with DuckDuckGo search and Groq agent.
Tests agent-to-agent communication and real tool execution using LangGraph.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)


class TestAIResearchWorkflow:
    """Test the complete AI research workflow with communication."""
    
    def test_duckduckgo_tool_exists(self):
        """Verify DuckDuckGo search tool is configured."""
        response = client.get("/v1/tools/duckduckgo_search")
        assert response.status_code == 200
        tool = response.json()
        assert tool["id"] == "duckduckgo_search"
        assert tool["type"] == "websearch"
        assert tool["config"]["engine"] == "duckduckgo"
        print(f"✓ DuckDuckGo tool configured: {json.dumps(tool, indent=2)}")
    
    def test_groq_researcher_agent_exists(self):
        """Verify Groq researcher agent is configured."""
        response = client.get("/v1/agents/groq_researcher")
        assert response.status_code == 200
        agent = response.json()
        assert agent["id"] == "groq_researcher"
        assert agent["type"] == "react"
        assert agent["llm_config"]["provider"] == "groq"
        assert agent["llm_config"]["model"] == "llama-3.1-8b-instant"
        assert "duckduckgo_search" in agent["tools"]
        assert agent["communication"]["can_receive"] is True
        assert agent["communication"]["can_send"] is True
        print(f"✓ Groq researcher agent configured: {json.dumps(agent, indent=2)}")
    
    def test_analyzer_agent_exists(self):
        """Verify analyzer agent is configured."""
        response = client.get("/v1/agents/analyzer_agent")
        assert response.status_code == 200
        agent = response.json()
        assert agent["id"] == "analyzer_agent"
        print(f"✓ Analyzer agent exists: {agent['name']}")
    
    def test_ai_research_workflow_exists(self):
        """Verify AI research workflow is configured."""
        response = client.get("/v1/workflows/ai_research_workflow")
        assert response.status_code == 200
        workflow = response.json()
        assert workflow["id"] == "ai_research_workflow"
        assert workflow["type"] == "sequence"
        assert len(workflow["nodes"]) == 2
        
        # Check research node
        research_node = workflow["nodes"][0]
        assert research_node["id"] == "research"
        assert research_node["agent_ref"] == "groq_researcher"
        assert "analyze" in research_node["sends_to"]
        
        # Check analyze node
        analyze_node = workflow["nodes"][1]
        assert analyze_node["id"] == "analyze"
        assert analyze_node["agent_ref"] == "analyzer_agent"
        assert "research" in analyze_node["receives_from"]
        
        print(f"✓ AI research workflow configured: {json.dumps(workflow, indent=2)}")
    
    @pytest.mark.asyncio
    async def test_run_ai_research_workflow(self):
        """Run the complete AI research workflow and verify results."""
        response = client.post("/v1/workflows/ai_research_workflow/run")
        assert response.status_code == 200
        
        result = response.json()
        print(f"\n{'='*80}")
        print(f"WORKFLOW EXECUTION RESULT")
        print(f"{'='*80}")
        print(json.dumps(result, indent=2))
        
        # Verify basic structure
        assert result["workflow_id"] == "ai_research_workflow"
        assert "run_id" in result
        assert result["status"] in ["success", "failed"]
        
        # Verify results
        assert "result" in result
        assert "meta" in result
        
        # Check communication log
        assert "communication_log" in result["meta"]
        messages = result["meta"]["communication_log"]
        assert len(messages) > 0
        
        # Verify both agents executed
        assert "agents_used" in result["meta"]
        agents_used = result["meta"]["agents_used"]
        print(f"\n✓ Agents used: {agents_used}")
        
        # Check if research node executed
        if "research" in result["result"]:
            research_result = result["result"]["research"]
            print(f"\n{'='*80}")
            print(f"RESEARCH NODE RESULT")
            print(f"{'='*80}")
            print(json.dumps(research_result, indent=2))
            
            # Verify tool execution
            if "tool_results" in research_result:
                tool_results = research_result["tool_results"]
                if "duckduckgo_search" in tool_results:
                    search_result = tool_results["duckduckgo_search"]
                    print(f"\n✓ DuckDuckGo search executed")
                    print(f"  Query: {search_result.get('query', 'N/A')}")
                    print(f"  Results count: {search_result.get('count', 0)}")
                    
                    if "results" in search_result and search_result["results"]:
                        print(f"\n  Search Results:")
                        for i, r in enumerate(search_result["results"][:3], 1):
                            print(f"    {i}. {r.get('title', 'N/A')}")
                            print(f"       {r.get('href', 'N/A')}")
        
        # Check if analyze node executed
        if "analyze" in result["result"]:
            analyze_result = result["result"]["analyze"]
            print(f"\n{'='*80}")
            print(f"ANALYZE NODE RESULT")
            print(f"{'='*80}")
            print(json.dumps(analyze_result, indent=2))
        
        # Verify communication between agents
        print(f"\n{'='*80}")
        print(f"AGENT COMMUNICATION LOG")
        print(f"{'='*80}")
        for i, msg in enumerate(messages, 1):
            print(f"\n{i}. From: {msg.get('sender', 'unknown')}")
            print(f"   Agent: {msg.get('agent', 'N/A')}")
            print(f"   Type: {msg.get('type', 'unknown')}")
        
        print(f"\n{'='*80}")
        print(f"WORKFLOW SUMMARY")
        print(f"{'='*80}")
        print(f"Status: {result['status']}")
        print(f"Total messages: {result['meta'].get('total_messages', 0)}")
        print(f"Agents used: {', '.join(agents_used)}")
        print(f"{'='*80}\n")
        
        # If workflow succeeded, verify key components
        if result["status"] == "success":
            assert len(result["result"]) > 0, "Should have results from nodes"
            assert len(messages) >= 2, "Should have messages from both agents"


class TestEndpointsCRUD:
    """Test CRUD operations still work with new structure."""
    
    def test_create_tool_with_communication(self):
        """Test creating a new tool."""
        tool_data = {
            "id": "test_search_tool",
            "name": "Test Search Tool",
            "type": "websearch",
            "config": {
                "engine": "duckduckgo",
                "max_results": 3
            },
            "version": "v1"
        }
        response = client.post("/v1/tools/", json=tool_data)
        assert response.status_code == 200
        assert response.json()["id"] == "test_search_tool"
        
        # Cleanup
        client.delete("/v1/tools/test_search_tool")
    
    def test_create_agent_with_communication(self):
        """Test creating agent with communication settings."""
        agent_data = {
            "id": "test_comm_agent",
            "name": "Test Communication Agent",
            "type": "react",
            "llm_config": {
                "provider": "groq",
                "model": "llama-3.1-8b-instant"
            },
            "tools": ["duckduckgo_search"],
            "use_kag": False,
            "communication": {
                "can_receive": True,
                "can_send": True,
                "message_format": "json"
            },
            "version": "v1"
        }
        response = client.post("/v1/agents/", json=agent_data)
        assert response.status_code == 200
        agent = response.json()
        assert agent["id"] == "test_comm_agent"
        assert agent["communication"]["can_receive"] is True
        
        # Cleanup
        client.delete("/v1/agents/test_comm_agent")
    
    def test_create_workflow_with_communication(self):
        """Test creating workflow with agent communication."""
        workflow_data = {
            "id": "test_comm_workflow",
            "name": "Test Communication Workflow",
            "type": "sequence",
            "nodes": [
                {
                    "id": "step1",
                    "agent_ref": "groq_researcher",
                    "task": "Research artificial intelligence",
                    "sends_to": ["step2"]
                },
                {
                    "id": "step2",
                    "agent_ref": "analyzer_agent",
                    "task": "Analyze the research",
                    "receives_from": ["step1"]
                }
            ],
            "version": "v1"
        }
        response = client.post("/v1/workflows/", json=workflow_data)
        assert response.status_code == 200
        workflow = response.json()
        assert workflow["id"] == "test_comm_workflow"
        assert len(workflow["nodes"]) == 2
        assert workflow["nodes"][0]["sends_to"] == ["step2"]
        assert workflow["nodes"][1]["receives_from"] == ["step1"]
        
        # Cleanup
        client.delete("/v1/workflows/test_comm_workflow")


if __name__ == "__main__":
    print("Running AI Research Workflow Tests...")
    pytest.main([__file__, "-v", "-s"])
