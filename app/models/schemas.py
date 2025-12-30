"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    version: str
    timestamp: datetime
    database: str


class ErrorResponse(BaseModel):
    """Error response model"""
    detail: str
    message: Optional[str] = None


# Article models matching running_articles table schema
class ArticleBase(BaseModel):
    """Base article model"""
    title: Optional[str] = None
    content: Optional[str] = None


class ArticleCreate(ArticleBase):
    """Article creation model"""
    pass


class ArticleUpdate(BaseModel):
    """Article update model"""
    title: Optional[str] = None
    content: Optional[str] = None


class ArticleResponse(ArticleBase):
    """Article response model"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ArticleListResponse(BaseModel):
    """Article list response model"""
    items: List[ArticleResponse]
    total: int
    page: int = 1
    page_size: int = 10

