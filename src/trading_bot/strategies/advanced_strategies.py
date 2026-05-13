import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

def _to_scalar(val):
    """Convert Series to scalar value"""
    if isinstance(val, pd.Series):
        return val.item() if len(val) == 1 else val.iloc[0]
    return val


class RSIStrategy:
    """Relative Strength Index strategy"""
    
    def __init__(self, period: int = 14, overbought: float = 70, oversold: float = 30):
        self.period = period
        self.overbought = overbought
        self.oversold = oversold
        logger.info(f"Initialized RSI strategy: period={period}, overbought={overbought}, oversold={oversold}")

    def calculate_rsi(self, prices: pd.Series) -> pd.Series:
        """Calculate RSI indicator"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def generate_signal(self, prices: pd.Series) -> str:
        """Generate trading signal based on RSI"""
        if len(prices) < self.period + 2:
            logger.debug("Insufficient data for RSI")
            return 'HOLD'
        
        rsi = self.calculate_rsi(prices)
        current_rsi = float(_to_scalar(rsi.iloc[-1]))
        previous_rsi = float(_to_scalar(rsi.iloc[-2]))
        
        if np.isnan(current_rsi) or np.isnan(previous_rsi):
            logger.debug("RSI values contain NaN")
            return 'HOLD'
        
        if current_rsi < self.oversold and previous_rsi >= self.oversold:
            logger.info(f"RSI signal: BUY (RSI={current_rsi:.2f})")
            return 'BUY'
        elif current_rsi > self.overbought and previous_rsi <= self.overbought:
            logger.info(f"RSI signal: SELL (RSI={current_rsi:.2f})")
            return 'SELL'
        
        logger.debug(f"RSI signal: HOLD (RSI={current_rsi:.2f})")
        return 'HOLD'


class MACDStrategy:
    """MACD (Moving Average Convergence Divergence) strategy"""
    
    def __init__(self, fast: int = 12, slow: int = 26, signal: int = 9):
        self.fast = fast
        self.slow = slow
        self.signal = signal
        logger.info(f"Initialized MACD strategy: fast={fast}, slow={slow}, signal={signal}")

    def calculate_macd(self, prices: pd.Series):
        """Calculate MACD indicator"""
        ema_fast = prices.ewm(span=self.fast).mean()
        ema_slow = prices.ewm(span=self.slow).mean()
        macd = ema_fast - ema_slow
        signal_line = macd.ewm(span=self.signal).mean()
        histogram = macd - signal_line
        return macd, signal_line, histogram

    def generate_signal(self, prices: pd.Series) -> str:
        """Generate trading signal based on MACD"""
        if len(prices) < self.slow + self.signal + 2:
            logger.debug("Insufficient data for MACD")
            return 'HOLD'
        
        macd, signal_line, histogram = self.calculate_macd(prices)
        
        current_macd = float(_to_scalar(macd.iloc[-1]))
        current_signal = float(_to_scalar(signal_line.iloc[-1]))
        previous_macd = float(_to_scalar(macd.iloc[-2]))
        previous_signal = float(_to_scalar(signal_line.iloc[-2]))
        
        if np.isnan(current_macd) or np.isnan(current_signal) or np.isnan(previous_macd) or np.isnan(previous_signal):
            logger.debug("MACD values contain NaN")
            return 'HOLD'
        
        if current_macd > current_signal and previous_macd <= previous_signal:
            logger.info(f"MACD signal: BUY (MACD={current_macd:.4f}, Signal={current_signal:.4f})")
            return 'BUY'
        elif current_macd < current_signal and previous_macd >= previous_signal:
            logger.info(f"MACD signal: SELL (MACD={current_macd:.4f}, Signal={current_signal:.4f})")
            return 'SELL'
        
        logger.debug(f"MACD signal: HOLD")
        return 'HOLD'


class BollingerBandsStrategy:
    """Bollinger Bands strategy"""
    
    def __init__(self, period: int = 20, std_dev: float = 2.0):
        self.period = period
        self.std_dev = std_dev
        logger.info(f"Initialized Bollinger Bands strategy: period={period}, std_dev={std_dev}")

    def calculate_bollinger_bands(self, prices: pd.Series):
        """Calculate Bollinger Bands"""
        sma = prices.rolling(window=self.period).mean()
        std = prices.rolling(window=self.period).std()
        upper_band = sma + (self.std_dev * std)
        lower_band = sma - (self.std_dev * std)
        return sma, upper_band, lower_band

    def generate_signal(self, prices: pd.Series) -> str:
        """Generate trading signal based on Bollinger Bands"""
        if len(prices) < self.period + 2:
            logger.debug("Insufficient data for Bollinger Bands")
            return 'HOLD'
        
        sma, upper_band, lower_band = self.calculate_bollinger_bands(prices)
        
        current_price = float(_to_scalar(prices.iloc[-1]))
        current_upper = float(_to_scalar(upper_band.iloc[-1]))
        current_lower = float(_to_scalar(lower_band.iloc[-1]))
        
        if np.isnan(current_upper) or np.isnan(current_lower):
            logger.debug("Bollinger Bands values contain NaN")
            return 'HOLD'
        
        if current_price < current_lower:
            logger.info(f"Bollinger Bands signal: BUY (Price=${current_price:.2f} below lower band=${current_lower:.2f})")
            return 'BUY'
        elif current_price > current_upper:
            logger.info(f"Bollinger Bands signal: SELL (Price=${current_price:.2f} above upper band=${current_upper:.2f})")
            return 'SELL'
        
        logger.debug(f"Bollinger Bands signal: HOLD")
        return 'HOLD'
