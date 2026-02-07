# Blue Jays Home Games Calendar Automation

Automatically add Toronto Blue Jays home games to your Google Calendar!

## Features

- ✅ Fetches latest Blue Jays schedule from ESPN
- ✅ Filters for home games only
- ✅ Automatically adds games to Google Calendar
- ✅ Prevents duplicate entries
- ✅ Includes game reminders (1 hour and 1 day before)
- ✅ Sets proper venue (Rogers Centre)
- ✅ Color-codes games in blue
- ✅ Handles TBD game times

## Prerequisites

1. **Python 3.7+** installed on your computer
2. **Google Account** with Google Calendar access

## Setup Instructions

### Step 1: Install Required Packages

Open your terminal/command prompt and run:

```bash
pip install requests beautifulsoup4 google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### Step 2: Enable Google Calendar API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable the **Google Calendar API**:
   - Click "Enable APIs and Services"
   - Search for "Google Calendar API"
   - Click "Enable"
4. Create OAuth 2.0 credentials:
   - Go to "Credentials" in the sidebar
   - Click "Create Credentials" → "OAuth client ID"
   - Choose "Desktop app" as application type
   - Name it "Blue Jays Calendar Automation"
   - Click "Create"
5. Download the credentials:
   - Click the download icon next to your new OAuth client
   - Save the file as `credentials.json` in the same folder as the script

### Step 3: Run the Script

```bash
python blue_jays_calendar_automation.py
```

**First Run:**
- A browser window will open asking you to authorize the app
- Sign in with your Google account
- Allow the app to access your calendar
- A `token.pickle` file will be created for future runs

**Subsequent Runs:**
- No browser authentication needed (uses saved token)
- Automatically checks for and adds new games

## Automating the Script

### Option A: Manual Runs
Run the script whenever you want to update your calendar:
```bash
python blue_jays_calendar_automation.py
```

### Option B: Scheduled Runs (Recommended)

#### On Mac/Linux (using cron):
```bash
# Edit crontab
crontab -e

# Add this line to run weekly on Sundays at 9 AM
0 9 * * 0 cd /path/to/script && /usr/bin/python3 blue_jays_calendar_automation.py
```

#### On Windows (using Task Scheduler):
1. Open Task Scheduler
2. Create Basic Task
3. Name: "Blue Jays Calendar Update"
4. Trigger: Weekly (e.g., every Sunday)
5. Action: Start a program
6. Program: `python`
7. Arguments: `C:\path\to\blue_jays_calendar_automation.py`
8. Start in: `C:\path\to\`

## Customization

### Change Calendar
By default, events are added to your primary calendar. To use a different calendar:

```python
# In the script, change this line:
self.calendar_id = 'primary'

# To your calendar ID (found in Google Calendar settings):
self.calendar_id = 'your-calendar-id@group.calendar.google.com'
```

### Adjust Reminders
Modify the reminders in the `add_game_to_calendar` method:

```python
'reminders': {
    'useDefault': False,
    'overrides': [
        {'method': 'popup', 'minutes': 60},     # Change to your preference
        {'method': 'popup', 'minutes': 1440},   # Change to your preference
    ],
},
```

### Change Game Duration
Default is 3 hours. Modify in `add_game_to_calendar`:

```python
end_date = game_date + timedelta(hours=3)  # Change hours here
```

### Filter by Month
Add this filter in the `run` method after parsing games:

```python
# Only add games in certain months (e.g., June-August)
games = [g for g in games if parse_date(g['date']).month in [6, 7, 8]]
```

## Troubleshooting

### "ModuleNotFoundError"
Install missing packages:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### "Authentication Error"
Delete `token.pickle` and run again to re-authenticate.

### "No games found"
The ESPN website structure may have changed. Check the URL or parsing logic.

### "Duplicate events"
The script checks for duplicates, but if you've manually added events with different names, it may not detect them.

## File Structure

```
blue-jays-calendar/
├── blue_jays_calendar_automation.py  # Main script
├── credentials.json                   # Google OAuth credentials (you download this)
├── token.pickle                       # Auto-generated after first auth
├── README.md                          # This file
└── requirements.txt                   # Python dependencies
```

## Security Notes

- **Never commit `credentials.json` or `token.pickle` to version control**
- Add them to `.gitignore` if using Git
- Keep these files secure as they provide access to your calendar

## Schedule Updates

Run this script:
- **Weekly** to catch newly announced game times
- **Before the season** to add all games at once
- **Monthly** during the season for schedule changes

## Support

If you encounter issues:
1. Check that your `credentials.json` is in the same directory
2. Verify you have internet connection
3. Ensure Google Calendar API is enabled in your Google Cloud project
4. Check Python version: `python --version` (should be 3.7+)

## License

MIT License - Feel free to modify and distribute!

---

**Go Blue Jays! 🧢⚾**
