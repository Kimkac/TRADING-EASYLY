"""
Flask Web App with M-Pesa & Airtel Money Integration
Complete SaaS application with demo/real account support and mobile money payments
"""

from flask import Flask, render_template_string, request, jsonify, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import json
import os
from datetime import datetime
from src.trading_bot.payments import UnifiedPaymentGateway, MpesaPaymentProcessor

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "trading-bot-secret-2024")

# Initialize payment gateway
payment_gateway = UnifiedPaymentGateway({
    "mpesa": {
        "consumer_key": os.environ.get("MPESA_CONSUMER_KEY", "test_key"),
        "consumer_secret": os.environ.get("MPESA_CONSUMER_SECRET", "test_secret"),
        "business_shortcode": os.environ.get("MPESA_SHORTCODE", "174379"),
        "passkey": os.environ.get("MPESA_PASSKEY", "test_passkey"),
        "environment": "sandbox"
    },
    "airtel": {
        "client_id": os.environ.get("AIRTEL_CLIENT_ID", "test_id"),
        "client_secret": os.environ.get("AIRTEL_CLIENT_SECRET", "test_secret"),
        "merchant_id": os.environ.get("AIRTEL_MERCHANT_ID", "test_merchant"),
        "environment": "sandbox"
    }
})

# Database setup
def init_db():
    conn = sqlite3.connect("tradebot.db")
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, email TEXT UNIQUE, password TEXT,
                  created_at TEXT, subscription_tier TEXT, phone TEXT, country TEXT)''')
    
    # Subscriptions table
    c.execute('''CREATE TABLE IF NOT EXISTS subscriptions
                 (id INTEGER PRIMARY KEY, user_id INTEGER, tier TEXT, 
                  start_date TEXT, end_date TEXT, payment_method TEXT,
                  payment_status TEXT, mpesa_checkout_id TEXT)''')
    
    # Payment history
    c.execute('''CREATE TABLE IF NOT EXISTS payments
                 (id INTEGER PRIMARY KEY, user_id INTEGER, amount REAL,
                  currency TEXT, method TEXT, status TEXT, 
                  reference TEXT, timestamp TEXT)''')
    
    # Broker connections table
    c.execute('''CREATE TABLE IF NOT EXISTS broker_connections
                 (id INTEGER PRIMARY KEY, user_id INTEGER, broker TEXT,
                  account_type TEXT, api_token TEXT, created_at TEXT)''')
    
    conn.commit()
    conn.close()

init_db()


def get_user(user_id):
    conn = sqlite3.connect("tradebot.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = c.fetchone()
    conn.close()
    return user


def get_subscription(user_id):
    conn = sqlite3.connect("tradebot.db")
    c = conn.cursor()
    c.execute("SELECT * FROM subscriptions WHERE user_id=? ORDER BY id DESC LIMIT 1", (user_id,))
    sub = c.fetchone()
    conn.close()
    return sub


# ========== ROUTES ==========

@app.route("/")
def index():
    """Landing page"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Trading Bot - Automate Your Trading</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
            .navbar { background: rgba(0,0,0,0.3); padding: 1rem 2rem; display: flex; justify-content: space-between; }
            .navbar a { color: white; margin-left: 2rem; text-decoration: none; font-weight: bold; }
            .container { max-width: 1200px; margin: 0 auto; padding: 3rem 2rem; }
            .hero { text-align: center; color: white; margin-bottom: 4rem; }
            .hero h1 { font-size: 3rem; margin-bottom: 1rem; }
            .hero p { font-size: 1.2rem; opacity: 0.9; margin-bottom: 2rem; }
            .btn { padding: 1rem 2rem; background: #ff6b6b; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; text-decoration: none; display: inline-block; }
            .btn:hover { background: #ff5252; }
            .features { display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; margin: 4rem 0; }
            .feature { background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
            .feature h3 { color: #667eea; margin-bottom: 1rem; }
            .pricing { display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; margin: 4rem 0; }
            .plan { background: white; padding: 2rem; border-radius: 10px; text-align: center; }
            .plan h3 { color: #667eea; margin-bottom: 1rem; font-size: 1.5rem; }
            .plan .price { font-size: 2rem; font-weight: bold; color: #ff6b6b; margin: 1rem 0; }
            .plan ul { list-style: none; margin: 1rem 0; text-align: left; }
            .plan li { padding: 0.5rem 0; color: #666; }
            .payment-methods { display: flex; gap: 1rem; margin-top: 2rem; justify-content: center; }
            .payment-badge { background: #f0f0f0; padding: 0.5rem 1rem; border-radius: 5px; font-size: 0.9rem; }
            .mpesa-badge { background: #40b34f; color: white; }
            .airtel-badge { background: #e31937; color: white; }
        </style>
    </head>
    <body>
        <div class="navbar">
            <h2 style="color: white;">🤖 Trading Bot</h2>
            <div>
                <a href="/login">Login</a>
                <a href="/signup">Get Started</a>
            </div>
        </div>
        
        <div class="container">
            <div class="hero">
                <h1>🚀 Automate Your Trading</h1>
                <p>Start with FREE demo account. Upgrade to real money whenever ready.</p>
                <a href="/signup" class="btn">Start Free</a>
            </div>
            
            <div class="features">
                <div class="feature">
                    <h3>📊 Real-Time Signals</h3>
                    <p>Get trading signals based on moving average strategy. Updated every minute.</p>
                </div>
                <div class="feature">
                    <h3>🔄 Auto Trading</h3>
                    <p>Trades placed automatically. No manual intervention needed.</p>
                </div>
                <div class="feature">
                    <h3>💡 Demo + Real</h3>
                    <p>Practice with virtual money first. Switch to real accounts anytime.</p>
                </div>
            </div>
            
            <h2 style="text-align: center; color: white; margin: 3rem 0;">💳 Pricing & Payment Methods</h2>
            <div class="pricing">
                <div class="plan">
                    <h3>FREE</h3>
                    <div class="price">$0</div>
                    <ul>
                        <li>✓ Demo Account</li>
                        <li>✓ Basic Signals</li>
                        <li>✓ 1 Symbol</li>
                        <li>✗ Auto Trading</li>
                    </ul>
                    <a href="/signup" class="btn">Start Free</a>
                </div>
                
                <div class="plan">
                    <h3>PRO</h3>
                    <div class="price">$49<span style="font-size: 1rem;"> /month</span></div>
                    <ul>
                        <li>✓ Demo Account</li>
                        <li>✓ Real Account</li>
                        <li>✓ Auto Trading</li>
                        <li>✓ Unlimited Symbols</li>
                    </ul>
                    <div class="payment-methods">
                        <span class="payment-badge mpesa-badge">M-Pesa</span>
                        <span class="payment-badge airtel-badge">Airtel Money</span>
                    </div>
                </div>
                
                <div class="plan">
                    <h3>ENTERPRISE</h3>
                    <div class="price">$199<span style="font-size: 1rem;"> /month</span></div>
                    <ul>
                        <li>✓ Everything in Pro</li>
                        <li>✓ Priority Support</li>
                        <li>✓ Custom Strategies</li>
                        <li>✓ API Access</li>
                    </ul>
                    <a href="/signup" class="btn">Contact Sales</a>
                </div>
            </div>
            
            <div style="text-align: center; color: white; margin-top: 3rem;">
                <h3>💰 More Traders. More Signals. More Profits.</h3>
                <p style="font-size: 1.1rem; opacity: 0.9;">Join 2,500+ traders making automated decisions</p>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        phone = request.form.get("phone")
        country = request.form.get("country", "Kenya")
        
        if not email or not password:
            return "Email and password required", 400
        
        try:
            conn = sqlite3.connect("tradebot.db")
            c = conn.cursor()
            c.execute("INSERT INTO users (email, password, created_at, subscription_tier, phone, country) VALUES (?,?,?,?,?,?)",
                     (email, generate_password_hash(password), datetime.now().isoformat(), "FREE", phone, country))
            conn.commit()
            user_id = c.lastrowid
            conn.close()
            
            session["user_id"] = user_id
            return redirect("/dashboard")
        except sqlite3.IntegrityError:
            return "Email already exists", 400
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sign Up - Trading Bot</title>
        <style>
            body { font-family: Arial; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; }
            .form-container { background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); width: 100%; max-width: 400px; }
            h2 { color: #333; margin-bottom: 1.5rem; }
            input { width: 100%; padding: 0.8rem; margin-bottom: 1rem; border: 1px solid #ddd; border-radius: 5px; font-size: 1rem; }
            select { width: 100%; padding: 0.8rem; margin-bottom: 1rem; border: 1px solid #ddd; border-radius: 5px; }
            button { width: 100%; padding: 0.8rem; background: #667eea; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; }
            button:hover { background: #5568d3; }
            .info { font-size: 0.9rem; color: #666; margin-top: 1rem; }
        </style>
    </head>
    <body>
        <div class="form-container">
            <h2>Create Account</h2>
            <form method="POST">
                <input type="email" name="email" placeholder="Email" required>
                <input type="password" name="password" placeholder="Password" required>
                <input type="tel" name="phone" placeholder="Phone (254712345678)" required>
                <select name="country">
                    <option>Kenya (M-Pesa)</option>
                    <option>Uganda (Airtel)</option>
                    <option>Tanzania (Airtel)</option>
                    <option>DRC (Airtel)</option>
                    <option>Other</option>
                </select>
                <button type="submit">Sign Up Free</button>
            </form>
            <div class="info">
                Already have account? <a href="/login">Login here</a>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        conn = sqlite3.connect("tradebot.db")
        c = conn.cursor()
        c.execute("SELECT id, password FROM users WHERE email=?", (email,))
        user = c.fetchone()
        conn.close()
        
        if user and check_password_hash(user[1], password):
            session["user_id"] = user[0]
            return redirect("/dashboard")
        else:
            return "Invalid email or password", 401
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login - Trading Bot</title>
        <style>
            body { font-family: Arial; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; }
            .form-container { background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); width: 100%; max-width: 400px; }
            h2 { color: #333; margin-bottom: 1.5rem; }
            input { width: 100%; padding: 0.8rem; margin-bottom: 1rem; border: 1px solid #ddd; border-radius: 5px; font-size: 1rem; }
            button { width: 100%; padding: 0.8rem; background: #667eea; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; }
            button:hover { background: #5568d3; }
        </style>
    </head>
    <body>
        <div class="form-container">
            <h2>Login</h2>
            <form method="POST">
                <input type="email" name="email" placeholder="Email" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">Login</button>
            </form>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")
    
    user = get_user(session["user_id"])
    sub = get_subscription(session["user_id"])
    tier = sub[2] if sub else "FREE"
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dashboard - Trading Bot</title>
        <style>
            body {{ font-family: Arial; background: #f5f5f5; }}
            .navbar {{ background: #333; padding: 1rem 2rem; color: white; }}
            .container {{ max-width: 1000px; margin: 0 auto; padding: 2rem; }}
            .card {{ background: white; padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
            .btn {{ padding: 0.8rem 1.5rem; background: #667eea; color: white; border: none; border-radius: 5px; cursor: pointer; }}
            .btn:hover {{ background: #5568d3; }}
            .tier-badge {{ display: inline-block; padding: 0.5rem 1rem; background: #667eea; color: white; border-radius: 5px; }}
            .payment-option {{ display: inline-block; margin: 0.5rem; padding: 0.8rem 1rem; background: #f0f0f0; border-radius: 5px; cursor: pointer; border: 2px solid transparent; }}
            .payment-option:hover {{ border-color: #667eea; background: #e8e8e8; }}
            .mpesa {{ background: #40b34f; color: white; }}
            .airtel {{ background: #e31937; color: white; }}
        </style>
    </head>
    <body>
        <div class="navbar">
            <h2>Trading Bot Dashboard</h2>
        </div>
        
        <div class="container">
            <div class="card">
                <h3>Your Account</h3>
                <p><strong>Email:</strong> {user[1]}</p>
                <p><strong>Phone:</strong> {user[4]}</p>
                <p><strong>Country:</strong> {user[5]}</p>
                <p><strong>Tier:</strong> <span class="tier-badge">{tier}</span></p>
            </div>
            
            <div class="card">
                <h3>💳 Upgrade to Pro ($49/month)</h3>
                <p>Get auto-trading, unlimited symbols, real account support</p>
                
                <h4>Choose Payment Method:</h4>
                <div style="margin: 1rem 0;">
                    <button class="payment-option mpesa" onclick="initiateMpesa()">
                        📱 M-Pesa (Kenya)
                    </button>
                    <button class="payment-option airtel" onclick="initiateAirtel()">
                        📱 Airtel Money
                    </button>
                </div>
            </div>
            
            <div class="card">
                <h3>🤖 Connect Broker</h3>
                <p>Select demo or real account type:</p>
                <form action="/connect-broker" method="POST">
                    <select name="account_type" required>
                        <option value="demo">Demo Account (Practice)</option>
                        <option value="real">Real Account (Live Money)</option>
                    </select>
                    <input type="password" name="api_token" placeholder="Your API Token" required>
                    <button type="submit" class="btn">Connect</button>
                </form>
            </div>
            
            <a href="/logout" class="btn">Logout</a>
        </div>
        
        <script>
            function initiateMpesa() {{
                const phone = prompt("Enter M-Pesa phone number (254712345678):");
                if (phone) {{
                    fetch('/api/mpesa_payment', {{
                        method: 'POST',
                        headers: {{'Content-Type': 'application/json'}},
                        body: JSON.stringify({{
                            phone: phone,
                            amount: 4900,
                            account_ref: 'user_' + {session["user_id"]}
                        }})
                    }})
                    .then(r => r.json())
                    .then(d => {{
                        if (d.success) {{
                            alert('Check your phone for M-Pesa prompt!');
                        }} else {{
                            alert('Error: ' + d.error);
                        }}
                    }})
                    .catch(e => alert('Error: ' + e));
                }}
            }}
            
            function initiateAirtel() {{
                const phone = prompt("Enter Airtel phone number:");
                if (phone) {{
                    fetch('/api/airtel_payment', {{
                        method: 'POST',
                        headers: {{'Content-Type': 'application/json'}},
                        body: JSON.stringify({{
                            phone: phone,
                            amount: 49,
                            account_ref: 'user_' + {session["user_id"]}
                        }})
                    }})
                    .then(r => r.json())
                    .then(d => {{
                        if (d.success) {{
                            alert('Payment initiated! Check your Airtel app.');
                        }} else {{
                            alert('Error: ' + d.error);
                        }}
                    }})
                    .catch(e => alert('Error: ' + e));
                }}
            }}
        </script>
    </body>
    </html>
    """
    return render_template_string(html)


@app.route("/api/mpesa_payment", methods=["POST"])
def mpesa_payment():
    """Initiate M-Pesa payment"""
    if "user_id" not in session:
        return jsonify({"success": False, "error": "Not logged in"}), 401
    
    data = request.get_json()
    phone = data.get("phone")
    amount = data.get("amount", 4900)  # 49.00 KES
    account_ref = data.get("account_ref")
    
    try:
        # Initiate STK push
        result = payment_gateway.providers["mpesa"].initiate_stk_push(
            phone_number=phone,
            amount=amount,
            account_reference=account_ref,
            transaction_desc="Trading Bot Pro Subscription"
        )
        
        if result.get("success"):
            # Store payment record
            conn = sqlite3.connect("tradebot.db")
            c = conn.cursor()
            c.execute("""INSERT INTO payments 
                        (user_id, amount, currency, method, status, reference, timestamp)
                        VALUES (?, ?, ?, ?, ?, ?, ?)""",
                     (session["user_id"], amount/100, "KES", "mpesa", "pending", 
                      result.get("checkout_id"), datetime.now().isoformat()))
            conn.commit()
            conn.close()
            
            return jsonify(result)
        else:
            return jsonify(result)
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/airtel_payment", methods=["POST"])
def airtel_payment():
    """Initiate Airtel Money payment"""
    if "user_id" not in session:
        return jsonify({"success": False, "error": "Not logged in"}), 401
    
    data = request.get_json()
    phone = data.get("phone")
    amount = data.get("amount", 49)  # 49 USD
    account_ref = data.get("account_ref")
    
    try:
        result = payment_gateway.providers["airtel"].charge_customer(
            phone_number=phone,
            amount=amount,
            reference=account_ref,
            narration="Trading Bot Pro Subscription"
        )
        
        # Store payment record
        conn = sqlite3.connect("tradebot.db")
        c = conn.cursor()
        c.execute("""INSERT INTO payments 
                    (user_id, amount, currency, method, status, reference, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?)""",
                 (session["user_id"], amount, "USD", "airtel", "pending", 
                  account_ref, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        
        return jsonify({"success": True, "result": result})
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/connect-broker", methods=["POST"])
def connect_broker():
    """Store broker connection"""
    if "user_id" not in session:
        return redirect("/login")
    
    broker = request.form.get("broker", "deriv")
    account_type = request.form.get("account_type", "demo")
    api_token = request.form.get("api_token")
    
    conn = sqlite3.connect("tradebot.db")
    c = conn.cursor()
    c.execute("""INSERT INTO broker_connections 
                (user_id, broker, account_type, api_token, created_at)
                VALUES (?, ?, ?, ?, ?)""",
             (session["user_id"], broker, account_type, api_token, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    
    return redirect("/dashboard")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
