"""
M-Pesa Payment Integration for Trading Bot

Supports:
- Safaricom M-Pesa (Kenya)
- Airtel Money (Uganda, Tanzania, etc)
- Recurring subscriptions
- Instant payment confirmation
"""

import requests
import json
import base64
from datetime import datetime
from typing import Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class MpesaPaymentProcessor:
    """Handle M-Pesa payments via Daraja API"""
    
    def __init__(self, 
                 consumer_key: str,
                 consumer_secret: str,
                 business_shortcode: str,
                 passkey: str,
                 environment: str = "sandbox"):
        """
        Initialize M-Pesa processor
        
        Args:
            consumer_key: Daraja API consumer key
            consumer_secret: Daraja API consumer secret
            business_shortcode: Your Till/Business number
            passkey: M-Pesa pass key for STK push
            environment: 'sandbox' or 'production'
        """
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.business_shortcode = business_shortcode
        self.passkey = passkey
        self.environment = environment
        
        # API endpoints
        self.auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        self.stk_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        self.callback_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate"
        self.query_url = "https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query"
        
        if environment == "production":
            self.auth_url = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
            self.stk_url = "https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
            self.callback_url = "https://api.safaricom.co.ke/mpesa/c2b/v1/simulate"
            self.query_url = "https://api.safaricom.co.ke/mpesa/stkpushquery/v1/query"
        
        self.access_token = None
        self.token_expiry = None
    
    def get_access_token(self) -> str:
        """Get M-Pesa access token from Daraja API"""
        try:
            # Create base64 encoded credentials
            credentials = f"{self.consumer_key}:{self.consumer_secret}"
            encoded = base64.b64encode(credentials.encode()).decode()
            
            headers = {
                "Authorization": f"Basic {encoded}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(self.auth_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            self.access_token = data.get('access_token')
            
            logger.info("✅ M-Pesa access token obtained successfully")
            return self.access_token
            
        except Exception as e:
            logger.error(f"❌ Failed to get M-Pesa access token: {e}")
            raise
    
    def generate_password(self) -> Tuple[str, str]:
        """Generate M-Pesa password for STK push"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        data_string = f"{self.business_shortcode}{self.passkey}{timestamp}"
        encoded = base64.b64encode(data_string.encode()).decode()
        return encoded, timestamp
    
    def initiate_stk_push(self,
                         phone_number: str,
                         amount: int,
                         account_reference: str,
                         transaction_desc: str = "Trading Bot Subscription") -> Dict:
        """
        Initiate STK push (pop-up payment prompt on customer's phone)
        
        Args:
            phone_number: Customer's M-Pesa registered phone (254712345678 format)
            amount: Amount in KES/currency
            account_reference: Your reference (e.g., user_id or subscription_id)
            transaction_desc: Description of transaction
            
        Returns:
            Response from M-Pesa API with CheckoutRequestID
        """
        try:
            if not self.access_token:
                self.get_access_token()
            
            password, timestamp = self.generate_password()
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "BusinessShortCode": self.business_shortcode,
                "Password": password,
                "Timestamp": timestamp,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": amount,
                "PartyA": phone_number,
                "PartyB": self.business_shortcode,
                "PhoneNumber": phone_number,
                "CallBackURL": self.callback_url,
                "AccountReference": account_reference,
                "TransactionDesc": transaction_desc
            }
            
            response = requests.post(
                self.stk_url,
                json=payload,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            
            result = response.json()
            
            if result.get('ResponseCode') == '0':
                logger.info(f"✅ STK Push initiated for {phone_number}: {result.get('CheckoutRequestID')}")
                return {
                    "success": True,
                    "checkout_id": result.get('CheckoutRequestID'),
                    "request_id": result.get('RequestId'),
                    "response_code": result.get('ResponseCode'),
                    "response_description": result.get('ResponseDescription'),
                    "customer_message": result.get('CustomerMessage')
                }
            else:
                logger.warning(f"⚠️ STK Push failed: {result.get('ResponseDescription')}")
                return {
                    "success": False,
                    "error": result.get('ResponseDescription'),
                    "response_code": result.get('ResponseCode')
                }
        
        except Exception as e:
            logger.error(f"❌ STK Push error: {e}")
            return {"success": False, "error": str(e)}
    
    def query_transaction(self, checkout_request_id: str) -> Dict:
        """Query transaction status"""
        try:
            if not self.access_token:
                self.get_access_token()
            
            password, timestamp = self.generate_password()
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "BusinessShortCode": self.business_shortcode,
                "Password": password,
                "Timestamp": timestamp,
                "CheckoutRequestID": checkout_request_id
            }
            
            response = requests.post(
                self.query_url,
                json=payload,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            
            return response.json()
        
        except Exception as e:
            logger.error(f"❌ Transaction query failed: {e}")
            return {"success": False, "error": str(e)}
    
    def validate_callback(self, callback_data: Dict) -> Tuple[bool, Optional[str]]:
        """
        Validate M-Pesa payment callback
        
        Args:
            callback_data: Data received from M-Pesa callback
            
        Returns:
            (is_valid, transaction_id)
        """
        try:
            result_code = callback_data.get('Body', {}).get('stkCallback', {}).get('ResultCode')
            
            if result_code == 0:
                # Payment successful
                checkout_id = callback_data.get('Body', {}).get('stkCallback', {}).get('CheckoutRequestID')
                merchant_request_id = callback_data.get('Body', {}).get('stkCallback', {}).get('MerchantRequestID')
                
                logger.info(f"✅ Payment validated: {checkout_id}")
                return True, checkout_id
            else:
                logger.warning(f"⚠️ Payment failed with code: {result_code}")
                return False, None
        
        except Exception as e:
            logger.error(f"❌ Callback validation error: {e}")
            return False, None


class AirtelMoneyProcessor:
    """Handle Airtel Money payments (Uganda, Tanzania, DRC, etc)"""
    
    def __init__(self,
                 client_id: str,
                 client_secret: str,
                 merchant_id: str,
                 environment: str = "sandbox"):
        """
        Initialize Airtel Money processor
        
        Args:
            client_id: Airtel API client ID
            client_secret: Airtel API client secret
            merchant_id: Your merchant ID
            environment: 'sandbox' or 'production'
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.merchant_id = merchant_id
        self.environment = environment
        
        self.auth_url = "https://sandbox.airtel.africa/auth/oauth2/token"
        self.payment_url = "https://sandbox.airtel.africa/merchant/v1/payments/"
        
        if environment == "production":
            self.auth_url = "https://api.airtel.africa/auth/oauth2/token"
            self.payment_url = "https://api.airtel.africa/merchant/v1/payments/"
        
        self.access_token = None
    
    def get_access_token(self) -> str:
        """Get Airtel Money access token"""
        try:
            headers = {
                "Content-Type": "application/x-www-form-urlencoded"
            }
            
            data = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "client_credentials"
            }
            
            response = requests.post(self.auth_url, headers=headers, data=data, timeout=10)
            response.raise_for_status()
            
            self.access_token = response.json().get('access_token')
            logger.info("✅ Airtel Money access token obtained")
            return self.access_token
        
        except Exception as e:
            logger.error(f"❌ Airtel Money token error: {e}")
            raise
    
    def charge_customer(self,
                       phone_number: str,
                       amount: float,
                       reference: str,
                       narration: str = "Trading Bot Subscription") -> Dict:
        """
        Charge customer via Airtel Money
        
        Args:
            phone_number: Customer's phone number
            amount: Amount to charge
            reference: Unique transaction reference
            narration: Transaction description
            
        Returns:
            Transaction response
        """
        try:
            if not self.access_token:
                self.get_access_token()
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "reference": reference,
                "subscriber": {
                    "country": "UG",  # Uganda
                    "currency": "UGX",
                    "msisdn": phone_number
                },
                "transaction": {
                    "amount": amount,
                    "country": "UG",
                    "currency": "UGX",
                    "id": reference,
                    "type": "MerchantPayment"
                },
                "merchant": {
                    "consumerId": self.merchant_id,
                    "feesIncluded": False
                },
                "narration": narration
            }
            
            response = requests.post(
                f"{self.payment_url}",
                json=payload,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"✅ Airtel charge initiated: {reference}")
            return result
        
        except Exception as e:
            logger.error(f"❌ Airtel Money charge failed: {e}")
            return {"success": False, "error": str(e)}


