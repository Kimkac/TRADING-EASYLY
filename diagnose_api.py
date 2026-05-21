#!/usr/bin/env python3
"""
Deriv API Diagnostic - Check token validity
"""

import requests
import json
import os

api_token = os.getenv("DERIV_API_TOKEN")

if not api_token:
    print("[ERROR] DERIV_API_TOKEN not set")
    exit(1)

print(f"Testing Deriv API with token: {api_token[:15]}...")
print("="*60)

base_url = "https://api.deriv.com/api/v3"

# Test 1: Get account status
print("\n[TEST 1] Getting account status...")
try:
    payload = {
        "get_account_status": 1,
        "authorize": api_token,
        "app_id": 1089,
        "req_id": 1
    }
    response = requests.post(base_url, json=payload, timeout=10)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text[:200]}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"[OK] Response received: {list(data.keys())}")
    else:
        print(f"[ERROR] HTTP {response.status_code}")
except Exception as e:
    print(f"[ERROR] {e}")

# Test 2: Get balance
print("\n[TEST 2] Getting account balance...")
try:
    payload = {
        "balance": 1,
        "authorize": api_token,
        "app_id": 1089,
        "req_id": 2
    }
    response = requests.post(base_url, json=payload, timeout=10)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text[:300]}")
except Exception as e:
    print(f"[ERROR] {e}")

# Test 3: Get available assets
print("\n[TEST 3] Getting available underlyings...")
try:
    payload = {
        "active_symbols": "brief",
        "app_id": 1089,
        "req_id": 3
    }
    response = requests.post(base_url, json=payload, timeout=10)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        if "active_symbols" in data:
            symbols = data["active_symbols"][:5]
            print(f"[OK] Found {len(data.get('active_symbols', []))} symbols")
            print(f"Sample: {symbols}")
except Exception as e:
    print(f"[ERROR] {e}")

print("\n" + "="*60)
print("Diagnostic complete")
