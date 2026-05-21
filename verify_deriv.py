#!/usr/bin/env python3
"""Quick verification test for Deriv API connection"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from trading_bot.platforms.deriv_platform import DerivPlatform
import logging

# Suppress verbose logging
logging.basicConfig(level=logging.WARNING)

print("\n" + "="*60)
print("DERIV API CONNECTION TEST")
print("="*60)

api_token = os.getenv("DERIV_API_TOKEN", "KyalQ6MUAnoB5Fb")

try:
    deriv = DerivPlatform(api_token=api_token, account_type="demo")
    
    if deriv.connect():
        balance = deriv.get_balance()
        print("\n[OK] CONNECTION STATUS")
        print(f"  - Status: CONNECTED")
        print(f"  - Account Type: Demo")
        print(f"  - Balance: ${balance['portfolio_value']:.2f}")
        print(f"  - Cash: ${balance['cash']:.2f}")
        print("\n[OK] Deriv API is working with WebSocket!")
        print("="*60 + "\n")
    else:
        print("\n[FAILED] Could not connect to Deriv")
        print("="*60 + "\n")
        
except Exception as e:
    print(f"\n[ERROR] {str(e)}")
    print("="*60 + "\n")
