# DEPLOYMENT.md

## Quick Start

### Local Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/trading-bot.git
   cd trading-bot
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Mac/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure settings:**
   - Edit `src/trading_bot/config/settings.py`
   - Add your API credentials and trading parameters

5. **Run the bot:**
   ```bash
   python -m trading_bot.main
   ```

### Docker Installation

1. **Build image:**
   ```bash
   docker build -t trading-bot .
   ```

2. **Run container:**
   ```bash
   docker run -e API_KEY="your_key" -e API_SECRET="your_secret" trading-bot
   ```

## GitHub Setup

### Initial Setup

1. **Create GitHub repository:**
   - Go to https://github.com/new
   - Name: `trading-bot`
   - Description: "Trading bot for forex and stocks"
   - Make it Public or Private

2. **Add remote and push:**
   ```bash
   git remote add origin https://github.com/your-username/trading-bot.git
   git branch -M main
   git push -u origin main
   ```

### GitHub Actions (CI/CD)

Create `.github/workflows/tests.yml`:
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - run: pip install -r requirements.txt
      - run: python -m pytest
```

## Deployment Options

### Option 1: Cloud Deployment (AWS Lambda)

```bash
pip install zappa
zappa init
zappa deploy production
```

### Option 2: Heroku

```bash
heroku login
heroku create trading-bot-app
git push heroku main
```

### Option 3: DigitalOcean App Platform

1. Connect GitHub account
2. Select repository
3. Auto-deploy on push

### Option 4: Docker + Kubernetes

```bash
docker build -t trading-bot:latest .
kubectl apply -f k8s/deployment.yaml
```

## Environment Variables

Set these for production:
```bash
API_KEY=your_alpaca_key
API_SECRET=your_alpaca_secret
SYMBOL=AAPL
QUANTITY=100
LOG_LEVEL=INFO
```

## Monitoring

- Check logs: `tail -f logs/trading_bot_*.log`
- Monitor performance: See backtest results
- Track trades: Query positions and order history

## Troubleshooting

### Import errors:
```bash
pip install -e .
```

### Connection issues:
- Verify API credentials
- Check network connectivity
- Review logs in `logs/` directory

### Data fetching:
- Ensure Yahoo Finance is accessible
- Check yfinance library version
- Verify symbol format (e.g., AAPL vs AAPL-USD)

## Testing

```bash
# Run main bot
python -m trading_bot.main

# Run specific strategy
python -c "from trading_bot.strategies.ma_strategy import MovingAverageStrategy; print('OK')"

# Test data fetching
python -c "from trading_bot.data.data_fetcher import DataFetcher; print(DataFetcher.get_real_time_price('AAPL'))"
```

## Performance Tuning

- Adjust `SHORT_WINDOW` and `LONG_WINDOW` for MA strategy
- Tune RSI period and thresholds
- Optimize Bollinger Bands parameters
- Reduce position size to lower risk

## Support

- GitHub Issues: Report bugs and request features
- Documentation: See README.md
- Community: Discussions section on GitHub
