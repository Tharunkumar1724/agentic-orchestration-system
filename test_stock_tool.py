"""
Test Stock Prediction Tool
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_stock_tool():
    """Test stock prediction tool execution"""
    
    # Test stocks
    symbols = ["AAPL", "GOOGL", "MSFT", "TSLA"]
    
    print("="*70)
    print("STOCK PREDICTION TOOL - TEST")
    print("="*70)
    print()
    
    for symbol in symbols:
        print(f"Testing: {symbol}")
        print("-" * 70)
        
        response = requests.post(
            f"{BASE_URL}/tools/stock_prediction_tool/execute",
            json={"parameters": {"symbol": symbol}}
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("success"):
                chart_data = data.get("data", {}).get("json", {}).get("chart", {})
                
                if chart_data.get("result"):
                    result = chart_data["result"][0]
                    meta = result.get("meta", {})
                    
                    print(f"✅ SUCCESS")
                    print(f"   Symbol: {meta.get('symbol')}")
                    print(f"   Price: ${meta.get('regularMarketPrice', 'N/A')}")
                    print(f"   Currency: {meta.get('currency', 'N/A')}")
                    print(f"   Exchange: {meta.get('fullExchangeName', 'N/A')}")
                    print(f"   Execution Time: {data.get('execution_time', 0):.2f}s")
                    
                    # Check if we have historical data
                    timestamps = result.get("timestamp", [])
                    if timestamps:
                        print(f"   Historical Data Points: {len(timestamps)}")
                else:
                    error = chart_data.get("error", {})
                    print(f"❌ API Error: {error.get('description', 'Unknown error')}")
            else:
                print(f"❌ Tool execution failed")
                print(f"   Error: {data.get('error', 'Unknown error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
        
        print()
    
    print("="*70)
    print("TEST COMPLETE")
    print("="*70)

if __name__ == "__main__":
    test_stock_tool()
