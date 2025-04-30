# services/health_service.py
from .base_service import BaseService
from garminconnect import Garmin
from datetime import datetime, timedelta
import asyncio
import os

class HealthService(BaseService):
    def __init__(self):
        super().__init__()
        self.client = None

    async def initialize_client(self):
        if not self.client:
            self.client = Garmin(
                os.getenv('GARMIN_EMAIL'),
                os.getenv('GARMIN_PASSWORD')
            )
            await self.client.login()

    async def get_sleep_data(self, start_date: str, end_date: str):
        await self.initialize_client()
        return await self.client.get_sleep_data(start_date, end_date)

    async def get_heart_rate_data(self, start_date: str, end_date: str):
        await self.initialize_client()
        return await self.client.get_heart_rates(start_date, end_date)

    async def get_activity_data(self, start_date: str, end_date: str):
        await self.initialize_client()
        return await self.client.get_activities(start_date, end_date)

    async def get_body_battery(self, start_date: str, end_date: str):
        await self.initialize_client()
        return await self.client.get_body_battery(start_date, end_date)

    async def get_stress_data(self, start_date: str, end_date: str):
        await self.initialize_client()
        return await self.client.get_stress_data(start_date, end_date)

    async def fetch_data(self, start_date: str, end_date: str):
        tasks = [
            self.get_sleep_data(start_date, end_date),
            self.get_heart_rate_data(start_date, end_date),
            self.get_activity_data(start_date, end_date),
            self.get_body_battery(start_date, end_date),
            self.get_stress_data(start_date, end_date)
        ]
        
        sleep, heart, activity, battery, stress = await asyncio.gather(*tasks)
        
        return {
            "sleep": sleep,
            "heart_rate": heart,
            "activity": activity,
            "body_battery": battery,
            "stress": stress
        }
