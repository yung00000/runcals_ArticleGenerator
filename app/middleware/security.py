"""
Security middleware for API key authentication and security headers
"""
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.config import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses"""
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # Remove server header for security
        if "server" in response.headers:
            del response.headers["server"]
        
        return response


class APIKeyMiddleware(BaseHTTPMiddleware):
    """API Key authentication middleware"""
    
    def __init__(self, app, exclude_paths: list = None):
        super().__init__(app)
        if exclude_paths is not None:
            self.exclude_paths = exclude_paths
        else:
            self.exclude_paths = [
                "/",
                "/docs",
                "/redoc",
                "/openapi.json",
                "/api/v1/health"
            ]
    
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        
        # Skip API key check for excluded paths (exact match only)
        is_excluded = path in self.exclude_paths
        
        if is_excluded:
            return await call_next(request)
        
        # Require API key to be configured
        if not settings.API_KEY or settings.API_KEY.strip() == "":
            logger.error("API_KEY not configured in .env file. Authentication is required!")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "API key authentication is not configured. Please set API_KEY in .env file."},
            )
        
        # Get API key from header (case-insensitive)
        api_key = None
        
        # Try different header name variations (case-insensitive)
        header_variations = [
            settings.API_KEY_HEADER,
            settings.API_KEY_HEADER.lower(),
            "x-api-key",
            "X-API-Key"
        ]
        
        for header_name in header_variations:
            api_key = request.headers.get(header_name)
            if api_key:
                break
        
        # Also check all headers (case-insensitive search)
        if not api_key:
            for header_name, header_value in request.headers.items():
                if header_name.lower() == "x-api-key" or header_name.lower() == settings.API_KEY_HEADER.lower():
                    api_key = header_value
                    break
        
        if not api_key:
            logger.warning(f"API key missing from request: {path} from {request.client.host if request.client else 'unknown'}")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "API key required. Please provide X-API-Key header."},
                headers={"WWW-Authenticate": "ApiKey"},
            )
        
        # Validate API key
        if api_key.strip() != settings.API_KEY.strip():
            logger.warning(f"Invalid API key attempt: {path} from {request.client.host if request.client else 'unknown'}")
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": "Invalid API key."},
            )
        
        return await call_next(request)

