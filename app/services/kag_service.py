"""
Knowledge-Aided Generation (KAG) Service with LangGraph
Orchestrates fact extraction, reasoning, and memory management for workflow communication
"""
from typing import Dict, List, Any, Optional, TypedDict, Annotated
from datetime import datetime
import json
import operator

from langgraph.graph import StateGraph, END
from .gemini_client import get_gemini_client, GeminiResponse


class ConversationMemory:
    """Manages conversation memory for workflow chains"""
    
    def __init__(self):
        self.memories: Dict[str, List[Dict[str, Any]]] = {}
    
    def add_memory(self, solution_id: str, workflow_id: str, memory: Dict[str, Any]):
        """Add a memory entry for a workflow in a solution"""
        key = f"{solution_id}:{workflow_id}"
        if key not in self.memories:
            self.memories[key] = []
        
        self.memories[key].append({
            **memory,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_memories(self, solution_id: str, workflow_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get memories for a solution or specific workflow"""
        if workflow_id:
            key = f"{solution_id}:{workflow_id}"
            return self.memories.get(key, [])
        
        # Get all memories for the solution
        all_memories = []
        for key, memories in self.memories.items():
            if key.startswith(f"{solution_id}:"):
                all_memories.extend(memories)
        
        return sorted(all_memories, key=lambda x: x.get("timestamp", ""))
    
    def get_solution_context(self, solution_id: str) -> str:
        """Get full context summary for a solution"""
        memories = self.get_memories(solution_id)
        if not memories:
            return ""
        
        context_parts = []
        for mem in memories:
            context_parts.append(f"[{mem.get('workflow_name', 'Unknown')}]: {mem.get('summary', '')}")
        
        return "\n".join(context_parts)
    
    def clear_solution(self, solution_id: str):
        """Clear all memories for a solution"""
        keys_to_delete = [key for key in self.memories.keys() if key.startswith(f"{solution_id}:")]
        for key in keys_to_delete:
            del self.memories[key]


# Global conversation memory store
_conversation_memory = ConversationMemory()


def get_conversation_memory() -> ConversationMemory:
    """Get the global conversation memory instance"""
    return _conversation_memory


# LangGraph State Definition
class KAGState(TypedDict):
    """State for KAG LangGraph workflow"""
    workflow_output: str
    workflow_name: str
    solution_id: str
    workflow_id: str
    context: str
    previous_context: str
    facts: List[str]
    summary: str
    reasoning: str
    memory_stored: bool
    error: Optional[str]


class KAGService:
    """Knowledge-Aided Generation Service using LangGraph for workflow intelligence"""
    
    def __init__(self):
        self.gemini_client = get_gemini_client()
        self.memory = get_conversation_memory()
        self.graph = self._build_kag_graph()
    
    def _build_kag_graph(self) -> StateGraph:
        """Build the LangGraph workflow for KAG processing"""
        
        workflow = StateGraph(KAGState)
        
        # Define nodes
        workflow.add_node("retrieve_context", self._retrieve_context_node)
        workflow.add_node("extract_facts", self._extract_facts_node)
        workflow.add_node("generate_summary", self._generate_summary_node)
        workflow.add_node("store_memory", self._store_memory_node)
        
        # Define edges
        workflow.set_entry_point("retrieve_context")
        workflow.add_edge("retrieve_context", "extract_facts")
        workflow.add_edge("extract_facts", "generate_summary")
        workflow.add_edge("generate_summary", "store_memory")
        workflow.add_edge("store_memory", END)
        
        return workflow.compile()
    
    def _retrieve_context_node(self, state: KAGState) -> Dict[str, Any]:
        """Node 1: Retrieve previous context from memory"""
        try:
            previous_context = self.memory.get_solution_context(state["solution_id"])
            
            # Build full context
            full_context = state.get("context", "")
            if previous_context:
                full_context = f"{full_context}\n\nPrevious workflows:\n{previous_context}"
            
            return {
                "previous_context": previous_context,
                "context": full_context
            }
        except Exception as e:
            return {"error": f"Context retrieval failed: {str(e)}"}
    
    def _extract_facts_node(self, state: KAGState) -> Dict[str, Any]:
        """Node 2: Extract facts using Gemini"""
        if state.get("error"):
            return {}
        
        try:
            result: GeminiResponse = self.gemini_client.extract_facts(
                state["workflow_output"], 
                state["context"]
            )
            
            return {
                "facts": result.facts,
                "reasoning": result.reasoning
            }
        except Exception as e:
            return {"error": f"Fact extraction failed: {str(e)}"}
    
    def _generate_summary_node(self, state: KAGState) -> Dict[str, Any]:
        """Node 3: Generate summary from facts"""
        if state.get("error"):
            return {}
        
        try:
            # Use Gemini to generate summary
            summary_prompt = f"""Based on the following facts and workflow output, generate a concise summary:

Workflow: {state['workflow_name']}
Facts: {', '.join(state.get('facts', []))}
Output: {state['workflow_output'][:500]}

Generate a 2-3 sentence summary."""
            
            result = self.gemini_client.generate_content(summary_prompt)
            
            return {"summary": result.content}
        except Exception as e:
            # Fallback summary
            return {"summary": f"Workflow {state['workflow_name']} completed processing"}
    
    def _store_memory_node(self, state: KAGState) -> Dict[str, Any]:
        """Node 4: Store results in memory"""
        if state.get("error"):
            return {"memory_stored": False}
        
        try:
            memory_entry = {
                "workflow_id": state["workflow_id"],
                "workflow_name": state["workflow_name"],
                "summary": state.get("summary", ""),
                "facts": state.get("facts", []),
                "reasoning": state.get("reasoning", ""),
                "raw_output": state["workflow_output"][:500]
            }
            
            self.memory.add_memory(
                state["solution_id"], 
                state["workflow_id"], 
                memory_entry
            )
            
            return {"memory_stored": True}
        except Exception as e:
            return {
                "memory_stored": False,
                "error": f"Memory storage failed: {str(e)}"
            }
    
    def invoke_kag(self, 
                   workflow_output: str,
                   workflow_name: str,
                   solution_id: str,
                   workflow_id: str,
                   context: str = "") -> Dict[str, Any]:
        """
        Main KAG invocation using LangGraph: Extract facts, generate summary, and store in memory
        
        Args:
            workflow_output: Raw output from workflow execution
            workflow_name: Name of the workflow
            solution_id: ID of the solution this workflow belongs to
            workflow_id: ID of the workflow
            context: Additional context
            
        Returns:
            Dict with summary, facts, reasoning, and memory reference
        """
        # Initialize state
        initial_state: KAGState = {
            "workflow_output": workflow_output,
            "workflow_name": workflow_name,
            "solution_id": solution_id,
            "workflow_id": workflow_id,
            "context": context,
            "previous_context": "",
            "facts": [],
            "summary": "",
            "reasoning": "",
            "memory_stored": False,
            "error": None
        }
        
        # Execute LangGraph workflow
        final_state = self.graph.invoke(initial_state)
        
        # Handle errors
        if final_state.get("error"):
            return {
                "summary": f"Error in KAG processing: {final_state['error']}",
                "facts": [],
                "reasoning": "",
                "memory_stored": False,
                "context_available": False,
                "error": final_state["error"]
            }
        
        return {
            "summary": final_state.get("summary", ""),
            "facts": final_state.get("facts", []),
            "reasoning": final_state.get("reasoning", ""),
            "memory_stored": final_state.get("memory_stored", False),
            "context_available": bool(final_state.get("previous_context"))
        }
    
    def prepare_handoff(self,
                       source_workflow_id: str,
                       target_workflow_id: str,
                       target_workflow_description: str,
                       solution_id: str) -> Dict[str, Any]:
        """
        Prepare data handoff from source workflow to target workflow
        
        Args:
            source_workflow_id: ID of source workflow
            target_workflow_id: ID of target workflow
            target_workflow_description: Description of target workflow task
            solution_id: Solution ID
            
        Returns:
            Handoff data package with context and instructions
        """
        # Get source workflow memories
        source_memories = self.memory.get_memories(solution_id, source_workflow_id)
        
        if not source_memories:
            return {
                "handoff_data": "",
                "relevance": "No previous context available",
                "context": "",
                "facts": []
            }
        
        # Get the most recent memory
        latest_memory = source_memories[-1]
        
        # Use Gemini to reason about the handoff
        handoff_reasoning = self.gemini_client.reason_about_handoff(
            source_workflow_summary=latest_memory.get("summary", ""),
            source_facts=latest_memory.get("facts", []),
            target_workflow_description=target_workflow_description
        )
        
        return {
            **handoff_reasoning,
            "facts": latest_memory.get("facts", []),
            "source_summary": latest_memory.get("summary", "")
        }
    
    def get_solution_summary(self, solution_id: str) -> Dict[str, Any]:
        """
        Get comprehensive summary of all workflows in a solution
        
        Args:
            solution_id: Solution ID
            
        Returns:
            Summary data
        """
        all_memories = self.memory.get_memories(solution_id)
        
        if not all_memories:
            return {
                "total_workflows": 0,
                "summaries": [],
                "combined_facts": [],
                "overall_context": ""
            }
        
        summaries = []
        all_facts = []
        
        for mem in all_memories:
            summaries.append({
                "workflow_name": mem.get("workflow_name", "Unknown"),
                "summary": mem.get("summary", ""),
                "timestamp": mem.get("timestamp", "")
            })
            all_facts.extend(mem.get("facts", []))
        
        # Generate overall context using Gemini
        context_text = "\n\n".join([
            f"{s['workflow_name']}: {s['summary']}"
            for s in summaries
        ])
        
        overall_summary = self.gemini_client.summarize_conversation(
            [{"role": "workflow", "content": context_text}],
            f"Solution with {len(summaries)} workflows"
        )
        
        return {
            "total_workflows": len(summaries),
            "summaries": summaries,
            "combined_facts": all_facts,
            "overall_context": overall_summary
        }
    
    def clear_solution_memory(self, solution_id: str):
        """Clear all memory for a solution"""
        self.memory.clear_solution(solution_id)


# Global KAG service instance
_kag_service = None


def get_kag_service() -> KAGService:
    """Get or create the global KAG service instance"""
    global _kag_service
    if _kag_service is None:
        _kag_service = KAGService()
    return _kag_service


def invoke_kag(workflow_output: str,
               workflow_name: str,
               solution_id: str,
               workflow_id: str,
               context: str = "") -> Dict[str, Any]:
    """
    Convenience function to invoke KAG
    
    This is the main entry point for workflow-to-workflow communication
    """
    service = get_kag_service()
    return service.invoke_kag(workflow_output, workflow_name, solution_id, workflow_id, context)
