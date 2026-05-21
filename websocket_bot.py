#!/usr/bin/env python3
"""
DERIV TRADING BOT - WebSocket Trading
Places actual trades using WebSocket connection
"""

import os
import sys
import time
import json
import asyncio
import websockets
from datetime import datetime
import pandas as pd

# Set token
TOKEN = "KyalQ6MUAnoB5Fb"
os.environ["DERIV_API_TOKEN"] = TOKEN

# Add src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from trading_bot.data.data_fetcher import DataFetcher
import logging

logging.getLogger('urllib3').setLevel(logging.CRITICAL)
logging.getLogger('trading_bot').setLevel(logging.CRITICAL)

class DerivBot:
    def __init__(self, api_token):
        self.api_token = api_token
        self.app_id = "1089"
        self.req_counter = 100
        self.ws = None
        self.balance = 0
        
    async def connect_ws(self):
        """Connect to Deriv WebSocket"""
        url = f"wss://ws.derivws.com/websockets/v3?app_id={self.app_id}"
        try:
            self.ws = await websockets.connect(url, ping_interval=None)
            
            # Send authorization
            auth_payload = {
                "authorize": self.api_token,
                "req_id": self.req_counter
            }
            self.req_counter += 1
            
            await self.ws.send(json.dumps(auth_payload))
            response = await self.ws.recv()
            data = json.loads(response)
            
            if data.get("authorize"):
                print("✓ WebSocket authorized")
                return True
            else:
                print("✗ Authorization failed")
                return False
        except Exception as e:
            print(f"✗ WebSocket connection failed: {str(e)}")
            return False
    
    async def get_balance(self):
        """Get account balance via WebSocket"""
        try:
            payload = {
                "balance": 1,
                "subscribe": 0,
                "req_id": self.req_counter
            }
            self.req_counter += 1
            
            await self.ws.send(json.dumps(payload))
            response = await self.ws.recv()
            data = json.loads(response)
            
            if data.get("balance"):
                self.balance = float(data["balance"].get("balance", 0))
                return self.balance
            return 0
        except Exception as e:
            print(f"Error getting balance: {str(e)}")
            return 0
    
    async def place_trade(self, contract_type, amount=10):
        """Place actual trade via WebSocket"""
        try:
            payload = {
                "buy": 1 if contract_type == "CALL" else 0,
                "sell": 1 if contract_type == "PUT" else 0,
                "symbol": "frxEURUSD",
                "amount": amount,
                "basis": "stake",
                "contract_type": contract_type,
                "duration": 1,
                "duration_unit": "m",
                "req_id": self.req_counter
            }
            self.req_counter += 1
            
            await self.ws.send(json.dumps(payload))
            response = await self.ws.recv()
            data = json.loads(response)
            
            if data.get("buy") or data.get("sell"):
                order_info = data.get("buy") or data.get("sell")
                order_id = order_info.get("transaction_id")
                return True, order_id
            else:
                error = data.get("error", {})
                return False, error.get("message", "Unknown error")
        except Exception as e:
            return False, str(e)

def simple_trading_signal(data):
    """Generate trading signal from data"""
    try:
        if len(data) < 21:
            return "HOLD", 0, 0, 0
        
        # Get Close prices
        if isinstance(data.columns, pd.MultiIndex):
            close_col = [col for col in data.columns if col[0] == 'Close'][0]
            close_prices = data[close_col].values
        else:
            close_prices = data['Close'].values
        
        current_price = float(close_prices[-1])
        short_ma = float(close_prices[-5:].mean())
        long_ma = float(close_prices[-20:].mean())
        
        if short_ma > long_ma:
            signal = "BUY"
        elif short_ma < long_ma:
            signal = "SELL"
        else:
            signal = "HOLD"
        
        return signal, current_price, short_ma, long_ma
    except Exception as e:
        print(f"Signal Error: {str(e)}")
        return "HOLD", 0, 0, 0

async def main():
    print("\n" + "="*70)
    print("📈 DERIV TRADING BOT - WEBSOCKET VERSION")
    print("="*70)
    
    # Initialize
    bot = DerivBot(TOKEN)
    fetcher = DataFetcher()
    
    # Connect
    print("\nConnecting to Deriv via WebSocket...", end=" ", flush=True)
    if not await bot.connect_ws():
        print("FAILED")
        return
    
    print("OK")
    
    # Get balance
    balance = await bot.get_balance()
    print(f"Account: Demo")
    print(f"Balance: ${balance:.2f}\n")
    print("="*70 + "\n")
    
    iteration = 0
    
    # Main loop
    while True:
        iteration += 1
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        try:
            print(f"[{timestamp}] Iteration {iteration}")
            
            # Get data
            print(f"  Fetching data...", end=" ", flush=True)
            data = fetcher.fetch_data("EURUSD=X", days=30)
            
            if data.empty:
                print("NO DATA")
                await asyncio.sleep(60)
                continue
            
            print(f"OK")
            
            # Get signal
            signal, price, short_ma, long_ma = simple_trading_signal(data)
            
            print(f"  Price: ${price:.5f}")
            print(f"  Short MA: ${short_ma:.5f}")
            print(f"  Long MA:  ${long_ma:.5f}")
            print(f"  Signal: {signal}")
            
            # Place trade
            if signal == "BUY":
                print(f"  ACTION: Placing BUY order...")
                success, result = await bot.place_trade("CALL", amount=10)
                if success:
                    print(f"  ✓ BUY order placed (ID: {result})")
                else:
                    print(f"  ✗ BUY failed: {result}")
            
            elif signal == "SELL":
                print(f"  ACTION: Placing SELL order...")
                success, result = await bot.place_trade("PUT", amount=10)
                if success:
                    print(f"  ✓ SELL order placed (ID: {result})")
                else:
                    print(f"  ✗ SELL failed: {result}")
            
            else:
                print(f"  ACTION: HOLD (waiting for signal)")
            
            print()
            
        except KeyboardInterrupt:
            print("\n" + "="*70)
            print("Bot stopped by user")
            print("="*70 + "\n")
            break
        except Exception as e:
            print(f"  Error: {str(e)}\n")
        
        print(f"  Waiting 60 seconds...\n")
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
