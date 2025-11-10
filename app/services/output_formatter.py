"""
Output Formatter Service
Transforms raw workflow execution results into clean, structured, user-friendly formats.
"""

from typing import Dict, Any, List
from datetime import datetime


class OutputFormatter:
    """Format workflow execution results for better readability."""
    
    @staticmethod
    def format_workflow_result(result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform raw workflow result into structured, user-friendly format.
        
        Args:
            result: Raw workflow execution result
            
        Returns:
            Formatted result with clean structure
        """
        workflow_id = result.get("workflow_id", "unknown")
        run_id = result.get("run_id", "unknown")
        status = result.get("status", "unknown")
        
        # Extract clean summary
        formatted = {
            "workflow_id": workflow_id,
            "run_id": run_id,
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "summary": OutputFormatter._generate_summary(result),
            "results": OutputFormatter._format_results(result.get("result", {})),
            "metadata": {
                "total_nodes": len(result.get("result", {})),
                "agents_used": result.get("meta", {}).get("agents_used", []),
                "execution_steps": result.get("meta", {}).get("total_messages", 0)
            }
        }
        
        # Add error if present
        if result.get("error"):
            formatted["error"] = result["error"]
            formatted["status"] = "failed"
        
        return formatted
    
    @staticmethod
    def _generate_summary(result: Dict[str, Any]) -> str:
        """Generate a concise summary of the workflow execution."""
        status = result.get("status", "unknown")
        node_count = len(result.get("result", {}))
        
        if status == "success":
            return f"Workflow completed successfully. Executed {node_count} node(s)."
        elif status == "failed":
            error = result.get("error", "Unknown error")
            return f"Workflow failed: {error}"
        else:
            return f"Workflow status: {status}"
    
    @staticmethod
    def _format_results(raw_results: Dict[str, Any]) -> Dict[str, Any]:
        """Format individual node results into clean structure."""
        formatted_results = {}
        
        for node_id, node_result in raw_results.items():
            formatted_results[node_id] = {
                "node_id": node_id,
                "agent": node_result.get("agent_name", node_result.get("agent_id", "unknown")),
                "task": node_result.get("task", ""),
                "response": OutputFormatter._extract_response(node_result),
                "tools_executed": OutputFormatter._format_tool_results(
                    node_result.get("tool_results", {})
                )
            }
        
        return formatted_results
    
    @staticmethod
    def _extract_response(node_result: Dict[str, Any]) -> str:
        """Extract the main LLM response from node result."""
        llm_response = node_result.get("llm_response", "")
        
        # Clean up the response - remove excessive technical details
        if isinstance(llm_response, str):
            # Limit length for summary
            max_length = 1000
            if len(llm_response) > max_length:
                return llm_response[:max_length] + "... (truncated)"
            return llm_response
        
        return str(llm_response)
    
    @staticmethod
    def _format_tool_results(tool_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Format tool execution results into clean structure."""
        formatted_tools = []
        
        for tool_id, tool_result in tool_results.items():
            if isinstance(tool_result, dict):
                formatted_tool = {
                    "tool": tool_id,
                    "status": "success" if tool_result.get("success") else "executed",
                    "summary": OutputFormatter._summarize_tool_result(tool_result)
                }
                formatted_tools.append(formatted_tool)
        
        return formatted_tools
    
    @staticmethod
    def _summarize_tool_result(tool_result: Dict[str, Any]) -> str:
        """Create a brief summary of tool execution result."""
        # For web search tools
        if "results" in tool_result:
            results = tool_result.get("results", [])
            count = len(results) if isinstance(results, list) else tool_result.get("count", 0)
            return f"Found {count} results"
        
        # For API tools
        if "data" in tool_result or "json" in tool_result:
            return "API call completed successfully"
        
        # For general tools
        if "output" in tool_result:
            output = str(tool_result.get("output", ""))
            if len(output) > 100:
                return output[:100] + "..."
            return output
        
        # For tool orchestrator format
        if tool_result.get("tool"):
            tool_name = tool_result.get("tool")
            query_info = tool_result.get("query", "")
            count = tool_result.get("count", 0)
            
            if count > 0:
                return f"{tool_name}: {count} results"
            return f"{tool_name} executed"
        
        return "Executed successfully"
    
    @staticmethod
    def format_for_display(result: Dict[str, Any]) -> str:
        """
        Format result as readable text output.
        
        Args:
            result: Formatted workflow result
            
        Returns:
            Human-readable text representation
        """
        lines = []
        lines.append("=" * 80)
        lines.append(f"WORKFLOW EXECUTION REPORT")
        lines.append("=" * 80)
        lines.append(f"Workflow ID: {result.get('workflow_id')}")
        lines.append(f"Run ID: {result.get('run_id')}")
        lines.append(f"Status: {result.get('status', 'unknown').upper()}")
        lines.append(f"Timestamp: {result.get('timestamp')}")
        lines.append("")
        
        # Summary
        lines.append("SUMMARY")
        lines.append("-" * 80)
        lines.append(result.get('summary', 'No summary available'))
        lines.append("")
        
        # Results
        lines.append("DETAILED RESULTS")
        lines.append("-" * 80)
        
        results = result.get('results', {})
        for node_id, node_data in results.items():
            lines.append(f"\n[{node_id}]")
            lines.append(f"  Agent: {node_data.get('agent')}")
            lines.append(f"  Task: {node_data.get('task')}")
            lines.append(f"  Response:")
            
            response = node_data.get('response', '')
            # Indent response
            for line in response.split('\n'):
                lines.append(f"    {line}")
            
            # Tool results
            tools = node_data.get('tools_executed', [])
            if tools:
                lines.append(f"  Tools Used:")
                for tool in tools:
                    lines.append(f"    - {tool.get('tool')}: {tool.get('summary')}")
            lines.append("")
        
        # Metadata
        metadata = result.get('metadata', {})
        lines.append("EXECUTION METADATA")
        lines.append("-" * 80)
        lines.append(f"Total Nodes: {metadata.get('total_nodes', 0)}")
        lines.append(f"Agents Used: {', '.join(metadata.get('agents_used', []))}")
        lines.append(f"Execution Steps: {metadata.get('execution_steps', 0)}")
        
        # Error if present
        if result.get('error'):
            lines.append("")
            lines.append("ERROR")
            lines.append("-" * 80)
            lines.append(result.get('error'))
        
        lines.append("")
        lines.append("=" * 80)
        
        return "\n".join(lines)
    
    @staticmethod
    def format_compact(result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a compact version of the result with only essential information.
        
        Args:
            result: Formatted workflow result
            
        Returns:
            Compact result dictionary
        """
        compact = {
            "workflow_id": result.get("workflow_id"),
            "run_id": result.get("run_id"),
            "status": result.get("status"),
            "summary": result.get("summary"),
            "node_responses": {}
        }
        
        # Extract just the responses from each node
        results = result.get("results", {})
        for node_id, node_data in results.items():
            compact["node_responses"][node_id] = {
                "agent": node_data.get("agent"),
                "response": node_data.get("response")
            }
        
        if result.get("error"):
            compact["error"] = result["error"]
        
        return compact


# Global formatter instance
output_formatter = OutputFormatter()
