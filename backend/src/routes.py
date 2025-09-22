"""
Routes module for News Summary Backend
Contains all Flask API routes and endpoints
"""

import time

from ai import chat_with_ai, pretreat_articles
from cache import article_cache
from config import DEBUG_LOGGING
from flask import Blueprint, jsonify, request
from models import ArticleManager, ChatManager, normalize_tags
from settings import SettingsManager

# Create a Blueprint for API routes
api_bp = Blueprint('api', __name__, url_prefix='/api')


def log_request(endpoint_name: str, start_time: float, **kwargs):
    """Helper function to log request details"""
    if DEBUG_LOGGING:
        print(f"[API] Starting {endpoint_name} at {start_time} with params: {kwargs}")


def log_response(endpoint_name: str, start_time: float, status: str = "success", **kwargs):
    """Helper function to log response details"""
    if DEBUG_LOGGING:
        end_time = time.time()
        duration = end_time - start_time
        print(f"[API] {endpoint_name} completed in {duration:.3f}s - {status} - {kwargs}")


@api_bp.route('/articles', methods=['GET'])
def get_articles():
    """Route GET for retrieving all articles (backward compatibility)"""
    start_time = time.time()
    log_request("get_articles", start_time)
    
    try:
        articles = article_cache.get_articles()
        log_response("get_articles", start_time, count=len(articles))
        return jsonify(articles)
    except Exception as e:
        log_response("get_articles", start_time, "error", error=str(e))
        return jsonify({"error": f"Server error: {str(e)}"}), 500


@api_bp.route('/articles', methods=['POST'])
def get_articles_paginated():
    """Route POST for retrieving articles with pagination"""
    start_time = time.time()
    
    try:
        # Get pagination parameters from JSON body
        data = request.get_json() or {}
        start = data.get('start', 1)
        end = data.get('end', 20)
        
        log_request("get_articles_paginated", start_time, start=start, end=end)
        
        # Validate parameters
        if not isinstance(start, int) or not isinstance(end, int):
            return jsonify({"error": "Parameters 'start' and 'end' must be integers"}), 400
        
        if start < 1:
            return jsonify({"error": "Parameter 'start' must be greater than 0"}), 400
        
        if end < start:
            return jsonify({"error": "Parameter 'end' must be greater than or equal to 'start'"}), 400
        
        # Get paginated articles
        result = article_cache.get_paginated_articles(start, end)
        
        log_response("get_articles_paginated", start_time, 
                    returned=result["pagination"]["returned"],
                    total=result["pagination"]["total"])
        
        return jsonify(result)
        
    except Exception as e:
        log_response("get_articles_paginated", start_time, "error", error=str(e))
        return jsonify({"error": f"Server error: {str(e)}"}), 500


@api_bp.route('/titles', methods=['POST'])
def get_titles_paginated():
    """Route POST for retrieving only titles with pagination and sorting"""
    start_time = time.time()
    
    try:
        # Get pagination parameters from JSON body
        data = request.get_json() or {}
        page = data.get('page', 1)
        per_page = data.get('per_page', 20)
        sort_by = data.get('sort_by', 'date')  # 'date' or 'order'
        
        log_request("get_titles_paginated", start_time, page=page, per_page=per_page, sort_by=sort_by)
        
        # Validate parameters
        if not isinstance(page, int) or not isinstance(per_page, int):
            return jsonify({"error": "Parameters 'page' and 'per_page' must be integers"}), 400
            
        if sort_by not in ['date', 'order']:
            return jsonify({"error": "Parameter 'sort_by' must be 'date' or 'order'"}), 400
        
        if page < 1:
            return jsonify({"error": "Parameter 'page' must be greater than 0"}), 400
        
        if per_page < 1:
            return jsonify({"error": "Parameter 'per_page' must be greater than 0"}), 400
        
        # Get paginated titles
        result = article_cache.get_paginated_titles(page, per_page, sort_by)
        
        log_response("get_titles_paginated", start_time,
                    returned=result["pagination"]["returned"],
                    total=result["pagination"]["total"])
        
        return jsonify(result)
        
    except Exception as e:
        log_response("get_titles_paginated", start_time, "error", error=str(e))
        return jsonify({"error": f"Server error: {str(e)}"}), 500


