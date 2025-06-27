import pickle
import httplib2
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from datetime import datetime, timedelta

def get_calendar_service():
    print("🔐 Loading calendar credentials...")
    creds = pickle.load(open("token.pkl", "rb"))

    # Ensure credentials are valid
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            print("🔁 Token refreshed successfully.")
        except RefreshError as e:
            print(f"❌ Failed to refresh token: {e}")
            raise

    service = build("calendar", "v3", credentials=creds, cache_discovery=False)
    print("✅ Google Calendar service loaded")
    return service

def check_availability(start_time, end_time, service):
    print(f"⏳ Checking availability from {start_time} to {end_time}")
    events_result = service.events().list(
        calendarId='primary',
        timeMin=start_time.isoformat() + 'Z',
        timeMax=end_time.isoformat() + 'Z',
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])
    print(f"📁 Events found: {len(events)}")
    return len(events) == 0

def book_event(summary, start_time, end_time, service):
    print(f"📝 Booking event: {summary} from {start_time} to {end_time}")
    event = {
        'summary': summary,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
    }
    created_event = service.events().insert(calendarId='primary', body=event).execute()
    print(f"✅ Event created: {created_event.get('htmlLink')}")
    return created_event.get('htmlLink')

