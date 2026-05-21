# Commercial Bot Setup & Deployment

## Quick Start

### 1. Launch Dashboard (View Plans & Manage Subscriptions)
```bash
python subscription_dashboard.py
```
Open browser: http://localhost:5000

### 2. Run Commercial Bot (With Subscription Enforcement)
```bash
python commercial_bot.py
```

### 3. Run Signal Bot (Without Auto-Trading)
```bash
python signal_bot.py
```

---

## For Developers / Selling the Bot

### Architecture Overview

```
Trading Bot (Subscription Model)
├── Free Tier
│   ├── Signal detection (1/hour limit)
│   ├── Deriv platform only
│   └── Community support
├── Pro Tier ($49/month)
│   ├── Unlimited signals
│   ├── Auto-trading (10 symbols max)
│   ├── Deriv + Alpaca
│   └── Email support
├── Enterprise ($199/month)
│   ├── Everything in Pro
│   ├── All platforms (IB, TradingView, etc.)
│   ├── Custom strategies
│   └── Priority support
├── Desktop App ($299 one-time)
│   └── Standalone .exe (PyInstaller)
└── Cloud Managed ($99-299/month)
    ├── 24/7 bot running on servers
    ├── Web dashboard + mobile alerts
    └── 99.9% SLA
```

### Implementation Details

#### 1. License System
```python
from trading_bot.subscription import get_license_manager, PlanTier

manager = get_license_manager()

# Activate license
manager.activate_license(
    license_key="abc123xyz",
    user_id="user@example.com",
    plan_tier=PlanTier.PRO,
    billing_cycle="monthly"
)

# Check status
status = manager.get_status()
print(status)
# Output: {
#     'status': 'active',
#     'plan': 'pro',
#     'is_active': True,
#     'days_remaining': 29,
#     'auto_trading': True
# }
```

#### 2. Feature Enforcement
```python
from trading_bot.subscription import require_feature, require_auto_trading

# Protect signal detection
@require_feature("signal_detection")
def my_trading_function():
    # Throws PermissionError if feature not in plan
    pass

# Protect auto-trading
@require_auto_trading()
def execute_trade():
    # Only runs for Pro+ plans
    pass
```

#### 3. Rate Limiting
```python
from trading_bot.subscription import enforce_api_limit

# Check API limit before each request
enforce_api_limit()  # Throws PermissionError if limit exceeded

# API limits by plan:
# - Free: 100 requests/day
# - Pro: 10,000 requests/day
# - Enterprise: Unlimited
```

#### 4. License File Format
License stored at: `~/.trading-bot/license.json`
```json
{
  "user_id": "user@example.com",
  "license_key": "abc123xyz",
  "plan": "pro",
  "status": "active",
  "start_date": "2026-05-20T10:00:00",
  "end_date": "2026-06-20T10:00:00",
  "auto_renew": true,
  "billing_cycle": "monthly",
  "activated_at": "2026-05-20T10:00:00"
}
```

---

## Deployment Options

### Option 1: Cloud SaaS (Recommended for Revenue)

**Setup:**
```
Your Server (AWS/Azure/Digital Ocean)
├── Flask web app (subscription dashboard)
├── Database (PostgreSQL - store licenses)
├── Payment processor (Stripe integration)
└── Trading bot runners (one per user)
```

**Monthly Revenue:**
- 100 Pro users @ $49 = $4,900/mo
- 50 Enterprise users @ $199 = $9,950/mo
- **Total: ~$15k/month recurring**

**Steps:**
1. Set up Stripe account for payments
2. Deploy Flask app to production
3. Create database schema for users/licenses
4. Implement payment webhook handlers
5. Auto-provision bot instances per user

---

### Option 2: Desktop App (Single Install)

**Setup:**
```
PyInstaller → .exe installer
├── Embeds Python + bot code
├── Local license storage
├── Single-machine license key
└── Auto-update capability
```

**Steps:**
1. Install PyInstaller
2. Build executable
3. Create installer with Inno Setup
4. Generate unique license keys per download
5. Host on website with payment processing

```bash
# Build standalone exe
pyinstaller --onefile commercial_bot.py \
    --add-data "src:trading_bot" \
    --icon=bot-icon.ico
```

---

### Option 3: White-Label for Brokers

**Setup:**
```
Your infrastructure
├── Customizable branding
├── Broker-specific strategy templates
├── API integrations (Alpaca, IB, etc.)
└── Broker handles payments/users
```

