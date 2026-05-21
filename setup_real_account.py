#!/usr/bin/env python3
"""
Deriv Real Account Configuration
This script helps set up the trading bot for real account trading.

IMPORTANT: Real account trading involves actual money. 
Proceed with caution and test thoroughly first!
"""

import os
import sys

def setup_real_account():
    """Setup instructions for real account trading"""
    
    print("\n" + "="*70)
    print("DERIV REAL ACCOUNT SETUP")
    print("="*70)
    
    print("""
IMPORTANT WARNINGS:
─────────────────────────────────────────────────────────────────────
⚠️  REAL MONEY TRADING - You are about to enable live trading
⚠️  This will use REAL money from your Deriv account
⚠️  Test thoroughly on demo account FIRST
⚠️  Start with SMALL amounts
⚠️  Never risk more than you can afford to lose
─────────────────────────────────────────────────────────────────────

RECOMMENDED STEPS:
─────────────────────────────────────────────────────────────────────
1. Thoroughly test your strategy on DEMO account
2. Verify all indicators and signals are correct
3. Start with SMALL trade sizes ($5-$10)
4. Monitor trades closely in the beginning
5. Gradually increase trade size as you gain confidence
─────────────────────────────────────────────────────────────────────
    """)
    
    # Confirm real account
    confirm = input("\nDo you want to proceed with REAL account setup? (yes/no): ").strip().lower()
    
    if confirm != "yes":
        print("\nSetup cancelled. Staying with demo account.")
        return False
    
    # Get API token
    print("\n" + "─"*70)
    print("STEP 1: Get Your Real Account API Token")
    print("─"*70)
    print("""
1. Go to: https://app.deriv.com
2. Log in with your real account
3. Go to: Settings → API tokens
4. Create new token and name it "TradingBot-Real"
5. Select these scopes:
   ✓ read (read account/market data)
   ✓ trade (place/manage trades)
   ✓ admin (optional, for account management)
6. Copy the token (you'll need it below)
    """)
    
    api_token = input("\nEnter your REAL account API token: ").strip()
    
    if not api_token or len(api_token) < 20:
        print("\n❌ Invalid token. Setup cancelled.")
        return False
    
    # Confirm token
    confirm = input(f"\nToken: {api_token[:10]}...{api_token[-5:]}\nIs this correct? (yes/no): ").strip().lower()
    
    if confirm != "yes":
        print("\nSetup cancelled.")
        return False
    
    # Set environment variable
    print("\n" + "─"*70)
    print("STEP 2: Save API Token to Environment")
    print("─"*70)
    
    print(f"\nYou can set the environment variable in multiple ways:\n")
    
    print("Option A: Permanently set in PowerShell")
    print("────────────────────────────────────────")
    print(f"""
Run this command in PowerShell (as Administrator):
$env:DERIV_API_TOKEN = "{api_token}"
[Environment]::SetEnvironmentVariable("DERIV_API_TOKEN", "{api_token}", "User")
    """)
    
    print("\nOption B: Set per session in PowerShell")
    print("─────────────────────────────────────────")
    print(f"""
$env:DERIV_API_TOKEN = "{api_token}"
    """)
    
    print("\nOption C: Use configuration file")
    print("──────────────────────────────────")
    print(f"""
Edit: src/trading_bot/config/settings.py
And add:
DERIV_API_TOKEN = '{api_token}'
DERIV_ACCOUNT_TYPE = 'real'
    """)
    
    # Configure account type
    print("\n" + "─"*70)
    print("STEP 3: Configure Account Type")
    print("─"*70)
    
    trade_amount = input("\nEnter initial trade amount in USD (default: 10): ").strip()
    if not trade_amount:
        trade_amount = "10"
    
    print(f"\nTrade Configuration:")
    print(f"  - Account Type: REAL")
    print(f"  - Initial Trade Amount: ${trade_amount}")
    print(f"  - API Token: {api_token[:10]}...{api_token[-5:]}")
    
    # Generate start script
    print("\n" + "─"*70)
    print("STEP 4: Start Trading Bot for Real Account")
    print("─"*70)
    
    print("""
You can now run the bot with:

Option A: With environment variable set
$ set DERIV_API_TOKEN=your_token_here
$ python examples/deriv_quickstart.py

Option B: Using configuration file
$ python -c "
from trading_bot.platforms.deriv_platform import DerivPlatform
from trading_bot.strategies.ma_strategy import MovingAverageStrategy

deriv = DerivPlatform(api_token='your_token', account_type='real')
if deriv.connect():
    print(f'Connected! Balance: {deriv.get_balance()}')
"
    """)
    
    # Final warning
    print("\n" + "="*70)
    print("FINAL CHECKLIST BEFORE STARTING:")
    print("="*70)
    print("""
☐ Tested strategy thoroughly on demo account
☐ Reviewed all trading signals and indicators
☐ Understand the risks involved
☐ Set appropriate stop-loss levels
☐ Have sufficient funds in account
☐ Monitor bot regularly in first few trades
☐ Can afford to lose the trade amount
☐ Backed up API token in safe place
    """)
    
    final_confirm = input("\nI have completed the checklist and want to proceed (yes/no): ").strip().lower()
    
    if final_confirm == "yes":
        # Save to environment
        os.environ["DERIV_API_TOKEN"] = api_token
        print("\n✓ API token configured in environment")
        print("✓ Ready for real account trading")
        print("\nIMPORTANT: Monitor your trades carefully!")
        return True
    else:
        print("\nSetup cancelled. You can run this script again later.")
        return False

