"""
Article Manager module for News Summary Backend
Main ArticleManager class that combines all article operations
"""

from typing import Dict, List, Optional

from .article_operations import ArticleOperations
from .article_queries import ArticleQueries
from .article_storage import ArticleStorage


class ArticleManager:
    """Manages article persistence and operations"""

    # Storage operations
    @staticmethod
    def load_articles() -> List[Dict]:
        return ArticleStorage.load_articles()

    @staticmethod
    def save_articles(articles: List[Dict]) -> None:
        ArticleStorage.save_articles(articles)

    @staticmethod
    def ensure_article_ids() -> None:
        ArticleStorage.ensure_article_ids()

    @staticmethod
    def add_new_articles(new_articles: List) -> int:
        return ArticleStorage.add_new_articles(new_articles)

    # Query operations
    @staticmethod
    def get_article_by_id(article_id: int) -> Optional[Dict]:
        return ArticleQueries.get_article_by_id(article_id)

    @staticmethod
    def get_all_tags() -> List[str]:
        return ArticleQueries.get_all_tags()

    @staticmethod
    def get_unpretreat_articles() -> List[Dict]:
        return ArticleQueries.get_unpretreat_articles()

    @staticmethod
    def filter_by_tags(tags: List[str]) -> List[Dict]:
        return ArticleQueries.filter_by_tags(tags)

    @staticmethod
    def filter_by_rating(min_rating: int) -> List[Dict]:
        return ArticleQueries.filter_by_rating(min_rating)

    # Operation methods
    @staticmethod
    def mark_article_as_pretreat(article_id: int) -> bool:
        return ArticleOperations.mark_article_as_pretreat(article_id)

    @staticmethod
    def update_article_rating(article_id: int, rating: int) -> bool:
        return ArticleOperations.update_article_rating(article_id, rating)

    @staticmethod
    def add_reading_time(article_id: int, seconds: int) -> bool:
        return ArticleOperations.add_reading_time(article_id, seconds)

    @staticmethod
    def update_article_comments(article_id: int, comments: str) -> bool:
        return ArticleOperations.update_article_comments(article_id, comments)

    @staticmethod
    def update_article_tags(article_id: int, tags: List[str]) -> bool:
        return ArticleOperations.update_article_tags(article_id, tags)