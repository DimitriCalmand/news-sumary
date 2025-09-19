import json

import requests
from config import DEBUG_LOGGING
from models import ArticleManager


def pretreat_articles() -> None:
    articles = ArticleManager.load_articles()
    for article in articles:
        if not article.get("has_been_pretreat", False):
            if DEBUG_LOGGING:
                print(f"[AI] Pretreating article: {article['title']}")
            # Simulate AI processing (e.g., summarization, keyword extraction)
            processed_content = process_article_content(article["content"])
            article["content"] = processed_content
            article["has_been_pretreat"] = True
    ArticleManager.save_articles(articles)
    return None
def load_models_settings(model_name: str) -> dict:
    # open the json file and load the settings for the given model_name
    try:
        with open("../data/models.json", "r") as f:
            models_settings = json.load(f)
        for model in models_settings:
            if model["name"] == model_name:
                return model
        return {}
    except Exception as e:
        if DEBUG_LOGGING:
            print(f"[AI] Error loading model settings: {e}")
        return {}
    
def process_article_content(content: str, model_name) -> str:
    model = load_models_settings(model_name)
    if not model:
        if DEBUG_LOGGING:
            print(f"[AI] No settings found for model: {model_name}. Returning original content.")
        return content  # Return original content if no model settings found
    url = model.get("api_url")
    api_key = model.get("api_key")
    id = model.get("id")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    body = {
        "model": id,

        "messages": [
            {
                "role": "user",
                "content": content
            }
        ]
    }
    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        return response.json().get("choices", [])[0].get("message", {}).get("content", "")
    else:
        if DEBUG_LOGGING:
            print(f"[AI] Error processing article content: {response.status_code} {response.text}")
        return content