"""
AI Chat module
Handles conversational AI interactions about articles
"""

import sys
import os
import requests
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import DEBUG_LOGGING
from models import ArticleManager
from settings import SettingsManager

from .models import load_models_settings


def chat_with_ai(article_id: str, user_question: str, model_name: str = None) -> dict:
    """
    Chat with AI about a specific article

    Args:
        article_id: ID of the article to discuss
        user_question: User's question about the article
        model_name: Name of the AI model to use (optional, uses configured chat model if not provided)

    Returns:
        dict: Response with success status and AI answer or error
    """
    # Use configured chat model if none specified
    if model_name is None:
        model_name = SettingsManager.get_chat_model()
    try:
        # Get article details
        articles = ArticleManager.load_articles()

        if DEBUG_LOGGING:
            print(f"[AI_CHAT] Looking for article_id: '{article_id}' (type: {type(article_id)})")
            print(f"[AI_CHAT] Total articles loaded: {len(articles)}")
            if articles:
                print(f"[AI_CHAT] First article ID: '{articles[0].get('id')}' (type: {type(articles[0].get('id'))})")
                print(f"[AI_CHAT] Available article IDs: {[str(art.get('id')) for art in articles[:5]]}")  # Show first 5

        article = None
        for art in articles:
            # Convert both to string for comparison since article_id comes as string from URL
            if str(art.get("id")) == str(article_id):
                article = art
                break

        if not article:
            return {
                "success": False,
                "error": f"Article not found. Looking for ID: {article_id}. Available IDs: {[str(art.get('id')) for art in articles[:10]]}"
            }

        # Get model settings
        model_settings = load_models_settings(model_name)
        if not model_settings:
            return {
                "success": False,
                "error": f"Model '{model_name}' not found in configuration"
            }

        # Prepare the chat prompt with article context
        chat_prompt = SettingsManager.get_prompt("chat").format(
            article_content=article.get("content", ""),
            article_title=article.get("title", ""),
            article_source=article.get("source", ""),
            user_question=user_question
        )

        # Make API request
        url = model_settings["url"]
        api_key = model_settings["apikey"]
        model_id = model_settings["id"]

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        body = {
            "model": model_id,
            "messages": [
                {
                    "role": "user",
                    "content": chat_prompt
                }
            ],
            "max_tokens": 1000,
            "temperature": 0.7
        }

        if DEBUG_LOGGING:
            print(f"[AI_CHAT] Sending question about article '{article.get('title', 'Unknown')}' to {model_name}")

        response = requests.post(url, headers=headers, json=body)

        if response.status_code == 200:
            ai_response = response.json().get("choices", [])[0].get("message", {}).get("content", "")

            return {
                "success": True,
                "answer": ai_response,
                "article_title": article.get("title", ""),
                "model_used": model_name
            }
        else:
            if DEBUG_LOGGING:
                print(f"[AI_CHAT] Error: {response.status_code} {response.text}")
            return {
                "success": False,
                "error": f"AI service error: {response.status_code}"
            }

    except Exception as e:
        if DEBUG_LOGGING:
            print(f"[AI_CHAT] Exception: {str(e)}")
        return {
            "success": False,
            "error": f"Error processing chat request: {str(e)}"
        }