#!/usr/bin/env python3
"""
Trading Bot Main Entry Point
"""

import logging
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from trading_bot.config.settings import SYMBOL, QUANTITY, SHORT_WINDOW, LONG_WINDOW
from trading_bot.strategies.ma_strategy import MovingAverageStrategy
from trading_bot.strategies.advanced_strategies import RSIStrategy, MACDStrategy, BollingerBandsStrategy
from trading_bot.data.data_fetcher import DataFetcher
from trading_bot.backtest.backtester import Backtester
from trading_bot.platforms.alpaca_platform import AlpacaPlatform
from trading_bot.utils.logger import setup_logging

# Setup logging
logger = setup_logging()

def main():
    logger.info("="*60)
    logger.info("Trading Bot Started")
    logger.info("="*60)

    try:
        # Fetch real market data
        logger.info(f"Fetching market data for {SYMBOL}...")
        prices = DataFetcher.get_historical_prices(SYMBOL, days=100)
        
        if prices.empty:
            logger.error("Failed to fetch market data")
            return
        
        logger.info(f"Retrieved {len(prices)} price points")
        
        # Test different strategies
        logger.info("\n" + "="*60)
        logger.info("Testing Strategies")
        logger.info("="*60)
        
        # Moving Average Strategy
        ma_strategy = MovingAverageStrategy(short_window=SHORT_WINDOW, long_window=LONG_WINDOW)
        ma_signal = ma_strategy.generate_signal(prices)
        logger.info(f"Moving Average Signal: {ma_signal}")
        
        # RSI Strategy
        rsi_strategy = RSIStrategy(period=14)
        rsi_signal = rsi_strategy.generate_signal(prices)
        logger.info(f"RSI Signal: {rsi_signal}")
        
        # MACD Strategy
        macd_strategy = MACDStrategy()
        macd_signal = macd_strategy.generate_signal(prices)
        logger.info(f"MACD Signal: {macd_signal}")
        
        # Bollinger Bands Strategy
        bb_strategy = BollingerBandsStrategy()
        bb_signal = bb_strategy.generate_signal(prices)
        logger.info(f"Bollinger Bands Signal: {bb_signal}")
        
        # Backtest Moving Average Strategy
        logger.info("\n" + "="*60)
        logger.info("Running Backtest")
        logger.info("="*60)
        
        backtester = Backtester(initial_balance=10000)
        results = backtester.run(prices, lambda p: ma_strategy.generate_signal(p))
        
        logger.info(f"\nBacktest Results:")
        logger.info(f"  Total Return: {results['total_return_pct']:.2f}%")
        logger.info(f"  Final Balance: ${results['final_balance']:.2f}")
        logger.info(f"  Total Trades: {results['total_trades']}")
        logger.info(f"  Win Rate: {results['win_rate']:.2f}%")
        logger.info(f"  Sharpe Ratio: {results['sharpe_ratio']:.2f}")
        logger.info(f"  Max Drawdown: {results['max_drawdown']:.2f}%")
        
        # Show current price
        current_price = DataFetcher.get_real_time_price(SYMBOL)
        logger.info(f"\nCurrent {SYMBOL} Price: ${current_price:.2f}")
        
        logger.info("\n" + "="*60)
        logger.info("Trading Bot Completed Successfully")
        logger.info("="*60)
        
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    main()