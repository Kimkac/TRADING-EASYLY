#!/usr/bin/env python3
import sys
sys.path.insert(0, 'src')
from trading_bot.data.data_fetcher import DataFetcher
import pandas as pd

fetcher = DataFetcher()
data = fetcher.fetch_data('EURUSD=X', days=30)

print(f"Data shape: {data.shape}")
print(f"Data type: {type(data)}")
print(f"Columns: {data.columns.tolist()}")
print(f"\nLast 3 rows:")
print(data.tail(3))
print(f"\nClose column last value: {data['Close'].iloc[-1]}")
print(f"Type: {type(data['Close'].iloc[-1])}")
print(f"Close tail(5): {data['Close'].tail(5)}")
print(f"Mean of tail(5): {data['Close'].tail(5).mean()}")
print(f"Type of mean: {type(data['Close'].tail(5).mean())}")
