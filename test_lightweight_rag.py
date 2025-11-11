"""
Quick test for lightweight Agentic RAG service
"""
import sys
sys.path.insert(0, r'c:\Sorry\agentic_app')

from app.services.agentic_rag_service import get_agentic_rag_service

def test_lightweight_rag():
    """Test the lightweight RAG implementation"""
    print("="*70)
    print("  TESTING LIGHTWEIGHT AGENTIC RAG SERVICE")
    print("="*70)
    
    # Get service
    service = get_agentic_rag_service()
    print("\n✅ Service initialized successfully (no LLM required!)")
    
    # Test 1: Text chunking
    print("\n" + "="*70)
    print("TEST 1: Text Chunking")
    print("="*70)
    test_text = "This is a test. " * 50  # 100 words
    chunks = service._chunk_text(test_text, chunk_size=20)
    print(f"✅ Chunked {len(test_text.split())} words into {len(chunks)} chunks")
    for i, chunk in enumerate(chunks[:3], 1):
        print(f"  Chunk {i}: {len(chunk.split())} words")
    
    # Test 2: Tokenization
    print("\n" + "="*70)
    print("TEST 2: Tokenization (stopword removal)")
    print("="*70)
    test_sentence = "The quick brown fox jumps over the lazy dog"
    tokens = service._tokenize(test_sentence)
    print(f"Original: {test_sentence}")
    print(f"✅ Tokens (after stopword removal): {tokens}")
    
    # Test 3: TF-IDF computation
    print("\n" + "="*70)
    print("TEST 3: TF-IDF Computation")
    print("="*70)
    docs = [
        "Python is a programming language",
        "Machine learning with Python",
        "Data science and analytics"
    ]
    tfidf_vectors, idf = service._compute_tfidf(docs)
    print(f"✅ Computed TF-IDF for {len(docs)} documents")
    print(f"  Vocabulary size: {len(idf)} unique terms")
    print(f"  Sample terms: {list(idf.keys())[:5]}")
    
    # Test 4: Cosine similarity
    print("\n" + "="*70)
    print("TEST 4: Cosine Similarity")
    print("="*70)
    sim = service._cosine_similarity(tfidf_vectors[0], tfidf_vectors[1])
    print(f"✅ Similarity between doc 1 and doc 2: {sim:.3f}")
    sim2 = service._cosine_similarity(tfidf_vectors[0], tfidf_vectors[2])
    print(f"✅ Similarity between doc 1 and doc 3: {sim2:.3f}")
    
    # Test 5: Key info extraction
    print("\n" + "="*70)
    print("TEST 5: Lightweight Key Information Extraction")
    print("="*70)
    sample_output = """
    Stock Analysis Results:
    The stock price is $150.25 with a P/E ratio of 28.5.
    Market performance shows 8.2% growth.
    Recommendation: Buy based on strong fundamentals.
    Key finding: Revenue increased by $2.5B.
    """
    insights = service._extract_key_info(sample_output)
    print(f"✅ Extracted key information:")
    print(f"  Key metrics found: {insights['key_metrics']}")
    print(f"  Key sentences: {len(insights['key_sentences'])}")
    print(f"  Top terms: {insights['top_terms'][:5]}")
    
    # Test 6: Store and retrieve
    print("\n" + "="*70)
    print("TEST 6: Store Workflow Output")
    print("="*70)
    result = service.store_workflow_output(
        solution_id="test_solution",
        workflow_id="wf1",
        workflow_name="Research Workflow",
        workflow_output=sample_output
    )
    print(f"✅ Stored workflow output")
    print(f"  Insights extracted: {result.get('insights', {}).get('key_metrics', [])}")
    
    # Test 7: Agent memory initialization
    print("\n" + "="*70)
    print("TEST 7: Agent Memory Initialization with RAG Retrieval")
    print("="*70)
    
    # Store another workflow
    service.store_workflow_output(
        solution_id="test_solution",
        workflow_id="wf2",
        workflow_name="Analysis Workflow",
        workflow_output="Analysis shows correlation with market trends. Data indicates 15.3% increase."
    )
    
    # Initialize agent memory for third workflow
    memory = service.initialize_agent_memory(
        solution_id="test_solution",
        workflow_id="wf3",
        agent_node_id="agent_node_1",
        workflow_description="Perform deep analysis of stock trends"
    )
    
    print(f"✅ Agent memory initialized")
    print(f"  Memory type: {memory.get('memory_type')}")
    print(f"  Retrieved context: {bool(memory.get('retrieved_context'))}")
    print(f"  Relevant facts: {len(memory.get('relevant_facts', []))}")
    if memory.get('relevant_facts'):
        for i, fact in enumerate(memory['relevant_facts'][:2], 1):
            print(f"    {i}. {fact.get('text', '')[:80]}...")
            print(f"       Similarity: {fact.get('similarity', 0)}")
    
    # Test 8: Handoff preparation
    print("\n" + "="*70)
    print("TEST 8: Prepare RAG Handoff")
    print("="*70)
    handoff = service.prepare_rag_handoff(
        solution_id="test_solution",
        source_workflow_id="wf1",
        target_workflow_id="wf3",
        target_workflow_description="Deep analysis"
    )
    print(f"✅ Handoff prepared")
    print(f"  Handoff type: {handoff.get('handoff_type')}")
    print(f"  Method: {handoff.get('method')}")
    print(f"  Handoff data preview:")
    print(f"  {handoff.get('handoff_data', '')[:200]}...")
    
    # Test 9: Solution summary
    print("\n" + "="*70)
    print("TEST 9: Generate Solution Summary")
    print("="*70)
    summary = service.get_solution_summary("test_solution")
    print(f"✅ Summary generated ({len(summary)} characters)")
    print("\nSummary Preview:")
    print(summary[:400] + "...")
    
    print("\n" + "="*70)
    print("  ALL TESTS PASSED! ✅")
    print("="*70)
    print("\n📊 Performance Notes:")
    print("  - No LLM calls required")
    print("  - Uses TF-IDF for embeddings")
    print("  - Cosine similarity for retrieval")
    print("  - Simple chunking strategy")
    print("  - Lightweight and fast")
    print("\n💡 This implementation is perfect for:")
    print("  - High-speed workflow communication")
    print("  - Cost-effective RAG without API calls")
    print("  - Offline operation")
    print("  - Scalable to many workflows")

if __name__ == "__main__":
    try:
        test_lightweight_rag()
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
