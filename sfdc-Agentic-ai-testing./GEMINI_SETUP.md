# Google Gemini API Setup Guide

## Why Gemini?
✅ **Completely FREE** - No credit card required  
✅ **Generous limits** - 1,500 requests/day (free tier)  
✅ **High quality** - Comparable to Claude for text generation  
✅ **Fast** - Quick response times  

---

## Step 1: Get Your Free API Key

1. **Go to Google AI Studio**:
   - Visit: https://aistudio.google.com/app/apikey

2. **Sign in with your Google account**
   - Use any personal or work Google account

3. **Create API Key**:
   - Click **"Get API Key"** or **"Create API Key"**
   - Select **"Create API key in new project"** (recommended)
   - Copy the API key (starts with `AIza...`)

4. **Save it securely** - You'll need this in the next step

---

## Step 2: Configure Your Environment

1. **Create your `.env` file**:
   ```bash
   cp config/.env.example config/.env
   ```

2. **Edit `config/.env`** and add your API key:
   ```bash
   # Google Gemini API (Free tier: 1500 requests/day)
   GEMINI_API_KEY=AIzaSy...your-actual-key-here
   
   # Keep your other Salesforce credentials as-is
   SFDC_USERNAME=your_email@example.com
   SFDC_PASSWORD=your_password
   SFDC_SECURITY_TOKEN=your_security_token
   SFDC_DOMAIN=test
   ```

---

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 4: Test the Integration

Run the standalone test:
```bash
python src/comment_generator.py
```

You should see:
- ✅ "Successfully generated comment using Google Gemini API"
- A formatted cluster insights comment

---

## Free Tier Limits

| Feature | Free Tier |
|---------|-----------|
| **Requests/minute** | 15 |
| **Requests/day** | 1,500 |
| **Tokens/minute** | 1 million |
| **Models** | Gemini 1.5 Flash, Gemini 1.5 Pro |

**This is more than enough** for most automation tasks!

---

## Troubleshooting

### Error: "API key not valid"
- Make sure you copied the entire key (starts with `AIza`)
- Check there are no extra spaces in the `.env` file
- Regenerate the key if needed

### Error: "Quota exceeded"
- You've hit the free tier limit (1500 requests/day)
- Wait 24 hours for quota reset
- Or upgrade to paid tier (not required for most uses)

### Error: "Module not found: google.generativeai"
- Run: `pip install google-generativeai`

---

## What Changed?

We replaced **Anthropic Claude API** with **Google Gemini API** in:

1. ✅ `requirements.txt` - Updated dependency
2. ✅ `src/comment_generator.py` - Replaced API client
3. ✅ `src/agent.py` - Updated environment variable
4. ✅ `config/.env.example` - Updated example config

---

## Next Steps

Once you have your API key configured:

1. Follow the main setup guide: `START_HERE.md`
2. Configure Salesforce credentials
3. Run the agent: `./run_agent.sh`

---

## Need Help?

- **Gemini API Docs**: https://ai.google.dev/tutorials/python_quickstart
- **Get API Key**: https://aistudio.google.com/app/apikey
- **Pricing**: https://ai.google.dev/pricing (Free tier is generous!)
