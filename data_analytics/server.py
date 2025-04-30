# api/server.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from database.db import Database
from database.models import HealthCheck, Metric, Event
import logging

app = FastAPI(title="Data Analytics API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database dependency
async def get_db():
    db = Database()
    await db.connect()
    return db

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
