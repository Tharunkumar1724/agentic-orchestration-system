"""
Test script to demonstrate formatted workflow outputs.
Shows different output formats: structured, compact, text, and raw.
"""

import asyncio
import json
from app.services.orchestrator import orchestrator
from app.storage import load


async def test_formatted_outputs():
    """Test different output formatting options."""
    
    # Load a test workflow
    workflow = load("workflows", "test-sequential-workflow")
    
    if not workflow:
        print("ERROR: test-sequential-workflow not found!")
        print("Please create a workflow first using the API or frontend.")
        return
    
    print("=" * 80)
    print("TESTING WORKFLOW OUTPUT FORMATS")
    print("=" * 80)
    print(f"Workflow: {workflow.get('name', workflow.get('id'))}")
    print()
    
    # 1. Test STRUCTURED format (default)
    print("\n" + "=" * 80)
    print("1. STRUCTURED FORMAT (Default)")
    print("=" * 80)
    result_structured = await orchestrator.run_workflow(workflow, format_output=True)
    print(json.dumps(result_structured, indent=2, default=str))
    
    # 2. Test COMPACT format
    print("\n" + "=" * 80)
    print("2. COMPACT FORMAT")
    print("=" * 80)
    from app.services.output_formatter import output_formatter
    result_compact = output_formatter.format_compact(result_structured)
    print(json.dumps(result_compact, indent=2, default=str))
    
    # 3. Test TEXT format
    print("\n" + "=" * 80)
    print("3. TEXT FORMAT")
    print("=" * 80)
    text_output = output_formatter.format_for_display(result_structured)
    print(text_output)
    
    # 4. Show RAW format (for comparison)
    print("\n" + "=" * 80)
    print("4. RAW FORMAT (Unformatted - for debugging)")
    print("=" * 80)
    result_raw = await orchestrator.run_workflow(workflow, format_output=False)
    # Only show first 1000 chars of raw output as it's very verbose
    raw_json = json.dumps(result_raw, indent=2, default=str)
    if len(raw_json) > 2000:
        print(raw_json[:2000])
        print("\n... (truncated, too long) ...")
    else:
        print(raw_json)
    
    print("\n" + "=" * 80)
    print("SUMMARY OF FORMATS:")
    print("=" * 80)
    print("✓ STRUCTURED: Clean, organized output with summary and metadata")
    print("✓ COMPACT: Minimal output with just essential responses")
    print("✓ TEXT: Human-readable report format")
    print("✓ RAW: Full technical details (for debugging)")
    print("=" * 80)


async def test_api_format_parameter():
    """Demonstrate how to use format parameter in API requests."""
    
    print("\n" + "=" * 80)
    print("API FORMAT PARAMETER USAGE")
    print("=" * 80)
    print()
    print("You can now specify output format when running workflows via API:")
    print()
    print("1. Structured format (default):")
    print('   POST /workflows/{workflow_id}/run?format=structured')
    print()
    print("2. Compact format:")
    print('   POST /workflows/{workflow_id}/run?format=compact')
    print()
    print("3. Text format:")
    print('   POST /workflows/{workflow_id}/run?format=text')
    print()
    print("4. Raw format (unformatted):")
    print('   POST /workflows/{workflow_id}/run?format=raw')
    print()
    print("Example with curl:")
    print('  curl -X POST "http://localhost:8000/workflows/my-workflow/run?format=compact" \\')
    print('       -H "Content-Type: application/json" \\')
    print('       -d \'{"query": "Tell me about AI"}\'')
    print("=" * 80)


if __name__ == "__main__":
    print("Starting formatted output tests...")
    print()
    
    asyncio.run(test_formatted_outputs())
    asyncio.run(test_api_format_parameter())
    
    print("\n✅ Testing complete!")
    print("\nNow your workflow outputs will be clean and structured!")
