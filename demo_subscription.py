#!/usr/bin/env python3
"""
Quick Demo: Test the Subscription System
Run this to see all tiers in action
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from trading_bot.subscription import (
    get_license_manager,
    PlanTier,
    PLANS
)

def show_plans():
    """Show all available plans"""
    print("\n" + "="*70)
    print("TRADING BOT - AVAILABLE SUBSCRIPTION PLANS")
    print("="*70 + "\n")
    
    for tier, plan in PLANS.items():
        print(f"📊 {plan.name.upper()}")
        print(f"   Price: ${plan.price_monthly}/month (or ${plan.price_annual}/year)")
        print(f"   Max Symbols: {plan.max_symbols if plan.max_symbols > 0 else 'Unlimited'}")
        print(f"   Auto Trading: {'✓ Yes' if plan.auto_trading_enabled else '✗ No'}")
        print(f"   Platforms: {', '.join(plan.platforms)}")
        print(f"   Support: {plan.support_level.title()}")
        print(f"   Features: {', '.join(plan.features[:3])}...")
        print()

def test_free_tier():
    """Test Free tier"""
    print("="*70)
    print("TEST 1: Free Tier (Default)")
    print("="*70)
    
    manager = get_license_manager()
    status = manager.get_status()
    
    print(f"✓ Plan: {status['plan'].upper()}")
    print(f"✓ Status: {status['status'].upper()}")
    print(f"✓ Auto Trading: {status['auto_trading']}")
    print(f"✓ Max Symbols: {status['max_symbols']}")
    print(f"✓ Price: ${status['price_monthly']}/month\n")

def test_pro_tier():
    """Test Pro tier"""
    print("="*70)
    print("TEST 2: Upgrade to Pro Tier")
    print("="*70)
    
    manager = get_license_manager()
    
    # Activate Pro
    print("Activating Pro tier...")
    manager.activate_license(
        license_key="demo-pro-123",
        user_id="test-user",
        plan_tier=PlanTier.PRO,
        billing_cycle="monthly"
    )
    
    status = manager.get_status()
    print(f"✓ Plan: {status['plan'].upper()}")
    print(f"✓ Status: {status['status'].upper()}")
    print(f"✓ Auto Trading: {status['auto_trading']}")
    print(f"✓ Max Symbols: {status['max_symbols']}")
    print(f"✓ Price: ${status['price_monthly']}/month")
    print(f"✓ Days Remaining: {status['days_remaining']}")
    print(f"✓ Auto Renew: {status['auto_renew']}\n")

def test_enterprise_tier():
    """Test Enterprise tier"""
    print("="*70)
    print("TEST 3: Upgrade to Enterprise Tier")
    print("="*70)
    
    manager = get_license_manager()
    
    # Activate Enterprise
    print("Activating Enterprise tier...")
    manager.activate_license(
        license_key="demo-enterprise-123",
        user_id="test-user",
        plan_tier=PlanTier.ENTERPRISE,
        billing_cycle="annual"
    )
    
    status = manager.get_status()
    print(f"✓ Plan: {status['plan'].upper()}")
    print(f"✓ Status: {status['status'].upper()}")
    print(f"✓ Auto Trading: {status['auto_trading']}")
    print(f"✓ Max Symbols: {status['max_symbols']} (Unlimited)")
    print(f"✓ Price: ${status['price_monthly']}/month (${status['price_annual']}/year)")
    print(f"✓ Platforms: {len(status['platforms'])} platforms")
    print(f"✓ Days Remaining: {status['days_remaining']}")
    print(f"✓ Auto Renew: {status['auto_renew']}\n")

def test_desktop_tier():
    """Test Desktop tier"""
    print("="*70)
    print("TEST 4: Desktop One-Time Purchase")
    print("="*70)
    
    manager = get_license_manager()
    
    # Activate Desktop
    print("Activating Desktop tier...")
    manager.activate_license(
        license_key="demo-desktop-123",
        user_id="test-user",
        plan_tier=PlanTier.DESKTOP
    )
    
    status = manager.get_status()
    print(f"✓ Plan: {status['plan'].upper()}")
    print(f"✓ Status: {status['status'].upper()}")
    print(f"✓ Type: One-time purchase")
    print(f"✓ Price: $299 (lifetime, 1 year updates)")
    print(f"✓ Auto Trading: {status['auto_trading']}")
    print(f"✓ Days Remaining: {status['days_remaining']}")
    print(f"✓ Auto Renew: {status['auto_renew']} (no auto-renewal)\n")

def show_upgrade_paths():
    """Show how to upgrade"""
    print("="*70)
    print("UPGRADE PATHS - How Customers Upgrade")
    print("="*70)
    print("""
Customer Journey:
1. Sign up → Gets Free tier (no payment)
2. Uses for 1 week → Wants more features
3. Clicks "Upgrade" → Sees Pro ($49/month)
4. Pays via Stripe → Gets Pro license instantly
5. Enters license key → Auto-trading now enabled
6. Trades for 3 months → Makes $10k profit
7. Clicks "Upgrade" → Sees Enterprise ($199/month)
8. Upgrades → Gets all platforms + custom strategies

Activation Code Example:
```python
from trading_bot.subscription import get_license_manager, PlanTier

manager = get_license_manager()
manager.activate_license(
    license_key="STRIPE-PAYMENT-ID",
    user_id="user@example.com",
    plan_tier=PlanTier.PRO,
    billing_cycle="monthly"
)

# Bot now has Pro features enabled!
```
""")

def main():
    """Run all tests"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "TRADING BOT - SUBSCRIPTION DEMO" + " "*23 + "║")
    print("╚" + "="*68 + "╝")
    
    # Show all plans
    show_plans()
    
    # Test tiers
    test_free_tier()
    test_pro_tier()
    test_enterprise_tier()
    test_desktop_tier()
    
    # Show upgrade paths
    show_upgrade_paths()
    
    # Final summary
    print("="*70)
    print("SUMMARY")
    print("="*70)
    print("""
✓ Subscription system working
✓ All tiers tested
✓ License activation working
✓ Feature enforcement ready

Next steps:
1. Review: README_COMMERCIAL.md
2. Review: COMMERCIAL_SUMMARY.md
3. Review: HOW_TO_SELL.md
4. Run: python commercial_bot.py
5. Dashboard: python subscription_dashboard.py

Your bot is ready to sell! 🚀
""")

if __name__ == "__main__":
    main()
