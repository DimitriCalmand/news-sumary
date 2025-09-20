import json

import requests
from config import DEBUG_LOGGING, MODEL_CONFIG_FILE, PROMPT_MESSAGE
from models import ArticleManager


def pretreat_articles() -> None:
    """Pretreat articles that have not been pretreat yet using an AI model"""
    if DEBUG_LOGGING:
        print("[AI] Starting pretreatment of articles")
    articles = ArticleManager.load_articles()
    for article in articles:
        if not article.get("has_been_pretreat", False):
            if DEBUG_LOGGING:
                print(f"[AI] Pretreating article: {article['title']}")
            # Simulate AI processing (e.g., summarization, keyword extraction)
            processed_content, tags = process_article_content(article["content"], "mistral small")
            article["content"] = processed_content
            article["has_been_pretreat"] = True
            article["tags"] = tags
            break
    ArticleManager.save_articles(articles)
    return None
def load_models_settings(model_name: str) -> dict:
    # open the json file and load the settings for the given model_name
    try:
        with open(MODEL_CONFIG_FILE, "r") as f:
            models_settings = json.load(f)
        for model in models_settings["models"]:
            if model["name"] == model_name:
                return model
        return {}
    except Exception as e:
        if DEBUG_LOGGING:
            print(f"[AI] Error loading model settings: {e}")
        return {}
def prepare_tag_to_str() -> str:
    tags = ArticleManager.get_all_tags()
    if not tags:
        return "[No tags available]"
    tag_str = "["
    tag_str += ", ".join(tags)
    tag_str += "]"
    return tag_str
def extract_content_and_tags(answer: str) -> tuple[str, list]:
    """
    if the llm answer is like this:
    article
    TAGS:[tag1, tag2, tag3]
    return the list of tags
    """
    contents =answer.split("TAGS:")
    if len(contents)<2:
        return []
    tags=contents[1].strip()
    tags=tags.replace("[","").replace("]","").replace(".","").strip()
    tags_list = []
    if tags:
        for tag in tags.split(","):
            tags_list.append(tag.strip().lower())
    return contents[0], tags_list

def process_article_content(content: str, model_name) -> str:
    model = load_models_settings(model_name)
    if not model:
        if DEBUG_LOGGING:
            print(f"[AI] No settings found for model: {model_name}. Returning original content.")
        return content  # Return original content if no model settings found
    url = model.get("url")
    api_key = model.get("apikey")
    id = model.get("id")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    body = {
        "model": id,
        # add a admin message to explain the task

        "messages": [
            {"role": "system", "content": PROMPT_MESSAGE.format(tags=prepare_tag_to_str())},
            {"role": "user", "content": f"Pretreat the following article content:\n\n{content}"}
        ]
    }
    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        res = response.json().get("choices", [])[0].get("message", {}).get("content", "")
        res, tags = extract_content_and_tags(res)
        return res, tags
    else:
        if DEBUG_LOGGING:
            print(f"[AI] Error processing article content: {response.status_code} {response.text}")
        return content