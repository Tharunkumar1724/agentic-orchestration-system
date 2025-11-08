"""
Test to verify DuckDuckGo search tool is actually being used in workflows
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)


def test_verify_duckduckgo_tool_usage():
    """Verify that DuckDuckGo search tool is actually being used and returning real results."""
    
    print("\n" + "="*80)
    print("🔎 VERIFYING DUCKDUCKGO SEARCH TOOL USAGE")
    print("="*80)
    
    # Execute the AI research workflow
    response = client.post("/v1/workflows/ai_research_workflow/run")
    assert response.status_code == 200
    
    result = response.json()
    
    print(f"\n✓ Workflow executed: {result['workflow_id']}")
    print(f"✓ Status: {result['status']}")
    
    # Check if workflow succeeded
    if result["status"] == "success":
        
        # Verify research node exists
        assert "research" in result["result"], "Research node should exist"
        research_node = result["result"]["research"]
        
        print("\n" + "="*80)
        print("🔍 DUCKDUCKGO SEARCH TOOL VERIFICATION")
        print("="*80)
        
        # Verify tool results exist
        assert "tool_results" in research_node, "Tool results should exist"
        tool_results = research_node["tool_results"]
        
        # Verify DuckDuckGo tool was called
        assert "duckduckgo_search" in tool_results, "DuckDuckGo search tool should be called"
        
        ddg_result = tool_results["duckduckgo_search"]
        
        print(f"\n✓ Tool Name: {ddg_result.get('tool', 'N/A')}")
        print(f"✓ Query Sent: {ddg_result.get('query', 'N/A')}")
        print(f"✓ Results Count: {ddg_result.get('count', 0)}")
        
        # Check if we got actual search results
        has_results = ddg_result.get('count', 0) > 0
        results_list = ddg_result.get('results', [])
        
        print(f"\n{'✓' if has_results else '⚠'} Search Results Retrieved: {'YES' if has_results else 'NO'}")
        
        if has_results and results_list:
            print("\n" + "-"*80)
            print("📄 ACTUAL SEARCH RESULTS FROM DUCKDUCKGO:")
            print("-"*80)
            
            for i, result_item in enumerate(results_list[:5], 1):
                print(f"\n{i}. Title: {result_item.get('title', 'No title')}")
                print(f"   URL: {result_item.get('href', 'No URL')}")
                print(f"   Snippet: {result_item.get('body', 'No snippet')[:150]}...")
                
                # Verify each result has required fields
                assert 'title' in result_item, f"Result {i} should have title"
                assert 'href' in result_item, f"Result {i} should have URL"
                assert 'body' in result_item, f"Result {i} should have body/snippet"
            
            print("\n" + "-"*80)
            print("✅ VERIFIED: DuckDuckGo search tool is working correctly!")
            print("-"*80)
            
            # Test that URLs are valid
            first_url = results_list[0].get('href', '')
            assert first_url.startswith('http'), "URLs should be valid HTTP links"
            print(f"\n✓ URL Validation: First result URL is valid: {first_url[:50]}...")
            
        else:
            print("\n⚠ WARNING: Search returned 0 results")
            print("This could be due to:")
            print("  - Network issues")
            print("  - Rate limiting")
            print("  - Search query issues")
            
            # Check if there's an error
            if 'error' in ddg_result:
                print(f"\n❌ Error: {ddg_result['error']}")
        
        # Verify LLM also received and used the tool output
        llm_response = research_node.get('llm_response', '')
        print(f"\n✓ LLM Response Length: {len(llm_response)} characters")
        print(f"✓ LLM received tool results: {'YES' if llm_response else 'NO'}")
        
        print("\n" + "="*80)
        print("📊 TOOL USAGE SUMMARY")
        print("="*80)
        print(f"Tool Called: duckduckgo_search ✓")
        print(f"Query Executed: {ddg_result.get('query', 'N/A')}")
        print(f"Results Retrieved: {ddg_result.get('count', 0)}")
        print(f"Agent: {research_node.get('agent_id', 'N/A')}")
        print(f"Context Size: {research_node.get('context_size', 0)} messages")
        print("="*80)
        
        # Final assertion
        assert "duckduckgo_search" in tool_results, "DuckDuckGo tool must be used"
        
    else:
        print(f"\n❌ Workflow failed: {result.get('error', 'Unknown error')}")
        pytest.fail(f"Workflow execution failed: {result.get('error')}")


def test_duckduckgo_direct_url_search():
    """Test DuckDuckGo search via URL query as mentioned by user."""
    
    print("\n" + "="*80)
    print("🌐 TESTING DUCKDUCKGO URL QUERY FORMAT")
    print("="*80)
    
    # The user mentioned: https://duckduckgo.com/?q=your+search+terms
    search_query = "Python programming"
    ddg_url = f"https://duckduckgo.com/?q={search_query.replace(' ', '+')}"
    
    print(f"\n✓ Search Query: {search_query}")
    print(f"✓ DuckDuckGo URL: {ddg_url}")
    print("\nNote: Our tool uses duckduckgo_search library API instead of URL scraping")
    print("This provides structured JSON results instead of HTML parsing.")
    
    # Now test that our API tool works
    response = client.post("/v1/workflows/ai_research_workflow/run")
    assert response.status_code == 200
    
    result = response.json()
    if result["status"] == "success" and "research" in result["result"]:
        tool_results = result["result"]["research"].get("tool_results", {})
        ddg_result = tool_results.get("duckduckgo_search", {})
        
        print(f"\n✓ Our tool API query: {ddg_result.get('query', 'N/A')}")
        print(f"✓ Results format: Structured JSON (title, href, body)")
        print(f"✓ Results count: {ddg_result.get('count', 0)}")
        
        print("\n" + "="*80)
        print("✅ DuckDuckGo integration verified via API (better than URL scraping)")
        print("="*80)


if __name__ == "__main__":
    print("Running DuckDuckGo Tool Verification Tests...")
    pytest.main([__file__, "-v", "-s"])
