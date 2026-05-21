import requests
import json
import logging
import asyncio
import websockets
from typing import Dict, Any, Optional
from .base_platform import TradingPlatform

logger = logging.getLogger(__name__)

class DerivPlatform(TradingPlatform):
    """Deriv.com trading platform adapter with WebSocket support"""
    
    def __init__(self, api_token: str, app_id: str = "1089", account_type: str = "demo"):
        """
        Initialize Deriv platform adapter
        
        Args:
            api_token: Your Deriv API token from account settings
            app_id: Deriv app ID (default: 1089)
            account_type: "demo" or "real"
        """
        self.api_token = api_token
        self.app_id = app_id
        self.account_type = account_type
        # Use WebSocket endpoint for real-time API
        self.base_url = "wss://ws.derivws.com/websockets/v3?app_id=" + app_id
        self.rest_url = "https://api.deriv.com/api/v3"
        self.session = None
        self.ws_connection = None
        self.balance = 0
        self.account_id = None
        self.req_counter = 1
        logger.info(f"Initialized Deriv platform ({account_type} account) with WebSocket support")

    def connect(self) -> bool:
        """Connect to Deriv API and verify credentials"""
        try:
            # Try WebSocket connection first (async)
            logger.info("Attempting WebSocket connection...")
            
            # Create event loop for async connection
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                result = loop.run_until_complete(self._async_connect())
                if result:
                    logger.info("[WebSocket] Successfully connected")
                    return True
            except Exception as e:
                logger.warning(f"WebSocket connection failed: {str(e)}")
            finally:
                loop.close()
            
            # Fallback to REST API with updated endpoint
            logger.info("Attempting REST API connection (fallback)...")
            self.session = requests.Session()
            self.session.headers.update({
                "Content-Type": "application/json"
            })
            
            # Try REST API connection
            result = self._test_rest_connection()
            if result:
                logger.info("[REST API] Successfully connected")
                self._get_account_info()
                return True
            else:
                logger.error("Failed to connect via both WebSocket and REST API")
                return False
                
        except Exception as e:
            logger.error(f"Failed to connect to Deriv: {str(e)}")
            return False

    async def _async_connect(self) -> bool:
        """Async WebSocket connection"""
        try:
            # Connect to WebSocket
            async with websockets.connect(self.base_url, ping_interval=None) as ws:
                self.ws_connection = ws
                
                # Send authorization
                auth_payload = {
                    "authorize": self.api_token,
                    "req_id": self.req_counter
                }
                self.req_counter += 1
                
                await ws.send(json.dumps(auth_payload))
                
                # Receive response
                response_text = await ws.recv()
                response = json.loads(response_text)
                
                if response.get("authorize"):
                    logger.info("WebSocket authorization successful")
                    self.account_id = response["authorize"].get("loginid")
                    await self._async_get_account_info()
                    return True
                else:
                    error_msg = response.get("error", {}).get("message", "Unknown error")
                    logger.error(f"Authorization failed: {error_msg}")
                    return False
        except Exception as e:
            logger.debug(f"WebSocket connection error: {str(e)}")
            return False

    async def _async_get_account_info(self) -> bool:
        """Get account info via WebSocket"""
        try:
            balance_payload = {
                "balance": 1,
                "subscribe": 0,
                "req_id": self.req_counter
            }
            self.req_counter += 1
            
            await self.ws_connection.send(json.dumps(balance_payload))
            response_text = await self.ws_connection.recv()
            response = json.loads(response_text)
            
            if response.get("balance"):
                self.balance = float(response["balance"].get("balance", 0))
                logger.info(f"Account balance: ${self.balance:.2f}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to get account info via WebSocket: {str(e)}")
            return False

    def _test_rest_connection(self) -> bool:
        """Test REST API connection with multiple endpoint options"""
        endpoints = [
            "https://api.deriv.com/api/v3",
            "https://api.deriv.app/api/v3",
            "https://api.deriv.app/api",
        ]
        
        payload = {
            "get_account_status": 1,
            "authorize": self.api_token,
            "app_id": self.app_id,
            "req_id": 1
        }
        
        for endpoint in endpoints:
            try:
                logger.debug(f"Testing endpoint: {endpoint}")
                response = requests.post(endpoint, json=payload, timeout=5)
                
                # Check if response is JSON
                try:
                    data = response.json()
                    if response.status_code == 200 and data.get("account_status"):
                        self.rest_url = endpoint
                        logger.info(f"Working endpoint found: {endpoint}")
                        return True
                except (json.JSONDecodeError, ValueError):
                    logger.debug(f"Endpoint returned non-JSON response: {endpoint}")
                    
            except requests.exceptions.RequestException as e:
                logger.debug(f"Endpoint {endpoint} error: {str(e)}")
        
        return False

    def _send_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send request to Deriv API (REST fallback)"""
        try:
            # Initialize session if not already done
            if self.session is None:
                self.session = requests.Session()
                self.session.headers.update({
                    "Content-Type": "application/json"
                })
            
            payload["authorize"] = self.api_token
            payload["app_id"] = self.app_id
            
            response = self.session.post(self.rest_url, json=payload, timeout=10)
            
            # Check if response is JSON
            try:
                response.raise_for_status()
                data = response.json()
                return data
            except (json.JSONDecodeError, ValueError):
                logger.warning(f"REST API returned non-JSON response (status: {response.status_code})")
                # Return generic error response
                return {"error": {"message": "API returned non-JSON response - endpoint may have changed"}}
                
        except requests.exceptions.Timeout:
            logger.error("Request timeout - API may be unavailable")
            return {"error": {"message": "Request timeout"}}
        except requests.exceptions.ConnectionError:
            logger.error("Connection error - cannot reach API endpoint")
            return {"error": {"message": "Connection error"}}
        except Exception as e:
            logger.error(f"Request failed: {str(e)}")
            return {"error": {"message": str(e)}}

    def _get_account_info(self) -> bool:
        """Get account information"""
        try:
            payload = {
                "balance": 1,
                "subscribe": 0,
                "req_id": 2
            }
            response = self._send_request(payload)
            
            if response.get("balance"):
                self.balance = float(response["balance"].get("balance", 0))
                self.account_id = response["balance"].get("loginid")
                logger.info(f"Account balance: ${self.balance:.2f}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to get account info: {str(e)}")
            return False

    def get_balance(self) -> Dict[str, Any]:
        """Get account balance"""
        try:
            self._get_account_info()
            balance = {
                "cash": self.balance,
                "portfolio_value": self.balance,
                "buying_power": self.balance
            }
            return balance
        except Exception as e:
            logger.error(f"Failed to get balance: {str(e)}")
            return {"cash": 0, "portfolio_value": 0, "buying_power": 0}

    def get_price(self, symbol: str) -> float:
        """Get current price for a symbol (Deriv uses underlyings, not stocks)"""
        try:
            # Deriv uses different symbol format, e.g., R_50 for Volatility Index
            # This example uses major currency pairs and indices
            deriv_symbol = self._convert_symbol(symbol)
            
            payload = {
                "ticks": deriv_symbol,
                "subscribe": 0,
                "req_id": 3
            }
            response = self._send_request(payload)
            
            if response.get("tick"):
                price = float(response["tick"].get("quote", 0))
                logger.debug(f"{symbol}: ${price:.2f}")
                return price
            else:
                logger.warning(f"Could not get price for {symbol}")
                return 0.0
        except Exception as e:
            logger.error(f"Failed to get price for {symbol}: {str(e)}")
            return 0.0

    def place_order(self, symbol: str, quantity: int, side: str, order_type: str = "market") -> Optional[Dict[str, Any]]:
        """
        Place an order on Deriv
        
        Args:
            symbol: Trading symbol (e.g., 'EUR_USD')
            quantity: Trade amount (bet size in contract)
            side: 'buy' or 'sell'
            order_type: 'market' or 'limit'
            
        Returns:
            Order details or None if failed
        """
        try:
            deriv_symbol = self._convert_symbol(symbol)
            
            # Deriv contracts require specific parameters
            payload = {
                "buy": 1 if side.lower() == "buy" else 0,
                "sell": 1 if side.lower() == "sell" else 0,
                "symbol": deriv_symbol,
                "amount": quantity,
                "basis": "stake",  # stake = amount in currency
                "contract_type": "CALL" if side.lower() == "buy" else "PUT",
                "duration": 1,
                "duration_unit": "m",  # 1 minute contract
                "req_id": 4
            }
            
            response = self._send_request(payload)
            
            if response.get("buy") or response.get("sell"):
                order_info = response.get("buy") or response.get("sell")
                order_id = order_info.get("transaction_id")
                logger.info(f"Order placed: {side} {quantity} {symbol} (ID: {order_id})")
                return {
                    "order_id": order_id,
                    "symbol": symbol,
                    "quantity": quantity,
                    "side": side,
                    "status": "accepted"
                }
            else:
                error_msg = response.get("error", {}).get("message", "Unknown error")
                logger.error(f"Failed to place order: {error_msg}")
                return None
        except Exception as e:
            logger.error(f"Failed to place order: {str(e)}")
            return None

    def _convert_symbol(self, symbol: str) -> str:
        """Convert standard symbol format to Deriv format"""
        # Map common symbols to Deriv underlyings
        symbol_map = {
            "EUR_USD": "frxEURUSD",
            "GBP_USD": "frxGBPUSD",
            "USD_JPY": "frxUSDJPY",
            "EURUSD": "frxEURUSD",
            "GBPUSD": "frxGBPUSD",
            "USDJPY": "frxUSDJPY",
            "AAPL": "AAPL",
            "GOOGL": "GOOGL",
            "MSFT": "MSFT",
            "BTC": "BTCUSD",
            "ETH": "ETHUSD",
            "R_50": "R_50",  # Volatility Index
            "VIX": "R_50",   # Map VIX to Volatility Index
        }
        
        return symbol_map.get(symbol.upper(), symbol)

    def get_positions(self) -> list:
        """Get open positions"""
        try:
            payload = {
                "portfolio": 1,
                "subscribe": 0,
                "req_id": 5
            }
            response = self._send_request(payload)
            
            if response.get("portfolio"):
                positions = response["portfolio"]
                logger.info(f"Open positions: {len(positions)}")
                return positions
            return []
        except Exception as e:
            logger.error(f"Failed to get positions: {str(e)}")
            return []

    def close_position(self, position_id: str) -> bool:
        """Close an open position"""
        try:
            payload = {
                "sell": 1,
                "contract_id": position_id,
                "req_id": 6
            }
            response = self._send_request(payload)
            
            if response.get("sell"):
                logger.info(f"Position closed: {position_id}")
                return True
            else:
                logger.error(f"Failed to close position: {position_id}")
                return False
        except Exception as e:
            logger.error(f"Failed to close position: {str(e)}")
            return False

    def get_account_status(self) -> Dict[str, Any]:
        """Get detailed account status"""
        try:
            payload = {
                "get_account_status": 1,
                "req_id": 7
            }
            response = self._send_request(payload)
            
            if response.get("account_status"):
                return response["account_status"]
            return {}
        except Exception as e:
            logger.error(f"Failed to get account status: {str(e)}")
            return {}

    def __repr__(self) -> str:
        return f"DerivPlatform(account_type={self.account_type}, balance=${self.balance:.2f})"
