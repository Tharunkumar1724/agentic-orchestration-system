"""
Quick test to see what Gemini actually returns
"""
import os
import requests
import json

API_KEY = "your-gemini-api-key-here"  # Replace with your actual API key
URL = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent"

full_url = f"{URL}?key={API_KEY}"

payload = {
    "contents": [{
        "parts": [{
            "text": "What is 2+2? Answer briefly."
        }]
    }],
    "generationConfig": {
        "temperature": 0.7,
        "topK": 40,
        "topP": 0.95,
        "maxOutputTokens": 2048,
    }
}

print(f"Making request to: {URL}")
print(f"With API key: {API_KEY[:10]}...")

response = requests.post(full_url, json=payload, headers={"Content-Type": "application/json"})

print(f"\nStatus Code: {response.status_code}")
print(f"Response Headers: {dict(response.headers)}")
print(f"\nResponse Body:")
print(json.dumps(response.json(), indent=2))
