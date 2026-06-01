# Quick Command Reference

All the commands you need in one place.

## 🚀 Running the Agent

```bash
# Start the agent (recommended)
./run_agent.sh

# Run in background
nohup ./run_agent.sh > logs/nohup.log 2>&1 &

# Stop background agent
pkill -f "python -m src.agent"

# Check if agent is running
ps aux | grep "python -m src.agent"

# View live logs
tail -f logs/agent.log
```

## 🧪 Testing

```bash
# Test all components
./quick_test.sh

# Test individual components
python -m src.insights_service
python -m src.sfdc_client
python -m src.comment_generator

# Run unit tests
source venv/bin/activate
pytest tests/ -v

# Run unit tests with coverage
pytest tests/ -v --cov=src
```

## ⚙️ Setup Commands

```bash
# Initial setup
cd /Users/soujain/insights-tool
cp config/.env.example config/.env
nano config/.env  # Edit credentials

# Create virtual environment manually
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Update dependencies
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 📝 Git Commands

```bash
# Initialize repository (already done)
git init
git branch -m main

# Add all files
git add -A

# Commit changes
git commit -m "Your commit message"

# Add GitHub remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/sfdc-insights-agent.git

# Push to GitHub
git push -u origin main

# Check status
git status

# View changes
git diff

# View commit history
git log --oneline

# Create a new branch
git checkout -b feature/new-feature

# Switch branches
git checkout main

# Pull latest changes
git pull
```

## 📂 File Operations

```bash
# View project structure
find . -type f -name "*.py" | grep -v __pycache__

# View logs
tail -f logs/agent.log
cat logs/agent.log

# Clear logs
> logs/agent.log

# Check disk usage
du -sh .
du -sh venv/

# Count lines of code
find src -name "*.py" | xargs wc -l

# Search for text in code
grep -r "Platform Event" src/
```

## 🔍 Debugging

```bash
# Enable debug logging
# Edit config/.env and set:
LOG_LEVEL=DEBUG

# Run Python debugger
python -m pdb src/agent.py

# Check Python version
python3 --version

# Check installed packages
source venv/bin/activate
pip list

# Verify imports work
python -c "import anthropic; print('Anthropic SDK OK')"
python -c "from simple_salesforce import Salesforce; print('Salesforce SDK OK')"
```

## 🧹 Cleanup

```bash
# Remove virtual environment
rm -rf venv/

# Remove logs
rm -rf logs/*.log

# Remove Python cache
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Git clean (removes untracked files)
git clean -fd

# Full reset to last commit
git reset --hard HEAD
```

## 📦 Adding New Cluster Data

```bash
# Edit mock data
nano data/mock_insights.json

# Validate JSON
python -m json.tool data/mock_insights.json

# Test new cluster
python -c "
from src.insights_service import InsightsService
s = InsightsService()
print(s.get_cluster_insights('your-new-cluster-id'))
"
```

## 🔐 Security

```bash
# Check .env is not tracked
git status | grep .env
# Should return nothing (file is ignored)

# View what's ignored
cat .gitignore

# Make sure no secrets in commits
git log -p | grep -i "password\|token\|secret"
```

## 📊 Monitoring

```bash
# Check agent is running
ps aux | grep agent

# Monitor CPU/memory usage
top -pid $(pgrep -f "python -m src.agent")

# Check network connections
lsof -i -P | grep python

# View recent log entries
tail -20 logs/agent.log

# Search logs for errors
grep -i error logs/agent.log
grep -i exception logs/agent.log
```

## 🌐 Salesforce Commands (via Browser)

```
# Login to SFDC
https://login.salesforce.com (production)
https://test.salesforce.com (sandbox/developer)

# Quick Find shortcuts (in Setup)
Object Manager → Case
Developer Console
Platform Events
Apex Triggers
Debug Logs
```

## 🔧 Configuration Changes

```bash
# Edit agent config
nano config/config.yaml

# Edit environment variables
nano config/.env

# Validate YAML
python -c "import yaml; yaml.safe_load(open('config/config.yaml'))"

# View current config
cat config/config.yaml
```

## 📱 macOS Service (Launchd)

```bash
# Create launchd plist
nano ~/Library/LaunchAgents/com.insights.agent.plist

# Load service
launchctl load ~/Library/LaunchAgents/com.insights.agent.plist

# Unload service
launchctl unload ~/Library/LaunchAgents/com.insights.agent.plist

# Check service status
launchctl list | grep insights

# View service logs
tail -f logs/stdout.log
tail -f logs/stderr.log
```

## 🐍 Python Virtual Environment

```bash
# Activate venv
source venv/bin/activate

# Deactivate venv
deactivate

# Check active environment
which python
# Should show: /Users/soujain/insights-tool/venv/bin/python

# Install new package
pip install package-name

# Freeze dependencies
pip freeze > requirements.txt

# Install from requirements
pip install -r requirements.txt
```

## 📈 GitHub Actions

```bash
# View workflow status
open https://github.com/YOUR_USERNAME/sfdc-insights-agent/actions

# Manually trigger workflow (if configured)
gh workflow run test.yml

# View workflow logs
gh run list
gh run view RUN_ID
```

## 🆘 Emergency Commands

```bash
# Kill all Python processes (use carefully!)
pkill -9 python

# Check what's using a port
lsof -i :8000

# Force remove stuck process
kill -9 PID

# Restore from git if something broke
git reset --hard HEAD
git clean -fd

# Restore a single file
git checkout HEAD -- path/to/file.py
```

## 💡 Useful One-Liners

```bash
# Count total lines of Python code
find src -name "*.py" | xargs wc -l | tail -1

# Show all TODO comments in code
grep -rn "TODO" src/

# Find large files
find . -type f -size +1M

# Show git commit stats
git log --stat

# Show files changed in last commit
git diff --name-only HEAD~1 HEAD

# Create a backup
tar -czf backup-$(date +%Y%m%d).tar.gz \
  src/ config/ data/ tests/ *.md *.sh requirements.txt

# Extract backup
tar -xzf backup-20260601.tar.gz
```

## 🎯 Common Workflows

### First Time Setup
```bash
cd /Users/soujain/insights-tool
cp config/.env.example config/.env
nano config/.env  # Add credentials
./run_agent.sh
```

### Daily Development
```bash
cd /Users/soujain/insights-tool
source venv/bin/activate
# Make changes...
python -m src.agent  # Test
git add .
git commit -m "Description"
git push
```

### Deploy Update
```bash
git pull
source venv/bin/activate
pip install -r requirements.txt
./run_agent.sh
```

### Troubleshooting
```bash
tail -f logs/agent.log  # Check logs
./quick_test.sh         # Test components
nano config/.env        # Verify credentials
git status              # Check file changes
```

## 📚 Documentation Links

- Main README: `cat README.md`
- Quick Start: `cat QUICK_START.md`
- How to Run: `cat HOW_TO_RUN.md`
- Salesforce Setup: `cat SALESFORCE_SETUP.md`
- GitHub Setup: `cat GITHUB_SETUP.md`
- Project Summary: `cat PROJECT_SUMMARY.md`

---

**Pro Tip**: Bookmark this file! 🔖

```bash
# Create an alias for quick access
echo "alias insights='cd /Users/soujain/insights-tool && cat COMMANDS.md'" >> ~/.zshrc
source ~/.zshrc

# Now just type:
insights
```
