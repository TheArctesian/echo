# Development Guide

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Configure `.env`
3. Start services: `docker-compose up -d`

## Testing
- Unit: `pytest tests/unit`
- Integration: `pytest tests/integration`
- E2E: `pytest tests/e2e`

## Adding Services
1. Create service in `Services/`
2. Implement required methods
3. Add tests
4. Update documentation
