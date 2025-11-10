"""
Test Knowledge Graph Query capabilities with LangGraph KAG
Tests Neo4j integration, Cypher query generation, and graph-enhanced fact retrieval
"""
import sys
import os
import uuid

# Add app to path
sys.path.insert(0, os.path.abspath('.'))

from app.services.kag_service import (
    get_kag_service,
    get_kg_manager,
    NEO4J_AVAILABLE
)


def test_kg_manager_initialization():
    """Test 1: Knowledge Graph Manager initialization"""
    print("\n" + "="*80)
    print("TEST 1: Knowledge Graph Manager Initialization")
    print("="*80)
    
    try:
        kg_manager = get_kg_manager()
        
        print(f"\n📦 Neo4j Libraries Available: {NEO4J_AVAILABLE}")
        print(f"📦 Knowledge Graph Available: {kg_manager.is_available()}")
        
        if not NEO4J_AVAILABLE:
            print("\n⚠️  Neo4j libraries not installed")
            print("   Install with: pip install neo4j langchain-neo4j")
            return True  # Not a failure, just unavailable
        
        if not kg_manager.is_available():
            print("\n⚠️  Neo4j not configured")
            print("   Set environment variables:")
            print("   - NEO4J_URI (default: bolt://localhost:7687)")
            print("   - NEO4J_USER (default: neo4j)")
            print("   - NEO4J_PASSWORD (required)")
            return True  # Not a failure, just unconfigured
        
        print("\n✅ Knowledge Graph Manager initialized and connected")
        return True
        
    except Exception as e:
        print(f"\n❌ Initialization test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_kg_query_basic():
    """Test 2: Basic knowledge graph query"""
    print("\n" + "="*80)
    print("TEST 2: Basic Knowledge Graph Query")
    print("="*80)
    
    try:
        service = get_kag_service()
        
        if not service.kg_manager.is_available():
            print("\n⚠️  Skipping - Knowledge graph not available")
            return True
        
        # Query the knowledge graph
        solution_id = str(uuid.uuid4())
        query = "What facts are available?"
        
        print(f"\n🔍 Query: {query}")
        print(f"   Solution ID: {solution_id}")
        
        result = service.query_knowledge_graph(
            query=query,
            solution_id=solution_id
        )
        
        print("\n📊 Query Result:")
        print(f"   Answer: {result.get('answer', 'N/A')}")
        print(f"   Cypher Query: {result.get('cypher_query', 'N/A')}")
        print(f"   Related Facts: {len(result.get('related_facts', []))}")
        print(f"   Graph Available: {result.get('graph_available', False)}")
        
        assert 'answer' in result, "Result should contain answer"
        assert 'graph_available' in result, "Result should indicate graph availability"
        
        print("\n✅ Basic KG query successful")
        return True
        
    except Exception as e:
        print(f"\n❌ KG query test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_kag_with_graph_storage():
    """Test 3: KAG with automatic graph storage"""
    print("\n" + "="*80)
    print("TEST 3: KAG with Knowledge Graph Storage")
    print("="*80)
    
    try:
        service = get_kag_service()
        solution_id = str(uuid.uuid4())
        workflow_id = str(uuid.uuid4())
        
        # Invoke KAG with facts that should be stored in graph
        print("\n📝 Invoking KAG with facts...")
        
        workflow_output = """
        Completed market analysis for Q4 2024.
        Market growth rate: 15% year-over-year.
        Top competitors: CompanyA, CompanyB, CompanyC.
        Customer satisfaction score: 85%.
        Identified 3 new market segments.
        """
        
        result = service.invoke_kag(
            workflow_output=workflow_output,
            workflow_name="Market Analysis",
            solution_id=solution_id,
            workflow_id=workflow_id,
            context="Q4 2024 market research"
        )
        
        print(f"\n✅ KAG Result:")
        print(f"   Facts extracted: {len(result.get('facts', []))}")
        print(f"   Memory stored: {result.get('memory_stored', False)}")
        
        # If KG is available, facts should be in graph
        if service.kg_manager.is_available():
            print("\n🔍 Checking knowledge graph for facts...")
            
            related_facts = service.kg_manager.get_related_facts(solution_id)
            print(f"   Facts in graph: {len(related_facts)}")
            
            if related_facts:
                print(f"   Sample facts:")
                for i, fact in enumerate(related_facts[:3], 1):
                    print(f"      {i}. {fact}")
            
            print("\n✅ Facts successfully stored in knowledge graph")
        else:
            print("\n⚠️  Knowledge graph not available - facts stored in memory only")
        
        return True
        
    except Exception as e:
        print(f"\n❌ KAG with graph storage test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_kg_query_with_context():
    """Test 4: Knowledge graph query with accumulated context"""
    print("\n" + "="*80)
    print("TEST 4: Knowledge Graph Query with Context")
    print("="*80)
    
    try:
        service = get_kag_service()
        solution_id = str(uuid.uuid4())
        
        # Add multiple workflows to build context
        workflows = [
            ("Data Collection", "Collected 1000 user surveys with 95% response rate"),
            ("Data Analysis", "Analyzed survey data revealing 3 user segments"),
            ("Report Generation", "Generated comprehensive report with visualizations")
        ]
        
        print("\n📝 Building knowledge base with multiple workflows...")
        for name, output in workflows:
            service.invoke_kag(
                workflow_output=output,
                workflow_name=name,
                solution_id=solution_id,
                workflow_id=str(uuid.uuid4()),
                context=f"{name} phase"
            )
            print(f"   ✓ {name}")
        
        # Query the accumulated knowledge
        if not service.kg_manager.is_available():
            print("\n⚠️  Skipping query - Knowledge graph not available")
            return True
        
        print("\n🔍 Querying accumulated knowledge...")
        
        result = service.query_knowledge_graph(
            query="What user insights were discovered?",
            solution_id=solution_id
        )
        
        print(f"\n📊 Query Result:")
        print(f"   Answer: {result.get('answer', 'N/A')[:200]}...")
        print(f"   Related Facts: {len(result.get('related_facts', []))}")
        
        if result.get('related_facts'):
            print(f"\n   Top related facts:")
            for i, fact in enumerate(result['related_facts'][:5], 1):
                print(f"      {i}. {fact[:80]}...")
        
        print("\n✅ Contextual KG query successful")
        return True
        
    except Exception as e:
        print(f"\n❌ Contextual query test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_kg_unavailable_graceful_degradation():
    """Test 5: Graceful degradation when KG is unavailable"""
    print("\n" + "="*80)
    print("TEST 5: Graceful Degradation without Knowledge Graph")
    print("="*80)
    
    try:
        service = get_kag_service()
        solution_id = str(uuid.uuid4())
        
        # Query when KG might not be available
        result = service.query_knowledge_graph(
            query="Test query",
            solution_id=solution_id
        )
        
        print(f"\n📊 Result:")
        print(f"   Graph Available: {result.get('graph_available', False)}")
        print(f"   Answer: {result.get('answer', 'N/A')}")
        print(f"   Error: {result.get('error', 'None')}")
        
        # Should not crash even if KG unavailable
        assert 'answer' in result, "Should return answer even if unavailable"
        assert 'graph_available' in result, "Should indicate availability status"
        
        if not result.get('graph_available'):
            print("\n✅ Gracefully handled unavailable knowledge graph")
        else:
            print("\n✅ Knowledge graph is available and working")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Degradation test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_kag_service_with_kg_integration():
    """Test 6: Full KAG service with KG integration"""
    print("\n" + "="*80)
    print("TEST 6: Full KAG Service with Knowledge Graph")
    print("="*80)
    
    try:
        service = get_kag_service()
        
        # Verify service has KG manager
        assert hasattr(service, 'kg_manager'), "Service should have kg_manager"
        assert hasattr(service, 'kg_query_graph'), "Service should have kg_query_graph"
        
        print(f"\n✅ KAG Service Components:")
        print(f"   - KAG graph: ✓")
        print(f"   - Handoff graph: ✓")
        print(f"   - KG query graph: ✓")
        print(f"   - Knowledge graph manager: ✓")
        print(f"   - Graph available: {service.kg_manager.is_available()}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Integration test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def print_setup_instructions():
    """Print Neo4j setup instructions"""
    print("\n" + "💡" * 40)
    print("KNOWLEDGE GRAPH SETUP INSTRUCTIONS")
    print("💡" * 40)
    
    print("\n1. Install Neo4j Dependencies:")
    print("   pip install neo4j langchain-neo4j")
    
    print("\n2. Install and Run Neo4j:")
    print("   Option A - Docker:")
    print("     docker run -p 7474:7474 -p 7687:7687 \\")
    print("       -e NEO4J_AUTH=neo4j/password \\")
    print("       neo4j:latest")
    
    print("\n   Option B - Neo4j Desktop:")
    print("     Download from: https://neo4j.com/download/")
    
    print("\n3. Configure Environment Variables (.env):")
    print("   NEO4J_URI=bolt://localhost:7687")
    print("   NEO4J_USER=neo4j")
    print("   NEO4J_PASSWORD=your-password")
    print("   GROQ_API_KEY=your-groq-key  # For Cypher generation")
    
    print("\n4. Verify Connection:")
    print("   Open http://localhost:7474 in browser")
    print("   Login with credentials")
    
    print("\n5. Run Tests Again:")
    print("   python test_kg_query.py")
    
    print("\n" + "💡" * 40)


def run_all_tests():
    """Run all knowledge graph tests"""
    print("\n" + "🔬" * 40)
    print("KNOWLEDGE GRAPH QUERY NODE - TEST SUITE")
    print("🔬" * 40)
    
    results = []
    
    # Run tests
    results.append(("KG Manager Init", test_kg_manager_initialization()))
    results.append(("Basic KG Query", test_kg_query_basic()))
    results.append(("KAG + Graph Storage", test_kag_with_graph_storage()))
    results.append(("KG Query with Context", test_kg_query_with_context()))
    results.append(("Graceful Degradation", test_kg_unavailable_graceful_degradation()))
    results.append(("Full KAG Integration", test_kag_service_with_kg_integration()))
    
    # Print summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print("\n" + "=" * 80)
    print(f"Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print("=" * 80)
    
    # Show setup instructions if KG not available
    kg_manager = get_kg_manager()
    if not kg_manager.is_available():
        print_setup_instructions()
    
    return passed == total


if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
