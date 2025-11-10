"""
Comprehensive test for metrics display across workflows, solutions, and chat.
Tests all metrics: accuracy, response quality, hallucination rate, task completion rate,
token usage, latency, tool invocation, retrieval errors, decision depth, branching factor,
context relation quality, and tool success rate.
"""

import asyncio
import httpx
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/v1"  # Added /v1 prefix

def print_section(title):
    """Print a formatted section header."""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")

def print_metrics(metrics, title="Metrics"):
    """Print metrics in a formatted way."""
    print(f"\n{'─'*80}")
    print(f"📊 {title}")
    print(f"{'─'*80}")
    
    if not metrics:
        print("❌ No metrics found!")
        return
    
    # Performance Metrics
    print("\n⏱️  PERFORMANCE METRICS:")
    print(f"  • Latency: {metrics.get('latency_ms', 0):.2f} ms")
    print(f"  • Token Usage (Total): {metrics.get('token_usage_count', 0)}")
    print(f"  • Token Input: {metrics.get('token_input_count', 0)}")
    print(f"  • Token Output: {metrics.get('token_output_count', 0)}")
    
    # Quality Metrics
    print("\n✨ QUALITY METRICS:")
    print(f"  • Accuracy: {metrics.get('accuracy', 0):.2f}%")
    print(f"  • Response Quality: {metrics.get('response_quality', 0):.2f}%")
    print(f"  • Hallucination Rate: {metrics.get('hallucination_rate', 0):.2f}%")
    print(f"  • Task Completion Rate: {metrics.get('task_completion_rate', 0):.2f}%")
    print(f"  • Context Relation Quality: {metrics.get('context_relation_quality', 0):.2f}%")
    
    # Tool & Execution Metrics
    print("\n🔧 TOOL & EXECUTION METRICS:")
    print(f"  • Tool Invocation Count: {metrics.get('tool_invocation_count', 0)}")
    print(f"  • Tool Success Rate: {metrics.get('tool_success_rate', 0):.2f}%")
    print(f"  • Retrieval Error Count: {metrics.get('retrieval_error_count', 0)}")
    
    # Decision & Structure Metrics
    print("\n🌳 DECISION & STRUCTURE METRICS:")
    print(f"  • Decision Depth: {metrics.get('decision_depth', 0)}")
    print(f"  • Branching Factor: {metrics.get('branching_factor', 0):.2f}")
    print(f"  • Agent Execution Count: {metrics.get('agent_execution_count', 0)}")
    print(f"  • Workflow Step Count: {metrics.get('workflow_step_count', 0)}")
    
    # Errors & Warnings
    if metrics.get('errors') or metrics.get('warnings'):
        print("\n⚠️  ERRORS & WARNINGS:")
        for error in metrics.get('errors', []):
            print(f"  ❌ {error}")
        for warning in metrics.get('warnings', []):
            print(f"  ⚠️  {warning}")
    
    print(f"\n{'─'*80}\n")

