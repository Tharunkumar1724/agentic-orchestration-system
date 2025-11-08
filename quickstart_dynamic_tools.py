"""
Quick Start Script for Dynamic Tool Creation
Run this to verify everything is working
"""

import requests
import json
import sys


def check_backend():
    """Check if backend is running"""
    try:
        response = requests.get("http://localhost:8000/docs")
        return response.status_code == 200
    except:
        return False


def main():
    print("\n" + "="*70)
    print("🚀 DYNAMIC TOOL CREATION - QUICK START")
    print("="*70 + "\n")
    
    # Check backend
    print("1. Checking backend...")
    if not check_backend():
        print("   ❌ Backend is not running!")
        print("\n   Please start it first:")
        print("   > python run.py\n")
        sys.exit(1)
    print("   ✅ Backend is running\n")
    
    # Create a simple DuckDuckGo search tool
    print("2. Creating DuckDuckGo search tool...")
    response = requests.post(
        "http://localhost:8000/tools/dynamic/duckduckgo",
        json={
            "name": "Quick Start Search",
            "max_results": 5,
            "region": "wt-wt",
            "description": "Quick start example search tool"
        }
    )
    
    if response.status_code == 200:
        tool = response.json()
        tool_id = tool["tool"]["id"]
        print(f"   ✅ Tool created: {tool_id}\n")
    else:
        print(f"   ❌ Failed: {response.text}\n")
        sys.exit(1)
    
    # List all templates
    print("3. Available templates:")
    response = requests.get("http://localhost:8000/tools/dynamic/templates")
    if response.status_code == 200:
        templates = response.json()["templates"]
        print(f"   ✅ Found {len(templates)} templates:")
        for t in templates[:5]:  # Show first 5
            print(f"      • {t['template']} ({t['type']})")
        print(f"      ... and {len(templates) - 5} more\n")
    
    # List all tools
    print("4. Your tools:")
    response = requests.get("http://localhost:8000/tools/")
    if response.status_code == 200:
        tools = response.json()
        print(f"   ✅ You have {len(tools)} tools")
        if tools:
            print(f"      Latest: {tools[-1].get('name', 'Unknown')}\n")
    
    # Success
    print("="*70)
    print("✅ SUCCESS! Everything is working!")
    print("="*70)
    
    print("\n📚 Next Steps:\n")
    print("1. Try the Python client:")
    print("   > python agentic_tool_client.py\n")
    
    print("2. Run comprehensive tests:")
    print("   > python test_dynamic_tools.py\n")
    
    print("3. Try the interactive tool creator:")
    print("   > python interactive_tool_creator.py\n")
    
    print("4. Run the complete workflow example:")
    print("   > python example_complete_workflow.py\n")
    
    print("5. Read the guide:")
    print("   Open: DYNAMIC_TOOL_CREATION_GUIDE.md\n")
    
    print("Your tool ID for testing:", tool_id)
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Cancelled")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
