# AI Module

Ce module contient toute la logique d'intelligence artificielle pour le traitement des articles et le chat.

## Structure

- **`__init__.py`** : Interface publique du module
- **`models.py`** : Gestion des modèles et paramètres IA
- **`processing.py`** : Traitement des articles avec l'IA
- **`chat.py`** : Fonctionnalités de chat avec l'IA
- **`tags.py`** : Gestion et préparation des tags
- **`utils.py`** : Utilitaires pour l'extraction de contenu

## Fonctions principales

- `pretreat_articles()` : Prétraitement par lots des articles
- `process_article_content()` : Traitement individuel d'un article
- `chat_with_ai()` : Chat conversationnel sur un article
- `prepare_tag_to_str()` : Préparation des tags pour l'IA
- `load_models_settings()` : Chargement des paramètres de modèle

## Utilisation

```python
from ai import pretreat_articles, chat_with_ai

# Prétraiter tous les articles
pretreat_articles()

# Chatter avec l'IA sur un article
result = chat_with_ai("article_id", "Quelle est la conclusion de cet article?")
```