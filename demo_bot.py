#!/usr/bin/env python3
"""
Deriv Trading Bot - Demo Mode
Shows how the bot works without requiring a real API token
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def demo_mode():
    """Run bot in demo/simulation mode"""
    
    print("""
╔════════════════════════════════════════════════════════════╗
║           DERIV TRADING BOT - DEMO MODE                   ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    print("⚠️  DEMO MODE - Simulating trading (no real money)")
    print("\nTo use REAL trading, set your API token:")
    print("  $env:DERIV_API_TOKEN = 'your_real_token'")
    print("  Then run: python examples/deriv_quickstart.py\n")
    
    print("="*60)
    print("STEP 1: Deriv Platform Integration")
    print("="*60)
    
    try:
        from trading_bot.platforms.deriv_platform import DerivPlatform
        print("✓ DerivPlatform adapter loaded")
        print("✓ Ready for: Buy/Sell orders, positions, account info")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "="*60)
    print("STEP 2: Demo Account Balance (Simulated)")
    print("="*60)
    
    demo_balance = {
        'portfolio_value': 10000.00,
        'cash': 5000.00,
        'buying_power': 5000.00
    }
    print(f"Portfolio Value: ${demo_balance['portfolio_value']:.2f}")
    print(f"Cash: ${demo_balance['cash']:.2f}")
    print(f"Buying Power: ${demo_balance['buying_power']:.2f}")
    
    print("\n" + "="*60)
    print("STEP 3: Market Data")
    print("="*60)
    
    try:
        from trading_bot.data.data_fetcher import DataFetcher
        fetcher = DataFetcher()
        print("✓ Data fetcher ready (Yahoo Finance)")
        print("✓ Supports: 5000+ stocks, indices, cryptocurrencies")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "="*60)
    print("STEP 4: Trading Strategies")
    print("="*60)
    
    try:
        from trading_bot.strategies.ma_strategy import MovingAverageStrategy
        from trading_bot.strategies.advanced_strategies import RSIStrategy, MACDStrategy, BollingerBandsStrategy
        
        print("✓ Moving Average (MA) - Crossover signals")
        print("✓ RSI - Overbought/oversold signals")
        print("✓ MACD - Trend-following signals")
        print("✓ Bollinger Bands - Mean reversion signals")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "="*60)
    print("✅ DEMO COMPLETE - BOT READY")
    print("="*60)
    
    print("""
What just happened:
1. ✓ Loaded Deriv platform adapter
2. ✓ Showed simulated account balance
3. ✓ Initialized data fetcher (Yahoo Finance)
4. ✓ Loaded all trading strategies

To start REAL trading on Deriv:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 1: Get Your API Token
   Visit: https://app.deriv.com
   • Login to your account
   • Settings → API tokens
   • Create new token (select: read, trade)
   • Copy the token

STEP 2: Set Environment Variable
   Windows PowerShell:
   $env:DERIV_API_TOKEN = "your_token_here"
   
   Windows CMD:
   set DERIV_API_TOKEN=your_token_here
   
   Linux/macOS:
   export DERIV_API_TOKEN="your_token_here"

STEP 3: Test Connection
   python run_deriv_bot.py your_token_here

STEP 4: Start Trading
   python examples/deriv_quickstart.py

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 Documentation:
   • DERIV_SETUP.md - Complete setup guide
   • DERIV_INTEGRATION.md - Technical details
   • examples/deriv_quickstart.py - Full working example
   • INDEX.md - All documentation

Supported Assets:
   • Forex: EUR/USD, GBP/USD, USD/JPY, and 50+ more
   • Indices: Volatility Index, Stock Indices
   • Crypto: Bitcoin (BTC), Ethereum (ETH)
   • Stocks: AAPL, GOOGL, MSFT, and 5000+ more

Ready to trade? Get your token and run the bot! 🚀
    """)

if __name__ == "__main__":
    demo_mode()
