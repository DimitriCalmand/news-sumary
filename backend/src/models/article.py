"""
Article model module for News Summary Backend
Contains the Article data model class
"""

from datetime import datetime
from typing import Dict, List, Optional

from .tags import normalize_tags


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