"""
Chat routes module for News Summary Backend
Contains routes for AI chat functionality and conversation management
"""

import time

from flask import Blueprint, jsonify, request

from ai import chat_with_ai
from config import DEBUG_LOGGING
from models import ChatManager

# Create a Blueprint for chat routes
api_bp = Blueprint('chat', __name__, url_prefix='/api')


def log_request(endpoint_name: str, start_time: float, **kwargs):
    """Helper function to log request details"""
    if DEBUG_LOGGING:
        print(f"[API] Starting {endpoint_name} at {start_time} with params: {kwargs}")


@api_bp.route('/articles/<article_id>/chat', methods=['POST'])
def chat_about_article(article_id):
    """Chat with AI about a specific article"""
    start_time = time.time()

    try:
        # Get request data
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({"error": "Question is required"}), 400

        user_question = data['question'].strip()
        if not user_question:
            return jsonify({"error": "Question cannot be empty"}), 400

        # Optional model selection (default to mistral small)
        model_name = data.get('model', 'mistral small')

        log_request("chat_about_article", start_time,
                   article_id=article_id,
                   question_length=len(user_question),
                   model=model_name)

        # Call AI chat function
        result = chat_with_ai(article_id, user_question, model_name)

        if result['success']:
            # Save user question to conversation history
            ChatManager.add_message(article_id, 'user', user_question)

            # Save AI response to conversation history
            ChatManager.add_message(article_id, 'ai', result['answer'], result['model_used'])

            log_request("chat_about_article", start_time,
                       article_id=article_id,
                       response_length=len(result['answer']),
                       status="success")

            return jsonify({
                "success": True,
                "answer": result['answer'],
                "article_title": result['article_title'],
                "model_used": result['model_used'],
                "question": user_question
            }), 200
        else:
            log_request("chat_about_article", start_time,
                       article_id=article_id,
                       error=result['error'],
                       status="error")

            return jsonify({
                "success": False,
                "error": result['error']
            }), 400

    except Exception as e:
        log_request("chat_about_article", start_time,
                   article_id=article_id,
                   error=str(e),
                   status="exception")

        return jsonify({"error": f"Error processing chat request: {str(e)}"}), 500


@api_bp.route('/articles/<article_id>/chat/history', methods=['GET'])
def get_chat_history(article_id):
    """Get chat history for a specific article"""
    start_time = time.time()

    try:
        log_request("get_chat_history", start_time, article_id=article_id)

        # Get conversation history
        conversation = ChatManager.get_conversation(article_id)

        # Convert timestamps for frontend compatibility
        for message in conversation:
            if 'timestamp' in message:
                # Simple timestamp format for now
                message['timestamp'] = time.time() * 1000  # JavaScript timestamp

        log_request("get_chat_history", start_time,
                   article_id=article_id,
                   message_count=len(conversation),
                   status="success")

        return jsonify({
            "success": True,
            "conversation": conversation,
            "article_id": article_id
        }), 200

    except Exception as e:
        log_request("get_chat_history", start_time,
                   article_id=article_id,
                   error=str(e),
                   status="exception")

        return jsonify({"error": f"Error retrieving chat history: {str(e)}"}), 500


@api_bp.route('/articles/<article_id>/chat/clear', methods=['DELETE'])
def clear_chat_history(article_id):
    """Clear chat history for a specific article"""
    start_time = time.time()

    try:
        log_request("clear_chat_history", start_time, article_id=article_id)

        # Clear conversation history
        success = ChatManager.clear_conversation(article_id)

        if success:
            log_request("clear_chat_history", start_time,
                       article_id=article_id,
                       status="success")

            return jsonify({
                "success": True,
                "message": "Chat history cleared successfully"
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": "Failed to clear chat history"
            }), 500

    except Exception as e:
        log_request("clear_chat_history", start_time,
                   article_id=article_id,
                   error=str(e),
                   status="exception")

        return jsonify({"error": f"Error clearing chat history: {str(e)}"}), 500