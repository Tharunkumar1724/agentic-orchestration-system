"""
DuckDuckGo Search Tool - Comprehensive Test Script
Tests the DuckDuckGo tool through the backend API
"""
import asyncio
import aiohttp
import json
from datetime import datetime
from typing import Dict, Any


BASE_URL = "http://localhost:8000"


async def test_duckduckgo_tool():
    """Test the DuckDuckGo search tool with various queries."""
    
    print("=" * 80)
    print("DUCKDUCKGO SEARCH TOOL - COMPREHENSIVE TEST")
    print("=" * 80)
    print()
    
    async with aiohttp.ClientSession() as session:
        
        # Test 1: Simple keyword search
        print("Test 1: Simple Keyword Search")
        print("-" * 80)
        result1 = await execute_search(
            session, 
            "Python programming language",
            "Simple search for a well-known topic"
        )
        print_result(result1)
        print()
        
        # Test 2: Question query
        print("Test 2: Question Query")
        print("-" * 80)
        result2 = await execute_search(
            session,
            "What is artificial intelligence?",
            "Search with a question format"
        )
        print_result(result2)
        print()
        
        # Test 3: Calculation
        print("Test 3: Calculation Query")
        print("-" * 80)
        result3 = await execute_search(
            session,
            "2+2",
            "Test instant answer calculation"
        )
        print_result(result3)
        print()
        
        # Test 4: Person/Entity search
        print("Test 4: Entity Search (Person)")
        print("-" * 80)
        result4 = await execute_search(
            session,
            "Albert Einstein",
            "Search for a famous person"
        )
        print_result(result4)
        print()
        
        # Test 5: Technical term
        print("Test 5: Technical Term")
        print("-" * 80)
        result5 = await execute_search(
            session,
            "machine learning",
            "Search for a technical concept"
        )
        print_result(result5)
        print()
        
        # Test 6: Location/Place
        print("Test 6: Location Search")
        print("-" * 80)
        result6 = await execute_search(
            session,
            "Eiffel Tower",
            "Search for a famous landmark"
        )
        print_result(result6)
        print()
        
        # Test 7: Definition query
        print("Test 7: Definition Query")
        print("-" * 80)
        result7 = await execute_search(
            session,
            "define ubiquitous",
            "Search for word definition"
        )
        print_result(result7)
        print()
        
        # Summary
        print("=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        results = [result1, result2, result3, result4, result5, result6, result7]
        successful = sum(1 for r in results if r.get('success'))
        print(f"Total Tests: {len(results)}")
        print(f"Successful: {successful}")
        print(f"Failed: {len(results) - successful}")
        print(f"Success Rate: {(successful/len(results)*100):.1f}%")
        print()


async def execute_search(
    session: aiohttp.ClientSession,
    query: str,
    description: str
) -> Dict[str, Any]:
    """Execute a DuckDuckGo search via the backend API."""
    
    print(f"Query: '{query}'")
    print(f"Description: {description}")
    print()
    
    try:
        # Call the tool execution endpoint
        url = f"{BASE_URL}/tools/duckduckgo_search/execute"
        payload = {
            "parameters": {
                "query": query
            }
        }
        
        start_time = datetime.now()
        
        async with session.post(
            url,
            json=payload,
            timeout=aiohttp.ClientTimeout(total=20)
        ) as response:
            
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            
            if response.status == 200:
                data = await response.json()
                data['execution_time_ms'] = execution_time
                return data
            else:
                error_text = await response.text()
                return {
                    'success': False,
                    'error': {
                        'code': str(response.status),
                        'message': f"HTTP {response.status}",
                        'details': error_text
                    },
                    'execution_time_ms': execution_time
                }
    
    except asyncio.TimeoutError:
        return {
            'success': False,
            'error': {
                'code': '5002',
                'message': 'Request timeout',
                'details': 'Request took longer than 20 seconds'
            }
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': {
                'code': '5000',
                'message': 'Execution error',
                'details': str(e)
            }
        }


