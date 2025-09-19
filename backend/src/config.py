"""
Configuration module for News Summary Backend
Contains all configuration constants and settings
"""

import os

# File paths
JSON_FILE = "./data/articles_seen.json"

# Cache settings
CACHE_DURATION = 60  # Cache valid for 60 seconds

# TechCrunch scraping settings
TECHCRUNCH_URL = "https://techcrunch.com/category/artificial-intelligence/"
TITLE_CLASS = "loop-card__title"
PARAGRAPH_CLASS = "wp-block-paragraph"

# Scraping intervals
SCRAPING_INTERVAL = 1800  # 30 minutes in seconds

# Flask settings
CORS_ORIGINS = ['http://localhost:5173', 'http://localhost:3000']
DEFAULT_PORT = 3001

# Debug settings
DEBUG_LOGGING = True
FLASK_DEBUG = True  # Active le hot reload en développement

# AI  model settings
MODEL_CONFIG_FILE = "./data/models.json"
PROMPT_MESSAGE = "Tu vas recevoir un article.\n1) Fais un résumé clair et concis au début.\n2) Réécris ensuite l'article en ajoutant des emojis pertinents, en mettant en **gras** certains mots, et en structurant le texte avec des sections et titres si nécessaire, sans modifier le contenu ni l'ordre des idées.\n3) Ne renvoie rien d'autre que le résumé suivi du nouvel article, sans ajouter de message ou commentaire hors du texte."

def get_port():
    """Get the port from environment variable or use default"""
    return int(os.getenv("PORT", DEFAULT_PORT))

def get_environment():
    """Get the current environment"""
    return os.getenv("FLASK_ENV", "development")

def is_production():
    """Check if running in production"""
    return get_environment() == "production"

def is_development():
    """Check if running in development"""
    return get_environment() == "development"