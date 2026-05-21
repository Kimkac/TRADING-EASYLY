#!/usr/bin/env python3
"""
QUICK START TRADING BOT - Demo Account
One command to start trading!

Run this: python start_bot.py
"""

import os
import sys

# Ensure token is set
TOKEN = "KyalQ6MUAnoB5Fb"
os.environ["DERIV_API_TOKEN"] = TOKEN

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Run the trading bot
from examples.deriv_quickstart import main

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🚀 STARTING DERIV TRADING BOT - DEMO ACCOUNT")
    print("="*70)
    print(f"\nAPI Token: {TOKEN[:10]}...{TOKEN[-5:]}")
    print("Account: Demo ($9,999.49)")
    print("Strategy: Moving Average (5/20)")
    print("Symbol: EUR_USD")
    print("Trade Size: 10 USD")
    print("\nPress Ctrl+C to stop the bot\n")
    print("="*70 + "\n")
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n" + "="*70)
        print("✓ Bot stopped")
        print("="*70)
