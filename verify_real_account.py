#!/usr/bin/env python3
"""
Quick verification for Real Account Setup
Shows account status without placing trades
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from trading_bot.platforms.deriv_platform import DerivPlatform
import logging

logging.basicConfig(level=logging.WARNING)

def verify_real_account(api_token: str):
    """Verify real account connection"""
    
    print("\n" + "="*70)
    print("DERIV REAL ACCOUNT VERIFICATION")
    print("="*70)
    
    try:
        print("\n[1] Connecting to real account...")
        deriv = DerivPlatform(api_token=api_token, account_type="real")
        
        if deriv.connect():
            # Get balance
            balance = deriv.get_balance()
            status = deriv.get_account_status()
            
            print("\n[OK] REAL ACCOUNT CONNECTED")
            print("─" * 70)
            print(f"Account Type: Real Trading")
            print(f"Portfolio Value: ${balance['portfolio_value']:.2f}")
            print(f"Available Cash: ${balance['cash']:.2f}")
            print(f"Buying Power: ${balance['buying_power']:.2f}")
            
            if status:
                print(f"Account Status: {status}")
            
            print("─" * 70)
            print("\n[OK] Ready for real account trading!")
            print("\nNEXT STEPS:")
            print("1. Test strategy on DEMO account first")
            print("2. Start with small trade amounts ($5-$10)")
            print("3. Monitor trades carefully")
            print("4. Gradually increase amounts as you gain confidence")
            
            return True
        else:
            print("\n[ERROR] Failed to connect to real account")
            print("Please check your API token and try again")
            return False
            
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        return False

if __name__ == "__main__":
    # Get API token from environment or input
    api_token = os.getenv("DERIV_API_TOKEN")
    
    if not api_token:
        print("\nEnter your Deriv REAL account API token:")
        print("(Go to: app.deriv.com → Settings → API tokens)")
        api_token = input("\nAPI Token: ").strip()
    
    if api_token:
        verify_real_account(api_token)
    else:
        print("\n[ERROR] No API token provided")
        print("="*70)
