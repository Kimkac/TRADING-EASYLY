# Trading Bot

A comprehensive, production-ready trading bot for forex and stocks that can integrate with any trading platform.

## Features

### Trading Strategies
- **Moving Average (MA)** - Crossover signals based on short and long term moving averages
- **RSI (Relative Strength Index)** - Overbought/oversold signals
- **MACD (Moving Average Convergence Divergence)** - Trend-following signals
- **Bollinger Bands** - Mean reversion signals based on price bands

### Platform Support
- **Alpaca** - Full trading platform adapter with paper trading support
- **Generic REST API** - Extensible adapter for any REST-based trading platform
- Custom platform integration via base class inheritance

### Market Data
- **Yahoo Finance Integration** - Real-time and historical price data
- Historical backtesting with up to 100+ days of data
- Real-time price fetching

### Backtesting Engine
- Full trade simulation with commission handling
- Performance metrics:
  - Total return percentage
  - Win rate
  - Sharpe ratio
  - Maximum drawdown
  - Equity curve tracking

### Logging & Error Handling
- Comprehensive logging to both console and rotating file logs
- Structured error handling throughout
- Debug-level logging for detailed troubleshooting

## Project Structure

```
src/trading_bot/
├── __init__.py
├── main.py                 # Entry point
├── config/
│   └── settings.py        # Configuration and API keys
├── platforms/
│   ├── base_platform.py   # Abstract base class
│   ├── alpaca_platform.py # Alpaca broker integration
│   └── rest_api_platform.py # Generic REST API adapter
├── strategies/
│   ├── ma_strategy.py     # Moving Average strategy
│   └── advanced_strategies.py # RSI, MACD, Bollinger Bands
├── data/
│   └── data_fetcher.py    # Market data integration (yfinance)
├── backtest/
│   └── backtester.py      # Backtesting engine
└── utils/
    └── logger.py          # Logging configuration
```

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   # or
   pip install -e .
   ```

## Configuration

Edit `src/trading_bot/config/settings.py`:
- Add your API credentials
- Configure trading parameters (symbol, quantity, strategy windows)

```python
API_KEY = 'your_alpaca_api_key'
API_SECRET = 'your_alpaca_api_secret'
SYMBOL = 'AAPL'  # or any stock/forex symbol
```

## Usage

### Run the Trading Bot

```bash
python -m trading_bot.main
```

### Example Output

The bot will:
1. Fetch real market data
2. Test multiple trading strategies
3. Run backtests on historical data
4. Display current market price
5. Log all activities to `logs/` directory

### Integration Examples

**Using Alpaca Broker:**
```python
from trading_bot.platforms.alpaca_platform import AlpacaPlatform

platform = AlpacaPlatform(api_key='KEY', api_secret='SECRET')
if platform.connect():
    balance = platform.get_balance()
    price = platform.get_price('AAPL')
    order = platform.place_order('AAPL', 100, 'BUY')
```

**Custom REST API:**
```python
from trading_bot.platforms.rest_api_platform import RestApiPlatform

platform = RestApiPlatform(base_url='https://api.example.com', api_key='KEY')
```

**Custom Strategy:**
```python
from trading_bot.strategies.ma_strategy import MovingAverageStrategy

strategy = MovingAverageStrategy(short_window=5, long_window=20)
signal = strategy.generate_signal(prices)  # Returns 'BUY', 'SELL', or 'HOLD'
```

**Backtesting:**
```python
from trading_bot.backtest.backtester import Backtester
from trading_bot.data.data_fetcher import DataFetcher

prices = DataFetcher.get_historical_prices('AAPL', days=100)
backtester = Backtester(initial_balance=10000)
results = backtester.run(prices, strategy_func)
```

## Dependencies

- **requests** - HTTP library for API calls
- **pandas** - Data manipulation and analysis
- **numpy** - Numerical computations
- **yfinance** - Yahoo Finance data access

## Future Enhancements

- Multi-asset portfolio management
- Advanced risk management (position sizing, stop-losses)
- Live trading execution
- Performance analytics dashboard
- Machine learning strategy optimization
- Options trading support

## License

MIT License - feel free to use and modify

## Support

For issues and feature requests, please check the project documentation or create an issue in the repository.