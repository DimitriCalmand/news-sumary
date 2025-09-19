"""
Cache module for News Summary Backend
Manages in-memory caching of articles for better performance
"""

import time
from typing import List, Dict, Optional
from config import CACHE_DURATION, DEBUG_LOGGING
from models import ArticleManager


class ArticleCache:
    """In-memory cache for articles with automatic expiration"""
    
    def __init__(self):
        self._cache: List[Dict] = []
        self._cache_timestamp: float = 0
        self._cache_duration = CACHE_DURATION
    
    def is_cache_valid(self) -> bool:
        """Check if the current cache is still valid"""
        if not self._cache:
            return False
        
        current_time = time.time()
        return (current_time - self._cache_timestamp) <= self._cache_duration
    
    def invalidate_cache(self) -> None:
        """Manually invalidate the cache"""
        self._cache_timestamp = 0
        if DEBUG_LOGGING:
            print("[CACHE] Cache manually invalidated")
    
    def get_articles(self, force_refresh: bool = False) -> List[Dict]:
        """
        Get articles from cache or reload from storage if expired
        
        Args:
            force_refresh: If True, bypass cache and reload from storage
        
        Returns:
            List of article dictionaries
        """
        current_time = time.time()
        
        # Check if we need to refresh the cache
        if force_refresh or not self.is_cache_valid():
            try:
                self._cache = ArticleManager.load_articles()
                self._cache_timestamp = current_time
                
                if DEBUG_LOGGING:
                    print(f"[CACHE] Articles reloaded in cache: {len(self._cache)} articles")
                    
            except Exception as e:
                if DEBUG_LOGGING:
                    print(f"[CACHE] Error loading articles: {e}")
                # Return empty list if there's an error
                self._cache = []
                self._cache_timestamp = current_time
        
        return self._cache.copy()  # Return a copy to prevent external modifications
    
    def get_cache_info(self) -> Dict:
        """Get information about the current cache status"""
        current_time = time.time()
        age = current_time - self._cache_timestamp if self._cache_timestamp > 0 else -1
        
        return {
            "cache_size": len(self._cache),
            "cache_age_seconds": age,
            "cache_valid": self.is_cache_valid(),
            "cache_duration": self._cache_duration,
            "last_updated": self._cache_timestamp
        }
    
    def get_articles_count(self) -> int:
        """Get the total number of articles in cache"""
        articles = self.get_articles()
        return len(articles)
    
    def get_article_by_id(self, article_id: int) -> Optional[Dict]:
        """Get a specific article by ID from cache"""
        articles = self.get_articles()
        if 0 <= article_id < len(articles):
            article = articles[article_id].copy()
            article["id"] = article_id
            return article
        return None
    
    def get_paginated_articles(self, start: int, end: int) -> Dict:
        """
        Get a paginated slice of articles
        
        Args:
            start: Starting position (1-based)
            end: Ending position (inclusive)
        
        Returns:
            Dictionary with articles and pagination info
        """
        articles = self.get_articles()
        
        # Convert 1-based to 0-based indexing
        start_index = max(0, start - 1)
        end_index = min(end, len(articles))
        
        articles_slice = articles[start_index:end_index]
        
        return {
            "articles": articles_slice,
            "pagination": {
                "start": start,
                "end": min(end, len(articles)),
                "total": len(articles),
                "returned": len(articles_slice)
            }
        }
    
    def get_paginated_titles(self, page: int, per_page: int) -> Dict:
        """
        Get paginated article titles
        
        Args:
            page: Page number (1-based)
            per_page: Number of articles per page
        
        Returns:
            Dictionary with titles and pagination info
        """
        articles = self.get_articles()
        
        # Calculate indices
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        
        # Extract slice
        articles_slice = articles[start_index:end_index]
        
        # Create titles with minimal data
        titles = []
        for i, article in enumerate(articles_slice):
            titles.append({
                "id": start_index + i,
                "title": article.get("title", ""),
                "url": article.get("url", ""),
                "has_been_pretreat": article.get("has_been_pretreat", False)
            })
        
        return {
            "titles": titles,
            "pagination": {
                "start": start_index + 1,
                "end": min(end_index, len(articles)),
                "total": len(articles),
                "returned": len(titles)
            }
        }
    
    def update_cache_after_modification(self) -> None:
        """Update cache after articles have been modified externally"""
        self.invalidate_cache()
        # Preload the cache with fresh data
        self.get_articles(force_refresh=True)


# Global cache instance
article_cache = ArticleCache()


def get_cached_articles(force_refresh: bool = False) -> List[Dict]:
    """Get articles from the global cache"""
    return article_cache.get_articles(force_refresh)


def invalidate_article_cache() -> None:
    """Invalidate the global article cache"""
    article_cache.invalidate_cache()


def get_cache_stats() -> Dict:
    """Get cache statistics"""
    return article_cache.get_cache_info()