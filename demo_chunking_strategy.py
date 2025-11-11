"""
Interactive Chunking Strategy Demo
Shows exactly how text is chunked with different sizes
"""

from app.services.agentic_rag_service import AgenticRAGService


def print_header(title):
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def demo_chunking():
    """Interactive demonstration of chunking strategy"""
    
    print_header("CHUNKING STRATEGY DEMONSTRATION")
    
    service = AgenticRAGService()
    
    # Sample text
    sample_text = """
    Artificial Intelligence has revolutionized the field of Natural Language Processing.
    Modern transformer models like BERT, GPT, and T5 have achieved state-of-the-art 
    results on numerous benchmarks including GLUE, SuperGLUE, and SQuAD. These models 
    leverage self-attention mechanisms to capture long-range dependencies in text, 
    enabling them to understand context more effectively than previous architectures.
    
    The training process involves pre-training on massive corpora followed by fine-tuning
    on task-specific datasets. Pre-training typically uses objectives like masked language
    modeling or next sentence prediction. Fine-tuning adapts the pre-trained model to
    specific tasks such as sentiment analysis, named entity recognition, or question answering.
    
    Performance metrics show remarkable improvements. BERT achieved 93.2% accuracy on MNLI,
    while GPT-3 demonstrated few-shot learning capabilities with 175 billion parameters.
    The computational requirements are substantial, often requiring hundreds of GPUs and
    weeks of training time. However, the resulting models exhibit strong generalization
    across diverse NLP tasks.
    
    Recent research focuses on efficiency improvements. Techniques like knowledge distillation,
    pruning, and quantization reduce model size while maintaining performance. Mobile-optimized
    models like DistilBERT and TinyBERT achieve 95% of BERT's performance with only 40% of
    the parameters, making deployment on edge devices feasible.
    """
    
    print(f"\n📄 Sample Text:")
    print(f"   Total Characters: {len(sample_text):,}")
    print(f"   Total Words: {len(sample_text.split()):,}")
    print(f"   Lines: {len(sample_text.strip().split(chr(10)))}")
    
    # Demonstrate different chunk sizes
    chunk_sizes = [50, 100, 200, 300]
    
    for chunk_size in chunk_sizes:
        print_header(f"CHUNK SIZE: {chunk_size} WORDS")
        
        chunks = service._chunk_text(sample_text, chunk_size=chunk_size)
        
        print(f"\n📊 Statistics:")
        print(f"   Total Chunks Created: {len(chunks)}")
        print(f"   Average Chunk Size: {sum(len(c.split()) for c in chunks) / len(chunks):.1f} words")
        print(f"   Average Chunk Bytes: {sum(len(c) for c in chunks) / len(chunks):.0f} bytes")
        
        # Show each chunk
        print(f"\n📦 Chunk Breakdown:")
        for i, chunk in enumerate(chunks, 1):
            words = len(chunk.split())
            chars = len(chunk)
            print(f"\n   Chunk {i}:")
            print(f"   ├─ Words: {words}")
            print(f"   ├─ Characters: {chars}")
            print(f"   ├─ Size: {chars / 1024:.2f} KB")
            print(f"   └─ Preview: {chunk.strip()[:100]}...")
    
    # Detailed view for 200 words (default)
    print_header("DETAILED VIEW: 200-WORD CHUNKS (DEFAULT)")
    
    chunks = service._chunk_text(sample_text, chunk_size=200)
    
    print(f"\n🔍 Full Chunk Contents:\n")
    
    for i, chunk in enumerate(chunks, 1):
        print(f"{'─' * 80}")
        print(f"CHUNK {i} of {len(chunks)}")
        print(f"{'─' * 80}")
        print(f"Words: {len(chunk.split())} | Characters: {len(chunk)}")
        print(f"\n{chunk.strip()}\n")
    
    # Show boundaries
    print_header("CHUNK BOUNDARY ANALYSIS")
    
    chunks = service._chunk_text(sample_text, chunk_size=200)
    
    print("\n🔗 Examining Chunk Boundaries:\n")
    
    for i in range(len(chunks) - 1):
        current_chunk = chunks[i]
        next_chunk = chunks[i + 1]
        
        # Get last 10 words of current chunk
        current_words = current_chunk.split()
        last_words = ' '.join(current_words[-10:])
        
        # Get first 10 words of next chunk
        next_words = next_chunk.split()
        first_words = ' '.join(next_words[:10])
        
        print(f"   Boundary {i + 1} (between Chunk {i + 1} and Chunk {i + 2}):")
        print(f"   ├─ Last 10 words of Chunk {i + 1}:")
        print(f"   │  '...{last_words}'")
        print(f"   │")
        print(f"   └─ First 10 words of Chunk {i + 2}:")
        print(f"      '{first_words}...'")
        print()
    
    # Visual representation
    print_header("VISUAL CHUNK DISTRIBUTION")
    
    chunks = service._chunk_text(sample_text, chunk_size=200)
    total_words = len(sample_text.split())
    
    print(f"\n📊 Document Word Distribution (Total: {total_words} words)\n")
    
    cumulative = 0
    for i, chunk in enumerate(chunks, 1):
        words_in_chunk = len(chunk.split())
        cumulative += words_in_chunk
        
        # Create visual bar
        bar_length = int((words_in_chunk / total_words) * 60)
        bar = '█' * bar_length
        
        print(f"   Chunk {i}: {bar} {words_in_chunk:3d} words ({words_in_chunk/total_words*100:5.1f}%)")
    
    print(f"\n   Total:   {'█' * 60} {cumulative:3d} words (100.0%)")
    
    # Impact of chunk size on retrieval
    print_header("IMPACT ON RETRIEVAL")
    
    print("\n💡 How chunk size affects retrieval:\n")
    
    for size in [50, 100, 200, 300]:
        chunks = service._chunk_text(sample_text, chunk_size=size)
        
        # Simulate TF-IDF computation
        tfidf_vectors, idf_scores = service._compute_tfidf(chunks)
        
        print(f"   Chunk Size: {size:3d} words")
        print(f"   ├─ Chunks created: {len(chunks)}")
        print(f"   ├─ TF-IDF vectors: {len(tfidf_vectors)}")
        print(f"   ├─ Unique terms: {len(idf_scores)}")
        print(f"   ├─ Avg terms/chunk: {sum(len(v) for v in tfidf_vectors) / len(tfidf_vectors):.1f}")
        print(f"   └─ Search space: {len(chunks)} chunks to search")
        print()
    
    # Recommendations
    print_header("CHUNKING STRATEGY RECOMMENDATIONS")
    
    print("""
📋 CHUNK SIZE SELECTION GUIDE:

┌────────────────┬─────────────┬──────────────────────────────────┐
│ Chunk Size     │ Best For    │ Characteristics                  │
├────────────────┼─────────────┼──────────────────────────────────┤
│ 50-100 words   │ Tweets      │ • Very precise retrieval         │
│                │ Short posts │ • Many chunks (slower)           │
│                │ Q&A pairs   │ • Less context per chunk         │
├────────────────┼─────────────┼──────────────────────────────────┤
│ 150-200 words  │ Articles    │ • Balanced precision/context ✓   │
│ ⭐ DEFAULT     │ Papers      │ • Optimal for most cases         │
│                │ Reports     │ • Good retrieval speed           │
├────────────────┼─────────────┼──────────────────────────────────┤
│ 250-300 words  │ Books       │ • More context per chunk         │
│                │ Long docs   │ • Fewer chunks (faster)          │
│                │ Narratives  │ • Less precise matching          │
├────────────────┼─────────────┼──────────────────────────────────┤
│ 400+ words     │ Chapters    │ • Maximum context                │
│                │ Sections    │ • Very few chunks                │
│                │             │ • Coarse-grained retrieval       │
└────────────────┴─────────────┴──────────────────────────────────┘

✅ RECOMMENDATIONS:

• Keep DEFAULT (200 words) for general use
• Decrease to 100-150 for technical/precise content
• Increase to 250-300 for narrative/contextual content
• NEVER go below 50 (too fragmented)
• NEVER go above 500 (too coarse)

💡 THE SWEET SPOT: 150-250 words
   - Captures 1-2 paragraphs
   - Enough context for meaning
   - Efficient for TF-IDF
   - Fast similarity search
""")
    
    print("\n" + "=" * 80)
    print("  DEMONSTRATION COMPLETE")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    demo_chunking()
