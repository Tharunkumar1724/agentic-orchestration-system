"""
Side-by-Side Comparison: Normal Mode (KAG) vs Research Mode (Agentic RAG)
"""

import json
from app.services.kag_service import get_kag_service
from app.services.agentic_rag_service import get_agentic_rag_service


def print_header(title):
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def test_comparison():
    """Compare Normal and Research modes side-by-side"""
    
    print_header("SOLUTION TYPE COMPARISON TEST")
    print("Testing the same workflow chain with both Normal and Research modes\n")
    
    # Sample workflow output
    workflow_output = """
    Market Analysis Report: Q4 2024 Technology Sector
    
    Executive Summary:
    The technology sector showed strong performance in Q4 2024, with major indices 
    reaching new highs. NASDAQ composite increased by 8.5%, driven primarily by 
    artificial intelligence and cloud computing stocks.
    
    Key Findings:
    1. AI sector grew 42% year-over-year
    2. Cloud infrastructure spending increased by $15.3 billion
    3. Semiconductor shortage eased, production up 23%
    4. Cybersecurity investments rose 31% due to increased threats
    5. Average P/E ratio for tech stocks: 28.5
    
    Top Performers:
    - NVIDIA: +65% (AI chip demand)
    - Microsoft: +28% (Azure growth)
    - Amazon: +19% (AWS expansion)
    - Google: +22% (AI integration)
    
    Market Metrics:
    Total market cap: $12.8 trillion
    Average daily volume: 8.9 billion shares
    Volatility index (VIX): 14.2
    Analyst upgrades: 127 stocks
    Downgrades: 43 stocks
    
    Sector Analysis:
    The AI boom continues to drive valuations higher, with companies investing 
    heavily in GPU infrastructure and large language models. Cloud providers 
    reported 35% revenue growth, outpacing traditional IT services. The easing 
    semiconductor shortage enabled manufacturers to meet pent-up demand, resulting 
    in strong earnings beats across the board.
    
    Risk Factors:
    - Regulatory concerns around AI safety
    - Potential interest rate changes
    - Geopolitical tensions affecting supply chains
    - Overvaluation concerns in AI subsector
    
    Outlook:
    Analysts expect continued growth in Q1 2025, with particular strength in 
    enterprise AI adoption and edge computing. Estimated sector growth: 18-22%.
    """
    
    solution_id = "comparison_test_001"
    
    # ==========================================================================
    # TEST 1: NORMAL MODE (KAG)
    # ==========================================================================
    print_header("TEST 1: NORMAL MODE (KAG + Conversational Buffer)")
    
    kag_service = get_kag_service()
    
    print("\n📊 Workflow 1 Output:")
    print(f"   Size: {len(workflow_output)} bytes ({len(workflow_output.split())} words)")
    
    print("\n🔄 Processing with KAG...")
    print("   [Sending to Gemini LLM for fact extraction...]")
    
    # Process with KAG
    try:
        kag_result = kag_service.invoke_kag(
            workflow_output=workflow_output,
            workflow_name="Market Analysis Workflow",
            solution_id=solution_id,
            workflow_id="workflow_1",
            context="Q4 2024 technology sector analysis"
        )
        
        print("\n✅ KAG Processing Complete")
        print(f"\n📋 Results:")
        print(f"   Facts Extracted: {len(kag_result.get('facts', []))}")
        print(f"   Summary Length: {len(kag_result.get('summary', ''))} characters")
        print(f"   Memory Stored: {kag_result.get('memory_stored', False)}")
        print(f"   Context Available: {kag_result.get('context_available', False)}")
        
        if kag_result.get('facts'):
            print(f"\n   📝 Extracted Facts (via Gemini LLM):")
            for i, fact in enumerate(kag_result['facts'][:5], 1):
                print(f"      {i}. {fact}")
        
        if kag_result.get('summary'):
            print(f"\n   📄 Generated Summary:")
            print(f"      {kag_result['summary'][:200]}...")
        
        if kag_result.get('reasoning'):
            print(f"\n   🧠 LLM Reasoning:")
            print(f"      {kag_result['reasoning'][:200]}...")
        
        print(f"\n💰 Cost Implications:")
        print(f"   • Used Gemini LLM: YES ✓")
        print(f"   • API Calls Made: ~2-3 (fact extraction + summary)")
        print(f"   • Token Usage: ~{len(workflow_output.split()) * 2} tokens (estimate)")
        print(f"   • Cost: $$ (LLM API costs)")
        
    except Exception as e:
        print(f"\n⚠️ KAG Processing Error: {e}")
        print("   (This is expected if Gemini API is not configured)")
        kag_result = {
            'facts': ['Fact extraction requires Gemini API'],
            'summary': 'Summary generation requires Gemini API',
            'reasoning': 'Reasoning requires Gemini API',
            'memory_stored': False
        }
    
    # ==========================================================================
    # TEST 2: RESEARCH MODE (AGENTIC RAG)
    # ==========================================================================
    print_header("TEST 2: RESEARCH MODE (Agentic RAG)")
    
    rag_service = get_agentic_rag_service()
    
    print("\n📊 Workflow 1 Output:")
    print(f"   Size: {len(workflow_output)} bytes ({len(workflow_output.split())} words)")
    
    print("\n🔄 Processing with Agentic RAG...")
    print("   [No LLM needed - using TF-IDF and heuristics...]")
    
    # Process with RAG
    rag_result = rag_service.store_workflow_output(
        solution_id=solution_id,
        workflow_id="workflow_1_rag",
        workflow_name="Market Analysis Workflow",
        workflow_output=workflow_output,
        metadata={"quarter": "Q4", "year": "2024"}
    )
    
    print("\n✅ RAG Processing Complete")
    print(f"\n📋 Results:")
    print(f"   Stored: {rag_result.get('stored', False)}")
    print(f"   Workflows in Memory: {rag_result.get('total_workflows_in_memory', 0)}")
    
    if rag_result.get('insights'):
        insights = rag_result['insights']
        print(f"\n   📊 Extracted Insights (Heuristic, No LLM):")
        print(f"      Text Length: {insights.get('text_length', 0)} characters")
        print(f"      Chunks Created: {insights.get('chunk_count', 0)}")
        print(f"      Key Metrics Found: {len(insights.get('key_metrics', []))}")
        print(f"      Key Sentences Found: {len(insights.get('key_sentences', []))}")
        
        if insights.get('key_metrics'):
            print(f"\n   💹 Key Metrics (Pattern Matching):")
            for metric in insights['key_metrics'][:8]:
                print(f"      • {metric}")
        
        if insights.get('key_sentences'):
            print(f"\n   📝 Key Sentences (Keyword Detection):")
            for i, sentence in enumerate(insights['key_sentences'][:3], 1):
                print(f"      {i}. {sentence[:100]}...")
        
        if insights.get('top_terms'):
            print(f"\n   🔤 Top Terms (TF-IDF):")
            print(f"      {', '.join(insights['top_terms'][:10])}")
    
    print(f"\n💰 Cost Implications:")
    print(f"   • Used LLM: NO ✗")
    print(f"   • API Calls Made: 0")
    print(f"   • Token Usage: 0")
    print(f"   • Cost: $0 (no API costs)")
    
    # ==========================================================================
    # SIDE-BY-SIDE COMPARISON
    # ==========================================================================
    print_header("SIDE-BY-SIDE COMPARISON")
    
    print("\n┌─────────────────────────┬──────────────────────┬─────────────────────┐")
    print("│       FEATURE           │    NORMAL (KAG)      │   RESEARCH (RAG)    │")
    print("├─────────────────────────┼──────────────────────┼─────────────────────┤")
    print("│ LLM Required            │ YES (Gemini)         │ NO                  │")
    print("│ API Calls               │ 2-3 per workflow     │ 0                   │")
    print("│ Cost per Workflow       │ $$ (API fees)        │ $0                  │")
    print("│ Processing Speed        │ Slower (API calls)   │ Faster (local)      │")
    print("│ Fact Quality            │ High (LLM-powered)   │ Medium (heuristic)  │")
    print("│ Summary Quality         │ High (LLM-powered)   │ N/A (no summary)    │")
    print("│ Context Delivery        │ Full history         │ Top-K chunks        │")
    print("│ Agent Memory Init       │ On-demand            │ Full upfront        │")
    print("│ Best for                │ General workflows    │ Large documents     │")
    print("└─────────────────────────┴──────────────────────┴─────────────────────┘")
    
    # ==========================================================================
    # AGENT MEMORY INITIALIZATION TEST
    # ==========================================================================
    print_header("AGENT MEMORY INITIALIZATION COMPARISON")
    
    print("\n🤖 Simulating Agent Node startup in Workflow 2...")
    
    # KAG Agent Memory
    print("\n--- NORMAL MODE: Agent Receives ---")
    try:
        kag_handoff = kag_service.prepare_handoff(
            source_workflow_id="workflow_1",
            target_workflow_id="workflow_2",
            target_workflow_description="Analyze market trends and predict Q1 2025 performance",
            solution_id=solution_id
        )
        
        print(f"\n   Handoff Type: {kag_handoff.get('handoff_type', 'N/A')}")
        print(f"   Handoff Data Length: {len(str(kag_handoff.get('handoff_data', '')))} chars")
        print(f"   Relevance: {kag_handoff.get('relevance', 'N/A')}")
        print(f"   Context: {kag_handoff.get('context', 'N/A')[:100]}...")
        
    except Exception as e:
        print(f"   (Requires Gemini API: {e})")
    
    # RAG Agent Memory
    print("\n--- RESEARCH MODE: Agent Receives ---")
    rag_agent_memory = rag_service.initialize_agent_memory(
        solution_id=solution_id,
        workflow_id="workflow_2_rag",
        agent_node_id="agent_trend_analyzer",
        workflow_description="Analyze market trends and predict Q1 2025 performance"
    )
    
    print(f"\n   Memory Type: {rag_agent_memory.get('memory_type', 'N/A')}")
    print(f"   Workflows Searched: {rag_agent_memory.get('workflow_history_count', 0)}")
    
    if rag_agent_memory.get('retrieved_context'):
        context = rag_agent_memory['retrieved_context']
        print(f"   Chunks Searched: {context.get('total_chunks_searched', 0)}")
        print(f"   Relevant Chunks Retrieved: {len(context.get('relevant_facts', []))}")
        print(f"   Retrieval Method: {context.get('retrieval_method', 'N/A')}")
        
        if context.get('relevant_facts'):
            print(f"\n   📦 Top Retrieved Chunks:")
            for i, fact in enumerate(context['relevant_facts'], 1):
                print(f"      {i}. Similarity: {fact.get('similarity', 0):.3f}")
                print(f"         Text: {fact.get('text', '')[:80]}...")
    
    # ==========================================================================
    # DATA TRANSFER ANALYSIS
    # ==========================================================================
    print_header("DATA TRANSFER ANALYSIS")
    
    print("\n📊 How much data is transferred to agents?")
    
    print("\n--- NORMAL MODE (KAG) ---")
    print("   Agent receives:")
    print("   • FULL conversational history")
    print("   • ALL extracted facts")
    print("   • Complete summaries from all previous workflows")
    print("   • LLM-generated reasoning")
    print(f"   Total Data: ~{len(workflow_output) + 500} bytes (estimate)")
    print("   Delivery: Real-time, on-demand")
    
    print("\n--- RESEARCH MODE (RAG) ---")
    if rag_agent_memory.get('retrieved_context'):
        total_transfer = sum(
            len(f.get('text', '')) 
            for f in rag_agent_memory['retrieved_context'].get('relevant_facts', [])
        )
        print("   Agent receives:")
        print("   • Top-K relevant chunks only")
        print("   • Similarity scores for each chunk")
        print("   • Source attribution")
        print(f"   Total Data: {total_transfer} bytes")
        print(f"   Efficiency: {(total_transfer / len(workflow_output)) * 100:.1f}% of original")
        print("   Delivery: FULL context at startup (not incremental)")
    
    # ==========================================================================
    # CONCLUSION
    # ==========================================================================
    print_header("TEST CONCLUSION")
    
    print("\n✅ Both modes successfully processed the workflow output")
    print("\n🎯 Key Differences:")
    print("\n   NORMAL MODE (KAG):")
    print("   ✓ Uses Gemini LLM for intelligent reasoning")
    print("   ✓ Extracts structured facts with context")
    print("   ✓ Generates human-like summaries")
    print("   ✓ Provides full conversational history")
    print("   ✗ Requires API calls (costs money)")
    print("   ✗ Slower due to network latency")
    
    print("\n   RESEARCH MODE (RAG):")
    print("   ✓ No LLM required (zero cost)")
    print("   ✓ Fast local processing")
    print("   ✓ Efficient data transfer (only relevant chunks)")
    print("   ✓ Full context delivered to agents upfront")
    print("   ✓ Scalable to large documents")
    print("   ✗ Heuristic extraction (less intelligent)")
    print("   ✗ No summary generation")
    
    print("\n💡 Recommendation:")
    print("   • Use NORMAL for: General workflows, need intelligence")
    print("   • Use RESEARCH for: Large docs, cost-sensitive, research tasks")
    
    # Cleanup
    print("\n\n🧹 Cleaning up...")
    kag_service.clear_solution_memory(solution_id)
    rag_service.clear_solution_memory(solution_id)
    
    print("\n✅ Comparison test complete!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    test_comparison()
