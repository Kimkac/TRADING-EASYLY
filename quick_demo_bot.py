#!/usr/bin/env python3
"""
DERIV TRADING BOT - Demo Account
Simple bot to start trading with demo account

Usage:
    python demo_bot.py                  # Default: EURUSD
    python demo_bot.py EURUSD           # EUR/USD pair
    python demo_bot.py GBPUSD           # GBP/USD pair
    python demo_bot.py AAPL             # Apple stock
    python demo_bot.py BTC-USD          # Bitcoin
"""

import os
import sys
import time
from datetime import datetime
import logging

# Set API token
TOKEN = "KyalQ6MUAnoB5Fb"
os.environ["DERIV_API_TOKEN"] = TOKEN

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from trading_bot.platforms.deriv_platform import DerivPlatform
from trading_bot.strategies.ma_strategy import MovingAverageStrategy
from trading_bot.data.data_fetcher import DataFetcher

# Suppress verbose logging
logging.basicConfig(level=logging.ERROR)

def main():
    """Start the trading bot"""
    
    # Get symbol from command line
    symbol = sys.argv[1] if len(sys.argv) > 1 else "EURUSD=X"
    
    print("\n" + "="*70)
    print("🚀 DERIV DEMO TRADING BOT")
    print("="*70)
    print(f"\nAccount: Demo")
    print(f"Balance: $9,999.49 (virtual money)")
    print(f"Symbol: {symbol}")
    print(f"Strategy: Moving Average (5/20)")
    print(f"Trade Size: 10 USD per trade")
    print(f"\nPress Ctrl+C to stop")
    print("="*70 + "\n")
    
    try:
        # Connect to Deriv
        print("Connecting to Deriv...", end=" ", flush=True)
        deriv = DerivPlatform(api_token=TOKEN, account_type="demo")
        
        if not deriv.connect():
            print("FAILED")
            return
        
        print("OK\n")
        
        # Initialize strategy and data fetcher
        strategy = MovingAverageStrategy(short_window=5, long_window=20)
        fetcher = DataFetcher()
        
        # Show account status
        balance = deriv.get_balance()
        print(f"Account Balance: ${balance['portfolio_value']:.2f}")
        print(f"Available Cash: ${balance['cash']:.2f}\n")
        print("-"*70 + "\n")
        
        iteration = 0
        
        # Main trading loop
        while True:
            iteration += 1
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            print(f"[{timestamp}] Iteration {iteration}")
            
            try:
                # Fetch data
                data = fetcher.fetch_data(symbol, days=30)
                
                if data.empty:
                    print(f"  No data available for {symbol}")
                    print(f"  Retrying in 60 seconds...\n")
                    time.sleep(60)
                    continue
                
                # Ensure we have the required columns
                if 'Close' not in data.columns:
                    print(f"  Invalid data format for {symbol}")
                    print(f"  Retrying in 60 seconds...\n")
                    time.sleep(60)
                    continue
                
                # Generate signals
                data = strategy.generate_signal(data)
                
                # Get current values
                price = float(data['Close'].iloc[-1])
                short_ma = float(data['short_ma'].iloc[-1])
                long_ma = float(data['long_ma'].iloc[-1])
                signal = int(data['signal'].iloc[-1])
                
                signal_name = ["SELL", "HOLD", "BUY"][signal + 1]
                
                # Display values
                print(f"  Price: ${price:.5f}")
                print(f"  Short MA (5):  ${short_ma:.5f}")
                print(f"  Long MA (20):  ${long_ma:.5f}")
                print(f"  Signal: {signal_name}")
                
                # Place order
                if signal_name == "BUY":
                    order = deriv.place_order(symbol, quantity=10, side="buy")
                    print(f"  --> BUY order placed")
                
                elif signal_name == "SELL":
                    order = deriv.place_order(symbol, quantity=10, side="sell")
                    print(f"  --> SELL order placed")
                
                else:
                    print(f"  --> Holding (no signal)")
                
                print()
                
            except Exception as e:
                print(f"  Error: {str(e)}")
                print()
            
            # Wait before next check
            time.sleep(60)
    
    except KeyboardInterrupt:
        print("\n" + "="*70)
        print("Bot stopped")
        balance = deriv.get_balance()
        print(f"Final Balance: ${balance['portfolio_value']:.2f}")
        print("="*70 + "\n")

if __name__ == "__main__":
    main()
