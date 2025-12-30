"""
Configuration module for loading environment variables from .env file
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Supabase Configuration
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_SERVICE_ROLE_KEY: str = ""
    
    # Database Connection - can use DATABASE_URL or individual parameters
    DATABASE_URL: str = ""
    
    # Individual connection parameters (alternative to DATABASE_URL)
    # Format from Supabase Dashboard: Session pooler
    user: str = ""
    password: str = ""
    host: str = ""
    port: str = ""
    dbname: str = ""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Build DATABASE_URL from individual parameters if DATABASE_URL is not provided
        if not self.DATABASE_URL and all([self.user, self.password, self.host, self.port, self.dbname]):
            from urllib.parse import quote
            encoded_password = quote(self.password, safe='')
            self.DATABASE_URL = f"postgresql://{self.user}:{encoded_password}@{self.host}:{self.port}/{self.dbname}"
        elif not self.DATABASE_URL:
            raise ValueError(
                "Either DATABASE_URL or all individual parameters (user, password, host, port, dbname) must be provided"
            )
    
    # Application Settings
    APP_NAME: str = "runcals_ArticleGenerator"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS Settings
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8080"
    
    # Security Settings
    API_KEY: str = ""  # API key for frontend authentication (REQUIRED for protected endpoints - set in .env)
    API_KEY_HEADER: str = "X-API-Key"  # Header name for API key
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 60  # Requests per minute per IP
    RATE_LIMIT_PER_HOUR: int = 1000  # Requests per hour per IP
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convert CORS_ORIGINS string to list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields in .env file


# Global settings instance
settings = Settings()

