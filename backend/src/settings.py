"""
Settings management module for News Summary Backend
Handles loading and saving of configuration settings including prompts and models
"""

import json
import os
from typing import Any, Dict

from config import DEBUG_LOGGING, SETTINGS_CONFIG_FILE


class SettingsManager:
    """Manager class for application settings"""
    
    _settings_cache = None
    
    @classmethod
    def load_settings(cls) -> Dict[str, Any]:
        """Load settings from JSON file"""
        if cls._settings_cache is not None:
            return cls._settings_cache
            
        try:
            if not os.path.exists(SETTINGS_CONFIG_FILE):
                if DEBUG_LOGGING:
                    print(f"[SETTINGS] Settings file not found: {SETTINGS_CONFIG_FILE}")
                return cls._get_default_settings()
                
            with open(SETTINGS_CONFIG_FILE, "r", encoding="utf-8") as f:
                settings = json.load(f)
                cls._settings_cache = settings
                return settings
                
        except Exception as e:
            if DEBUG_LOGGING:
                print(f"[SETTINGS] Error loading settings: {e}")
            return cls._get_default_settings()
    
    @classmethod
    def save_settings(cls, settings: Dict[str, Any]) -> bool:
        """Save settings to JSON file"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(SETTINGS_CONFIG_FILE), exist_ok=True)
            
            with open(SETTINGS_CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
            
            # Update cache
            cls._settings_cache = settings
            
            if DEBUG_LOGGING:
                print(f"[SETTINGS] Settings saved successfully")
            return True
            
        except Exception as e:
            if DEBUG_LOGGING:
                print(f"[SETTINGS] Error saving settings: {e}")
            return False
    
    @classmethod
    def get_prompt(cls, prompt_type: str) -> str:
        """Get prompt by type (article_processing or chat)"""
        settings = cls.load_settings()
        return settings.get("prompts", {}).get(prompt_type, "")
    
    @classmethod
    def get_models(cls) -> list:
        """Get list of available models"""
        settings = cls.load_settings()
        return settings.get("models", [])
    
    @classmethod
    def get_model_by_name(cls, model_name: str) -> Dict[str, Any]:
        """Get model configuration by name"""
        models = cls.get_models()
        for model in models:
            if model.get("name") == model_name:
                return model
        return {}
    
    @classmethod
    def get_default_model(cls) -> str:
        """Get default model name"""
        settings = cls.load_settings()
        return settings.get("default_model", "mistral small")
    
    @classmethod
    def clear_cache(cls):
        """Clear settings cache to force reload"""
        cls._settings_cache = None
    
    @classmethod
    def _get_default_settings(cls) -> Dict[str, Any]:
        """Get default settings if file doesn't exist"""
        return {
            "prompts": {
                "article_processing": "Tu vas recevoir un article. Fais un résumé et réécris-le de manière structurée.",
                "chat": "Tu es un assistant IA spécialisé dans l'analyse d'articles. Réponds aux questions basées sur l'article fourni."
            },
            "models": [
                {
                    "name": "mistral small",
                    "id": "mistral-small-latest",
                    "url": "https://api.mistral.ai/v1/chat/completions",
                    "apikey": "",
                    "llm": "mistral"
                }
            ],
            "default_model": "mistral small"
        }