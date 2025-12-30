"""
Database connection module for Supabase PostgreSQL using SQLAlchemy
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import text
from typing import Optional, List, Dict, Any
from app.config import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

# SQLAlchemy Base for models
Base = declarative_base()


class Database:
    """Database connection manager using SQLAlchemy"""
    
    def __init__(self):
        self.engine: Optional[Any] = None
        self.async_session_maker: Optional[async_sessionmaker] = None
    
    def _build_database_url(self) -> str:
        """
        Build SQLAlchemy database URL from DATABASE_URL or individual parameters
        
        Returns:
            Database URL string for SQLAlchemy
        """
        # If DATABASE_URL is provided, use it directly
        if settings.DATABASE_URL:
            # SQLAlchemy async uses postgresql+psycopg:// for psycopg v3
            # Convert postgres:// or postgresql:// to postgresql+psycopg:// for async support
            db_url = settings.DATABASE_URL
            if db_url.startswith('postgres://'):
                db_url = db_url.replace('postgres://', 'postgresql+psycopg://', 1)
            elif db_url.startswith('postgresql://'):
                # Only replace if not already using a driver
                if '+psycopg' not in db_url and '+asyncpg' not in db_url:
                    db_url = db_url.replace('postgresql://', 'postgresql+psycopg://', 1)
            return db_url
        
        raise ValueError("DATABASE_URL is required")
    
    async def connect(self, retries: int = 3, delay: int = 5):
        """
        Create database connection engine with retry logic
        
        Args:
            retries: Number of retry attempts
            delay: Initial delay between retries in seconds
        """
        import asyncio
        
        db_url = self._build_database_url()
        
        # Log connection info (without password) for debugging
        if '@' in db_url:
            # Mask password in URL for logging
            parts = db_url.split('@')
            if ':' in parts[0]:
                user_pass = parts[0].split('://')[-1]
                if ':' in user_pass:
                    user = user_pass.split(':')[0]
                    masked_url = db_url.replace(user_pass, f"{user}:***", 1)
                    logger.info(f"Connecting to database: {masked_url.split('@')[-1]}")
                else:
                    logger.info(f"Connecting to database: {parts[-1]}")
            else:
                logger.info(f"Connecting to database: {parts[-1]}")
        else:
            logger.info(f"Connecting to database: {db_url}")
        
        # Verify DATABASE_URL is set
        if not settings.DATABASE_URL or settings.DATABASE_URL.strip() == "":
            error_msg = "DATABASE_URL is not set in environment variables. Please check your .env file."
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        last_exception = None
        
        for attempt in range(1, retries + 1):
            try:
                logger.info(f"Database connection attempt {attempt}/{retries}")
                
                # Create async engine with connection pooling
                self.engine = create_async_engine(
                    db_url,
                    pool_size=5,
                    max_overflow=10,
                    pool_pre_ping=True,  # Verify connections before using
                    echo=settings.DEBUG,  # Log SQL queries in debug mode
                    connect_args={
                        "connect_timeout": 10,  # 10 second connection timeout
                    }
                )
                
                # Create async session maker
                self.async_session_maker = async_sessionmaker(
                    self.engine,
                    class_=AsyncSession,
                    expire_on_commit=False
                )
                
                # Test connection with timeout
                async with self.engine.begin() as conn:
                    await conn.execute(text("SELECT 1"))
                
                logger.info("Database connection pool created successfully")
                return  # Success, exit retry loop
                
            except Exception as e:
                last_exception = e
                error_msg = str(e)
                logger.error(f"Database connection attempt {attempt}/{retries} failed: {error_msg}")
                
                if attempt < retries:
                    wait_time = delay * attempt  # Exponential backoff
                    logger.info(f"Retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(f"All {retries} connection attempts failed. Last error: {error_msg}")
                    logger.error("Please check:")
                    logger.error("1. DATABASE_URL in .env file is correct")
                    logger.error("2. Database credentials are valid")
                    logger.error("3. Network connectivity to database server")
                    logger.error("4. If using Supabase, check if circuit breaker is open (wait a few minutes)")
                    raise
    
    async def disconnect(self):
        """Close database connection engine"""
        if self.engine:
            await self.engine.dispose()
            logger.info("Database connection pool closed")
    
    async def get_session(self) -> AsyncSession:
        """
        Get async database session
        
        Returns:
            AsyncSession instance
        """
        if not self.async_session_maker:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self.async_session_maker()
    
    async def fetch(self, query: str, **kwargs) -> List[Dict[str, Any]]:
        """
        Execute SELECT query and return results
        
        Args:
            query: SQL query string with named parameters (:param_name)
            **kwargs: Query parameters as keyword arguments
            
        Returns:
            List of dictionaries representing rows
        """
        async with await self.get_session() as session:
            result = await session.execute(text(query), kwargs)
            rows = result.fetchall()
            # Convert rows to dictionaries
            return [dict(row._mapping) for row in rows]
    
    async def fetchrow(self, query: str, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Execute SELECT query and return single row
        
        Args:
            query: SQL query string with named parameters (:param_name)
            **kwargs: Query parameters as keyword arguments
            
        Returns:
            Dictionary representing row or None if not found
        """
        async with await self.get_session() as session:
            result = await session.execute(text(query), kwargs)
            row = result.fetchone()
            return dict(row._mapping) if row else None
    
    async def fetchval(self, query: str, **kwargs) -> Any:
        """
        Execute SELECT query and return single value
        
        Args:
            query: SQL query string with named parameters (:param_name)
            **kwargs: Query parameters as keyword arguments
            
        Returns:
            Single value or None
        """
        async with await self.get_session() as session:
            result = await session.execute(text(query), kwargs)
            row = result.fetchone()
            return row[0] if row else None
    
    async def execute(self, query: str, **kwargs) -> Any:
        """
        Execute INSERT/UPDATE/DELETE query
        
        Args:
            query: SQL query string with named parameters (:param_name)
            **kwargs: Query parameters as keyword arguments
            
        Returns:
            Result object
        """
        async with await self.get_session() as session:
            result = await session.execute(text(query), kwargs)
            await session.commit()
            return result


# Global database instance
db = Database()
