# Solution Types: Visual Comparison

## 🎯 Normal Mode (KAG + Conversational Buffer)

```
┌─────────────────────────────────────────────────────────────────┐
│                     WORKFLOW EXECUTION CHAIN                     │
└─────────────────────────────────────────────────────────────────┘

                    ┌──────────────┐
                    │  Workflow 1  │
                    │   Executes   │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ KAG Pipeline │
                    │  (LangGraph) │
                    └──────┬───────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
   Retrieve          Extract Facts      Generate
   Context          (Gemini LLM)         Summary
        │                  │                  │
        └──────────────────┼──────────────────┘
                           ▼
                ┌────────────────────┐
                │ Conversational     │
                │ Buffer Memory      │
                │ - Full History     │
                │ - Facts List       │
                │ - Reasoning        │
                └────────┬───────────┘
                         │
                         ▼
                  ┌──────────────┐
                  │  Workflow 2  │◄──── Receives Context
                  │   Executes   │      from Memory
                  └──────┬───────┘
                         │
                         ▼
                    [Repeat...]
```

### Key Features:
- **LLM-Powered**: Uses Gemini for fact extraction
- **Intelligent Reasoning**: Understands relationships
- **Full Context**: All previous workflows available
- **Real-time**: Context available immediately

---

## 🔬 Research Mode (Agentic RAG)

```
┌─────────────────────────────────────────────────────────────────┐
│              RESEARCH-INTENSIVE WORKFLOW CHAIN                   │
└─────────────────────────────────────────────────────────────────┘

                    ┌──────────────┐
                    │  Workflow 1  │
                    │   Executes   │
                    │ (Large Text) │
                    └──────┬───────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Text Chunking   │
                  │ (~200 words ea) │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │  TF-IDF Index   │
                  │  (No LLM)       │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │  Vector Store   │
                  │  - Chunk 1      │
                  │  - Chunk 2      │
                  │  - Chunk N      │
                  │  + Metadata     │
                  └────────┬────────┘
                           │
                           │
                    ┌──────┴───────┐
                    │  Workflow 2  │
                    │ (Has Agent)  │
                    └──────┬───────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Agent Node Init │◄──── FULL CONTEXT
                  └────────┬────────┘      AT STARTUP!
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
   Query Vector    Similarity Search    Top-K Chunks
   (Workflow       (Cosine)             Retrieved
   Description)                         (Top 3)
        │                  │                  │
        └──────────────────┼──────────────────┘
                           ▼
                  ┌─────────────────┐
                  │ Agent Memory    │
                  │ INITIALIZED     │
                  │ - Chunk 1 (95%) │
                  │ - Chunk 2 (87%) │
                  │ - Chunk 3 (76%) │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │  Agent Executes │
                  │  with FULL      │
                  │  Context        │
                  └─────────────────┘
```

### Key Features:
- **Chunking**: Large texts split into manageable pieces
- **TF-IDF**: Lightweight embeddings (no LLM)
- **Similarity Search**: Find relevant chunks
- **Full Context to Agent**: All info at startup
- **Efficient**: Minimal LLM usage

---

## 📊 Side-by-Side Comparison

```
┌─────────────────────┬──────────────────────┬─────────────────────┐
│     FEATURE         │   NORMAL (KAG)       │  RESEARCH (RAG)     │
├─────────────────────┼──────────────────────┼─────────────────────┤
│ Memory Type         │ Conversational       │ Chunked Vector      │
│                     │ Buffer               │ Store               │
├─────────────────────┼──────────────────────┼─────────────────────┤
│ Fact Extraction     │ ✓ Gemini LLM         │ ✗ Heuristics        │
├─────────────────────┼──────────────────────┼─────────────────────┤
│ Context Delivery    │ Full History         │ Top-K Chunks        │
├─────────────────────┼──────────────────────┼─────────────────────┤
│ Agent Memory Init   │ On-Demand            │ ✓✓ FULL UPFRONT     │
├─────────────────────┼──────────────────────┼─────────────────────┤
│ Retrieval Method    │ All Context          │ Similarity Search   │
├─────────────────────┼──────────────────────┼─────────────────────┤
│ LLM Usage           │ High (per workflow)  │ Low (minimal)       │
├─────────────────────┼──────────────────────┼─────────────────────┤
│ Best for Size       │ Small-Medium         │ Large Documents     │
├─────────────────────┼──────────────────────┼─────────────────────┤
│ Speed               │ Medium               │ Fast                │
├─────────────────────┼──────────────────────┼─────────────────────┤
│ Cost                │ Higher               │ Lower               │
└─────────────────────┴──────────────────────┴─────────────────────┘
```

---

## 🎨 Frontend Selection UI

