"""
Advanced Tool Orchestration System
Handles all types of tools with complex execution strategies
"""

import asyncio
import httpx
import json
import subprocess
import os
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
from enum import Enum


class ToolType(Enum):
    """All supported tool types"""
    WEBSEARCH = "websearch"
    API = "api"
    CODE = "code"
    DATABASE = "database"
    FILE = "file"
    PYTHON = "python"
    SHELL = "shell"
    HTTP = "http"
    GRAPHQL = "graphql"
    CUSTOM = "custom"


class ToolExecutionStrategy(Enum):
    """Tool execution strategies"""
    SEQUENTIAL = "sequential"  # Execute one after another
    PARALLEL = "parallel"      # Execute all at once
    CONDITIONAL = "conditional"  # Execute based on conditions
    RETRY = "retry"            # Retry on failure
    FALLBACK = "fallback"      # Use fallback on failure


class ToolResult:
    """Standardized tool execution result"""
    def __init__(
        self,
        success: bool,
        data: Any = None,
        error: Optional[str] = None,
        metadata: Optional[Dict] = None,
        execution_time: float = 0.0
    ):
        self.success = success
        self.data = data
        self.error = error
        self.metadata = metadata or {}
        self.execution_time = execution_time
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "metadata": self.metadata,
            "execution_time": self.execution_time,
            "timestamp": self.timestamp
        }