# Unified payment gateway supporting multiple methods
class UnifiedPaymentGateway:
    """Support multiple payment methods: M-Pesa, Airtel, Stripe, etc."""
    
    def __init__(self, config: Dict):
        """
        Initialize gateway with payment providers
        
        Config example:
        {
            "mpesa": {
                "consumer_key": "...",
                "consumer_secret": "...",
                "business_shortcode": "...",
                "passkey": "..."
            },
            "airtel": {
                "client_id": "...",
                "client_secret": "...",
                "merchant_id": "..."
            },
            "stripe": {
                "api_key": "..."
            }
        }
        """
        self.config = config
        self.providers = {}
        
        # Initialize M-Pesa
        if "mpesa" in config:
            self.providers["mpesa"] = MpesaPaymentProcessor(**config["mpesa"])
        
        # Initialize Airtel Money
        if "airtel" in config:
            self.providers["airtel"] = AirtelMoneyProcessor(**config["airtel"])
        
        # Initialize Stripe (if needed)
        if "stripe" in config:
            import stripe
            stripe.api_key = config["stripe"]["api_key"]
            self.providers["stripe"] = "stripe"
    
    def charge(self, 
               provider: str,
               phone_number: str,
               amount: int,
               account_reference: str) -> Dict:
        """
        Charge customer using specified provider
        
        Args:
            provider: 'mpesa', 'airtel', or 'stripe'
            phone_number: Customer phone
            amount: Amount to charge
            account_reference: Subscription ID or user ID
            
        Returns:
            Payment response
        """
        if provider == "mpesa":
            return self.providers["mpesa"].initiate_stk_push(
                phone_number, amount, account_reference
            )
        elif provider == "airtel":
            return self.providers["airtel"].charge_customer(
                phone_number, amount, account_reference
            )
        elif provider == "stripe":
            # Use Stripe API
            import stripe
            return stripe.Charge.create(
                amount=amount,
                currency="usd",
                source="tok_visa",  # Token from frontend
                description=f"Trading Bot - {account_reference}"
            )
        else:
            return {"success": False, "error": f"Unknown provider: {provider}"}


if __name__ == "__main__":
    # Example usage
    config = {
        "mpesa": {
            "consumer_key": "YOUR_CONSUMER_KEY",
            "consumer_secret": "YOUR_CONSUMER_SECRET",
            "business_shortcode": "174379",
            "passkey": "YOUR_PASSKEY",
            "environment": "sandbox"
        }
    }
    
    gateway = UnifiedPaymentGateway(config)
    
    # Initiate payment
    result = gateway.charge(
        provider="mpesa",
        phone_number="254712345678",
        amount=4900,  # KES 49.00 (Pro subscription)
        account_reference="user_123_subscription"
    )
    
    print(result)
