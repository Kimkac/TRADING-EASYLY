# Start Trading with Demo Account - Quick Start

## ✅ Your Demo Account Status

```
Account Type: Demo (Virtual Money)
Balance: $9,999.49
Connection: Active (WebSocket)
API Token: KyalQ6MUAnoB5Fb (Already configured)
Status: Ready to Trade
```

---

## 🚀 Quick Start in 3 Steps

### Step 1: Set Your API Token

```powershell
# Windows PowerShell (one command)
$env:DERIV_API_TOKEN = "KyalQ6MUAnoB5Fb"
```

That's it! The token is now set for this terminal session.

### Step 2: Start the Trading Bot

```powershell
# Run the trading bot with Moving Average strategy
python examples/deriv_quickstart.py
```

### Step 3: Watch the Bot Trade!

The bot will:
- ✓ Connect to your demo account
- ✓ Fetch market data (EUR/USD)
- ✓ Generate trading signals (Buy/Sell/Hold)
- ✓ Place demo trades automatically
- ✓ Show real-time updates every minute

---

## 📊 What You'll See

```
======================================================================
DERIV TRADING BOT - QUICK START
======================================================================

[*] Connecting to Deriv...
[OK] Connected to Deriv

📊 Account Status:
   Portfolio Value: $9999.49
   Cash: $9999.49

🤖 Starting trading bot for EUR_USD
   Strategy: Moving Average (5/20)
   Position Size: 10
   Account Type: Demo

----------------------------------------------------------------------

[2026-05-19 15:55:30] Iteration 1
  📥 Fetching 30 days of data for EUR_USD...
  ✓ Data loaded: 252 candles
  💡 Generating trading signals...
  📈 Latest price: 1.09543
  📊 Short MA: 1.09450 | Long MA: 1.09520
  🎯 Signal: BUY (short MA > long MA)
  📍 Placing order: BUY 10 EUR_USD
  ✓ Order placed: transaction_id=12345
```

---

## 🎮 Trading Parameters

The bot uses these default settings:

| Setting | Value | Meaning |
|---------|-------|---------|
| Symbol | EUR_USD | Currency pair to trade |
| Quantity | 10 | Trade size (virtual USD) |
| Short MA | 5 | Fast moving average |
| Long MA | 20 | Slow moving average |
| Lookback | 30 days | Historical data for analysis |
| Account | Demo | Virtual money (safe to test) |

---

## 🔧 Customize the Bot

### Option 1: Edit the Script

Edit `examples/deriv_quickstart.py` to change settings:

```python
SYMBOL = "EUR_USD"        # Change to GBP_USD, USD_JPY, etc.
QUANTITY = 10             # Change trade size
SHORT_WINDOW = 5          # Change fast MA
LONG_WINDOW = 20          # Change slow MA
LOOKBACK_DAYS = 30        # Change how much historical data
```

### Option 2: Create Custom Script

Create a file `my_trading_bot.py`:

```python
import os
import sys
sys.path.insert(0, 'src')

from trading_bot.platforms.deriv_platform import DerivPlatform
from trading_bot.strategies.ma_strategy import MovingAverageStrategy
from trading_bot.data.data_fetcher import DataFetcher

# Your settings
API_TOKEN = os.getenv("DERIV_API_TOKEN")
SYMBOL = "GBP_USD"  # Your choice
QUANTITY = 5        # Smaller size
SHORT_MA = 5
LONG_MA = 20

# Connect
deriv = DerivPlatform(api_token=API_TOKEN, account_type="demo")
if deriv.connect():
    print("Connected!")
    balance = deriv.get_balance()
    print(f"Balance: ${balance['portfolio_value']:.2f}")
```

---

## 📈 Available Strategies

### 1. Moving Average (Simple) ⭐ START HERE

```python
from trading_bot.strategies.ma_strategy import MovingAverageStrategy

strategy = MovingAverageStrategy(short_window=5, long_window=20)
signals = strategy.generate_signal(data)
```

**How it works:**
- Fast MA (5-day) vs Slow MA (20-day)
- BUY when fast > slow
- SELL when fast < slow
- Simple and reliable

### 2. Advanced Strategies (When Ready)

```python
from trading_bot.strategies.advanced_strategies import RSIStrategy, MACDStrategy

# RSI Strategy
rsi = RSIStrategy(period=14, overbought=70, oversold=30)

# MACD Strategy
macd = MACDStrategy(fast=12, slow=26, signal=9)
```

