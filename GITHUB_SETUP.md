# GITHUB_SETUP.md

## Publishing to GitHub

### Step 1: Create a GitHub Account (if needed)

1. Visit https://github.com/signup
2. Create account with email
3. Verify email

### Step 2: Create New Repository

1. Go to https://github.com/new
2. Fill in details:
   - **Repository name:** `trading-bot`
   - **Description:** `Trading bot for forex and stocks with multiple strategies and platform adapters`
   - **Public/Private:** Choose based on preference
   - **Initialize:** Leave unchecked (we have local repo)

3. Click "Create repository"

### Step 3: Connect Local Repository

```bash
cd trading-bot
git remote add origin https://github.com/YOUR_USERNAME/trading-bot.git
git branch -M main
git push -u origin main
```

### Step 4: Push All Commits

```bash
git push origin main
```

### Step 5: Enable GitHub Features

#### Enable GitHub Actions
1. Go to repository → Settings → Actions
2. Enable GitHub Actions
3. Workflows in `.github/workflows/` will auto-run

#### Add Topics (for discoverability)
1. Repository → About (gear icon)
2. Add topics: `trading`, `bot`, `stocks`, `forex`, `alpaca`, `python`

#### Add README to Repository About
1. Ensure README.md is at root (already there)
2. GitHub auto-displays it

### Step 6: Configure Secrets (if using CI/CD with credentials)

1. Settings → Secrets and variables → Actions
2. Add secrets:
   - `ALPACA_API_KEY`
   - `ALPACA_API_SECRET`

Note: Don't commit real credentials to git!

### Step 7: Link Development Branches

```bash
# Create develop branch
git checkout -b develop
git push -u origin develop

# Protect main branch (on GitHub)
Settings → Branches → Add rule for "main"
- Require pull request reviews
- Require status checks to pass
```

---

## GitHub Actions Setup

### Automatic Testing

Tests run on every push and pull request:

```yaml
# Runs on:
- Python 3.9, 3.10, 3.11
- Windows, macOS, Linux
- Code linting and imports
```

View results: **Actions** tab → **Trading Bot Tests**

### View Test Results

1. Go to **Actions** tab
2. Click on workflow run
3. See job output and artifacts

### Badges for README

Add to your README.md:

```markdown
![Tests](https://github.com/YOUR_USERNAME/trading-bot/workflows/Trading%20Bot%20Tests/badge.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
```

---

## Docker Hub Integration (Optional)

### Setup Docker Hub

1. Create account at https://hub.docker.com
2. Create repository: `trading-bot`

### Auto-build from GitHub

1. Docker Hub → Repositories → Create
2. Link GitHub account
3. Select repository
4. Configure automated build

### Build and Push Manually

```bash
docker build -t YOUR_USERNAME/trading-bot:latest .
docker push YOUR_USERNAME/trading-bot:latest
```

---

## Collaboration Setup

### For Team Members

1. Repository URL: `https://github.com/YOUR_USERNAME/trading-bot`
2. Clone: `git clone <URL>`
3. Create feature branch: `git checkout -b feature/feature-name`
4. Make changes
5. Push: `git push origin feature/feature-name`
6. Create Pull Request on GitHub

### Code Review Process

1. PR created
2. GitHub Actions runs tests
3. Team reviews code
4. Approve and merge
5. Delete branch

---

## Release Management

### Create a Release

1. Go to **Releases** → **Create a new release**
2. Tag version: `v1.0.0`
3. Title: `Version 1.0.0 - Initial Release`
4. Description:
```markdown
## Features
- ✅ Multiple trading strategies (MA, RSI, MACD, Bollinger Bands)
- ✅ Alpaca broker integration
- ✅ Backtesting engine
- ✅ Comprehensive logging

## Installation
```bash
pip install -r requirements.txt
python -m trading_bot.main
```

## Known Issues
- None

## Upgrading
See [INSTALL.md](INSTALL.md)
```

5. Attach binary/source code if needed
6. Click "Publish release"

---

## Documentation on GitHub

### GitHub Pages (Optional)

Create `docs/` folder with Markdown files:

```
docs/
├── index.md
├── installation.md
├── usage.md
└── api.md
```

Enable in Settings → Pages:
- Source: Deploy from branch
- Branch: main
- Folder: docs/

---

## Communication Channels

### GitHub Discussions

Enable: Settings → Discussions  
Use for:
- Q&A
- Ideas
- Polls

### GitHub Issues

For:
- Bug reports
- Feature requests
- Documentation

Create issue templates in `.github/ISSUE_TEMPLATE/`:

```markdown
---
name: Bug Report
about: Report a bug
---

## Describe the bug
...

## Steps to reproduce
1.
2.

## Expected behavior
...

## Environment
- OS:
- Python version:
```

---

## Security

### Protect Sensitive Data

1. Never commit API keys
2. Use `.env` files (in `.gitignore`)
3. Use GitHub Secrets for CI/CD
4. Enable branch protection
5. Require code reviews

### GitHub Security Features

1. Settings → Security analysis
   - Enable Dependabot alerts
   - Enable secret scanning
2. Code scanning with CodeQL
3. Dependency updates

---

## Monitoring

### Check Repository Health

1. Insights → Community
2. Insights → Network
3. Insights → Traffic
4. Pulse (recent activity)

### GitHub Stats

View stars, forks, watchers on main page

---

## Publishing to PyPI (Advanced)

Make installable via `pip`:

1. Add `setup.py` or `pyproject.toml` (already configured)
2. Create PyPI account
3. Add GitHub token to PyPI
4. Create GitHub Actions workflow for publishing

See: [Python Packaging](https://packaging.python.org/)

---

## Troubleshooting

### Push rejected
```bash
git pull origin main
git push origin main
```

### Branch conflicts
```bash
git fetch origin
git rebase origin/main
git push origin feature-branch --force-with-lease
```

### Remove file from history
```bash
git rm --cached filename
git commit --amend
git push -f origin main
```

---

## Support

- GitHub Issues: Bug reports & feature requests
- GitHub Discussions: Q&A & ideas
- Documentation: README, INSTALL, DEPLOYMENT files
- Community: GitHub Stars & followers

---

**You're now ready to go live on GitHub!** 🚀