def create_real_account_script(api_token: str, trade_amount: str):
    """Create a startup script for real account"""
    
    script_content = f"""#!/usr/bin/env python3
\"\"\"
Deriv Real Account Trading Bot
LIVE TRADING - REAL MONEY

WARNINGS:
- This uses REAL money from your Deriv account
- Monitor trades closely
- Stop immediately if something seems wrong
- Start with small amounts
\"\"\"

import sys
import os
import logging
from datetime import datetime

# Setup path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from trading_bot.platforms.deriv_platform import DerivPlatform
from trading_bot.strategies.ma_strategy import MovingAverageStrategy
from trading_bot.data.data_fetcher import DataFetcher
from trading_bot.utils.logger import setup_logging

# Configure logging
setup_logging()
logger = logging.getLogger('trading_bot')

def main():
    print("\\n" + "="*70)
    print("DERIV REAL ACCOUNT TRADING BOT")
    print("="*70)
    print(f"Started: {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}")
    print(f"Trade Amount: ${trade_amount}")
    print("="*70 + "\\n")
    
    # Verify API token
    api_token = os.getenv("DERIV_API_TOKEN", "{api_token}")
    if not api_token:
        print("[ERROR] DERIV_API_TOKEN not set!")
        return
    
    try:
        # Connect to REAL account
        print("[1] Connecting to Deriv REAL account...")
        deriv = DerivPlatform(api_token=api_token, account_type="real")
        
        if not deriv.connect():
            print("[ERROR] Failed to connect to real account")
            return
        
        # Show account status
        balance = deriv.get_balance()
        print(f"[OK] Connected to real account")
        print(f"     Balance: ${balance['portfolio_value']:.2f}")
        print(f"     Cash: ${balance['cash']:.2f}")
        
        # Initialize strategy
        print("\\n[2] Initializing trading strategy...")
        strategy = MovingAverageStrategy(short_window=5, long_window=20)
        
        # Note: Actual trading would happen here with real orders
        print("[WARNING] Real trading mode - orders would be placed for real!")
        print("[STATUS] Bot ready - start trading with caution")
        
    except Exception as e:
        logger.error(f"Error: {{str(e)}}", exc_info=True)
        print(f"[ERROR] {{str(e)}}")

if __name__ == "__main__":
    main()
"""
    
    filepath = "run_real_account.py"
    with open(filepath, 'w') as f:
        f.write(script_content)
    
    print(f"\n✓ Created: {filepath}")
    return filepath

if __name__ == "__main__":
    if setup_real_account():
        api_token = os.getenv("DERIV_API_TOKEN", "")
        if api_token:
            create_real_account_script(api_token, "10")
