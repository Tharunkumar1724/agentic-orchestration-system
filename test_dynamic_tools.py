"""
Test Dynamic Tool Creation
Demonstrates how to create tools dynamically via API
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"


def print_response(title: str, response: requests.Response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    
    try:
        data = response.json()
        print(json.dumps(data, indent=2))
    except:
        print(response.text)
    print()


def test_list_templates():
    """Test: List all available tool templates"""
    print("\n🔍 TEST 1: List Available Templates")
    response = requests.get(f"{BASE_URL}/tools/dynamic/templates")
    print_response("Available Templates", response)
    return response.json()


def test_get_template_schema():
    """Test: Get schema for DuckDuckGo template"""
    print("\n🔍 TEST 2: Get DuckDuckGo Template Schema")
    response = requests.get(f"{BASE_URL}/tools/dynamic/templates/duckduckgo_search")
    print_response("DuckDuckGo Template Schema", response)
    return response.json()


def test_create_from_template():
    """Test: Create tool from template"""
    print("\n🔍 TEST 3: Create Tool from Template")
    
    payload = {
        "template": "duckduckgo_search",
        "name": "AI Research Search",
        "description": "Search tool optimized for AI research",
        "config_overrides": {
            "max_results": 10,
            "region": "us-en",
            "safesearch": "moderate"
        },
        "save_to_disk": True
    }
    
    response = requests.post(
        f"{BASE_URL}/tools/dynamic/from-template",
        json=payload
    )
    print_response("Created Tool from Template", response)
    return response.json()


def test_quick_duckduckgo_tool():
    """Test: Quick DuckDuckGo tool creation"""
    print("\n🔍 TEST 4: Quick DuckDuckGo Tool Creation")
    
    payload = {
        "name": "News Search Tool",
        "max_results": 8,
        "region": "wt-wt",
        "safesearch": "moderate",
        "timelimit": "d",  # Last day
        "description": "Search for recent news articles"
    }
    
    response = requests.post(
        f"{BASE_URL}/tools/dynamic/duckduckgo",
        json=payload
    )
    print_response("Quick DuckDuckGo Tool", response)
    return response.json()


def test_create_custom_tool():
    """Test: Create a completely custom tool"""
    print("\n🔍 TEST 5: Create Custom API Tool")
    
    payload = {
        "name": "Weather API Tool",
        "type": "api",
        "config": {
            "url": "https://api.weather.gov",
            "method": "GET",
            "headers": {
                "User-Agent": "AgenticApp/1.0"
            },
            "timeout": 15.0
        },
        "input_schema": {
            "type": "object",
            "properties": {
                "latitude": {
                    "type": "number",
                    "description": "Latitude coordinate"
                },
                "longitude": {
                    "type": "number",
                    "description": "Longitude coordinate"
                }
            },
            "required": ["latitude", "longitude"]
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "temperature": {"type": "number"},
                "conditions": {"type": "string"},
                "forecast": {"type": "array"}
            }
        },
        "description": "Get weather information by coordinates",
        "save_to_disk": True
    }
    
    response = requests.post(
        f"{BASE_URL}/tools/dynamic/custom",
        json=payload
    )
    print_response("Custom Weather Tool", response)
    return response.json()


def test_batch_create_tools():
    """Test: Create multiple tools at once"""
    print("\n🔍 TEST 6: Batch Create Tools")
    
    payload = {
        "tools": [
            {
                "template": "duckduckgo_search",
                "name": "Quick Search",
                "description": "Fast search with 3 results",
                "config": {"max_results": 3}
            },
            {
                "template": "duckduckgo_search",
                "name": "Deep Search",
                "description": "Comprehensive search with 15 results",
                "config": {"max_results": 15}
            },
            {
                "template": "api_rest",
                "name": "GitHub Stars API",
                "description": "Get repository stars",
                "config": {
                    "url": "https://api.github.com",
                    "method": "GET",
                    "headers": {
                        "Accept": "application/vnd.github.v3+json"
                    }
                }
            }
        ],
        "save_to_disk": True
    }
    
    response = requests.post(
        f"{BASE_URL}/tools/dynamic/batch",
        json=payload
    )
    print_response("Batch Created Tools", response)
    return response.json()


def test_create_from_recipe():
    """Test: Create tools from a predefined recipe"""
    print("\n🔍 TEST 7: Create Tools from Recipe")
    
    # First, list available recipes
    response = requests.get(f"{BASE_URL}/tools/dynamic/recipes")
    print_response("Available Recipes", response)
    
    # Create from web_search recipe
    response = requests.post(f"{BASE_URL}/tools/dynamic/recipes/web_search")
    print_response("Created from 'web_search' Recipe", response)
    return response.json()


def test_list_all_tools():
    """Test: List all created tools"""
    print("\n🔍 TEST 8: List All Tools")
    response = requests.get(f"{BASE_URL}/tools/")
    print_response("All Created Tools", response)
    return response.json()


def test_full_workflow():
    """Test: Complete workflow with dynamic tools"""
    print("\n🔍 TEST 9: Full Workflow Test")
    
    # 1. Create a custom search tool
    print("\n📝 Step 1: Create Custom Search Tool")
    search_tool_payload = {
        "name": "Python Tutorial Search",
        "max_results": 7,
        "description": "Search for Python programming tutorials"
    }
    search_response = requests.post(
        f"{BASE_URL}/tools/dynamic/duckduckgo",
        json=search_tool_payload
    )
    search_tool = search_response.json()
    tool_id = search_tool.get("tool", {}).get("id")
    print(f"✅ Created tool: {tool_id}")
    
    # 2. Create an agent that uses this tool
    print("\n📝 Step 2: Create Agent with Dynamic Tool")
    agent_payload = {
        "id": f"agent_with_dynamic_tool_{tool_id}",
        "name": "Python Tutorial Researcher",
        "type": "react",
        "llm_config": {
            "provider": "groq",
            "model": "llama-3.1-70b-versatile",
            "temperature": 0.3
        },
        "tools": [tool_id],
        "version": "v1"
    }
    agent_response = requests.post(
        f"{BASE_URL}/agents/",
        json=agent_payload
    )
    print(f"✅ Created agent: {agent_response.json().get('id')}")
    
    # 3. Create workflow using the agent
    print("\n📝 Step 3: Create Workflow")
    workflow_payload = {
        "id": f"workflow_dynamic_tools_{tool_id[:8]}",
        "name": "Dynamic Tool Workflow",
        "description": "Workflow using dynamically created tools",
        "type": "sequence",
        "nodes": [
            {
                "id": "search_node",
                "agent_ref": agent_payload["id"],
                "task": "Find the best Python tutorials for beginners"
            }
        ]
    }
    workflow_response = requests.post(
        f"{BASE_URL}/workflows/",
        json=workflow_payload
    )
    print(f"✅ Created workflow: {workflow_response.json().get('id')}")
    
    # 4. Execute the workflow
    print("\n📝 Step 4: Execute Workflow")
    exec_response = requests.post(
        f"{BASE_URL}/workflows/{workflow_payload['id']}/execute",
        json={"parameters": {"topic": "Python for beginners"}}
    )
    print_response("Workflow Execution Result", exec_response)
    
    return {
        "tool": search_tool,
        "agent": agent_response.json(),
        "workflow": workflow_response.json(),
        "execution": exec_response.json() if exec_response.status_code == 200 else None
    }


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("🚀 DYNAMIC TOOL CREATION TESTS")
    print("="*60)
    
    try:
        # Basic tests
        test_list_templates()
        test_get_template_schema()
        test_create_from_template()
        test_quick_duckduckgo_tool()
        test_create_custom_tool()
        test_batch_create_tools()
        test_create_from_recipe()
        test_list_all_tools()
        
        # Advanced workflow test
        test_full_workflow()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS COMPLETED!")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to backend at", BASE_URL)
        print("Please ensure the backend is running:")
        print("  python run.py")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()
