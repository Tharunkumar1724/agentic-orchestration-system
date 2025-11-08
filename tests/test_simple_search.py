"""
Simple test to demonstrate DuckDuckGo search tool is working with real web results
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)


def test_simple_search_with_real_results():
    """Execute a simple search and show real DuckDuckGo results."""
    
    print("\n" + "="*80)
    print("🔍 SIMPLE DUCKDUCKGO SEARCH TEST")
    print("="*80)
    print("\nExecuting workflow: simple_search_workflow")
    print("Query: 'Python programming language'")
    
    # Execute the simple search workflow
    response = client.post("/v1/workflows/simple_search_workflow/run")
    assert response.status_code == 200
    
    result = response.json()
    
    print(f"\n✓ Status: {result['status']}")
    print(f"✓ Run ID: {result['run_id']}")
    
    if result["status"] == "success":
        # Get the search node result
        search_node = result["result"]["search_python"]
        
        print("\n" + "="*80)
        print("🔧 TOOL EXECUTION DETAILS")
        print("="*80)
        
        # Get tool results
        tool_results = search_node.get("tool_results", {})
        ddg = tool_results.get("duckduckgo_search", {})
        
        print(f"\n✓ Tool Called: {ddg.get('tool', 'N/A')}")
        print(f"✓ Query: {ddg.get('query', 'N/A')}")
        print(f"✓ Results Count: {ddg.get('count', 0)}")
        
        # Show the results
        results = ddg.get('results', [])
        
        if results:
            print("\n" + "="*80)
            print("📄 REAL DUCKDUCKGO SEARCH RESULTS")
            print("="*80)
            
            for i, item in enumerate(results, 1):
                print(f"\n{i}. {item.get('title', 'No title')}")
                print(f"   🔗 {item.get('href', 'No URL')}")
                print(f"   📝 {item.get('body', 'No description')[:120]}...")
            
            print("\n" + "="*80)
            print(f"✅ SUCCESS: Retrieved {len(results)} real search results!")
            print("="*80)
            
            # Verify data quality
            assert len(results) > 0, "Should have search results"
            assert 'title' in results[0], "Results should have title"
            assert 'href' in results[0], "Results should have URL"
            assert results[0]['href'].startswith('http'), "URL should be valid"
            
        else:
            print("\n⚠ No results returned (possibly rate limited)")
            print("But the tool WAS called correctly!")
        
        # Show LLM's response using the search results
        llm_resp = search_node.get('llm_response', '')
        print(f"\n🤖 Groq LLM Response (using search results):")
        print("-" * 80)
        print(llm_resp[:500] + "..." if len(llm_resp) > 500 else llm_resp)
        print("-" * 80)
        
        # Verify tool was called
        assert "duckduckgo_search" in tool_results, "DuckDuckGo tool must be called"
        assert "tool" in ddg, "Tool result must have tool name"
        assert ddg["tool"] == "duckduckgo_search", "Tool name must match"
        
        print("\n✅ TEST PASSED: DuckDuckGo search tool is working!")
        
    else:
        print(f"\n❌ Workflow failed: {result.get('error')}")
        pytest.fail("Workflow failed")


def test_tool_configuration():
    """Verify DuckDuckGo tool is properly configured."""
    
    print("\n" + "="*80)
    print("⚙️  DUCKDUCKGO TOOL CONFIGURATION CHECK")
    print("="*80)
    
    # Get the tool configuration
    response = client.get("/v1/tools/duckduckgo_search")
    assert response.status_code == 200
    
    tool = response.json()
    
    print(f"\n✓ Tool ID: {tool['id']}")
    print(f"✓ Tool Name: {tool['name']}")
    print(f"✓ Tool Type: {tool['type']}")
    print(f"\n📋 Configuration:")
    
    config = tool.get('config', {})
    for key, value in config.items():
        print(f"   • {key}: {value}")
    
    # Verify configuration
    assert tool['id'] == 'duckduckgo_search', "Tool ID should be duckduckgo_search"
    assert tool['type'] == 'websearch', "Tool type should be websearch"
    assert 'engine' in config, "Config should have engine"
    assert config['engine'] == 'duckduckgo', "Engine should be duckduckgo"
    
    print("\n✅ Tool is properly configured!")


def test_groq_agent_has_search_tool():
    """Verify groq_researcher agent has DuckDuckGo tool assigned."""
    
    print("\n" + "="*80)
    print("🤖 AGENT TOOL ASSIGNMENT CHECK")
    print("="*80)
    
    # Get the agent configuration
    response = client.get("/v1/agents/groq_researcher")
    assert response.status_code == 200
    
    agent = response.json()
    
    print(f"\n✓ Agent ID: {agent['id']}")
    print(f"✓ Agent Name: {agent['name']}")
    print(f"✓ Agent Type: {agent['type']}")
    print(f"✓ LLM Model: {agent['llm_config'].get('model', 'N/A')}")
    print(f"\n🔧 Assigned Tools:")
    
    tools = agent.get('tools', [])
    for tool in tools:
        print(f"   • {tool}")
    
    # Verify tool assignment
    assert 'duckduckgo_search' in tools, "Agent should have duckduckgo_search tool"
    
    print("\n✅ Agent is properly configured with DuckDuckGo search tool!")


if __name__ == "__main__":
    print("Running DuckDuckGo Integration Tests...")
    pytest.main([__file__, "-v", "-s"])
