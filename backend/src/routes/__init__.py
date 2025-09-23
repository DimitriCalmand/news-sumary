"""
Routes package for News Summary Backend
Contains all Flask API routes organized by functionality
"""

from .articles import api_bp as articles_bp
from .article_modifications import api_bp as modifications_bp
from .chat import api_bp as chat_bp
from .health import api_bp as health_bp
from .settings import api_bp as settings_bp
from .tags import api_bp as tags_bp


def register_routes(app):
    """Register all API routes with the Flask app"""
    app.register_blueprint(articles_bp)
    app.register_blueprint(modifications_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(tags_bp)

    # Register health check at root level as well
    @app.route('/health', methods=['GET'])
    def root_health_check():
        """Health check endpoint at root level"""
        return {
            "status": "healthy",
            "service": "news-summary-backend"
        }, 200