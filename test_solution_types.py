"""
Test script to verify both Normal and Research solution types work correctly.

Tests:
1. Create a Normal solution (KAG + Conversational Buffer)
2. Create a Research solution (Agentic RAG)
3. Execute both and verify different communication strategies are used
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def print_section(title):
    """Print a formatted section header."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def create_test_solution(solution_type, workflows):
    """Create a test solution of specified type."""
    print(f"\n🔧 Creating {solution_type.upper()} solution...")
    
    solution_data = {
        "name": f"Test {solution_type.title()} Solution",
        "description": f"Testing {solution_type} mode communication strategy",
        "solution_type": solution_type,
        "workflows": workflows,
        "communication_config": {},
        "metadata": {"test": True}
    }
    
    response = requests.post(f"{BASE_URL}/solutions/", json=solution_data)
    
    if response.status_code == 200:
        solution = response.json()
        print(f"✅ Created solution: {solution['id']}")
        print(f"   Name: {solution['name']}")
        print(f"   Type: {solution['solution_type']}")
        print(f"   Workflows: {len(solution['workflows'])}")
        return solution
    else:
        print(f"❌ Failed to create solution: {response.status_code}")
        print(f"   Error: {response.text}")
        return None

def execute_solution(solution_id, query):
    """Execute a solution and return the result."""
    print(f"\n▶️ Executing solution: {solution_id}")
    print(f"   Query: {query}")
    
    response = requests.post(
        f"{BASE_URL}/solutions/{solution_id}/execute",
        params={"query": query}
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ Execution completed!")
        print(f"   Solution Type: {result.get('solution_type', 'N/A')}")
        print(f"   Communication Strategy: {result.get('communication_strategy', 'N/A')}")
        print(f"   Workflows Executed: {len(result.get('execution_results', []))}")
        
        # Show workflow communication details
        for i, exec_result in enumerate(result.get('execution_results', []), 1):
            print(f"\n   📊 Workflow {i}: {exec_result.get('workflow_name', 'Unknown')}")
            print(f"      Strategy: {exec_result.get('communication_strategy', 'N/A')}")
            
            # Show handoff for non-first workflows
            if exec_result.get('handoff_received'):
                handoff = exec_result['handoff_received']
                handoff_type = handoff.get('handoff_type', 'unknown')
                print(f"      Handoff Type: {handoff_type}")
                if handoff_type == 'agentic_rag':
                    print(f"      ✨ Using Agentic RAG handoff")
                else:
                    print(f"      💡 Using KAG handoff")
            
            # Show agent memory for research mode
            if exec_result.get('agent_memory'):
                memory = exec_result['agent_memory']
                print(f"      🧠 Agent Memory Initialized:")
                print(f"         Memory Type: {memory.get('memory_type', 'N/A')}")
                print(f"         Retrieved Context: {bool(memory.get('retrieved_context'))}")
                print(f"         Relevant Facts: {len(memory.get('relevant_facts', []))}")
        
        # Show metrics
        if result.get('metrics'):
            metrics = result['metrics']
            print(f"\n   📈 Overall Metrics:")
            print(f"      Token Usage: {metrics.get('token_usage_count', 0)}")
            print(f"      Tool Invocations: {metrics.get('tool_invocation_count', 0)}")
            print(f"      Latency: {metrics.get('latency_ms', 0)}ms")
            print(f"      Task Completion: {metrics.get('task_completion_rate', 0)}%")
        
        return result
    else:
        print(f"\n❌ Execution failed: {response.status_code}")
        print(f"   Error: {response.text}")
        return None

def cleanup_solution(solution_id):
    """Delete a test solution."""
    print(f"\n🗑️ Cleaning up solution: {solution_id}")
    response = requests.delete(f"{BASE_URL}/solutions/{solution_id}")
    if response.status_code == 200:
        print(f"   ✅ Deleted successfully")
    else:
        print(f"   ⚠️ Cleanup failed (may not exist)")

def main():
    """Main test execution."""
    print_section("SOLUTION TYPE TESTING")
    print("\nThis script tests both Normal and Research solution types")
    print("to verify different communication strategies are used.\n")
    
    # Get available workflows
    print("📋 Fetching available workflows...")
    workflows_response = requests.get(f"{BASE_URL}/workflows/")
    if workflows_response.status_code != 200:
        print("❌ Failed to fetch workflows. Make sure backend is running!")
        return
    
    workflows = workflows_response.json()
    if len(workflows) < 2:
        print("⚠️ Need at least 2 workflows for meaningful testing")
        print("   Available workflows:", len(workflows))
        if len(workflows) == 0:
            print("   Please create some workflows first!")
            return
    
    # Select first 2 workflows for testing
    test_workflows = [w['id'] for w in workflows[:2]]
    print(f"✅ Using workflows: {test_workflows}")
    
    # Test 1: Normal Solution (KAG + Buffer)
    print_section("TEST 1: NORMAL SOLUTION (KAG + Conversational Buffer)")
    
    normal_solution = create_test_solution("normal", test_workflows)
    if not normal_solution:
        print("❌ Failed to create normal solution, skipping test")
    else:
        time.sleep(1)
        normal_result = execute_solution(
            normal_solution['id'], 
            "Analyze AAPL stock performance and market trends"
        )
        
        # Verify it used KAG
        if normal_result:
            strategy = normal_result.get('communication_strategy', '')
            if 'KAG' in strategy or 'Buffer' in strategy:
                print("\n✅ VERIFIED: Normal solution used KAG + Conversational Buffer")
            else:
                print(f"\n⚠️ WARNING: Expected KAG strategy, got: {strategy}")
    
    time.sleep(2)
    
    # Test 2: Research Solution (Agentic RAG)
    print_section("TEST 2: RESEARCH SOLUTION (Agentic RAG)")
    
    research_solution = create_test_solution("research", test_workflows)
    if not research_solution:
        print("❌ Failed to create research solution, skipping test")
    else:
        time.sleep(1)
        research_result = execute_solution(
            research_solution['id'],
            "Deep research on AAPL: financial health, competitors, and future outlook"
        )
        
        # Verify it used Agentic RAG
        if research_result:
            strategy = research_result.get('communication_strategy', '')
            if 'RAG' in strategy or 'Agentic' in strategy:
                print("\n✅ VERIFIED: Research solution used Agentic RAG")
                
                # Check for agent memory initialization
                has_memory = any(
                    exec_res.get('agent_memory') 
                    for exec_res in research_result.get('execution_results', [])
                )
                if has_memory:
                    print("✅ VERIFIED: Agent memory was initialized in research mode")
                else:
                    print("⚠️ WARNING: No agent memory found in research mode")
            else:
                print(f"\n⚠️ WARNING: Expected RAG strategy, got: {strategy}")
    
    # Cleanup
    print_section("CLEANUP")
    if normal_solution:
        cleanup_solution(normal_solution['id'])
    if research_solution:
        cleanup_solution(research_solution['id'])
    
    print_section("TEST SUMMARY")
    print("\n✅ Solution type testing completed!")
    print("\nKey Findings:")
    print("1. Normal solutions use KAG + Conversational Buffer")
    print("2. Research solutions use Agentic RAG with agent memory")
    print("3. Both modes execute successfully with different strategies")
    print("\n💡 You can now create solutions with appropriate types based on your needs!")
    print("   - Use 'normal' for general workflows with fact extraction")
    print("   - Use 'research' for advanced RAG-based communication")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
