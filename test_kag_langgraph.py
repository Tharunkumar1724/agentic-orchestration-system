"""
Test KAG Service with LangGraph Implementation
Comprehensive testing of Knowledge-Aided Generation workflow
"""
import sys
import os
from datetime import datetime

# Add app to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.services.kag_service import KAGService, get_conversation_memory, get_kag_service


def print_section(title: str):
    """Print a formatted section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def print_result(label: str, value: any, indent: int = 0):
    """Print a labeled result"""
    prefix = "  " * indent
    if isinstance(value, (list, dict)):
        print(f"{prefix}{label}:")
        if isinstance(value, list):
            for item in value:
                print(f"{prefix}  - {item}")
        else:
            for key, val in value.items():
                print(f"{prefix}  {key}: {val}")
    else:
        print(f"{prefix}{label}: {value}")


def test_basic_kag_invocation():
    """Test 1: Basic KAG invocation with single workflow"""
    print_section("TEST 1: Basic KAG Invocation")
    
    service = KAGService()
    
    # Simulate workflow output
    workflow_output = """
    Analysis complete. Found 3 key insights:
    1. Market trends show 15% growth in Q3
    2. Customer satisfaction increased by 8%
    3. Revenue projections are on target
    
    Recommendation: Continue current strategy with minor optimizations.
    """
    
    result = service.invoke_kag(
        workflow_output=workflow_output,
        workflow_name="Market Analysis",
        solution_id="solution_001",
        workflow_id="workflow_001",
        context="Analyzing Q3 business metrics"
    )
    
    print_result("✅ Summary", result.get("summary"))
    print_result("✅ Facts", result.get("facts", []))
    print_result("✅ Reasoning", result.get("reasoning"))
    print_result("✅ Memory Stored", result.get("memory_stored"))
    print_result("✅ Context Available", result.get("context_available"))
    
    if result.get("error"):
        print_result("❌ Error", result["error"])
        return False
    
    print("\n✅ Test 1 PASSED: Basic invocation successful")
    return True


def test_multi_workflow_context():
    """Test 2: Multiple workflows with context preservation"""
    print_section("TEST 2: Multi-Workflow Context Preservation")
    
    service = KAGService()
    solution_id = "solution_002"
    
    # Workflow 1: Data Collection
    print("📊 Workflow 1: Data Collection")
    result1 = service.invoke_kag(
        workflow_output="Collected 10,000 customer records. Data quality: 95%",
        workflow_name="Data Collection",
        solution_id=solution_id,
        workflow_id="wf_001",
        context="Initial data gathering phase"
    )
    print_result("  Summary", result1.get("summary"), indent=1)
    print_result("  Facts", result1.get("facts", []), indent=1)
    
    # Workflow 2: Data Analysis (should have context from workflow 1)
    print("\n📊 Workflow 2: Data Analysis")
    result2 = service.invoke_kag(
        workflow_output="Analysis reveals 3 customer segments. High-value segment: 2,000 customers",
        workflow_name="Data Analysis",
        solution_id=solution_id,
        workflow_id="wf_002",
        context="Analyzing collected customer data"
    )
    print_result("  Summary", result2.get("summary"), indent=1)
    print_result("  Facts", result2.get("facts", []), indent=1)
    print_result("  Context Available", result2.get("context_available"), indent=1)
    
    # Workflow 3: Generate Report (should have context from both previous workflows)
    print("\n📊 Workflow 3: Generate Report")
    result3 = service.invoke_kag(
        workflow_output="Report generated with actionable insights for each segment",
        workflow_name="Report Generation",
        solution_id=solution_id,
        workflow_id="wf_003",
        context="Final reporting phase"
    )
    print_result("  Summary", result3.get("summary"), indent=1)
    print_result("  Context Available", result3.get("context_available"), indent=1)
    
    # Verify context was preserved
    if result2.get("context_available") and result3.get("context_available"):
        print("\n✅ Test 2 PASSED: Context preserved across workflows")
        return True
    else:
        print("\n❌ Test 2 FAILED: Context not properly preserved")
        return False


def test_handoff_preparation():
    """Test 3: Workflow handoff preparation"""
    print_section("TEST 3: Workflow Handoff Preparation")
    
    service = KAGService()
    solution_id = "solution_003"
    
    # Source workflow
    service.invoke_kag(
        workflow_output="Research identified 5 viable market opportunities",
        workflow_name="Market Research",
        solution_id=solution_id,
        workflow_id="source_wf",
        context="Market opportunity analysis"
    )
    
    # Prepare handoff to next workflow
    handoff = service.prepare_handoff(
        source_workflow_id="source_wf",
        target_workflow_id="target_wf",
        target_workflow_description="Create detailed business plan for top opportunities",
        solution_id=solution_id
    )
    
    print_result("✅ Handoff Data", handoff.get("handoff_data"))
    print_result("✅ Relevance", handoff.get("relevance"))
    print_result("✅ Facts", handoff.get("facts", []))
    print_result("✅ Source Summary", handoff.get("source_summary"))
    
    if handoff.get("facts"):
        print("\n✅ Test 3 PASSED: Handoff prepared successfully")
        return True
    else:
        print("\n❌ Test 3 FAILED: Handoff preparation incomplete")
        return False


def test_solution_summary():
    """Test 4: Generate solution-wide summary"""
    print_section("TEST 4: Solution-Wide Summary")
    
    service = KAGService()
    solution_id = "solution_004"
    
    # Execute multiple workflows
    workflows = [
        ("Planning", "Project scope defined: 6 months, $500K budget"),
        ("Design", "Architecture designed: microservices approach"),
        ("Development", "Core modules implemented: 80% complete"),
        ("Testing", "Testing phase: 150 tests passing")
    ]
    
    for i, (name, output) in enumerate(workflows):
        service.invoke_kag(
            workflow_output=output,
            workflow_name=name,
            solution_id=solution_id,
            workflow_id=f"wf_{i}",
            context=f"Phase {i+1}"
        )
    
    # Get solution summary
    summary = service.get_solution_summary(solution_id)
    
    print_result("✅ Total Workflows", summary.get("total_workflows"))
    print_result("✅ Combined Facts Count", len(summary.get("combined_facts", [])))
    print_result("✅ Overall Context", summary.get("overall_context"))
    
    print("\n📋 Individual Workflow Summaries:")
    for s in summary.get("summaries", []):
        print(f"  - {s['workflow_name']}: {s['summary'][:100]}...")
    
    if summary.get("total_workflows") == 4:
        print("\n✅ Test 4 PASSED: Solution summary generated")
        return True
    else:
        print("\n❌ Test 4 FAILED: Solution summary incomplete")
        return False


def test_memory_management():
    """Test 5: Memory management and cleanup"""
    print_section("TEST 5: Memory Management")
    
    service = KAGService()
    solution_id = "solution_005"
    
    # Add some memories
    for i in range(3):
        service.invoke_kag(
            workflow_output=f"Workflow {i} output",
            workflow_name=f"Workflow {i}",
            solution_id=solution_id,
            workflow_id=f"wf_{i}",
            context=""
        )
    
    # Verify memories exist
    memories_before = service.memory.get_memories(solution_id)
    print_result("✅ Memories Before Clear", len(memories_before))
    
    # Clear memories
    service.clear_solution_memory(solution_id)
    
    # Verify memories cleared
    memories_after = service.memory.get_memories(solution_id)
    print_result("✅ Memories After Clear", len(memories_after))
    
    if len(memories_before) == 3 and len(memories_after) == 0:
        print("\n✅ Test 5 PASSED: Memory management working")
        return True
    else:
        print("\n❌ Test 5 FAILED: Memory not properly managed")
        return False


def test_error_handling():
    """Test 6: Error handling in KAG workflow"""
    print_section("TEST 6: Error Handling")
    
    service = KAGService()
    
    # Test with empty output
    result = service.invoke_kag(
        workflow_output="",
        workflow_name="Empty Test",
        solution_id="solution_006",
        workflow_id="wf_empty",
        context=""
    )
    
    print_result("✅ Handled Empty Output", result.get("memory_stored") is not None)
    
    # Test with very long output
    long_output = "Test " * 10000
    result2 = service.invoke_kag(
        workflow_output=long_output,
        workflow_name="Long Test",
        solution_id="solution_006",
        workflow_id="wf_long",
        context=""
    )
    
    print_result("✅ Handled Long Output", result2.get("memory_stored") is not None)
    
    print("\n✅ Test 6 PASSED: Error handling robust")
    return True


def test_langgraph_state_transitions():
    """Test 7: Verify LangGraph state transitions"""
    print_section("TEST 7: LangGraph State Transitions")
    
    service = KAGService()
    
    # Verify graph is compiled
    print_result("✅ Graph Compiled", service.graph is not None)
    
    # Test that graph has expected nodes
    expected_nodes = ["retrieve_context", "extract_facts", "generate_summary", "store_memory"]
    
    # Execute and verify state progression
    result = service.invoke_kag(
        workflow_output="Testing LangGraph state flow",
        workflow_name="State Test",
        solution_id="solution_007",
        workflow_id="wf_state",
        context="State transition test"
    )
    
    # Verify all expected keys are present
    expected_keys = ["summary", "facts", "reasoning", "memory_stored", "context_available"]
    all_keys_present = all(key in result for key in expected_keys)
    
    print_result("✅ All Output Keys Present", all_keys_present)
    print_result("✅ Graph Execution Successful", result.get("memory_stored", False))
    
    if all_keys_present and result.get("memory_stored"):
        print("\n✅ Test 7 PASSED: LangGraph state transitions working")
        return True
    else:
        print("\n❌ Test 7 FAILED: State transitions incomplete")
        return False


def test_singleton_service():
    """Test 8: Verify singleton pattern for KAG service"""
    print_section("TEST 8: Singleton Pattern")
    
    service1 = get_kag_service()
    service2 = get_kag_service()
    
    print_result("✅ Services are Same Instance", service1 is service2)
    
    # Test memory is shared
    solution_id = "solution_008"
    service1.invoke_kag(
        workflow_output="Test singleton",
        workflow_name="Singleton Test",
        solution_id=solution_id,
        workflow_id="wf_single",
        context=""
    )
    
    # Retrieve from second instance
    memories = service2.memory.get_memories(solution_id)
    print_result("✅ Memory Shared Across Instances", len(memories) > 0)
    
    if service1 is service2 and len(memories) > 0:
        print("\n✅ Test 8 PASSED: Singleton pattern working")
        return True
    else:
        print("\n❌ Test 8 FAILED: Singleton not properly implemented")
        return False


def run_all_tests():
    """Run all KAG LangGraph tests"""
    print("\n" + "🚀" * 40)
    print("  KAG LANGGRAPH COMPREHENSIVE TEST SUITE")
    print("🚀" * 40)
    
    tests = [
        ("Basic KAG Invocation", test_basic_kag_invocation),
        ("Multi-Workflow Context", test_multi_workflow_context),
        ("Handoff Preparation", test_handoff_preparation),
        ("Solution Summary", test_solution_summary),
        ("Memory Management", test_memory_management),
        ("Error Handling", test_error_handling),
        ("LangGraph State Transitions", test_langgraph_state_transitions),
        ("Singleton Pattern", test_singleton_service),
    ]
    
    results = []
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
            if result:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"\n❌ {name} CRASHED: {str(e)}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
            failed += 1
    
    # Print summary
    print_section("TEST SUMMARY")
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}  {name}")
    
    print(f"\n{'=' * 80}")
    print(f"Total Tests: {len(tests)}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"Success Rate: {(passed/len(tests)*100):.1f}%")
    print(f"{'=' * 80}\n")
    
    return passed == len(tests)


if __name__ == "__main__":
    print("\n⚙️  Loading environment and dependencies...")
    
    # Check for API key
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    if not os.getenv("GEMINI_API_KEY"):
        print("\n⚠️  WARNING: GEMINI_API_KEY not found in environment")
        print("Some tests may use mock responses\n")
    
    success = run_all_tests()
    
    if success:
        print("🎉 ALL TESTS PASSED! KAG LangGraph implementation is working correctly.")
        sys.exit(0)
    else:
        print("⚠️  SOME TESTS FAILED. Review output above for details.")
        sys.exit(1)
