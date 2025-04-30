# api/routes/health.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from database.db import Database
from database.models import HealthCheck
from ..dependencies import get_db

router = APIRouter(prefix="/health", tags=["health"])

@router.post("/check")
async def store_health_check(
    health_check: HealthCheck,
    db: Database = Depends(get_db)
):
    try:
        await db.store_health_check(health_check)
        return {"status": "success", "message": "Health check stored successfully"}
    except Exception as e:
        logger.error(f"Error storing health check: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{service_name}")
async def get_service_health(
    service_name: str,
    hours: int = 24,
    db: Database = Depends(get_db)
):
    try:
        health_checks = await db.get_service_health(service_name, hours)
        return {"health_checks": health_checks}
    except Exception as e:
        logger.error(f"Error fetching health status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/overview")
async def get_health_overview(db: Database = Depends(get_db)):
    try:
        services = await db.get_all_services_health()
        return {"services": services}
    except Exception as e:
        logger.error(f"Error fetching health overview: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