@api_bp.route('/article/<int:article_id>', methods=['GET'])
def get_single_article(article_id):
    """Route GET for retrieving a single article by ID"""
    start_time = time.time()
    log_request("get_single_article", start_time, article_id=article_id)
    
    try:
        article = article_cache.get_article_by_id(article_id)
        
        if article is None:
            log_response("get_single_article", start_time, "not_found", article_id=article_id)
            return jsonify({"error": "Article not found"}), 404
        
        log_response("get_single_article", start_time, article_id=article_id)
        return jsonify(article)
        
    except Exception as e:
        log_response("get_single_article", start_time, "error", error=str(e))
        return jsonify({"error": f"Server error: {str(e)}"}), 500


@api_bp.route('/unpretreat', methods=['GET'])
def get_unpretreat_articles():
    """Route GET for retrieving articles that haven't been pretreated"""
    start_time = time.time()
    log_request("get_unpretreat_articles", start_time)
    
    try:
        unpretreat_articles = ArticleManager.get_unpretreat_articles()
        
        result = {
            "unpretreat_articles": unpretreat_articles,
            "count": len(unpretreat_articles)
        }
        
        log_response("get_unpretreat_articles", start_time, count=len(unpretreat_articles))
        return jsonify(result)
        
    except Exception as e:
        log_response("get_unpretreat_articles", start_time, "error", error=str(e))
        return jsonify({"error": f"Server error: {str(e)}"}), 500




@api_bp.route('/length', methods=['GET'])
def get_articles_length():
    """Route GET for retrieving the total number of articles"""
    start_time = time.time()
    log_request("get_articles_length", start_time)
    
    try:
        count = article_cache.get_articles_count()
        
        log_response("get_articles_length", start_time, count=count)
        return jsonify(count)
        
    except Exception as e:
        log_response("get_articles_length", start_time, "error", error=str(e))
        return jsonify(0), 500


