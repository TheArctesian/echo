# api/routes/system.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any, Optional
from database.db import Database
from ..dependencies import get_db

router = APIRouter(prefix="/system", tags=["system"])

@router.get("/sources")
async def get_data_sources(db: Database = Depends(get_db)):
    try:
        sources = await db.get_all_sources()
        return {"sources": sources}
    except Exception as e:
        logger.error(f"Error fetching data sources: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/config/{service_name}")
async def get_service_config(
    service_name: str,
    db: Database = Depends(get_db)
):
    try:
        config = await db.get_service_config(service_name)
        return {"config": config}
    except Exception as e:
        logger.error(f"Error fetching service config: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/config/{service_name}")
async def update_service_config(
    service_name: str,
    config: Dict[str, Any],
    db: Database = Depends(get_db)
):
    try:
        await db.update_service_config(service_name, config)
        return {"status": "success", "message": "Config updated successfully"}
    except Exception as e:
        logger.error(f"Error updating service config: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
