# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any

# Import service modules
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

load_dotenv()
app = FastAPI(title="Personal Data Analytics API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/data/summary")
async def get_all_data_summary(start_date: str, end_date: str):
    try:
        tasks = [
            google_service.get_summary(start_date, end_date),
            health_service.get_summary(start_date, end_date),
            entertainment_service.get_summary(start_date, end_date),
            productivity_service.get_summary(start_date, end_date),
            financial_service.get_summary(start_date, end_date),
            knowledge_service.get_summary(start_date, end_date),
            device_service.get_summary(start_date, end_date),
            crypto_service.get_summary(start_date, end_date)
        ]
        results = await asyncio.gather(*tasks)
        
        return {
            "google": results[0],
            "health": results[1],
            "entertainment": results[2],
            "productivity": results[3],
            "financial": results[4],
            "knowledge": results[5],
            "devices": results[6],
            "crypto": results[7]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Individual service endpoints
@app.get("/data/google")
async def get_google_data(start_date: str, end_date: str):
    return await google_service.get_data(start_date, end_date)

@app.get("/data/health")
async def get_health_data(start_date: str, end_date: str):
    return await health_service.get_data(start_date, end_date)

@app.get("/data/finance")
async def get_financial_data(start_date: str, end_date: str):
    return await financial_service.get_data(start_date, end_date)

@app.get("/data/crypto")
async def get_crypto_data(start_date: str, end_date: str):
    return await crypto_service.get_data(start_date, end_date)

@app.get("/data/productivity")
async def get_productivity_data(start_date: str, end_date: str):
    return await productivity_service.get_data(start_date, end_date)

@app.get("/data/knowledge")
async def get_knowledge_data(start_date: str, end_date: str):
    return await knowledge_service.get_data(start_date, end_date)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
