# database/init_db.py
import asyncpg
import asyncio
from datetime import datetime
import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

async def init_database():
    """Initialize the database and create necessary tables"""
    conn = await asyncpg.connect(
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        host=os.getenv('DB_HOST')
    )

    # Enable TimescaleDB extension
    await conn.execute('CREATE EXTENSION IF NOT EXISTS timescaledb;')

    # Create tables
    await conn.execute('''
        -- Health checks table for system monitoring
        CREATE TABLE IF NOT EXISTS health_checks (
            time TIMESTAMPTZ NOT NULL,
            service_name TEXT NOT NULL,
            status TEXT NOT NULL,
            response_time FLOAT,
            error_message TEXT,
            details JSONB
        );

        -- Convert to hypertable
        SELECT create_hypertable('health_checks', 'time', if_not_exists => TRUE);

        -- Metrics table for all numerical data
        CREATE TABLE IF NOT EXISTS metrics (
            time TIMESTAMPTZ NOT NULL,
            source TEXT NOT NULL,
            metric_name TEXT NOT NULL,
            value DOUBLE PRECISION,
            tags JSONB,
            metadata JSONB
        );

        -- Convert to hypertable
        SELECT create_hypertable('metrics', 'time', if_not_exists => TRUE);

        -- Events table for non-numerical data
        CREATE TABLE IF NOT EXISTS events (
            time TIMESTAMPTZ NOT NULL,
            source TEXT NOT NULL,
            event_type TEXT NOT NULL,
            event_data JSONB,
            tags JSONB
        );

        -- Convert to hypertable
        SELECT create_hypertable('events', 'time', if_not_exists => TRUE);

        -- Service configurations
        CREATE TABLE IF NOT EXISTS service_configs (
            service_name TEXT PRIMARY KEY,
            config JSONB NOT NULL,
            last_updated TIMESTAMPTZ NOT NULL,
            is_active BOOLEAN DEFAULT true
        );

        -- API credentials
        CREATE TABLE IF NOT EXISTS api_credentials (
            service_name TEXT PRIMARY KEY,
            credentials JSONB NOT NULL,
            last_updated TIMESTAMPTZ NOT NULL,
            expiry TIMESTAMPTZ,
            is_valid BOOLEAN DEFAULT true
        );

        -- Create indexes
        CREATE INDEX IF NOT EXISTS idx_metrics_source_metric 
            ON metrics (source, metric_name, time DESC);
        
        CREATE INDEX IF NOT EXISTS idx_events_source_type 
            ON events (source, event_type, time DESC);
        
        CREATE INDEX IF NOT EXISTS idx_health_service 
            ON health_checks (service_name, time DESC);
    ''')

    # Create retention policies
    await conn.execute('''
        -- Keep detailed data for 3 months
        SELECT add_retention_policy('metrics', INTERVAL '3 months');
        SELECT add_retention_policy('events', INTERVAL '3 months');
        SELECT add_retention_policy('health_checks', INTERVAL '1 month');
    ''')

    await conn.close()
