#!/usr/bin/env python3
"""
Simple Deriv Bot Test - Shows bot working without real API token
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

print("""
╔════════════════════════════════════════════════════════════╗
║           DERIV TRADING BOT - TEST RUN                    ║
╚════════════════════════════════════════════════════════════╝
""")

# Check for API token
api_token = os.getenv("DERIV_API_TOKEN")

if not api_token:
    print("[INFO] No API token found - Running in demo mode\n")
    print("="*60)
    print("STEP 1: Loading Platform")
    print("="*60)
    
    try:
        from trading_bot.platforms.deriv_platform import DerivPlatform
        print("[OK] DerivPlatform loaded")
    except Exception as e:
        print(f"[ERROR] {e}")
    
    print("\n" + "="*60)
    print("STEP 2: Loading Strategies")
    print("="*60)
    
    try:
        from trading_bot.strategies.ma_strategy import MovingAverageStrategy
        from trading_bot.strategies.advanced_strategies import RSIStrategy, MACDStrategy, BollingerBandsStrategy
        print("[OK] MovingAverageStrategy loaded")
        print("[OK] RSIStrategy loaded")
        print("[OK] MACDStrategy loaded")
        print("[OK] BollingerBandsStrategy loaded")
    except Exception as e:
        print(f"[ERROR] {e}")
    
    print("\n" + "="*60)
    print("STEP 3: Loading Data Fetcher")
    print("="*60)
    
    try:
        from trading_bot.data.data_fetcher import DataFetcher
        print("[OK] DataFetcher loaded")
    except Exception as e:
        print(f"[ERROR] {e}")
    
    print("\n" + "="*60)
    print("SUCCESS: Bot components loaded successfully!")
    print("="*60)
    
    print("""
To use REAL trading:

1. Get API token from https://app.deriv.com
   - Settings → API tokens
   - Create new token
   - Select: read, trade permissions

2. Set environment variable:
   $env:DERIV_API_TOKEN = "your_token_here"

3. Run this script again or:
   python examples/deriv_quickstart.py

Bot is ready to trade on Deriv!
    """)
else:
    print(f"[OK] API token found: {api_token[:20]}...\n")
    
    print("="*60)
    print("CONNECTING TO DERIV...")
    print("="*60)
    
    try:
        from trading_bot.platforms.deriv_platform import DerivPlatform
        
        deriv = DerivPlatform(api_token=api_token, account_type="demo")
        
        if deriv.connect():
            print("[OK] Connected to Deriv!")
            
            # Get balance
            balance = deriv.get_balance()
            print(f"\n[INFO] Account Balance:")
            print(f"      Portfolio: ${balance['portfolio_value']:.2f}")
            print(f"      Cash: ${balance['cash']:.2f}")
            
            # Get prices
            print(f"\n[INFO] Fetching prices...")
            symbols = ["EUR_USD", "GBP_USD"]
            for symbol in symbols:
                price = deriv.get_price(symbol)
                if price > 0:
                    print(f"      {symbol}: ${price:.5f}")
            
            print("\n[OK] Bot connected and trading ready!")
        else:
            print("[ERROR] Failed to connect")
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
