"""
Articles routes module for News Summary Backend
Contains routes for retrieving articles
"""

import time

from flask import Blueprint, jsonify, request

from ai import pretreat_articles
from cache import article_cache
from config import DEBUG_LOGGING

# Create a Blueprint for article routes
api_bp = Blueprint('articles', __name__, url_prefix='/api')


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
        search = data.get('search')  # Optional search term

        log_request("get_titles_paginated", start_time, page=page, per_page=per_page, sort_by=sort_by, search=search)

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
        result = article_cache.get_paginated_titles(page, per_page, sort_by, search)

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
        from models import ArticleManager
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
        from models import ArticleManager
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