"""
Unit tests for News Summary Backend models
"""

import json
import os
import sys
import tempfile
import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import List, Dict, Any

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models import (
    ArticleManager,
    ChatManager,
    Article,
    normalize_tag,
    normalize_tags
)
from settings import SettingsManager


@pytest.fixture
def temp_data_dir():
    """Create a temporary directory for test data."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test data files
        articles_file = os.path.join(temp_dir, 'articles_seen.json')
        chat_file = os.path.join(temp_dir, 'chat_history.json')
        settings_file = os.path.join(temp_dir, 'settings.json')

        # Create sample data
        sample_articles = [
            {
                "id": 0,
                "title": "Test Article 1",
                "url": "https://example.com/1",
                "content": "Content 1",
                "has_been_pretreat": True,
                "rating": 5,
                "time_spent": 300,
                "comments": "Great article!",
                "tags": ["tech", "ai"],
                "source": "TechCrunch",
                "scraped_date": "2025-01-01T10:00:00Z",
                "date": "2025-01-01"
            },
            {
                "id": 1,
                "title": "Test Article 2",
                "url": "https://example.com/2",
                "content": "Content 2",
                "has_been_pretreat": False,
                "rating": None,
                "time_spent": 0,
                "comments": "",
                "tags": ["politics"],
                "source": "France Info",
                "scraped_date": "2025-01-02T10:00:00Z",
                "date": "2025-01-02"
            }
        ]

        sample_chat = {
            "0": [
                {
                    "message": "What is this about?",
                    "response": "This article discusses AI technology.",
                    "timestamp": "2025-01-01T10:30:00Z"
                }
            ]
        }

        sample_settings = {
            "theme": "dark",
            "language": "fr",
            "notifications": True
        }

        # Write test data
        with open(articles_file, 'w', encoding='utf-8') as f:
            json.dump(sample_articles, f, ensure_ascii=False, indent=2)

        with open(chat_file, 'w', encoding='utf-8') as f:
            json.dump(sample_chat, f, ensure_ascii=False, indent=2)

        with open(settings_file, 'w', encoding='utf-8') as f:
            json.dump(sample_settings, f, ensure_ascii=False, indent=2)

        yield temp_dir


class TestNormalizeTag:
    """Test cases for tag normalization functions."""

    def test_normalize_tag_basic(self):
        """Test basic tag normalization."""
        assert normalize_tag("TECHNOLOGIE") == "technologie"
        assert normalize_tag("   économie   ") == "économie"
        assert normalize_tag("Intelligence Artificielle") == "intelligence artificielle"

    def test_normalize_tag_special_chars(self):
        """Test normalization with special characters."""
        assert normalize_tag("tech@nologie") == "technologie"
        assert normalize_tag("finance & économie") == "finance économie"
        assert normalize_tag("santé-publique") == "santé-publique"
        assert normalize_tag("POLITIQUE!!!") == "politique"

    def test_normalize_tag_length_limit(self):
        """Test that tags are limited to 30 characters."""
        # Tag exactement 30 caractères
        long_tag = "a" * 30
        assert normalize_tag(long_tag) == long_tag
        assert len(normalize_tag(long_tag)) == 30
        
        # Tag plus long que 30 caractères
        too_long_tag = "a" * 35
        assert normalize_tag(too_long_tag) == "a" * 30
        assert len(normalize_tag(too_long_tag)) == 30
        
        # Tag avec espaces à la fin après troncature
        tag_with_spaces = "a" * 25 + "     "
        assert normalize_tag(tag_with_spaces) == "a" * 25

    def test_normalize_tags_list(self):
        """Test normalization of tag lists."""
        input_tags = ["TECHNOLOGIE", "  économie  ", "tech@nologie", "", "ai"]
        expected = ["technologie", "économie", "ai"]  # Duplicates and empty tags are removed
        assert normalize_tags(input_tags) == expected

    def test_normalize_tags_duplicates(self):
        """Test that duplicates are removed during normalization."""
        input_tags = ["tech", "TECH", "Tech", "ai", "AI"]
        expected = ["tech", "ai"]
        result = normalize_tags(input_tags)
        assert set(result) == set(expected)  # Order doesn't matter for uniqueness


class TestArticle:
    """Test cases for Article class."""

    def test_article_creation(self):
        """Test Article object creation."""
        article = Article(
            title="Test Title",
            url="https://example.com",
            content="Test content",
            has_been_pretreat=True,
            rating=4,
            time_spent=200,
            comments="Good article",
            tags=["test", "sample"],
            source="Test Source"
        )

        assert article.title == "Test Title"
        assert article.url == "https://example.com"
        assert article.rating == 4
        assert article.tags == ["test", "sample"]

    def test_article_to_dict(self):
        """Test Article to_dict method."""
        article = Article(
            title="Test Title",
            url="https://example.com",
            content="Test content"
        )

        article_dict = article.to_dict()
        assert article_dict['title'] == "Test Title"
        assert article_dict['url'] == "https://example.com"
        assert article_dict['content'] == "Test content"
        assert 'id' not in article_dict  # id is not part of the Article object

    def test_article_from_dict(self):
        """Test Article from_dict method."""
        data = {
            "id": 1,
            "title": "Test Title",
            "url": "https://example.com",
            "content": "Test content",
            "has_been_pretreat": True,
            "rating": 4,
            "time_spent": 200,
            "comments": "Good article",
            "tags": ["test", "sample"],
            "source": "Test Source",
            "scraped_date": "2025-01-01T10:00:00Z",
            "date": "2025-01-01"
        }

        article = Article.from_dict(data)
        assert article.title == "Test Title"
        assert article.rating == 4
        assert article.tags == ["test", "sample"]
        assert hasattr(article, 'id') == False  # Article doesn't have id attribute


class TestArticleManager:
    """Test cases for ArticleManager class."""

    @patch('models.article_storage.ArticleStorage.save_articles')
    @patch('models.article_storage.ArticleStorage.load_articles')
    def test_update_article_tags_success(self, mock_load, mock_save):
        """Test successful tag update."""
        mock_load.return_value = [
            {"id": 0, "title": "Test", "tags": ["old"]},
            {"id": 1, "title": "Test2", "tags": ["existing"]}
        ]

        result = ArticleManager.update_article_tags(0, ["new", "tags"])
        assert result is True

        # Check that save was called with normalized tags
        mock_save.assert_called_once()
        saved_articles = mock_save.call_args[0][0]
        assert saved_articles[0]["tags"] == ["new", "tags"]

    @patch('models.ArticleManager.load_articles')
    def test_update_article_tags_not_found(self, mock_load):
        """Test tag update for non-existent article."""
        mock_load.return_value = [{"id": 0, "title": "Test"}]

        result = ArticleManager.update_article_tags(999, ["tags"])
        assert result is False

    @patch('models.ArticleManager.load_articles')
    @patch('models.ArticleManager.save_articles')
    def test_update_article_rating_success(self, mock_save, mock_load):
        """Test successful rating update."""
        mock_load.return_value = [{"id": 0, "rating": None}]

        result = ArticleManager.update_article_rating(0, 4)
        assert result is True

    def test_update_article_rating_invalid(self):
        """Test rating update with invalid values."""
        # Test rating too low
        result = ArticleManager.update_article_rating(0, 0)
        assert result is False

        # Test rating too high
        result = ArticleManager.update_article_rating(0, 6)
        assert result is False

    @patch('models.article_storage.ArticleStorage.load_articles')
    def test_get_all_tags(self, mock_load):
        """Test getting all unique tags."""
        mock_load.return_value = [
            {"tags": ["tech", "ai"]},
            {"tags": ["politics", "tech"]},
            {"tags": []}
        ]

        tags = ArticleManager.get_all_tags()
        expected_tags = ["tech", "ai", "politics"]
        assert set(tags) == set(expected_tags)

    @patch('models.article_storage.ArticleStorage.load_articles')
    def test_filter_by_rating(self, mock_load):
        """Test filtering articles by minimum rating."""
        mock_load.return_value = [
            {"id": 0, "rating": 5, "title": "Good"},
            {"id": 1, "rating": 3, "title": "Average"},
            {"id": 2, "rating": None, "title": "Unrated"}
        ]

        result = ArticleManager.filter_by_rating(4)
        assert len(result) == 1
        assert result[0]["title"] == "Good"

    @patch('models.article_storage.ArticleStorage.load_articles')
    def test_get_unpretreat_articles(self, mock_load):
        """Test getting unpretreat articles."""
        mock_load.return_value = [
            {"title": "Article 1", "url": "url1", "has_been_pretreat": True},
            {"title": "Article 2", "url": "url2", "has_been_pretreat": False},
            {"title": "Article 3", "url": "url3", "has_been_pretreat": False}
        ]

        result = ArticleManager.get_unpretreat_articles()
        assert len(result) == 2
        # The method returns dicts with id, title, url (not the full articles)
        assert result[0]["title"] == "Article 2"
        assert result[0]["url"] == "url2"
        assert result[0]["id"] == 1  # index in the array
        assert result[1]["title"] == "Article 3"
        assert result[1]["url"] == "url3"
        assert result[1]["id"] == 2


class TestChatManager:
    """Test cases for ChatManager class."""

    @patch('models.ChatManager.load_conversations')
    def test_get_chat_history_success(self, mock_load):
        """Test getting chat history."""
        mock_load.return_value = {
            "1": [
                {"id": "1", "type": "user", "content": "Hello", "timestamp": "2025-01-01T10:00:00Z"}
            ]
        }

        history = ChatManager.get_conversation("1")
        assert len(history) == 1
        assert history[0]["content"] == "Hello"

    @patch('models.ChatManager.save_conversations')
    @patch('models.ChatManager.load_conversations')
    def test_add_chat_message(self, mock_load, mock_save):
        """Test adding a chat message."""
        mock_load.return_value = {}
        mock_save.return_value = True

        result = ChatManager.add_message("1", "user", "Test message")
        assert result is True

        # Check that save was called
        mock_save.assert_called_once()

    @patch('models.ChatManager.save_conversations')
    @patch('models.ChatManager.load_conversations')
    def test_clear_chat_history_success(self, mock_load, mock_save):
        """Test clearing chat history."""
        mock_load.return_value = {"1": [{"content": "test"}]}
        mock_save.return_value = True

        result = ChatManager.clear_conversation("1")
        assert result is True

        # Check that save was called
        mock_save.assert_called_once()


class TestSettingsManager:
    """Test cases for SettingsManager class."""

    @patch('settings.SettingsManager.load_settings')
    def test_get_settings(self, mock_load):
        """Test getting settings."""
        mock_load.return_value = {"theme": "dark", "language": "fr"}

        settings = SettingsManager.load_settings()
        assert settings["theme"] == "dark"
        assert settings["language"] == "fr"

    @patch('settings.SettingsManager.save_settings')
    @patch('settings.SettingsManager.load_settings')
    def test_update_settings(self, mock_load, mock_save):
        """Test updating settings."""
        mock_load.return_value = {"theme": "light"}
        mock_save.return_value = True

        result = SettingsManager.save_settings({"theme": "dark", "language": "en"})
        assert result is True

        # Check that save was called with updated settings
        mock_save.assert_called_once()
        saved_settings = mock_save.call_args[0][0]
        assert saved_settings["theme"] == "dark"
        assert saved_settings["language"] == "en"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])