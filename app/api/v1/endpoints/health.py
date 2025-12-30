"""
Health check endpoint
"""
from datetime import datetime
from fastapi import APIRouter, Depends
from app.models.schemas import HealthResponse
from app.dependencies import get_database
from app.database import Database
from app.config import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check(db: Database = Depends(get_database)):
    """
    Health check endpoint to verify API and database connectivity
    
    Returns:
        Health status information
    """
    try:
        # Test database connection
        await db.fetchval("SELECT 1 as test")
        db_status = "connected"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "disconnected"
    
    return HealthResponse(
        status="healthy" if db_status == "connected" else "degraded",
        version=settings.APP_VERSION,
        timestamp=datetime.utcnow(),
        database=db_status
    )

