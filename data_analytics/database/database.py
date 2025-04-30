# database/db.py
from typing import List, Dict, Any
import asyncpg
from datetime import datetime
import os
from .models import HealthCheck, Metric, Event, ServiceConfig, ApiCredential

class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        if not self.pool:
            self.pool = await asyncpg.create_pool(
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                database=os.getenv('DB_NAME'),
                host=os.getenv('DB_HOST'),
                min_size=5,
                max_size=20
            )

    async def store_metric(self, metric: Metric):
        async with self.pool.acquire() as conn:
            await conn.execute('''
                INSERT INTO metrics (time, source, metric_name, value, tags, metadata)
                VALUES ($1, $2, $3, $4, $5, $6)
            ''', metric.time, metric.source, metric.metric_name, 
                metric.value, metric.tags, metric.metadata)

    async def store_health_check(self, health_check: HealthCheck):
        async with self.pool.acquire() as conn:
            await conn.execute('''
                INSERT INTO health_checks 
                (time, service_name, status, response_time, error_message, details)
                VALUES ($1, $2, $3, $4, $5, $6)
            ''', health_check.time, health_check.service_name, 
                health_check.status, health_check.response_time,
                health_check.error_message, health_check.details)

    async def get_latest_metrics(self, source: str, metric_name: str, 
                               limit: int = 100) -> List[Dict[str, Any]]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch('''
                SELECT * FROM metrics 
                WHERE source = $1 AND metric_name = $2
                ORDER BY time DESC LIMIT $3
            ''', source, metric_name, limit)
            return [dict(row) for row in rows]

    async def get_service_health(self, service_name: str, 
                               hours: int = 24) -> List[Dict[str, Any]]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch('''
                SELECT * FROM health_checks 
                WHERE service_name = $1 
                AND time > NOW() - INTERVAL '$2 hours'
                ORDER BY time DESC
            ''', service_name, hours)
            return [dict(row) for row in rows]
