import pandas as pd
import logging
from typing import Callable, Dict, Any
import numpy as np

logger = logging.getLogger(__name__)

def _to_scalar(val):
    """Convert Series to scalar value"""
    if isinstance(val, pd.Series):
        return val.item() if len(val) == 1 else val.iloc[0]
    return val

class Backtester:
    """Backtest trading strategies"""
    
    def __init__(self, initial_balance: float = 10000, commission: float = 0.001):
        self.initial_balance = initial_balance
        self.commission = commission
        self.balance = initial_balance
        self.positions = {}
        self.trades = []
        self.equity_curve = []
        logger.info(f"Initialized backtester with balance: ${initial_balance:.2f}")

    def run(self, prices: pd.Series, strategy_func: Callable[[pd.Series], str], position_size: float = 0.95) -> Dict[str, Any]:
        """Run backtest"""
        logger.info(f"Starting backtest with {len(prices)} data points")
        
        for i in range(len(prices) - 1):
            current_prices = prices.iloc[:i+1]
            signal = strategy_func(current_prices)
            
            current_price = float(_to_scalar(prices.iloc[i]))
            current_balance_before = self.balance
            
            if signal == 'BUY' and 'position' not in self.positions:
                quantity = (self.balance * position_size) / current_price
                cost = quantity * current_price * (1 + self.commission)
                if cost <= self.balance:
                    self.positions['position'] = {'quantity': quantity, 'entry_price': current_price}
                    self.balance -= cost
                    self.trades.append({'date': prices.index[i], 'signal': 'BUY', 'price': current_price, 'quantity': quantity})
                    logger.debug(f"BUY signal: {quantity:.2f} units at ${current_price:.2f}")
            
            elif signal == 'SELL' and 'position' in self.positions:
                position = self.positions['position']
                proceeds = position['quantity'] * current_price * (1 - self.commission)
                self.balance += proceeds
                profit = proceeds - (position['quantity'] * position['entry_price'])
                self.trades.append({'date': prices.index[i], 'signal': 'SELL', 'price': current_price, 'quantity': position['quantity'], 'profit': profit})
                logger.debug(f"SELL signal: {position['quantity']:.2f} units at ${current_price:.2f}, Profit: ${profit:.2f}")
                del self.positions['position']
            
            # Calculate equity
            equity = self.balance
            if 'position' in self.positions:
                equity += self.positions['position']['quantity'] * current_price
            self.equity_curve.append(equity)
        
        return self._calculate_metrics()

    def _calculate_metrics(self) -> Dict[str, Any]:
        """Calculate performance metrics"""
        equity_curve = pd.Series(self.equity_curve)
        returns = equity_curve.pct_change().dropna()
        
        total_return = ((self.equity_curve[-1] - self.initial_balance) / self.initial_balance) * 100 if self.equity_curve else 0
        win_trades = sum(1 for t in self.trades if t.get('profit', 0) > 0)
        loss_trades = sum(1 for t in self.trades if t.get('profit', 0) < 0)
        win_rate = (win_trades / len(self.trades) * 100) if self.trades else 0
        
        sharpe_ratio = (returns.mean() / returns.std() * 252**0.5) if len(returns) > 0 and returns.std() > 0 else 0
        max_drawdown = self._calculate_max_drawdown()
        
        metrics = {
            'total_return_pct': total_return,
            'final_balance': self.equity_curve[-1] if self.equity_curve else self.initial_balance,
            'total_trades': len(self.trades),
            'winning_trades': win_trades,
            'losing_trades': loss_trades,
            'win_rate': win_rate,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown
        }
        
        logger.info(f"Backtest Results: Return={total_return:.2f}%, Win Rate={win_rate:.2f}%, Max Drawdown={max_drawdown:.2f}%")
        return metrics

    def _calculate_max_drawdown(self) -> float:
        """Calculate maximum drawdown"""
        equity_series = pd.Series(self.equity_curve)
        cummax = equity_series.cummax()
        drawdown = (equity_series - cummax) / cummax
        return float(drawdown.min() * 100) if len(drawdown) > 0 else 0
