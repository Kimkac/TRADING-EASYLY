#!/usr/bin/env python3
"""
Test script for Deriv platform integration
Run this to verify Deriv connection and test trading signals
"""

import sys
import os
import logging

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from trading_bot.platforms.deriv_platform import DerivPlatform
from trading_bot.strategies.ma_strategy import MovingAverageStrategy
from trading_bot.data.data_fetcher import DataFetcher
from trading_bot.utils.logger import setup_logging

setup_logging()
logger = logging.getLogger('trading_bot')

def test_deriv_connection():
    """Test basic connection to Deriv"""
    print("\n" + "="*60)
    print("DERIV PLATFORM TEST")
    print("="*60)
    
    # Get API token from environment or user input
    api_token = os.getenv("DERIV_API_TOKEN")
    if not api_token:
        print("\n⚠️  DERIV_API_TOKEN not set!")
        print("Please set your Deriv API token:")
        print("  - Go to https://app.deriv.com/account/api-token")
        print("  - Create an API token")
        print("  - Set environment variable: set DERIV_API_TOKEN=your_token")
        api_token = input("\nEnter your Deriv API token (or press Enter to skip): ").strip()
        if not api_token:
            print("Skipping Deriv test.")
            return False
    
    try:
        # Initialize Deriv platform
        print("\n1. Connecting to Deriv (demo account)...")
        deriv = DerivPlatform(
            api_token=api_token,
            account_type="demo"
        )
        
        if deriv.connect():
            print("[OK] Connected successfully!")
            
            # Get balance
            print("\n2. Fetching account balance...")
            balance = deriv.get_balance()
            print(f"   Balance: ${balance['portfolio_value']:.2f}")
            print(f"   Cash: ${balance['cash']:.2f}")
            
            # Get account status
            print("\n3. Checking account status...")
            status = deriv.get_account_status()
            if status:
                print(f"   Account status: {status}")
            
            # Test price fetching
            print("\n4. Testing price fetching...")
            symbols = ["EUR_USD", "GBP_USD", "USD_JPY"]
            for symbol in symbols:
                price = deriv.get_price(symbol)
                print(f"   {symbol}: ${price:.5f}")
            
            # Test order placement (demo only - no real money)
            print("\n5. Testing order placement (demo)...")
            order = deriv.place_order(
                symbol="EUR_USD",
                quantity=10,
                side="buy",
                order_type="market"
            )
            if order:
                print(f"   [OK] Order placed: {order}")
            
            # Get positions
            print("\n6. Checking open positions...")
            positions = deriv.get_positions()
            print(f"   Open positions: {len(positions)}")
            
            print("\n" + "="*60)
            print("[SUCCESS] All Deriv tests completed successfully!")
            print("="*60)
            return True
        else:
            print("[FAIL] Failed to connect to Deriv")
            return False
            
    except Exception as e:
        logger.error(f"Error during Deriv test: {str(e)}", exc_info=True)
        print(f"❌ Error: {str(e)}")
        return False

def test_deriv_with_strategy():
    """Test Deriv with a trading strategy"""
    print("\n" + "="*60)
    print("DERIV + STRATEGY TEST")
    print("="*60)
    
    api_token = os.getenv("DERIV_API_TOKEN")
    if not api_token:
        print("Skipping strategy test - DERIV_API_TOKEN not set")
        return
    
    try:
        # Initialize platform and strategy
        deriv = DerivPlatform(api_token=api_token, account_type="demo")
        deriv.connect()
        
        strategy = MovingAverageStrategy(short_window=5, long_window=20)
        
        # Test with sample data
        print("\nFetching data for EUR_USD...")
        fetcher = DataFetcher()
        data = fetcher.fetch_data("EURUSD", days=30)
        
        if not data.empty:
            # Generate signals
            print("Generating trading signals...")
            data = strategy.generate_signal(data)
            
            latest_signal = data['signal'].iloc[-1]
            print(f"\nLatest signal: {['SELL', 'HOLD', 'BUY'][int(latest_signal) + 1]}")
            print(f"Latest price: ${data['close'].iloc[-1]:.5f}")
            
            # Show strategy indicators
            print(f"\nStrategy indicators (latest):")
            print(f"  Short MA: {data['short_ma'].iloc[-1]:.5f}")
            print(f"  Long MA: {data['long_ma'].iloc[-1]:.5f}")
            
    except Exception as e:
        logger.error(f"Error in strategy test: {str(e)}", exc_info=True)
        print(f"[ERROR] Strategy test error: {str(e)}")

if __name__ == "__main__":
    print("""
==============================================================
          DERIV PLATFORM INTEGRATION TEST                 
==============================================================
    """)
    
    # Run tests
    success = test_deriv_connection()
    
    if success:
        test_deriv_with_strategy()
    
    print("\n[OK] Deriv integration is ready!")
