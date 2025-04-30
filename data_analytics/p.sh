#!/bin/bash

# Create missing configuration directories and files
mkdir -p config/{development,production,testing}

cat > config/development/config.yml << EOF
database:
  host: localhost
  port: 5432
  name: data_analytics_dev
  pool_size: 5

logging:
  level: DEBUG
  file: logs/development.log

services:
  google:
    rate_limit: 100
  crypto:
    rate_limit: 50
  health:
    check_interval: 300
EOF

cat > config/production/config.yml << EOF
database:
  host: timescaledb
  port: 5432
  name: data_analytics_prod
  pool_size: 20

logging:
  level: INFO
  file: logs/production.log

services:
  google:
    rate_limit: 1000
  crypto:
    rate_limit: 500
  health:
    check_interval: 60
EOF

cat > config/testing/config.yml << EOF
database:
  host: localhost
  port: 5432
  name: data_analytics_test
  pool_size: 5

logging:
  level: DEBUG
  file: logs/test.log

services:
  google:
    rate_limit: 100
  crypto:
    rate_limit: 50
  health:
    check_interval: 60
EOF

# Create missing documentation directories and files
mkdir -p docs/{api,deployment,development}

cat > docs/api/README.md << EOF
# API Documentation

## Endpoints

### Metrics
- \`GET /metrics/{source}/{metric_name}\`
- \`POST /metrics/\`

### Health
- \`GET /health/status/{service_name}\`
- \`POST /health/check\`

### Analytics
- \`GET /analytics/summary\`
- \`GET /analytics/trends/{source}/{metric_name}\`

## Authentication
Bearer token authentication required for all endpoints.

## Rate Limiting
Rate limits are configured per service in config files.
EOF

cat > docs/deployment/README.md << EOF
# Deployment Guide

## Prerequisites
- Docker
- Docker Compose
- PostgreSQL 14+
- Node.js 16+

## Setup
1. Copy \`template.env\` to \`.env\`
2. Configure environment variables
3. Run \`docker-compose up -d\`

## Database Setup
1. Run \`python database/init_db.py\`

## Monitoring
Check \`/monitoring\` for Prometheus metrics
EOF

cat > docs/development/README.md << EOF
# Development Guide

## Setup
1. Install dependencies: \`pip install -r requirements.txt\`
2. Configure \`.env\`
3. Start services: \`docker-compose up -d\`

## Testing
- Unit: \`pytest tests/unit\`
- Integration: \`pytest tests/integration\`
- E2E: \`pytest tests/e2e\`

## Adding Services
1. Create service in \`Services/\`
2. Implement required methods
3. Add tests
4. Update documentation
EOF

# Create missing test directories
mkdir -p tests/e2e

cat > tests/e2e/test_full_flow.py << EOF
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
EOF

# Create logs directory if it doesn't exist
mkdir -p logs

# Ensure monitoring directory exists with prometheus config
mkdir -p monitoring
cat > monitoring/prometheus.yml << EOF
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'api'
    static_configs:
      - targets: ['localhost:8000']

  - job_name: 'database'
    static_configs:
      - targets: ['localhost:5432']
EOF

echo "All missing directories and files have been created successfully"
