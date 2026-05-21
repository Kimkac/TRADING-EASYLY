#!/usr/bin/env python3
"""
SIMPLE DERIV DEMO BOT - No Strategy Errors
Just shows connection and account status
"""

import os
import sys
from datetime import datetime

# Set token
TOKEN = "KyalQ6MUAnoB5Fb"
os.environ["DERIV_API_TOKEN"] = TOKEN

# Add src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from trading_bot.platforms.deriv_platform import DerivPlatform

def main():
    print("\n" + "="*70)
    print("🚀 DERIV DEMO ACCOUNT - STATUS")
    print("="*70)
    
    try:
        # Connect
        print("\nConnecting to Deriv...", end=" ", flush=True)
        deriv = DerivPlatform(api_token=TOKEN, account_type="demo")
        
        if deriv.connect():
            print("OK ✓\n")
        else:
            print("FAILED ✗")
            return
        
        # Get balance
        balance = deriv.get_balance()
        
        print("📊 Account Status:")
        print(f"   Account Type: Demo (Virtual Money)")
        print(f"   Portfolio Value: ${balance['portfolio_value']:.2f}")
        print(f"   Available Cash: ${balance['cash']:.2f}")
        print(f"   Buying Power: ${balance['buying_power']:.2f}")
        
        print(f"\n⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        print(f"\n✓ Connection Status: ACTIVE")
        print(f"✓ API Token: {'*' * 15}{TOKEN[-5:]}")
        print(f"✓ Account: Ready for trading")
        
        print("\n" + "="*70)
        print("Your demo account is ready to trade!")
        print("="*70 + "\n")
        
        print("Next steps:")
        print("1. Run the trading bot: python trading_bot.py")
        print("2. Monitor your trades")
        print("3. Switch to real account when ready")
        
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()
