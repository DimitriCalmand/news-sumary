"""
Settings routes module for News Summary Backend
Contains routes for application settings management
"""

import time

from flask import Blueprint, jsonify, request

from config import DEBUG_LOGGING
from settings import SettingsManager

# Create a Blueprint for settings routes
api_bp = Blueprint('settings', __name__, url_prefix='/api')


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


@api_bp.route('/settings/models/chat', methods=['GET'])
def get_chat_model():
    """Get current chat model"""
    start_time = time.time()
    log_request("get_chat_model", start_time)

    try:
        chat_model = SettingsManager.get_chat_model()
        log_response("get_chat_model", start_time, model=chat_model)
        return jsonify({"chat_model": chat_model}), 200

    except Exception as e:
        log_response("get_chat_model", start_time, "error", error=str(e))
        return jsonify({"error": f"Error retrieving chat model: {str(e)}"}), 500


@api_bp.route('/settings/models/chat', methods=['PUT'])
def set_chat_model():
    """Set chat model"""
    start_time = time.time()

    try:
        data = request.get_json()

        if not data or "model_name" not in data:
            return jsonify({"error": "model_name is required"}), 400

        model_name = data["model_name"]

        # Validate that the model exists
        models = SettingsManager.get_models()
        model_names = [model["name"] for model in models]
        if model_name not in model_names:
            return jsonify({"error": f"Model '{model_name}' not found. Available models: {model_names}"}), 400

        success = SettingsManager.set_chat_model(model_name)

        if success:
            log_response("set_chat_model", start_time, model=model_name)
            return jsonify({
                "success": True,
                "message": f"Chat model set to '{model_name}'"
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": "Failed to save chat model setting"
            }), 500

    except Exception as e:
        log_response("set_chat_model", start_time, "error", error=str(e))
        return jsonify({"error": f"Error setting chat model: {str(e)}"}), 500


@api_bp.route('/settings/models/article-processing', methods=['GET'])
def get_article_processing_model():
    """Get current article processing model"""
    start_time = time.time()
    log_request("get_article_processing_model", start_time)

    try:
        article_processing_model = SettingsManager.get_article_processing_model()
        log_response("get_article_processing_model", start_time, model=article_processing_model)
        return jsonify({"article_processing_model": article_processing_model}), 200

    except Exception as e:
        log_response("get_article_processing_model", start_time, "error", error=str(e))
        return jsonify({"error": f"Error retrieving article processing model: {str(e)}"}), 500


@api_bp.route('/settings/models/article-processing', methods=['PUT'])
def set_article_processing_model():
    """Set article processing model"""
    start_time = time.time()

    try:
        data = request.get_json()

        if not data or "model_name" not in data:
            return jsonify({"error": "model_name is required"}), 400

        model_name = data["model_name"]

        # Validate that the model exists
        models = SettingsManager.get_models()
        model_names = [model["name"] for model in models]
        if model_name not in model_names:
            return jsonify({"error": f"Model '{model_name}' not found. Available models: {model_names}"}), 400

        success = SettingsManager.set_article_processing_model(model_name)

        if success:
            log_response("set_article_processing_model", start_time, model=model_name)
            return jsonify({
                "success": True,
                "message": f"Article processing model set to '{model_name}'"
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": "Failed to save article processing model setting"
            }), 500

    except Exception as e:
        log_response("set_article_processing_model", start_time, "error", error=str(e))
        return jsonify({"error": f"Error setting article processing model: {str(e)}"}), 500