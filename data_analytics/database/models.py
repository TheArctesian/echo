# database/models.py
from datetime import datetime
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class HealthCheck(BaseModel):
    time: datetime
    service_name: str
    status: str
    response_time: Optional[float]
    error_message: Optional[str]
    details: Dict[str, Any] = Field(default_factory=dict)

class Metric(BaseModel):
    time: datetime
    source: str
    metric_name: str
    value: float
    tags: Dict[str, str] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class Event(BaseModel):
    time: datetime
    source: str
    event_type: str
    event_data: Dict[str, Any] = Field(default_factory=dict)
    tags: Dict[str, str] = Field(default_factory=dict)

class ServiceConfig(BaseModel):
    service_name: str
    config: Dict[str, Any]
    last_updated: datetime
    is_active: bool = True

class ApiCredential(BaseModel):
    service_name: str
    credentials: Dict[str, Any]
    last_updated: datetime
    expiry: Optional[datetime]
    is_valid: bool = True