# Health check route (not under /api prefix)
@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Docker and monitoring"""
    return jsonify({
        "status": "healthy 🔥 HOT RELOAD WORKS!",
        "service": "news-summary-backend",
        "cache_info": article_cache.get_cache_info()
    }), 200


# Cache management routes for debugging
@api_bp.route('/cache/status', methods=['GET'])
def get_cache_status():
    """Get cache status information"""
    if not DEBUG_LOGGING:
        return jsonify({"error": "Debug endpoint not available"}), 404
    
    return jsonify(article_cache.get_cache_info())


@api_bp.route('/cache/refresh', methods=['POST'])
def refresh_cache():
    """Force refresh the cache"""
    if not DEBUG_LOGGING:
        return jsonify({"error": "Debug endpoint not available"}), 404
    
    try:
        articles = article_cache.get_articles(force_refresh=True)
        return jsonify({
            "message": "Cache refreshed successfully",
            "article_count": len(articles)
        })
    except Exception as e:
        return jsonify({"error": f"Error refreshing cache: {str(e)}"}), 500


@api_bp.route('/articles/<int:article_id>/rating', methods=['PUT'])
def update_article_rating(article_id: int):
    """Update article rating (1-5 stars)"""
    start_time = time.time()
    log_request("update_article_rating", start_time, article_id=article_id)
    
    try:
        data = request.get_json()
        if not data or 'rating' not in data:
            return jsonify({"error": "Rating is required"}), 400
        
        rating = data['rating']
        if not isinstance(rating, int) or not 1 <= rating <= 5:
            return jsonify({"error": "Rating must be an integer between 1 and 5"}), 400
        
        success = ArticleManager.update_article_rating(article_id, rating)
        if success:
            # Clear cache to ensure fresh data
            article_cache.invalidate_cache()
            log_response("update_article_rating", start_time, article_id=article_id, rating=rating)
            return jsonify({"message": "Rating updated successfully", "rating": rating})
        else:
            return jsonify({"error": "Article not found"}), 404
    
    except Exception as e:
        log_response("update_article_rating", start_time, status="error", error=str(e))
        return jsonify({"error": f"Error updating rating: {str(e)}"}), 500


@api_bp.route('/articles/<int:article_id>/reading-time', methods=['POST'])
def add_reading_time(article_id: int):
    """Add reading time to article (cumulative)"""
    start_time = time.time()
    log_request("add_reading_time", start_time, article_id=article_id)
    
    try:
        data = request.get_json()
        if not data or 'seconds' not in data:
            return jsonify({"error": "Seconds is required"}), 400
        
        seconds = data['seconds']
        if not isinstance(seconds, int) or seconds < 0:
            return jsonify({"error": "Seconds must be a positive integer"}), 400
        print(seconds)
        success = ArticleManager.add_reading_time(article_id, seconds)
        if success:
            # Clear cache to ensure fresh data
            article_cache.invalidate_cache()
            log_response("add_reading_time", start_time, article_id=article_id, seconds=seconds)
            return jsonify({"message": "Reading time added successfully", "seconds_added": seconds})
        else:
            return jsonify({"error": "Article not found"}), 404
    
    except Exception as e:
        log_response("add_reading_time", start_time, status="error", error=str(e))
        return jsonify({"error": f"Error adding reading time: {str(e)}"}), 500


@api_bp.route('/articles/<int:article_id>/comments', methods=['PUT'])
def update_article_comments(article_id: int):
    """Update article comments"""
    start_time = time.time()
    log_request("update_article_comments", start_time, article_id=article_id)
    
    try:
        data = request.get_json()
        if not data or 'comments' not in data:
            return jsonify({"error": "Comments is required"}), 400
        
        comments = data['comments']
        if not isinstance(comments, str):
            return jsonify({"error": "Comments must be a string"}), 400
        
        success = ArticleManager.update_article_comments(article_id, comments)
        if success:
            # Clear cache to ensure fresh data
            article_cache.invalidate_cache()
            log_response("update_article_comments", start_time, article_id=article_id)
            return jsonify({"message": "Comments updated successfully", "comments": comments})
        else:
            return jsonify({"error": "Article not found"}), 404
    
    except Exception as e:
        log_response("update_article_comments", start_time, status="error", error=str(e))
        return jsonify({"error": f"Error updating comments: {str(e)}"}), 500


@api_bp.route('/articles/<int:article_id>/tags', methods=['PUT'])
def update_article_tags(article_id: int):
    """Update article tags"""
    start_time = time.time()
    log_request("update_article_tags", start_time, article_id=article_id)
    
    try:
        data = request.get_json()
        if not data or 'tags' not in data:
            return jsonify({"error": "Tags is required"}), 400
        
        tags = data['tags']
        if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
            return jsonify({"error": "Tags must be a list of strings"}), 400
        
        # Normalize tags before updating
        normalized_tags = normalize_tags(tags)
        
        success = ArticleManager.update_article_tags(article_id, normalized_tags)
        if success:
            # Clear cache to ensure fresh data
            article_cache.invalidate_cache()
            log_response("update_article_tags", start_time, article_id=article_id, tags=normalized_tags)
            return jsonify({"message": "Tags updated successfully", "tags": normalized_tags})
        else:
            return jsonify({"error": "Article not found"}), 404
    
    except Exception as e:
        log_response("update_article_tags", start_time, status="error", error=str(e))
        return jsonify({"error": f"Error updating tags: {str(e)}"}), 500


@api_bp.route('/tags', methods=['GET'])
def get_all_tags():
    """Get all unique tags from all articles"""
    start_time = time.time()
    log_request("get_all_tags", start_time)
    
    try:
        tags = ArticleManager.get_all_tags()
        log_response("get_all_tags", start_time, tag_count=len(tags))
        return jsonify({"tags": tags})
    
    except Exception as e:
        log_response("get_all_tags", start_time, status="error", error=str(e))
        return jsonify({"error": f"Error getting tags: {str(e)}"}), 500

@api_bp.route('/tags/categories', methods=['GET'])
def get_tag_categories():
    """Get organized tag categories"""
    from config import TAG_CATEGORIES, BASIC_TAGS
    
    start_time = time.time()
    log_request("get_tag_categories", start_time)
    
    try:
        # Get all actual tags from articles
        all_article_tags = ArticleManager.get_all_tags()
        
        # Organize tags by categories
        organized_tags = {
            "categories": {},
            "basic_tags": [],
            "other_tags": []
        }
        
        # Process defined categories
        for category_key, category_data in TAG_CATEGORIES.items():
            main_tag = category_data["main_tag"]
            sub_tags = category_data["sub_tags"]
            
            # Only include tags that actually exist in articles
            available_sub_tags = [tag for tag in sub_tags if tag in all_article_tags]
            
            if main_tag in all_article_tags or available_sub_tags:
                organized_tags["categories"][category_key] = {
                    "main_tag": main_tag,
                    "sub_tags": available_sub_tags,
                    "has_main": main_tag in all_article_tags
                }
        
        # Process basic tags
        organized_tags["basic_tags"] = [tag for tag in BASIC_TAGS if tag in all_article_tags]
        
        # Process other tags (not in categories or basic)
        all_defined_tags = set()
        for category_data in TAG_CATEGORIES.values():
            all_defined_tags.add(category_data["main_tag"])
            all_defined_tags.update(category_data["sub_tags"])
        all_defined_tags.update(BASIC_TAGS)
        
        organized_tags["other_tags"] = [tag for tag in all_article_tags if tag not in all_defined_tags]
        
        log_response("get_tag_categories", start_time)
        return jsonify(organized_tags)
    
    except Exception as e:
        log_response("get_tag_categories", start_time, status="error", error=str(e))
        return jsonify({"error": f"Error getting tag categories: {str(e)}"}), 500

@api_bp.route('/pretreat', methods=['GET'])
def pretreat_articles_route():
    """Pretreat articles for better summarization"""
    try:
        pretreat_articles()
        return jsonify({"message": "Articles pretreatment initiated"}), 200
    except Exception as e:
        return jsonify({"error": f"Error initiating pretreatment: {str(e)}"}), 500

@api_bp.route('/articles/filter', methods=['GET'])
def filter_articles():
    """Filter articles by tags and/or rating"""
    start_time = time.time()
    
    tags = request.args.getlist('tags')  # Permet plusieurs tags: ?tags=tech&tags=ai
    min_rating = request.args.get('min_rating', type=int)
    
    log_request("filter_articles", start_time, tags=tags, min_rating=min_rating)
    
    try:
        articles = ArticleManager.load_articles()
        
        # Filter by tags if provided
        if tags:
            filtered_by_tags = []
            for article in articles:
                article_tags = article.get("tags", [])
                if any(tag in article_tags for tag in tags):
                    filtered_by_tags.append(article)
            articles = filtered_by_tags
        
        # Filter by rating if provided
        if min_rating is not None:
            filtered_by_rating = []
            for article in articles:
                rating = article.get("rating")
                if rating is not None and rating >= min_rating:
                    filtered_by_rating.append(article)
            articles = filtered_by_rating
        
        # Les IDs originaux sont déjà dans les articles, pas besoin de les redéfinir
        
        log_response("filter_articles", start_time, article_count=len(articles))
        return jsonify(articles)
    
    except Exception as e:
        log_response("filter_articles", start_time, status="error", error=str(e))
        return jsonify({"error": f"Error filtering articles: {str(e)}"}), 500


@api_bp.route('/articles/<article_id>/chat', methods=['POST'])
def chat_about_article(article_id):
    """Chat with AI about a specific article"""
    start_time = time.time()
    
    try:
        # Get request data
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({"error": "Question is required"}), 400
        
        user_question = data['question'].strip()
        if not user_question:
            return jsonify({"error": "Question cannot be empty"}), 400
        
        # Optional model selection (default to mistral small)
        model_name = data.get('model', 'mistral small')
        
        log_request("chat_about_article", start_time, 
                   article_id=article_id, 
                   question_length=len(user_question),
                   model=model_name)
        
        # Call AI chat function
        result = chat_with_ai(article_id, user_question, model_name)
        
        if result['success']:
            # Save user question to conversation history
            ChatManager.add_message(article_id, 'user', user_question)
            
            # Save AI response to conversation history
            ChatManager.add_message(article_id, 'ai', result['answer'], result['model_used'])
            
            log_request("chat_about_article", start_time, 
                       article_id=article_id, 
                       response_length=len(result['answer']),
                       status="success")
            
            return jsonify({
                "success": True,
                "answer": result['answer'],
                "article_title": result['article_title'],
                "model_used": result['model_used'],
                "question": user_question
            }), 200
        else:
            log_request("chat_about_article", start_time, 
                       article_id=article_id, 
                       error=result['error'],
                       status="error")
            
            return jsonify({
                "success": False,
                "error": result['error']
            }), 400
            
    except Exception as e:
        log_request("chat_about_article", start_time, 
                   article_id=article_id, 
                   error=str(e),
                   status="exception")
        
        return jsonify({"error": f"Error processing chat request: {str(e)}"}), 500


@api_bp.route('/articles/<article_id>/chat/history', methods=['GET'])
def get_chat_history(article_id):
    """Get chat history for a specific article"""
    start_time = time.time()
    
    try:
        log_request("get_chat_history", start_time, article_id=article_id)
        
        # Get conversation history
        conversation = ChatManager.get_conversation(article_id)
        
        # Convert timestamps for frontend compatibility
        for message in conversation:
            if 'timestamp' in message:
                # Simple timestamp format for now
                message['timestamp'] = time.time() * 1000  # JavaScript timestamp
        
        log_request("get_chat_history", start_time, 
                   article_id=article_id, 
                   message_count=len(conversation),
                   status="success")
        
        return jsonify({
            "success": True,
            "conversation": conversation,
            "article_id": article_id
        }), 200
        
    except Exception as e:
        log_request("get_chat_history", start_time, 
                   article_id=article_id, 
                   error=str(e),
                   status="exception")
        
        return jsonify({"error": f"Error retrieving chat history: {str(e)}"}), 500


@api_bp.route('/articles/<article_id>/chat/clear', methods=['DELETE'])
def clear_chat_history(article_id):
    """Clear chat history for a specific article"""
    start_time = time.time()
    
    try:
        log_request("clear_chat_history", start_time, article_id=article_id)
        
        # Clear conversation history
        success = ChatManager.clear_conversation(article_id)
        
        if success:
            log_request("clear_chat_history", start_time, 
                       article_id=article_id, 
                       status="success")
            
            return jsonify({
                "success": True,
                "message": "Chat history cleared successfully"
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": "Failed to clear chat history"
            }), 500
        
    except Exception as e:
        log_request("clear_chat_history", start_time, 
                   article_id=article_id, 
                   error=str(e),
                   status="exception")
        
        return jsonify({"error": f"Error clearing chat history: {str(e)}"}), 500


@api_bp.route('/settings', methods=['GET'])
def get_settings():
    """Get current application settings"""
    start_time = time.time()
    log_request("get_settings", start_time)
    
    try:
        settings = SettingsManager.load_settings()
        log_response("get_settings", start_time)
        return jsonify(settings), 200
        
    except Exception as e:
        log_response("get_settings", start_time, "error", error=str(e))
        return jsonify({"error": f"Error retrieving settings: {str(e)}"}), 500


@api_bp.route('/settings', methods=['PUT'])
def update_settings():
    """Update application settings"""
    start_time = time.time()
    log_request("update_settings", start_time)
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Validate the structure (basic validation)
        if "prompts" not in data or "models" not in data:
            return jsonify({"error": "Invalid settings structure. Must contain 'prompts' and 'models'"}), 400
        
        # Save settings
        success = SettingsManager.save_settings(data)
        
        if success:
            log_response("update_settings", start_time)
            return jsonify({
                "success": True,
                "message": "Settings updated successfully"
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": "Failed to save settings"
            }), 500
        
    except Exception as e:
        log_response("update_settings", start_time, "error", error=str(e))
        return jsonify({"error": f"Error updating settings: {str(e)}"}), 500


@api_bp.route('/settings/models', methods=['GET'])
def get_models():
    """Get available models"""
    start_time = time.time()
    log_request("get_models", start_time)
    
    try:
        models = SettingsManager.get_models()
        default_model = SettingsManager.get_default_model()
        
        log_response("get_models", start_time, count=len(models))
        return jsonify({
            "models": models,
            "default_model": default_model
        }), 200
        
    except Exception as e:
        log_response("get_models", start_time, "error", error=str(e))
        return jsonify({"error": f"Error retrieving models: {str(e)}"}), 500


@api_bp.route('/settings/prompts', methods=['GET'])
def get_prompts():
    """Get available prompts"""
    start_time = time.time()
    log_request("get_prompts", start_time)
    
    try:
        settings = SettingsManager.load_settings()
        prompts = settings.get("prompts", {})
        
        log_response("get_prompts", start_time, count=len(prompts))
        return jsonify(prompts), 200
        
    except Exception as e:
        log_response("get_prompts", start_time, "error", error=str(e))
        return jsonify({"error": f"Error retrieving prompts: {str(e)}"}), 500


def register_routes(app):
    """Register all API routes with the Flask app"""
    app.register_blueprint(api_bp)
    
    # Register health check at root level as well
    @app.route('/health', methods=['GET'])
    def root_health_check():
        """Health check endpoint at root level"""
        return jsonify({
            "status": "healthy",
            "service": "news-summary-backend"
        }), 200