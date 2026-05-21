# Real Account Trading Guide

## ⚠️ IMPORTANT DISCLAIMER

**REAL MONEY TRADING** - This configuration uses actual funds from your Deriv account. 
Proceed with caution and start with small amounts.

### Risk Warning
- You can lose money with automated trading
- Test thoroughly on demo account first
- Never risk more than you can afford to lose
- Start with amounts like $5-$10 per trade
- Monitor the bot closely in the beginning

---

## Step 1: Get Real Account API Token

### For Real Account Trading:

1. Go to **https://app.deriv.com** (Make sure you're logged into your REAL account, not demo)
2. Click **Settings** → **API tokens**
3. Click **Create new token**
4. Name it: `TradingBot-Real`
5. Select these scopes:
   - ✅ `read` - Read account and market data
   - ✅ `trade` - Place and manage orders
   - ✅ `admin` - (optional) Full account management
6. Click **Create**
7. **Copy the token** (you'll use it below)

⚠️ **Security Note**: Never share your API token with anyone!

---

## Step 2: Verify Real Account Connection

Test the connection without trading:

```bash
# Set your API token
set DERIV_API_TOKEN=your_real_token_here

# Run verification (read-only, no trades)
python verify_real_account.py
```

You should see:
```
[OK] REAL ACCOUNT CONNECTED
Portfolio Value: $5000.00
Available Cash: $5000.00
```

---

## Step 3: Configure for Real Trading

### Option A: Environment Variable (Recommended)

**Windows PowerShell:**
```powershell
# Set for current session
$env:DERIV_API_TOKEN = "your_real_token_here"

# Set permanently (requires Administrator)
[Environment]::SetEnvironmentVariable("DERIV_API_TOKEN", "your_real_token_here", "User")
```

**Windows Command Prompt:**
```cmd
set DERIV_API_TOKEN=your_real_token_here
```

### Option B: Configuration File

Edit `src/trading_bot/config/settings.py`:
```python
DERIV_API_TOKEN = 'your_real_token_here'
DERIV_ACCOUNT_TYPE = 'real'
TRADE_AMOUNT = 10  # Start with $10 per trade
```

### Option C: Direct in Code

```python
from trading_bot.platforms.deriv_platform import DerivPlatform

deriv = DerivPlatform(
    api_token='your_real_token_here',
    account_type='real'
)
```

---

## Step 4: Important Configuration Settings

Create or update your configuration with these settings:

```python
# Trading Parameters for Real Account
TRADE_AMOUNT = 10  # Start with $10 per trade
MAX_DAILY_LOSS = 100  # Stop if you lose $100 per day
MAX_TRADES_PER_DAY = 5  # Limit trades per day
ACCOUNT_TYPE = 'real'

# Risk Management
STOP_LOSS_PERCENT = 2  # Stop loss at 2%
TAKE_PROFIT_PERCENT = 3  # Take profit at 3%

# Strategy Settings
STRATEGY = 'moving_average'
SHORT_MA = 5
LONG_MA = 20
```

---

## Step 5: Test Thoroughly First

### 1. Start on DEMO Account

```bash
# Set to demo account
set DERIV_API_TOKEN=your_demo_token_here
python test_deriv.py
```

### 2. Verify Your Strategy

Run trading signals for 1-2 weeks on demo to ensure:
- ✓ Strategy generates correct signals
- ✓ Indicators are working properly
- ✓ Risk management is appropriate
- ✓ Bot runs without errors

### 3. Start Small on Real Account

Only after thorough testing:

```bash
# Set to real account (VERY SMALL amount)
set DERIV_API_TOKEN=your_real_token_here
python run_trading_bot.py  # Will use $5-10 per trade
```

---

## Running the Bot on Real Account

### Option 1: Quick Setup Script

```bash
python setup_real_account.py
```

This interactive script will:
- Verify you understand the risks
- Confirm your real account API token
- Set up the environment
- Create a startup script

### Option 2: Manual Startup

```bash
# Set API token
set DERIV_API_TOKEN=your_real_token_here

# Run the bot
python examples/deriv_quickstart.py
```

### Option 3: With Configuration File

```python
# In your script
from trading_bot.platforms.deriv_platform import DerivPlatform
from trading_bot.strategies.ma_strategy import MovingAverageStrategy

deriv = DerivPlatform(api_token="your_token", account_type="real")

if deriv.connect():
    balance = deriv.get_balance()
    print(f"Real Account Balance: ${balance['portfolio_value']:.2f}")
    
    # Start trading...
    strategy = MovingAverageStrategy()
```

---

## Monitoring Your Real Account

### Check Account Status Anytime

```bash
python verify_real_account.py
```

### View Open Positions

```python
positions = deriv.get_positions()
for pos in positions:
    print(f"Position: {pos}")
```

### Check Balance

```python
balance = deriv.get_balance()
print(f"Balance: ${balance['portfolio_value']:.2f}")
```

---

## Safety Checklist

Before starting real account trading:

- [ ] Tested strategy for 1+ week on demo account
- [ ] Verified all trading signals are correct
- [ ] Understand stop-loss and risk management
- [ ] Have adequate funds ($500+ recommended)
- [ ] Can afford to lose the trade amount
- [ ] Have monitored first few trades manually
- [ ] Bot can run without interruption
- [ ] API token is secure and backed up
- [ ] Know how to emergency stop the bot
- [ ] Have reviewed all logs and settings

---

## Emergency Stop

If something goes wrong, you can:

1. **Stop the bot immediately** - Press Ctrl+C in terminal
2. **Manually close positions** - Go to app.deriv.com → Trade
3. **Revoke API token** - Go to Settings → API tokens → Delete token

---

## Troubleshooting

### Connection Failed on Real Account

```
[ERROR] Failed to connect to real account
```

**Solutions:**
1. Check API token is for REAL account, not demo
2. Verify token has `read` and `trade` scopes
3. Ensure token hasn't expired
4. Check internet connection

### Insufficient Funds Error

```
[ERROR] Insufficient balance for trade
```

**Solutions:**
1. Check current balance: `python verify_real_account.py`
2. Reduce `TRADE_AMOUNT` in settings
3. Close losing positions first
4. Add more funds to account

### Connection Timeout

```
[ERROR] Request timeout
```

**Solutions:**
1. Check your internet connection
2. Verify Deriv API is up: https://app.deriv.com
3. Try again after a few minutes
4. Check firewall/VPN settings

---

## Support Resources

- **Deriv Support:** https://deriv.com/support
- **API Documentation:** https://deriv.api.docs.deriv.com/
- **Trading Platform:** https://app.deriv.com
- **Account Settings:** https://app.deriv.com/account/settings

---

## Quick Reference

| Action | Command |
|--------|---------|
| Verify Real Account | `python verify_real_account.py` |
| Setup Wizard | `python setup_real_account.py` |
| Run Trading Bot | `python run_trading_bot.py` |
| Test Connection | `python test_deriv.py` |
| Check Balance | `python verify_real_account.py` |

---

**Remember:** Start small, monitor closely, and never risk more than you can afford to lose.

