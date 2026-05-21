"""
Subscription and licensing module
"""

from .models import (
    PlanTier,
    BillingCycle,
    SubscriptionPlan,
    Subscription,
    PLANS,
    get_plan,
    is_feature_allowed,
    can_trade_symbols,
    get_api_rate_for_day
)

from .license import (
    LicenseManager,
    get_license_manager,
    enforce_api_limit,
    require_feature,
    require_auto_trading
)

__all__ = [
    'PlanTier',
    'BillingCycle',
    'SubscriptionPlan',
    'Subscription',
    'PLANS',
    'get_plan',
    'is_feature_allowed',
    'can_trade_symbols',
    'get_api_rate_for_day',
    'LicenseManager',
    'get_license_manager',
    'enforce_api_limit',
    'require_feature',
    'require_auto_trading',
]