class ToolOrchestrator:
    """Advanced tool orchestration with multiple execution strategies"""
    
    def __init__(self):
        self.tool_handlers = {
            ToolType.WEBSEARCH: self._handle_websearch,
            ToolType.API: self._handle_api,
            ToolType.CODE: self._handle_code,
            ToolType.DATABASE: self._handle_database,
            ToolType.FILE: self._handle_file,
            ToolType.PYTHON: self._handle_python,
            ToolType.SHELL: self._handle_shell,
            ToolType.HTTP: self._handle_http,
            ToolType.GRAPHQL: self._handle_graphql,
            ToolType.CUSTOM: self._handle_custom,
        }
        self.execution_history: List[Dict] = []
    
    async def execute_tool(
        self,
        tool_def: Dict[str, Any],
        inputs: Dict[str, Any],
        context: Optional[Dict] = None
    ) -> ToolResult:
        """Execute a single tool with proper error handling"""
        start_time = datetime.now()
        
        try:
            tool_type = ToolType(tool_def.get("type", "custom"))
            handler = self.tool_handlers.get(tool_type, self._handle_custom)
            
            # Execute tool
            result_data = await handler(tool_def, inputs, context or {})
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            result = ToolResult(
                success=True,
                data=result_data,
                metadata={
                    "tool_id": tool_def.get("id"),
                    "tool_name": tool_def.get("name"),
                    "tool_type": tool_type.value
                },
                execution_time=execution_time
            )
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            result = ToolResult(
                success=False,
                error=str(e),
                metadata={
                    "tool_id": tool_def.get("id"),
                    "tool_name": tool_def.get("name"),
                },
                execution_time=execution_time
            )
        
        # Log execution
        self.execution_history.append({
            "tool_id": tool_def.get("id"),
            "result": result.to_dict(),
            "timestamp": datetime.now().isoformat()
        })
        
        return result
    
    async def execute_tools(
        self,
        tools: List[Dict[str, Any]],
        inputs: Dict[str, Any],
        strategy: ToolExecutionStrategy = ToolExecutionStrategy.SEQUENTIAL,
        context: Optional[Dict] = None
    ) -> List[ToolResult]:
        """Execute multiple tools with specified strategy"""
        
        if strategy == ToolExecutionStrategy.PARALLEL:
            return await self._execute_parallel(tools, inputs, context)
        elif strategy == ToolExecutionStrategy.SEQUENTIAL:
            return await self._execute_sequential(tools, inputs, context)
        elif strategy == ToolExecutionStrategy.CONDITIONAL:
            return await self._execute_conditional(tools, inputs, context)
        elif strategy == ToolExecutionStrategy.RETRY:
            return await self._execute_with_retry(tools, inputs, context)
        elif strategy == ToolExecutionStrategy.FALLBACK:
            return await self._execute_with_fallback(tools, inputs, context)
        else:
            return await self._execute_sequential(tools, inputs, context)
    
    # ===================== Execution Strategies =====================
    
    async def _execute_sequential(
        self,
        tools: List[Dict[str, Any]],
        inputs: Dict[str, Any],
        context: Optional[Dict]
    ) -> List[ToolResult]:
        """Execute tools one after another"""
        results = []
        accumulated_context = context or {}
        
        for tool in tools:
            result = await self.execute_tool(tool, inputs, accumulated_context)
            results.append(result)
            
            # Pass successful results to next tool
            if result.success:
                accumulated_context[f"prev_result_{tool.get('id')}"] = result.data
        
        return results
    
    async def _execute_parallel(
        self,
        tools: List[Dict[str, Any]],
        inputs: Dict[str, Any],
        context: Optional[Dict]
    ) -> List[ToolResult]:
        """Execute all tools simultaneously"""
        tasks = [
            self.execute_tool(tool, inputs, context)
            for tool in tools
        ]
        return await asyncio.gather(*tasks)
    
    async def _execute_conditional(
        self,
        tools: List[Dict[str, Any]],
        inputs: Dict[str, Any],
        context: Optional[Dict]
    ) -> List[ToolResult]:
        """Execute tools based on conditions"""
        results = []
        
        for tool in tools:
            # Check condition if exists
            condition = tool.get("condition")
            if condition:
                # Evaluate condition (simple example)
                should_execute = self._evaluate_condition(condition, context, results)
                if not should_execute:
                    continue
            
            result = await self.execute_tool(tool, inputs, context)
            results.append(result)
        
        return results
    
    async def _execute_with_retry(
        self,
        tools: List[Dict[str, Any]],
        inputs: Dict[str, Any],
        context: Optional[Dict],
        max_retries: int = 3
    ) -> List[ToolResult]:
        """Execute tools with retry on failure"""
        results = []
        
        for tool in tools:
            retry_count = 0
            result = None
            
            while retry_count < max_retries:
                result = await self.execute_tool(tool, inputs, context)
                
                if result.success:
                    break
                
                retry_count += 1
                if retry_count < max_retries:
                    await asyncio.sleep(0.5 * retry_count)  # Exponential backoff
            
            results.append(result)
        
        return results
    
    async def _execute_with_fallback(
        self,
        tools: List[Dict[str, Any]],
        inputs: Dict[str, Any],
        context: Optional[Dict]
    ) -> List[ToolResult]:
        """Execute tools with fallback options"""
        results = []
        
        for tool in tools:
            result = await self.execute_tool(tool, inputs, context)
            
            if not result.success:
                # Try fallback if defined
                fallback_tool = tool.get("fallback")
                if fallback_tool:
                    fallback_result = await self.execute_tool(fallback_tool, inputs, context)
                    results.append(fallback_result)
                else:
                    results.append(result)
            else:
                results.append(result)
        
        return results
    
    # ===================== Tool Handlers =====================
    
    async def _handle_websearch(
        self,
        tool_def: Dict[str, Any],
        inputs: Dict[str, Any],
        context: Dict
    ) -> Any:
        """Handle web search tools with DuckDuckGo"""
        from ddgs import DDGS
        
        config = tool_def.get("config", {})
        query = inputs.get("query") or inputs.get("q") or inputs.get("prompt") or inputs.get("task") or ""
        
        max_results = config.get("max_results", 5)
        region = config.get("region", "wt-wt")
        safesearch = config.get("safesearch", "moderate")
        timelimit = config.get("timelimit")
        
        with DDGS() as ddgs:
            results = list(ddgs.text(
                query=query,
                region=region,
                safesearch=safesearch,
                timelimit=timelimit,
                max_results=max_results
            ))
        
        return {
            "query": query,
            "count": len(results),
            "results": results,
            "metadata": {
                "region": region,
                "max_results": max_results
            }
        }
    
    async def _handle_api(
        self,
        tool_def: Dict[str, Any],
        inputs: Dict[str, Any],
        context: Dict
    ) -> Any:
        """Handle API calls with proper HTTP methods"""
        config = tool_def.get("config", {})
        url = config.get("url")
        method = config.get("method", "GET").upper()
        headers = config.get("headers", {})
        timeout = config.get("timeout", 10.0)
        
        async with httpx.AsyncClient(timeout=timeout) as client:
            if method == "GET":
                response = await client.get(url, params=inputs, headers=headers)
            elif method == "POST":
                response = await client.post(url, json=inputs, headers=headers)
            elif method == "PUT":
                response = await client.put(url, json=inputs, headers=headers)
            elif method == "DELETE":
                response = await client.delete(url, params=inputs, headers=headers)
            elif method == "PATCH":
                response = await client.patch(url, json=inputs, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
        
        return {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": response.text,
            "json": response.json() if response.headers.get("content-type", "").startswith("application/json") else None
        }
    
    async def _handle_http(
        self,
        tool_def: Dict[str, Any],
        inputs: Dict[str, Any],
        context: Dict
    ) -> Any:
        """Handle generic HTTP requests"""
        return await self._handle_api(tool_def, inputs, context)
    
    async def _handle_graphql(
        self,
        tool_def: Dict[str, Any],
        inputs: Dict[str, Any],
        context: Dict
    ) -> Any:
        """Handle GraphQL queries"""
        config = tool_def.get("config", {})
        url = config.get("url")
        query = inputs.get("query") or config.get("query")
        variables = inputs.get("variables", {})
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                url,
                json={"query": query, "variables": variables},
                headers={"Content-Type": "application/json"}
            )
        
        return response.json()
    
    async def _handle_code(
        self,
        tool_def: Dict[str, Any],
        inputs: Dict[str, Any],
        context: Dict
    ) -> Any:
        """Handle code execution (sandboxed)"""
        config = tool_def.get("config", {})
        code = inputs.get("code") or config.get("snippet") or config.get("code")
        language = config.get("language", "python")
        
        # For safety, we'll simulate execution
        return {
            "executed": True,
            "language": language,
            "code": code[:200],
            "output": f"Simulated execution of {language} code",
            "note": "Code execution is simulated for safety"
        }
    
    async def _handle_python(
        self,
        tool_def: Dict[str, Any],
        inputs: Dict[str, Any],
        context: Dict
    ) -> Any:
        """Handle Python code execution"""
        config = tool_def.get("config", {})
        code = inputs.get("code") or config.get("code")
        
        # Simulated for safety - in production, use a sandbox
        return {
            "executed": True,
            "code": code[:200],
            "output": "Python execution simulated",
            "note": "Use a proper sandbox for production"
        }
    
    async def _handle_shell(
        self,
        tool_def: Dict[str, Any],
        inputs: Dict[str, Any],
        context: Dict
    ) -> Any:
        """Handle shell command execution"""
        config = tool_def.get("config", {})
        command = inputs.get("command") or config.get("command")
        
        # Simulated for safety
        return {
            "executed": True,
            "command": command,
            "output": "Shell execution simulated",
            "note": "Use with caution in production"
        }
    
    async def _handle_database(
        self,
        tool_def: Dict[str, Any],
        inputs: Dict[str, Any],
        context: Dict
    ) -> Any:
        """Handle database queries"""
        config = tool_def.get("config", {})
        db_type = config.get("db_type", "sql")
        query = inputs.get("query") or config.get("query")
        
        return {
            "db_type": db_type,
            "query": query,
            "result": "Database query simulated",
            "note": "Implement actual database connection in production"
        }
    
    async def _handle_file(
        self,
        tool_def: Dict[str, Any],
        inputs: Dict[str, Any],
        context: Dict
    ) -> Any:
        """Handle file operations"""
        config = tool_def.get("config", {})
        operation = config.get("operation", "read")
        path = inputs.get("path") or config.get("path")
        
        if operation == "read":
            # Simulated file read
            return {
                "operation": "read",
                "path": path,
                "content": "File content simulated",
                "note": "Implement actual file operations with proper security"
            }
        elif operation == "write":
            content = inputs.get("content")
            return {
                "operation": "write",
                "path": path,
                "success": True,
                "note": "File write simulated"
            }
        else:
            return {
                "operation": operation,
                "error": f"Unsupported operation: {operation}"
            }
    
    async def _handle_custom(
        self,
        tool_def: Dict[str, Any],
        inputs: Dict[str, Any],
        context: Dict
    ) -> Any:
        """Handle custom tool types"""
        return {
            "tool_id": tool_def.get("id"),
            "tool_name": tool_def.get("name"),
            "inputs": inputs,
            "output": "Custom tool executed",
            "note": "Implement custom logic as needed"
        }
    
    # ===================== Helper Methods =====================
    
    def _evaluate_condition(
        self,
        condition: str,
        context: Optional[Dict],
        previous_results: List[ToolResult]
    ) -> bool:
        """Evaluate execution condition"""
        # Simple condition evaluation
        # In production, use a proper expression evaluator
        if condition == "if_previous_success":
            return len(previous_results) > 0 and previous_results[-1].success
        elif condition == "if_previous_failure":
            return len(previous_results) > 0 and not previous_results[-1].success
        else:
            return True
    
    def get_execution_stats(self) -> Dict[str, Any]:
        """Get execution statistics"""
        total_executions = len(self.execution_history)
        successful = sum(1 for e in self.execution_history if e["result"]["success"])
        failed = total_executions - successful
        
        return {
            "total_executions": total_executions,
            "successful": successful,
            "failed": failed,
            "success_rate": successful / total_executions if total_executions > 0 else 0
        }


# Global orchestrator instance
tool_orchestrator = ToolOrchestrator()