def print_result(result: Dict[str, Any]):
    """Print search result in a readable format."""
    
    if result.get('success'):
        data = result.get('data', {})
        
        print(f"✅ Success (took {result.get('execution_time_ms', 0):.0f}ms)")
        print()
        
        # Abstract
        if data.get('AbstractText'):
            print(f"Abstract: {data['AbstractText'][:200]}...")
            print(f"Source: {data.get('AbstractSource', 'N/A')}")
            if data.get('AbstractURL'):
                print(f"URL: {data['AbstractURL']}")
            print()
        
        # Heading
        if data.get('Heading'):
            print(f"Heading: {data['Heading']}")
            print()
        
        # Instant Answer
        if data.get('Answer'):
            print(f"Instant Answer: {data['Answer']}")
            print(f"Answer Type: {data.get('AnswerType', 'N/A')}")
            print()
        
        # Definition
        if data.get('Definition'):
            print(f"Definition: {data['Definition'][:200]}...")
            print(f"Source: {data.get('DefinitionSource', 'N/A')}")
            print()
        
        # Related Topics
        related = data.get('RelatedTopics', [])
        if related:
            print(f"Related Topics: {len(related)} items")
            for i, topic in enumerate(related[:3], 1):
                if isinstance(topic, dict) and topic.get('Text'):
                    print(f"  {i}. {topic['Text'][:80]}...")
            if len(related) > 3:
                print(f"  ... and {len(related) - 3} more")
            print()
        
        # Entity
        if data.get('Entity'):
            print(f"Entity: {data['Entity']}")
            print()
        
        # Type
        if data.get('Type'):
            type_map = {
                'A': 'Article',
                'D': 'Disambiguation',
                'C': 'Category',
                'N': 'Name',
                'E': 'Exclusive'
            }
            print(f"Result Type: {type_map.get(data['Type'], data['Type'])}")
            print()
        
        # Image
        if data.get('Image'):
            print(f"Image: {data['Image']}")
            print()
    
    else:
        error = result.get('error', {})
        print(f"❌ Failed")
        print(f"Code: {error.get('code', 'UNKNOWN')}")
        print(f"Message: {error.get('message', 'No error message')}")
        if error.get('details'):
            print(f"Details: {error['details']}")
        print()


async def test_tool_registration():
    """Test that the tool is properly registered in the system."""
    
    print("=" * 80)
    print("TOOL REGISTRATION TEST")
    print("=" * 80)
    print()
    
    async with aiohttp.ClientSession() as session:
        
        # Check if tool exists
        print("Checking if duckduckgo_search tool is registered...")
        
        try:
            async with session.get(
                f"{BASE_URL}/tools/duckduckgo_search",
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                
                if response.status == 200:
                    tool_data = await response.json()
                    print("✅ Tool is registered!")
                    print()
                    print(f"ID: {tool_data.get('id')}")
                    print(f"Name: {tool_data.get('name')}")
                    print(f"Type: {tool_data.get('type')}")
                    print(f"Description: {tool_data.get('description', '')[:100]}...")
                    print()
                    return True
                
                elif response.status == 404:
                    print("❌ Tool not found - may need to be loaded")
                    print("Tip: Restart the backend or manually load the tool")
                    print()
                    return False
                
                else:
                    print(f"⚠️ Unexpected response: HTTP {response.status}")
                    print()
                    return False
        
        except Exception as e:
            print(f"❌ Error checking tool registration: {e}")
            print()
            return False


async def main():
    """Main test runner."""
    
    # First check if tool is registered
    is_registered = await test_tool_registration()
    
    if not is_registered:
        print("Skipping execution tests - tool not registered")
        print("Please ensure the backend is running and the tool is loaded")
        return
    
    # Run search tests
    await test_duckduckgo_tool()


if __name__ == "__main__":
    asyncio.run(main())
