"""
Article processing module
Handles AI-powered article content processing and tag generation
"""

import sys
import os
import requests
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import DEBUG_LOGGING
from models import ArticleManager
from settings import SettingsManager

from .models import load_models_settings
from .tags import get_required_tag_for_source, prepare_tag_to_str
from .utils import extract_content_and_tags


def process_article_content(content: str, model_name: str, source: str = None) -> tuple[str, list]:
    """
    Process article content using AI model

    Args:
        content: Article content to process
        model_name: Name of the AI model to use
        source: Article source for tag filtering

    Returns:
        tuple: (processed_content, tags_list)
    """
    model = load_models_settings(model_name)
    if not model:
        if DEBUG_LOGGING:
            print(f"[AI] No settings found for model: {model_name}. Returning original content.")
        return content, []  # Return original content if no model settings found

    url = model.get("url")
    api_key = model.get("apikey")
    model_id = model.get("id")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    body = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": SettingsManager.get_prompt("article_processing").format(tags=prepare_tag_to_str(source))},
            {"role": "user", "content": f"Pretreat the following article content:\n\n{content}"}
        ]
    }

    response = requests.post(url, headers=headers, json=body)

    if response.status_code == 200:
        ai_response = response.json().get("choices", [])[0].get("message", {}).get("content", "")
        if DEBUG_LOGGING:
            print(f"[AI] Raw AI response: {ai_response}")
        processed_content, tags = extract_content_and_tags(ai_response)
        return processed_content, tags
    else:
        if DEBUG_LOGGING:
            print(f"[AI] Error processing article content: {response.status_code} {response.text}")
        return content, []


def pretreat_articles() -> None:
    """Pretreat articles that have not been pretreat yet using an AI model"""
    if DEBUG_LOGGING:
        print("[AI] Starting pretreatment of articles")

    articles = ArticleManager.load_articles()

    for article in articles:
        if not article.get("has_been_pretreat", False):
            if DEBUG_LOGGING:
                print(f"[AI] Pretreating article: {article['title']}")

            # Process article content
            article_source = article.get("source", "")
            processed_content, ai_tags = process_article_content(
                article["content"],
                "mistral small",
                article_source
            )

            if DEBUG_LOGGING:
                print(f"[AI] Processed content: {processed_content[:60]}...")  # Print first 60 chars
                print(f"[AI] AI suggested tags: {ai_tags}")

            # Add required tag based on source
            required_tag = get_required_tag_for_source(article_source)
            final_tags = ai_tags.copy() if ai_tags else []

            # Add required tag if not already present
            if required_tag and required_tag not in final_tags:
                final_tags.append(required_tag)
                if DEBUG_LOGGING:
                    print(f"[AI] Added required tag '{required_tag}' for source '{article_source}'")

            # Merge with existing tags if any
            existing_tags = article.get("tags", [])
            if existing_tags:
                # Merge existing with new tags, remove duplicates
                all_tags = list(set(existing_tags + final_tags))
                final_tags = all_tags
                if DEBUG_LOGGING:
                    print(f"[AI] Merged with existing tags: {existing_tags} -> {final_tags}")

            # Update article
            article["content"] = processed_content
            article["has_been_pretreat"] = True
            article["tags"] = final_tags

            ArticleManager.save_articles(articles)

            if DEBUG_LOGGING:
                print(f"[AI] Article '{article['title']}' saved with final tags: {final_tags}")

    return None