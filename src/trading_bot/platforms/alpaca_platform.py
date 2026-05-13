import requests
import logging
from typing import Dict, Any
from .base_platform import TradingPlatform

logger = logging.getLogger(__name__)

class AlpacaPlatform(TradingPlatform):
    """Alpaca trading platform adapter"""
    
    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://paper-api.alpaca.markets"):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.session = None
        logger.info(f"Initialized Alpaca platform with base URL: {base_url}")

    def connect(self) -> bool:
        """Connect to Alpaca API"""
        try:
            self.session = requests.Session()
            self.session.headers.update({
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            })
            # Test connection
            response = self.session.get(f"{self.base_url}/v2/account")
            response.raise_for_status()
            logger.info("Successfully connected to Alpaca")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Alpaca: {str(e)}")
            return False

    def get_balance(self) -> Dict[str, Any]:
        """Get account balance"""
        try:
            response = self.session.get(f"{self.base_url}/v2/account")
            response.raise_for_status()
            account = response.json()
            balance = {
                "cash": float(account.get("cash", 0)),
                "portfolio_value": float(account.get("portfolio_value", 0)),
                "buying_power": float(account.get("buying_power", 0))
            }
            logger.info(f"Account balance: ${balance['portfolio_value']:.2f}")
            return balance
        except Exception as e:
            logger.error(f"Failed to get balance: {str(e)}")
            return {}

    def get_price(self, symbol: str) -> float:
        """Get current price for a symbol"""
        try:
            response = self.session.get(
                f"{self.base_url}/v2/bars/latest",
                params={"symbols": symbol, "feed": "sip"}
            )
            response.raise_for_status()
            data = response.json()
            if "bars" in data and symbol in data["bars"]:
                price = float(data["bars"][symbol]["c"])
                logger.debug(f"Price for {symbol}: ${price:.2f}")
                return price
            logger.warning(f"No price data available for {symbol}")
            return 0.0
        except Exception as e:
            logger.error(f"Failed to get price for {symbol}: {str(e)}")
            return 0.0

    def place_order(self, symbol: str, quantity: float, side: str, order_type: str = "market", limit_price: float = None) -> Dict[str, Any]:
        """Place an order"""
        try:
            order_data = {
                "symbol": symbol,
                "qty": quantity,
                "side": side.lower(),
                "type": order_type,
                "time_in_force": "day"
            }
            if order_type == "limit" and limit_price:
                order_data["limit_price"] = limit_price
            
            response = self.session.post(
                f"{self.base_url}/v2/orders",
                json=order_data
            )
            response.raise_for_status()
            order = response.json()
            logger.info(f"Order placed: {side} {quantity} {symbol} at ${order.get('filled_avg_price', 'market')}")
            return {
                "order_id": order.get("id"),
                "status": order.get("status"),
                "filled_qty": float(order.get("filled_qty", 0))
            }
        except Exception as e:
            logger.error(f"Failed to place order: {str(e)}")
            return {}

    def get_positions(self) -> Dict[str, Any]:
        """Get current positions"""
        try:
            response = self.session.get(f"{self.base_url}/v2/positions")
            response.raise_for_status()
            positions = response.json()
            logger.info(f"Retrieved {len(positions)} positions")
            return {pos["symbol"]: {"qty": float(pos["qty"]), "current_price": float(pos["current_price"])} for pos in positions}
        except Exception as e:
            logger.error(f"Failed to get positions: {str(e)}")
            return {}
