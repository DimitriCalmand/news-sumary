"""
Article Queries module for News Summary Backend
Contains query and filtering operations for articles
"""

from typing import Dict, List, Optional

from config import BASIC_TAGS, DEBUG_LOGGING

from .article_storage import ArticleStorage


class ArticleQueries:
    """Handles article query and filtering operations"""

    @staticmethod
    def get_article_by_id(article_id: int) -> Optional[Dict]:
        """Get a specific article by its ID"""
        articles = ArticleStorage.load_articles()
        if 0 <= article_id < len(articles):
            article = articles[article_id].copy()
            article["id"] = article_id
            return article
        return None

    @staticmethod
    def get_all_tags() -> List[str]:
        """Get all unique tags from all articles"""
        articles = ArticleStorage.load_articles()
        all_tags = set()
        for article in articles:
            tags = article.get("tags", [])
            all_tags.update(tags)
        # add basic tags if not already present
        for tag in BASIC_TAGS:
            all_tags.add(tag)
        return sorted(list(all_tags))

    @staticmethod
    def get_unpretreat_articles() -> List[Dict]:
        """Get all articles that haven't been pretreated"""
        try:
            articles = ArticleStorage.load_articles()
            unpretreat = []
            for i, article in enumerate(articles):
                if not article.get("has_been_pretreat", False):
                    unpretreat.append({
                        "id": i,
                        "title": article.get("title", ""),
                        "url": article.get("url", "")
                    })
            return unpretreat
        except Exception as e:
            if DEBUG_LOGGING:
                print(f"[MODELS] Error getting unpretreat articles: {e}")
            return []

    @staticmethod
    def filter_by_tags(tags: List[str]) -> List[Dict]:
        """Filter articles by tags"""
        articles = ArticleStorage.load_articles()
        if not tags:
            return articles

        filtered = []
        for article in articles:
            article_tags = article.get("tags", [])
            if any(tag in article_tags for tag in tags):
                filtered.append(article)

        return filtered

    @staticmethod
    def filter_by_rating(min_rating: int) -> List[Dict]:
        """Filter articles by minimum rating"""
        articles = ArticleStorage.load_articles()
        filtered = []
        for article in articles:
            rating = article.get("rating")
            if rating is not None and rating >= min_rating:
                filtered.append(article)

        return filtered