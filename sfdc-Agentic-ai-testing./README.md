# SFDC OpenShift Insights Auto-Comment Agent

An AI-powered agent that automatically posts OpenShift cluster insights as internal comments on Salesforce cases when they are created.

## Overview

This agent listens for Salesforce Platform Events when new cases are created with cluster IDs, fetches cluster insights data (currently from mock data, designed for future Tableau integration), and uses Google Gemini AI to generate well-formatted internal comments for support engineers.

## Architecture

```
SFDC Developer Org → Platform Event (Case_Created__e)
        ↓
Event Listener (aiosfstream)
        ↓
Insights Service (Mock Data / Future: Tableau API)
        ↓
Comment Generator (Google Gemini AI)
        ↓
SFDC Client → Post Internal Comment
```

## Features

- 🎯 **Real-time Event Processing**: Listens to Salesforce Platform Events
- 🤖 **AI-Powered Formatting**: Uses Google Gemini API (FREE) to generate clear, actionable comments
- 📊 **Mock Insights Data**: Simulates Tableau data source (ready for future integration)
- 🔄 **Automatic Retry Logic**: Handles transient failures gracefully
- ✅ **Idempotency**: Prevents duplicate comments on the same case
- 📝 **Comprehensive Logging**: Track all operations and errors

## Prerequisites

- Python 3.9+
- Salesforce Developer Edition Org (free)
- Google Gemini API key (100% FREE - no credit card required)
- macOS (tested) or Linux

## Project Structure

```
insights-tool/
├── src/
│   ├── agent.py              # Main orchestrator
│   ├── sfdc_client.py        # Salesforce API wrapper
│   ├── event_listener.py     # Platform Event streaming
│   ├── insights_service.py   # Mock Tableau data service
│   └── comment_generator.py  # AI comment formatting
├── data/
│   └── mock_insights.json    # Sample cluster data
├── config/
│   ├── config.yaml           # Application configuration
│   ├── .env.example          # Environment variables template
│   └── .env                  # Your credentials (create this)
├── logs/                     # Application logs
├── requirements.txt          # Python dependencies
├── run_agent.sh             # Launcher script
└── README.md                # This file
```

## Setup Instructions

### Part 1: Salesforce Developer Org Setup

#### 1.1 Create Developer Org
1. Go to https://developer.salesforce.com/signup
2. Fill out the form and create a free Developer Edition org
3. Verify your email and set your password
4. Log in to your new org

#### 1.2 Create Custom Fields on Case Object
1. Navigate to **Setup** → **Object Manager** → **Case**
2. Click **Fields & Relationships** → **New**
3. Create field: `Cluster_ID__c`
   - Field Type: Text
   - Length: 255
   - Field Label: Cluster ID
   - Field Name: Cluster_ID
4. Create field: `Auto_Insights_Posted__c`
   - Field Type: Checkbox
   - Field Label: Auto Insights Posted
   - Field Name: Auto_Insights_Posted
   - Default: Unchecked

#### 1.3 Create Platform Event
1. Navigate to **Setup** → **Platform Events** → **New Platform Event**
2. Create event: `Case_Created`
   - Label: Case Created
   - Plural Label: Case Created Events
   - Object Name: `Case_Created__e`
3. Add fields to the Platform Event:
   - `Case_Id__c` (Text, Length: 18)
   - `Cluster_Id__c` (Text, Length: 255)

#### 1.4 Create Apex Trigger
1. Navigate to **Setup** → **Apex Triggers** → **New**
2. Select Object: **Case**
3. Paste the following trigger code:

```apex
trigger CaseEventPublisher on Case (after insert) {
    List<Case_Created__e> events = new List<Case_Created__e>();
    
    for (Case c : Trigger.new) {
        // Only publish event if Cluster ID is populated
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
                    System.debug('Error publishing event: ' + error.getMessage());
                }
            }
        }
    }
}
```

4. Save the trigger

#### 1.5 Get Security Token
1. Click your profile icon → **Settings**
2. Navigate to **Personal** → **Reset My Security Token**
3. Click **Reset Security Token**
4. Check your email for the new security token

### Part 2: Python Agent Setup

#### 2.1 Clone/Navigate to Project
```bash
cd /Users/soujain/insights-tool
```

#### 2.2 Configure Environment Variables
```bash
# Copy the example file
cp config/.env.example config/.env

# Edit with your credentials
nano config/.env
```

Fill in your Salesforce and Google Gemini credentials:
```
SFDC_USERNAME=your_email@example.com
SFDC_PASSWORD=your_salesforce_password
SFDC_SECURITY_TOKEN=your_security_token_from_email
SFDC_DOMAIN=test
GEMINI_API_KEY=AIzaSy...your-gemini-api-key
LOG_LEVEL=INFO
```

**Get your FREE Gemini API key**: https://aistudio.google.com/app/apikey

