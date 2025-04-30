import pytest
from fastapi.testclient import TestClient
from api.server import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health/status/test_service")
    assert response.status_code == 200

def test_metrics_endpoint():
    response = client.get("/metrics/test_source/test_metric")
    assert response.status_code == 200

def test_analytics_endpoint():
    response = client.get("/analytics/summary")
    assert response.status_code == 200
