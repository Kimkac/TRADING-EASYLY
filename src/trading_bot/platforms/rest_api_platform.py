import requests
import logging
from typing import Dict, Any
from .base_platform import TradingPlatform

logger = logging.getLogger(__name__)

class RestApiPlatform(TradingPlatform):
    """Generic REST API platform adapter for custom trading platforms"""
    
    def __init__(self, base_url: str, api_key: str = None, headers: Dict[str, str] = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = None
        self.custom_headers = headers or {}
        logger.info(f"Initialized REST API platform with base URL: {base_url}")

    def connect(self) -> bool:
        """Connect to REST API platform"""
        try:
            self.session = requests.Session()
            if self.api_key:
                self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})
            self.session.headers.update(self.custom_headers)
            logger.info("Successfully initialized REST API session")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize session: {str(e)}")
            return False

    def get_balance(self) -> Dict[str, Any]:
        """Get account balance"""
        try:
            response = self.session.get(f"{self.base_url}/account/balance")
            response.raise_for_status()
            balance = response.json()
            logger.info(f"Retrieved account balance")
            return balance
        except Exception as e:
            logger.error(f"Failed to get balance: {str(e)}")
            return {}

    def get_price(self, symbol: str) -> float:
        """Get current price for a symbol"""
        try:
            response = self.session.get(f"{self.base_url}/price/{symbol}")
            response.raise_for_status()
            data = response.json()
            price = float(data.get("price", 0))
            logger.debug(f"Price for {symbol}: ${price:.2f}")
            return price
        except Exception as e:
            logger.error(f"Failed to get price for {symbol}: {str(e)}")
            return 0.0

    def place_order(self, symbol: str, quantity: float, side: str, **kwargs) -> Dict[str, Any]:
        """Place an order"""
        try:
            order_data = {
                "symbol": symbol,
                "quantity": quantity,
                "side": side.lower()
            }
            order_data.update(kwargs)
            response = self.session.post(f"{self.base_url}/orders", json=order_data)
            response.raise_for_status()
            order = response.json()
            logger.info(f"Order placed: {side} {quantity} {symbol}")
            return order
        except Exception as e:
            logger.error(f"Failed to place order: {str(e)}")
            return {}
