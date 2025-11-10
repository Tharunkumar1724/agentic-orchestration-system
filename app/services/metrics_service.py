"""
Comprehensive metrics tracking service for workflows, solutions, and chat.

Tracks:
- Accuracy
- Response Quality
- Hallucination Rate
- Task Completion Rate
- Token Usage
- Latency
- Tool Invocation Count
- Retrieval Errors
- Decision Depth
- Branching Factor
- Context Relation Quality
- Tool Success Rate
"""

import time
from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class MetricsData(BaseModel):
    """Comprehensive metrics for workflow/solution/chat execution."""
    
    # Performance Metrics
    latency_ms: float = Field(0.0, description="Total execution time in milliseconds")
    token_usage_count: int = Field(0, description="Total tokens used (input + output)")
    token_input_count: int = Field(0, description="Input tokens used")
    token_output_count: int = Field(0, description="Output tokens used")
    
    # Quality Metrics
    accuracy: float = Field(0.0, description="Estimated accuracy score (0-100)")
    response_quality: float = Field(0.0, description="Response quality score (0-100)")
    hallucination_rate: float = Field(0.0, description="Estimated hallucination rate (0-100)")
    task_completion_rate: float = Field(0.0, description="Task completion percentage (0-100)")
    context_relation_quality: float = Field(0.0, description="Context relevance score (0-100)")
    
    # Tool & Execution Metrics
    tool_invocation_count: int = Field(0, description="Number of tools invoked")
    tool_success_rate: float = Field(0.0, description="Tool success rate (0-100)")
    retrieval_error_count: int = Field(0, description="Number of retrieval/tool errors")
    
    # Decision & Structure Metrics
    decision_depth: int = Field(0, description="Depth of decision tree traversed")
    branching_factor: float = Field(0.0, description="Average branching in execution graph")
    
    # Detailed Breakdown
    agent_execution_count: int = Field(0, description="Number of agents executed")
    workflow_step_count: int = Field(0, description="Number of workflow steps executed")
    
    # Timestamps
    start_time: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    end_time: Optional[str] = None
    
    # Additional Details
    errors: List[str] = Field(default_factory=list, description="List of errors encountered")
    warnings: List[str] = Field(default_factory=list, description="List of warnings")


