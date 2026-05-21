"""
Subscription and Licensing Models
Handles user tiers, feature limits, and permissions
"""

from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Dict, Any
import json

class PlanTier(Enum):
    """Subscription tiers"""
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"
    DESKTOP = "desktop"
    CLOUD_PRO = "cloud_pro"
    CLOUD_ENTERPRISE = "cloud_enterprise"

class BillingCycle(Enum):
    """Billing options"""
    MONTHLY = "monthly"
    ANNUAL = "annual"
    ONE_TIME = "one_time"

@dataclass
class SubscriptionPlan:
    """Subscription plan definition"""
    tier: PlanTier
    name: str
    price_monthly: float
    price_annual: float
    billing_cycle: BillingCycle
    
    # Feature limits
    max_symbols: int  # Max trading symbols
    signal_check_interval: int  # Minutes between signal checks (0 = unlimited)
    auto_trading_enabled: bool
    platforms: List[str]  # List of supported platforms
    api_rate_limit: int  # Requests per day
    backtesting_enabled: bool
    advanced_backtesting: bool
    webhook_enabled: bool
    custom_strategy: bool
    white_label: bool
    
    # Support level
    support_level: str  # "community", "email", "priority"
    support_response_hours: int
    
    # Additional features
    features: List[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'tier': self.tier.value,
            'name': self.name,
            'price_monthly': self.price_monthly,
            'price_annual': self.price_annual,
            'billing_cycle': self.billing_cycle.value,
            'max_symbols': self.max_symbols,
            'signal_check_interval': self.signal_check_interval,
            'auto_trading_enabled': self.auto_trading_enabled,
            'platforms': self.platforms,
            'api_rate_limit': self.api_rate_limit,
            'backtesting_enabled': self.backtesting_enabled,
            'advanced_backtesting': self.advanced_backtesting,
            'webhook_enabled': self.webhook_enabled,
            'custom_strategy': self.custom_strategy,
            'white_label': self.white_label,
            'support_level': self.support_level,
            'support_response_hours': self.support_response_hours,
            'features': self.features or []
        }

@dataclass
class Subscription:
    """User subscription"""
    user_id: str
    plan: SubscriptionPlan
    status: str  # "active", "inactive", "cancelled", "expired"
    start_date: datetime
    end_date: datetime
    auto_renew: bool
    payment_method: str  # "stripe", "paypal", etc.
    billing_cycle: BillingCycle
    
    def is_active(self) -> bool:
        """Check if subscription is active"""
        return (
            self.status == "active" and
            datetime.now() < self.end_date
        )
    
    def days_remaining(self) -> int:
        """Days until subscription expires"""
        delta = self.end_date - datetime.now()
        return max(0, delta.days)
    
    def is_trial(self) -> bool:
        """Check if currently in trial period"""
        trial_end = self.start_date + timedelta(days=7)
        return datetime.now() < trial_end
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'user_id': self.user_id,
            'plan': self.plan.tier.value,
            'status': self.status,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'auto_renew': self.auto_renew,
            'billing_cycle': self.billing_cycle.value,
            'days_remaining': self.days_remaining(),
            'is_trial': self.is_trial()
        }

