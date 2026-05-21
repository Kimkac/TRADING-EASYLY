"""
License and subscription enforcement
Validates user permissions and enforces limits
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional
from .models import Subscription, SubscriptionPlan, PlanTier, PLANS, get_plan

class LicenseManager:
    """Manages licenses and subscriptions"""
    
    def __init__(self, storage_dir: str = None):
        """Initialize license manager"""
        self.storage_dir = Path(storage_dir or "~/.trading-bot").expanduser()
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.license_file = self.storage_dir / "license.json"
        self.usage_file = self.storage_dir / "usage.json"
    
    def activate_license(self, license_key: str, user_id: str, plan_tier: PlanTier, 
                        billing_cycle: str = "monthly") -> bool:
        """Activate a license for user"""
        try:
            plan = get_plan(plan_tier)
            
            if plan_tier == PlanTier.DESKTOP:
                # Desktop: one-time license
                end_date = datetime.now() + timedelta(days=365)
                auto_renew = False
            else:
                # Cloud/SaaS: recurring
                if billing_cycle.lower() == "annual":
                    end_date = datetime.now() + timedelta(days=365)
                else:
                    end_date = datetime.now() + timedelta(days=30)
                auto_renew = True
            
            subscription = Subscription(
                user_id=user_id,
                plan=plan,
                status="active",
                start_date=datetime.now(),
                end_date=end_date,
                auto_renew=auto_renew,
                payment_method="stripe",  # Default
                billing_cycle=billing_cycle
            )
            
            # Save license
            license_data = {
                'user_id': user_id,
                'license_key': license_key,
                'plan': subscription.plan.tier.value,
                'status': subscription.status,
                'start_date': subscription.start_date.isoformat(),
                'end_date': subscription.end_date.isoformat(),
                'auto_renew': subscription.auto_renew,
                'billing_cycle': billing_cycle,
                'activated_at': datetime.now().isoformat()
            }
            
            with open(self.license_file, 'w') as f:
                json.dump(license_data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"License activation failed: {e}")
            return False
    
    def get_subscription(self) -> Optional[Subscription]:
        """Get current subscription"""
        try:
            if not self.license_file.exists():
                # Return default free subscription
                return self._create_free_subscription()
            
            with open(self.license_file, 'r') as f:
                data = json.load(f)
            
            plan = get_plan(PlanTier(data['plan']))
            subscription = Subscription(
                user_id=data.get('user_id', 'default'),
                plan=plan,
                status=data['status'],
                start_date=datetime.fromisoformat(data['start_date']),
                end_date=datetime.fromisoformat(data['end_date']),
                auto_renew=data.get('auto_renew', False),
                payment_method=data.get('payment_method', 'stripe'),
                billing_cycle=data.get('billing_cycle', 'monthly')
            )
            
            # Check if expired
            if subscription.end_date < datetime.now():
                subscription.status = "expired"
            
            return subscription
        except Exception as e:
            print(f"Failed to load subscription: {e}")
            return self._create_free_subscription()
    
    def _create_free_subscription(self) -> Subscription:
        """Create default free subscription"""
        plan = get_plan(PlanTier.FREE)
        return Subscription(
            user_id="guest",
            plan=plan,
            status="active",
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=999999),
            auto_renew=False,
            payment_method="none",
            billing_cycle="monthly"
        )
    
    def check_feature(self, feature: str) -> bool:
        """Check if feature is available"""
        subscription = self.get_subscription()
        if not subscription or not subscription.is_active():
            return False
        return feature in subscription.plan.features
    
    def check_api_limit(self) -> bool:
        """Check if API limit exceeded for today"""
        subscription = self.get_subscription()
        if not subscription or not subscription.is_active():
            return False
        
        # Load usage
        usage = self._load_usage()
        today = datetime.now().date().isoformat()
        
        if today not in usage:
            usage[today] = 0
        
        limit = subscription.plan.api_rate_limit
        if limit == 0:  # Unlimited
            return True
        
        return usage[today] < limit
    
    def increment_api_usage(self):
        """Increment API usage counter"""
        usage = self._load_usage()
        today = datetime.now().date().isoformat()
        
        if today not in usage:
            usage[today] = 0
        
        usage[today] += 1
        self._save_usage(usage)
    
    def _load_usage(self) -> Dict[str, int]:
        """Load usage data"""
        try:
            if self.usage_file.exists():
                with open(self.usage_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return {}
    
    def _save_usage(self, usage: Dict[str, int]):
        """Save usage data"""
        try:
            with open(self.usage_file, 'w') as f:
                json.dump(usage, f, indent=2)
        except Exception as e:
            print(f"Failed to save usage: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get subscription status"""
        subscription = self.get_subscription()
        
        if not subscription:
            return {
                'status': 'inactive',
                'plan': 'none',
                'message': 'No active subscription'
            }
        
        return {
            'status': subscription.status,
            'plan': subscription.plan.tier.value,
            'is_active': subscription.is_active(),
            'is_trial': subscription.is_trial(),
            'days_remaining': subscription.days_remaining(),
            'auto_renew': subscription.auto_renew,
            'max_symbols': subscription.plan.max_symbols,
            'auto_trading': subscription.plan.auto_trading_enabled,
            'platforms': subscription.plan.platforms,
            'support_level': subscription.plan.support_level,
            'price_monthly': subscription.plan.price_monthly,
            'price_annual': subscription.plan.price_annual,
        }

# Global license manager
_license_manager = None

def get_license_manager() -> LicenseManager:
    """Get global license manager"""
    global _license_manager
    if _license_manager is None:
        _license_manager = LicenseManager()
    return _license_manager

def enforce_api_limit() -> bool:
    """Check if API call is allowed (rate limiting)"""
    manager = get_license_manager()
    
    if not manager.check_api_limit():
        raise PermissionError(f"API rate limit exceeded for today")
    
    manager.increment_api_usage()
    return True

def require_feature(feature: str):
    """Decorator: require a feature"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            manager = get_license_manager()
            if not manager.check_feature(feature):
                raise PermissionError(f"Feature '{feature}' not available in your plan")
            return func(*args, **kwargs)
        return wrapper
    return decorator

def require_auto_trading():
    """Decorator: require auto trading feature"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            manager = get_license_manager()
            subscription = manager.get_subscription()
            
            if not subscription or not subscription.plan.auto_trading_enabled:
                raise PermissionError("Auto-trading not enabled in your plan. Upgrade to Pro or Enterprise.")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator
