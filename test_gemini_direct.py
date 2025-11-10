"""
Test Gemini Client with Direct API Calls (No LangChain)
"""
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from app.services.gemini_client import get_gemini_client

def test_generate():
    """Test basic text generation"""
    print("\n=== Testing generate() ===")
    client = get_gemini_client()
    
    result = client.generate("What is 2+2? Give a brief answer.")
    print(f"Response: {result.get('text', 'No text')}")
    print(f"Success: {'text' in result}")
    
def test_extract_facts():
    """Test fact extraction from workflow output"""
    print("\n=== Testing extract_facts() ===")
    client = get_gemini_client()
    
    workflow_output = """
    The data analysis workflow processed 1000 customer records.
    Key findings:
    - 45% of customers are repeat buyers
    - Average order value is $127
    - Peak sales occur on weekends
    - Mobile app generates 60% of orders
    """
    
    result = client.extract_facts(
        workflow_output,
        context="Data Analysis workflow - Analyze customer purchase patterns"
    )
    
    print(f"Summary: {result.summary}")
    print(f"Facts ({len(result.facts)}):")
    for i, fact in enumerate(result.facts, 1):
        print(f"  {i}. {fact}")
    print(f"Reasoning: {result.reasoning}")
    
def test_summarize_conversation():
    """Test conversation summarization"""
    print("\n=== Testing summarize_conversation() ===")
    client = get_gemini_client()
    
    messages = [
        {"role": "user", "content": "Find all customers in California"},
        {"role": "assistant", "content": "Found 234 customers in California"},
        {"role": "user", "content": "Filter for purchases over $100"},
        {"role": "assistant", "content": "Filtered to 89 high-value customers"}
    ]
    
    summary = client.summarize_conversation(
        messages,
        workflow_context="Customer filtering workflow"
    )
    print(f"Summary: {summary}")

def test_handoff_reasoning():
    """Test workflow handoff reasoning"""
    print("\n=== Testing reason_about_handoff() ===")
    client = get_gemini_client()
    
    result = client.reason_about_handoff(
        source_workflow_summary="Identified 89 high-value California customers with purchases over $100",
        source_facts=[
            "234 total customers in California",
            "89 customers with purchases over $100",
            "Average purchase value: $156"
        ],
        target_workflow_description="Send targeted email campaign to high-value customers"
    )
    
    print(f"Handoff Data: {result.get('handoff_data', 'N/A')}")
    print(f"Relevance: {result.get('relevance', 'N/A')}")
    print(f"Context: {result.get('context', 'N/A')}")

if __name__ == "__main__":
    print("Testing Gemini Client (Direct API - No LangChain)")
    print("=" * 60)
    
    try:
        test_generate()
        test_extract_facts()
        test_summarize_conversation()
        test_handoff_reasoning()
        
        print("\n" + "=" * 60)
        print("✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
