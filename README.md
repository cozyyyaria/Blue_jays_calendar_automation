# Blue Jays Home Games Calendar Automation

Automatically add all Toronto Blue Jays 2026 home games to your Google Calendar!

## What It Does

✅ Adds **all 70+ home games** to your Google Calendar  
✅ Includes correct dates and game times  
✅ Sets reminders (1 hour and 1 day before each game)  
✅ Color-codes games in blue  
✅ Prevents duplicate entries  
✅ **100% FREE** - no costs anywhere!  

## Quick Start

### 1. Install Python Packages

```bash
pip install -r requirements.txt
```

### 2. Set Up Google Calendar API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable **Google Calendar API**
4. Create **OAuth credentials** (Desktop app)
5. Download as `credentials.json`
6. Add yourself as a **test user**

[Detailed setup instructions here](#detailed-setup)

### 3. Run the Script

```bash
python blue_jays_calendar_automation.py
```

First time: Browser opens for authorization  
After that: Just runs automatically!

## What Gets Added

Each game includes:
- 📅 **Event:** "Blue Jays vs [Opponent]"
- 🏟️ **Location:** Rogers Centre, Toronto
- ⏰ **Time:** Actual game time
- 🔔 **Reminders:** 1 hour + 1 day before
- 💙 **Blue color coding**

## Complete 2026 Schedule

**70+ home games from March to September:**

- **March/April:** 19 games (Athletics, Rockies, Dodgers, Twins, Guardians, Red Sox)
- **May:** 12 games (Angels, Rays, Pirates, Marlins)
- **June:** 16 games (Orioles, Phillies, Yankees, Astros, Rangers, Mets)
- **July:** 6 games (Mets, Rays, White Sox)
- **August:** 13 games (White Sox, Cardinals, Orioles, Phillies, Yankees, Royals, Mariners)
- **September:** 3 games (Mariners)

## Update Anytime!

The script uses the latest schedule data. Just run it again to:
- ✅ Catch schedule changes
- ✅ Update game times (if changed from TBD)
- ✅ Add any new games

It automatically skips games already in your calendar!

---

## Detailed Setup

### Step 1: Install Python

**Check if you have Python:**
```bash
python --version
```

Need 3.7 or higher. If not installed:
- **Windows:** https://www.python.org/downloads/
- **Mac:** https://www.python.org/downloads/

### Step 2: Install Packages

```bash
cd C:\BlueJaysCalendar  # Or your folder
pip install -r requirements.txt
```

### Step 3: Google Calendar API Setup

#### 3a. Create Google Cloud Project
1. Go to https://console.cloud.google.com/
2. Click "Select a project" → "NEW PROJECT"
3. Name: `Blue Jays Calendar`
4. Click "CREATE"

#### 3b. Enable Calendar API
1. Search for "Calendar API"
2. Click "Google Calendar API"
3. Click "ENABLE"

#### 3c. Configure OAuth Consent Screen
1. Click "OAuth consent screen" (left sidebar)
2. Select "External"
3. Fill in:
   - App name: `Blue Jays Calendar`
   - Your email (support + developer contact)
4. Click "SAVE AND CONTINUE" (skip scopes)
5. Click "SAVE AND CONTINUE" (skip test users for now)
6. Click "BACK TO DASHBOARD"

#### 3d. Create Credentials
1. Click "Credentials" (left sidebar)
2. Click "+ CREATE CREDENTIALS"
3. Select "OAuth client ID"
4. Application type: **Desktop app**
5. Name: `Blue Jays Script`
6. Click "CREATE"
7. Click "DOWNLOAD JSON"
8. Save as `credentials.json` in your folder

#### 3e. Add Test User
1. Go back to "OAuth consent screen"
2. Click "Audience" (or scroll to Test users)
3. Click "+ ADD USERS"
4. Add your Gmail address
5. Click "SAVE"

### Step 4: Run!

```bash
python blue_jays_calendar_automation.py
```

**First run:**
- Browser opens
- Sign in to Google
- Click "Advanced" → "Go to Blue Jays Calendar (unsafe)"
  - (It's YOUR app, so it's safe!)
- Click "Allow"
- Done!

**See your games:**
- Go to https://calendar.google.com/
- Games are labeled "Blue Jays vs [Team]"

---

## Troubleshooting

**"credentials.json not found"**
- Make sure it's in the same folder as the script

**"Authentication failed"**
- Delete `token.pickle` and run again
- Make sure you added yourself as test user

**"No games found"**
- Check your internet connection
- Script will use verified schedule data

**Games not showing**
- Refresh Google Calendar (F5)
- Check you're viewing the right calendar
- Scroll to late March 2026

---

## Automate Updates

### Windows Task Scheduler:
Run monthly to catch updates:
1. Create Basic Task
2. Trigger: Monthly (1st of month)
3. Action: `python C:\path\to\blue_jays_calendar_automation.py`

### Mac/Linux cron:
```bash
# Run 1st of every month at 9 AM
0 9 1 * * cd /path/to/script && python3 blue_jays_calendar_automation.py
```

---

## Customization

### Change Calendar
Edit the script:
```python
self.calendar_id = 'your-calendar-id@group.calendar.google.com'
```

### Adjust Reminders
Edit the script:
```python
'overrides': [
    {'method': 'popup', 'minutes': 120},  # 2 hours before
    {'method': 'popup', 'minutes': 2880},  # 2 days before
],
```

---

## Security

**NEVER share:**
- ❌ `credentials.json` - Your Google credentials
- ❌ `token.pickle` - Your access token

These files give access to your Google Calendar!

---

## FAQ

**Q: Does this cost money?**
A: No! Everything is 100% free.

**Q: Will it create duplicates?**
A: No! Script checks and skips existing games.

**Q: Can I delete games later?**
A: Yes! Delete them in Google Calendar normally.

**Q: What if game times change?**
A: Run the script again. You may need to manually update times or delete and re-add.

**Q: Can I use this for other teams?**
A: Yes! Modify the script with their schedule.

**Q: Where does the schedule come from?**
A: The script uses verified 2026 Blue Jays home schedule data.

---

## What Changed from v1

**Old version:**
- ❌ Only found ~49 games (ESPN had incomplete data)
- ❌ Missing series
- ❌ Some inaccurate times

**New version:**
- ✅ Complete 70+ game schedule
- ✅ All series included
- ✅ Accurate game times
- ✅ Simpler - no PDF needed!

---

## Support

Having issues?
1. Check Python version: `python --version` (need 3.7+)
2. Verify `credentials.json` is in the right folder
3. Make sure you added yourself as test user
4. Try deleting `token.pickle` and re-authenticating

---

## License

MIT License - Free to use, modify, and share!

---

**Go Blue Jays! 🧢⚾**

*Schedule verified from official 2026 Blue Jays schedule*  
*Last updated: February 2026*