```
┌────────────────────────────────────────────────────────────────┐
│                    Create/Edit Solution                        │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Solution Type *                                               │
│                                                                │
│  ┌─────────────────────────┐  ┌─────────────────────────┐    │
│  │ ✓ Normal                │  │   Research              │    │
│  │                         │  │                         │    │
│  │ KAG + Conversational    │  │ Agentic RAG with        │    │
│  │ Buffer Memory           │  │ Embedding & Chunking    │    │
│  │                         │  │                         │    │
│  │ LLM-powered fact        │  │ Full context to agent   │    │
│  │ extraction with         │  │ nodes via intelligent   │    │
│  │ intelligent reasoning   │  │ retrieval               │    │
│  │                    ✓    │  │                         │    │
│  └─────────────────────────┘  └─────────────────────────┘    │
│                                                                │
│  💡 Normal mode: KAG extracts facts using Gemini LLM and       │
│     maintains conversational buffer memory across workflows    │
│                                                                │
└────────────────────────────────────────────────────────────────┘

OR (when Research selected):

┌────────────────────────────────────────────────────────────────┐
│                    Create/Edit Solution                        │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Solution Type *                                               │
│                                                                │
│  ┌─────────────────────────┐  ┌─────────────────────────┐    │
│  │   Normal                │  │ ✓ Research              │    │
│  │                         │  │                         │    │
│  │ KAG + Conversational    │  │ Agentic RAG with        │    │
│  │ Buffer Memory           │  │ Embedding & Chunking    │    │
│  │                         │  │                         │    │
│  │ LLM-powered fact        │  │ Full context to agent   │    │
│  │ extraction with         │  │ nodes via intelligent   │    │
│  │ intelligent reasoning   │  │ retrieval          ✓    │    │
│  └─────────────────────────┘  └─────────────────────────┘    │
│                                                                │
│  🔬 Research mode: Full information chunked & embedded,        │
│     delivered to agent nodes at startup via TF-IDF similarity  │
│     search                                                     │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Execution Flow Examples

### Example 1: Normal Mode (Market Analysis)

```
User Query: "Analyze stock market trends"

Workflow 1: Data Collection
   ↓
   Output: "Collected 500 data points from NYSE..."
   ↓
KAG Processing (Gemini):
   - Facts: ["NYSE data collected", "500 data points", "Tech sector up 5%"]
   - Summary: "Market data collected showing tech sector growth"
   - Stored in Conversational Buffer
   ↓
Workflow 2: Trend Analysis (receives full context)
   ↓
   Input Context:
      Previous: Workflow 1 summary + facts
      Reasoning: "Analyze the 500 data points for trends"
   ↓
   Output: "Tech sector trending up, finance stable..."
   ↓
KAG Processing (Gemini):
   - Facts: ["Tech up trend", "Finance stable", "Energy down 2%"]
   - Summary: "Market trends identified across sectors"
   - Stored in Buffer (accumulated)
   ↓
Workflow 3: Report Generation (receives ALL context)
   ↓
   Input Context:
      Full History: Workflow 1 + Workflow 2
      All Facts: Combined list
   ↓
   Output: "Comprehensive Market Report..."
```

### Example 2: Research Mode (Academic Paper Analysis)

```
User Query: "Analyze research papers on AI"

Workflow 1: Paper Scraping
   ↓
   Output: 10,000 words of paper abstracts and content
   ↓
Chunking:
   - 50 chunks created (~200 words each)
   ↓
TF-IDF Indexing:
   - Vector representation for each chunk
   - Stored in Vector Store
   ↓
Workflow 2: Literature Review (has Agent Node)
   ↓
   Description: "Identify key themes in AI research"
   ↓
Agent Memory Initialization:
   - Query Vector: "identify key themes AI research"
   - Similarity Search across 50 chunks
   - Top 3 Retrieved:
      1. Chunk 12: "...machine learning applications..." (95%)
      2. Chunk 34: "...neural network architectures..." (87%)
      3. Chunk 8: "...AI ethics and governance..." (76%)
   ↓
Agent Receives FULL CONTEXT at startup:
   {
     "retrieved_context": {
       "relevant_facts": [chunk12, chunk34, chunk8],
       "total_chunks_searched": 50
     }
   }
   ↓
   Agent Executes with Complete Information
   ↓
   Output: "Key themes identified: ML applications, NN arch, Ethics"
   ↓
Workflow 3: Synthesis
   ↓
   Retrieves relevant chunks again...
   ↓
   Output: "Research synthesis report..."
```

---

## 🎯 Decision Tree

```
                    Creating a Solution?
                           │
          ┌────────────────┴────────────────┐
          ▼                                 ▼
   Workflows produce          Workflows produce
   small-medium text?         large documents?
          │                                 │
          │                                 │
     ┌────┴────┐                      ┌────┴────┐
     ▼         ▼                      ▼         ▼
  Need LLM   Just need              Need       Cost
  reasoning? extraction?         chunking?  sensitive?
     │         │                      │         │
     ✓         ✗                      ✓         ✓
     │         │                      │         │
     └────┬────┘                      └────┬────┘
          ▼                                ▼
     NORMAL MODE                     RESEARCH MODE
  (KAG + Buffer)                   (Agentic RAG)
```

---

## 📝 Quick Reference

### When to Choose Normal Mode:
- ✅ Workflows with structured data
- ✅ Need intelligent fact extraction
- ✅ Want LLM-powered reasoning
- ✅ Small to medium outputs
- ✅ Real-time context needed
- ✅ Budget allows LLM usage

### When to Choose Research Mode:
- ✅ Large text documents (papers, articles)
- ✅ Agent nodes need comprehensive context
- ✅ Want to minimize LLM costs
- ✅ Need efficient chunking/indexing
- ✅ Similarity-based retrieval preferred
- ✅ Research and analysis workflows

---

## 🚀 Example Use Cases

### Normal Mode Examples:
1. **Customer Support Pipeline**
   - Extract customer facts → Analyze sentiment → Generate response
   
2. **Financial Analysis**
   - Collect market data → Identify trends → Create report

3. **Content Moderation**
   - Scan content → Extract policy violations → Generate action

### Research Mode Examples:
1. **Academic Literature Review**
   - Scrape papers → Agent analyzes → Synthesize findings

2. **Legal Document Analysis**
   - Extract case documents → Agent reviews → Summary report

3. **News Aggregation**
   - Collect articles → Agent identifies themes → Create digest

---

**Last Updated**: November 11, 2025  
**Status**: ✅ Both modes fully implemented and production-ready
