"""
Models module for News Summary Backend
Contains data models and article management functions
"""

import json
import os
from typing import Dict, List, Optional

from config import DEBUG_LOGGING, JSON_FILE


class Article:
    """Article data model"""
    
    def __init__(self, title: str, url: str, content: str = "", has_been_pretreat: bool = False, 
                 rating: Optional[int] = None, time_spent: int = 0, comments: str = "", 
                 tags: Optional[List[str]] = None):
        self.title = title
        self.url = url
        self.content = content
        self.has_been_pretreat = has_been_pretreat
        self.rating = rating  # Note de 1 à 5 étoiles
        self.time_spent = time_spent  # Temps passé en secondes
        self.comments = comments  # Commentaires personnels
        self.tags = tags or []  # Liste des tags
    
    def to_dict(self) -> Dict:
        """Convert article to dictionary"""
        return {
            "title": self.title,
            "url": self.url,
            "content": self.content,
            "has_been_pretreat": self.has_been_pretreat,
            "rating": self.rating,
            "time_spent": self.time_spent,
            "comments": self.comments,
            "tags": self.tags
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Article':
        """Create article from dictionary"""
        return cls(
            title=data.get("title", ""),
            url=data.get("url", ""),
            content=data.get("content", ""),
            has_been_pretreat=data.get("has_been_pretreat", False),
            rating=data.get("rating"),
            time_spent=data.get("time_spent", 0),
            comments=data.get("comments", ""),
            tags=data.get("tags", [])
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
    
    @staticmethod
    def update_article_rating(article_id: int, rating: int) -> bool:
        """Update article rating (1-5 stars)"""
        if not 1 <= rating <= 5:
            return False
        
        articles = ArticleManager.load_articles()
        if 0 <= article_id < len(articles):
            articles[article_id]["rating"] = rating
            ArticleManager.save_articles(articles)
            if DEBUG_LOGGING:
                print(f"[MODELS] Updated rating for article {article_id}: {rating} stars")
            return True
        return False
    
    @staticmethod
    def add_reading_time(article_id: int, seconds: int) -> bool:
        """Add reading time to article (cumulative)"""
        articles = ArticleManager.load_articles()
        if 0 <= article_id < len(articles):
            current_time = articles[article_id].get("time_spent", 0)
            articles[article_id]["time_spent"] = current_time + 1
            ArticleManager.save_articles(articles)
            if DEBUG_LOGGING:
                print(f"[MODELS] Added {seconds}s to article {article_id} (total: {articles[article_id]['time_spent']}s)")
            return True
        return False
    
    @staticmethod
    def update_article_comments(article_id: int, comments: str) -> bool:
        """Update article comments"""
        articles = ArticleManager.load_articles()
        if 0 <= article_id < len(articles):
            articles[article_id]["comments"] = comments
            ArticleManager.save_articles(articles)
            if DEBUG_LOGGING:
                print(f"[MODELS] Updated comments for article {article_id}")
            return True
        return False
    
    @staticmethod
    def update_article_tags(article_id: int, tags: List[str]) -> bool:
        """Update article tags"""
        articles = ArticleManager.load_articles()
        if 0 <= article_id < len(articles):
            # Clean and validate tags
            clean_tags = [tag.strip().lower() for tag in tags if tag.strip()]
            articles[article_id]["tags"] = clean_tags
            ArticleManager.save_articles(articles)
            if DEBUG_LOGGING:
                print(f"[MODELS] Updated tags for article {article_id}: {clean_tags}")
            return True
        return False
    
    @staticmethod
    def get_all_tags() -> List[str]:
        """Get all unique tags from all articles"""
        articles = ArticleManager.load_articles()
        all_tags = set()
        for article in articles:
            tags = article.get("tags", [])
            all_tags.update(tags)
        return sorted(list(all_tags))
    
    @staticmethod
    def filter_by_tags(tags: List[str]) -> List[Dict]:
        """Filter articles by tags"""
        articles = ArticleManager.load_articles()
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
        articles = ArticleManager.load_articles()
        filtered = []
        for article in articles:
            rating = article.get("rating")
            if rating is not None and rating >= min_rating:
                filtered.append(article)
        
        return filtered