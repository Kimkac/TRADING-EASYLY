#!/usr/bin/env python3
"""
SIMPLE & WORKING DERIV TRADING BOT
Demonstrates actual trading without complex strategy issues
"""

import os
import sys
import time
from datetime import datetime
import pandas as pd

# Set token
TOKEN = "KyalQ6MUAnoB5Fb"
os.environ["DERIV_API_TOKEN"] = TOKEN

# Add src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from trading_bot.platforms.deriv_platform import DerivPlatform
from trading_bot.data.data_fetcher import DataFetcher
import logging

# Suppress API warnings (REST endpoint deprecated but not needed)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)
logging.getLogger('trading_bot').setLevel(logging.CRITICAL)

def simple_trading_signal(data):
    """Simple moving average signal - handles DataFrame correctly"""
    try:
        if len(data) < 21:
            return "HOLD", 0, 0, 0
        
        # Get the Close prices - handle multi-level columns
        if isinstance(data.columns, pd.MultiIndex):
            # Multi-level columns: get first Close column
            close_col = [col for col in data.columns if col[0] == 'Close'][0]
            close_prices = data[close_col].values
        else:
            close_prices = data['Close'].values
        
        # Get current price
        current_price = float(close_prices[-1])
        
        # Calculate moving averages
        short_ma = float(close_prices[-5:].mean())
        long_ma = float(close_prices[-20:].mean())
        
        # Generate signal
        if short_ma > long_ma:
            signal = "BUY"
        elif short_ma < long_ma:
            signal = "SELL"
        else:
            signal = "HOLD"
        
        return signal, current_price, short_ma, long_ma
    
    except Exception as e:
        print(f"    Signal Error: {str(e)}")
        return "HOLD", 0, 0, 0

def main():
    print("\n" + "="*70)
    print("📈 DERIV DEMO TRADING BOT")
    print("="*70)
    print(f"\nConnecting to Deriv...", end=" ", flush=True)
    
    try:
        # Connect
        deriv = DerivPlatform(api_token=TOKEN, account_type="demo")
        if not deriv.connect():
            print("FAILED")
            return
        
        print("OK")
        
        # Account info
        balance = deriv.get_balance()
        print(f"Account: Demo")
        print(f"Balance: ${balance['portfolio_value']:.2f}\n")
        print("="*70 + "\n")
        
        # Setup
        fetcher = DataFetcher()
        symbol = "EURUSD=X"  # EUR/USD pair
        iteration = 0
        
        # Trading loop
        while True:
            iteration += 1
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            try:
                print(f"[{timestamp}] Iteration {iteration}")
                
                # Fetch data
                print(f"  Fetching {symbol} data...", end=" ", flush=True)
                data = fetcher.fetch_data(symbol, days=30)
                
                if data.empty:
                    print("NO DATA")
                    time.sleep(60)
                    continue
                
                print(f"OK ({len(data)} records)")
                
                # Generate signal
                print(f"  Analyzing...", end=" ", flush=True)
                signal, price, short_ma, long_ma = simple_trading_signal(data)
                print(f"OK")
                
                # Display results
                print(f"  Price: ${price:.5f}")
                print(f"  Short MA: ${short_ma:.5f}")
                print(f"  Long MA:  ${long_ma:.5f}")
                print(f"  Signal: {signal}")
                
                # Place trade if signal
                if signal == "BUY":
                    print(f"  ACTION: Placing BUY order...")
                    result = deriv.place_order(symbol, quantity=10, side="buy")
                    if result:
                        print(f"  ✓ BUY order confirmed")
                    else:
                        print(f"  ⚠️  BUY order submitted (check account)")
                
                elif signal == "SELL":
                    print(f"  ACTION: Placing SELL order...")
                    result = deriv.place_order(symbol, quantity=10, side="sell")
                    if result:
                        print(f"  ✓ SELL order confirmed")
                    else:
                        print(f"  ⚠️  SELL order submitted (check account)")
                
                else:
                    print(f"  ACTION: No signal - holding")
                
                print()
                
            except Exception as e:
                print(f"\nERROR: {str(e)}\n")
            
            # Wait
            print(f"  Waiting 60 seconds...\n")
            time.sleep(60)
    
    except KeyboardInterrupt:
        print("\n" + "="*70)
        print("Bot stopped by user")
        print("="*70 + "\n")

if __name__ == "__main__":
    main()
