"""
AI Module for News Summary Backend
Provides AI-powered article processing and chat functionality
"""

from .chat import chat_with_ai
from .models import load_models_settings
from .processing import pretreat_articles, process_article_content
from .tags import prepare_tag_to_str, get_required_tag_for_source
from .utils import extract_content_and_tags

__all__ = [
    "chat_with_ai",
    "load_models_settings",
    "pretreat_articles",
    "process_article_content",
    "prepare_tag_to_str",
    "get_required_tag_for_source",
    "extract_content_and_tags"
]