class MetricsTracker:
    """Tracks metrics during execution."""
    
    def __init__(self):
        self.start_time: float = 0
        self.end_time: float = 0
        self.token_count: int = 0
        self.token_input: int = 0
        self.token_output: int = 0
        self.tool_invocations: List[Dict[str, Any]] = []
        self.agent_executions: List[Dict[str, Any]] = []
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.steps_executed: int = 0
        self.decision_points: int = 0
        self.branches_taken: List[int] = []
    
    def start(self):
        """Start tracking."""
        self.start_time = time.time()
    
    def end(self):
        """End tracking."""
        self.end_time = time.time()
    
    def add_token_usage(self, input_tokens: int, output_tokens: int):
        """Track token usage."""
        self.token_input += input_tokens
        self.token_output += output_tokens
        self.token_count += input_tokens + output_tokens
    
    def add_tool_invocation(self, tool_id: str, success: bool, error: Optional[str] = None):
        """Track tool invocation."""
        self.tool_invocations.append({
            "tool_id": tool_id,
            "success": success,
            "error": error,
            "timestamp": time.time()
        })
    
    def add_agent_execution(self, agent_id: str, success: bool, tokens_used: int = 0):
        """Track agent execution."""
        self.agent_executions.append({
            "agent_id": agent_id,
            "success": success,
            "tokens_used": tokens_used,
            "timestamp": time.time()
        })
    
    def add_error(self, error: str):
        """Track error."""
        self.errors.append(error)
    
    def add_warning(self, warning: str):
        """Track warning."""
        self.warnings.append(warning)
    
    def add_step(self):
        """Increment step count."""
        self.steps_executed += 1
    
    def add_decision(self, branches_available: int):
        """Track decision point."""
        self.decision_points += 1
        self.branches_taken.append(branches_available)
    
    def calculate_metrics(self, task_completed: bool = True, context_quality: Optional[float] = None) -> MetricsData:
        """Calculate final metrics from tracked data."""
        
        # Calculate latency
        latency = (self.end_time - self.start_time) * 1000 if self.end_time > 0 else 0
        
        # Calculate tool metrics
        tool_count = len(self.tool_invocations)
        successful_tools = sum(1 for t in self.tool_invocations if t["success"])
        tool_success_rate = (successful_tools / tool_count * 100) if tool_count > 0 else 0
        retrieval_errors = sum(1 for t in self.tool_invocations if not t["success"])
        
        # Calculate task completion rate
        task_completion = 100.0 if task_completed else 0.0
        if task_completed and len(self.errors) > 0:
            # Partial completion if there were errors
            task_completion = max(50.0, 100.0 - (len(self.errors) * 10))
        
        # Calculate accuracy (heuristic based on success rates and errors)
        accuracy = 0.0
        if tool_count > 0 or len(self.agent_executions) > 0:
            # Base accuracy on tool success and absence of errors
            accuracy = tool_success_rate
            if len(self.errors) > 0:
                accuracy = max(0, accuracy - (len(self.errors) * 10))
            if len(self.agent_executions) > 0:
                agent_success = sum(1 for a in self.agent_executions if a["success"])
                agent_rate = (agent_success / len(self.agent_executions)) * 100
                accuracy = (accuracy + agent_rate) / 2
        else:
            accuracy = 100.0 if task_completed and len(self.errors) == 0 else 50.0
        
        # Calculate response quality (based on token usage, completion, and errors)
        response_quality = 70.0  # Base quality
        if task_completed:
            response_quality += 20.0
        if len(self.errors) == 0:
            response_quality += 10.0
        if self.token_count > 0:
            # Higher token usage might indicate more detailed response
            if self.token_output > 500:
                response_quality = min(100, response_quality + 5)
        response_quality = max(0, response_quality - (len(self.errors) * 5))
        
        # Calculate hallucination rate (heuristic - lower is better)
        # Factors: errors, tool failures, context quality
        hallucination_rate = 0.0
        if len(self.errors) > 0:
            hallucination_rate += len(self.errors) * 5
        if tool_count > 0:
            failed_tools = tool_count - successful_tools
            hallucination_rate += (failed_tools / tool_count) * 20
        if context_quality is not None and context_quality < 70:
            hallucination_rate += (70 - context_quality) * 0.3
        hallucination_rate = min(100, hallucination_rate)
        
        # Calculate context relation quality
        if context_quality is not None:
            context_relation = context_quality
        else:
            # Estimate based on tool success and agent performance
            context_relation = 80.0  # Base
            if tool_success_rate > 0:
                context_relation = (context_relation + tool_success_rate) / 2
            if len(self.errors) > 0:
                context_relation = max(0, context_relation - (len(self.errors) * 10))
        
        # Calculate decision depth and branching factor
        decision_depth = self.decision_points
        branching_factor = (sum(self.branches_taken) / len(self.branches_taken)) if self.branches_taken else 1.0
        
        return MetricsData(
            latency_ms=round(latency, 2),
            token_usage_count=self.token_count,
            token_input_count=self.token_input,
            token_output_count=self.token_output,
            accuracy=round(accuracy, 2),
            response_quality=round(response_quality, 2),
            hallucination_rate=round(hallucination_rate, 2),
            task_completion_rate=round(task_completion, 2),
            context_relation_quality=round(context_relation, 2),
            tool_invocation_count=tool_count,
            tool_success_rate=round(tool_success_rate, 2),
            retrieval_error_count=retrieval_errors,
            decision_depth=decision_depth,
            branching_factor=round(branching_factor, 2),
            agent_execution_count=len(self.agent_executions),
            workflow_step_count=self.steps_executed,
            start_time=datetime.fromtimestamp(self.start_time).isoformat() if self.start_time > 0 else datetime.utcnow().isoformat(),
            end_time=datetime.fromtimestamp(self.end_time).isoformat() if self.end_time > 0 else None,
            errors=self.errors,
            warnings=self.warnings
        )


# Global metrics tracker factory
def create_metrics_tracker() -> MetricsTracker:
    """Create a new metrics tracker instance."""
    return MetricsTracker()