#### 2.3 Install Dependencies
```bash
# The run_agent.sh script will create venv and install dependencies
# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Part 3: Testing Individual Components

#### Test Mock Insights Service
```bash
source venv/bin/activate
python -m src.insights_service
```

Expected output:
```
✓ Found insights for test-cluster-001
✓ Correctly returned None for non-existent cluster
✓ Available cluster IDs: test-cluster-001, prod-cluster-042, ...
```

#### Test SFDC Client
```bash
source venv/bin/activate
python -m src.sfdc_client
```

Expected output:
```
✓ Authentication successful
```

#### Test Comment Generator
```bash
source venv/bin/activate
python -m src.comment_generator
```

This will generate a sample AI-formatted comment.

#### Test Event Listener (Optional)
```bash
source venv/bin/activate
python -m src.event_listener
```

This will connect to SFDC and wait for Platform Events.

### Part 4: Running the Agent

#### Start the Agent
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

#### Test End-to-End

1. **In Salesforce**, create a new case:
   - Navigate to the **Cases** tab
   - Click **New**
   - Fill in required fields (Subject, Status, etc.)
   - **Important**: Set `Cluster ID` field to `test-cluster-001`
   - Click **Save**

2. **Watch the agent logs** - within 5 seconds you should see:
   ```
   INFO - Received event: {...}
   INFO - Processing case 500... with cluster test-cluster-001
   INFO - Found insights for cluster: test-cluster-001
   INFO - Successfully generated comment using Google Gemini API
   INFO - Successfully posted internal comment ... to case 500...
   INFO - Successfully processed case 500...
   ```

3. **Verify in Salesforce**:
   - Open the case you just created
   - Click on the **Related** tab
   - Look under **Case Comments**
   - You should see an internal comment with formatted cluster insights

## Configuration

### config/config.yaml

Customize agent behavior:
```yaml
agent:
  comment_prefix: "🔍 OpenShift Cluster Insights - Auto-Generated"
  max_retries: 3
  retry_delay_seconds: 5
  include_support_tips: true  # AI-generated support recommendations
```

### Mock Cluster Data

Edit `data/mock_insights.json` to add more test clusters:
```json
{
  "clusters": {
    "your-cluster-id": {
      "cluster_id": "your-cluster-id",
      "version": "4.15.2",
      "platform": "AWS",
      "install_type": "IPI",
      ...
    }
  }
}
```

## Running as macOS Service (Optional)

To run the agent automatically on system boot:

1. Create a launchd plist file:
```bash
cat > ~/Library/LaunchAgents/com.insights.agent.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.insights.agent</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/soujain/insights-tool/run_agent.sh</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/soujain/insights-tool</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/Users/soujain/insights-tool/logs/stdout.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/soujain/insights-tool/logs/stderr.log</string>
</dict>
</plist>
EOF
```

2. Load the service:
```bash
launchctl load ~/Library/LaunchAgents/com.insights.agent.plist
```

3. Check status:
```bash
launchctl list | grep insights
```

4. Unload if needed:
```bash
launchctl unload ~/Library/LaunchAgents/com.insights.agent.plist
```

## Troubleshooting

### Agent fails to authenticate
- Verify credentials in `config/.env`
- Ensure security token is appended to password (the code does this automatically)
- Check that SFDC_DOMAIN is set to `test` for Developer orgs

### No events received
- Verify the Apex trigger is active in Salesforce
- Ensure the Platform Event `Case_Created__e` exists
- Check that you're setting the `Cluster_ID__c` field when creating cases
- Look at Salesforce Debug Logs for trigger execution

### Comment not posted
- Check agent logs in `logs/agent.log`
- Verify CaseComment object permissions in Salesforce
- Ensure the case ID is valid

### Gemini API errors
- Verify `GEMINI_API_KEY` in `.env`
- Check API quota/limits (1,500 requests/day on free tier)
- Review logs for specific error messages
- Get your free API key: https://aistudio.google.com/app/apikey

## Future Enhancements

- [ ] Replace mock data with Tableau REST API integration
- [ ] Support multiple cluster IDs per case
- [ ] Include historical trend analysis
- [ ] Fetch and include active cluster alerts
- [ ] Add webhook fallback for SFDC Outbound Messages
- [ ] Deploy to cloud (AWS Lambda, Heroku)
- [ ] Add web dashboard for monitoring
- [ ] Support batch processing of existing cases

## Architecture Notes

### Why Platform Events?
- Real-time processing (vs polling)
- Native Salesforce integration
- Scalable and reliable
- No custom REST endpoint needed

### Why Google Gemini API?
- 100% FREE with generous limits (1,500 requests/day)
- No credit card required
- Superior formatting and contextual awareness
- Can provide support tips based on cluster config
- Handles edge cases better than templates

### Why Mock Data?
- Tableau API requires authentication and may not be available initially
- Easy to test and develop against
- Simple to swap with real API later (same interface)

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review logs in `logs/agent.log`
3. Enable DEBUG logging: `LOG_LEVEL=DEBUG` in `.env`

## License

MIT
