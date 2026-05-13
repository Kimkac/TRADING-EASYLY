import pandas as pd
import logging
import numpy as np

logger = logging.getLogger(__name__)

def _to_scalar(val):
    """Convert Series to scalar value"""
    if isinstance(val, pd.Series):
        return val.item() if len(val) == 1 else val.iloc[0]
    return val


class MovingAverageStrategy:
    def __init__(self, short_window=5, long_window=20):
        self.short_window = short_window
        self.long_window = long_window
        logger.info(f"Initialized MA strategy: short_window={short_window}, long_window={long_window}")

    def generate_signal(self, prices):
        if len(prices) < self.long_window + 1:
            logger.debug(f"Insufficient data for MA strategy: {len(prices)} < {self.long_window + 1}")
            return 'HOLD'
        
        short_ma = prices.rolling(window=self.short_window).mean()
        long_ma = prices.rolling(window=self.long_window).mean()
        
        current_short = float(_to_scalar(short_ma.iloc[-1]))
        current_long = float(_to_scalar(long_ma.iloc[-1]))
        previous_short = float(_to_scalar(short_ma.iloc[-2]))
        previous_long = float(_to_scalar(long_ma.iloc[-2]))
        
        # Handle NaN values
        if np.isnan(current_short) or np.isnan(current_long) or np.isnan(previous_short) or np.isnan(previous_long):
            logger.debug("MA values contain NaN")
            return 'HOLD'
        
        if current_short > current_long and previous_short <= previous_long:
            logger.info(f"MA signal: BUY (Short MA={current_short:.2f} > Long MA={current_long:.2f})")
            return 'BUY'
        elif current_short < current_long and previous_short >= previous_long:
            logger.info(f"MA signal: SELL (Short MA={current_short:.2f} < Long MA={current_long:.2f})")
            return 'SELL'
        
        logger.debug("MA signal: HOLD")
        return 'HOLD'