# Deployment Guide

## Prerequisites
- Docker
- Docker Compose
- PostgreSQL 14+
- Node.js 16+

## Setup
1. Copy `template.env` to `.env`
2. Configure environment variables
3. Run `docker-compose up -d`

## Database Setup
1. Run `python database/init_db.py`

## Monitoring
Check `/monitoring` for Prometheus metrics
