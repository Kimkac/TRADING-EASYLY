# How to Start Trading - Demo Account (5 Minutes)

## ✅ Current Status

Your demo account is **ready to trade**:
- ✓ Account Connected via WebSocket
- ✓ Balance: $9,999.49 (virtual)
- ✓ API Token: Configured
- ✓ Trading Bot: Ready

---

## 🚀 Start Trading in 2 Commands

### Command 1: Start Bot with Default Settings (EUR/USD)

```powershell
python quick_demo_bot.py
```

**What it does:**
- Connects to your Deriv demo account
- Trades EUR/USD pair
- Uses Moving Average strategy (5/20)
- Checks every 60 seconds
- Places automatic trades

**Output:**
```
======================================================================
🚀 DERIV DEMO TRADING BOT
======================================================================

Account: Demo
Balance: $9,999.49 (virtual money)
Symbol: EURUSD=X
Strategy: Moving Average (5/20)
Trade Size: 10 USD per trade

------

[16:05:30] Iteration 1
  Price: $1.09543
  Short MA (5):  $1.09450
  Long MA (20):  $1.09520
  Signal: BUY
  --> BUY order placed
```

### Command 2: Stop the Bot

Press: **`Ctrl + C`**

The bot will stop and show your final balance.

---

## 📊 Trade Different Symbols

### Change Symbol

```powershell
# GBP/USD
python quick_demo_bot.py GBPUSD=X

# Bitcoin
python quick_demo_bot.py BTC-USD

# Apple stock
python quick_demo_bot.py AAPL

# Google stock
python quick_demo_bot.py GOOGL
```

---

## 📈 What the Bot Does

### Every 60 Seconds:

1. **Fetches Data** - Gets last 30 days of price data
2. **Calculates Moving Averages**:
   - Fast MA (5-day) - Recent trend
   - Slow MA (20-day) - Long-term trend
3. **Generates Signal**:
   - **BUY** - Fast MA crosses above slow MA
   - **SELL** - Fast MA crosses below slow MA
   - **HOLD** - No clear signal
4. **Places Trade** - Automatically places order based on signal
5. **Repeats** - Waits 60 seconds and does it again

---

## 💡 Understanding the Output

```
[16:05:30] Iteration 1
  Price: $1.09543                    ← Current market price
  Short MA (5):  $1.09450            ← 5-day average (fast)
  Long MA (20):  $1.09520            ← 20-day average (slow)
  Signal: BUY                        ← Trading signal
  --> BUY order placed               ← Order confirmation
```

**Signal Meanings:**
- **BUY**: Short MA is above long MA (momentum up)
- **SELL**: Short MA is below long MA (momentum down)
- **HOLD**: Moving averages are close or crossing (uncertain)

---

## 🛑 Stop the Bot Anytime

**Press: `Ctrl + C`**

The bot will:
- Close current connection
- Show final balance
- Exit cleanly

---

## ✅ Check Balance Without Trading

```powershell
python verify_deriv.py
```

Shows current account status without placing trades.

---

## 🔍 Troubleshooting

### Bot says "No data available"

The data source (Yahoo Finance) might not have data for that symbol. Try:
- Different symbol
- Wait a moment and it will retry

### No trades are being placed

This could mean:
- No clear trading signal
- Bot is waiting for signal confirmation
- Market conditions unclear

### Bot won't connect

Run this to verify connection:
```powershell
python verify_deriv.py
```

---

## 📚 Next Steps After Trading

### 1. Let Bot Trade for a While
- Run for 2-4 hours or overnight
- Watch trades happen
- Monitor balance changes

### 2. Review Performance
- How many trades executed?
- How many were profitable?
- How many lost money?
- What's the overall profit/loss?

### 3. Experiment
- Try different symbols
- Change strategy parameters
- Run multiple bots simultaneously

### 4. Switch to Real Account
When confident, use:
```powershell
python setup_real_account.py
```

---

## 🎯 Quick Reference

| Task | Command |
|------|---------|
| Start trading (EUR/USD) | `python quick_demo_bot.py` |
| Trade GBP/USD | `python quick_demo_bot.py GBPUSD=X` |
| Trade Bitcoin | `python quick_demo_bot.py BTC-USD` |
| Check balance | `python verify_deriv.py` |
| Stop bot | Press `Ctrl + C` |

---

## ⚠️ Demo Account Notes

✓ **Safe to experiment**
- Virtual money only
- No real financial risk
- Test strategies freely
- Practice without penalty

⚠️ **Not exactly like real**
- Real market conditions may differ
- Slippage might be different
- Psychological pressure different (not real money)

---

## Ready to Start? 

```powershell
python quick_demo_bot.py
```

Your bot will:
1. Connect to Deriv ✓
2. Check your balance ✓
3. Fetch market data ✓
4. Generate signals ✓
5. Place trades automatically ✓

Watch the magic happen! 🎉

---

## Questions?

See:
- `START_TRADING.md` - Detailed guide
- `DERIV_README.md` - Overview
- `DEMO_VS_REAL.md` - Demo vs Real

