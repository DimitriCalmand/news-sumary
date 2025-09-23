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

# France Info scraping settings
FRANCE_INFO_BASE_URL = "https://www.franceinfo.fr"
FRANCE_INFO_POLITIQUE_URL = FRANCE_INFO_BASE_URL + "/europe/"
FRANCE_INFO_CARD_CLASSES = ["card-article-m__link", "card-article-majeure__link"]
FRANCE_INFO_CONTENT_CLASS = "c-body"

# Sources
TECHCRUNCH_SOURCE = "TechCrunch"
FRANCE_INFO_SOURCE = "France Info"

# Système de tags hiérarchique
TAG_CATEGORIES = {
    "ia": {
        "main_tag": "ia",
        "sub_tags": [
            "découverte", "technologie", "innovation", "économie", "finance", "entreprise", "juridique", "santé", "éducation", "productivité"
        ]
    },
    "politique": {
        "main_tag": "politique",
        "sub_tags": [
            "elections",
            "gouvernement",
            "parlement",
            "union européenne",
            "relations internationales",
            "économie politique",
            "réformes",
            "débats publics",
            "institutions",
            "politique sociale"
        ]
    }
}

# Tags obligatoires (catégories principales)
REQUIRED_TAGS = ["ia", "politique"]

# Tags de base pour compléter (tags fréquents)
BASIC_TAGS = []

# Scraping intervals
SCRAPING_INTERVAL = 1800  # 30 minutes in seconds

# Flask settings
CORS_ORIGINS = ['http://localhost:5173', 'http://localhost:3000']
DEFAULT_PORT = 3001

# Debug settings
DEBUG_LOGGING = True
FLASK_DEBUG = True  # Active le hot reload en développement

# AI model settings
MODEL_CONFIG_FILE = "./data/models.json"
SETTINGS_CONFIG_FILE = "./data/settings.json"

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