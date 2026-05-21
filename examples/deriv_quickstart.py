#!/usr/bin/env python3
"""
Quick start example for trading on Deriv with Moving Average strategy
"""

import os
import sys
import time
from datetime import datetime
import logging

# Add src to path (go up one level from examples)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from trading_bot.platforms.deriv_platform import DerivPlatform
from trading_bot.strategies.ma_strategy import MovingAverageStrategy
from trading_bot.data.data_fetcher import DataFetcher
from trading_bot.utils.logger import setup_logging

logger = logging.getLogger('trading_bot')

def main():
    """Quick start trading bot for Deriv"""
    
    print("\n" + "="*70)
    print("DERIV TRADING BOT - QUICK START")
    print("="*70 + "\n")
    
    # Configuration
    API_TOKEN = os.getenv("DERIV_API_TOKEN")
    if not API_TOKEN:
        print("❌ Error: DERIV_API_TOKEN environment variable not set")
        print("\nTo set it:")
        print("  Windows (PowerShell): $env:DERIV_API_TOKEN = 'your_token'")
        print("  Windows (CMD): set DERIV_API_TOKEN=your_token")
        print("  Linux/macOS: export DERIV_API_TOKEN='your_token'")
        print("\nTo get your token:")
        print("  1. Go to https://app.deriv.com")
        print("  2. Settings → API tokens")
        print("  3. Create new token")
        return
    
    SYMBOL = "EUR_USD"
    QUANTITY = 10
    LOOKBACK_DAYS = 30
    SHORT_WINDOW = 5
    LONG_WINDOW = 20
    
    # Initialize platform
    print(f"[*] Connecting to Deriv...")
    deriv = DerivPlatform(
        api_token=API_TOKEN,
        account_type="demo"
    )
    
    if not deriv.connect():
        print("[ERROR] Failed to connect to Deriv")
        return
    
    print("[OK] Connected to Deriv\n")
    
    # Initialize strategy and data fetcher
    strategy = MovingAverageStrategy(
        short_window=SHORT_WINDOW,
        long_window=LONG_WINDOW
    )
    fetcher = DataFetcher()
    
    # Get account info
    balance = deriv.get_balance()
    print(f"📊 Account Status:")
    print(f"   Portfolio Value: ${balance['portfolio_value']:.2f}")
    print(f"   Cash: ${balance['cash']:.2f}\n")
    
    # Main trading loop
    print(f"🤖 Starting trading bot for {SYMBOL}")
    print(f"   Strategy: Moving Average ({SHORT_WINDOW}/{LONG_WINDOW})")
    print(f"   Position Size: {QUANTITY}")
    print(f"   Account Type: Demo\n")
    print("-" * 70)
    
    iteration = 0
    try:
        while True:
            iteration += 1
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"\n[{timestamp}] Iteration {iteration}")
            
            # Fetch market data
            try:
                print(f"  📥 Fetching {LOOKBACK_DAYS} days of data for {SYMBOL}...")
                data = fetcher.fetch_data(SYMBOL, days=LOOKBACK_DAYS)
                
                if data.empty:
                    print(f"  ⚠️  No data available for {SYMBOL}")
                    time.sleep(60)
                    continue
                
                # Generate trading signals
                data = strategy.generate_signal(data)
                
                # Get latest values
                latest_price = data['close'].iloc[-1]
                latest_signal = int(data['signal'].iloc[-1])
                short_ma = data['short_ma'].iloc[-1]
                long_ma = data['long_ma'].iloc[-1]
                
                # Display current status
                signal_text = ['🔴 SELL', '⚪ HOLD', '🟢 BUY'][latest_signal + 1]
                print(f"  💹 Price: ${latest_price:.5f}")
                print(f"  📈 Short MA ({SHORT_WINDOW}): ${short_ma:.5f}")
                print(f"  📉 Long MA ({LONG_WINDOW}): ${long_ma:.5f}")
                print(f"  🎯 Signal: {signal_text}")
                
                # Execute trades based on signal
                if latest_signal == 1:  # BUY signal
                    print(f"  ✅ BUY signal detected!")
                    order = deriv.place_order(
                        symbol=SYMBOL,
                        quantity=QUANTITY,
                        side="buy"
                    )
                    if order:
                        print(f"     Order placed: {order['order_id']}")
                
                elif latest_signal == -1:  # SELL signal
                    print(f"  ✅ SELL signal detected!")
                    order = deriv.place_order(
                        symbol=SYMBOL,
                        quantity=QUANTITY,
                        side="sell"
                    )
                    if order:
                        print(f"     Order placed: {order['order_id']}")
                
                else:  # HOLD
                    print(f"  ⏸️  No action (HOLD)")
                
                # Show open positions
                positions = deriv.get_positions()
                if positions:
                    print(f"  📋 Open positions: {len(positions)}")
                
                # Update balance
                balance = deriv.get_balance()
                print(f"  💰 Portfolio Value: ${balance['portfolio_value']:.2f}")
                
            except Exception as e:
                logger.error(f"Error in trading loop: {str(e)}", exc_info=True)
                print(f"  ❌ Error: {str(e)}")
            
            # Wait before next iteration (1 minute)
            print(f"  ⏳ Waiting 60 seconds until next check...")
            time.sleep(60)
    
    except KeyboardInterrupt:
        print("\n\n⛔ Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        print(f"\n❌ Fatal error: {str(e)}")

if __name__ == "__main__":
    main()
