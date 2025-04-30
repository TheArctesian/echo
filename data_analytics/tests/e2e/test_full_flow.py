import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from api.server import app

client = TestClient(app)

def test_complete_flow():
    # Test metric creation
    metric_data = {
        "time": datetime.now().isoformat(),
        "source": "test",
        "metric_name": "test_metric",
        "value": 1.0
    }
    response = client.post("/metrics/", json=metric_data)
    assert response.status_code == 200

    # Test metric retrieval
    response = client.get("/metrics/test/test_metric")
    assert response.status_code == 200

    # Test health check
    response = client.get("/health/status/test")
    assert response.status_code == 200
