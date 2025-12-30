"""
Article endpoints for CRUD operations
"""
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from app.models.schemas import (
    ArticleCreate,
    ArticleUpdate,
    ArticleResponse,
    ArticleListResponse
)
from app.dependencies import get_database
from app.database import Database
from app.services.article_service import ArticleService
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

router = APIRouter()


@router.get("/articles", response_model=ArticleListResponse)
async def get_articles(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    date_from: Optional[str] = Query(
        None, 
        description="Filter articles from this date (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)"
    ),
    date_to: Optional[str] = Query(
        None, 
        description="Filter articles until this date (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)"
    ),
    db: Database = Depends(get_database)
):
    """
    Get all articles with pagination and optional date filtering
    
    Query Parameters:
        - page: Page number (starts from 1)
        - page_size: Number of items per page (1-100)
        - date_from: Filter articles created from this date (e.g., "2025-12-20" or "2025-12-20T00:00:00")
        - date_to: Filter articles created until this date (e.g., "2025-12-28" or "2025-12-28T23:59:59")
    
    Examples:
        - Get all articles: GET /api/v1/articles
        - Get articles from Dec 20: GET /api/v1/articles?date_from=2025-12-20
        - Get articles between dates: GET /api/v1/articles?date_from=2025-12-20&date_to=2025-12-28
        - Get articles on specific date: GET /api/v1/articles?date_from=2025-12-28&date_to=2025-12-28
    
    Returns:
        Paginated list of articles filtered by created date
    """
    try:
        # Validate date formats if provided
        if date_from:
            try:
                datetime.fromisoformat(date_from.replace('Z', '+00:00'))
            except ValueError:
                raise HTTPException(
                    status_code=400, 
                    detail="Invalid date_from format. Use YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS"
                )
        
        if date_to:
            try:
                datetime.fromisoformat(date_to.replace('Z', '+00:00'))
            except ValueError:
                raise HTTPException(
                    status_code=400, 
                    detail="Invalid date_to format. Use YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS"
                )
        
        service = ArticleService(db)
        offset = (page - 1) * page_size
        
        articles = await service.get_all_articles(
            limit=page_size, 
            offset=offset,
            date_from=date_from,
            date_to=date_to
        )
        total = await service.count_articles(date_from=date_from, date_to=date_to)
        
        return ArticleListResponse(
            items=[ArticleResponse(**article) for article in articles],
            total=total,
            page=page,
            page_size=page_size
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching articles: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch articles")


@router.get("/articles/{article_id}", response_model=ArticleResponse)
async def get_article(
    article_id: int,
    db: Database = Depends(get_database)
):
    """
    Get article by ID
    
    Args:
        article_id: Article ID
        db: Database dependency
        
    Returns:
        Article details
    """
    try:
        service = ArticleService(db)
        article = await service.get_article_by_id(article_id)
        
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        
        return ArticleResponse(**article)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching article {article_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch article")


@router.post("/articles", response_model=ArticleResponse, status_code=201)
async def create_article(
    article: ArticleCreate,
    db: Database = Depends(get_database)
):
    """
    Create a new article
    
    Args:
        article: Article creation data
        db: Database dependency
        
    Returns:
        Created article
    """
    try:
        service = ArticleService(db)
        created_article = await service.create_article(article)
        return ArticleResponse(**created_article)
    except Exception as e:
        logger.error(f"Error creating article: {e}")
        raise HTTPException(status_code=500, detail="Failed to create article")


@router.put("/articles/{article_id}", response_model=ArticleResponse)
async def update_article(
    article_id: int,
    article: ArticleUpdate,
    db: Database = Depends(get_database)
):
    """
    Update an article
    
    Args:
        article_id: Article ID
        article: Article update data
        db: Database dependency
        
    Returns:
        Updated article
    """
    try:
        service = ArticleService(db)
        updated_article = await service.update_article(article_id, article)
        
        if not updated_article:
            raise HTTPException(status_code=404, detail="Article not found")
        
        return ArticleResponse(**updated_article)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating article {article_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update article")


@router.delete("/articles/{article_id}", status_code=204)
async def delete_article(
    article_id: int,
    db: Database = Depends(get_database)
):
    """
    Delete an article
    
    Args:
        article_id: Article ID
        db: Database dependency
    """
    try:
        service = ArticleService(db)
        deleted = await service.delete_article(article_id)
        
        if not deleted:
            raise HTTPException(status_code=404, detail="Article not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting article {article_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete article")

