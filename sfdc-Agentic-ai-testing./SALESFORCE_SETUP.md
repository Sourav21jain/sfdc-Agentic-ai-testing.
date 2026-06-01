# Salesforce Developer Org Setup Guide

This guide walks through setting up a Salesforce Developer Edition org for testing the OpenShift Insights Agent.

## Step 1: Create Developer Org

1. Visit https://developer.salesforce.com/signup
2. Fill in the form:
   - **First Name**: Your first name
   - **Last Name**: Your last name
   - **Email**: Use a valid email (you'll need to verify it)
   - **Username**: Must be email format but doesn't need to be a real email (e.g., `yourname.insights@example.com`)
   - **Role**: Developer
   - **Company**: Your company or personal name
3. Click **Sign me up**
4. Check your email and click the verification link
5. Set your password
6. You're now in your Developer org!

## Step 2: Create Custom Fields on Case

### Cluster_ID__c Field

1. Click the **Setup** gear icon (top right)
2. In the Quick Find box, type `Object Manager`
3. Click **Object Manager**
4. Find and click **Case**
5. Click **Fields & Relationships**
6. Click **New** button
7. Select **Text** as field type, click **Next**
8. Fill in:
   - **Field Label**: `Cluster ID`
   - **Length**: `255`
   - **Field Name**: `Cluster_ID` (this will become `Cluster_ID__c`)
9. Click **Next** through the remaining screens
10. Click **Save**

### Auto_Insights_Posted__c Field

1. Still in **Case** → **Fields & Relationships**
2. Click **New**
3. Select **Checkbox** as field type, click **Next**
4. Fill in:
   - **Field Label**: `Auto Insights Posted`
   - **Field Name**: `Auto_Insights_Posted`
   - **Default Value**: Unchecked
5. Click **Next** through remaining screens
6. Click **Save**

### Add Fields to Page Layout

1. Still in **Object Manager** → **Case**
2. Click **Page Layouts**
3. Click **Case Layout**
4. Find the fields in the top section and drag them to the **Case Information** section
5. Click **Save**

## Step 3: Create Platform Event

1. In Setup, Quick Find box, type `Platform Events`
2. Click **Platform Events**
3. Click **New Platform Event**
4. Fill in:
   - **Label**: `Case Created`
   - **Plural Label**: `Case Created Events`
   - **Object Name**: `Case_Created` (will become `Case_Created__e`)
5. Click **Save**

### Add Fields to Platform Event

1. You're now on the Platform Event detail page
2. Scroll to **Custom Fields & Relationships**
3. Click **New**
4. Create first field:
   - **Type**: Text
   - **Field Label**: `Case Id`
   - **Length**: `18`
   - **Field Name**: `Case_Id`
   - Click **Save & New**
5. Create second field:
   - **Type**: Text
   - **Field Label**: `Cluster Id`
   - **Length**: `255`
   - **Field Name**: `Cluster_Id`
   - Click **Save**

## Step 4: Create Apex Trigger

1. In Setup, Quick Find box, type `Apex Triggers`
2. Click **Apex Triggers**
3. Click **Developer Console** (or use Setup → Developer Console)

**Alternative: In Developer Console**
1. File → New → Apex Trigger
2. Name: `CaseEventPublisher`
3. sObject: `Case`
4. Paste this code:

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
        
        // Log any errors
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

5. Click **Save**

### Test the Trigger

1. In Developer Console, click **Debug** → **Open Execute Anonymous Window**
2. Paste:
```apex
Case testCase = new Case(
    Subject = 'Test Case for Event',
    Status = 'New',
    Origin = 'Web',
    Cluster_ID__c = 'test-cluster-001'
);
insert testCase;
System.debug('Created case: ' + testCase.Id);
```
3. Click **Execute**
4. Check the logs - you should see the case created successfully

## Step 5: Get Your Security Token

1. Click your profile icon (top right)
2. Click **Settings**
3. In the left sidebar, under **Personal**, click **Reset My Security Token**
4. Click **Reset Security Token** button
5. Check your email - you'll receive the new security token
6. **Save this token** - you'll need it in the `.env` file

## Step 6: Find Your Username and Password

- **Username**: This is what you used to sign up (the email-format username)
- **Password**: This is what you set when you verified your account
- **Security Token**: From Step 5 above

## Step 7: Configure the Python Agent

1. Edit `config/.env` file:
```
SFDC_USERNAME=yourname.insights@example.com
SFDC_PASSWORD=YourPassword123
SFDC_SECURITY_TOKEN=AbCdEfGhIjKlMnOpQrSt
SFDC_DOMAIN=test
ANTHROPIC_API_KEY=sk-ant-your-key-here
LOG_LEVEL=INFO
```

**Important**: The code automatically appends the security token to the password, so keep them separate in the `.env` file.

## Step 8: Verify Setup

### Check via Workbench (Optional)

1. Go to https://workbench.developerforce.com
2. Login with your credentials
3. Environment: **Production** (Developer orgs count as production)
4. API Version: Latest
5. Login
6. Go to **Info** → **Standard & Custom Objects**
7. Find **Case** and verify your custom fields exist
8. Find **Case_Created__e** and verify it exists

### Check via Salesforce UI

1. Go to the **Cases** tab
2. Click **New**
3. Verify you can see the **Cluster ID** field
4. Create a test case with:
   - Subject: `Test OpenShift Case`
   - Status: `New`
   - Cluster ID: `test-cluster-001`
5. Click **Save**
6. Verify the case is created

## Troubleshooting

### Can't Find Object Manager
- Make sure you're in **Setup** (gear icon, top right)
- Use the **Quick Find** search box on the left

### Custom Fields Not Showing on Case Form
- Go to **Setup** → **Object Manager** → **Case** → **Page Layouts**
- Edit the **Case Layout**
- Drag your custom fields onto the layout

### Trigger Won't Save
- Make sure you're in Developer Console
- Check for syntax errors
- Ensure the Platform Event `Case_Created__e` exists first

### Security Token Email Not Received
- Check spam folder
- Wait a few minutes
- Make sure your email is verified in your Salesforce profile

### Authentication Fails from Python
- Double-check username (it's case-sensitive)
- Verify password is correct
- Ensure security token is from the most recent reset
- For Developer orgs, use `SFDC_DOMAIN=test` (not `login`)

## Next Steps

After completing this setup:
1. Return to the main [README.md](README.md)
2. Continue with **Part 2: Python Agent Setup**
3. Test the end-to-end flow

## Resources

- [Salesforce Developer Documentation](https://developer.salesforce.com/docs)
- [Platform Events Guide](https://developer.salesforce.com/docs/atlas.en-us.platform_events.meta/platform_events/)
- [Apex Triggers](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_triggers.htm)
