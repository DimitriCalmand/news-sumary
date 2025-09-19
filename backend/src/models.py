"""
Models module for News Summary Backend
Contains data models and article management functions
"""

import json
import os
from typing import List, Dict, Optional
from config import JSON_FILE, DEBUG_LOGGING


class Article:
    """Article data model"""
    
    def __init__(self, title: str, url: str, content: str = "", has_been_pretreat: bool = False):
        self.title = title
        self.url = url
        self.content = content
        self.has_been_pretreat = has_been_pretreat
    
    def to_dict(self) -> Dict:
        """Convert article to dictionary"""
        return {
            "title": self.title,
            "url": self.url,
            "content": self.content,
            "has_been_pretreat": self.has_been_pretreat
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Article':
        """Create article from dictionary"""
        return cls(
            title=data.get("title", ""),
            url=data.get("url", ""),
            content=data.get("content", ""),
            has_been_pretreat=data.get("has_been_pretreat", False)
        )


class ArticleManager:
    """Manages article persistence and operations"""
    
    @staticmethod
    def load_articles() -> List[Dict]:
        """Load articles from JSON file"""
        if os.path.exists(JSON_FILE):
            try:
                with open(JSON_FILE, "r", encoding="utf-8") as f:
                    articles = json.load(f)
                    # Ensure all articles have the has_been_pretreat field
                    for article in articles:
                        if "has_been_pretreat" not in article:
                            article["has_been_pretreat"] = False
                    return articles
            except (json.JSONDecodeError, FileNotFoundError) as e:
                if DEBUG_LOGGING:
                    print(f"[MODELS] Error loading articles: {e}")
                return []
        return []
    
    @staticmethod
    def save_articles(articles: List[Dict]) -> None:
        """Save articles to JSON file"""
        try:
            # Ensure data directory exists
            os.makedirs(os.path.dirname(JSON_FILE), exist_ok=True)
            
            with open(JSON_FILE, "w", encoding="utf-8") as f:
                json.dump(articles, f, ensure_ascii=False, indent=2)
            
            if DEBUG_LOGGING:
                print(f"[MODELS] Saved {len(articles)} articles to file")
        except Exception as e:
            if DEBUG_LOGGING:
                print(f"[MODELS] Error saving articles: {e}")
            raise
    
    @staticmethod
    def get_article_by_id(article_id: int) -> Optional[Dict]:
        """Get a specific article by its ID"""
        articles = ArticleManager.load_articles()
        if 0 <= article_id < len(articles):
            article = articles[article_id].copy()
            article["id"] = article_id
            return article
        return None
    
    @staticmethod
    def mark_article_as_pretreat(article_id: int) -> bool:
        """Mark an article as pretreated"""
        try:
            articles = ArticleManager.load_articles()
            if 0 <= article_id < len(articles):
                articles[article_id]["has_been_pretreat"] = True
                ArticleManager.save_articles(articles)
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
    def get_unpretreat_articles() -> List[Dict]:
        """Get all articles that haven't been pretreated"""
        try:
            articles = ArticleManager.load_articles()
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
    def add_new_articles(new_articles: List[Article]) -> None:
        """Add new articles to the collection"""
        if not new_articles:
            return
        
        existing_articles = ArticleManager.load_articles()
        existing_titles = {a["title"] for a in existing_articles}
        existing_urls = {a["url"] for a in existing_articles}
        
        added_count = 0
        for article in new_articles:
            if article.title not in existing_titles and article.url not in existing_urls:
                existing_articles.append(article.to_dict())
                existing_titles.add(article.title)
                existing_urls.add(article.url)
                added_count += 1
        
        if added_count > 0:
            ArticleManager.save_articles(existing_articles)
            if DEBUG_LOGGING:
                print(f"[MODELS] Added {added_count} new articles")
        
        return added_count