"""
Article Operations module for News Summary Backend
Contains operations for updating individual article properties
"""

from typing import List

from config import DEBUG_LOGGING

from .article_storage import ArticleStorage
from .tags import normalize_tags


class ArticleOperations:
    """Handles individual article update operations"""

    @staticmethod
    def mark_article_as_pretreat(article_id: int) -> bool:
        """Mark an article as pretreated"""
        try:
            articles = ArticleStorage.load_articles()
            if 0 <= article_id < len(articles):
                articles[article_id]["has_been_pretreat"] = True
                ArticleStorage.save_articles(articles)
                if DEBUG_LOGGING:
                    print(f"[MODELS] Article {article_id} marked as pretreated")
                return True
            else:
                if DEBUG_LOGGING:
                    print(f"[MODELS] Invalid article ID: {article_id}")
                return False
        except Exception as e:
            if DEBUG_LOGGING:
                print(f"[MODELS] Error marking article as pretreated: {e}")
            return False

    @staticmethod
    def update_article_rating(article_id: int, rating: int) -> bool:
        """Update article rating (1-5 stars)"""
        if not 1 <= rating <= 5:
            return False

        articles = ArticleStorage.load_articles()
        if 0 <= article_id < len(articles):
            articles[article_id]["rating"] = rating
            ArticleStorage.save_articles(articles)
            if DEBUG_LOGGING:
                print(f"[MODELS] Updated rating for article {article_id}: {rating} stars")
            return True
        return False

    @staticmethod
    def add_reading_time(article_id: int, seconds: int) -> bool:
        """Add reading time to article (cumulative)"""
        articles = ArticleStorage.load_articles()
        if 0 <= article_id < len(articles):
            current_time = articles[article_id].get("time_spent", 0)
            articles[article_id]["time_spent"] = current_time + 1
            ArticleStorage.save_articles(articles)
            if DEBUG_LOGGING:
                print(f"[MODELS] Added {seconds}s to article {article_id} (total: {articles[article_id]['time_spent']}s)")
            return True
        return False

    @staticmethod
    def update_article_comments(article_id: int, comments: str) -> bool:
        """Update article comments"""
        articles = ArticleStorage.load_articles()
        if 0 <= article_id < len(articles):
            articles[article_id]["comments"] = comments
            ArticleStorage.save_articles(articles)
            if DEBUG_LOGGING:
                print(f"[MODELS] Updated comments for article {article_id}")
            return True
        return False

    @staticmethod
    def update_article_tags(article_id: int, tags: List[str]) -> bool:
        """Update article tags"""
        articles = ArticleStorage.load_articles()
        if 0 <= article_id < len(articles):
            # Normalize tags using the comprehensive normalization function
            normalized_tags = normalize_tags(tags)
            articles[article_id]["tags"] = normalized_tags
            ArticleStorage.save_articles(articles)
            if DEBUG_LOGGING:
                print(f"[MODELS] Updated tags for article {article_id}: {normalized_tags}")
            return True
        return False