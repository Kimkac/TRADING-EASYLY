#!/usr/bin/env python3
"""
Test different Deriv API endpoints
"""

import requests
import os

api_token = os.getenv("DERIV_API_TOKEN")

if not api_token:
    print("[ERROR] DERIV_API_TOKEN not set")
    exit(1)

endpoints = [
    "https://api.deriv.com/api/v3",
    "https://api.deriv.com/api",
    "https://api.deriv.app/api/v3",
    "https://ws.derivws.com/websockets/v3",
]

print(f"Testing API token: {api_token[:20]}...\n")
print("="*60)

for endpoint in endpoints:
    print(f"\nTesting: {endpoint}")
    try:
        payload = {
            "ping": 1,
            "req_id": 1
        }
        
        if "websockets" in endpoint.lower() or "ws" in endpoint.lower():
            print("  [SKIP] WebSocket endpoint (need different client)")
        else:
            response = requests.post(endpoint, json=payload, timeout=5)
            print(f"  Status: {response.status_code}")
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"  Response: {list(data.keys())[:5]}")
                except:
                    print(f"  Response: Not JSON (likely HTML)")
            else:
                print(f"  Error: {response.status_code}")
    except Exception as e:
        print(f"  Error: {type(e).__name__}")

print("\n" + "="*60)
print("\nNote: Deriv may have moved to WebSocket API v3")
print("Current implementation uses REST API")
print("May need to update to WebSocket or check API status")
