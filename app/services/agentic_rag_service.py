"""
Agentic RAG Service for Research-type Solutions

This service provides lightweight RAG (Retrieval-Augmented Generation) for workflow communication.
Unlike the KAG+Buffer approach, this uses:
- Simple chunking strategy for text processing
- TF-IDF based embeddings (no LLM required)
- Cosine similarity for retrieval
- Memory initialization at agent node start
- Context-aware handoffs
"""

import json
import re
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from collections import Counter
import math


class AgenticRAGService:
    """
    Agentic RAG service for research-type solutions.
    Lightweight implementation using TF-IDF and cosine similarity.
    """
    
    def __init__(self):
        """Initialize Agentic RAG service without LLM dependency."""
        # In-memory storage for workflow outputs
        self.workflow_memory: Dict[str, List[Dict[str, Any]]] = {}
        self.solution_contexts: Dict[str, Dict[str, Any]] = {}
        
        # Simple stopwords for text processing
        self.stopwords = set([
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'been', 'be',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those'
        ])
    
    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization."""
        # Convert to lowercase and split on non-alphanumeric
        tokens = re.findall(r'\b\w+\b', text.lower())
        # Remove stopwords
        return [t for t in tokens if t not in self.stopwords and len(t) > 2]
    
    def _chunk_text(self, text: str, chunk_size: int = 200) -> List[str]:
        """
        Simple chunking strategy: split text into chunks of approximately chunk_size words.
        """
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size):
            chunk = ' '.join(words[i:i + chunk_size])
            if chunk.strip():
                chunks.append(chunk)
        
        return chunks if chunks else [text]
    
    def _compute_tfidf(self, documents: List[str]) -> Tuple[List[Dict[str, float]], Dict[str, float]]:
        """
        Compute TF-IDF vectors for documents.
        Returns: (tfidf_vectors, idf_scores)
        """
        # Tokenize all documents
        tokenized_docs = [self._tokenize(doc) for doc in documents]
        
        # Calculate document frequency
        df = Counter()
        for tokens in tokenized_docs:
            unique_tokens = set(tokens)
            for token in unique_tokens:
                df[token] += 1
        
        # Calculate IDF
        num_docs = len(documents)
        idf = {
            token: math.log(num_docs / (freq + 1)) + 1
            for token, freq in df.items()
        }
        
        # Calculate TF-IDF for each document
        tfidf_vectors = []
        for tokens in tokenized_docs:
            # Term frequency
            tf = Counter(tokens)
            total_terms = len(tokens)
            
            # TF-IDF vector
            tfidf = {}
            for term, count in tf.items():
                tf_score = count / total_terms if total_terms > 0 else 0
                tfidf[term] = tf_score * idf.get(term, 0)
            
            tfidf_vectors.append(tfidf)
        
        return tfidf_vectors, idf
    
    def _cosine_similarity(self, vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """Calculate cosine similarity between two TF-IDF vectors."""
        # Get common terms
        common_terms = set(vec1.keys()) & set(vec2.keys())
        
        if not common_terms:
            return 0.0
        
        # Calculate dot product
        dot_product = sum(vec1[term] * vec2[term] for term in common_terms)
        
        # Calculate magnitudes
        mag1 = math.sqrt(sum(v * v for v in vec1.values()))
        mag2 = math.sqrt(sum(v * v for v in vec2.values()))
        
        if mag1 == 0 or mag2 == 0:
            return 0.0
        
        return dot_product / (mag1 * mag2)
    
    def _extract_key_info(self, text: str) -> Dict[str, Any]:
        """
        Lightweight extraction of key information from text.
        No LLM - uses simple heuristics.
        """
        lines = text.split('\n')
        
        # Extract numbers and metrics (likely important data)
        numbers = re.findall(r'\$?[\d,]+\.?\d*%?', text)
        
        # Extract sentences with important keywords
        important_keywords = ['result', 'finding', 'conclusion', 'recommend', 'analysis', 'data', 'metric', 'performance']
        key_sentences = []
        
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in important_keywords):
                key_sentences.append(line.strip())
        
        # Get top terms by frequency (excluding stopwords)
        tokens = self._tokenize(text)
        term_freq = Counter(tokens).most_common(10)
        
        return {
            "key_metrics": numbers[:10],  # Top 10 numbers
            "key_sentences": key_sentences[:5],  # Top 5 important sentences
            "top_terms": [term for term, _ in term_freq],
            "text_length": len(text),
            "chunk_count": len(self._chunk_text(text))
        }
    
    def initialize_agent_memory(
        self, 
        solution_id: str, 
        workflow_id: str, 
        agent_node_id: str,
        workflow_description: str = ""
    ) -> Dict[str, Any]:
        """
        Initialize RAG memory for an agent node at the start of execution.
        Retrieves relevant context from previous workflows using TF-IDF similarity.
        
        Args:
            solution_id: ID of the solution
            workflow_id: ID of the current workflow
            agent_node_id: ID of the agent node being initialized
            workflow_description: Description of the workflow for context
            
        Returns:
            Dict with retrieved memory and context
        """
        print(f"🧠 [Agentic RAG] Initializing memory for agent {agent_node_id} in workflow {workflow_id}")
        
        # Get solution context
        solution_key = f"solution_{solution_id}"
        if solution_key not in self.workflow_memory or not self.workflow_memory[solution_key]:
            print(f"   No previous workflow memory found - starting fresh")
            return {
                "memory_type": "agentic_rag",
                "retrieved_context": None,
                "workflow_history": [],
                "relevant_facts": [],
                "retrieval_method": "none"
            }
        
        # Get previous workflow outputs
        workflow_history = self.workflow_memory[solution_key]
        
        # Create query from workflow description
        query_text = f"{workflow_id} {workflow_description}"
        
        # Retrieve relevant chunks using TF-IDF
        try:
            # Collect all text chunks from previous workflows
            all_chunks = []
            chunk_sources = []
            
            for record in workflow_history:
                output_text = record.get('raw_output', '')
                chunks = self._chunk_text(output_text)
                
                for chunk in chunks:
                    all_chunks.append(chunk)
                    chunk_sources.append({
                        'workflow_id': record['workflow_id'],
                        'workflow_name': record['workflow_name']
                    })
            
            if not all_chunks:
                print(f"   No chunks found in previous workflows")
                return {
                    "memory_type": "agentic_rag",
                    "retrieved_context": None,
                    "workflow_history": workflow_history,
                    "relevant_facts": []
                }
            
            # Compute TF-IDF for all chunks + query
            documents = all_chunks + [query_text]
            tfidf_vectors, _ = self._compute_tfidf(documents)
            
            # Query vector is the last one
            query_vector = tfidf_vectors[-1]
            chunk_vectors = tfidf_vectors[:-1]
            
            # Calculate similarity scores
            similarities = []
            for i, chunk_vector in enumerate(chunk_vectors):
                sim = self._cosine_similarity(query_vector, chunk_vector)
                similarities.append((i, sim, all_chunks[i], chunk_sources[i]))
            
            # Sort by similarity and get top 3
            similarities.sort(key=lambda x: x[1], reverse=True)
            top_chunks = similarities[:3]
            
            # Build retrieved context
            relevant_facts = []
            for idx, sim, chunk, source in top_chunks:
                if sim > 0.1:  # Threshold for relevance
                    relevant_facts.append({
                        'text': chunk[:200],  # First 200 chars
                        'source': source['workflow_name'],
                        'similarity': round(sim, 3)
                    })
            
            print(f"   ✅ Retrieved {len(relevant_facts)} relevant chunks from {len(workflow_history)} workflows")
            
            # Create summary of retrieved context
            context_summary = "\n".join([
                f"- {fact['text'][:100]}... (from {fact['source']}, relevance: {fact['similarity']})"
                for fact in relevant_facts
            ])
            
            return {
                "memory_type": "agentic_rag",
                "retrieved_context": {
                    "relevant_facts": relevant_facts,
                    "context_summary": context_summary,
                    "total_chunks_searched": len(all_chunks),
                    "retrieval_method": "tfidf_cosine"
                },
                "workflow_history_count": len(workflow_history),
                "relevant_facts": relevant_facts
            }
            
        except Exception as e:
            print(f"   ⚠️ Error retrieving context: {e}")
            return {
                "memory_type": "agentic_rag",
                "retrieved_context": None,
                "workflow_history": workflow_history,
                "relevant_facts": [],
                "error": str(e)
            }
    
    def store_workflow_output(
        self,
        solution_id: str,
        workflow_id: str,
        workflow_name: str,
        workflow_output: str,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Store workflow output in RAG memory with lightweight indexing.
        
        Args:
            solution_id: ID of the solution
            workflow_id: ID of the workflow
            workflow_name: Name of the workflow
            workflow_output: Raw output from workflow execution
            metadata: Additional metadata to store
            
        Returns:
            Dict with storage confirmation and extracted insights
        """
        print(f"💾 [Agentic RAG] Storing output for workflow {workflow_id}")
        
        solution_key = f"solution_{solution_id}"
        if solution_key not in self.workflow_memory:
            self.workflow_memory[solution_key] = []
        
        # Extract key information using lightweight methods
        try:
            insights = self._extract_key_info(workflow_output)
            
            # Store in memory
            workflow_record = {
                "workflow_id": workflow_id,
                "workflow_name": workflow_name,
                "timestamp": datetime.utcnow().isoformat(),
                "raw_output": workflow_output,
                "insights": insights,
                "metadata": metadata or {}
            }
            
            self.workflow_memory[solution_key].append(workflow_record)
            
            print(f"   ✅ Stored workflow output with {len(insights.get('key_sentences', []))} key sentences")
            print(f"   📊 Extracted {len(insights.get('key_metrics', []))} metrics")
            
            return {
                "stored": True,
                "workflow_id": workflow_id,
                "insights": insights,
                "total_workflows_in_memory": len(self.workflow_memory[solution_key])
            }
            
        except Exception as e:
            print(f"   ⚠️ Error storing workflow output: {e}")
            # Store raw output as fallback
            workflow_record = {
                "workflow_id": workflow_id,
                "workflow_name": workflow_name,
                "timestamp": datetime.utcnow().isoformat(),
                "raw_output": workflow_output,
                "metadata": metadata or {},
                "error": str(e)
            }
            self.workflow_memory[solution_key].append(workflow_record)
            
            return {
                "stored": True,
                "workflow_id": workflow_id,
                "error": str(e)
            }
    
    def prepare_rag_handoff(
        self,
        solution_id: str,
        source_workflow_id: str,
        target_workflow_id: str,
        target_workflow_description: str = ""
    ) -> Dict[str, Any]:
        """
        Prepare intelligent handoff from one workflow to another using lightweight RAG.
        
        Args:
            solution_id: ID of the solution
            source_workflow_id: ID of the source workflow
            target_workflow_id: ID of the target workflow
            target_workflow_description: Description of target workflow
            
        Returns:
            Dict with handoff data and relevant context
        """
        print(f"🤝 [Agentic RAG] Preparing handoff from {source_workflow_id} to {target_workflow_id}")
        
        solution_key = f"solution_{solution_id}"
        if solution_key not in self.workflow_memory or not self.workflow_memory[solution_key]:
            print(f"   ⚠️ No workflow memory found")
            return {
                "handoff_type": "agentic_rag",
                "source_workflow": source_workflow_id,
                "target_workflow": target_workflow_id,
                "handoff_data": "No previous context available"
            }
        
        # Get the source workflow's output
        source_output = None
        for record in reversed(self.workflow_memory[solution_key]):
            if record["workflow_id"] == source_workflow_id:
                source_output = record
                break
        
        if not source_output:
            print(f"   ⚠️ Source workflow output not found")
            return {
                "handoff_type": "agentic_rag",
                "source_workflow": source_workflow_id,
                "target_workflow": target_workflow_id,
                "handoff_data": "Source workflow output not available"
            }
        
        # Create handoff using extracted insights
        try:
            insights = source_output.get('insights', {})
            raw_output = source_output.get('raw_output', '')
            
            # Build concise handoff
            handoff_parts = []
            
            # Add key sentences
            if insights.get('key_sentences'):
                handoff_parts.append("KEY FINDINGS:")
                handoff_parts.extend(f"- {s}" for s in insights['key_sentences'][:3])
            
            # Add metrics
            if insights.get('key_metrics'):
                handoff_parts.append("\nIMPORTANT METRICS:")
                handoff_parts.append(", ".join(insights['key_metrics'][:5]))
            
            # Add top terms context
            if insights.get('top_terms'):
                handoff_parts.append(f"\nCONTEXT: Related to {', '.join(insights['top_terms'][:5])}")
            
            # Add brief raw output excerpt
            handoff_parts.append(f"\nSOURCE OUTPUT EXCERPT:\n{raw_output[:300]}...")
            
            handoff_data = "\n".join(handoff_parts)
            
            print(f"   ✅ Generated handoff with {len(handoff_data)} characters")
            
            return {
                "handoff_type": "agentic_rag",
                "source_workflow": source_workflow_id,
                "target_workflow": target_workflow_id,
                "handoff_data": handoff_data,
                "source_insights": insights,
                "timestamp": datetime.utcnow().isoformat(),
                "method": "lightweight_extraction"
            }
            
        except Exception as e:
            print(f"   ⚠️ Error creating handoff: {e}")
            return {
                "handoff_type": "agentic_rag",
                "source_workflow": source_workflow_id,
                "target_workflow": target_workflow_id,
                "handoff_data": source_output.get('raw_output', ''),
                "error": str(e)
            }
    
    def get_solution_summary(self, solution_id: str) -> str:
        """
        Generate comprehensive solution summary using lightweight aggregation.
        
        Args:
            solution_id: ID of the solution
            
        Returns:
            Comprehensive summary of all workflows in the solution
        """
        print(f"📋 [Agentic RAG] Generating solution summary for {solution_id}")
        
        solution_key = f"solution_{solution_id}"
        if solution_key not in self.workflow_memory or not self.workflow_memory[solution_key]:
            return "No workflow execution data available for this solution."
        
        workflow_history = self.workflow_memory[solution_key]
        
        try:
            summary_parts = []
            summary_parts.append(f"SOLUTION EXECUTION SUMMARY")
            summary_parts.append(f"=" * 60)
            summary_parts.append(f"Total Workflows Executed: {len(workflow_history)}")
            summary_parts.append("")
            
            # Aggregate all key information
            all_metrics = []
            all_key_sentences = []
            all_top_terms = []
            
            for i, record in enumerate(workflow_history, 1):
                workflow_name = record.get('workflow_name', 'Unknown')
                insights = record.get('insights', {})
                
                summary_parts.append(f"\n{i}. {workflow_name}")
                summary_parts.append("-" * 60)
                
                # Key sentences
                if insights.get('key_sentences'):
                    summary_parts.append("Key Findings:")
                    for sentence in insights['key_sentences'][:3]:
                        summary_parts.append(f"  • {sentence}")
                        all_key_sentences.append(sentence)
                
                # Metrics
                if insights.get('key_metrics'):
                    summary_parts.append(f"Metrics: {', '.join(insights['key_metrics'][:5])}")
                    all_metrics.extend(insights['key_metrics'][:5])
                
                # Top terms
                if insights.get('top_terms'):
                    all_top_terms.extend(insights['top_terms'])
            
            # Overall insights
            summary_parts.append(f"\n{'=' * 60}")
            summary_parts.append("OVERALL INSIGHTS")
            summary_parts.append(f"{'=' * 60}")
            
            # Most common terms across all workflows
            if all_top_terms:
                term_freq = Counter(all_top_terms).most_common(10)
                summary_parts.append("\nMost Common Topics:")
                for term, count in term_freq:
                    summary_parts.append(f"  • {term} (appeared {count} times)")
            
            # All metrics collected
            if all_metrics:
                summary_parts.append(f"\nAll Metrics Collected: {', '.join(set(all_metrics))}")
            
            # Key findings count
            summary_parts.append(f"\nTotal Key Findings: {len(all_key_sentences)}")
            
            summary = "\n".join(summary_parts)
            
            print(f"   ✅ Generated summary with {len(summary)} characters")
            
            return summary
            
        except Exception as e:
            print(f"   ⚠️ Error generating summary: {e}")
            # Fallback: concatenate all workflow outputs
            summary_parts = [f"Workflow Execution Summary for Solution {solution_id}\n"]
            for record in workflow_history:
                summary_parts.append(f"\n{record['workflow_name']}:")
                summary_parts.append(record['raw_output'][:300] + "...")
            return "\n".join(summary_parts)
    
    def clear_solution_memory(self, solution_id: str):
        """Clear all memory for a solution."""
        solution_key = f"solution_{solution_id}"
        if solution_key in self.workflow_memory:
            del self.workflow_memory[solution_key]
            print(f"🗑️ [Agentic RAG] Cleared memory for solution {solution_id}")


# Global instance
_agentic_rag_service = None


def get_agentic_rag_service() -> AgenticRAGService:
    """Get or create the global Agentic RAG service instance."""
    global _agentic_rag_service
    if _agentic_rag_service is None:
        _agentic_rag_service = AgenticRAGService()
    return _agentic_rag_service
