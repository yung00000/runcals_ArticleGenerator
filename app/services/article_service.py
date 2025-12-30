"""
Article service layer for business logic
"""
from typing import List, Optional
from app.database import Database
from app.models.schemas import ArticleCreate, ArticleUpdate, ArticleResponse
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class ArticleService:
    """Service for article-related operations"""
    
    def __init__(self, db: Database):
        self.db = db
    
    async def get_all_articles(
        self,
        limit: int = 10,
        offset: int = 0,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None
    ) -> List[dict]:
        """
        Get all articles with pagination and optional date filtering
        
        Args:
            limit: Number of articles to return
            offset: Number of articles to skip
            date_from: Filter articles from this date (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)
            date_to: Filter articles until this date (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)
            
        Returns:
            List of article dictionaries
        """
        try:
            conditions = []
            params = {}
            param_num = 1
            
            # Add date filtering
            if date_from:
                param_name = f"date_from_{param_num}"
                conditions.append(f"created_at >= :{param_name}")
                params[param_name] = date_from
                param_num += 1
            
            if date_to:
                param_name = f"date_to_{param_num}"
                conditions.append(f"created_at <= :{param_name}")
                params[param_name] = date_to
                param_num += 1
            
            # Build WHERE clause
            where_clause = ""
            if conditions:
                where_clause = "WHERE " + " AND ".join(conditions)
            
            # Add pagination parameters
            params['limit_val'] = limit
            params['offset_val'] = offset
            
            query = f"""
                SELECT id, title, content, created_at
                FROM running_articles
                {where_clause}
                ORDER BY created_at DESC
                LIMIT :limit_val OFFSET :offset_val
            """
            
            rows = await self.db.fetch(query, **params)
            return rows
        except Exception as e:
            logger.error(f"Error fetching articles: {e}")
            raise
    
    async def get_article_by_id(self, article_id: int) -> Optional[dict]:
        """
        Get article by ID
        
        Args:
            article_id: Article ID
            
        Returns:
            Article dictionary or None if not found
        """
        try:
            query = """
                SELECT id, title, content, created_at
                FROM running_articles
                WHERE id = :article_id
            """
            row = await self.db.fetchrow(query, article_id=article_id)
            return row if row else None
        except Exception as e:
            logger.error(f"Error fetching article {article_id}: {e}")
            raise
    
    async def create_article(self, article: ArticleCreate) -> dict:
        """
        Create a new article
        
        Args:
            article: Article creation data
            
        Returns:
            Created article dictionary
        """
        try:
            query = """
                INSERT INTO running_articles (title, content)
                VALUES (:title, :content)
                RETURNING id, title, content, created_at
            """
            row = await self.db.fetchrow(
                query,
                title=article.title,
                content=article.content
            )
            return row
        except Exception as e:
            logger.error(f"Error creating article: {e}")
            raise
    
    async def update_article(
        self,
        article_id: int,
        article: ArticleUpdate
    ) -> Optional[dict]:
        """
        Update an article
        
        Args:
            article_id: Article ID
            article: Article update data
            
        Returns:
            Updated article dictionary or None if not found
        """
        try:
            # Build dynamic update query
            updates = []
            params = {}
            param_num = 1
            
            if article.title is not None:
                param_name = f"title_{param_num}"
                updates.append(f"title = :{param_name}")
                params[param_name] = article.title
                param_num += 1
            
            if article.content is not None:
                param_name = f"content_{param_num}"
                updates.append(f"content = :{param_name}")
                params[param_name] = article.content
                param_num += 1
            
            if not updates:
                return await self.get_article_by_id(article_id)
            
            params['article_id'] = article_id
            
            query = f"""
                UPDATE running_articles
                SET {', '.join(updates)}
                WHERE id = :article_id
                RETURNING id, title, content, created_at
            """
            
            row = await self.db.fetchrow(query, **params)
            return row if row else None
        except Exception as e:
            logger.error(f"Error updating article {article_id}: {e}")
            raise
    
    async def delete_article(self, article_id: int) -> bool:
        """
        Delete an article
        
        Args:
            article_id: Article ID
            
        Returns:
            True if deleted, False if not found
        """
        try:
            query = "DELETE FROM running_articles WHERE id = :article_id RETURNING id"
            result = await self.db.fetchrow(query, article_id=article_id)
            return result is not None
        except Exception as e:
            logger.error(f"Error deleting article {article_id}: {e}")
            raise
    
    async def count_articles(
        self,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None
    ) -> int:
        """
        Get total count of articles with optional date filtering
        
        Args:
            date_from: Filter articles from this date (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)
            date_to: Filter articles until this date (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)
            
        Returns:
            Total number of articles
        """
        try:
            conditions = []
            params = {}
            param_num = 1
            
            # Add date filtering
            if date_from:
                param_name = f"date_from_{param_num}"
                conditions.append(f"created_at >= :{param_name}")
                params[param_name] = date_from
                param_num += 1
            
            if date_to:
                param_name = f"date_to_{param_num}"
                conditions.append(f"created_at <= :{param_name}")
                params[param_name] = date_to
                param_num += 1
            
            # Build WHERE clause
            where_clause = ""
            if conditions:
                where_clause = "WHERE " + " AND ".join(conditions)
            
            query = f"SELECT COUNT(*) FROM running_articles {where_clause}"
            count = await self.db.fetchval(query, **params) if params else await self.db.fetchval(query)
            return int(count) if count is not None else 0
        except Exception as e:
            logger.error(f"Error counting articles: {e}")
            raise

