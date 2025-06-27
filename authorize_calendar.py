from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pickle

SCOPES = ['https://www.googleapis.com/auth/calendar']

flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
creds = flow.run_local_server(port=0)

with open('token.pkl', 'wb') as token:
    pickle.dump(creds, token)

print("✅ Authorization complete. token.pkl saved.")
