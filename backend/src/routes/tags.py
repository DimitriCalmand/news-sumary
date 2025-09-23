"""
Tags routes module for News Summary Backend
Contains routes for tag management and categorization
"""

import time

from flask import Blueprint, jsonify

from config import DEBUG_LOGGING, TAG_CATEGORIES, BASIC_TAGS
from models import ArticleManager

# Create a Blueprint for tag routes
api_bp = Blueprint('tags', __name__, url_prefix='/api')


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