**Revenue Model:**
- Charge brokers $5-20/user/month
- Or revenue share (20-30% of subscription fees)
- Broker gets own branded bot with their platform integration

---

## Customer Journey

### Free User → Pro User

1. **Discovery**: User finds your website, sees $0 price
2. **Signup**: Register with email, get Free tier automatically
3. **Signal Detection**: Sees signals working 1x/hour
4. **Upgrade Prompt**: After 5 signals, offer "Upgrade to Pro for unlimited signals + auto-trading"
5. **Checkout**: Stripe payment, instant license generation
6. **Activation**: Dashboard shows "Upgrade successful"
7. **Auto-Trading**: Commercial bot now places real trades

### Enterprise Prospect

1. **High-Volume Trader**: Tries bot, realizes 10-symbol limit too restrictive
2. **Upgrade Request**: Contacts support asking about higher tier
3. **Sales Call**: 15-min demo of Enterprise features (custom strategies, priority support, all platforms)
4. **Contract**: Annual payment ($1,990), white-label option for hedge fund
5. **Implementation**: Dedicated account manager, custom API integrations

---

## Pricing Psychology

**Why These Prices Work:**

| Tier | Target User | Price | Value Prop |
|------|-------------|-------|-----------|
| Free | Hobbyists | $0 | Try before buying |
| Pro | Day traders | $49 | $49/mo = passive income from 1-2 winning trades |
| Enterprise | Professionals | $199 | ROI: if bot makes 1% profit, pays for itself |
| Desktop | Privacy-focused | $299 | One-time, total control |

**Annual Discount**: 17% off ($490 for Pro, $1,990 for Enterprise) encourages longer commitment

---

## Monetization Channels

### 1. Subscriptions (Primary)
- Pro: $49/mo → $588/year
- Enterprise: $199/mo → $2,388/year
- Cloud add-ons: +$50/mo

### 2. Desktop App
- One-time purchase: $299
- Premium updates: $49/year after 1st year

### 3. Consulting
- Strategy development: $500-2,000
- Platform integration: $1,000-5,000
- Custom bot training: $200/hour

### 4. White-Label / Licensing
- Per-broker annual: $5,000-50,000
- Revenue share: 20-30%

### 5. Affiliate Commissions
- Broker referrals: 10-20% of signup fees
- VPS hosting (for cloud bot): 5-10% recurring

**Annual Revenue Target** (with 1,000 customers):
- 400 Pro users: $235,200
- 150 Enterprise users: $358,200
- 50 Desktop sales: $14,950
- **Total: ~$608k/year (recurring) from subscriptions alone**

---

## Launch Checklist

### Phase 1 (Week 1-2): MVP
- [ ] Finalize pricing
- [ ] Set up Stripe account
- [ ] Deploy dashboard to production
- [ ] Generate test license keys
- [ ] Create payment webhook handlers

### Phase 2 (Week 3-4): Beta
- [ ] Beta test with 10 users
- [ ] Fix license validation issues
- [ ] Document licensing API
- [ ] Create user onboarding guide

### Phase 3 (Month 2): Launch
- [ ] Public website with pricing page
- [ ] Marketing email campaign
- [ ] Product Hunt launch
- [ ] Reddit AMAs in finance/trading communities

### Phase 4 (Month 3-6): Growth
- [ ] Desktop app release
- [ ] Cloud version launch
- [ ] Broker partnerships
- [ ] Advanced features (backtesting optimization, AI strategy, etc.)

---

## Support & Documentation

### Customer Support Tiers

**Free**: Community (Discord/GitHub)
**Pro**: Email support, 24-48 hour response
**Enterprise**: Priority email + Discord, 4-hour response + monthly calls
**Cloud**: Phone support available, dedicated account manager

### Knowledge Base Topics

1. How to activate your license
2. Connecting your broker account
3. Backtesting your strategy
4. Understanding trading signals
5. Upgrading/downgrading plans
6. Troubleshooting common errors
7. Performance optimization
8. Risk management best practices

---

## Questions?

Review:
- `SUBSCRIPTION_PLANS.md` - Detailed plan features
- `src/trading_bot/subscription/models.py` - Subscription data models
- `src/trading_bot/subscription/license.py` - License enforcement
- `subscription_dashboard.py` - Web dashboard code
- `commercial_bot.py` - Bot with subscription checks

**Next Steps:**
1. Test the dashboard: `python subscription_dashboard.py`
2. Run commercial bot: `python commercial_bot.py`
3. Try activating a license: See "License System" section above
