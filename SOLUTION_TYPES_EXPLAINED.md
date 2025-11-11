# Solution Types: Research vs Normal Mode

## Overview

When creating a solution in the Agentic Orchestration System, you can choose between two research strategies that determine how workflows communicate and share information:

1. **Normal Mode** - KAG + Conversational Buffer Memory
2. **Research Mode** - Agentic RAG with Embedding & Chunking

---

## 🎯 Normal Mode (KAG + Conversational Buffer)

### Description
Uses **Knowledge-Augmented Generation (KAG)** with LangGraph and conversational buffer memory for workflow-to-workflow communication.

### How It Works

```
Workflow 1 → [KAG Processing] → Memory Store
                ↓
         - Extract Facts (via Gemini LLM)
         - Generate Summary
         - Store in Conversational Buffer
                ↓
Workflow 2 ← [Retrieve Context] ← Memory Store
```

### Key Features

1. **LLM-Powered Fact Extraction**
   - Uses Gemini to extract structured facts from workflow outputs
   - Intelligent reasoning about relationships between facts
   - Context-aware summarization

2. **LangGraph Workflow**
   - Multi-node processing pipeline:
     - `retrieve_context`: Gets previous workflow memory
     - `extract_facts`: Extracts facts using Gemini
     - `generate_summary`: Creates intelligent summaries
     - `store_memory`: Saves to conversational buffer

3. **Conversational Buffer Memory**
   - Maintains conversation history across workflows
   - Accumulates context progressively
   - Provides full solution context for downstream workflows

4. **Intelligent Handoffs**
   - Uses Gemini to reason about workflow transitions
   - Determines relevance of previous workflow data
   - Generates targeted handoff instructions

### Best Use Cases

- ✅ General-purpose multi-workflow solutions
- ✅ Workflows requiring fact extraction and structured reasoning
- ✅ Complex decision-making workflows
- ✅ Scenarios where LLM-powered intelligence is beneficial
- ✅ Real-time workflows with immediate context needs

### Example Workflow Chain

```
Research Workflow → Extract facts about a topic
        ↓
Analysis Workflow → Reason about extracted facts
        ↓
Report Workflow → Generate comprehensive report
```

---

## 🔬 Research Mode (Agentic RAG)

### Description
Uses **Agentic RAG** with lightweight embedding, chunking, and retrieval for research-intensive solutions.

### How It Works

```
Workflow 1 → [Chunking] → [TF-IDF Indexing] → Vector Store
                                                    ↓
Workflow 2 [Agent Node] ← [Memory Init] ← [Similarity Search]
                                           (Top-K Retrieval)
```

### Key Features

1. **Text Chunking Strategy**
   - Splits large outputs into ~200-word chunks
   - Preserves semantic coherence
   - Enables granular retrieval

2. **TF-IDF Embeddings (No LLM Required)**
   - Lightweight vector representation
   - Fast computation without API calls
   - Cosine similarity for relevance matching

3. **Agent Memory Initialization**
   - **Full information delivered to agent nodes at startup**
   - Agent receives complete relevant context before execution
   - Memory is initialized with retrieved chunks
   - No incremental loading - all at once

4. **Intelligent Retrieval**
   - Similarity-based context retrieval
   - Top-3 most relevant chunks per query
   - Source attribution and relevance scores

5. **Lightweight Processing**
   - Simple heuristics for key information extraction
   - No LLM dependencies for storage/retrieval
   - Fast execution with minimal overhead

### Best Use Cases

- ✅ Research-intensive workflows with large text outputs
- ✅ Document analysis and information retrieval tasks
- ✅ Scenarios requiring efficient chunking and indexing
- ✅ Workflows where agent nodes need comprehensive context
- ✅ Cost-sensitive applications (minimal LLM usage)
- ✅ Batch processing with delayed analysis

### Example Workflow Chain

```
Web Scraping → Extract large articles (chunked & indexed)
        ↓
Literature Review Agent → Receives top-K relevant chunks at init
        ↓
Synthesis → Generates research summary
```

### Key Information Extraction

The Agentic RAG service automatically extracts:

- **Metrics**: Numbers, percentages, currency values
- **Key Sentences**: Important statements with keywords (result, finding, conclusion, etc.)
- **Top Terms**: Most frequent significant terms
- **Context Metadata**: Chunk counts, text length, timestamps

---

## 📊 Feature Comparison

| Feature | Normal (KAG) | Research (RAG) |
|---------|-------------|----------------|
| **Memory Strategy** | Conversational Buffer | Chunked Vector Store |
| **Fact Extraction** | LLM-Powered (Gemini) | Heuristic-Based |
| **Context Retrieval** | Full Conversation | Similarity Search (Top-K) |
| **Agent Memory Init** | On-demand | **Full context at startup** |
| **Processing Framework** | LangGraph | Custom RAG Pipeline |
| **API Dependencies** | High (Gemini calls) | Low (TF-IDF only) |
| **Best for Text Size** | Small-Medium | Large Documents |
| **Context Handoff** | Intelligent Reasoning | Extracted Insights |
| **Cost** | Higher (LLM usage) | Lower (minimal LLM) |
| **Speed** | Medium | Fast |

---

## 🎨 Frontend Selection

When creating a solution, users see two radio button options:

