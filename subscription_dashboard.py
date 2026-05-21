"""
Web Dashboard for Trading Bot Subscriptions
Simple Flask app for managing subscriptions and viewing status
"""

from flask import Flask, render_template_string, request, jsonify
from datetime import datetime
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from trading_bot.subscription import (
    get_license_manager,
    PlanTier,
    PLANS,
    get_plan
)

app = Flask(__name__)

# HTML Template
DASHBOARD_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Trading Bot Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }
        
        header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .status-box {
            background: white;
            border-radius: 10px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .status-item {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        
        .status-item label {
            display: block;
            font-size: 0.9em;
            color: #666;
            margin-bottom: 5px;
        }
        
        .status-item .value {
            font-size: 1.4em;
            font-weight: bold;
            color: #333;
        }
        
        .plans-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .plan-card {
            background: white;
            border-radius: 10px;
            padding: 25px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
            position: relative;
        }
        
        .plan-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        }
        
        .plan-card.current {
            border: 3px solid #667eea;
            background: #f0f4ff;
        }
        
        .plan-name {
            font-size: 1.3em;
            font-weight: bold;
            margin-bottom: 10px;
            color: #333;
        }
        
        .plan-price {
            font-size: 1.8em;
            color: #667eea;
            margin-bottom: 10px;
        }
        
        .plan-price .period {
            font-size: 0.7em;
            color: #666;
        }
        
        .plan-features {
            list-style: none;
            margin-bottom: 20px;
            font-size: 0.95em;
        }
        
        .plan-features li {
            padding: 8px 0;
            border-bottom: 1px solid #eee;
            color: #555;
        }
        
        .plan-features li:before {
            content: "✓ ";
            color: #667eea;
            font-weight: bold;
            margin-right: 8px;
        }
        
        .plan-features li.disabled {
            opacity: 0.5;
        }
        
        .plan-features li.disabled:before {
            content: "✗ ";
            color: #ccc;
        }
        
        .btn {
            display: inline-block;
            padding: 12px 24px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1em;
            transition: all 0.3s;
            text-decoration: none;
        }
        
        .btn-primary {
            background: #667eea;
            color: white;
        }
        
        .btn-primary:hover {
            background: #5568d3;
        }
        
        .btn-secondary {
            background: #e9ecef;
            color: #333;
        }
        
        .btn-secondary:hover {
            background: #dee2e6;
        }
        
        .btn-current {
            background: #28a745;
            color: white;
        }
        
        .badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            margin-bottom: 15px;
        }
        
        .badge-trial {
            background: #fff3cd;
            color: #856404;
        }
        
        .badge-active {
            background: #d4edda;
            color: #155724;
        }
        
        .trial-warning {
            background: #fff3cd;
            border: 1px solid #ffc107;
            color: #856404;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        
        footer {
            text-align: center;
            color: white;
            margin-top: 40px;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📈 Trading Bot</h1>
            <p>Subscription & Licensing Dashboard</p>
        </header>
        
        <div class="status-box">
            <h2>Your Subscription</h2>
            
            {% if status.is_trial %}
            <div class="trial-warning">
                ⏰ You're in trial mode ({{ status.days_remaining }} days remaining)
            </div>
            {% endif %}
            
            <div class="status-grid">
                <div class="status-item">
                    <label>Current Plan</label>
                    <div class="value">{{ status.plan|upper }}</div>
                </div>
                <div class="status-item">
                    <label>Status</label>
                    <div class="value">
                        {% if status.is_active %}
                        <span style="color: #28a745;">✓ Active</span>
                        {% else %}
                        <span style="color: #dc3545;">✗ Inactive</span>
                        {% endif %}
                    </div>
                </div>
                <div class="status-item">
                    <label>Days Remaining</label>
                    <div class="value">{{ status.days_remaining }}</div>
                </div>
                <div class="status-item">
                    <label>Auto-Renewal</label>
                    <div class="value">
                        {% if status.auto_renew %}
                        Enabled
                        {% else %}
                        Disabled
                        {% endif %}
                    </div>
                </div>
                <div class="status-item">
                    <label>Support Level</label>
                    <div class="value">{{ status.support_level|title }}</div>
                </div>
                <div class="status-item">
                    <label>Auto Trading</label>
                    <div class="value">
                        {% if status.auto_trading %}
                        ✓ Enabled
                        {% else %}
                        ✗ Disabled
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="status-box">
            <h2>Available Plans</h2>
            <p style="color: #666; margin-bottom: 20px;">Click upgrade to change your subscription</p>
            
            <div class="plans-grid">
                {% for plan in plans %}
                <div class="plan-card {% if plan.id == status.plan %}current{% endif %}">
                    {% if plan.id == status.plan %}
                    <div class="badge badge-active">Your Current Plan</div>
                    {% endif %}
                    
                    <div class="plan-name">{{ plan.name }}</div>
                    
                    <div class="plan-price">
                        ${{ plan.price }}
                        <span class="period">/{{ plan.period }}</span>
                    </div>
                    
                    <ul class="plan-features">
                        {% for feature, value in plan.features.items() %}
                        <li {% if not value %}class="disabled"{% endif %}>
                            {{ feature }}
                        </li>
                        {% endfor %}
                    </ul>
                    
                    {% if plan.id == status.plan %}
                    <button class="btn btn-current">Current Plan</button>
                    {% else %}
                    <button class="btn btn-primary" onclick="upgrade('{{ plan.id }}')">
                        Upgrade
                    </button>
                    {% endif %}
                </div>
                {% endfor %}
            </div>
        </div>
        
        <footer>
            <p>© 2026 Trading Bot • All plans include 7-day free trial • Cancel anytime</p>
        </footer>
    </div>
    
    <script>
        function upgrade(plan) {
            alert(`Redirecting to checkout for ${plan} plan...`);
            // In production: window.location.href = `/checkout?plan=${plan}`;
        }
    </script>
</body>
</html>
'''

@app.route('/')
def dashboard():
    """Main dashboard"""
    manager = get_license_manager()
    subscription = manager.get_subscription()
    status = manager.get_status()
    
    # Prepare plans for display
    plans = [
        {
            'id': 'free',
            'name': 'Free',
            'price': '$0',
            'period': 'forever',
            'features': {
                'Signal Detection': True,
                'Auto Trading': False,
                'Email Alerts': False,
                'Trade History': False,
                'Backtesting': False,
                'Support': False,
            }
        },
        {
            'id': 'pro',
            'name': 'Pro',
            'price': '$49',
            'period': 'month',
            'features': {
                'Signal Detection': True,
                'Auto Trading': True,
                'Email Alerts': True,
                'Trade History': True,
                'Backtesting': True,
                'Priority Support': False,
            }
        },
        {
            'id': 'enterprise',
            'name': 'Enterprise',
            'price': '$199',
            'period': 'month',
            'features': {
                'Signal Detection': True,
                'Auto Trading': True,
                'Email Alerts': True,
                'Trade History': True,
                'Backtesting': True,
                'Priority Support': True,
            }
        },
        {
            'id': 'desktop',
            'name': 'Desktop App',
            'price': '$299',
            'period': 'one-time',
            'features': {
                'Signal Detection': True,
                'Auto Trading': True,
                'Offline Mode': True,
                'Local Database': True,
                'Backtesting': True,
                'Lifetime Updates': False,
            }
        },
    ]
    
    return render_template_string(
        DASHBOARD_HTML,
        status=status,
        plans=plans
    )

@app.route('/api/status')
def api_status():
    """API endpoint for subscription status"""
    manager = get_license_manager()
    return jsonify(manager.get_status())

@app.route('/api/activate', methods=['POST'])
def api_activate():
    """API endpoint to activate license"""
    data = request.get_json()
    manager = get_license_manager()
    
    try:
        plan_tier = PlanTier[data.get('plan', 'FREE').upper()]
        success = manager.activate_license(
            license_key=data.get('license_key', 'temp'),
            user_id=data.get('user_id', 'user'),
            plan_tier=plan_tier,
            billing_cycle=data.get('billing_cycle', 'monthly')
        )
        
        if success:
            return jsonify({'success': True, 'message': 'License activated'})
        else:
            return jsonify({'success': False, 'message': 'Failed to activate license'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

if __name__ == '__main__':
    print("\n" + "="*70)
    print("Trading Bot - Subscription Dashboard")
    print("="*70)
    print("\nServer running at: http://localhost:5000")
    print("Open your browser and navigate to the URL above")
    print("\nPress Ctrl+C to stop the server\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
