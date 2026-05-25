#!/usr/bin/env python3
"""
Automated GitHub Push Helper
Guides you through pushing to GitHub and deploying to Render
"""

print("=" * 80)
print("🚀 PUSH YOUR BOT TO GITHUB & DEPLOY TO RENDER")
print("=" * 80)

print("""
✅ YOU HAVE:
├─ Local git repository with 8+ commits
├─ 70+ files ready to deploy
├─ M-Pesa integration working
├─ Tests passing
└─ Production-ready code

❌ YOU NEED:
├─ GitHub repository created
├─ Code pushed to GitHub
└─ Render deployment configured

⏱️ TIME REQUIRED:
├─ GitHub: 5 minutes
├─ Push code: 2 minutes
├─ Render: 5 minutes
└─ TOTAL: 12 MINUTES TO LIVE! 🎯

""")

print("=" * 80)
print("STEP 1: CREATE GITHUB REPOSITORY")
print("=" * 80)

print("""
1. Open: https://github.com/new
2. Sign in if needed
3. Enter:
   Repository name: trading-bot
   Description: M-Pesa Trading Bot - Automated trading
   Public: ✓ Check this box
4. Click: "Create repository"
5. Copy the URL shown (should look like):
   https://github.com/YOUR_USERNAME/trading-bot.git

⏸️ PAUSE HERE - Go create the repository, then come back!
""")

print("\n" + "=" * 80)
print("STEP 2: PUSH YOUR CODE")
print("=" * 80)

print("""
After creating the GitHub repo, run these commands in PowerShell:

cd c:\\Users\\ADMIN\\OneDrive\\project\\bot

# Connect to GitHub (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/trading-bot.git

# Rename branch to main (GitHub default)
git branch -M main

# Push all your code to GitHub
git push -u origin main

Expected output:
  Enumerating objects: 150, done.
  Counting objects: 100% (150/150), done.
  Delta compression using up to 8 threads
  ...
  To https://github.com/YOUR_USERNAME/trading-bot.git
   * [new branch]      main -> main
  Branch 'main' set up to track remote branch 'main' from 'origin'.

✅ Code is now on GitHub!
""")

print("\n" + "=" * 80)
print("STEP 3: VERIFY ON GITHUB")
print("=" * 80)

print("""
1. Visit: https://github.com/YOUR_USERNAME/trading-bot
2. You should see:
   ✓ 70+ files
   ✓ 8+ commits
   ✓ landing_page.html
   ✓ web_app_mpesa.py
   ✓ MPESA_INTEGRATION.md
   ✓ All your code!

3. If you see "This repository is empty":
   - The push didn't work
   - Check your GitHub URL is correct
   - Run the push commands again
""")

print("\n" + "=" * 80)
print("STEP 4: DEPLOY TO RENDER")
print("=" * 80)

print("""
Now that code is on GitHub, deploy it:

1. Go to: https://render.com/
2. Sign up with GitHub (easiest!)
3. Click: "New +" button
4. Select: "Web Service"
5. Connect: Your GitHub repository
   - Select: trading-bot
   - Click: Connect
6. Fill in:
   - Name: trading-bot-mpesa
   - Runtime: Python 3
   - Build Command: pip install -r requirements.txt
   - Start Command: python web_app_mpesa.py
7. Click: "Environment" tab
8. Add environment variables:
   
   Key: MPESA_CONSUMER_KEY
   Value: 6o6AGEbH7i7Kr9xXaxtn6glXhvwGxaUEqoYWIpWPAlU9oqEx
   
   Key: MPESA_CONSUMER_SECRET
   Value: NpwsH9jYG3qktd824AZAn6EAbRieprOL5uJ2eAmW4c3dzXHtJqgRORWK537IEgZv
   
   Key: MPESA_SHORTCODE
   Value: 174379
   
   Key: SECRET_KEY
   Value: (generate random string like: my_secret_key_12345)

9. Click: "Create Web Service"
10. Wait 2-3 minutes for deployment
11. ✅ You get a live URL!

Your URL will be something like:
https://trading-bot-mpesa.onrender.com
""")

print("\n" + "=" * 80)
print("STEP 5: SHARE YOUR BOT")
print("=" * 80)

print("""
Your bot is now LIVE and can:

✓ Accept M-Pesa payments
✓ Generate licenses automatically
✓ Run trading bots 24/7
✓ Make you money!

Share your URL:
https://trading-bot-mpesa.onrender.com

Post on:
- Reddit (r/algotrading, r/investing, r/Kenya)
- Twitter
- Email to friends
- Trading groups

When customers:
1. Sign up (free)
2. Upgrade to Pro ($49)
3. Pay via M-Pesa
4. You get $49 every month! 💰
""")

print("\n" + "=" * 80)
print("⚠️  IMPORTANT NOTES")
print("=" * 80)

print("""
1. GITHUB URL:
   - Replace YOUR_USERNAME with your actual GitHub username
   - Example: git@github.com:john_doe/trading-bot.git
   
2. IF YOU GET "Permission denied":
   - Use HTTPS instead of SSH
   - Replace git@ with https://
   - Example: https://github.com/john_doe/trading-bot.git

3. IF YOU GET "remote origin already exists":
   - Run: git remote remove origin
   - Then add again: git remote add origin ...

4. RENDER FREE TIER:
   - $0/month for first 750 hours
   - Perfect to start!
   - Enough for 1-100 customers
   - Upgrade to $7/month if needed

5. GITHUB + RENDER:
   - Updates to GitHub = auto-deployed to Render
   - No need to re-deploy manually
   - Perfect for continuous updates!
""")

print("\n" + "=" * 80)
print("🎯 TIMELINE")
print("=" * 80)

print("""
RIGHT NOW:
  5 min → Create GitHub repo
  2 min → Push code
  1 min → Verify on GitHub

NEXT 5 MINUTES:
  5 min → Deploy to Render
  
TOTAL: 15 MINUTES TO LIVE ⚡

THEN:
  Week 1: Get first customer ($49)
  Month 2: 10 customers ($490)
  Month 6: 100 customers ($4,900)
  Year 1: $50,000+
""")

print("\n" + "=" * 80)
print("✅ YOU'RE READY!")
print("=" * 80)

print("""
Your trading bot is production-ready!

Next steps:
1. Go to: https://github.com/new
2. Create repository: "trading-bot"
3. Copy GitHub URL
4. Come back and run the push commands
5. Deploy to Render
6. Make money! 💰

LET'S GO! 🚀
""")

print("=" * 80)
