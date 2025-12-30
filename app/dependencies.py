"""
Shared dependencies for FastAPI routes
"""
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import db


async def get_database():
    """
    Dependency to get database connection pool
    
    Yields:
        Database instance
    """
    yield db


async def get_db_session() -> AsyncSession:
    """
    Dependency to get database session
    
    Yields:
        AsyncSession instance
    """
    async with await db.get_session() as session:
        yield session

