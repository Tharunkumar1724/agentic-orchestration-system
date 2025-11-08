"""
Solution Service - Manages workflow communication and memory transfer within solutions.
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
import copy


class SolutionService:
    """Service for managing solution-level operations and workflow orchestration."""
    
    def __init__(self):
        self.active_solutions: Dict[str, Dict[str, Any]] = {}
        self.communication_buffers: Dict[str, List[Dict[str, Any]]] = {}
    
    def initialize_solution_runtime(self, solution_id: str, solution_data: Dict[str, Any]):
        """Initialize runtime context for a solution."""
        self.active_solutions[solution_id] = {
            "id": solution_id,
            "workflows": solution_data.get("workflows", []),
            "shared_memory": solution_data.get("workflow_memory", {}),
            "communication_config": solution_data.get("communication_config", {}),
            "active_workflows": {},  # Track currently running workflows
            "runtime_started": datetime.utcnow().isoformat()
        }
        self.communication_buffers[solution_id] = []
    
    def transfer_memory_between_workflows(
        self,
        solution_id: str,
        from_workflow_id: str,
        to_workflow_id: str,
        memory_to_transfer: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Transfer conversation memory from one workflow to another within a solution."""
        if solution_id not in self.active_solutions:
            raise ValueError(f"Solution '{solution_id}' not initialized")
        
        solution = self.active_solutions[solution_id]
        
        # Get or create workflow-specific memory
        if "workflow_memories" not in solution["shared_memory"]:
            solution["shared_memory"]["workflow_memories"] = {}
        
        # Extract memory from source workflow
        source_memory = solution["shared_memory"]["workflow_memories"].get(from_workflow_id, {})
        
        # Merge with memory to transfer
        if memory_to_transfer:
            source_memory = {**source_memory, **memory_to_transfer}
        
        # Transfer to target workflow
        target_memory = solution["shared_memory"]["workflow_memories"].get(to_workflow_id, {})
        
        # Intelligent merge - preserve important context
        transferred_memory = {
            "previous_workflow": from_workflow_id,
            "transfer_timestamp": datetime.utcnow().isoformat(),
            "conversation_context": source_memory.get("conversation_context", {}),
            "user_preferences": source_memory.get("user_preferences", {}),
            "session_data": source_memory.get("session_data", {}),
            "inherited_context": target_memory.get("inherited_context", []),
        }
        
        # Add transfer record
        if "transfer_history" not in transferred_memory["inherited_context"]:
            transferred_memory["inherited_context"] = []
        
        transferred_memory["inherited_context"].append({
            "from": from_workflow_id,
            "at": datetime.utcnow().isoformat(),
            "context_size": len(str(source_memory))
        })
        
        # Update target workflow memory
        solution["shared_memory"]["workflow_memories"][to_workflow_id] = {
            **target_memory,
            **transferred_memory
        }
        
        return transferred_memory
    
    def send_workflow_message(
        self,
        solution_id: str,
        from_workflow_id: str,
        to_workflow_id: str,
        message_type: str,
        payload: Dict[str, Any]
    ):
        """Send a message from one workflow to another."""
        if solution_id not in self.communication_buffers:
            self.communication_buffers[solution_id] = []
        
        message = {
            "from_workflow_id": from_workflow_id,
            "to_workflow_id": to_workflow_id,
            "message_type": message_type,
            "payload": payload,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "sent"
        }
        
        self.communication_buffers[solution_id].append(message)
        
        # Update shared memory
        if solution_id in self.active_solutions:
            if "communication_log" not in self.active_solutions[solution_id]["shared_memory"]:
                self.active_solutions[solution_id]["shared_memory"]["communication_log"] = []
            self.active_solutions[solution_id]["shared_memory"]["communication_log"].append(message)
        
        return message
    
    def get_workflow_messages(self, solution_id: str, workflow_id: str) -> List[Dict[str, Any]]:
        """Get all messages for a specific workflow."""
        if solution_id not in self.communication_buffers:
            return []
        
        return [
            msg for msg in self.communication_buffers[solution_id]
            if msg["to_workflow_id"] == workflow_id
        ]
    
    def get_shared_memory(self, solution_id: str, workflow_id: Optional[str] = None) -> Dict[str, Any]:
        """Get shared memory for a solution or specific workflow."""
        if solution_id not in self.active_solutions:
            return {}
        
        shared_memory = self.active_solutions[solution_id]["shared_memory"]
        
        if workflow_id:
            return shared_memory.get("workflow_memories", {}).get(workflow_id, {})
        
        return shared_memory
    
    def update_shared_memory(
        self,
        solution_id: str,
        workflow_id: str,
        memory_update: Dict[str, Any]
    ):
        """Update shared memory for a workflow."""
        if solution_id not in self.active_solutions:
            raise ValueError(f"Solution '{solution_id}' not initialized")
        
        solution = self.active_solutions[solution_id]
        
        if "workflow_memories" not in solution["shared_memory"]:
            solution["shared_memory"]["workflow_memories"] = {}
        
        if workflow_id not in solution["shared_memory"]["workflow_memories"]:
            solution["shared_memory"]["workflow_memories"][workflow_id] = {}
        
        # Deep merge
        current_memory = solution["shared_memory"]["workflow_memories"][workflow_id]
        solution["shared_memory"]["workflow_memories"][workflow_id] = {
            **current_memory,
            **memory_update,
            "last_updated": datetime.utcnow().isoformat()
        }
    
    def get_communication_blueprint(self, solution_id: str) -> Dict[str, Any]:
        """Generate a blueprint showing all workflow communications."""
        if solution_id not in self.active_solutions:
            return {"workflows": [], "communications": []}
        
        solution = self.active_solutions[solution_id]
        communications = self.communication_buffers.get(solution_id, [])
        
        # Build workflow graph
        workflow_nodes = {}
        for wf_id in solution["workflows"]:
            workflow_nodes[wf_id] = {
                "id": wf_id,
                "sent_messages": 0,
                "received_messages": 0,
                "connections": set()
            }
        
        # Analyze communications
        communication_edges = []
        for comm in communications:
            from_id = comm["from_workflow_id"]
            to_id = comm["to_workflow_id"]
            
            if from_id in workflow_nodes:
                workflow_nodes[from_id]["sent_messages"] += 1
                workflow_nodes[from_id]["connections"].add(to_id)
            
            if to_id in workflow_nodes:
                workflow_nodes[to_id]["received_messages"] += 1
            
            communication_edges.append({
                "from": from_id,
                "to": to_id,
                "type": comm["message_type"],
                "timestamp": comm["timestamp"]
            })
        
        # Convert sets to lists for JSON serialization
        for node in workflow_nodes.values():
            node["connections"] = list(node["connections"])
        
        return {
            "solution_id": solution_id,
            "workflows": list(workflow_nodes.values()),
            "communications": communication_edges,
            "total_messages": len(communications),
            "active_workflows": list(solution["active_workflows"].keys())
        }
    
    def cleanup_solution(self, solution_id: str):
        """Cleanup solution runtime resources."""
        if solution_id in self.active_solutions:
            del self.active_solutions[solution_id]
        if solution_id in self.communication_buffers:
            del self.communication_buffers[solution_id]


# Global solution service instance
solution_service = SolutionService()