### Normal Mode Card
```
✓ Normal
  KAG + Conversational Buffer
  Best for general workflows with fact extraction
```

### Research Mode Card
```
  Research
  Agentic RAG
  Advanced retrieval with agent memory initialization
```

Dynamic help text updates based on selection:
- **Normal**: "💡 Normal mode uses KAG (Knowledge Augmented Generation) with conversational buffer for workflow communication"
- **Research**: "🔬 Research mode uses Agentic RAG with intelligent retrieval and memory initialization at agent nodes"

---

## 💻 Implementation Details

### Backend Services

#### 1. KAG Service (`app/services/kag_service.py`)

```python
class KAGService:
    """Knowledge-Aided Generation using LangGraph"""
    
    def invoke_kag(workflow_output, workflow_name, solution_id, workflow_id):
        # LangGraph workflow:
        # 1. Retrieve context from memory
        # 2. Extract facts using Gemini
        # 3. Generate summary
        # 4. Store in conversational buffer
        pass
    
    def prepare_handoff(source_workflow_id, target_workflow_id):
        # Use Gemini to reason about handoff
        pass
```

#### 2. Agentic RAG Service (`app/services/agentic_rag_service.py`)

```python
class AgenticRAGService:
    """Lightweight RAG with TF-IDF"""
    
    def store_workflow_output(solution_id, workflow_id, workflow_output):
        # 1. Chunk text
        # 2. Extract key info
        # 3. Store with metadata
        pass
    
    def initialize_agent_memory(solution_id, workflow_id, agent_node_id):
        # 1. Create query from workflow description
        # 2. Compute TF-IDF for all chunks
        # 3. Retrieve Top-K similar chunks
        # 4. Return full context for agent initialization
        pass
    
    def prepare_rag_handoff(source_workflow_id, target_workflow_id):
        # 1. Get source insights
        # 2. Build concise handoff with key findings
        pass
```

### Solution Execution Flow

```python
@router.post("/{solution_id}/execute")
async def execute_solution(solution_id, query):
    solution = load("solutions", solution_id)
    solution_type = solution.get("solution_type", "normal")
    
    # Select service based on solution type
    if solution_type == "research":
        service = get_agentic_rag_service()
    else:
        service = get_kag_service()
    
    for workflow in solution.workflows:
        # For research mode: Initialize agent memory
        if solution_type == "research":
            agent_memory = service.initialize_agent_memory(
                solution_id, workflow_id, agent_node_id
            )
        
        # Execute workflow
        result = await run_workflow(workflow)
        
        # Store output
        if solution_type == "research":
            service.store_workflow_output(...)
        else:
            service.invoke_kag(...)
```

---

## 🚀 Quick Start Examples

### Creating a Normal Solution (KAG)

```javascript
const normalSolution = {
  name: "Market Analysis Solution",
  description: "Analyze market trends and generate reports",
  solution_type: "normal",  // KAG + Buffer
  workflows: ["data_collection", "trend_analysis", "report_generation"]
};
```

### Creating a Research Solution (RAG)

```javascript
const researchSolution = {
  name: "Academic Research Solution",
  description: "Process research papers and synthesize findings",
  solution_type: "research",  // Agentic RAG
  workflows: ["paper_scraping", "literature_review", "synthesis"]
};
```

---

## 🎯 Decision Guide

### Choose **Normal Mode** (KAG) when:
- You need intelligent fact extraction and reasoning
- Workflows have small to medium outputs
- You want LLM-powered context understanding
- Real-time intelligent handoffs are important
- Budget allows for LLM API usage

### Choose **Research Mode** (RAG) when:
- Workflows produce large text outputs (documents, articles)
- You need efficient chunking and retrieval
- Agent nodes require comprehensive context at initialization
- You want to minimize LLM costs
- Fast similarity-based search is preferred
- Research and document analysis is the primary use case

---

## 📝 Key Takeaways

1. **Both modes are production-ready** and fully implemented in the system
2. **Normal mode** is **LLM-intensive** for intelligent reasoning
3. **Research mode** is **lightweight** and efficient for large documents
4. **Agent memory initialization** in research mode provides **full context upfront**
5. **Frontend selection** is seamless with clear visual indicators
6. **Backend automatically** switches between services based on `solution_type`

---

## 🔧 Configuration

### Model Definition (`app/models.py`)

```python
class SolutionCreate(BaseModel):
    name: str
    description: Optional[str] = None
    solution_type: str = Field(
        default="normal", 
        description="Solution type: 'normal' (KAG+Buffer) or 'research' (Agentic RAG)"
    )
    workflows: List[str] = Field(default_factory=list)
```

### Frontend Component (`SolutionsManagement.js`)

```javascript
const [formData, setFormData] = useState({
  name: '',
  description: '',
  solution_type: 'normal',  // Default
  workflows: []
});
```

---

## 📚 Related Documentation

- `LIGHTWEIGHT_RAG_IMPLEMENTATION.md` - Detailed RAG implementation
- `KAG_LANGGRAPH_GUIDE.md` - KAG and LangGraph details
- `SOLUTION_SYSTEM_COMPLETE.md` - Overall solution architecture
- `API_EXAMPLES.md` - API usage examples

---

**Last Updated**: November 11, 2025  
**Status**: ✅ Fully Implemented and Production Ready
