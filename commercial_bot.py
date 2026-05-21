#!/usr/bin/env python3
"""
COMMERCIAL TRADING BOT - Multi-Plan Version
Enforces subscription tiers and features
Supports: Free, Pro, Enterprise, Desktop, Cloud
"""

import os
import sys
import time
from datetime import datetime

# Set token
TOKEN = os.getenv("DERIV_API_TOKEN", "KyalQ6MUAnoB5Fb")
os.environ["DERIV_API_TOKEN"] = TOKEN

# Add src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from trading_bot.platforms.deriv_platform import DerivPlatform
from trading_bot.data.data_fetcher import DataFetcher
from trading_bot.subscription import (
    get_license_manager,
    require_auto_trading,
    require_feature,
    PlanTier
)
import logging
import pandas as pd

logging.getLogger('urllib3').setLevel(logging.CRITICAL)
logging.getLogger('trading_bot').setLevel(logging.CRITICAL)

def show_subscription_status():
    """Display current subscription"""
    manager = get_license_manager()
    status = manager.get_status()
    
    print("\n" + "="*70)
    print("SUBSCRIPTION STATUS")
    print("="*70)
    print(f"Plan:           {status['plan'].upper()}")
    print(f"Status:         {status['status'].upper()}")
    print(f"Days Remaining: {status['days_remaining']}")
    print(f"Auto Trading:   {'✓ Enabled' if status['auto_trading'] else '✗ Disabled'}")
    print(f"Max Symbols:    {status['max_symbols'] if status['max_symbols'] > 0 else 'Unlimited'}")
    print(f"Platforms:      {', '.join(status['platforms'])}")
    print(f"Support:        {status['support_level'].title()}")
    print("="*70 + "\n")

def check_signal_interval(plan_tier: str):
    """Get signal check interval for plan"""
    intervals = {
        'free': 60,           # 1 check per hour
        'pro': 0,             # Unlimited
        'enterprise': 0,      # Unlimited
        'desktop': 0,         # Unlimited
        'cloud_pro': 0,       # Unlimited
        'cloud_enterprise': 0 # Unlimited
    }
    return intervals.get(plan_tier.lower(), 60)

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

@require_feature("signal_detection")
def fetch_and_analyze():
    """Fetch data and generate signals (requires feature)"""
    fetcher = DataFetcher()
    data = fetcher.fetch_data("EURUSD=X", days=30)
    
    if data.empty:
        return None, None, None, None
    
    return simple_trading_signal(data)

@require_auto_trading()
def execute_trade(signal: str, price: float):
    """Execute trade (requires auto trading)"""
    deriv = DerivPlatform(api_token=TOKEN, account_type="demo")
    deriv.connect()
    
    print(f"  [AUTO-TRADING] {signal} signal at ${price:.5f}")
    return True

def main():
    print("\n" + "="*70)
    print("📈 COMMERCIAL TRADING BOT")
    print("="*70)
    
    # Show subscription
    show_subscription_status()
    
    manager = get_license_manager()
    status = manager.get_status()
    
    # Check if subscription is active
    if status['status'] != 'active':
        print(f"ERROR: Subscription is {status['status']}")
        print("Upgrade your plan at: http://localhost:5000")
        print("Or activate with: python -c \"")
        print("  from trading_bot.subscription import get_license_manager, PlanTier")
        print("  get_license_manager().activate_license('key', 'user', PlanTier.PRO)\"")
        return
    
    # Check signal interval
    check_interval = check_signal_interval(status['plan'])
    
    print("FEATURES ENABLED:")
    print(f"  Signal Detection: {'✓' if 'signal_detection' in [f for f, v in status.items() if v] else '✗'}")
    print(f"  Auto Trading: {'✓' if status['auto_trading'] else '✗'}")
    print(f"  Backtesting: ✗ (not implemented)")
    print(f"  Signal Check Interval: Every {check_interval} seconds")
    print("\n" + "="*70 + "\n")
    
    # Connect to platform
    print("Connecting to Deriv...", end=" ", flush=True)
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
    
    iteration = 0
    last_signal = None
    total_signals = 0
    
    # Main loop
    while True:
        iteration += 1
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        try:
            print(f"[{timestamp}] Iteration {iteration}")
            
            # Enforce API limits
            try:
                from trading_bot.subscription import enforce_api_limit
                enforce_api_limit()
            except PermissionError as e:
                print(f"  ERROR: {e}")
                print("  Upgrade your plan to increase API limits")
                time.sleep(60)
                continue
            
            # Fetch data and analyze
            try:
                signal, price, short_ma, long_ma = fetch_and_analyze()
            except PermissionError as e:
                print(f"  ERROR: {e}")
                print("  This feature requires a Pro or higher subscription")
                time.sleep(60)
                continue
            
            if signal is None:
                print("  FAILED to fetch data")
                time.sleep(60)
                continue
            
            print(f"  Price: ${price:.5f}")
            print(f"  5-day MA:  ${short_ma:.5f}")
            print(f"  20-day MA: ${long_ma:.5f}")
            print(f"  Signal: {signal}")
            
            # Show action
            if signal != last_signal and signal != "HOLD":
                total_signals += 1
                
                if status['auto_trading']:
                    try:
                        execute_trade(signal, price)
                    except PermissionError as e:
                        print(f"  ERROR: {e}")
                else:
                    print(f"  SIGNAL: {signal} (auto-trading disabled in your plan)")
                
                last_signal = signal
            
            print(f"  Signals detected: {total_signals}")
            print()
            
        except KeyboardInterrupt:
            print("\n" + "="*70)
            print("Bot stopped by user")
            print("="*70)
            print(f"\nSummary:")
            print(f"  Total signals: {total_signals}")
            print(f"  Iterations: {iteration}")
            print(f"\nTo upgrade your subscription, visit: http://localhost:5000\n")
            break
        except Exception as e:
            print(f"  Error: {str(e)}\n")
        
        print(f"  Waiting {check_interval} seconds...\n")
        time.sleep(check_interval)

if __name__ == "__main__":
    main()
