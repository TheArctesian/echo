# services/google_service.py
from .base_service import BaseService
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import pickle
import asyncio
from typing import Dict, Any

SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/youtube.readonly',
    'https://www.googleapis.com/auth/fitness.activity.read'
]

class GoogleService(BaseService):
    def __init__(self):
        super().__init__()
        self.credentials = None
        self.services = {}

    async def get_credentials(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        
        return creds

    async def get_service(self, service_name):
        if service_name not in self.services:
            creds = await self.get_credentials()
            self.services[service_name] = build(service_name, 'v3', credentials=creds)
        return self.services[service_name]

    async def get_calendar_data(self, start_date: str, end_date: str) -> Dict[str, Any]:
        calendar = await self.get_service('calendar')
        events_result = calendar.events().list(
            calendarId='primary',
            timeMin=start_date,
            timeMax=end_date,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        return events_result.get('items', [])

    async def get_youtube_data(self, start_date: str, end_date: str) -> Dict[str, Any]:
        youtube = await self.get_service('youtube')
        activities = youtube.activities().list(
            part='snippet,contentDetails',
            mine=True,
            maxResults=50
        ).execute()
        return activities.get('items', [])

    async def get_location_data(self, start_date: str, end_date: str) -> Dict[str, Any]:
        # This would require Timeline API access
        # Implementation depends on specific access method
        return {}

    async def fetch_data(self, start_date: str, end_date: str) -> Dict[str, Any]:
        tasks = [
            self.get_calendar_data(start_date, end_date),
            self.get_youtube_data(start_date, end_date),
            self.get_location_data(start_date, end_date)
        ]
        calendar_data, youtube_data, location_data = await asyncio.gather(*tasks)
        
        return {
            "calendar": calendar_data,
            "youtube": youtube_data,
            "location": location_data
        }
