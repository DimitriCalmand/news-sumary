import json

import requests
from config import DEBUG_LOGGING, get_tags_for_source, get_required_tag_for_source
from models import ArticleManager
from settings import SettingsManager



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
            article_source = article.get("source", "")
            processed_content, ai_tags = process_article_content(article["content"], "mistral small", article_source)
            if DEBUG_LOGGING:
                print(f"[AI] Processed content: {processed_content[:60]}...")  # Print first 60 chars
                print(f"[AI] AI suggested tags: {ai_tags}")
            
            # Ajouter automatiquement le tag obligatoire selon la source
            required_tag = get_required_tag_for_source(article_source)
            final_tags = ai_tags.copy() if ai_tags else []
            
            # Ajouter le tag obligatoire s'il n'est pas déjà présent
            if required_tag and required_tag not in final_tags:
                final_tags.append(required_tag)
                if DEBUG_LOGGING:
                    print(f"[AI] Added required tag '{required_tag}' for source '{article_source}'")
            
            # Garder les tags existants de l'article s'il y en a
            existing_tags = article.get("tags", [])
            if existing_tags:
                # Fusionner les tags existants avec les nouveaux, sans doublons
                all_tags = list(set(existing_tags + final_tags))
                final_tags = all_tags
                if DEBUG_LOGGING:
                    print(f"[AI] Merged with existing tags: {existing_tags} -> {final_tags}")
            
            article["content"] = processed_content
            article["has_been_pretreat"] = True
            article["tags"] = final_tags
            ArticleManager.save_articles(articles)
            if DEBUG_LOGGING:
                print(f"[AI] Article '{article['title']}' saved with final tags: {final_tags}")
    return None
def load_models_settings(model_name: str) -> dict:
    """Get model configuration from settings"""
    return SettingsManager.get_model_by_name(model_name)
def prepare_tag_to_str(source: str = None) -> str:
    """Prepare tags string for AI, filtered by source if provided"""
    if source:
        tags = get_tags_for_source(source)
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

def process_article_content(content: str, model_name: str, source: str = None) -> tuple:
    model = load_models_settings(model_name)
    if not model:
        if DEBUG_LOGGING:
            print(f"[AI] No settings found for model: {model_name}. Returning original content.")
        return content, []  # Return original content if no model settings found
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
            {"role": "system", "content": SettingsManager.get_prompt("article_processing").format(tags=prepare_tag_to_str(source))},
            {"role": "user", "content": f"Pretreat the following article content:\n\n{content}"}
        ]
    }
    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        res = response.json().get("choices", [])[0].get("message", {}).get("content", "")
        print(res)
        res, tags = extract_content_and_tags(res)
        return res, tags
    else:
        if DEBUG_LOGGING:
            print(f"[AI] Error processing article content: {response.status_code} {response.text}")
        return content, []


def chat_with_ai(article_id: str, user_question: str, model_name: str = "mistral small") -> dict:
    """
    Chat with AI about a specific article
    
    Args:
        article_id: ID of the article to discuss
        user_question: User's question about the article
        model_name: Name of the AI model to use
    
    Returns:
        dict: Response with success status and AI answer or error
    """
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