# INSTALL.md

## Installation Guide

### Prerequisites

- Python 3.9 or higher
- Git
- Virtual environment (recommended)
- API key for your trading platform (Alpaca, etc.)

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/trading-bot.git
cd trading-bot
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Or install in editable mode for development:
```bash
pip install -e .
```

### Step 4: Configure Settings

Edit `src/trading_bot/config/settings.py`:

```python
# API Keys
API_KEY = 'your_alpaca_api_key_here'
API_SECRET = 'your_alpaca_secret_here'

# Trading Parameters
SYMBOL = 'AAPL'  # Stock symbol to trade
QUANTITY = 100   # Number of shares per trade

# Strategy Parameters
SHORT_WINDOW = 5   # Short-term moving average window
LONG_WINDOW = 20   # Long-term moving average window
```

### Step 5: Verify Installation

Test that everything is installed correctly:

```bash
# Test import
python -c "from trading_bot.config.settings import SYMBOL; print('✓ Installation OK')"

# Test all modules
python -m trading_bot.main --test
```

### Step 6: Run the Bot

```bash
python -m trading_bot.main
```

You should see output like:
```
2026-05-13 12:15:21 - trading_bot - INFO - Logging configured successfully
2026-05-13 12:15:21 - trading_bot - INFO - Trading Bot Started
2026-05-13 12:15:21 - trading_bot - INFO - Fetching market data for AAPL...
...
```

## Platform-Specific Installation

### Alpaca Broker Setup

1. Create account at https://alpaca.markets
2. Get API key and secret
3. Test with paper trading (default)
4. Add credentials to `config/settings.py`

### Using Different Brokers

Create a custom adapter:

```python
from trading_bot.platforms.base_platform import TradingPlatform

class YourBrokerPlatform(TradingPlatform):
    def connect(self):
        # Your connection logic
        pass
    
    def get_balance(self):
        # Your balance logic
        pass
    
    def get_price(self, symbol):
        # Your price logic
        pass
    
    def place_order(self, symbol, quantity, side):
        # Your order logic
        pass
```

## Docker Installation

### Build and Run with Docker

```bash
# Build image
docker build -t trading-bot:latest .

# Run container
docker run -e API_KEY="your_key" -e API_SECRET="your_secret" trading-bot
```

### Using Docker Compose

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials
# Run services
docker-compose up -d
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'trading_bot'"

**Solution:** Make sure you're in the project root and virtual environment is activated:
```bash
cd trading-bot
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux
```

### "API connection failed"

**Solution:** Check your API credentials:
```bash
python -c "from trading_bot.platforms.alpaca_platform import AlpacaPlatform; p = AlpacaPlatform('key', 'secret'); print(p.connect())"
```

### "No data retrieved for AAPL"

**Solution:** Verify internet connection and yfinance access:
```bash
python -c "import yfinance as yf; print(yf.download('AAPL', period='1d'))"
```

### Permission denied on scripts

**Solution:** Try with Python explicitly:
```bash
python -m trading_bot.main
```

## Next Steps

1. **Customize strategies** - Edit files in `src/trading_bot/strategies/`
2. **Test with backtest** - Use historical data to validate strategies
3. **Paper trade first** - Use Alpaca's paper trading before live trading
4. **Monitor logs** - Check `logs/` directory for detailed execution logs

## Updating

To update to the latest version:

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

## Uninstall

```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf .venv  # Mac/Linux
rmdir /s /q .venv  # Windows
```

## Getting Help

- Check README.md for feature overview
- See DEPLOYMENT.md for production setup
- Review logs in `logs/` directory
- Open an issue on GitHub for bugs
