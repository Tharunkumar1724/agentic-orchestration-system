# Solution Types Quick Reference Card

## 🎯 Two Options When Creating Solutions

### Option 1: **Normal Mode**
**KAG + Conversational Buffer Memory**

```
✓ LLM-powered fact extraction (Gemini)
✓ Intelligent reasoning about context
✓ Full conversational history
✓ Best for general workflows
```

**When to use:**
- General-purpose workflows
- Need intelligent fact extraction
- Small to medium outputs
- Budget allows LLM usage

---

### Option 2: **Research Mode**
**Agentic RAG with Embedding & Chunking**

```
✓ Text chunking (~200 words)
✓ TF-IDF embeddings (no LLM needed)
✓ FULL context to agent nodes at startup
✓ Similarity-based retrieval
```

**When to use:**
- Large documents/papers
- Research-intensive tasks
- Want full info at agent startup
- Cost-sensitive (minimal LLM)

---

## 🔄 How They Work

### Normal (KAG):
```
Workflow 1 → Extract Facts (LLM) → Store in Buffer
                                         ↓
Workflow 2 ← Get Full Context ← Buffer Memory
```

### Research (RAG):
```
Workflow 1 → Chunk Text → TF-IDF Index → Vector Store
                                              ↓
Workflow 2 Agent ← Top-K Similar ← Similarity Search
   (Gets FULL context at init)
```

---

## 📊 Key Differences

| Feature | Normal | Research |
|---------|--------|----------|
| **Fact Extraction** | ✓ LLM | ✗ Heuristic |
| **Agent Memory** | On-demand | **FULL at startup** |
| **Retrieval** | All context | Top-K chunks |
| **LLM Usage** | High | Low |
| **Best for** | General | Large docs |
| **Cost** | Higher | Lower |

---

## 💡 Key Insight

**Research Mode** delivers **FULL INFORMATION** to agent nodes via:
1. Chunking large outputs
2. Creating TF-IDF embeddings
3. Finding similar chunks
4. **Initializing agent memory with ALL relevant context at startup**

Unlike Normal mode where context is pulled on-demand, Research mode gives agents **complete relevant information upfront** for comprehensive analysis.

---

## 🎨 UI Selection

Both options available as radio buttons when creating/editing solutions:

```
( • ) Normal              (   ) Research
  KAG + Buffer              Agentic RAG
  LLM-powered               Full context to agents
```

---

## 📝 Examples

**Normal**: Customer support (extract facts, analyze, respond)  
**Research**: Academic papers (chunk, retrieve, synthesize)

---

**Quick Start**: Choose **Normal** for most cases, **Research** for document analysis.

**Updated**: November 11, 2025