# Plan Definitions
PLANS = {
    PlanTier.FREE: SubscriptionPlan(
        tier=PlanTier.FREE,
        name="Free",
        price_monthly=0,
        price_annual=0,
        billing_cycle=BillingCycle.MONTHLY,
        max_symbols=1,
        signal_check_interval=60,  # 1 check per hour
        auto_trading_enabled=False,
        platforms=["deriv"],
        api_rate_limit=100,
        backtesting_enabled=False,
        advanced_backtesting=False,
        webhook_enabled=False,
        custom_strategy=False,
        white_label=False,
        support_level="community",
        support_response_hours=0,
        features=["signal_detection", "email_alerts"]
    ),
    
    PlanTier.PRO: SubscriptionPlan(
        tier=PlanTier.PRO,
        name="Pro",
        price_monthly=49,
        price_annual=490,
        billing_cycle=BillingCycle.MONTHLY,
        max_symbols=10,
        signal_check_interval=0,  # Unlimited
        auto_trading_enabled=True,
        platforms=["deriv", "alpaca"],
        api_rate_limit=10000,
        backtesting_enabled=True,
        advanced_backtesting=False,
        webhook_enabled=False,
        custom_strategy=False,
        white_label=False,
        support_level="email",
        support_response_hours=48,
        features=[
            "signal_detection",
            "auto_trading",
            "email_alerts",
            "trade_history",
            "analytics",
            "basic_backtesting"
        ]
    ),
    
    PlanTier.ENTERPRISE: SubscriptionPlan(
        tier=PlanTier.ENTERPRISE,
        name="Enterprise",
        price_monthly=199,
        price_annual=1990,
        billing_cycle=BillingCycle.MONTHLY,
        max_symbols=0,  # Unlimited
        signal_check_interval=0,  # Unlimited
        auto_trading_enabled=True,
        platforms=["deriv", "alpaca", "interactive_brokers", "tradingview"],
        api_rate_limit=0,  # Unlimited
        backtesting_enabled=True,
        advanced_backtesting=True,
        webhook_enabled=True,
        custom_strategy=True,
        white_label=True,
        support_level="priority",
        support_response_hours=4,
        features=[
            "signal_detection",
            "auto_trading",
            "email_alerts",
            "trade_history",
            "analytics",
            "advanced_backtesting",
            "custom_strategies",
            "webhook_support",
            "white_label",
            "api_access",
            "account_manager"
        ]
    ),
    
    PlanTier.DESKTOP: SubscriptionPlan(
        tier=PlanTier.DESKTOP,
        name="Desktop App",
        price_monthly=0,  # One-time: $299
        price_annual=299,  # Represents one-time price
        billing_cycle=BillingCycle.ONE_TIME,
        max_symbols=10,
        signal_check_interval=0,
        auto_trading_enabled=True,
        platforms=["deriv", "alpaca"],
        api_rate_limit=0,  # Unlimited
        backtesting_enabled=True,
        advanced_backtesting=False,
        webhook_enabled=False,
        custom_strategy=False,
        white_label=False,
        support_level="email",
        support_response_hours=48,
        features=[
            "standalone_app",
            "offline_signals",
            "local_database",
            "pro_features",
            "1_year_updates"
        ]
    ),
    
    PlanTier.CLOUD_PRO: SubscriptionPlan(
        tier=PlanTier.CLOUD_PRO,
        name="Cloud Pro",
        price_monthly=99,
        price_annual=990,
        billing_cycle=BillingCycle.MONTHLY,
        max_symbols=10,
        signal_check_interval=0,
        auto_trading_enabled=True,
        platforms=["deriv", "alpaca"],
        api_rate_limit=10000,
        backtesting_enabled=True,
        advanced_backtesting=False,
        webhook_enabled=False,
        custom_strategy=False,
        white_label=False,
        support_level="email",
        support_response_hours=24,
        features=[
            "cloud_hosting",
            "24_7_uptime",
            "99_9_sla",
            "web_dashboard",
            "mobile_alerts",
            "multi_device",
            "auto_backups",
            "pro_features"
        ]
    ),
    
    PlanTier.CLOUD_ENTERPRISE: SubscriptionPlan(
        tier=PlanTier.CLOUD_ENTERPRISE,
        name="Cloud Enterprise",
        price_monthly=299,
        price_annual=2990,
        billing_cycle=BillingCycle.MONTHLY,
        max_symbols=0,  # Unlimited
        signal_check_interval=0,
        auto_trading_enabled=True,
        platforms=["deriv", "alpaca", "interactive_brokers", "tradingview"],
        api_rate_limit=0,
        backtesting_enabled=True,
        advanced_backtesting=True,
        webhook_enabled=True,
        custom_strategy=True,
        white_label=True,
        support_level="priority",
        support_response_hours=2,
        features=[
            "cloud_hosting",
            "24_7_uptime",
            "99_9_sla",
            "web_dashboard",
            "mobile_alerts",
            "multi_device",
            "auto_backups",
            "enterprise_features",
            "white_label_option",
            "api_access",
            "dedicated_account_manager"
        ]
    ),
}

def get_plan(tier: PlanTier) -> SubscriptionPlan:
    """Get plan by tier"""
    return PLANS.get(tier, PLANS[PlanTier.FREE])

def is_feature_allowed(subscription: Subscription, feature: str) -> bool:
    """Check if feature is allowed for subscription"""
    return feature in subscription.plan.features

def can_trade_symbols(subscription: Subscription, symbol_count: int) -> bool:
    """Check if user can trade given number of symbols"""
    if subscription.plan.max_symbols == 0:
        return True  # Unlimited
    return symbol_count <= subscription.plan.max_symbols

def get_api_rate_for_day(subscription: Subscription) -> int:
    """Get API rate limit for the day"""
    if subscription.plan.api_rate_limit == 0:
        return 999999  # Unlimited
    return subscription.plan.api_rate_limit
