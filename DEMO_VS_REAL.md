# Demo vs Real Account - Quick Comparison

## Key Differences

| Feature | Demo Account | Real Account |
|---------|--------------|--------------|
| Money | Virtual (practice) | Real money |
| Risk | No financial risk | You can lose money |
| API Token | From demo account | From real account |
| Starting Balance | $10,000 (virtual) | Your actual funds |
| Trading | Full features available | Full features available |
| Use Case | Learning & testing | Live trading |
| Recommendation | Start here! | After thorough testing |

---

## Setup Comparison

### Demo Account (Current Setup)

```bash
# 1. Get demo token from https://app.deriv.com (demo account)
# 2. Set environment variable
set DERIV_API_TOKEN=your_demo_token

# 3. Test connection
python verify_deriv.py

# 4. Run trading bot
python test_deriv.py
```

**Account Balance:** $9,999.49 (virtual)

### Real Account (New Setup)

```bash
# 1. Get REAL account token from https://app.deriv.com (real account)
set DERIV_API_TOKEN=your_real_token

# 2. Verify real account connection
python verify_real_account.py

# 3. Run trading bot with REAL money
python examples/deriv_quickstart.py
```

**Account Balance:** Your actual funds (REAL MONEY)

---

## Step-by-Step Migration

### Phase 1: Demo Testing (Current)
- ✅ Bot connected and working
- ✅ Account balance: $9,999.49
- ✅ Ready for strategy testing

### Phase 2: Real Account Preparation

1. **Get Real Account Token**
   ```
   - Log into REAL account: https://app.deriv.com
   - Go to: Settings → API tokens
   - Create new token
   - Copy and save securely
   ```

2. **Verify Real Connection**
   ```bash
   set DERIV_API_TOKEN=your_real_token
   python verify_real_account.py
   ```

3. **Start Small**
   ```bash
   # First trades should be $5-10 amount
   python run_trading_bot.py
   ```

### Phase 3: Scale Up
- Monitor first 50+ trades
- Gradually increase trade amounts
- Add risk management rules
- Scale up only after consistent results

---

## Current Status

✅ **Demo Account Ready**
- Token: `KyalQ6MUAnoB5Fb`
- Connection: WebSocket (working)
- Balance: $9,999.49
- Status: Testing mode

---

## To Switch to Real Account

### Option 1: Interactive Setup (Recommended)

```bash
python setup_real_account.py
```

This guides you through:
- Risk acknowledgment
- Getting real API token
- Configuring environment
- Starting first trade

### Option 2: Manual Configuration

```bash
# 1. Get your REAL account API token
# 2. Set environment variable
set DERIV_API_TOKEN=your_real_token

# 3. Run with real account
python examples/deriv_quickstart.py
```

### Option 3: Configuration File

Edit `src/trading_bot/config/settings.py`:
```python
DERIV_ACCOUNT_TYPE = 'real'  # Changed from 'demo'
DERIV_API_TOKEN = 'your_real_token'
INITIAL_TRADE_AMOUNT = 10  # Start small
```

---

## Important Reminders

⚠️ **Before switching to real account:**
1. Test on demo for at least 1-2 weeks
2. Verify strategy signals are accurate
3. Understand your risk tolerance
4. Have adequate funds available
5. Know how to emergency stop

✓ **After switching:**
1. Monitor trades manually at first
2. Keep API token secure
3. Start with small amounts ($5-10)
4. Gradually increase after 50+ successful trades
5. Review logs and performance regularly

---

## Files Created for Real Account

- `setup_real_account.py` - Interactive setup wizard
- `verify_real_account.py` - Connection verification (read-only)
- `REAL_ACCOUNT_GUIDE.md` - Complete setup guide
- `run_real_account.py` - Startup script (auto-created by wizard)

---

## Next Steps

1. **Continue testing on demo:** `python test_deriv.py`
2. **When ready for real:** `python setup_real_account.py`
3. **Or manually:** Set `DERIV_API_TOKEN` to real token and run bot

---

Questions? See `REAL_ACCOUNT_GUIDE.md` for detailed instructions.
