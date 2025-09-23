"""
Article modifications routes module for News Summary Backend
Contains routes for updating article properties (rating, comments, tags, reading time)
"""

import time

from flask import Blueprint, jsonify, request

from cache import article_cache
from config import DEBUG_LOGGING
from models import ArticleManager, normalize_tags

# Create a Blueprint for article modification routes
api_bp = Blueprint('article_modifications', __name__, url_prefix='/api')


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