"""
Detailed Test of Agentic RAG Service
Shows exactly how data flows and is transferred between workflows
"""

import json
import sys
from app.services.agentic_rag_service import AgenticRAGService


def print_section(title):
    """Print a section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_subsection(title):
    """Print a subsection header"""
    print(f"\n--- {title} ---")


def format_bytes(bytes_count):
    """Format bytes to human readable"""
    if bytes_count < 1024:
        return f"{bytes_count} bytes"
    elif bytes_count < 1024 * 1024:
        return f"{bytes_count / 1024:.2f} KB"
    else:
        return f"{bytes_count / (1024 * 1024):.2f} MB"


def test_agentic_rag_workflow():
    """
    Comprehensive test showing:
    1. How data is chunked
    2. How embeddings are created
    3. How data is stored
    4. How agent memory is initialized
    5. How much data is transferred
    """
    
    print_section("AGENTIC RAG WORKFLOW TEST")
    print("This test demonstrates the complete Research Mode (Agentic RAG) workflow")
    print("showing exactly how data flows between workflows.\n")
    
    # Initialize service
    service = AgenticRAGService()
    solution_id = "test_research_solution_001"
    
    # ==========================================================================
    # WORKFLOW 1: Research Paper Scraping
    # ==========================================================================
    print_section("WORKFLOW 1: Research Paper Scraping")
    
    workflow_1_output = """
    Research Paper Analysis: Advances in Natural Language Processing
    
    Abstract:
    This paper presents a comprehensive survey of recent advances in natural language 
    processing (NLP) with a focus on transformer-based architectures. We analyze 
    the evolution from traditional statistical methods to modern deep learning 
    approaches, examining key milestones including word embeddings, recurrent neural 
    networks, attention mechanisms, and the transformer architecture.
    
    Introduction:
    Natural language processing has undergone a paradigm shift in recent years. 
    The introduction of word embeddings like Word2Vec and GloVe in 2013-2014 
    marked the beginning of the neural NLP era. These distributed representations 
    captured semantic relationships between words in continuous vector spaces, 
    enabling machines to understand linguistic patterns more effectively.
    
    Key Findings:
    1. Transformer models achieve 95% accuracy on GLUE benchmark
    2. Pre-training reduces task-specific training time by 73%
    3. Attention mechanisms improve long-range dependency modeling by 42%
    4. BERT and GPT families demonstrate strong transfer learning capabilities
    5. Model size correlates with performance: 175B parameters show optimal results
    
    Methodology:
    We conducted experiments on 12 different NLP datasets including SQuAD, MNLI, 
    and CoLA. Training was performed on 8 V100 GPUs with batch size 32. Learning 
    rate was set to 5e-5 with linear warmup over 10,000 steps. We used Adam 
    optimizer with weight decay of 0.01.
    
    Results:
    Our fine-tuned BERT model achieved 93.2% F1 score on SQuAD 2.0, outperforming 
    the baseline by 8.7 percentage points. On MNLI, we observed 86.5% accuracy 
    on matched data and 85.9% on mismatched data. The model processed 1,200 
    samples per second during inference on a single GPU.
    
    Discussion:
    The results demonstrate that transformer-based models excel at capturing 
    contextual information. The self-attention mechanism allows the model to 
    weigh the importance of different tokens dynamically. This is particularly 
    beneficial for tasks requiring long-range dependencies, such as question 
    answering and document classification.
    
    Furthermore, we observed that larger models benefit more from pre-training. 
    Models with 110M parameters showed 15% improvement with pre-training, while 
    340M parameter models showed 28% improvement. This suggests that scaling 
    model capacity enables better knowledge transfer.
    
    Conclusion:
    Transformer architectures represent a significant advancement in NLP. Their 
    ability to parallelize training and capture long-range dependencies makes 
    them superior to previous recurrent approaches. Future work should focus on 
    improving efficiency and reducing the computational requirements of these 
    large models. We recommend exploring model distillation, quantization, and 
    sparse attention mechanisms as promising directions.
    
    References:
    [1] Vaswani et al. (2017). Attention is All You Need.
    [2] Devlin et al. (2018). BERT: Pre-training of Deep Bidirectional Transformers.
    [3] Radford et al. (2019). Language Models are Unsupervised Multitask Learners.
    """
    
    print(f"Original Output Size: {format_bytes(len(workflow_1_output))}")
    print(f"Character Count: {len(workflow_1_output):,}")
    print(f"Word Count: {len(workflow_1_output.split()):,}")
    
    print_subsection("Storing Workflow 1 Output")
    
    # Store workflow 1 output
    storage_result = service.store_workflow_output(
        solution_id=solution_id,
        workflow_id="workflow_1_paper_scraping",
        workflow_name="Research Paper Scraper",
        workflow_output=workflow_1_output,
        metadata={"source": "arxiv", "paper_id": "2023.nlp.001"}
    )
    
    print("\n✅ Storage Result:")
    print(f"   Stored: {storage_result['stored']}")
    print(f"   Workflow ID: {storage_result['workflow_id']}")
    print(f"   Total Workflows in Memory: {storage_result['total_workflows_in_memory']}")
    
    if 'insights' in storage_result:
        insights = storage_result['insights']
        print(f"\n📊 Extracted Insights:")
        print(f"   Text Length: {insights.get('text_length', 0):,} characters")
        print(f"   Chunk Count: {insights.get('chunk_count', 0)} chunks")
        print(f"   Key Metrics Found: {len(insights.get('key_metrics', []))}")
        print(f"   Key Sentences Found: {len(insights.get('key_sentences', []))}")
        print(f"   Top Terms: {len(insights.get('top_terms', []))}")
        
        if insights.get('key_metrics'):
            print(f"\n   📈 Key Metrics Extracted:")
            for metric in insights['key_metrics'][:5]:
                print(f"      • {metric}")
        
        if insights.get('key_sentences'):
            print(f"\n   📝 Key Sentences Identified:")
            for i, sentence in enumerate(insights['key_sentences'][:3], 1):
                print(f"      {i}. {sentence[:80]}...")
        
        if insights.get('top_terms'):
            print(f"\n   🔤 Top Terms:")
            print(f"      {', '.join(insights['top_terms'][:10])}")
    
    # Show chunking details
    print_subsection("Chunking Analysis")
    chunks = service._chunk_text(workflow_1_output, chunk_size=200)
    print(f"\n📦 Text was divided into {len(chunks)} chunks (~200 words each)")
    print(f"\nFirst 3 chunks preview:")
    for i, chunk in enumerate(chunks[:3], 1):
        words = len(chunk.split())
        chunk_size = len(chunk)
        print(f"\n   Chunk {i}:")
        print(f"   - Size: {format_bytes(chunk_size)} ({words} words)")
        print(f"   - Preview: {chunk[:100]}...")
    
    # Show TF-IDF processing
    print_subsection("TF-IDF Embedding Analysis")
    tfidf_vectors, idf_scores = service._compute_tfidf(chunks)
    
    total_unique_terms = len(idf_scores)
    print(f"\n🔢 TF-IDF Statistics:")
    print(f"   Total Unique Terms: {total_unique_terms}")
    print(f"   Total Vectors Created: {len(tfidf_vectors)}")
    print(f"   Vector Dimensions: Variable (sparse)")
    
    # Show top IDF terms
    top_idf_terms = sorted(idf_scores.items(), key=lambda x: x[1], reverse=True)[:10]
    print(f"\n   Top 10 IDF Terms (most discriminative):")
    for term, score in top_idf_terms:
        print(f"      • {term}: {score:.3f}")
    
    # Calculate storage size
    print_subsection("Storage Analysis")
    solution_key = f"solution_{solution_id}"
    memory_size = sys.getsizeof(json.dumps(service.workflow_memory[solution_key]))
    print(f"\n💾 Memory Storage:")
    print(f"   Raw Output Size: {format_bytes(len(workflow_1_output))}")
    print(f"   Stored Memory Size: {format_bytes(memory_size)}")
    print(f"   Chunks Stored: {len(chunks)}")
    print(f"   Metadata Size: ~{format_bytes(sys.getsizeof(json.dumps(storage_result)))}")
    
    # ==========================================================================
    # WORKFLOW 2: Literature Review Agent
    # ==========================================================================
    print_section("WORKFLOW 2: Literature Review Agent")
    
    print("This workflow has an AGENT NODE that needs context from previous workflow")
    print("Agentic RAG will initialize agent memory with relevant chunks\n")
    
    workflow_2_id = "workflow_2_literature_review"
    agent_node_id = "agent_001_reviewer"
    workflow_2_description = "Analyze NLP research papers and identify key themes in transformer architectures and their applications"
    
    print(f"Workflow ID: {workflow_2_id}")
    print(f"Agent Node ID: {agent_node_id}")
    print(f"Description: {workflow_2_description}")
    
    print_subsection("Agent Memory Initialization")
    
    # Initialize agent memory
    agent_memory = service.initialize_agent_memory(
        solution_id=solution_id,
        workflow_id=workflow_2_id,
        agent_node_id=agent_node_id,
        workflow_description=workflow_2_description
    )
    
    print("\n🧠 Agent Memory Initialized!")
    print(f"\n📋 Memory Details:")
    print(f"   Memory Type: {agent_memory.get('memory_type', 'N/A')}")
    print(f"   Workflow History Count: {agent_memory.get('workflow_history_count', 0)}")
    
    if agent_memory.get('retrieved_context'):
        context = agent_memory['retrieved_context']
        print(f"\n🔍 Retrieval Statistics:")
        print(f"   Total Chunks Searched: {context.get('total_chunks_searched', 0)}")
        print(f"   Retrieval Method: {context.get('retrieval_method', 'N/A')}")
        print(f"   Relevant Facts Retrieved: {len(context.get('relevant_facts', []))}")
        
        # Show retrieved chunks
        if context.get('relevant_facts'):
            print(f"\n📦 Retrieved Chunks (Top-K by Similarity):")
            total_transferred = 0
            for i, fact in enumerate(context['relevant_facts'], 1):
                text = fact.get('text', '')
                source = fact.get('source', 'Unknown')
                similarity = fact.get('similarity', 0)
                chunk_size = len(text)
                total_transferred += chunk_size
                
                print(f"\n   Chunk {i}:")
                print(f"   - Source: {source}")
                print(f"   - Similarity Score: {similarity:.3f} ({similarity*100:.1f}%)")
                print(f"   - Size: {format_bytes(chunk_size)}")
                print(f"   - Preview: {text[:150]}...")
        
        print(f"\n📊 Data Transfer Summary:")
        print(f"   Total Data Transferred to Agent: {format_bytes(total_transferred)}")
        print(f"   Context Summary Size: {format_bytes(len(context.get('context_summary', '')))}")
        
        # Show context summary
        if context.get('context_summary'):
            print(f"\n📝 Context Summary Delivered to Agent:")
            print("   " + "-" * 76)
            for line in context['context_summary'].split('\n')[:5]:
                print(f"   {line}")
            if len(context['context_summary'].split('\n')) > 5:
                print(f"   ... ({len(context['context_summary'].split('\n'))} total lines)")
            print("   " + "-" * 76)
    
    # ==========================================================================
    # WORKFLOW 3: Research Synthesis
    # ==========================================================================
    print_section("WORKFLOW 3: Research Synthesis")
    
    # Simulate workflow 2 execution and storage
    workflow_2_output = """
    Literature Review Analysis Results:
    
    After analyzing the research papers on Natural Language Processing, several 
    key themes emerge:
    
    Theme 1: Transformer Architecture Dominance
    The transformer architecture has become the de facto standard for NLP tasks. 
    Key advantages include parallel processing capabilities and effective handling 
    of long-range dependencies through self-attention mechanisms. Performance 
    metrics show 95% accuracy on GLUE benchmark and significant improvements 
    over recurrent architectures.
    
    Theme 2: Pre-training and Transfer Learning
    Pre-training on large corpora followed by fine-tuning has proven highly 
    effective. Models like BERT and GPT demonstrate strong transfer learning 
    capabilities. Pre-training reduces task-specific training time by 73%, making 
    it cost-effective for various applications.
    
    Theme 3: Scaling Laws and Model Size
    Research indicates that model size correlates with performance. Models with 
    175B parameters show optimal results. However, larger models (110M to 340M 
    parameters) benefit more from pre-training, showing 15-28% improvement.
    
    Theme 4: Efficiency Concerns
    Despite impressive results, computational requirements remain a challenge. 
    Future research should focus on model distillation, quantization, and sparse 
    attention mechanisms to improve efficiency while maintaining performance.
    
    Recommendations:
    1. Adopt transformer-based architectures for new NLP projects
    2. Leverage pre-trained models when possible
    3. Consider model size vs. computational budget trade-offs
    4. Explore efficiency improvements for production deployment
    """
    
    print("Storing Workflow 2 output...")
    storage_2 = service.store_workflow_output(
        solution_id=solution_id,
        workflow_id=workflow_2_id,
        workflow_name="Literature Review Agent",
        workflow_output=workflow_2_output,
        metadata={"agent_node": agent_node_id}
    )
    
    print(f"\n✅ Workflow 2 Output Stored")
    print(f"   Size: {format_bytes(len(workflow_2_output))}")
    print(f"   Total Workflows in Memory: {storage_2['total_workflows_in_memory']}")
    
    # Initialize memory for workflow 3
    workflow_3_id = "workflow_3_synthesis"
    workflow_3_description = "Synthesize findings from literature review and create comprehensive research summary"
    
    print(f"\n\nInitializing Agent Memory for Workflow 3...")
    
    agent_memory_3 = service.initialize_agent_memory(
        solution_id=solution_id,
        workflow_id=workflow_3_id,
        agent_node_id="agent_002_synthesizer",
        workflow_description=workflow_3_description
    )
    
    print(f"\n🧠 Workflow 3 Agent Memory Initialized!")
    print(f"   Workflows Searched: {agent_memory_3.get('workflow_history_count', 0)}")
    
    if agent_memory_3.get('retrieved_context'):
        context_3 = agent_memory_3['retrieved_context']
        print(f"   Total Chunks Searched: {context_3.get('total_chunks_searched', 0)}")
        print(f"   Relevant Chunks Retrieved: {len(context_3.get('relevant_facts', []))}")
    
    # ==========================================================================
    # SOLUTION SUMMARY
    # ==========================================================================
    print_section("SOLUTION SUMMARY")
    
    summary = service.get_solution_summary(solution_id)
    print("\n📊 Complete Solution Summary:\n")
    print(summary)
    
    # ==========================================================================
    # FINAL STATISTICS
    # ==========================================================================
    print_section("FINAL DATA TRANSFER STATISTICS")
    
    solution_key = f"solution_{solution_id}"
    workflow_records = service.workflow_memory.get(solution_key, [])
    
    total_original_size = sum(len(r['raw_output']) for r in workflow_records)
    total_memory_size = sys.getsizeof(json.dumps(workflow_records))
    
    print(f"\n📈 Overall Statistics:")
    print(f"   Total Workflows Executed: {len(workflow_records)}")
    print(f"   Total Original Output Size: {format_bytes(total_original_size)}")
    print(f"   Total Memory Storage Size: {format_bytes(total_memory_size)}")
    print(f"   Compression Ratio: {total_memory_size/total_original_size:.2%}")
    
    # Calculate data transferred to agents
    if agent_memory.get('retrieved_context'):
        agent_1_transfer = sum(len(f['text']) for f in agent_memory['retrieved_context'].get('relevant_facts', []))
    else:
        agent_1_transfer = 0
    
    if agent_memory_3.get('retrieved_context'):
        agent_3_transfer = sum(len(f['text']) for f in agent_memory_3['retrieved_context'].get('relevant_facts', []))
    else:
        agent_3_transfer = 0
    
    total_agent_transfer = agent_1_transfer + agent_3_transfer
    
    print(f"\n🤖 Data Transferred to Agents:")
    print(f"   Agent 1 (Workflow 2): {format_bytes(agent_1_transfer)}")
    print(f"   Agent 2 (Workflow 3): {format_bytes(agent_3_transfer)}")
    print(f"   Total Agent Data Transfer: {format_bytes(total_agent_transfer)}")
    print(f"   Transfer Efficiency: {total_agent_transfer/total_original_size:.2%} of original data")
    
    print(f"\n✨ Key Insights:")
    print(f"   • Agentic RAG efficiently chunks large documents")
    print(f"   • Only relevant chunks ({total_agent_transfer/total_original_size:.1%}) transferred to agents")
    print(f"   • TF-IDF similarity search finds most relevant context")
    print(f"   • Agents receive FULL context upfront (not incremental)")
    print(f"   • No LLM needed for storage/retrieval (cost-effective)")
    
    # Cleanup
    print("\n\n🧹 Cleaning up test data...")
    service.clear_solution_memory(solution_id)
    print("✅ Test completed successfully!")
    
    print("\n" + "=" * 80)
    print("  END OF AGENTIC RAG WORKFLOW TEST")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    test_agentic_rag_workflow()
