"""
Complete Example: Dynamic Tool Creation and Workflow Execution
This demonstrates the full pipeline from tool creation to execution
"""

from agentic_tool_client import AgenticToolClient, SearchToolBuilder, APIToolBuilder
import requests
import time


def main():
    print("\n" + "="*70)
    print("🚀 COMPLETE DYNAMIC TOOL WORKFLOW EXAMPLE")
    print("="*70 + "\n")
    
    # Initialize client
    client = AgenticToolClient("http://localhost:8000")
    base_url = "http://localhost:8000"
    
    # =========================================================================
    # STEP 1: Create Dynamic Search Tools
    # =========================================================================
    print("📝 STEP 1: Creating Dynamic Search Tools\n")
    
    # Create a general web search tool
    web_search = (
        SearchToolBuilder(client)
        .with_name("AI Research Search")
        .with_max_results(8)
        .with_region("us-en")
        .moderate_search()
        .with_description("Search for AI research and papers")
        .build()
    )
    web_tool_id = web_search["tool"]["id"]
    print(f"✅ Created web search tool: {web_tool_id}")
    
    # Create a news search tool
    news_search = (
        SearchToolBuilder(client)
        .with_name("AI News Search")
        .with_max_results(5)
        .recent_week()
        .with_description("Search for recent AI news")
        .build()
    )
    news_tool_id = news_search["tool"]["id"]
    print(f"✅ Created news search tool: {news_tool_id}")
    
    # Create a code search tool (API)
    code_search = (
        APIToolBuilder(client)
        .with_name("GitHub Code Search")
        .with_url("https://api.github.com")
        .get()
        .with_header("Accept", "application/vnd.github.v3+json")
        .with_description("Search GitHub for code examples")
        .build()
    )
    code_tool_id = code_search["tool"]["id"]
    print(f"✅ Created GitHub API tool: {code_tool_id}\n")
    
    # =========================================================================
    # STEP 2: Create Agents Using Dynamic Tools
    # =========================================================================
    print("📝 STEP 2: Creating Agents with Dynamic Tools\n")
    
    # Create web researcher agent
    web_agent = {
        "id": f"web_researcher_{int(time.time())}",
        "name": "Web Research Agent",
        "type": "react",
        "llm_config": {
            "provider": "groq",
            "model": "llama-3.1-70b-versatile",
            "temperature": 0.3,
            "max_tokens": 2000
        },
        "tools": [web_tool_id],
        "version": "v1"
    }
    
    response = requests.post(f"{base_url}/agents/", json=web_agent)
    if response.status_code == 200:
        print(f"✅ Created web researcher: {web_agent['id']}")
    else:
        print(f"❌ Failed to create web researcher: {response.text}")
    
    # Create news researcher agent
    news_agent = {
        "id": f"news_researcher_{int(time.time())}",
        "name": "News Research Agent",
        "type": "react",
        "llm_config": {
            "provider": "groq",
            "model": "llama-3.1-70b-versatile",
            "temperature": 0.3,
            "max_tokens": 1500
        },
        "tools": [news_tool_id],
        "version": "v1"
    }
    
    response = requests.post(f"{base_url}/agents/", json=news_agent)
    if response.status_code == 200:
        print(f"✅ Created news researcher: {news_agent['id']}")
    else:
        print(f"❌ Failed to create news researcher: {response.text}")
    
    # Create code researcher agent
    code_agent = {
        "id": f"code_researcher_{int(time.time())}",
        "name": "Code Research Agent",
        "type": "react",
        "llm_config": {
            "provider": "groq",
            "model": "llama-3.1-70b-versatile",
            "temperature": 0.2,
            "max_tokens": 2000
        },
        "tools": [code_tool_id],
        "version": "v1"
    }
    
    response = requests.post(f"{base_url}/agents/", json=code_agent)
    if response.status_code == 200:
        print(f"✅ Created code researcher: {code_agent['id']}\n")
    else:
        print(f"❌ Failed to create code researcher: {response.text}\n")
    
    # =========================================================================
    # STEP 3: Create Multi-Agent Workflow
    # =========================================================================
    print("📝 STEP 3: Creating Multi-Agent Research Workflow\n")
    
    workflow = {
        "id": f"ai_research_workflow_{int(time.time())}",
        "name": "AI Research Workflow with Dynamic Tools",
        "description": "Comprehensive research using dynamically created tools",
        "type": "sequence",
        "nodes": [
            {
                "id": "web_research",
                "agent_ref": web_agent["id"],
                "task": "Search for latest information about transformers in AI"
            },
            {
                "id": "news_research",
                "agent_ref": news_agent["id"],
                "task": "Find recent news about transformer models",
                "receives_from": ["web_research"]
            },
            {
                "id": "code_examples",
                "agent_ref": code_agent["id"],
                "task": "Find transformer implementation examples on GitHub",
                "receives_from": ["web_research"]
            }
        ]
    }
    
    response = requests.post(f"{base_url}/workflows/", json=workflow)
    if response.status_code == 200:
        print(f"✅ Created workflow: {workflow['id']}\n")
    else:
        print(f"❌ Failed to create workflow: {response.text}\n")
        return
    
    # =========================================================================
    # STEP 4: Execute Workflow
    # =========================================================================
    print("📝 STEP 4: Executing Workflow\n")
    print("⏳ Running workflow... (this may take a moment)\n")
    
    exec_params = {
        "parameters": {
            "topic": "Transformer Neural Networks",
            "depth": "comprehensive"
        }
    }
    
    response = requests.post(
        f"{base_url}/workflows/{workflow['id']}/execute",
        json=exec_params
    )
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Workflow executed successfully!\n")
        
        print("-" * 70)
        print("EXECUTION RESULTS:")
        print("-" * 70)
        
        # Display results from each node
        if "steps" in result:
            for step in result["steps"]:
                print(f"\n📊 {step.get('node_id', 'Unknown').upper()}:")
                print(f"   Status: {step.get('status', 'unknown')}")
                if step.get("result"):
                    print(f"   Result: {str(step['result'])[:200]}...")
        
        print("\n" + "-" * 70)
        print(f"Run ID: {result.get('run_id', 'N/A')}")
        print(f"Status: {result.get('status', 'N/A')}")
        print("-" * 70)
        
    else:
        print(f"❌ Workflow execution failed: {response.text}\n")
    
    # =========================================================================
    # STEP 5: Summary
    # =========================================================================
    print("\n" + "="*70)
    print("📊 SUMMARY")
    print("="*70)
    
    all_tools = client.list_tools()
    print(f"\n✅ Total tools created: {len(all_tools)}")
    print(f"✅ Agents created: 3")
    print(f"✅ Workflows created: 1")
    print(f"✅ Workflow executed: {workflow['id']}")
    
    print("\n🎯 Key Components Created:")
    print(f"   • Web Search Tool: {web_tool_id}")
    print(f"   • News Search Tool: {news_tool_id}")
    print(f"   • GitHub API Tool: {code_tool_id}")
    print(f"   • Web Research Agent: {web_agent['id']}")
    print(f"   • News Research Agent: {news_agent['id']}")
    print(f"   • Code Research Agent: {code_agent['id']}")
    print(f"   • Research Workflow: {workflow['id']}")
    
    print("\n" + "="*70)
    print("✨ DYNAMIC TOOL WORKFLOW COMPLETE!")
    print("="*70 + "\n")
    
    # =========================================================================
    # BONUS: Show how to reuse tools
    # =========================================================================
    print("\n💡 BONUS: Reusing Dynamic Tools\n")
    
    print("You can now reuse these tools in other workflows:")
    print(f"""
    # Example: Create a new agent with existing tools
    new_agent = {{
        "id": "my_new_agent",
        "name": "My Research Agent",
        "type": "react",
        "llm_config": {{"provider": "groq", "model": "llama-3.1-70b-versatile"}},
        "tools": [
            "{web_tool_id}",  # Reuse web search
            "{news_tool_id}"   # Reuse news search
        ]
    }}
    """)


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to backend at http://localhost:8000")
        print("\nPlease start the backend first:")
        print("  python run.py")
        print("\nThen run this example again:")
        print("  python example_complete_workflow.py\n")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
