"""
Integration tests for News Summary Backend API
These tests run against a real server instance
"""

import json
import os
import sys
import time
import pytest
import requests
from typing import Dict, Any

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Configuration
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:5000/api')
TEST_TIMEOUT = 30  # seconds
SKIP_INTEGRATION = os.getenv('SKIP_INTEGRATION_TESTS', 'false').lower() == 'true'

# Global flag to track server availability
_server_available = None


def is_server_available():
    """Check if the server is available for integration tests."""
    global _server_available
    
    if _server_available is not None:
        return _server_available
    
    if SKIP_INTEGRATION:
        _server_available = False
        return False
    
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        _server_available = response.status_code == 200
        return _server_available
    except requests.exceptions.RequestException:
        _server_available = False
        return False


@pytest.fixture(scope="session")
def api_client():
    """API client for integration tests."""
    return APIClient(base_url=API_BASE_URL, timeout=TEST_TIMEOUT)


class APIClient:
    """Simple API client for testing."""

    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()

    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make an HTTP request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        kwargs.setdefault('timeout', self.timeout)
        return self.session.request(method, url, **kwargs)

    def get(self, endpoint: str, **kwargs) -> requests.Response:
        return self._make_request('GET', endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> requests.Response:
        return self._make_request('POST', endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs) -> requests.Response:
        return self._make_request('PUT', endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        return self._make_request('DELETE', endpoint, **kwargs)


@pytest.mark.integration
class TestIntegrationHealth:
    """Integration tests for basic health checks."""

    @pytest.mark.skipif(not is_server_available(), reason="Integration tests skipped - server not available")
    def test_health_endpoint(self, api_client):
        """Test that the health endpoint responds."""
        response = api_client.get('/health')
        assert response.status_code == 200

        data = response.json()
        assert data['status'] == 'healthy'

    @pytest.mark.skipif(not is_server_available(), reason="Integration tests skipped - server not available")
    def test_cache_status_endpoint(self, api_client):
        """Test that the cache status endpoint works."""
        response = api_client.get('/cache/status')
        assert response.status_code == 200

        data = response.json()
        assert 'cache_info' in data


@pytest.mark.integration
class TestIntegrationArticles:
    """Integration tests for article endpoints."""

    @pytest.mark.skipif(not is_server_available(), reason="Integration tests skipped - server not available")
    def test_get_articles(self, api_client):
        """Test getting articles list."""
        response = api_client.get('/articles')
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.skipif(not is_server_available(), reason="Integration tests skipped - server not available")
    def test_get_articles_paginated(self, api_client):
        """Test getting paginated articles."""
        payload = {
            "page": 1,
            "per_page": 5,
            "sort_by": "date"
        }

        response = api_client.post('/articles',
                                 json=payload,
                                 headers={'Content-Type': 'application/json'})
        assert response.status_code == 200

        data = response.json()
        assert 'articles' in data
        assert 'pagination' in data

    @pytest.mark.skipif(not is_server_available(), reason="Integration tests skipped - server not available")
    def test_get_titles_paginated(self, api_client):
        """Test getting paginated titles."""
        payload = {
            "page": 1,
            "per_page": 10,
            "sort_by": "date"
        }

        response = api_client.post('/titles',
                                 json=payload,
                                 headers={'Content-Type': 'application/json'})
        assert response.status_code == 200

        data = response.json()
        assert 'titles' in data
        assert 'pagination' in data

    @pytest.mark.skipif(not is_server_available(), reason="Integration tests skipped - server not available")
    def test_get_length(self, api_client):
        """Test getting articles count."""
        response = api_client.get('/length')
        assert response.status_code == 200

        data = response.json()
        assert 'length' in data
        assert isinstance(data['length'], int)
        assert data['length'] >= 0


@pytest.mark.integration
class TestIntegrationTags:
    """Integration tests for tag endpoints."""

    @pytest.mark.skipif(not is_server_available(), reason="Integration tests skipped - server not available")
    def test_get_tags(self, api_client):
        """Test getting all tags."""
        response = api_client.get('/tags')
        assert response.status_code == 200

        data = response.json()
        assert 'tags' in data
        assert isinstance(data['tags'], list)

    @pytest.mark.skipif(not is_server_available(), reason="Integration tests skipped - server not available")
    def test_get_tags_categories(self, api_client):
        """Test getting tag categories."""
        response = api_client.get('/tags/categories')
        assert response.status_code == 200

        data = response.json()
        assert 'categories' in data
        # Should have at least the basic categories
        assert isinstance(data['categories'], dict)


@pytest.mark.integration
class TestIntegrationFiltering:
    """Integration tests for filtering functionality."""

    @pytest.mark.skipif(not is_server_available(), reason="Integration tests skipped - server not available")
    def test_filter_articles_by_tags(self, api_client):
        """Test filtering articles by tags."""
        response = api_client.get('/articles/filter?tags=tech')
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.skipif(not is_server_available(), reason="Integration tests skipped - server not available")
    def test_filter_articles_by_rating(self, api_client):
        """Test filtering articles by minimum rating."""
        response = api_client.get('/articles/filter?min_rating=3')
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)


@pytest.mark.integration
class TestIntegrationPretreatment:
    """Integration tests for pretreatment functionality."""

    @pytest.mark.skipif(not is_server_available(), reason="Integration tests skipped - server not available")
    def test_get_unpretreat_articles(self, api_client):
        """Test getting unpretreat articles."""
        response = api_client.get('/unpretreat')
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.skipif(not is_server_available(), reason="Integration tests skipped - server not available")
    def test_get_pretreat_articles(self, api_client):
        """Test getting pretreat articles."""
        response = api_client.get('/pretreat')
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)


@pytest.mark.integration
class TestIntegrationSettings:
    """Integration tests for settings."""

    @pytest.mark.skipif(not is_server_available(), reason="Integration tests skipped - server not available")
    def test_get_settings(self, api_client):
        """Test getting application settings."""
        response = api_client.get('/settings')
        assert response.status_code == 200

        data = response.json()
        assert 'settings' in data
        assert isinstance(data['settings'], dict)


@pytest.mark.integration
@pytest.mark.slow
class TestIntegrationCache:
    """Integration tests for cache functionality."""

    @pytest.mark.skipif(not is_server_available(), reason="Integration tests skipped - server not available")
    def test_cache_refresh(self, api_client):
        """Test cache refresh functionality."""
        response = api_client.post('/cache/refresh')
        assert response.status_code == 200

        data = response.json()
        assert 'message' in data


# Helper functions for setup/teardown if needed
def setup_module():
    """Setup before running integration tests."""
    if SKIP_INTEGRATION:
        print("⏭️  Integration tests skipped by configuration")
        return

    print("Setting up integration tests...")
    # Wait for server to be ready
    max_retries = 5  # Reduced from 10
    for i in range(max_retries):
        try:
            response = requests.get(f"{API_BASE_URL}/health", timeout=2)  # Reduced timeout
            if response.status_code == 200:
                print("✅ Server is ready for integration tests")
                return
        except requests.exceptions.RequestException:
            pass

        print(f"⏳ Waiting for server... ({i+1}/{max_retries})")
        time.sleep(1)

    print("⚠️  Server is not ready for integration tests - tests will be skipped")
    # Don't fail here, let individual tests be skipped instead


def teardown_module():
    """Cleanup after integration tests."""
    print("Cleaning up integration tests...")


if __name__ == '__main__':
    # Run integration tests
    pytest.main([__file__, '-v', '-m', 'integration'])