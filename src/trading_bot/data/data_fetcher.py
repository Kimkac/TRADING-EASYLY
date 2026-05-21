import yfinance as yf
import pandas as pd
import logging
from datetime import datetime, timedelta
from typing import Optional

logger = logging.getLogger(__name__)

class DataFetcher:
    """Fetch market data from various sources"""
    
    @staticmethod
    def fetch_data(symbol: str, days: int = 100, interval: str = "1d") -> pd.DataFrame:
        """Fetch market data (main method used by trading bot)"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            return DataFetcher.fetch_yfinance_data(
                symbol, 
                start_date=start_date.strftime('%Y-%m-%d'),
                end_date=end_date.strftime('%Y-%m-%d'),
                interval=interval
            )
        except Exception as e:
            logger.error(f"Failed to fetch data for {symbol}: {str(e)}")
            return pd.DataFrame()

    @staticmethod
    def fetch_yfinance_data(symbol: str, start_date: Optional[str] = None, end_date: Optional[str] = None, interval: str = "1d") -> pd.DataFrame:
        """Fetch data from Yahoo Finance"""
        try:
            if start_date is None:
                start_date = (datetime.now() - timedelta(days=100)).strftime('%Y-%m-%d')
            if end_date is None:
                end_date = datetime.now().strftime('%Y-%m-%d')
            
            logger.info(f"Fetching {symbol} data from {start_date} to {end_date}")
            data = yf.download(symbol, start=start_date, end=end_date, interval=interval, progress=False)
            
            if data.empty:
                logger.warning(f"No data retrieved for {symbol}")
                return pd.DataFrame()
            
            logger.info(f"Successfully fetched {len(data)} records for {symbol}")
            return data
        except Exception as e:
            logger.error(f"Failed to fetch data for {symbol}: {str(e)}")
            return pd.DataFrame()

    @staticmethod
    def fetch_multiple_symbols(symbols: list, start_date: Optional[str] = None, end_date: Optional[str] = None) -> dict:
        """Fetch data for multiple symbols"""
        data = {}
        for symbol in symbols:
            data[symbol] = DataFetcher.fetch_yfinance_data(symbol, start_date, end_date)
        return data

    @staticmethod
    def get_historical_prices(symbol: str, days: int = 100) -> pd.Series:
        """Get historical closing prices"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            data = yf.download(symbol, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'), progress=False)
            
            if data.empty:
                logger.warning(f"No historical data for {symbol}")
                return pd.Series()
            
            # Extract Close column if DataFrame
            if isinstance(data, pd.DataFrame):
                prices = data['Close']
            else:
                prices = data
            
            logger.debug(f"Retrieved {len(prices)} historical prices for {symbol}")
            return prices
        except Exception as e:
            logger.error(f"Failed to get historical prices: {str(e)}")
            return pd.Series()

    @staticmethod
    def get_real_time_price(symbol: str) -> float:
        """Get real-time price"""
        try:
            data = yf.download(symbol, period="1d", interval="1m", progress=False)
            if data.empty:
                logger.warning(f"No real-time data for {symbol}")
                return 0.0
            
            close_price = data['Close'].iloc[-1]
            # Convert Series to scalar if needed
            if isinstance(close_price, pd.Series):
                price = float(close_price.iloc[0] if len(close_price) > 0 else 0.0)
            else:
                price = float(close_price)
            return price
        except Exception as e:
            logger.error(f"Failed to get real-time price: {str(e)}")
            return 0.0
