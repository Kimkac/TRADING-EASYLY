# Deriv Platform Integration

This document explains how to use the Trading Bot with [Deriv.com](https://deriv.com), a popular online trading platform.

## What is Deriv?

Deriv is an online trading platform that offers:
- **Forex** - Major and minor currency pairs
- **Synthetic Indices** - Volatility indices for 24/7 trading
- **Stocks & Commodities** - Real assets during market hours
- **Cryptocurrencies** - BTC, ETH, and other digital assets
- **Multipliers & Options** - Advanced trading products

## Setup Instructions

### 1. Create a Deriv Account

1. Go to [https://deriv.com](https://deriv.com)
2. Click "Sign up" and create an account
3. Verify your email
4. You automatically get a **demo account** with virtual funds to practice

### 2. Get Your API Token

1. Log in to [https://app.deriv.com](https://app.deriv.com)
2. Go to **Settings** → **API tokens**
3. Click "Create new token"
4. Name it "Trading Bot"
5. Select appropriate scopes:
   - ✅ `read` - Read-only access to account/market data
   - ✅ `trade` - Place and manage trades
   - ✅ `admin` - Full account management (optional)
6. Copy the token and save it safely

### 3. Configure the Trading Bot

**Option A: Environment Variable (Recommended)**
```bash
# Windows PowerShell
$env:DERIV_API_TOKEN = "your_api_token_here"

# Windows CMD
set DERIV_API_TOKEN=your_api_token_here

# Linux/macOS
export DERIV_API_TOKEN="your_api_token_here"
```

**Option B: Update Configuration File**
Edit `src/trading_bot/config/settings.py`:
```python
DERIV_API_TOKEN = 'your_api_token_here'
DERIV_ACCOUNT_TYPE = 'demo'  # 'demo' or 'real'
```

## Usage

### Basic Connection Test

```python
from trading_bot.platforms.deriv_platform import DerivPlatform

# Initialize with demo account
deriv = DerivPlatform(
    api_token="your_api_token",
    account_type="demo"
)

# Connect and check balance
if deriv.connect():
    balance = deriv.get_balance()
    print(f"Balance: ${balance['portfolio_value']}")
```

### Running the Test Script

```bash
# Set API token first
$env:DERIV_API_TOKEN = "your_token"

# Run the test
python test_deriv.py
```

This will:
1. Test connection to Deriv
2. Display account balance
3. Fetch current prices
4. Place a demo order
5. Show open positions

### Trading with Strategies

```python
from trading_bot.platforms.deriv_platform import DerivPlatform
from trading_bot.strategies.ma_strategy import MovingAverageStrategy
from trading_bot.data.data_fetcher import DataFetcher

# Setup
deriv = DerivPlatform(api_token="your_token", account_type="demo")
deriv.connect()

strategy = MovingAverageStrategy(short_window=5, long_window=20)
fetcher = DataFetcher()

# Get market data
data = fetcher.fetch_data("EUR_USD", days=30)

# Generate signals
data = strategy.generate_signal(data)

# Check signal
signal = data['signal'].iloc[-1]
if signal == 1:  # Buy signal
    order = deriv.place_order("EUR_USD", quantity=10, side="buy")
elif signal == -1:  # Sell signal
    order = deriv.place_order("EUR_USD", quantity=10, side="sell")
```

## Supported Symbols

### Currency Pairs
- EUR_USD, GBP_USD, USD_JPY
- EUR_GBP, EUR_JPY, GBP_JPY
- AUD_USD, NZD_USD, USD_CAD
- And many more...

### Indices
- `R_50` - Volatility Index
- `STPXUSD` - Stock Index

### Cryptocurrencies
- `BTCUSD` - Bitcoin
- `ETHUSD` - Ethereum

### Stocks (During market hours)
- `AAPL`, `GOOGL`, `MSFT`, `AMZN`, etc.

## API Reference

### DerivPlatform Class

```python
class DerivPlatform(TradingPlatform):
    def __init__(self, api_token: str, app_id: str = "1089", account_type: str = "demo")
    def connect(self) -> bool
    def get_balance(self) -> Dict[str, Any]
    def get_price(self, symbol: str) -> float
    def place_order(self, symbol: str, quantity: int, side: str) -> Optional[Dict[str, Any]]
    def get_positions(self) -> list
    def close_position(self, position_id: str) -> bool
    def get_account_status(self) -> Dict[str, Any]
```

### Methods

#### connect()
Establishes connection to Deriv API
```python
if deriv.connect():
    print("Connected!")
```

#### get_balance()
Returns account balance information
```python
balance = deriv.get_balance()
print(f"Portfolio Value: ${balance['portfolio_value']}")
print(f"Cash: ${balance['cash']}")
```

#### get_price(symbol)
Fetches current price for a symbol
```python
price = deriv.get_price("EUR_USD")
print(f"EUR/USD: {price}")
```

#### place_order(symbol, quantity, side)
Places a market order
```python
order = deriv.place_order(
    symbol="EUR_USD",
    quantity=10,        # Amount in currency
    side="buy"          # "buy" or "sell"
)
print(f"Order ID: {order['order_id']}")
```

#### get_positions()
Retrieves all open positions
```python
positions = deriv.get_positions()
for pos in positions:
    print(f"Position: {pos}")
```

#### close_position(position_id)
Closes an open position
```python
success = deriv.close_position("contract_id_123")
```

#### get_account_status()
Gets detailed account information
```python
status = deriv.get_account_status()
print(f"Status: {status}")
```

## Advanced: Market Data Integration

The bot automatically fetches data from Yahoo Finance. For real-time Deriv prices:

```python
from trading_bot.data.data_fetcher import DataFetcher

fetcher = DataFetcher()

# Fetch historical data (uses Yahoo Finance)
data = fetcher.fetch_data("EURUSD", days=30)

# Use with strategy
from trading_bot.strategies.advanced_strategies import RSIStrategy
strategy = RSIStrategy(period=14, overbought=70, oversold=30)
data = strategy.generate_signal(data)
```

## Demo vs. Real Account

### Demo Account
- **Virtual funds** for practice trading
- **No real money risk**
- Perfect for testing strategies
- Market data may be delayed

### Real Account
⚠️ **WARNING**: Real trading with real money!

1. Deposit funds to your Deriv account
2. Change `account_type` to `"real"`:
   ```python
   deriv = DerivPlatform(
       api_token="your_token",
       account_type="real"
   )
   ```
3. Start with small position sizes
4. **Always test thoroughly on demo first!**

## Troubleshooting

### Connection Failed
```
Error: Failed to connect to Deriv
```
- Check your API token is correct
- Verify internet connection
- Check token hasn't expired

### Invalid Symbol
```
Error: Could not get price for SYMBOL
```
- Check symbol is in correct format (e.g., `EUR_USD` not `EURUSD`)
- See [Supported Symbols](#supported-symbols) section

### Insufficient Funds
```
Error: Failed to place order
```
- Check account balance with `get_balance()`
- Demo account has limited virtual funds
- Reduce order quantity

### Rate Limiting
If making many requests:
- Add delays between requests
- Use WebSocket for real-time data (advanced)
- Contact Deriv support for higher limits

## Examples

### Example 1: Simple Price Ticker
```python
from trading_bot.platforms.deriv_platform import DerivPlatform

deriv = DerivPlatform(api_token="token", account_type="demo")
deriv.connect()

symbols = ["EUR_USD", "GBP_USD", "USD_JPY"]
for symbol in symbols:
    price = deriv.get_price(symbol)
    print(f"{symbol}: {price}")
```

### Example 2: Automated Trading
```python
from trading_bot.platforms.deriv_platform import DerivPlatform
from trading_bot.strategies.ma_strategy import MovingAverageStrategy
from trading_bot.data.data_fetcher import DataFetcher

deriv = DerivPlatform(api_token="token", account_type="demo")
deriv.connect()

strategy = MovingAverageStrategy()
fetcher = DataFetcher()

while True:
    data = fetcher.fetch_data("EUR_USD", days=30)
    data = strategy.generate_signal(data)
    
    signal = data['signal'].iloc[-1]
    if signal == 1:
        deriv.place_order("EUR_USD", 10, "buy")
    elif signal == -1:
        deriv.place_order("EUR_USD", 10, "sell")
    
    time.sleep(60)  # Wait 1 minute
```

### Example 3: Portfolio Monitoring
```python
from trading_bot.platforms.deriv_platform import DerivPlatform

deriv = DerivPlatform(api_token="token", account_type="demo")
deriv.connect()

balance = deriv.get_balance()
positions = deriv.get_positions()

print(f"Portfolio Value: ${balance['portfolio_value']}")
print(f"Open Positions: {len(positions)}")

for pos in positions:
    print(f"  {pos}")
```

## Security Best Practices

1. **Never commit API tokens** to version control
2. **Use environment variables** for credentials
3. **Start with demo account** before real money
4. **Limit token permissions** in Deriv settings
5. **Rotate tokens regularly** for security
6. **Don't share tokens** with others
7. **Monitor account activity** regularly

## Additional Resources

- [Deriv Official API Documentation](https://api.deriv.com/)
- [Deriv Support](https://deriv.com/help-centre/)
- [Trading Bot Documentation](README.md)
- [Strategy Examples](src/trading_bot/strategies/)

## Support

For issues with:
- **Trading Bot**: Check [README.md](README.md) and [CONTRIBUTING.md](CONTRIBUTING.md)
- **Deriv Platform**: Visit [https://deriv.com/help-centre/](https://deriv.com/help-centre/)
- **API Documentation**: See [https://api.deriv.com/](https://api.deriv.com/)

---

**Happy Trading!** Remember: Always start with a demo account and test strategies thoroughly before using real money.
