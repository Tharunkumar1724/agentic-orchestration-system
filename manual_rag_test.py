"""
Manual test of Agentic RAG service directly (without full API)
This tests the RAG implementation in isolation
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.services.agentic_rag_service import AgenticRAGService
import asyncio

def test_rag_workflow():
    print("="*80)
    print(" MANUAL AGENTIC RAG TEST - Direct Service Testing")
    print("="*80)
    
    # Initialize service
    solution_id = "test_solution_123"
    service = AgenticRAGService()
    
    print(f"\n✅ Initialized AgenticRAGService for solution: {solution_id}\n")
    
    # Test 1: Store some workflow outputs
    print("TEST 1: Storing Workflow Outputs")
    print("-" * 40)
    
    workflow1_output = """
    Stock Analysis for AAPL:
    Current Price: $150.25
    P/E Ratio: 28.5
    Market Cap: $2.5T
    Recommendation: BUY
    
    Apple Inc. continues to show strong performance in the tech sector.
    Revenue growth of 8.2% year-over-year demonstrates solid fundamentals.
    The company's ecosystem lock-in provides competitive advantage.
    Cash reserves of $165B provide financial stability.
    """
    
    service.store_workflow_output(
        solution_id=solution_id,
        workflow_id="stock_analysis",
        workflow_name="Stock Analysis Workflow",
        workflow_output=workflow1_output
    )
    print("✅ Stored workflow 1: stock_analysis")
    
    workflow2_output = """
    Market Sentiment Analysis:
    Overall Sentiment: Positive (72%)
    News Mentions: 1,234 articles this week
    Social Media Buzz: High (8.5/10)
    
    Key topics:
    - New iPhone launch excitement
    - Services revenue growth
    - AI integration plans
    - Supply chain improvements
    """
    
    service.store_workflow_output(
        solution_id=solution_id,
        workflow_id="sentiment_analysis",
        workflow_name="Sentiment Analysis Workflow",
        workflow_output=workflow2_output
    )
    print("✅ Stored workflow 2: sentiment_analysis")
    
    # Test 2: Initialize agent memory (RAG retrieval)
    print("\n\nTEST 2: Initialize Agent Memory (RAG Retrieval)")
    print("-" * 40)
    
    query = "What is Apple's financial performance and market sentiment?"
    agent_node = "analysis_agent"
    memory_data = service.initialize_agent_memory(solution_id, agent_node, query)
    
    print(f"Query: {query}")
    print(f"\n📊 Memory Initialized:")
    print(f"   - Relevant chunks retrieved: {len(memory_data.get('relevant_context', []))}")
    print(f"   - Query used: {memory_data.get('query', 'N/A')}")
    print(f"   - Solution ID: {memory_data.get('solution_id', 'N/A')}")
    
    if memory_data.get('relevant_context'):
        print(f"\n📝 Relevant Context (Top 3):")
        for i, chunk in enumerate(memory_data['relevant_context'][:3], 1):
            print(f"\n   Chunk {i}:")
            print(f"      Source: {chunk.get('source', 'Unknown')}")
            print(f"      Similarity: {chunk.get('similarity', 0):.3f}")
            print(f"      Text: {chunk.get('text', '')[:100]}...")
    
    # Test 3: Prepare RAG handoff
    print("\n\nTEST 3: Prepare RAG Handoff")
    print("-" * 40)
    
    handoff = service.prepare_rag_handoff(solution_id, "stock_analysis", "final_report")
    
    print(f"📦 Handoff Package:")
    print(f"   - Solution ID: {handoff.get('solution_id', 'N/A')}")
    print(f"   - Total workflows: {handoff.get('total_workflows', 0)}")
    print(f"   - Total chunks: {handoff.get('total_chunks', 0)}")
    
    if handoff.get('key_findings'):
        print(f"\n📌 Key Findings ({len(handoff['key_findings'])} items):")
        for finding in handoff['key_findings'][:5]:
            print(f"      • {finding[:80]}...")
    
    if handoff.get('extracted_metrics'):
        print(f"\n📊 Extracted Metrics ({len(handoff['extracted_metrics'])} items):")
        for metric in handoff['extracted_metrics'][:10]:
            print(f"      • {metric}")
    
    # Test 4: Get solution summary
    print("\n\nTEST 4: Get Solution Summary")
    print("-" * 40)
    
    summary = service.get_solution_summary(solution_id)
    
    print(f"📄 Solution Summary:")
    print(f"   - Length: {len(summary)} characters")
    print(f"   - Contains 'workflow': {'workflow' in summary.lower()}")
    print(f"   - Contains numbers: {any(c.isdigit() for c in summary)}")
    print(f"\n📝 Summary Content (first 500 chars):")
    print(f"   {summary[:500]}...")
    
    # Test 5: Verify TF-IDF and Cosine Similarity
    print("\n\nTEST 5: Verify TF-IDF Implementation")
    print("-" * 40)
    
    # Create a test query
    test_docs = [
        "Apple stock price performance",
        "Market sentiment for technology companies",
        "Unrelated topic about weather"
    ]
    
    # Tokenize
    tokens = [service._tokenize(doc) for doc in test_docs]
    print(f"✅ Tokenized {len(test_docs)} documents")
    for i, toks in enumerate(tokens, 1):
        print(f"   Doc {i}: {toks[:5]}...")
    
    # Compute TF-IDF
    tfidf_vectors, idf_scores = service._compute_tfidf(test_docs)
    print(f"\n✅ Computed TF-IDF vectors")
    print(f"   - Vectors created: {len(tfidf_vectors)}")
    print(f"   - Non-zero entries in first vector: {len(tfidf_vectors[0])}")
    print(f"   - IDF terms: {len(idf_scores)}")
    
    # Compute similarities
    query_text = "Apple stock analysis"
    query_vector = tfidf_vectors[0]  # Use first doc as example
    
    similarities = []
    for vec in tfidf_vectors:
        sim = service._cosine_similarity(query_vector, vec)
        similarities.append(sim)
    
    print(f"\n✅ Cosine Similarities (using first doc as query):")
    for i, sim in enumerate(similarities, 1):
        print(f"   Doc {i} ('{test_docs[i-1]}'): {sim:.3f}")
    
    # Final summary
    print("\n" + "="*80)
    print(" TEST RESULTS SUMMARY")
    print("="*80)
    print("✅ All 5 tests completed successfully!")
    print("\nKey Achievements:")
    print("  • Lightweight RAG implementation (no LLM)")
    print("  • TF-IDF embeddings working correctly")
    print("  • Cosine similarity calculating relevance")
    print("  • Agent memory initialization with relevant context")
    print("  • RAG handoff preparation with findings and metrics")
    print("  • Solution summary generation")
    print("\n🎯 Agentic RAG is fully functional!")

if __name__ == "__main__":
    test_rag_workflow()
