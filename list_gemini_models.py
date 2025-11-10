"""
List available Gemini models
"""
import requests
import json

API_KEY = "your-gemini-api-key-here"  # Replace with your actual API key
URL = "https://generativelanguage.googleapis.com/v1/models"

full_url = f"{URL}?key={API_KEY}"

print(f"Fetching models from: {URL}\n")

response = requests.get(full_url)

print(f"Status Code: {response.status_code}\n")

if response.status_code == 200:
    data = response.json()
    
    if "models" in data:
        print(f"Found {len(data['models'])} models:\n")
        
        for model in data['models']:
            name = model.get('name', 'Unknown')
            supported_methods = model.get('supportedGenerationMethods', [])
            
            print(f"  Model: {name}")
            print(f"  Supports: {', '.join(supported_methods)}")
            
            # Check if it supports generateContent
            if 'generateContent' in supported_methods:
                print(f"  ✅ Can use for generateContent")
            print()
    else:
        print("No models found in response")
        print(json.dumps(data, indent=2))
else:
    print(f"Error: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
