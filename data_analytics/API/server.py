# api/server.py (updated)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import metrics, health, analytics, system

app = FastAPI(title="Data Analytics API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(metrics.router)
app.include_router(health.router)
app.include_router(analytics.router)
app.include_router(system.router)

@app.get("/")
async def root():
    return {
        "status": "online",
        "version": "1.0.0",
        "documentation": "/docs"
    }
