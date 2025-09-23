"""
AI Models management module
Handles model configuration and settings loading
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import DEBUG_LOGGING
from settings import SettingsManager


def load_models_settings(model_name: str) -> dict:
    """Get model configuration from settings"""
    return SettingsManager.get_model_by_name(model_name)