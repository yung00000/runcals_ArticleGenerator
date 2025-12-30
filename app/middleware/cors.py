"""
CORS middleware configuration
"""
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.config import settings


def setup_cors(app: FastAPI):
    """
    Configure CORS middleware for the FastAPI application
    
    Args:
        app: FastAPI application instance
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

