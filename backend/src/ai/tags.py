"""
Tags management module for AI processing
Handles tag preparation and filtering for different sources
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import DEBUG_LOGGING, TECHCRUNCH_SOURCE, FRANCE_INFO_SOURCE, TAG_CATEGORIES, BASIC_TAGS
from models import ArticleManager


def prepare_tag_to_str(source: str = None) -> str:
    """Prepare tags string for AI, filtered by source if provided"""
    if source:
        if source == TECHCRUNCH_SOURCE:
            # TechCrunch = tags AI + tags de base
            ai_tags = [TAG_CATEGORIES["ia"]["main_tag"]] + TAG_CATEGORIES["ia"]["sub_tags"]
            tags = ai_tags + BASIC_TAGS
        elif source == FRANCE_INFO_SOURCE:
            # France Info = tags Politique + tags de base
            politique_tags = [TAG_CATEGORIES["politique"]["main_tag"]] + TAG_CATEGORIES["politique"]["sub_tags"]
            tags = politique_tags + BASIC_TAGS
        else:
            # Par défaut, tous les tags
            all_tags = []
            for category in TAG_CATEGORIES.values():
                all_tags.append(category["main_tag"])
                all_tags.extend(category["sub_tags"])
            tags = all_tags + BASIC_TAGS
    else:
        tags = ArticleManager.get_all_tags()

    if not tags:
        return "[No tags available]"
    tag_str = "["
    tag_str += ", ".join(tags)
    tag_str += "]"
    if DEBUG_LOGGING:
        print(f"[AI] Prepared tags for source '{source}': {tag_str}")
    return tag_str


def get_required_tag_for_source(source: str) -> str:
    """Get the required tag for a specific source"""
    if source == TECHCRUNCH_SOURCE:
        return TAG_CATEGORIES["ia"]["main_tag"]
    elif source == FRANCE_INFO_SOURCE:
        return TAG_CATEGORIES["politique"]["main_tag"]
    return None