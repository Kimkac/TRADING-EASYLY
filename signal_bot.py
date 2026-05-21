#!/usr/bin/env python3
"""
DERIV TRADING BOT - SIMPLIFIED VERSION
Shows all trading signals and demonstrates what would be traded
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

logging.getLogger('urllib3').setLevel(logging.CRITICAL)
logging.getLogger('trading_bot').setLevel(logging.CRITICAL)

def simple_trading_signal(data):
    """Generate trading signal"""
    try:
        if len(data) < 21:
            return "HOLD", 0, 0, 0
        
        # Get Close prices
        if isinstance(data.columns, pd.MultiIndex):
            close_col = [col for col in data.columns if col[0] == 'Close'][0]
            close_prices = data[close_col].values
        else:
            close_prices = data['Close'].values
        
        current_price = float(close_prices[-1])
        short_ma = float(close_prices[-5:].mean())
        long_ma = float(close_prices[-20:].mean())
        
        if short_ma > long_ma:
            signal = "BUY"
        elif short_ma < long_ma:
            signal = "SELL"
        else:
            signal = "HOLD"
        
        return signal, current_price, short_ma, long_ma
    except Exception as e:
        return "HOLD", 0, 0, 0

def main():
    print("\n" + "="*70)
    print("📈 DERIV TRADING BOT")
    print("="*70)
    
    # Connect
    print("\nConnecting to Deriv...", end=" ", flush=True)
    deriv = DerivPlatform(api_token=TOKEN, account_type="demo")
    
    if not deriv.connect():
        print("FAILED")
        return
    
    print("OK")
    
    # Get balance
    balance = deriv.get_balance()
    print(f"Account: Demo")
    print(f"Balance: ${balance['portfolio_value']:.2f}\n")
    print("="*70 + "\n")
    
    fetcher = DataFetcher()
    iteration = 0
    total_buy_signals = 0
    total_sell_signals = 0
    last_signal = None
    
    # Main loop
    while True:
        iteration += 1
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        try:
            print(f"[{timestamp}] Iteration {iteration}")
            
            # Get data
            print(f"  Fetching EUR/USD data...", end=" ", flush=True)
            data = fetcher.fetch_data("EURUSD=X", days=30)
            
            if data.empty:
                print("FAILED")
                time.sleep(60)
                continue
            
            print(f"OK ({len(data)} records)")
            
            # Get signal
            signal, price, short_ma, long_ma = simple_trading_signal(data)
            
            print(f"  Price: ${price:.5f}")
            print(f"  5-day MA:  ${short_ma:.5f}")
            print(f"  20-day MA: ${long_ma:.5f}")
            print(f"  Signal: {signal}")
            
            # Show action
            if signal == "BUY" and last_signal != "BUY":
                total_buy_signals += 1
                print(f"  🟢 BUY SIGNAL #{total_buy_signals}")
                print(f"     → Would BUY 10 USD")
                last_signal = "BUY"
            
            elif signal == "SELL" and last_signal != "SELL":
                total_sell_signals += 1
                print(f"  🔴 SELL SIGNAL #{total_sell_signals}")
                print(f"     → Would SELL 10 USD")
                last_signal = "SELL"
            
            elif signal == "HOLD":
                print(f"  ⚪ HOLD - No signal")
                last_signal = "HOLD"
            
            else:
                print(f"  ⊘ Signal maintained: {last_signal}")
            
            # Show stats
            print(f"  Stats: {total_buy_signals} buys, {total_sell_signals} sells")
            print()
            
        except KeyboardInterrupt:
            print("\n" + "="*70)
            print("Bot stopped")
            print("="*70)
            print(f"\nSummary:")
            print(f"  Total BUY signals: {total_buy_signals}")
            print(f"  Total SELL signals: {total_sell_signals}")
            print(f"  Total signals: {total_buy_signals + total_sell_signals}\n")
            break
        except Exception as e:
            print(f"  Error: {str(e)}\n")
        
        print(f"  Waiting 60 seconds...\n")
        time.sleep(60)

if __name__ == "__main__":
    main()
