"""
Quick DuckDuckGo API Direct Test
Tests the DuckDuckGo API directly without backend
"""
import asyncio
import aiohttp
import json


async def test_duckduckgo_direct():
    """Test DuckDuckGo API directly."""
    
    print("=" * 80)
    print("DUCKDUCKGO API DIRECT TEST")
    print("=" * 80)
    print()
    
    test_queries = [
        "Python programming language",
        "What is artificial intelligence?",
        "Albert Einstein",
        "2+2",
        "machine learning"
    ]
    
    async with aiohttp.ClientSession() as session:
        
        for i, query in enumerate(test_queries, 1):
            print(f"Test {i}: {query}")
            print("-" * 80)
            
            try:
                params = {
                    'q': query,
                    'format': 'json',
                    'no_html': '1',
                    'no_redirect': '1'
                }
                
                async with session.get(
                    'https://api.duckduckgo.com/',
                    params=params,
                    timeout=aiohttp.ClientTimeout(total=15)
                ) as response:
                    
                    if response.status in [200, 202]:  # DuckDuckGo returns 202
                        # DuckDuckGo returns application/x-javascript, need to specify content_type
                        data = await response.json(content_type=None)
                        
                        print(f"✅ Success (HTTP {response.status})")
                        print()
                        
                        # Display key fields
                        if data.get('AbstractText'):
                            print(f"Abstract: {data['AbstractText'][:150]}...")
                            print(f"Source: {data.get('AbstractSource', 'N/A')}")
                        
                        if data.get('Heading'):
                            print(f"Heading: {data['Heading']}")
                        
                        if data.get('Answer'):
                            print(f"Instant Answer: {data['Answer']}")
                            print(f"Type: {data.get('AnswerType', 'N/A')}")
                        
                        if data.get('Definition'):
                            print(f"Definition: {data['Definition'][:150]}...")
                        
                        related = data.get('RelatedTopics', [])
                        if related:
                            print(f"Related Topics: {len(related)} items")
                        
                        result_type = data.get('Type', '')
                        if result_type:
                            type_names = {
                                'A': 'Article',
                                'D': 'Disambiguation',
                                'C': 'Category',
                                'N': 'Name',
                                'E': 'Exclusive'
                            }
                            print(f"Type: {type_names.get(result_type, result_type)}")
                        
                        print()
                        print("✅ Test Passed")
                        
                    else:
                        print(f"❌ HTTP {response.status}")
                        print(await response.text())
                        print()
                        print("❌ Test Failed")
                
            except Exception as e:
                print(f"❌ Error: {e}")
                print()
                print("❌ Test Failed")
            
            print()
    
    print("=" * 80)
    print("ALL TESTS COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(test_duckduckgo_direct())
