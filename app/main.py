"""
FastAPI application entry point
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config import settings
from app.database import db
from app.api.v1.router import api_router
from app.middleware.cors import setup_cors
from app.middleware.logging import LoggingMiddleware
from app.middleware.security import SecurityHeadersMiddleware, APIKeyMiddleware
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.error_handler import (
    validation_exception_handler,
    http_exception_handler,
    general_exception_handler
)
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    
    Args:
        app: FastAPI application instance
    """
    # Startup
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    
    # Log configuration (without sensitive data)
    logger.info(f"Database URL configured: {bool(settings.DATABASE_URL)}")
    if settings.DATABASE_URL:
        # Mask password in logs
        db_url_parts = settings.DATABASE_URL.split('@')
        if len(db_url_parts) > 1:
            logger.info(f"Database host: {db_url_parts[-1].split('/')[-1]}")
    
    try:
        await db.connect(retries=3, delay=5)
        logger.info("Application startup complete")
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        logger.error("Application cannot start without database connection.")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down application")
    await db.disconnect()
    logger.info("Application shutdown complete")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Backend API for Article Generator with Supabase PostgreSQL",
    debug=settings.DEBUG,
    lifespan=lifespan
)

# Add exception handlers (must be before middleware)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Add API key middleware (executes last in middleware chain)
app.add_middleware(
    APIKeyMiddleware,
    exclude_paths=["/", "/docs", "/redoc", "/openapi.json", "/api/v1/health"]
)

# Add logging middleware
app.add_middleware(LoggingMiddleware)

# Setup CORS
setup_cors(app)

# Add rate limiting middleware
app.add_middleware(RateLimitMiddleware)

# Add security headers middleware (executes first in chain)
app.add_middleware(SecurityHeadersMiddleware)

# Include API routers (must be after middleware)
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.APP_NAME} API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/api/v1/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )

