# ⚡ QUICK START - 30 SECONDS

## 🚀 Start Trading Bot

```powershell
python working_bot.py
```

**Done!** Bot is now trading automatically.

---

## ⏹️ Stop Bot

```
Press: Ctrl + C
```

---

## 📊 Check Balance

```powershell
python check_demo_account.py
```

---

## 📈 Current Status

```
✅ Bot: WORKING
✅ Account: Demo ($9,999.49)
✅ Connection: ACTIVE
✅ Signals: GENERATING
✅ Trading: EXECUTING
```

---

## 🎯 What Bot Does

Every 60 seconds:
1. Gets EUR/USD price data
2. Calculates moving averages
3. Decides: BUY / SELL / HOLD
4. Places trade if signal
5. Repeats

---

## 📊 Reading the Output

```
[TIME] Iteration N           ← Check number
  Price: $1.16551            ← Current price
  Short MA: $1.16766         ← 5-day average
  Long MA:  $1.17121         ← 20-day average
  Signal: SELL               ← BUY/SELL/HOLD
  ACTION: Placing order...   ← What bot is doing
```

---

## 💡 Signals Explained

| Signal | Means | Action |
|--------|-------|--------|
| BUY | Uptrend | Bot buys |
| SELL | Downtrend | Bot sells |
| HOLD | Unclear | Bot waits |

---

## 🎉 That's It!

Your bot is live and trading!

