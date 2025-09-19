"""
Routes module for News Summary Backend
Contains all Flask API routes and endpoints
"""

import time

from cache import article_cache
from config import DEBUG_LOGGING
from flask import Blueprint, jsonify, request
from models import ArticleManager

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
    """Route POST for retrieving only titles with pagination"""
    start_time = time.time()
    
    try:
        # Get pagination parameters from JSON body
        data = request.get_json() or {}
        page = data.get('page', 1)
        per_page = data.get('per_page', 20)
        
        log_request("get_titles_paginated", start_time, page=page, per_page=per_page)
        
        # Validate parameters
        if not isinstance(page, int) or not isinstance(per_page, int):
            return jsonify({"error": "Parameters 'page' and 'per_page' must be integers"}), 400
        
        if page < 1:
            return jsonify({"error": "Parameter 'page' must be greater than 0"}), 400
        
        if per_page < 1:
            return jsonify({"error": "Parameter 'per_page' must be greater than 0"}), 400
        
        # Get paginated titles
        result = article_cache.get_paginated_titles(page, per_page)
        
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