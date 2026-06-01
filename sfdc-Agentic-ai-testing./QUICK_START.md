# Quick Start Guide

Get the OpenShift Insights Agent running in under 30 minutes.

## Prerequisites Checklist

- [ ] Python 3.9+ installed (`python3 --version`)
- [ ] Salesforce Developer Org (free - see Step 1)
- [ ] Anthropic API key for Claude ([Get one here](https://console.anthropic.com/))
- [ ] 30 minutes of time

## Step 1: Salesforce Setup (15 minutes)

### Create Developer Org
1. Go to https://developer.salesforce.com/signup
2. Sign up (use any email, username must be email format)
3. Verify email and set password

### Quick Setup via Setup UI
1. **Custom Fields** (Setup → Object Manager → Case → Fields & Relationships):
   - New → Text → "Cluster ID" (255 chars)
   - New → Checkbox → "Auto Insights Posted"
   
2. **Platform Event** (Setup → Platform Events → New):
   - Label: "Case Created"
   - Fields: `Case_Id__c` (Text, 18), `Cluster_Id__c` (Text, 255)

3. **Apex Trigger** (Setup → Developer Console → File → New → Apex Trigger):
   - Name: `CaseEventPublisher`, Object: `Case`
   - Copy/paste trigger from [SALESFORCE_SETUP.md](SALESFORCE_SETUP.md#step-4-create-apex-trigger)

4. **Get Security Token** (Profile → Settings → Reset Security Token)
   - Check your email for the token

📖 **Detailed instructions**: See [SALESFORCE_SETUP.md](SALESFORCE_SETUP.md)

## Step 2: Python Agent Setup (10 minutes)

### Install Dependencies
```bash
cd /Users/soujain/insights-tool

# Create virtual environment and install
./run_agent.sh  # This will set up everything and start the agent
# Press Ctrl+C after it starts to continue setup
```

### Configure Credentials
```bash
# Copy the example environment file
cp config/.env.example config/.env

# Edit with your credentials
nano config/.env
```

Fill in:
```env
SFDC_USERNAME=your.username@example.com
SFDC_PASSWORD=YourPassword123
SFDC_SECURITY_TOKEN=AbCdEfGhIjKlMnOp
SFDC_DOMAIN=test
ANTHROPIC_API_KEY=sk-ant-your-api-key-here
LOG_LEVEL=INFO
```

### Test Components (Optional)
```bash
./quick_test.sh
```

## Step 3: Run & Test (5 minutes)

### Start the Agent
```bash
./run_agent.sh
```

Expected output:
```
=========================================
SFDC OpenShift Insights Agent
=========================================
✓ Authenticated with Salesforce
✓ Connected to Salesforce Streaming API
✓ Listening for events on /event/Case_Created__e
Agent is running. Press Ctrl+C to stop.
=========================================
```

### Create Test Case in Salesforce

1. Go to your Salesforce org
2. Click **Cases** tab → **New**
3. Fill in:
   - **Subject**: "Test OpenShift Issue"
   - **Status**: "New"
   - **Cluster ID**: `test-cluster-001` ⚠️ Important!
4. Click **Save**

### Verify It Worked

**In the Agent Logs** (within 5 seconds):
```
INFO - Processing case 500... with cluster test-cluster-001
INFO - Successfully posted internal comment
```

**In Salesforce**:
1. Open the case you just created
2. Click **Related** tab
3. Look under **Case Comments**
4. You should see a formatted internal comment with cluster insights! 🎉

## Available Test Cluster IDs

Use any of these in the **Cluster ID** field when creating test cases:

- `test-cluster-001` - Healthy AWS IPI cluster
- `prod-cluster-042` - Azure UPI cluster with warnings
- `rosa-cluster-99` - Managed ROSA cluster
- `assisted-cluster-23` - BareMetal assisted installer
- `aro-cluster-17` - Azure Red Hat OpenShift (ARO)

## What You Should See

When everything works, the internal comment will look like:

```
🔍 OpenShift Cluster Insights - Auto-Generated

**Cluster Overview**
- Cluster ID: test-cluster-001
- Version: 4.15.2
- Platform: AWS (us-east-1)
- Installation Type: IPI
- Node Count: 5 (3 control, 2 workers)
- Health Status: ✅ Healthy

**Support Tips**
- Cluster running latest stable 4.15.x release
- IPI installation suggests standard AWS configuration
- Verify AWS service quotas if scaling issues reported
```

## Troubleshooting

### "Authentication failed"
- Check username/password/token in `config/.env`
- Ensure `SFDC_DOMAIN=test` for Developer orgs
- Security token must be from most recent reset

### "No events received"
- Verify Apex trigger is saved and active
- Make sure you filled in the **Cluster ID** field
- Check Salesforce Debug Logs (Setup → Debug Logs)

### "Comment not posted"
- Check `logs/agent.log` for errors
- Verify case ID is valid
- Ensure CaseComment object permissions are correct

### "Claude API error"
- Verify `ANTHROPIC_API_KEY` in `.env`
- Check your API quota/limits
- Agent will fall back to basic formatting if Claude fails

## Next Steps

✅ **Working?** Great! Now you can:
- Add more test clusters to `data/mock_insights.json`
- Customize comment formatting in `config/config.yaml`
- Set up as macOS service (see [README.md](README.md))
- Plan Tableau API integration to replace mock data

📚 **Full Documentation**:
- [README.md](README.md) - Complete documentation
- [SALESFORCE_SETUP.md](SALESFORCE_SETUP.md) - Detailed SFDC setup
- Component testing: `./quick_test.sh`

## Architecture Overview

```
┌─────────────────┐
│ SFDC Developer  │
│      Org        │
└────────┬────────┘
         │ Platform Event
         │ Case_Created__e
         ↓
┌─────────────────┐
│  Event Listener │ (Python - aiosfstream)
│  (agent.py)     │
└────────┬────────┘
         │
         ├─→ Insights Service (mock_insights.json)
         │
         ├─→ Comment Generator (Claude API)
         │
         └─→ SFDC Client (simple-salesforce)
                   │
                   ↓
            Internal Comment Posted
```

## File Structure

```
insights-tool/
├── src/
│   ├── agent.py              # Main orchestrator ⭐
│   ├── sfdc_client.py        # Salesforce API
│   ├── event_listener.py     # Platform Events
│   ├── insights_service.py   # Mock data
│   └── comment_generator.py  # Claude AI
├── data/
│   └── mock_insights.json    # Test cluster data
├── config/
│   ├── config.yaml           # Settings
│   └── .env                  # Your credentials ⚠️
├── run_agent.sh             # Start script ⭐
└── quick_test.sh            # Component tests
```

## Questions?

1. Check the full [README.md](README.md)
2. Review [SALESFORCE_SETUP.md](SALESFORCE_SETUP.md)
3. Enable debug logging: `LOG_LEVEL=DEBUG` in `.env`
4. Check logs in `logs/agent.log`
