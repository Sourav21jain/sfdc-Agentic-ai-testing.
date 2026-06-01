# 🚀 START HERE - Complete Setup Guide

Welcome! This guide will get you from zero to a running agent in **30-40 minutes**.

## 📋 What You're Building

An AI agent that:
1. Listens to Salesforce for new cases with cluster IDs
2. Fetches OpenShift cluster insights automatically
3. Uses Claude AI to format the data
4. Posts a beautiful internal comment on the case

Support engineers get instant context without searching!

## ⚡ Quick Path (Choose Your Route)

### Route A: Just Run It (Recommended First)
**Time**: 30 minutes

1. **[HOW_TO_RUN.md](HOW_TO_RUN.md)** ← Start here!
   - Step-by-step setup
   - Screenshots and examples
   - Troubleshooting included

### Route B: Quick Reference
**Time**: 15 minutes if you know SFDC/Python

1. **[QUICK_START.md](QUICK_START.md)** ← Fast track
   - Condensed instructions
   - For experienced developers

## 📚 All Documentation (Pick What You Need)

### Getting Started
- **[START_HERE.md](START_HERE.md)** ← You are here!
- **[HOW_TO_RUN.md](HOW_TO_RUN.md)** ← Best for first-time setup
- **[QUICK_START.md](QUICK_START.md)** ← Fast track guide

### Setup Details
- **[SALESFORCE_SETUP.md](SALESFORCE_SETUP.md)** ← SFDC configuration details
- **[GITHUB_SETUP.md](GITHUB_SETUP.md)** ← Push to GitHub
- **[COMMANDS.md](COMMANDS.md)** ← All commands in one place

### Reference
- **[README.md](README.md)** ← Complete documentation
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** ← Architecture & tech details

## 🎯 Your Next Steps

### Step 1: Read HOW_TO_RUN.md (2 minutes)
```bash
cat HOW_TO_RUN.md
# or
open HOW_TO_RUN.md
```

### Step 2: Get Prerequisites (10 minutes)
- [ ] Salesforce Developer Org (free) - https://developer.salesforce.com/signup
- [ ] Anthropic API Key (free tier available) - https://console.anthropic.com/
- [ ] Python 3.9+ installed - Check with: `python3 --version`

### Step 3: Configure SFDC (15 minutes)
Follow **[SALESFORCE_SETUP.md](SALESFORCE_SETUP.md)** or the SFDC section in **[HOW_TO_RUN.md](HOW_TO_RUN.md)**

### Step 4: Configure & Run Agent (5 minutes)
```bash
# Copy environment file
cp config/.env.example config/.env

# Edit with your credentials
nano config/.env

# Run the agent
./run_agent.sh
```

### Step 5: Test It! (3 minutes)
1. Create a case in Salesforce
2. Set Cluster ID = `test-cluster-001`
3. Watch the magic happen!

### Step 6: Push to GitHub (5 minutes)
Follow **[GITHUB_SETUP.md](GITHUB_SETUP.md)**

## 🆘 Getting Help

### Common Issues

**"Can't find Python"**
```bash
# Install Python 3.9+
brew install python@3.9
# or visit python.org
```

**"Authentication failed"**
- Check credentials in `config/.env`
- Verify security token is most recent
- Make sure `SFDC_DOMAIN=test`

**"No events received"**
- Verify Apex trigger is saved
- Check you filled in Cluster ID field
- Look at Salesforce Debug Logs

### Where to Look

1. **Logs**: `tail -f logs/agent.log`
2. **Test Components**: `./quick_test.sh`
3. **Documentation**: Check the file matching your issue
4. **Debug Mode**: Set `LOG_LEVEL=DEBUG` in `.env`

## 📖 Documentation Map

```
START_HERE.md (you are here)
    ↓
HOW_TO_RUN.md (step-by-step instructions)
    ↓
SALESFORCE_SETUP.md (detailed SFDC setup)
    ↓
Agent Running! ✅
    ↓
GITHUB_SETUP.md (push to GitHub)
    ↓
COMMANDS.md (reference for daily use)

README.md (complete reference)
PROJECT_SUMMARY.md (architecture details)
QUICK_START.md (experienced users)
```

