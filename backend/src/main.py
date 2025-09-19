"""
News Summary Backend - Main Application Entry Point

A Flask-based backend service that scrapes TechCrunch AI articles
and provides a REST API for accessing them.

Features:
- Automatic article scraping from TechCrunch AI category
- In-memory caching for better performance
- RESTful API with pagination support
- Article pretreatment status tracking
- Health monitoring endpoints

Architecture:
- config.py: Configuration constants and settings
- models.py: Data models and article management
- cache.py: In-memory caching system
- scraper.py: TechCrunch scraping functionality
- routes.py: Flask API routes and endpoints
- main.py: Application initialization and startup
"""

from cache import article_cache
# Import our modular components
from config import CORS_ORIGINS, DEBUG_LOGGING, get_port, is_development
from flask import Flask
from flask_cors import CORS
from routes import register_routes
from scraper import start_scraper


def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Configure CORS for frontend communication
    CORS(app, origins=CORS_ORIGINS)
    
    # Register all API routes
    register_routes(app)
    
    if DEBUG_LOGGING:
        print("[MAIN] Flask application created and configured")
        print("[MAIN] 🔥 HOT RELOAD TEST - FILE MODIFIED!")
    
    return app


def initialize_services():
    """Initialize all background services"""
    try:
        # Initialize the article cache
        article_cache.get_articles(force_refresh=True)
        if DEBUG_LOGGING:
            print("[MAIN] Article cache initialized")
        
        # Start the background scraping service
        start_scraper()
        if DEBUG_LOGGING:
            print("[MAIN] Background scraping service started")
            
    except Exception as e:
        if DEBUG_LOGGING:
            print(f"[MAIN] Error initializing services: {e}")
        raise


def main():
    """Main application entry point"""
    try:
        # Create Flask application
        app = create_app()
        
        # Initialize all services
        initialize_services()
        
        # Get configuration
        port = get_port()
        
        if DEBUG_LOGGING:
            print(f"[MAIN] Starting News Summary Backend on port {port}")
            print(f"[MAIN] Health check: http://localhost:{port}/health")
            print(f"[MAIN] API documentation: http://localhost:{port}/api/")
        
        # Start the Flask application
        app.run(
            host='0.0.0.0',
            port=port,
            debug=is_development(),  # Active le hot reload en développement
            use_reloader=is_development(),  # Reload automatique des fichiers
            threaded=True  # Enable multi-threading
        )
        
    except KeyboardInterrupt:
        if DEBUG_LOGGING:
            print("\n[MAIN] Shutting down gracefully...")
    except Exception as e:
        if DEBUG_LOGGING:
            print(f"[MAIN] Fatal error: {e}")
        raise


if __name__ == "__main__":
    main()