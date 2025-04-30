# services/base_service.py
from abc import ABC, abstractmethod
import aiohttp
import logging
from datetime import datetime, timedelta
from typing import Dict, Any
import asyncpg
import json
import os
from dotenv import load_dotenv

load_dotenv()

class BaseService(ABC):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.db_pool = None
        
    async def get_db_pool(self):
        if not self.db_pool:
            self.db_pool = await asyncpg.create_pool(os.getenv('DATABASE_URL'))
        return self.db_pool

    async def store_data(self, data: Dict[str, Any], category: str):
        pool = await self.get_db_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO data_points (category, data, timestamp)
                VALUES ($1, $2, $3)
                """,
                category,
                json.dumps(data),
                datetime.now()
            )

    @abstractmethod
    async def fetch_data(self, start_date: str, end_date: str) -> Dict[str, Any]:
        pass

    async def fetch_and_store(self):
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=1)
            data = await self.fetch_data(start_date.isoformat(), end_date.isoformat())
            await self.store_data(data, self.__class__.__name__)
            return data
        except Exception as e:
            self.logger.error(f"Error in fetch_and_store: {str(e)}")
            raise
