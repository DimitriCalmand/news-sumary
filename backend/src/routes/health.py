"""
Health and system routes module for News Summary Backend
Contains health checks and cache management routes
"""

from flask import Blueprint, jsonify

from cache import article_cache
from config import DEBUG_LOGGING

# Create a Blueprint for health and system routes
api_bp = Blueprint('health', __name__, url_prefix='/api')


@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Docker and monitoring"""
    return jsonify({
        "status": "healthy 🔥 HOT RELOAD WORKS!",
        "service": "news-summary-backend",
        "cache_info": article_cache.get_cache_info()
    }), 200


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