# api/routes/metrics.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from database.db import Database
from database.models import Metric
from ..dependencies import get_db

router = APIRouter(prefix="/metrics", tags=["metrics"])

@router.post("/")
async def store_metric(metric: Metric, db: Database = Depends(get_db)):
    try:
        await db.store_metric(metric)
        return {"status": "success", "message": "Metric stored successfully"}
    except Exception as e:
        logger.error(f"Error storing metric: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{source}/{metric_name}")
async def get_metrics(
    source: str,
    metric_name: str,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    limit: int = 100,
    db: Database = Depends(get_db)
):
    try:
        metrics = await db.get_latest_metrics(source, metric_name, limit)
        return {"metrics": metrics}
    except Exception as e:
        logger.error(f"Error fetching metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/aggregated/{source}/{metric_name}")
async def get_aggregated_metrics(
    source: str,
    metric_name: str,
    interval: str = "1h",
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    db: Database = Depends(get_db)
):
    try:
        metrics = await db.get_aggregated_metrics(
            source, metric_name, interval, start_time, end_time
        )
        return {"metrics": metrics}
    except Exception as e:
        logger.error(f"Error fetching aggregated metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
