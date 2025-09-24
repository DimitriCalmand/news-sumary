"""
Cache module for News Summary Backend
Manages in-memory caching of articles for better performance
"""

import time
from typing import Dict, List, Optional

from config import CACHE_DURATION, DEBUG_LOGGING
from models import ArticleManager


class ArticleCache:
    """In-memory cache for articles with automatic expiration"""
    
    def __init__(self):
        self._cache: List[Dict] = []
        self._cache_timestamp: float = 0
        self._cache_duration = CACHE_DURATION
    
    def _matches_search(self, title: str, search_term: str) -> bool:
        """
        Check if a title matches the search term using fuzzy search logic
        
        Args:
            title: Article title to search in
            search_term: Search term to match
        
        Returns:
            True if the title matches the search term
        """
        if not title or not search_term:
            return False
            
        title_lower = title.lower()
        search_lower = search_term.lower()
        
        # Recherche exacte d'abord (plus rapide)
        if search_lower in title_lower:
            return True
        
        # Recherche par mots pour les termes multi-mots
        title_words = title_lower.split()
        search_words = search_lower.split()
        
        # Si la recherche contient plusieurs mots, tous doivent matcher
        return all(
            any(search_word in title_word or 
                (len(title_word) > 3 and len(search_word) > 3 and 
                 self._calculate_similarity(title_word, search_word) >= 0.8)
                for title_word in title_words)
            for search_word in search_words
        )
    
    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """
        Calculate similarity between two strings using Levenshtein distance
        
        Args:
            str1: First string
            str2: Second string
        
        Returns:
            Similarity score between 0 and 1
        """
        if len(str1) < len(str2):
            return self._calculate_similarity(str2, str1)

        if len(str2) == 0:
            return 1.0

        previous_row = list(range(len(str2) + 1))
        for i, c1 in enumerate(str1):
            current_row = [i + 1]
            for j, c2 in enumerate(str2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return (len(str2) - previous_row[-1]) / len(str2)
    
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
    
    def get_paginated_titles(self, page: int, per_page: int, sort_by: str = 'date', search: Optional[str] = None) -> Dict:
        """
        Get paginated article titles with sorting and optional search
        
        Args:
            page: Page number (1-based)
            per_page: Number of articles per page
            sort_by: Sort order ('date' for newest first, 'order' for insertion order)
            search: Optional search term to filter titles
        
        Returns:
            Dictionary with titles and pagination info
        """
        articles = self.get_articles()
        
        # Appliquer le filtre de recherche si fourni
        if search and search.strip():
            search_term = search.strip().lower()
            # Utiliser la même logique de recherche floue que le frontend
            articles = [article for article in articles if self._matches_search(article.get('title', ''), search_term)]
        
        # Trier les articles selon le paramètre sort_by
        if sort_by == 'date':
            # Trier par date (plus récents en premier), puis par ordre d'arrivée (id) si pas de date
            articles_sorted = sorted(articles, key=lambda x: (
                x.get('date', '1900-01-01'),  # Date par défaut très ancienne si pas de date
                x.get('id', 0)  # ID croissant comme second critère
            ), reverse=True)
        else:
            # Garder l'ordre d'insertion (ordre original)
            articles_sorted = articles
        
        # Calculate indices
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        
        # Extract slice
        articles_slice = articles_sorted[start_index:end_index]
        
        # Create titles with minimal data
        titles = []
        for i, article in enumerate(articles_slice):
            titles.append({
                "id": article.get("id", start_index + i),  # Utiliser l'ID original de l'article
                "title": article.get("title", ""),
                "url": article.get("url", ""),
                "has_been_pretreat": article.get("has_been_pretreat", False),
                "rating": article.get("rating"),  # Inclure rating pour l'affichage des notes
                "time_spent": article.get("time_spent", 0),
                "comments": article.get("comments", ""),  # Inclure comments pour l'affichage des notes
                "tags": article.get("tags", []),  # Ajouter les tags
                "source": article.get("source"),  # Source de l'article
                "scraped_date": article.get("scraped_date"),  # Date de scraping
                "date": article.get("date", None)
            })
        
        return {
            "titles": titles,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": len(articles),
                "returned": len(titles),
                "sort_by": sort_by
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