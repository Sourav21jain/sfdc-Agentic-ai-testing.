# How to Push This to GitHub

## Step 1: Create a GitHub Repository

### Option A: Via GitHub Website (Easiest)

1. Go to https://github.com
2. Log in to your account
3. Click the **+** icon (top right) → **New repository**
4. Fill in:
   - **Repository name**: `sfdc-insights-agent` or `openshift-insights-agent`
   - **Description**: `AI-powered agent that auto-posts OpenShift cluster insights to Salesforce cases`
   - **Visibility**: 
     - Choose **Public** if you want to share it
     - Choose **Private** if it's internal only
   - **DO NOT** check "Initialize this repository with a README" (we already have one)
5. Click **Create repository**

### Option B: Via GitHub CLI (If you have it installed)

```bash
gh repo create sfdc-insights-agent --public --source=. --remote=origin --push
```

## Step 2: Link Local Repository to GitHub

After creating the repo on GitHub, you'll see a page with setup instructions. Use these commands:

```bash
# Make sure you're in the project directory
cd /Users/soujain/insights-tool

# Add GitHub as remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/sfdc-insights-agent.git

# Or if you use SSH:
# git remote add origin git@github.com:YOUR_USERNAME/sfdc-insights-agent.git

# Verify the remote was added
git remote -v
```

## Step 3: Push to GitHub

```bash
# Push the main branch to GitHub
git push -u origin main
```

You may be prompted for your GitHub credentials:
- **Username**: Your GitHub username
- **Password**: Your GitHub Personal Access Token (NOT your password)

### Creating a Personal Access Token (if needed)

If you need a token:

1. Go to https://github.com/settings/tokens
2. Click **Generate new token** → **Generate new token (classic)**
3. Give it a name: `SFDC Insights Agent`
4. Select scopes: Check **repo** (this gives full repository access)
5. Click **Generate token**
6. **Copy the token** (you won't see it again!)
7. Use this token as your password when pushing

## Step 4: Verify Upload

1. Go to your repository on GitHub: `https://github.com/YOUR_USERNAME/sfdc-insights-agent`
2. You should see all your files!
3. Check that the README.md displays properly

## Step 5: Add a Nice README Badge (Optional)

Add this to the top of your README.md:

```markdown
# SFDC OpenShift Insights Auto-Comment Agent

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
```

## Repository Structure on GitHub

Your repository will look like this:

```
sfdc-insights-agent/
├── .github/workflows/
│   └── test.yml              # GitHub Actions CI/CD
├── src/                      # Python source code
├── config/                   # Configuration files
├── data/                     # Mock data
├── tests/                    # Unit tests
├── README.md                 # Main documentation
├── QUICK_START.md           # Quick start guide
├── HOW_TO_RUN.md            # Detailed run instructions
├── SALESFORCE_SETUP.md      # SFDC setup guide
├── PROJECT_SUMMARY.md       # Technical overview
├── LICENSE                  # MIT License
└── requirements.txt         # Python dependencies
```

## Making Changes and Pushing Updates

When you make changes to the code:

```bash
# Check what changed
git status

# Stage your changes
git add .

# Commit with a message
git commit -m "Add feature: XYZ"

# Push to GitHub
git push
```

## Best Practices

### 1. Never Commit Secrets!

The `.gitignore` file already excludes:
- `config/.env` (your credentials)
- `venv/` (Python virtual environment)
- `logs/` (log files)

**Always verify before committing:**
```bash
git status
# Make sure config/.env is NOT in the list
```

### 2. Write Good Commit Messages

Good:
```bash
git commit -m "Add Tableau API integration to replace mock data"
git commit -m "Fix retry logic in event_listener.py"
git commit -m "Update documentation for cloud deployment"
```

Bad:
```bash
git commit -m "fix"
git commit -m "updates"
git commit -m "stuff"
```

### 3. Create Branches for Features

```bash
# Create a new branch for a feature
git checkout -b feature/tableau-integration

# Make your changes...
git add .
git commit -m "Add Tableau API integration"

# Push the branch
git push -u origin feature/tableau-integration

# On GitHub, create a Pull Request to merge into main
```

### 4. Tag Releases

When you reach milestones:

```bash
# Tag version 1.0.0
git tag -a v1.0.0 -m "Release version 1.0.0 - MVP complete"
git push origin v1.0.0
```

## Sharing Your Repository

Once it's public, share it with:

- **Clone URL**: `https://github.com/YOUR_USERNAME/sfdc-insights-agent.git`
- **Direct Link**: `https://github.com/YOUR_USERNAME/sfdc-insights-agent`

Others can clone it with:
```bash
git clone https://github.com/YOUR_USERNAME/sfdc-insights-agent.git
cd sfdc-insights-agent
./run_agent.sh
```

## Adding Collaborators (Private Repos)

If your repo is private and you want to add team members:

1. Go to your repository on GitHub
2. Click **Settings** tab
3. Click **Collaborators and teams** (left menu)
4. Click **Add people**
5. Enter their GitHub username
6. Choose permission level (Read, Write, or Admin)
7. Click **Add**

## GitHub Actions (CI/CD)

The repository includes a GitHub Actions workflow (`.github/workflows/test.yml`) that:
- Automatically runs tests when you push
- Verifies Python 3.9+ compatibility
- Ensures all dependencies install correctly

View the actions at: `https://github.com/YOUR_USERNAME/sfdc-insights-agent/actions`

## Troubleshooting

### "Permission denied (publickey)"

You're trying to use SSH but don't have SSH keys set up.

**Solution**: Use HTTPS instead:
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/sfdc-insights-agent.git
git push -u origin main
```

Or [set up SSH keys](https://docs.github.com/en/authentication/connecting-to-github-with-ssh).

### "Repository not found"

- Check the URL is correct
- Make sure you created the repository on GitHub
- Verify you're logged in to the right GitHub account

### "Authentication failed"

- Make sure you're using a Personal Access Token, not your password
- Check the token has `repo` permissions
- Generate a new token if needed

## Quick Reference

```bash
# Clone from GitHub
git clone https://github.com/YOUR_USERNAME/sfdc-insights-agent.git

# Check status
git status

# Stage changes
git add .

# Commit
git commit -m "Your message"

# Push
git push

# Pull latest changes
git pull

# View history
git log --oneline

# Create branch
git checkout -b branch-name

# Switch branches
git checkout main
```

## Next Steps

After pushing to GitHub:

1. ⭐ **Star your own repo** (top right on GitHub)
2. 📝 **Add topics** (Settings → Topics): `salesforce`, `openshift`, `ai`, `python`, `claude-api`
3. 🔒 **Review security** (Settings → Security): Enable Dependabot alerts
4. 📊 **Enable Discussions** (Settings → Features): For community questions
5. 📄 **Add a Wiki** (Settings → Features): For extended documentation

Enjoy your GitHub repository! 🎉
