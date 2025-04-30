# cron.py
import schedule
import time
import asyncio
from datetime import datetime, timedelta
import logging
from services import (
    google_service,
    health_service,
    entertainment_service,
    productivity_service,
    financial_service,
    knowledge_service,
    device_service,
    crypto_service
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def fetch_all_data():
    """Fetch data from all services"""
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=1)
        
        tasks = [
            google_service.fetch_and_store(),
            health_service.fetch_and_store(),
            entertainment_service.fetch_and_store(),
            productivity_service.fetch_and_store(),
            financial_service.fetch_and_store(),
            knowledge_service.fetch_and_store(),
            device_service.fetch_and_store(),
            crypto_service.fetch_and_store()
        ]
        
        await asyncio.gather(*tasks)
        logger.info(f"Successfully fetched all data at {datetime.now()}")
        
    except Exception as e:
        logger.error(f"Error fetching data: {str(e)}")

def run_fetch():
    """Wrapper to run async function"""
    asyncio.run(fetch_all_data())

def setup_schedules():
    # Hourly tasks
    schedule.every().hour.do(run_fetch)
    
    # Daily tasks (run at specific times)
    schedule.every().day.at("00:00").do(run_fetch)  # Daily reset
    schedule.every().day.at("12:00").do(run_fetch)  # Midday update
    
    # Weekly tasks
    schedule.every().sunday.at("23:59").do(run_fetch)  # Weekly summary

if __name__ == "__main__":
    setup_schedules()
    logger.info("Cron scheduler started")
    
    while True:
        schedule.run_pending()
        time.sleep(60)
