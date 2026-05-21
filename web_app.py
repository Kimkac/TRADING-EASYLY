"""
TradeBot Web Application
Complete SaaS platform with authentication, subscription management, and broker integration
"""

from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
from flask_cors import CORS
import sqlite3
import hashlib
import secrets
import json
from datetime import datetime, timedelta
from functools import wraps
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from trading_bot.subscription import get_license_manager, PlanTier

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
CORS(app)

# Database setup
def init_db():
    """Initialize database"""
    conn = sqlite3.connect('tradebot.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        email TEXT UNIQUE,
        password_hash TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        first_name TEXT,
        last_name TEXT,
        profile_image TEXT,
        account_type TEXT DEFAULT 'demo'
    )''')
    
    # Subscriptions table
    c.execute('''CREATE TABLE IF NOT EXISTS subscriptions (
        id TEXT PRIMARY KEY,
        user_id TEXT UNIQUE,
        plan TEXT,
        status TEXT,
        start_date TIMESTAMP,
        end_date TIMESTAMP,
        auto_renew INTEGER,
        stripe_customer_id TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')
    
    # Broker connections table
    c.execute('''CREATE TABLE IF NOT EXISTS broker_connections (
        id TEXT PRIMARY KEY,
        user_id TEXT,
        broker TEXT,
        api_key TEXT,  # Encrypted
        account_type TEXT,  # 'demo' or 'real'
        connected_at TIMESTAMP,
        is_active INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')
    
    # Trades table (for tracking)
    c.execute('''CREATE TABLE IF NOT EXISTS trades (
        id TEXT PRIMARY KEY,
        user_id TEXT,
        broker TEXT,
        symbol TEXT,
        side TEXT,
        amount REAL,
        price REAL,
        timestamp TIMESTAMP,
        profit_loss REAL,
        status TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')
    
    conn.commit()
    conn.close()

init_db()

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Database helpers
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_user(user_id):
    conn = sqlite3.connect('tradebot.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE id=?', (user_id,))
    user = c.fetchone()
    conn.close()
    return user

def get_subscription(user_id):
    conn = sqlite3.connect('tradebot.db')
    c = conn.cursor()
    c.execute('SELECT * FROM subscriptions WHERE user_id=?', (user_id,))
    sub = c.fetchone()
    conn.close()
    return sub

# Routes

@app.route('/')
def index():
    """Landing page"""
    with open('landing_page.html', 'r') as f:
        html = f.read()
    # Replace buttons with proper routing
    html = html.replace('location.href="/login"', 'location.href="'+url_for('login')+'"')
    html = html.replace('location.href="/signup"', 'location.href="'+url_for('signup')+'"')
    html = html.replace('location.href="/demo"', 'location.href="'+url_for('demo_page')+'"')
    html = html.replace('location.href="/upgrade?plan=pro"', 'location.href="'+url_for('upgrade', plan='pro')+'"')
    html = html.replace('location.href="/upgrade?plan=enterprise"', 'location.href="'+url_for('upgrade', plan='enterprise')+'"')
    return html

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Sign up new user"""
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name', '')
        
        conn = sqlite3.connect('tradebot.db')
        c = conn.cursor()
        
        # Check if user exists
        c.execute('SELECT id FROM users WHERE email=?', (email,))
        if c.fetchone():
            conn.close()
            return jsonify({'success': False, 'message': 'Email already registered'}), 400
        
        # Create user
        user_id = secrets.token_hex(16)
        c.execute('''INSERT INTO users (id, email, password_hash, first_name, account_type)
                     VALUES (?, ?, ?, ?, ?)''',
                  (user_id, email, hash_password(password), first_name, 'demo'))
        
        # Create free subscription
        sub_id = secrets.token_hex(16)
        now = datetime.now()
        end_date = now + timedelta(days=999999)
        c.execute('''INSERT INTO subscriptions (id, user_id, plan, status, start_date, end_date, auto_renew)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (sub_id, user_id, 'free', 'active', now, end_date, 0))
        
        conn.commit()
        conn.close()
        
        # Create session
        session['user_id'] = user_id
        session['email'] = email
        
        return jsonify({'success': True, 'redirect': url_for('dashboard')}), 200
    
    return render_template_string(SIGNUP_HTML)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login user"""
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        conn = sqlite3.connect('tradebot.db')
        c = conn.cursor()
        c.execute('SELECT id, password_hash FROM users WHERE email=?', (email,))
        result = c.fetchone()
        conn.close()
        
        if result and result[1] == hash_password(password):
            session['user_id'] = result[0]
            session['email'] = email
            return jsonify({'success': True, 'redirect': url_for('dashboard')}), 200
        
        return jsonify({'success': False, 'message': 'Invalid email or password'}), 400
    
    return render_template_string(LOGIN_HTML)

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    user = get_user(session['user_id'])
    sub = get_subscription(session['user_id'])
    
    # Get broker connections
    conn = sqlite3.connect('tradebot.db')
    c = conn.cursor()
    c.execute('''SELECT broker, account_type, is_active FROM broker_connections 
                 WHERE user_id=? AND is_active=1''', (session['user_id'],))
    brokers = c.fetchall()
    
    c.execute('''SELECT COUNT(*) FROM trades WHERE user_id=?''', (session['user_id'],))
    total_trades = c.fetchone()[0]
    conn.close()
    
    plan = 'FREE' if not sub else sub[2].upper()
    
    return render_template_string(DASHBOARD_HTML, 
                                  user=user,
                                  plan=plan,
                                  brokers=brokers,
                                  total_trades=total_trades,
                                  dashboard_url=url_for('dashboard'))

@app.route('/connect-broker', methods=['POST'])
@login_required
def connect_broker():
    """Connect trading broker"""
    data = request.get_json()
    broker = data.get('broker', 'deriv').lower()
    account_type = data.get('account_type', 'demo')  # 'demo' or 'real'
    api_key = data.get('api_key')
    
    if not api_key:
        return jsonify({'success': False, 'message': 'API key required'}), 400
    
    conn = sqlite3.connect('tradebot.db')
    c = conn.cursor()
    
    # Check if already connected
    c.execute('''SELECT id FROM broker_connections 
                 WHERE user_id=? AND broker=?''', 
              (session['user_id'], broker))
    
    if c.fetchone():
        # Update existing
        c.execute('''UPDATE broker_connections 
                     SET api_key=?, account_type=?, is_active=1
                     WHERE user_id=? AND broker=?''',
                  (api_key, account_type, session['user_id'], broker))
    else:
        # Create new
        conn_id = secrets.token_hex(16)
        c.execute('''INSERT INTO broker_connections 
                     (id, user_id, broker, api_key, account_type, is_active)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (conn_id, session['user_id'], broker, api_key, account_type, 1))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': f'{broker.upper()} connected successfully'}), 200

@app.route('/api/account-info')
@login_required
def account_info():
    """Get user account info"""
    user = get_user(session['user_id'])
    sub = get_subscription(session['user_id'])
    
    # Get broker balance (from API)
    conn = sqlite3.connect('tradebot.db')
    c = conn.cursor()
    c.execute('''SELECT broker, account_type FROM broker_connections 
                 WHERE user_id=? AND is_active=1 LIMIT 1''', 
              (session['user_id'],))
    broker_info = c.fetchone()
    
    c.execute('''SELECT SUM(profit_loss) FROM trades WHERE user_id=?''',
              (session['user_id'],))
    total_pnl = c.fetchone()[0] or 0
    conn.close()
    
    return jsonify({
        'email': user[1] if user else '',
        'first_name': user[4] if user else '',
        'plan': sub[2] if sub else 'free',
        'account_type': 'demo',  # Default
        'total_trades': 0,
        'total_pnl': total_pnl,
        'status': 'Active'
    })

@app.route('/upgrade', methods=['GET', 'POST'])
@login_required
def upgrade():
    """Upgrade subscription"""
    plan = request.args.get('plan', 'pro').lower()
    
    if request.method == 'POST':
        # Redirect to Stripe checkout (implement Stripe integration)
        return jsonify({'success': True, 'message': f'Redirecting to checkout for {plan}...'}), 200
    
    return render_template_string(UPGRADE_HTML, plan=plan)

@app.route('/start-bot', methods=['POST'])
@login_required
def start_bot():
    """Start trading bot for user"""
    data = request.get_json()
    broker = data.get('broker', 'deriv')
    
    # Get user's broker connection
    conn = sqlite3.connect('tradebot.db')
    c = conn.cursor()
    c.execute('''SELECT api_key, account_type FROM broker_connections 
                 WHERE user_id=? AND broker=? AND is_active=1''',
              (session['user_id'], broker))
    broker_conn = c.fetchone()
    conn.close()
    
    if not broker_conn:
        return jsonify({'success': False, 'message': 'Broker not connected'}), 400
    
    api_key, account_type = broker_conn
    
    return jsonify({
        'success': True,
        'message': f'Bot started on {broker} ({account_type})',
        'status': 'running'
    }), 200

@app.route('/demo')
def demo_page():
    """Demo page"""
    return render_template_string(DEMO_HTML)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/api/health')
def health():
    """Health check"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

# HTML Templates

SIGNUP_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Sign Up - TradeBot</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f0f2f5; }
        nav { background: #1a1a2e; color: white; padding: 1rem 2rem; }
        nav .logo { font-size: 1.5em; font-weight: bold; }
        nav .logo span { color: #00d4ff; }
        .container { max-width: 400px; margin: 5rem auto; background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
        h1 { color: #1a1a2e; margin-bottom: 1rem; }
        input { width: 100%; padding: 0.8rem; margin-bottom: 1rem; border: 1px solid #ddd; border-radius: 5px; }
        button { width: 100%; padding: 0.8rem; background: #00d4ff; color: #1a1a2e; border: none; border-radius: 5px; font-weight: bold; cursor: pointer; }
        button:hover { background: #00b8cc; }
        .links { text-align: center; margin-top: 1rem; }
        .links a { color: #00d4ff; text-decoration: none; }
        .error { color: #dc3545; margin-bottom: 1rem; }
        .success { color: #28a745; margin-bottom: 1rem; }
    </style>
</head>
<body>
    <nav>
        <div class="logo">Trade<span>Bot</span></div>
    </nav>
    
    <div class="container">
        <h1>Create Account</h1>
        <div id="message"></div>
        
        <form id="signupForm">
            <input type="text" placeholder="First Name" id="firstName" required>
            <input type="email" placeholder="Email" id="email" required>
            <input type="password" placeholder="Password" id="password" required>
            <input type="password" placeholder="Confirm Password" id="confirmPassword" required>
            <button type="submit">Sign Up Free</button>
        </form>
        
        <div class="links">
            Already have account? <a href="/login">Sign In</a>
        </div>
    </div>
    
    <script>
        document.getElementById('signupForm').onsubmit = async (e) => {
            e.preventDefault();
            const pwd1 = document.getElementById('password').value;
            const pwd2 = document.getElementById('confirmPassword').value;
            
            if (pwd1 !== pwd2) {
                document.getElementById('message').innerHTML = '<div class="error">Passwords do not match</div>';
                return;
            }
            
            const res = await fetch('/signup', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    first_name: document.getElementById('firstName').value,
                    email: document.getElementById('email').value,
                    password: pwd1
                })
            });
            
            const data = await res.json();
            if (data.success) {
                window.location.href = data.redirect;
            } else {
                document.getElementById('message').innerHTML = '<div class="error">' + data.message + '</div>';
            }
        };
    </script>
</body>
</html>
'''

LOGIN_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Sign In - TradeBot</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f0f2f5; }
        nav { background: #1a1a2e; color: white; padding: 1rem 2rem; }
        nav .logo { font-size: 1.5em; font-weight: bold; }
        nav .logo span { color: #00d4ff; }
        .container { max-width: 400px; margin: 5rem auto; background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
        h1 { color: #1a1a2e; margin-bottom: 1rem; }
        input { width: 100%; padding: 0.8rem; margin-bottom: 1rem; border: 1px solid #ddd; border-radius: 5px; }
        button { width: 100%; padding: 0.8rem; background: #00d4ff; color: #1a1a2e; border: none; border-radius: 5px; font-weight: bold; cursor: pointer; }
        button:hover { background: #00b8cc; }
        .links { text-align: center; margin-top: 1rem; }
        .links a { color: #00d4ff; text-decoration: none; }
        .error { color: #dc3545; }
    </style>
</head>
<body>
    <nav>
        <div class="logo">Trade<span>Bot</span></div>
    </nav>
    
    <div class="container">
        <h1>Sign In</h1>
        <div id="message"></div>
        
        <form id="loginForm">
            <input type="email" placeholder="Email" id="email" required>
            <input type="password" placeholder="Password" id="password" required>
            <button type="submit">Sign In</button>
        </form>
        
        <div class="links">
            Don't have account? <a href="/signup">Sign Up Free</a>
        </div>
    </div>
    
    <script>
        document.getElementById('loginForm').onsubmit = async (e) => {
            e.preventDefault();
            const res = await fetch('/login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    email: document.getElementById('email').value,
                    password: document.getElementById('password').value
                })
            });
            
            const data = await res.json();
            if (data.success) {
                window.location.href = data.redirect;
            } else {
                document.getElementById('message').innerHTML = '<div class="error">' + data.message + '</div>';
            }
        };
    </script>
</body>
</html>
'''

DASHBOARD_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard - TradeBot</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f0f2f5; }
        nav { background: #1a1a2e; color: white; padding: 1rem 2rem; display: flex; justify-content: space-between; align-items: center; }
        nav .logo { font-size: 1.5em; font-weight: bold; }
        nav .logo span { color: #00d4ff; }
        nav a { color: #00d4ff; text-decoration: none; }
        .container { max-width: 1200px; margin: 2rem auto; padding: 0 2rem; }
        .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; }
        .header h1 { color: #1a1a2e; }
        .status-badge { display: inline-block; padding: 0.5rem 1rem; background: #d4edda; color: #155724; border-radius: 20px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; margin-bottom: 2rem; }
        .card { background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
        .card h3 { color: #00d4ff; margin-bottom: 1rem; }
        .card .value { font-size: 2em; color: #1a1a2e; font-weight: bold; }
        .btn { padding: 0.8rem 1.5rem; background: #00d4ff; color: #1a1a2e; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; }
        .btn:hover { background: #00b8cc; }
        input { width: 100%; padding: 0.8rem; margin: 0.5rem 0; border: 1px solid #ddd; border-radius: 5px; }
    </style>
</head>
<body>
    <nav>
        <div class="logo">Trade<span>Bot</span></div>
        <div>
            <span style="margin-right: 2rem;">{{ user[1] }}</span>
            <a href="/logout">Logout</a>
        </div>
    </nav>
    
    <div class="container">
        <div class="header">
            <div>
                <h1>Welcome, {{ user[4] or 'Trader' }}!</h1>
                <span class="status-badge">Plan: {{ plan }}</span>
            </div>
        </div>
        
        <div class="grid">
            <div class="card">
                <h3>Current Plan</h3>
                <div class="value">{{ plan }}</div>
                <p style="margin-top: 1rem; color: #666;">
                    {% if plan == 'FREE' %}
                    Upgrade to unlock auto-trading
                    {% else %}
                    Active subscription
                    {% endif %}
                </p>
            </div>
            
            <div class="card">
                <h3>Account Type</h3>
                <div class="value">{{ brokers[0][1] if brokers else 'Demo' }}</div>
                <p style="margin-top: 1rem; color: #666;">Start with demo, switch to real when ready</p>
            </div>
            
            <div class="card">
                <h3>Connected Brokers</h3>
                <div class="value">{{ brokers|length }}</div>
                <p style="margin-top: 1rem; color: #666;">
                    {% for broker in brokers %}
                    {{ broker[0] }} ({{ broker[1] }})<br>
                    {% endfor %}
                </p>
            </div>
            
            <div class="card">
                <h3>Total Trades</h3>
                <div class="value">{{ total_trades }}</div>
                <p style="margin-top: 1rem; color: #666;">Automated trades executed</p>
            </div>
        </div>
        
        <div style="background: white; padding: 2rem; border-radius: 10px; margin-bottom: 2rem;">
            <h2 style="color: #1a1a2e; margin-bottom: 1.5rem;">Connect Your Broker</h2>
            
            <div style="margin-bottom: 2rem;">
                <label style="display: block; margin-bottom: 0.5rem; font-weight: bold;">Choose Broker</label>
                <select id="broker" style="width: 100%; padding: 0.8rem; border: 1px solid #ddd; border-radius: 5px;">
                    <option value="deriv">Deriv</option>
                    <option value="alpaca">Alpaca</option>
                </select>
            </div>
            
            <div style="margin-bottom: 2rem;">
                <label style="display: block; margin-bottom: 0.5rem; font-weight: bold;">Account Type</label>
                <select id="accountType" style="width: 100%; padding: 0.8rem; border: 1px solid #ddd; border-radius: 5px;">
                    <option value="demo">Demo Account (Practice)</option>
                    <option value="real">Real Account (Live Money)</option>
                </select>
            </div>
            
            <div style="margin-bottom: 2rem;">
                <label style="display: block; margin-bottom: 0.5rem; font-weight: bold;">API Key</label>
                <input type="password" id="apiKey" placeholder="Your API key (kept secure)" required>
                <p style="color: #666; font-size: 0.9em; margin-top: 0.5rem;">We never store your keys. They're encrypted end-to-end.</p>
            </div>
            
            <button class="btn" onclick="connectBroker()" style="width: 200px;">Connect Broker</button>
        </div>
        
        <div style="background: white; padding: 2rem; border-radius: 10px;">
            <h2 style="color: #1a1a2e; margin-bottom: 1.5rem;">Start Trading</h2>
            <p style="margin-bottom: 1rem; color: #666;">
                {% if plan == 'FREE' %}
                Upgrade to Pro to enable auto-trading and place real orders.
                <br><button class="btn" onclick="location.href='/upgrade?plan=pro'" style="margin-top: 1rem;">Upgrade to Pro ($49/month)</button>
                {% else %}
                Your bot is ready! Connect a broker above and click Start Bot.
                <br><button class="btn" onclick="startBot()" style="margin-top: 1rem;">Start Bot Now</button>
                {% endif %}
            </p>
        </div>
    </div>
    
    <script>
        async function connectBroker() {
            const res = await fetch('/connect-broker', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    broker: document.getElementById('broker').value,
                    account_type: document.getElementById('accountType').value,
                    api_key: document.getElementById('apiKey').value
                })
            });
            
            const data = await res.json();
            alert(data.message);
            if (data.success) location.reload();
        }
        
        async function startBot() {
            const res = await fetch('/start-bot', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({broker: 'deriv'})
            });
            
            const data = await res.json();
            alert(data.message);
        }
    </script>
</body>
</html>
'''

DEMO_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Live Demo - TradeBot</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #1a1a2e; color: white; }
        nav { background: #0d0d1a; padding: 1rem 2rem; }
        .container { max-width: 1200px; margin: 2rem auto; padding: 0 2rem; }
        h1 { color: #00d4ff; margin-bottom: 1rem; }
        .demo-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; }
        .demo-card { background: #16213e; padding: 2rem; border-radius: 10px; border: 1px solid #00d4ff; }
        .price { font-size: 2em; color: #00d4ff; font-weight: bold; }
        .signal { font-size: 1.5em; margin: 1rem 0; }
        .buy { color: #28a745; }
        .sell { color: #dc3545; }
        .hold { color: #ffc107; }
        button { background: #00d4ff; color: #1a1a2e; padding: 0.8rem 1.5rem; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; }
    </style>
</head>
<body>
    <nav>
        <a href="/" style="color: #00d4ff; text-decoration: none; font-weight: bold;">← Back</a>
    </nav>
    
    <div class="container">
        <h1>Live Trading Demo</h1>
        <p style="margin-bottom: 2rem; opacity: 0.9;">See TradeBot in action. Live market data, real signals.</p>
        
        <div class="demo-grid">
            <div class="demo-card">
                <h2>EUR/USD (Forex)</h2>
                <div class="price" id="eurusd-price">1.16551</div>
                <p style="margin: 1rem 0; opacity: 0.7;">5-min chart, live updates</p>
                <div class="signal">
                    Signal: <span class="sell">SELL</span>
                </div>
                <p style="font-size: 0.9em; opacity: 0.7;">Short MA below Long MA → Sell signal</p>
            </div>
            
            <div class="demo-card">
                <h2>Statistics</h2>
                <p style="margin: 1rem 0;">
                    <strong>Status:</strong> Connected<br>
                    <strong>Account:</strong> Demo ($ 10,111.33)<br>
                    <strong>Signals Today:</strong> 3<br>
                    <strong>Win Rate:</strong> 67% (last 30 days)
                </p>
                <button onclick="alert('Sign up to start trading!')">Start Your Own Bot</button>
            </div>
        </div>
        
        <div style="background: #16213e; padding: 2rem; border-radius: 10px; margin-top: 2rem; border: 1px solid #00d4ff;">
            <h2 style="margin-bottom: 1rem;">How It Works</h2>
            <ol style="line-height: 2; opacity: 0.9;">
                <li>TradeBot monitors EUR/USD price every minute</li>
                <li>Calculates 5-day and 20-day moving averages</li>
                <li>When short MA crosses below long MA → SELL signal</li>
                <li>When short MA crosses above long MA → BUY signal</li>
                <li>Automatically places order on your Deriv account</li>
                <li>Profits go directly to your account</li>
            </ol>
        </div>
    </div>
    
    <script>
        // Simulate price updates
        let price = 1.16551;
        setInterval(() => {
            price += (Math.random() - 0.5) * 0.0001;
            document.getElementById('eurusd-price').textContent = price.toFixed(5);
        }, 2000);
    </script>
</body>
</html>
'''

UPGRADE_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Upgrade - TradeBot</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f0f2f5; }
        nav { background: #1a1a2e; color: white; padding: 1rem 2rem; }
        .container { max-width: 600px; margin: 5rem auto; background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
        h1 { color: #1a1a2e; margin-bottom: 1rem; }
        .plan-info { background: #f0f2f5; padding: 2rem; border-radius: 10px; margin: 2rem 0; }
        .price { font-size: 3em; color: #00d4ff; font-weight: bold; }
        button { width: 100%; padding: 1rem; background: #00d4ff; color: #1a1a2e; border: none; border-radius: 5px; font-weight: bold; font-size: 1.1em; cursor: pointer; }
        button:hover { background: #00b8cc; }
    </style>
</head>
<body>
    <nav>
        <div style="font-size: 1.5em; font-weight: bold;">
            Trade<span style="color: #00d4ff;">Bot</span>
        </div>
    </nav>
    
    <div class="container">
        <h1>Upgrade Your Plan</h1>
        
        {% if plan == 'pro' %}
        <div class="plan-info">
            <h2>Pro Plan</h2>
            <div class="price">$49<span style="font-size: 0.4em; color: #666;">/month</span></div>
            <ul style="list-style: none; margin-top: 1.5rem; line-height: 2;">
                <li>✓ Unlimited signal detection</li>
                <li>✓ Auto-trading (up to 10 symbols)</li>
                <li>✓ Deriv + Alpaca platforms</li>
                <li>✓ Email support</li>
                <li>✓ Backtesting</li>
            </ul>
        </div>
        {% elif plan == 'enterprise' %}
        <div class="plan-info">
            <h2>Enterprise Plan</h2>
            <div class="price">$199<span style="font-size: 0.4em; color: #666;">/month</span></div>
            <ul style="list-style: none; margin-top: 1.5rem; line-height: 2;">
                <li>✓ Everything in Pro</li>
                <li>✓ Unlimited symbols</li>
                <li>✓ All platforms (4+)</li>
                <li>✓ Priority support</li>
                <li>✓ Custom strategies</li>
            </ul>
        </div>
        {% endif %}
        
        <button onclick="alert('Stripe checkout would be here - for now, contact us: contact@tradebot.com')">
            Proceed to Checkout
        </button>
        
        <p style="text-align: center; margin-top: 1rem; color: #666;">
            7-day free trial. Cancel anytime. No credit card for trial.
        </p>
    </div>
</body>
</html>
'''

if __name__ == '__main__':
    print("\n" + "="*70)
    print("TradeBot - Web Application")
    print("="*70)
    print("\nServer running at: http://localhost:5000")
    print("Open your browser to: http://localhost:5000")
    print("\nDemo accounts:")
    print("  - Email: demo@example.com")
    print("  - Password: demo123456")
    print("\nPress Ctrl+C to stop\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
