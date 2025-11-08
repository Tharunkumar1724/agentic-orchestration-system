import asyncio
import uuid
from typing import Any, Dict, List, TypedDict, Annotated
from langgraph.graph import StateGraph, END
from operator import add
from app.storage import load
from app.services.llm_client import LLMClient
from app.services.tool_orchestrator import tool_orchestrator, ToolExecutionStrategy
from langchain_core.tools import Tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from datetime import datetime
import json


class WorkflowState(TypedDict):
    """State shared across all nodes in the workflow graph."""
    messages: Annotated[List[BaseMessage], add]
    shared_data: Dict[str, Any]
    agents_used: List[str]
    current_step: str
    results: Dict[str, Any]
    error: str | None
    steps: List[Dict[str, Any]]  # Execution steps for visualization


class LangGraphOrchestrator:
    """Orchestrator using LangGraph + LangChain agents for workflow execution."""
    
    def __init__(self):
        self.agent_llms: Dict[str, LLMClient] = {}
    
    def get_agent_llm(self, agent_id: str) -> LLMClient:
        """Get or create LLM client for an agent."""
        if agent_id not in self.agent_llms:
            self.agent_llms[agent_id] = LLMClient()
        return self.agent_llms[agent_id]
    
    def create_tool_from_def(self, tool_def: Dict[str, Any]) -> Tool:
        """Create a LangChain Tool from tool definition."""
        tool_id = tool_def.get("id", "unknown-tool")
        tool_name = tool_def.get("name", tool_id).replace(" ", "_").replace("-", "_")
        tool_type = tool_def.get("type")
        config = tool_def.get("config", {})
        
        if tool_type == "websearch":
            def search_func(query: str) -> str:
                """Search the web for information."""
                try:
                    from ddgs import DDGS
                    max_results = config.get("max_results", 5)
                    
                    with DDGS() as ddgs:
                        results = list(ddgs.text(
                            query=query,
                            region=config.get("region", "wt-wt"),
                            safesearch=config.get("safesearch", "moderate"),
                            max_results=max_results
                        ))
                    
                    if not results:
                        return "No results found."
                    
                    formatted = "\n\n".join([
                        f"Title: {r.get('title', 'N/A')}\nURL: {r.get('href', 'N/A')}\nSnippet: {r.get('body', 'N/A')}"
                        for r in results
                    ])
                    return formatted
                    
                except Exception as e:
                    return f"Search failed: {str(e)}"
            
            return Tool(
                name=tool_name,
                func=search_func,
                description=f"Search the web for: {tool_name}. Input should be a search query string."
            )
        
        elif tool_type == "api":
            api_url = config.get("url", "")
            def api_func(input_data: str) -> str:
                """Call an API endpoint."""
                import httpx
                url = api_url
                method = config.get("method", "GET").upper()
                
                try:
                    with httpx.Client(timeout=10.0) as client:
                        if method == "GET":
                            r = client.get(url, params={"q": input_data})
                        else:
                            r = client.post(url, json={"input": input_data})
                        
                        return f"Status: {r.status_code}\nResponse: {r.text[:500]}"
                except Exception as e:
                    return f"API call failed: {str(e)}"
            
            return Tool(
                name=tool_name,
                func=api_func,
                description=f"Call API endpoint: {api_url}. Input should be the query or data to send."
            )
        
        elif tool_type == "code":
            def code_func(code: str) -> str:
                """Execute Python code safely (simulated)."""
                return f"Code execution (simulated): {code[:200]}"
            
            return Tool(
                name=tool_name,
                func=code_func,
                description="Execute Python code. Input should be valid Python code as a string."
            )
        
        else:
            def generic_func(input_str: str) -> str:
                return f"Tool {tool_name} executed with input: {input_str}"
            
            return Tool(
                name=tool_name,
                func=generic_func,
                description=f"Generic tool: {tool_name}"
            )
    
    def get_agent_llm(self, agent_id: str) -> LLMClient:
        """Get or create LLM client for an agent."""
        if agent_id not in self.agent_llms:
            self.agent_llms[agent_id] = LLMClient()
        return self.agent_llms[agent_id]
    
    async def run_tool(self, tool_def: Dict[str, Any], inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool using advanced tool orchestrator."""
        try:
            # Use advanced tool orchestrator
            result = await tool_orchestrator.execute_tool(tool_def, inputs, {})
            
            return result.to_dict()
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "tool_id": tool_def.get("id"),
                "tool_type": tool_def.get("type")
            }
    
    async def run_agent(self, agent_def: Dict[str, Any], task: str, state: WorkflowState) -> Dict[str, Any]:
        """Execute an agent with its tools."""
        agent_id = agent_def.get("id", "unknown-agent")
        agent_name = agent_def.get("name", agent_id)
        agent_type = agent_def.get("type", "zero_shot")
        system_prompt = agent_def.get("system_prompt", "")
        
        # Get dedicated LLM for this agent
        agent_llm = self.get_agent_llm(agent_id)
        
        # Build prompt with context from previous agents (communication)
        prompt = task
        
        # Add system prompt
        if system_prompt:
            prompt = f"{system_prompt}\n\n{prompt}"
        
        # Add communication context from agents this node receives from
        if state.get("messages"):
            recent_msgs = state["messages"][-5:]
            context_str = "\n".join([
                f"[From {m.get('sender', 'unknown')}]: {str(m.get('content', ''))[:200]}"
                for m in recent_msgs
                if m.get('type') in ['agent_result', 'tool_result']
            ])
            if context_str:
                prompt = f"Previous communication:\n{context_str}\n\nYour task: {prompt}"
        
        # Load and execute tools first to provide context to LLM
        tool_results = {}
        tool_names = []
        tools_to_execute = []
        
        # Collect all tools for this agent
        # Priority: node-specific tools (from workflow) override agent default tools
        for tool_id in agent_def.get("tools", []):
            tool = load("tools", tool_id)
            if not tool:
                print(f"WARNING: Tool {tool_id} not found in storage")
                continue
            print(f"DEBUG: Loaded tool {tool_id}: {tool.get('name', 'unnamed')}")
            tool_names.append(tool.get("name", tool_id))
            tools_to_execute.append(tool)
        
        # Determine execution strategy
        execution_strategy = agent_def.get("tool_execution_strategy", "sequential")
        strategy_map = {
            "sequential": ToolExecutionStrategy.SEQUENTIAL,
            "parallel": ToolExecutionStrategy.PARALLEL,
            "conditional": ToolExecutionStrategy.CONDITIONAL,
            "retry": ToolExecutionStrategy.RETRY,
            "fallback": ToolExecutionStrategy.FALLBACK
        }
        strategy = strategy_map.get(execution_strategy, ToolExecutionStrategy.SEQUENTIAL)
        
        # Execute tools using advanced orchestrator
        if tools_to_execute:
            tool_inputs = {"task": task, "prompt": prompt, "query": task, "q": task}
            execution_context = {"agent_id": agent_id, "state": state}
            
            orchestrated_results = await tool_orchestrator.execute_tools(
                tools_to_execute,
                tool_inputs,
                execution_context,
                strategy
            )
            
            # Process results and build context
            for i, result in enumerate(orchestrated_results):
                if i < len(tools_to_execute):
                    tool_id = tools_to_execute[i].get("id", f"tool_{i}")
                    tool_results[tool_id] = result.to_dict()
                    
                    # Add successful tool results to prompt context
                    if result.success and result.data:
                        tool_type = tools_to_execute[i].get("type")
                        
                        if tool_type == "websearch" and result.data.get("results"):
                            results_summary = "\n".join([
                                f"- {r.get('title', 'N/A')}: {r.get('body', 'N/A')[:150]}..."
                                for r in result.data.get("results", [])[:3]
                            ])
                            prompt += f"\n\nWeb search results:\n{results_summary}"
                        elif tool_type == "api" and result.data.get("body"):
                            prompt += f"\n\nAPI response: {str(result.data.get('body'))[:200]}"
                        elif result.data.get("output"):
                            prompt += f"\n\nTool output: {str(result.data.get('output'))[:200]}"
                        elif result.data.get("content"):
                            prompt += f"\n\nTool result: {str(result.data.get('content'))[:200]}"
        
        # Call LLM with enriched context
        llm_response = await agent_llm.generate(prompt)
        
        result = {
            "agent_id": agent_id,
            "agent_name": agent_name,
            "agent_type": agent_type,
            "task": task,
            "llm_response": llm_response,
            "context_size": len(agent_llm.context_window),
            "tool_results": tool_results,
            "tools_used": tool_names
        }
        
        return result
    
    async def build_graph_from_workflow(self, workflow_def: Dict[str, Any]) -> StateGraph:
        """Build a LangGraph StateGraph from workflow definition."""
        workflow_type = workflow_def.get("type", "sequence")
        nodes = workflow_def.get("nodes", [])
        
        # Create graph
        graph = StateGraph(WorkflowState)
        
        # Add nodes to graph
        for node in nodes:
            node_id = node.get("id")
            agent_ref = node.get("agent_ref")
            task = node.get("task", "")
            node_tools = node.get("tools", [])  # Tools specific to this workflow node
            
            # Create node function for agent execution
            async def node_fn(state: WorkflowState, agent_id=agent_ref, node_task=task, nid=node_id, tools_override=node_tools):
                agent = load("agents", agent_id)
                if not agent:
                    return {
                        "messages": [{"sender": nid, "content": f"Agent {agent_id} not found", "type": "error"}],
                        "results": {**state.get("results", {}), nid: {"error": f"Agent {agent_id} not found"}},
                        "error": f"Agent {agent_id} not found"
                    }
                
                # Override agent tools with node-specific tools if provided
                if tools_override:
                    print(f"DEBUG: Overriding agent {agent_id} tools with node tools: {tools_override}")
                    agent = {**agent, "tools": tools_override}
                else:
                    print(f"DEBUG: No tool override for node {nid}, using agent default tools: {agent.get('tools', [])}")
                
                result = await self.run_agent(agent, node_task, state)
                
                return {
                    "messages": [{"sender": nid, "agent": agent_id, "content": result, "type": "agent_result"}],
                    "agents_used": [agent_id],
                    "shared_data": {**state.get("shared_data", {}), nid: result},
                    "results": {**state.get("results", {}), nid: result},
                    "current_step": nid
                }
            
            graph.add_node(node_id, node_fn)
        
        # Add edges based on workflow type
        if workflow_type == "sequence" and nodes:
            # Sequential: chain nodes
            graph.set_entry_point(nodes[0]["id"])
            for i in range(len(nodes) - 1):
                graph.add_edge(nodes[i]["id"], nodes[i + 1]["id"])
            graph.add_edge(nodes[-1]["id"], END)
        
        elif workflow_type == "parallel" and nodes:
            # Parallel: all nodes run independently
            # Add a start node
            def start_node(state: WorkflowState):
                return {"current_step": "start", "messages": [{"sender": "system", "content": "Workflow started", "type": "start"}]}
            
            graph.add_node("__start__", start_node)
            graph.set_entry_point("__start__")
            
            # Connect start to all parallel nodes
            for node in nodes:
                graph.add_edge("__start__", node["id"])
                graph.add_edge(node["id"], END)
        
        elif nodes:
            # Default to sequence
            graph.set_entry_point(nodes[0]["id"])
            for i in range(len(nodes) - 1):
                graph.add_edge(nodes[i]["id"], nodes[i + 1]["id"])
            graph.add_edge(nodes[-1]["id"], END)
        
        return graph.compile()
    
    async def run_workflow(self, workflow_def: Dict[str, Any], run_id: str = None, initial_state: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute workflow using LangGraph.
        
        Args:
            workflow_def: Workflow definition
            run_id: Optional run ID
            initial_state: Optional initial state for resuming chat sessions
        """
        run_id = run_id or str(uuid.uuid4())
        workflow_id = workflow_def.get("id", "unknown")
        
        try:
            # Build LangGraph
            compiled_graph = await self.build_graph_from_workflow(workflow_def)
            
            # Use provided initial state or create new one
            if initial_state:
                state: WorkflowState = {
                    "messages": initial_state.get("messages", []),
                    "shared_data": initial_state.get("shared_data", {}),
                    "agents_used": initial_state.get("agents_used", []),
                    "current_step": initial_state.get("current_step", ""),
                    "results": initial_state.get("results", {}),
                    "error": initial_state.get("error")
                }
            else:
                state: WorkflowState = {
                    "messages": [],
                    "shared_data": {},
                    "agents_used": [],
                    "current_step": "",
                    "results": {},
                    "error": None
                }
            
            # Run the graph
            final_state = await compiled_graph.ainvoke(state)
            
            return {
                "workflow_id": workflow_id,
                "run_id": run_id,
                "status": "success" if not final_state.get("error") else "failed",
                "result": final_state.get("results", {}),
                "meta": {
                    "communication_log": final_state.get("messages", []),
                    "shared_state": final_state.get("shared_data", {}),
                    "agents_used": final_state.get("agents_used", []),
                    "total_messages": len(final_state.get("messages", [])),
                    "final_step": final_state.get("current_step", "")
                },
                "error": final_state.get("error"),
                "state": final_state  # Return full state for chat mode
            }
        
        except Exception as e:
            return {
                "workflow_id": workflow_id,
                "run_id": run_id,
                "status": "failed",
                "error": str(e),
                "result": {},
                "meta": {
                    "communication_log": [],
                    "error_details": str(e)
                }
            }


# Global orchestrator instance
orchestrator = LangGraphOrchestrator()


async def run_workflow(workflow_obj: Dict[str, Any], run_id: str = None) -> Dict[str, Any]:
    """Convenience function to run workflow."""
    return await orchestrator.run_workflow(workflow_obj, run_id)
