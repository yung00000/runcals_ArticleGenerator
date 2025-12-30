"""
API v1 router aggregation
"""
from fastapi import APIRouter
from app.api.v1.endpoints import health, articles

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(articles.router, tags=["Articles"])

