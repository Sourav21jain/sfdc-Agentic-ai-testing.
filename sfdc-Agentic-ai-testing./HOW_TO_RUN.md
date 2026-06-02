# How to Run This Agent - Step by Step

## Prerequisites Check

Before starting, make sure you have:
- [ ] Python 3.9 or higher installed
- [ ] A Salesforce Developer Org (we'll set this up)
- [ ] A Google Gemini API key (we'll get this - **100% FREE**)

Check Python version:
```bash
python3 --version
# Should show 3.9 or higher
```

## Step 1: Get FREE Google Gemini API Key (2 minutes)

1. Go to https://aistudio.google.com/app/apikey
2. Sign in with your Google account (personal or work)
3. Click **"Create API Key"** or **"Get API Key"**
4. Select **"Create API key in new project"** (recommended)
5. Copy the key (starts with `AIza...`)
6. Save it somewhere safe

**Why Gemini?**
- ✅ Completely FREE (no credit card required)
- ✅ 1,500 requests per day (free tier)
- ✅ High quality AI responses
- ✅ No expiration on free tier

## Step 2: Set Up Salesforce Developer Org (15 minutes)

### 2.1 Create the Org

1. Go to https://developer.salesforce.com/signup
2. Fill out the form:
   - Use your real email (you'll need to verify)
   - Username must be email format (e.g., `yourname.insights@mycompany.com`)
   - This username doesn't need to be a real email
3. Click "Sign me up"
4. Check your email and verify
5. Set your password
6. Log in to your new org

### 2.2 Add Custom Fields to Case

1. Click the **⚙️ Setup** gear (top right)
2. In the Quick Find box (left side), type: `Object Manager`
3. Click **Object Manager**
4. Find and click **Case**
5. Click **Fields & Relationships** in the left menu
6. Click **New** button

**First Field - Cluster ID:**
- Data Type: **Text**
- Click Next
- Field Label: `Cluster ID`
- Length: `255`
- Field Name: `Cluster_ID` (auto-fills)
- Click Next → Next → Save

**Second Field - Auto Insights Posted:**
- Click **New** again
- Data Type: **Checkbox**
- Click Next
- Field Label: `Auto Insights Posted`
- Field Name: `Auto_Insights_Posted`
- Default: **Unchecked**
- Click Next → Next → Save

### 2.3 Add Fields to Page Layout

1. Still in Case, click **Page Layouts** (left menu)
2. Click **Case Layout**
3. Look at the top section for available fields
4. Drag **Cluster ID** to the "Case Information" section
5. Drag **Auto Insights Posted** to the "Case Information" section
6. Click **Save**

### 2.4 Create Platform Event

1. In Quick Find box, type: `Platform Events`
2. Click **Platform Events**
3. Click **New Platform Event**
4. Fill in:
   - Label: `Case Created`
   - Plural Label: `Case Created Events`
   - Object Name: `Case_Created` (auto-fills to `Case_Created__e`)
5. Click **Save**

**Add Event Fields:**

You're now on the Platform Event detail page.

1. Scroll to **Custom Fields & Relationships**
2. Click **New**

**First Event Field:**
- Data Type: **Text**
- Click Next
- Field Label: `Case Id`
- Length: `18`
- Field Name: `Case_Id`
- Click **Save & New**

**Second Event Field:**
- Data Type: **Text**
- Click Next
- Field Label: `Cluster Id`
- Length: `255`
- Field Name: `Cluster_Id`
- Click **Save**

### 2.5 Create Apex Trigger

1. In Quick Find, type: `Developer Console`
2. Click **Developer Console** (opens new window)
3. In Developer Console: **File** → **New** → **Apex Trigger**
4. Name: `CaseEventPublisher`
5. Object: `Case`
6. Click **Submit**

**Paste this code:**
```apex
trigger CaseEventPublisher on Case (after insert) {
    List<Case_Created__e> events = new List<Case_Created__e>();
    
    for (Case c : Trigger.new) {
        if (c.Cluster_ID__c != null && c.Cluster_ID__c != '') {
            Case_Created__e event = new Case_Created__e(
                Case_Id__c = c.Id,
                Cluster_Id__c = c.Cluster_ID__c
            );
            events.add(event);
        }
    }
    
    if (!events.isEmpty()) {
        List<Database.SaveResult> results = EventBus.publish(events);
        for (Database.SaveResult result : results) {
            if (!result.isSuccess()) {
                for (Database.Error error : result.getErrors()) {
                    System.debug('Error: ' + error.getMessage());
                }
            }
        }
    }
}
```

7. Click **File** → **Save**
8. Close Developer Console

### 2.6 Get Security Token

1. Click your **profile picture** (top right)
2. Click **Settings**
3. In the left menu under "Personal", click **Reset My Security Token**
4. Click **Reset Security Token**
5. Check your email for the token
6. **Copy the token** - you'll need it next

## Step 3: Configure the Python Agent (5 minutes)

### 3.1 Open Terminal and Navigate to Project

```bash
cd /Users/soujain/insights-tool
```

### 3.2 Create Environment File

```bash
# Copy the example file
cp config/.env.example config/.env

# Open it for editing
nano config/.env
```

### 3.3 Fill in Your Credentials

Replace the placeholder values with your actual credentials:

```env
SFDC_USERNAME=yourname.insights@mycompany.com
SFDC_PASSWORD=YourSalesforcePassword123
SFDC_SECURITY_TOKEN=AbCdEfGhIjKlMnOpQrStUvWxYz
SFDC_DOMAIN=test
GEMINI_API_KEY=AIzaSy...your-actual-gemini-key-here
LOG_LEVEL=INFO
```

**Important**:
- `SFDC_USERNAME`: Your Salesforce username (from Step 2.1)
- `SFDC_PASSWORD`: Your Salesforce password (from Step 2.1)
- `SFDC_SECURITY_TOKEN`: The token from your email (Step 2.6)
- `SFDC_DOMAIN`: Use `test` for Developer Edition orgs
- `GEMINI_API_KEY`: Your Google Gemini API key (from Step 1)

Save the file:
- Press `Ctrl + X`
- Press `Y` to confirm
- Press `Enter`

## Step 4: Run the Agent (2 minutes)

### 4.1 Start the Agent

```bash
./run_agent.sh
```

This will:
- Create a Python virtual environment
- Install all dependencies
- Start the agent

**Expected Output:**
```
=========================================
SFDC OpenShift Insights Agent
=========================================
Activating virtual environment...
Installing dependencies...
✓ Dependencies installed
Starting agent...

=========================================
SFDC OpenShift Insights Agent Starting
=========================================
✓ Authenticated with Salesforce
✓ Connected to Salesforce Streaming API
✓ Listening for events on /event/Case_Created__e
Agent is running. Press Ctrl+C to stop.
=========================================
```

### 4.2 Keep This Terminal Open

Leave this terminal running - it's listening for events!

## Step 5: Test It! (2 minutes)

### 5.1 Create a Test Case in Salesforce

1. Go back to your Salesforce org (in browser)
2. Click the **App Launcher** (9 dots, top left)
3. Search for and click **Service**
4. Click the **Cases** tab
5. Click **New** button

Fill in the case:
- **Status**: New
- **Case Origin**: Web
- **Subject**: Test OpenShift cluster issue
- **Description**: Testing the insights agent
- **Cluster ID**: `test-cluster-001` ⚠️ **IMPORTANT - Must fill this!**

6. Click **Save**

### 5.2 Watch the Agent Logs

Switch back to your terminal. Within 5-10 seconds you should see:

```
INFO - Received event: {...}
INFO - Processing case 500... with cluster test-cluster-001
INFO - Found insights for cluster: test-cluster-001
INFO - Successfully generated comment using Google Gemini API
INFO - Successfully posted internal comment ... to case 500...
INFO - Successfully processed case 500...
```

### 5.3 Check Salesforce for the Comment

1. In Salesforce, go to the case you just created
2. Click the **Related** tab
3. Scroll to **Case Comments** section
4. You should see an internal comment like:

```
🔍 OpenShift Cluster Insights - Auto-Generated

**Cluster Overview**
- Cluster ID: test-cluster-001
- Version: 4.15.2
- Platform: AWS (us-east-1)
...
```

🎉 **SUCCESS!** Your agent is working!

## Available Test Cluster IDs

Try creating more cases with these cluster IDs:

- `test-cluster-001` - Healthy AWS IPI cluster
- `prod-cluster-042` - Azure UPI with warnings (shows alerts)
- `rosa-cluster-99` - Managed ROSA cluster
- `assisted-cluster-23` - BareMetal assisted installer
- `aro-cluster-17` - Azure Red Hat OpenShift

## Stopping the Agent

Press `Ctrl + C` in the terminal where the agent is running.

## Troubleshooting

### "Authentication failed"
- Double-check your `.env` file credentials
- Make sure there are no extra spaces
- Ensure `SFDC_DOMAIN=test` for Developer orgs
- Verify your security token is the most recent one

### "No events received"
- Verify the Apex trigger is saved in Developer Console
- Make sure you filled in the **Cluster ID** field when creating the case
- Try creating another case

### "Module not found" errors
```bash
# Make sure you're in the project directory
cd /Users/soujain/insights-tool

# Reinstall dependencies
source venv/bin/activate
pip install -r requirements.txt
```

### "Config file not found"
```bash
# Make sure .env exists
ls -la config/.env

# If not, copy the example
cp config/.env.example config/.env
# Then edit it with your credentials
```

## Running in Background (Optional)

To run the agent in the background:

```bash
# Start in background
nohup ./run_agent.sh > logs/nohup.log 2>&1 &

# Check if it's running
ps aux | grep agent

# View logs
tail -f logs/agent.log

# Stop it
pkill -f "python -m src.agent"
```

## Next Steps

Now that it's working:

1. **Add More Clusters**: Edit `data/mock_insights.json`
2. **Customize Comments**: Edit `config/config.yaml`
3. **Deploy to Cloud**: See README.md for Heroku/AWS options
4. **Integrate Tableau**: Replace mock data with real Tableau API

## Need Help?

Check these files:
- `QUICK_START.md` - Quick reference
- `README.md` - Full documentation  
- `SALESFORCE_SETUP.md` - Detailed SFDC setup
- `logs/agent.log` - Application logs

Enable debug logging:
```bash
# Edit .env file
nano config/.env

# Change this line:
LOG_LEVEL=DEBUG

# Restart the agent
```
