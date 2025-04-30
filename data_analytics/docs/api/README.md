# API Documentation

## Endpoints

### Metrics
- `GET /metrics/{source}/{metric_name}`
- `POST /metrics/`

### Health
- `GET /health/status/{service_name}`
- `POST /health/check`

### Analytics
- `GET /analytics/summary`
- `GET /analytics/trends/{source}/{metric_name}`

## Authentication
Bearer token authentication required for all endpoints.

## Rate Limiting
Rate limits are configured per service in config files.
