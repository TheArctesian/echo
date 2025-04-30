# api/routes/analytics.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from database.db import Database
from ..dependencies import get_db

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/summary")
async def get_data_summary(
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    db: Database = Depends(get_db)
):
    try:
        summary = await db.get_data_summary(start_time, end_time)
        return summary
    except Exception as e:
        logger.error(f"Error fetching data summary: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/trends/{source}/{metric_name}")
async def get_metric_trends(
    source: str,
    metric_name: str,
    window: str = "1d",
    db: Database = Depends(get_db)
):
    try:
        trends = await db.get_metric_trends(source, metric_name, window)
        return {"trends": trends}
    except Exception as e:
        logger.error(f"Error fetching trends: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/correlations")
async def get_metric_correlations(
    source1: str,
    metric1: str,
    source2: str,
    metric2: str,
    window: str = "7d",
    db: Database = Depends(get_db)
):
    try:
        correlation = await db.get_metric_correlation(
            source1, metric1, source2, metric2, window
        )
        return {"correlation": correlation}
    except Exception as e:
        logger.error(f"Error calculating correlation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
