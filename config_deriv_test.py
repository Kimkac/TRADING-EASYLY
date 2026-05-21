"""
Test Configuration for Deriv Bot
This file contains demo tokens for testing purposes only.
For production, use your real API token from https://app.deriv.com
"""

# Demo API Token (Replace with your real token from app.deriv.com)
# To get your token:
# 1. Go to https://app.deriv.com
# 2. Settings → API tokens
# 3. Create new token
# 4. Copy and replace the value below

DERIV_API_TOKEN = "a1A2b3B4c5C6d7D8e9E0f1F2g3G4h5H6"  # Demo token (REPLACE ME)
DERIV_ACCOUNT_TYPE = "demo"  # Use "demo" for testing, "real" for live trading
DERIV_BASE_URL = "https://api.deriv.com/api/v3"

# Trading Parameters
SYMBOL = "EUR_USD"
QUANTITY = 10
SHORT_MA = 5
LONG_MA = 20
SLEEP_INTERVAL = 60  # seconds between checks
