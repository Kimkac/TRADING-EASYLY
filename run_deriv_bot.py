#!/usr/bin/env python3
"""
Interactive Deriv Bot Setup & Test
This script helps you set up and test the trading bot with Deriv
"""

import os
import sys

# Add src to path so we can import trading_bot
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    print("""
╔════════════════════════════════════════════════════════════╗
║           DERIV TRADING BOT - SETUP & TEST                ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    # Check for API token
    api_token = os.getenv("DERIV_API_TOKEN")
    
    if not api_token:
        print("""
⚠️  NO API TOKEN FOUND

To get your API token:
1. Open https://app.deriv.com in your browser
2. Log in to your account
3. Go to Settings → API tokens
4. Click "Create new token"
5. Name it: "Trading Bot"
6. Select permissions: read, trade
7. Copy the token

Then run one of these commands:

Windows (PowerShell):
  $env:DERIV_API_TOKEN = "paste_your_token_here"
  
Windows (Command Prompt):
  set DERIV_API_TOKEN=paste_your_token_here
  
Linux/macOS:
  export DERIV_API_TOKEN="paste_your_token_here"

Or pass it directly:
  python run_deriv_bot.py your_token_here
        """)
        
        # Check if token passed as argument
        if len(sys.argv) > 1:
            api_token = sys.argv[1]
            print(f"\n✓ Using token from argument: {api_token[:20]}...")
            os.environ["DERIV_API_TOKEN"] = api_token
        else:
            print("\n❌ Please set your API token and try again.")
            return False
    else:
        print(f"✓ API Token found: {api_token[:20]}...")
    
    print("\n" + "="*60)
    print("STEP 1: Testing Connection")
    print("="*60)
    
    try:
        from trading_bot.platforms.deriv_platform import DerivPlatform
        
        deriv = DerivPlatform(api_token=api_token, account_type="demo")
        
        print("Connecting to Deriv...")
        if deriv.connect():
            print("✅ Connected successfully!")
            
            # Get balance
            print("\n" + "="*60)
            print("STEP 2: Account Balance")
            print("="*60)
            balance = deriv.get_balance()
            print(f"Portfolio Value: ${balance['portfolio_value']:.2f}")
            print(f"Cash: ${balance['cash']:.2f}")
            print(f"Buying Power: ${balance['buying_power']:.2f}")
            
            # Get prices
            print("\n" + "="*60)
            print("STEP 3: Market Prices")
            print("="*60)
            symbols = ["EUR_USD", "GBP_USD", "USD_JPY"]
            for symbol in symbols:
                price = deriv.get_price(symbol)
                print(f"{symbol}: ${price:.5f}")
            
            # Account status
            print("\n" + "="*60)
            print("STEP 4: Account Status")
            print("="*60)
            status = deriv.get_account_status()
            print(f"Account Status: {status}")
            
            print("\n" + "="*60)
            print("✅ ALL TESTS PASSED!")
            print("="*60)
            print("\nYour bot is ready to trade!")
            print("\nNext steps:")
            print("1. Run: python examples/deriv_quickstart.py")
            print("2. Or use in your own strategy")
            print("\nDocumentation:")
            print("- DERIV_SETUP.md - Complete setup guide")
            print("- DERIV_INTEGRATION.md - Technical details")
            print("- examples/deriv_quickstart.py - Full example")
            
            return True
        else:
            print("❌ Failed to connect to Deriv")
            print("Check your API token and try again")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
