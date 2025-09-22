"""
Models module for News Summary Backend
Contains data models and article management functions
"""

import json
import os
import re
from datetime import datetime
from typing import Dict, List, Optional

from config import BASIC_TAGS, DEBUG_LOGGING, JSON_FILE


def normalize_tag(tag: str) -> str:
    """
    Normalise un tag en:
    - convertissant en minuscules
    - supprimant les caractères spéciaux sauf lettres, chiffres, espaces et tirets
    - supprimant les espaces en début/fin
    - remplaçant les espaces multiples par un seul
    """
    if not tag or not isinstance(tag, str):
        return ""
    
    # Convertir en minuscules
    tag = tag.lower().strip()
    
    # Garder seulement lettres, chiffres, espaces, tirets et caractères accentués
    tag = re.sub(r'[^\w\s\-àâäçéèêëïîôöùûüÿ]', '', tag)
    
    # Remplacer plusieurs espaces par un seul
    tag = re.sub(r'\s+', ' ', tag)
    
    # Supprimer les espaces en début/fin
    tag = tag.strip()
    
    return tag


def normalize_tags(tags: List[str]) -> List[str]:
    """
    Normalise une liste de tags en:
    - normalisant chaque tag
    - supprimant les doublons
    - supprimant les tags vides
    """
    if not tags:
        return []
    
    normalized = []
    seen = set()
    
    for tag in tags:
        normalized_tag = normalize_tag(tag)
        if normalized_tag and normalized_tag not in seen:
            normalized.append(normalized_tag)
            seen.add(normalized_tag)
            if DEBUG_LOGGING and normalized_tag != tag:
                print(f"[MODELS] Tag normalized: '{tag}' -> '{normalized_tag}'")
    
    return normalized


class Article:
    """Article data model"""
    
    def __init__(self, title: str, url: str, content: str = "", has_been_pretreat: bool = False, 
                 rating: Optional[int] = None, time_spent: int = 0, comments: str = "", 
                 tags: Optional[List[str]] = None, source: str = "", scraped_date: Optional[str] = None):
        self.title = title
        self.url = url
        self.content = content
        self.has_been_pretreat = has_been_pretreat
        self.rating = rating  # Note de 1 à 5 étoiles
        self.time_spent = time_spent  # Temps passé en secondes
        self.comments = comments  # Commentaires personnels
        self.tags = normalize_tags(tags or [])  # Liste des tags normalisés
        self.source = source  # Source de l'article (TechCrunch, France Info, etc.)
        self.scraped_date = scraped_date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Date et heure de scraping
    
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
            "tags": normalize_tags(self.tags),  # Normaliser les tags lors de la sauvegarde
            "source": self.source,
            "scraped_date": self.scraped_date
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
            tags=normalize_tags(data.get("tags", [])),  # Normaliser les tags lors du chargement
            source=data.get("source", ""),
            scraped_date=data.get("scraped_date", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
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
    def get_article_by_id(article_id: int) -> Optional[Dict]:
        """Get a specific article by its ID"""
        articles = ArticleManager.load_articles()
        if 0 <= article_id < len(articles):
            article = articles[article_id].copy()
            article["id"] = article_id
            return article
        return None
    
    @staticmethod
    def ensure_article_ids() -> None:
        """Ensure all articles have proper IDs and save them"""
        try:
            articles = ArticleManager.load_articles()
            needs_save = False
            
            for i, article in enumerate(articles):
                if "id" not in article or article["id"] is None or article["id"] != i:
                    article["id"] = i
                    needs_save = True
            
            if needs_save:
                ArticleManager.save_articles(articles)
                if DEBUG_LOGGING:
                    print(f"[MODELS] Updated IDs for {len(articles)} articles")
        except Exception as e:
            if DEBUG_LOGGING:
                print(f"[MODELS] Error ensuring article IDs: {e}")
    
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
    def get_all_tags() -> List[str]:
        """Get all unique tags from all articles"""
        articles = ArticleManager.load_articles()
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
                # add tags, rating, comments, time_spent as default values
                article.tags = article.tags or []
                article.rating = article.rating or None
                article.comments = article.comments or ""
                article.time_spent = article.time_spent or 0
                
        
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
            # Normalize tags using the comprehensive normalization function
            normalized_tags = normalize_tags(tags)
            articles[article_id]["tags"] = normalized_tags
            ArticleManager.save_articles(articles)
            if DEBUG_LOGGING:
                print(f"[MODELS] Updated tags for article {article_id}: {normalized_tags}")
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


class ChatManager:
    """Manager for chat conversations with AI about articles"""
    
    CHAT_FILE = "./data/chat_history.json"
    
    @staticmethod
    def load_conversations() -> Dict:
        """Load all conversations from file"""
        try:
            if os.path.exists(ChatManager.CHAT_FILE):
                with open(ChatManager.CHAT_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            if DEBUG_LOGGING:
                print(f"[CHAT] Error loading conversations: {e}")
            return {}
    
    @staticmethod
    def save_conversations(conversations: Dict) -> bool:
        """Save all conversations to file"""
        try:
            # Ensure data directory exists
            os.makedirs("./data", exist_ok=True)
            
            with open(ChatManager.CHAT_FILE, 'w', encoding='utf-8') as f:
                json.dump(conversations, f, ensure_ascii=False, indent=2)
            
            if DEBUG_LOGGING:
                print(f"[CHAT] Conversations saved successfully")
            return True
        except Exception as e:
            if DEBUG_LOGGING:
                print(f"[CHAT] Error saving conversations: {e}")
            return False
    
    @staticmethod
    def get_conversation(article_id: str) -> List[Dict]:
        """Get conversation history for a specific article"""
        conversations = ChatManager.load_conversations()
        return conversations.get(article_id, [])
    
    @staticmethod
    def add_message(article_id: str, message_type: str, content: str, model_used: str = None) -> bool:
        """
        Add a message to the conversation
        
        Args:
            article_id: ID of the article
            message_type: 'user' or 'ai'
            content: Message content
            model_used: AI model used (for AI messages)
        """
        try:
            conversations = ChatManager.load_conversations()
            
            if article_id not in conversations:
                conversations[article_id] = []
            
            message = {
                "id": str(len(conversations[article_id]) + 1),
                "type": message_type,
                "content": content,
                "timestamp": json.dumps({"$date": {"$numberLong": str(int(1000 * __import__('time').time()))}}),
                "model_used": model_used if message_type == 'ai' else None
            }
            
            conversations[article_id].append(message)
            
            return ChatManager.save_conversations(conversations)
        except Exception as e:
            if DEBUG_LOGGING:
                print(f"[CHAT] Error adding message: {e}")
            return False
    
    @staticmethod
    def clear_conversation(article_id: str) -> bool:
        """Clear conversation history for a specific article"""
        try:
            conversations = ChatManager.load_conversations()
            if article_id in conversations:
                conversations[article_id] = []
                return ChatManager.save_conversations(conversations)
            return True
        except Exception as e:
            if DEBUG_LOGGING:
                print(f"[CHAT] Error clearing conversation: {e}")
            return False