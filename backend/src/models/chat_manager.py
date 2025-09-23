"""
Chat Manager module for News Summary Backend
Contains the ChatManager class for managing AI conversations
"""

import json
import os
from typing import Dict, List

from config import DEBUG_LOGGING


class ChatManager:
    """Manager for chat conversations with AI about articles"""

    CHAT_FILE = "./data/chat_history.json"

    @staticmethod
    def load_conversations() -> Dict:
        """Load all conversations from file"""
        try:
            if os.path.exists(ChatManager.CHAT_FILE):
                with open(ChatManager.CHAT_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            if DEBUG_LOGGING:
                print(f"[CHAT] Error loading conversations: {e}")
            return {}

    @staticmethod
    def save_conversations(conversations: Dict) -> bool:
        """Save all conversations to file"""
        try:
            # Ensure data directory exists
            os.makedirs("./data", exist_ok=True)

            with open(ChatManager.CHAT_FILE, 'w', encoding='utf-8') as f:
                json.dump(conversations, f, ensure_ascii=False, indent=2)

            if DEBUG_LOGGING:
                print(f"[CHAT] Conversations saved successfully")
            return True
        except Exception as e:
            if DEBUG_LOGGING:
                print(f"[CHAT] Error saving conversations: {e}")
            return False

    @staticmethod
    def get_conversation(article_id: str) -> List[Dict]:
        """Get conversation history for a specific article"""
        conversations = ChatManager.load_conversations()
        return conversations.get(article_id, [])

    @staticmethod
    def add_message(article_id: str, message_type: str, content: str, model_used: str = None) -> bool:
        """
        Add a message to the conversation

        Args:
            article_id: ID of the article
            message_type: 'user' or 'ai'
            content: Message content
            model_used: AI model used (for AI messages)
        """
        try:
            conversations = ChatManager.load_conversations()

            if article_id not in conversations:
                conversations[article_id] = []

            message = {
                "id": str(len(conversations[article_id]) + 1),
                "type": message_type,
                "content": content,
                "timestamp": json.dumps({"$date": {"$numberLong": str(int(1000 * __import__('time').time()))}}),
                "model_used": model_used if message_type == 'ai' else None
            }

            conversations[article_id].append(message)

            return ChatManager.save_conversations(conversations)
        except Exception as e:
            if DEBUG_LOGGING:
                print(f"[CHAT] Error adding message: {e}")
            return False

    @staticmethod
    def clear_conversation(article_id: str) -> bool:
        """Clear conversation history for a specific article"""
        try:
            conversations = ChatManager.load_conversations()
            if article_id in conversations:
                conversations[article_id] = []
                return ChatManager.save_conversations(conversations)
            return True
        except Exception as e:
            if DEBUG_LOGGING:
                print(f"[CHAT] Error clearing conversation: {e}")
            return False