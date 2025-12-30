"""
Rate limiting middleware
"""
from collections import defaultdict
from time import time
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from app.config import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware"""
    
    def __init__(self, app):
        super().__init__(app)
        self.requests_per_minute = defaultdict(list)
        self.requests_per_hour = defaultdict(list)
        self.cleanup_interval = 300  # Clean up old entries every 5 minutes
        self.last_cleanup = time()
    
    def _cleanup_old_entries(self):
        """Remove old entries to prevent memory leaks"""
        current_time = time()
        if current_time - self.last_cleanup < self.cleanup_interval:
            return
        
        # Clean up minute-based entries older than 1 minute
        cutoff_minute = current_time - 60
        for ip in list(self.requests_per_minute.keys()):
            self.requests_per_minute[ip] = [
                ts for ts in self.requests_per_minute[ip] if ts > cutoff_minute
            ]
            if not self.requests_per_minute[ip]:
                del self.requests_per_minute[ip]
        
        # Clean up hour-based entries older than 1 hour
        cutoff_hour = current_time - 3600
        for ip in list(self.requests_per_hour.keys()):
            self.requests_per_hour[ip] = [
                ts for ts in self.requests_per_hour[ip] if ts > cutoff_hour
            ]
            if not self.requests_per_hour[ip]:
                del self.requests_per_hour[ip]
        
        self.last_cleanup = current_time
    
    def _get_client_ip(self, request: Request) -> str:
        """Get client IP address"""
        # Check for forwarded IP (behind proxy)
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        return request.client.host if request.client else "unknown"
    
    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for health check and docs
        if request.url.path in ["/api/v1/health", "/docs", "/redoc", "/openapi.json", "/"]:
            return await call_next(request)
        
        if not settings.RATE_LIMIT_ENABLED:
            return await call_next(request)
        
        # Cleanup old entries periodically
        self._cleanup_old_entries()
        
        # Get client IP
        client_ip = self._get_client_ip(request)
        current_time = time()
        
        # Check per-minute limit
        minute_requests = self.requests_per_minute[client_ip]
        minute_requests = [ts for ts in minute_requests if ts > current_time - 60]
        
        if len(minute_requests) >= settings.RATE_LIMIT_PER_MINUTE:
            logger.warning(f"Rate limit exceeded (per minute) for IP: {client_ip}")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Maximum {settings.RATE_LIMIT_PER_MINUTE} requests per minute.",
                headers={"Retry-After": "60"},
            )
        
        # Check per-hour limit
        hour_requests = self.requests_per_hour[client_ip]
        hour_requests = [ts for ts in hour_requests if ts > current_time - 3600]
        
        if len(hour_requests) >= settings.RATE_LIMIT_PER_HOUR:
            logger.warning(f"Rate limit exceeded (per hour) for IP: {client_ip}")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Maximum {settings.RATE_LIMIT_PER_HOUR} requests per hour.",
                headers={"Retry-After": "3600"},
            )
        
        # Record request
        minute_requests.append(current_time)
        hour_requests.append(current_time)
        self.requests_per_minute[client_ip] = minute_requests
        self.requests_per_hour[client_ip] = hour_requests
        
        # Add rate limit headers
        response = await call_next(request)
        response.headers["X-RateLimit-Limit-Minute"] = str(settings.RATE_LIMIT_PER_MINUTE)
        response.headers["X-RateLimit-Remaining-Minute"] = str(settings.RATE_LIMIT_PER_MINUTE - len(minute_requests))
        response.headers["X-RateLimit-Limit-Hour"] = str(settings.RATE_LIMIT_PER_HOUR)
        response.headers["X-RateLimit-Remaining-Hour"] = str(settings.RATE_LIMIT_PER_HOUR - len(hour_requests))
        
        return response