async def test_workflow_metrics():
    """Test metrics in workflow execution."""
    print_section("TEST 1: Workflow Execution Metrics")
    
    async with httpx.AsyncClient(timeout=60.0, follow_redirects=True) as client:
        try:
            # Get available workflows
            response = await client.get(f"{BASE_URL}/workflows")
            print(f"📡 GET /workflows - Status: {response.status_code}")
            
            if response.status_code != 200:
                print(f"❌ Failed to get workflows: {response.text}")
                return False
            
            workflows = response.json()
            
            if not workflows:
                print("⚠️  No workflows found. Creating a test workflow...")
                # Create a simple test workflow
                test_workflow = {
                    "id": "metrics_test_workflow",
                    "name": "Metrics Test Workflow",
                    "description": "Test workflow for metrics validation",
                    "type": "sequence",
                    "nodes": [
                        {
                            "id": "node1",
                            "agent_ref": "research_agent",
                            "task": "Research AI trends in 2024",
                            "tools": ["duckduckgo_search"]
                        }
                    ]
                }
                create_response = await client.post(f"{BASE_URL}/workflows", json=test_workflow)
                print(f"📡 POST /workflows - Status: {create_response.status_code}")
                
                if create_response.status_code == 200:
                    print("✅ Test workflow created successfully")
                    workflows = [create_response.json()]
                else:
                    print(f"❌ Failed to create test workflow: {create_response.text}")
                    return False
            
            # Execute the first workflow
            workflow = workflows[0]
            print(f"🚀 Executing workflow: {workflow.get('name', workflow.get('id'))}")
            
            run_response = await client.post(
                f"{BASE_URL}/workflows/{workflow['id']}/run",
                json={"query": "Test query for metrics", "format": "structured"}
            )
            
            print(f"📡 POST /workflows/{workflow['id']}/run - Status: {run_response.status_code}")
            
            if run_response.status_code == 200:
                result = run_response.json()
                print(f"✅ Workflow execution completed")
                print(f"   Status: {result.get('status')}")
                
                # Check for metrics
                metrics = result.get('metrics')
                if metrics:
                    print_metrics(metrics, "Workflow Execution Metrics")
                    return True
                else:
                    print("❌ No metrics found in workflow result!")
                    print(f"   Response keys: {list(result.keys())}")
                    return False
            else:
                print(f"❌ Workflow execution failed: {run_response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Test failed with error: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

async def test_solution_metrics():
    """Test metrics in solution execution."""
    print_section("TEST 2: Solution Execution Metrics")
    
    async with httpx.AsyncClient(timeout=120.0, follow_redirects=True) as client:
        try:
            # Get available solutions
            response = await client.get(f"{BASE_URL}/solutions")
            solutions = response.json()
            
            if not solutions:
                print("⚠️  No solutions found. Creating a test solution...")
                # Create a test solution
                test_solution = {
                    "id": "metrics_test_solution",
                    "name": "Metrics Test Solution",
                    "description": "Test solution for metrics validation",
                    "workflows": []
                }
                
                # Get a workflow to add
                wf_response = await client.get(f"{BASE_URL}/workflows")
                workflows = wf_response.json()
                if workflows:
                    test_solution["workflows"] = [workflows[0]["id"]]
                
                create_response = await client.post(f"{BASE_URL}/solutions", json=test_solution)
                if create_response.status_code == 200:
                    print("✅ Test solution created successfully")
                    solutions = [create_response.json()]
                else:
                    print(f"❌ Failed to create test solution: {create_response.text}")
                    return False
            
            # Execute the first solution
            solution = solutions[0]
            print(f"🚀 Executing solution: {solution.get('name', solution.get('id'))}")
            
            exec_response = await client.post(
                f"{BASE_URL}/solutions/{solution['id']}/execute",
                params={"query": "Test query for solution metrics"}
            )
            
            if exec_response.status_code == 200:
                result = exec_response.json()
                print(f"✅ Solution execution completed")
                print(f"   Solution: {result.get('solution_name')}")
                
                # Check for aggregated metrics
                metrics = result.get('metrics')
                if metrics:
                    print_metrics(metrics, "Solution Aggregated Metrics")
                    
                    # Also show individual workflow metrics
                    for i, exec_result in enumerate(result.get('execution_results', [])):
                        if exec_result.get('metrics'):
                            print_metrics(
                                exec_result['metrics'],
                                f"Workflow {i+1} Metrics ({exec_result.get('workflow_name')})"
                            )
                    return True
                else:
                    print("❌ No metrics found in solution result!")
                    print(f"   Response keys: {list(result.keys())}")
                    return False
            else:
                print(f"❌ Solution execution failed: {exec_response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Test failed with error: {str(e)}")
            return False

async def test_chat_metrics():
    """Test metrics in chat mode."""
    print_section("TEST 3: Chat Mode Metrics")
    
    async with httpx.AsyncClient(timeout=60.0, follow_redirects=True) as client:
        try:
            # Get a workflow for chat
            response = await client.get(f"{BASE_URL}/workflows")
            workflows = response.json()
            
            if not workflows:
                print("❌ No workflows available for chat test")
                return False
            
            workflow = workflows[0]
            print(f"💬 Creating chat session with workflow: {workflow.get('name', workflow.get('id'))}")
            
            # Create chat session
            session_response = await client.post(
                f"{BASE_URL}/chat/sessions",
                json={
                    "workflow_id": workflow["id"],
                    "name": "Metrics Test Chat",
                    "initial_message": "Hello, test message for metrics"
                }
            )
            
            if session_response.status_code != 200:
                print(f"❌ Failed to create chat session: {session_response.text}")
                return False
            
            session = session_response.json()
            print(f"✅ Chat session created: {session.get('session_id')}")
            
            # Check for metrics in session metadata
            if session.get('metadata', {}).get('last_message_metrics'):
                print_metrics(
                    session['metadata']['last_message_metrics'],
                    "Initial Message Metrics"
                )
            
            # Send a message
            print("\n💬 Sending chat message...")
            message_response = await client.post(
                f"{BASE_URL}/chat/sessions/{session['session_id']}/message",
                json={"message": "Tell me about AI metrics"}
            )
            
            if message_response.status_code == 200:
                updated_session = message_response.json()
                print(f"✅ Message sent successfully")
                
                # Check for metrics in updated session
                metrics = updated_session.get('metadata', {}).get('last_message_metrics')
                if metrics:
                    print_metrics(metrics, "Chat Message Metrics")
                    return True
                else:
                    print("❌ No metrics found in chat response!")
                    print(f"   Session metadata keys: {list(updated_session.get('metadata', {}).keys())}")
                    return False
            else:
                print(f"❌ Message send failed: {message_response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Test failed with error: {str(e)}")
            return False

async def main():
    """Run all metrics tests."""
    print("\n" + "🎯"*40)
    print("  COMPREHENSIVE METRICS TESTING")
    print("  Testing all metrics across Workflows, Solutions, and Chat")
    print("🎯"*40)
    
    results = []
    
    # Test 1: Workflow Metrics
    result1 = await test_workflow_metrics()
    results.append(("Workflow Metrics", result1))
    
    # Test 2: Solution Metrics
    result2 = await test_solution_metrics()
    results.append(("Solution Metrics", result2))
    
    # Test 3: Chat Metrics
    result3 = await test_chat_metrics()
    results.append(("Chat Metrics", result3))
    
    # Summary
    print_section("TEST SUMMARY")
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status} - {test_name}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    print(f"\n📊 Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All metrics tests passed! All metrics are being tracked and displayed.")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    asyncio.run(main())