---

## 🛑 How to Stop the Bot

**Press: `Ctrl + C`**

The bot will gracefully shut down and show:
```
[OK] Bot stopped
Final Balance: $9999.49
Total trades: 5
```

---

## 📊 Monitor Your Trades

While bot is running, open another terminal to check status:

```powershell
# Check account balance anytime
$env:DERIV_API_TOKEN = "KyalQ6MUAnoB5Fb"
python verify_deriv.py
```

---

## ✅ Available Symbols to Trade

The bot can trade any of these:

**Forex:**
- EUR_USD, GBP_USD, USD_JPY, AUD_USD, NZD_USD

**Indices:**
- R_50 (Volatility Index 50)
- US_500 (S&P 500)

**Cryptocurrencies:**
- BTC, ETH

**Stocks:**
- AAPL, GOOGL, MSFT, AMZN

---

## 🔍 Understanding Trading Signals

### BUY Signal
```
Short MA (5-day) crosses ABOVE Long MA (20-day)
Interpretation: Price momentum turning upward
Action: Open BUY position
```

### SELL Signal
```
Short MA (5-day) crosses BELOW Long MA (20-day)
Interpretation: Price momentum turning downward
Action: Open SELL position
```

### HOLD Signal
```
Both MAs moving together or uncertain
Interpretation: No clear trend
Action: Stay in current position or wait
```

---

## 📝 Common Issues & Fixes

### "DERIV_API_TOKEN not set"

```powershell
# Make sure you run this first
$env:DERIV_API_TOKEN = "KyalQ6MUAnoB5Fb"

# Then run the bot
python examples/deriv_quickstart.py
```

### "Failed to connect"

```powershell
# Verify connection works
python verify_deriv.py

# If that fails, check internet connection
ping 8.8.8.8
```

### "No data available"

The market data fetcher might be having issues. The bot will retry automatically.

### "Order placement failed"

Usually means:
- Insufficient balance
- Market is closed
- Invalid symbol

The bot will keep trying each minute.

---

## 📊 What the Bot Does Each Minute

```
1. Fetch last 30 days of market data
   └─ Gets price, volume, open, close, etc.

2. Calculate Moving Averages
   └─ 5-day average (fast)
   └─ 20-day average (slow)

3. Generate Trading Signal
   └─ Compare fast MA vs slow MA
   └─ Decide: BUY, SELL, or HOLD

4. Place Order (if signal)
   └─ BUY: Open long position
   └─ SELL: Open short position
   └─ HOLD: Wait for next signal

5. Show Results
   └─ Display current price
   └─ Show indicator values
   └─ Print trade confirmation

6. Wait 60 seconds
   └─ Repeat from step 1
```

---

## 🎯 Next Steps

1. **Run the bot:**
   ```powershell
   $env:DERIV_API_TOKEN = "KyalQ6MUAnoB5Fb"
   python examples/deriv_quickstart.py
   ```

2. **Let it trade for a few hours/days**
   - Watch the trades
   - Monitor balance changes
   - See signals in action

3. **Customize settings** (if desired)
   - Change symbols
   - Adjust MA windows
   - Modify trade size

4. **Review performance**
   - How many winning trades?
   - How many losing trades?
   - Overall profit/loss?

5. **When satisfied**, you can:
   - Switch to real account
   - Adjust parameters
   - Add more strategies
   - Implement risk management

---

## ⚠️ Demo Account Notes

✓ **Advantages:**
- No real money risk
- Test strategies freely
- Practice without penalty
- Learn how bot works
- Unlimited trades

⚠️ **Limitations:**
- Real market conditions may differ
- Slippage/liquidity may be unrealistic
- Not real money (psychology different)
- Demo balance resets if unused

---

## 🚀 Ready to Start?

```powershell
# Set token
$env:DERIV_API_TOKEN = "KyalQ6MUAnoB5Fb"

# Run bot
python examples/deriv_quickstart.py

# Watch it trade! 🎉
```

Press `Ctrl + C` anytime to stop.

---

## Need Help?

See these files for more info:
- `DERIV_README.md` - Overview
- `DERIV_SETUP.md` - Detailed setup
- `DEMO_VS_REAL.md` - Demo vs Real account
- `REAL_ACCOUNT_GUIDE.md` - When ready for real money
