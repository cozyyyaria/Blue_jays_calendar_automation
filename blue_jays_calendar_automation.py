#!/usr/bin/env python3
"""
Blue Jays Home Games Calendar Automation Script
This script fetches the Toronto Blue Jays schedule and adds home games to Google Calendar
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
import os
import re

# Google Calendar API scopes
SCOPES = ['https://www.googleapis.com/auth/calendar']

class BlueJaysCalendarAutomation:
    def __init__(self):
        self.service = None
        self.calendar_id = 'primary'  # Use primary calendar or specify a calendar ID
        
    def authenticate_google_calendar(self):
        """Authenticate with Google Calendar API"""
        creds = None
        
        # Token file stores the user's access and refresh tokens
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        # If there are no valid credentials, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials for next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        
        self.service = build('calendar', 'v3', credentials=creds)
        print("✓ Successfully authenticated with Google Calendar")
        
    def fetch_blue_jays_schedule(self, year=2026):
        """Fetch Blue Jays schedule from ESPN"""
        url = f"https://www.espn.com/mlb/team/schedule/_/name/tor/seasontype/2"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        print(f"Fetching Blue Jays {year} schedule...")
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            raise Exception(f"Failed to fetch schedule. Status code: {response.status_code}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
    
    def parse_home_games(self, soup):
        """Parse home games from the schedule HTML"""
        games = []
        
        # Find all table rows with game data
        rows = soup.find_all('tr')
        
        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 2:
                # First cell contains date, second contains opponent
                date_cell = cells[0].get_text(strip=True)
                opponent_cell = cells[1].get_text(strip=True)
                
                # Check if it's a home game (starts with "vs")
                if opponent_cell.startswith('vs'):
                    # Extract opponent name
                    opponent = opponent_cell.replace('vs', '').strip()
                    
                    # Extract time if available
                    time_cell = cells[2].get_text(strip=True) if len(cells) > 2 else 'TBD'
                    
                    games.append({
                        'date': date_cell,
                        'opponent': opponent,
                        'time': time_cell
                    })
        
        print(f"✓ Found {len(games)} home games")
        return games
    
    def parse_date_time(self, date_str, time_str):
        """Parse date and time strings into datetime objects"""
        # Parse date (e.g., "Thu, Mar 26")
        try:
            # Add year to date string
            date_with_year = f"{date_str}, 2026"
            game_date = datetime.strptime(date_with_year, "%a, %b %d, %Y")
            
            # Parse time if not TBD
            if time_str and time_str != 'TBD':
                # Handle time formats like "7:07 PM"
                time_match = re.search(r'(\d{1,2}):(\d{2})\s*(AM|PM)', time_str)
                if time_match:
                    hour = int(time_match.group(1))
                    minute = int(time_match.group(2))
                    am_pm = time_match.group(3)
                    
                    if am_pm == 'PM' and hour != 12:
                        hour += 12
                    elif am_pm == 'AM' and hour == 12:
                        hour = 0
                    
                    game_date = game_date.replace(hour=hour, minute=minute)
                else:
                    # Default to 7:00 PM if time parsing fails
                    game_date = game_date.replace(hour=19, minute=0)
            else:
                # Default to 7:00 PM for TBD games
                game_date = game_date.replace(hour=19, minute=0)
            
            return game_date
        
        except Exception as e:
            print(f"Error parsing date/time: {date_str} {time_str} - {e}")
            return None
    
    def check_event_exists(self, opponent, game_date):
        """Check if event already exists in calendar to avoid duplicates"""
        # Search for events on the same day
        time_min = game_date.replace(hour=0, minute=0, second=0).isoformat() + 'Z'
        time_max = game_date.replace(hour=23, minute=59, second=59).isoformat() + 'Z'
        
        events_result = self.service.events().list(
            calendarId=self.calendar_id,
            timeMin=time_min,
            timeMax=time_max,
            q=f"Blue Jays vs {opponent}",
            singleEvents=True
        ).execute()
        
        events = events_result.get('items', [])
        return len(events) > 0
    
    def add_game_to_calendar(self, opponent, game_date, time_str):
        """Add a single game to Google Calendar"""
        
        # Check if event already exists
        if self.check_event_exists(opponent, game_date):
            print(f"  ⊘ Skipping: Blue Jays vs {opponent} on {game_date.strftime('%b %d')} (already exists)")
            return False
        
        # Calculate end time (assume 3 hours for a baseball game)
        end_date = game_date + timedelta(hours=3)
        
        event = {
            'summary': f'Blue Jays vs {opponent}',
            'location': 'Rogers Centre, Toronto, ON',
            'description': f'Toronto Blue Jays home game against {opponent}\n\n'
                          f'Game time: {time_str if time_str != "TBD" else "To Be Determined"}\n'
                          f'Venue: Rogers Centre',
            'start': {
                'dateTime': game_date.isoformat(),
                'timeZone': 'America/Toronto',
            },
            'end': {
                'dateTime': end_date.isoformat(),
                'timeZone': 'America/Toronto',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 60},  # 1 hour before
                    {'method': 'popup', 'minutes': 1440},  # 1 day before
                ],
            },
            'colorId': '9',  # Blue color for Blue Jays games
        }
        
        try:
            event = self.service.events().insert(
                calendarId=self.calendar_id,
                body=event
            ).execute()
            
            print(f"  ✓ Added: Blue Jays vs {opponent} on {game_date.strftime('%a, %b %d at %I:%M %p')}")
            return True
        
        except Exception as e:
            print(f"  ✗ Error adding game vs {opponent}: {e}")
            return False
    
    def run(self, year=2026):
        """Main execution function"""
        print("=" * 60)
        print("Blue Jays Home Games Calendar Automation")
        print("=" * 60)
        
        # Step 1: Authenticate
        self.authenticate_google_calendar()
        
        # Step 2: Fetch schedule
        soup = self.fetch_blue_jays_schedule(year)
        
        # Step 3: Parse home games
        games = self.parse_home_games(soup)
        
        if not games:
            print("No home games found!")
            return
        
        # Step 4: Add games to calendar
        print(f"\nAdding {len(games)} home games to calendar...")
        added_count = 0
        skipped_count = 0
        
        for game in games:
            game_date = self.parse_date_time(game['date'], game['time'])
            
            if game_date:
                result = self.add_game_to_calendar(
                    game['opponent'],
                    game_date,
                    game['time']
                )
                if result:
                    added_count += 1
                else:
                    skipped_count += 1
        
        # Summary
        print("\n" + "=" * 60)
        print(f"Summary:")
        print(f"  • Total home games found: {len(games)}")
        print(f"  • Successfully added: {added_count}")
        print(f"  • Skipped (already exist): {skipped_count}")
        print("=" * 60)

if __name__ == "__main__":
    automation = BlueJaysCalendarAutomation()
    automation.run()
