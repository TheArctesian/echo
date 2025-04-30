import pytest
from database.database import Database
from database.models import Metric, HealthCheck, Event

@pytest.mark.asyncio
async def test_store_metric(db):
    metric = Metric(
        time=datetime.now(),
        source="test",
        metric_name="test_metric",
        value=1.0
    )
    await db.store_metric(metric)
    # Add assertions

@pytest.mark.asyncio
async def test_store_health_check(db):
    health_check = HealthCheck(
        time=datetime.now(),
        service_name="test_service",
        status="healthy"
    )
    await db.store_health_check(health_check)
    # Add assertions
