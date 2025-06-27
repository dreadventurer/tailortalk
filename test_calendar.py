from calendar_helper import get_calendar_service, check_availability, book_event
from datetime import datetime, timedelta

# Load the service just once
service = get_calendar_service()

start_time = datetime(2025, 6, 30, 18, 0)
end_time = start_time + timedelta(minutes=30)

print("Checking availability...")
try:
    if check_availability(start_time, end_time, service):
        print("Slot is free. Booking now...")
        link = book_event("Manual Test Meeting", start_time, end_time, service)
        print("✅ Meeting booked! Link:", link)
    else:
        print("❌ Slot already booked.")
except Exception as e:
    print("❗ Error:", str(e))
