"""
Article Storage module for News Summary Backend
Contains storage-related operations for articles
"""

import os
from typing import Dict, List

from config import DEBUG_LOGGING, JSON_FILE

from .article import Article


class ArticleStorage:
    """Handles article persistence operations"""

    @staticmethod
    def load_articles() -> List[Dict]:
        """Load articles from JSON file"""
        import json

        if os.path.exists(JSON_FILE):
            try:
                with open(JSON_FILE, "r", encoding="utf-8") as f:
                    articles = json.load(f)
                    # Ensure all articles have the has_been_pretreat field and an ID
                    for i, article in enumerate(articles):
                        if "has_been_pretreat" not in article:
                            article["has_been_pretreat"] = False
                        # Add ID if missing (use index as ID)
                        if "id" not in article or article["id"] is None:
                            article["id"] = i
                    return articles
            except (json.JSONDecodeError, FileNotFoundError) as e:
                if DEBUG_LOGGING:
                    print(f"[MODELS] Error loading articles: {e}")
                return []
        return []

    @staticmethod
    def save_articles(articles: List[Dict]) -> None:
        """Save articles to JSON file"""
        import json

        try:
            # Ensure data directory exists
            os.makedirs(os.path.dirname(JSON_FILE), exist_ok=True)

            # Ensure all articles have IDs before saving
            for i, article in enumerate(articles):
                if "id" not in article or article["id"] is None:
                    article["id"] = i

            with open(JSON_FILE, "w", encoding="utf-8") as f:
                json.dump(articles, f, ensure_ascii=False, indent=2)

            if DEBUG_LOGGING:
                print(f"[MODELS] Saved {len(articles)} articles to file")
        except Exception as e:
            if DEBUG_LOGGING:
                print(f"[MODELS] Error saving articles: {e}")
            raise

    @staticmethod
    def ensure_article_ids() -> None:
        """Ensure all articles have proper IDs and save them"""
        try:
            articles = ArticleStorage.load_articles()
            needs_save = False

            for i, article in enumerate(articles):
                if "id" not in article or article["id"] is None or article["id"] != i:
                    article["id"] = i
                    needs_save = True

            if needs_save:
                ArticleStorage.save_articles(articles)
                if DEBUG_LOGGING:
                    print(f"[MODELS] Updated IDs for {len(articles)} articles")
        except Exception as e:
            if DEBUG_LOGGING:
                print(f"[MODELS] Error ensuring article IDs: {e}")

    @staticmethod
    def add_new_articles(new_articles: List[Article]) -> int:
        """Add new articles to the collection"""
        if not new_articles:
            return 0

        existing_articles = ArticleStorage.load_articles()
        existing_titles = {a["title"] for a in existing_articles}
        existing_urls = {a["url"] for a in existing_articles}

        added_count = 0
        for article in new_articles:
            if article.title not in existing_titles and article.url not in existing_urls:
                existing_articles.append(article.to_dict())
                existing_titles.add(article.title)
                existing_urls.add(article.url)
                added_count += 1
                # add tags, rating, comments, time_spent as default values
                article.tags = article.tags or []
                article.rating = article.rating or None
                article.comments = article.comments or ""
                article.time_spent = article.time_spent or 0


        if added_count > 0:
            ArticleStorage.save_articles(existing_articles)
            if DEBUG_LOGGING:
                print(f"[MODELS] Added {added_count} new articles")

        return added_count