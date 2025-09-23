"""
Tags utilities module for News Summary Backend
Contains functions for tag normalization and processing
"""

import re
from typing import List

from config import DEBUG_LOGGING


def normalize_tag(tag: str) -> str:
    """
    Normalise un tag en:
    - convertissant en minuscules
    - supprimant les caractères spéciaux sauf lettres, chiffres, espaces et tirets
    - supprimant les espaces en début/fin
    - remplaçant les espaces multiples par un seul
    """
    if not tag or not isinstance(tag, str):
        return ""

    # Convertir en minuscules
    tag = tag.lower().strip()

    # Garder seulement lettres, chiffres, espaces, tirets et caractères accentués
    tag = re.sub(r'[^\w\s\-àâäçéèêëïîôöùûüÿ]', '', tag)

    # Remplacer plusieurs espaces par un seul
    tag = re.sub(r'\s+', ' ', tag)

    # Supprimer les espaces en début/fin
    tag = tag.strip()

    return tag


def normalize_tags(tags: List[str]) -> List[str]:
    """
    Normalise une liste de tags en:
    - normalisant chaque tag
    - supprimant les doublons
    - supprimant les tags vides
    """
    if not tags:
        return []

    normalized = []
    seen = set()

    for tag in tags:
        normalized_tag = normalize_tag(tag)
        if normalized_tag and normalized_tag not in seen:
            normalized.append(normalized_tag)
            seen.add(normalized_tag)
            if DEBUG_LOGGING and normalized_tag != tag:
                print(f"[MODELS] Tag normalized: '{tag}' -> '{normalized_tag}'")

    return normalized