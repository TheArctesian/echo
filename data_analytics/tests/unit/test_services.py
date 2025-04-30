import pytest
from services.base_service import BaseService
from datetime import datetime, timedelta

@pytest.mark.asyncio
async def test_google_service():
    from services.google_service import GoogleService
    service = GoogleService()
    # Add your test cases here

@pytest.mark.asyncio
async def test_crypto_service():
    from services.crypto_service import CryptoService
    service = CryptoService()
    # Add your test cases here

@pytest.mark.asyncio
async def test_health_service():
    from services.health_service import HealthService
    service = HealthService()
    # Add your test cases here
