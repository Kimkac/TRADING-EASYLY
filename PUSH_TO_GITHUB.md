# 🚀 HOW TO PUSH YOUR BOT TO GITHUB

## Step 1: Create GitHub Repository (5 minutes)

1. Go to: https://github.com/new
2. Sign in with your account
3. Fill in:
   - **Repository name:** `trading-bot` (or any name you like)
   - **Description:** "M-Pesa Trading Bot - Automated trading with subscription system"
   - **Public:** ✓ (so customers can see your code)
   - Click: "Create repository"

4. Copy your repository URL
   - Should look like: `https://github.com/YOUR_USERNAME/trading-bot.git`
   - Or: `git@github.com:YOUR_USERNAME/trading-bot.git`

---

## Step 2: Push Code to GitHub (2 minutes)

Replace `YOUR_USERNAME` with your actual GitHub username:

```bash
cd c:\Users\ADMIN\OneDrive\project\bot

# Add remote (connect to GitHub)
git remote add origin https://github.com/YOUR_USERNAME/trading-bot.git

# Push code to GitHub
git branch -M main
git push -u origin main
```

---

## Step 3: Verify on GitHub (1 minute)

1. Go to: https://github.com/YOUR_USERNAME/trading-bot
2. You should see:
   - ✅ All your files
   - ✅ All your commits
   - ✅ Full trading bot code
   - ✅ M-Pesa integration
   - ✅ Ready to deploy!

---

## Step 4: Deploy to Render (5 minutes)

Once code is on GitHub:

1. Go to: https://render.com/
2. Click: "New Web Service"
3. Select: "Public Git repository"
4. Paste: Your GitHub repository URL
5. Fill in:
   - **Name:** `trading-bot-mpesa`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python web_app_mpesa.py`
6. Click: "Environment" tab
7. Add your environment variables:
   ```
   MPESA_CONSUMER_KEY=6o6AGEbH7i7Kr9xXaxtn6glXhvwGxaUEqoYWIpWPAlU9oqEx
   MPESA_CONSUMER_SECRET=NpwsH9jYG3qktd824AZAn6EAbRieprOL5uJ2eAmW4c3dzXHtJqgRORWK537IEgZv
   MPESA_SHORTCODE=174379
   SECRET_KEY=your_secret_key_here
   ```
8. Click: "Create Web Service"
9. Wait 2-3 minutes
10. ✅ Your bot is LIVE!

---

## Your Live URL

After deployment, you'll get:
```
https://trading-bot-mpesa.onrender.com
```

Share this with customers!

---

## Revenue Starts Now

When customers visit your URL:
1. They sign up
2. Choose "Upgrade to Pro" ($49/month)
3. Select M-Pesa payment
4. Payment confirmed
5. License activated
6. **You make $49!** 💰

---

## Quick Command Guide

If you're using GitHub with SSH key (more secure):

```bash
cd c:\Users\ADMIN\OneDrive\project\bot

# If using HTTPS:
git remote add origin https://github.com/YOUR_USERNAME/trading-bot.git

# If using SSH:
git remote add origin git@github.com:YOUR_USERNAME/trading-bot.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## Troubleshooting

### "fatal: remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/trading-bot.git
git push -u origin main
```

### "Permission denied (publickey)"
- You're using SSH without setting up keys
- Use HTTPS instead (easier):
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/trading-bot.git
git push -u origin main
```

### "Everything up-to-date"
- Your code is already pushed
- Go to GitHub and verify it's there
- Proceed to Render deployment

---

## NEXT STEPS

1. Create GitHub repository: https://github.com/new
2. Run the git commands above
3. Verify on GitHub
4. Deploy to Render
5. Start accepting payments!

You're almost there! 🚀