## 🎓 Learning Path

**First Time?** Follow in order:
1. START_HERE.md (this file)
2. HOW_TO_RUN.md
3. Create a test case
4. Explore the code

**Experienced?** Fast track:
1. QUICK_START.md
2. Configure `.env`
3. Run it!

## 💡 What Each File Does

| File | Purpose | Read When... |
|------|---------|--------------|
| **START_HERE.md** | Overview & navigation | First time |
| **HOW_TO_RUN.md** | Detailed setup steps | Setting up |
| **QUICK_START.md** | Condensed guide | You know SFDC/Python |
| **SALESFORCE_SETUP.md** | SFDC configuration | Setting up SFDC |
| **GITHUB_SETUP.md** | Push to GitHub | Sharing code |
| **COMMANDS.md** | Command reference | Daily use |
| **README.md** | Full documentation | Need complete info |
| **PROJECT_SUMMARY.md** | Technical details | Understanding architecture |

## ✅ Checklist

Use this to track your progress:

### Prerequisites
- [ ] Python 3.9+ installed (`python3 --version`)
- [ ] Salesforce Developer Org created
- [ ] Anthropic API key obtained
- [ ] GitHub account (for publishing)

### Salesforce Setup
- [ ] Custom fields created (Cluster_ID__c, Auto_Insights_Posted__c)
- [ ] Platform Event created (Case_Created__e)
- [ ] Apex Trigger created (CaseEventPublisher)
- [ ] Security token obtained

### Agent Setup
- [ ] Environment file configured (`config/.env`)
- [ ] Dependencies installed (automatic with `./run_agent.sh`)
- [ ] Agent started successfully
- [ ] Logs show "Authenticated with Salesforce"

### Testing
- [ ] Created test case with Cluster ID
- [ ] Agent processed the event
- [ ] Internal comment appeared on case
- [ ] Comment formatting looks good

### Optional
- [ ] Pushed to GitHub
- [ ] Added more cluster data
- [ ] Customized comment format
- [ ] Set up as background service

## 🎯 Success Criteria

You'll know it's working when:

1. ✅ Agent starts without errors
2. ✅ Logs show "Connected to Salesforce Streaming API"
3. ✅ Creating a case triggers an event
4. ✅ Internal comment appears within 10 seconds
5. ✅ Comment is well-formatted and helpful

## 🚀 After It's Working

**Customize**:
- Add more cluster data: Edit `data/mock_insights.json`
- Change comment format: Edit `config/config.yaml`
- Modify AI behavior: Edit `src/comment_generator.py`

**Deploy**:
- Run as macOS service: See README.md → "Running as macOS Service"
- Deploy to cloud: See README.md → "Future Enhancements"

**Extend**:
- Integrate Tableau API: Replace `insights_service.py`
- Add more data fields: Update mock data structure
- Multi-cluster support: Modify `agent.py`

## 📞 Support Resources

**Documentation**:
- This project: All the `.md` files
- Salesforce: https://developer.salesforce.com/docs
- Anthropic: https://docs.anthropic.com/

**Debugging**:
```bash
# View logs
tail -f logs/agent.log

# Test components
./quick_test.sh

# Enable debug mode
# In config/.env, set:
LOG_LEVEL=DEBUG
```

## 🎉 You're Ready!

**→ Open [HOW_TO_RUN.md](HOW_TO_RUN.md) and start building!**

Good luck! The agent is well-documented and ready to help support engineers save time. 🚀

---

**Quick Links**:
- [How to Run](HOW_TO_RUN.md) ← Start setup
- [Quick Start](QUICK_START.md) ← Fast track
- [Commands Reference](COMMANDS.md) ← Daily commands
- [GitHub Setup](GITHUB_SETUP.md) ← Publish code
- [Full README](README.md) ← Complete docs
