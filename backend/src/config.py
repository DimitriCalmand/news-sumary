"""
Configuration module for News Summary Backend
Contains all configuration constants and settings
"""

import os

# File paths
JSON_FILE = "./data/articles_seen.json"

# Cache settings
CACHE_DURATION = 60  # Cache valid for 60 seconds

# TechCrunch scraping settings
TECHCRUNCH_URL = "https://techcrunch.com/category/artificial-intelligence/"
TITLE_CLASS = "loop-card__title"
PARAGRAPH_CLASS = "wp-block-paragraph"

# Scraping intervals
SCRAPING_INTERVAL = 1800  # 30 minutes in seconds

# Flask settings
CORS_ORIGINS = ['http://localhost:5173', 'http://localhost:3000']
DEFAULT_PORT = 3001

# Debug settings
DEBUG_LOGGING = True
FLASK_DEBUG = True  # Active le hot reload en développement

# AI  model settings
MODEL_CONFIG_FILE = "./data/models.json"
PROMPT_MESSAGE = "Tu vas recevoir un article.\n1) Fais un résumé clair et concis au début.\n2) Réécris ensuite l'article en ajoutant des emojis pertinents, en mettant en **gras** certains mots, et en structurant le texte avec des sections et titres si nécessaire, sans modifier le contenu ni l'ordre des idées.\n3) À la fin, ajoute une ligne avec TAGS: [tag1, tag2, ...]. Tu disposes de cette liste de tags déjà utilisés: {tags}. Tu peux en reprendre, en ajouter de nouveaux si nécessaire (sans en abuser).\n4) Ne renvoie rien d'autre que le résumé suivi du nouvel article, puis les tags, sans ajouter de message ou commentaire hors du texte.\n############ Exemple ##############\n# 📢 Notion lance son premier agent IA\nLors de l'événement \"Make with Notion\" ce jeudi, la société a annoncé le lancement de son premier agent IA. Cet agent utilisera toutes les pages et bases de données d'un utilisateur comme contexte pour générer automatiquement des notes et des analyses pour des réunions, des évaluations de concurrents et des pages de feedback.\n## 🛠️ Fonctionnalités de l'agent\n### Création et mise à jour\nL'agent peut créer des pages et des bases de données ou les mettre à jour avec de nouvelles données, propriétés ou vues.\n### Intégration externe\nLes utilisateurs peuvent déclencher des agents Notion depuis des plateformes externes liées au service. Par exemple, vous pouvez demander à l'agent de créer un tableau de bord de suivi des bugs à partir de sources comme Slack, email et Google Drive.\n### Tâches complexes\nContrairement à Notion AI, qui pouvait seulement rechercher ou résumer du contenu, le nouvel agent peut effectuer des tâches complexes en plusieurs étapes, grâce à l'IA agentique. La version actuelle peut accomplir une tâche s'étendant sur 20 minutes et impliquant des centaines de pages.\n## 🤖 Personnalisation de l'agent\nLes utilisateurs peuvent configurer une page de profil pour l'agent afin de lui donner des instructions sur :\n- La référence des sources\n- Le style de sortie\n- L'endroit où mettre à jour les tâches et les résultats finaux\nIl est également possible de demander à l'agent de \"se souvenir\" de points clés. Ces mémoires seront stockées sur la page de profil et pourront être éditées par les utilisateurs.\n## 🎬 Exemples de démonstration\nDans les vidéos de démonstration, la société a montré des exemples d'agents capables de :\n- Fournir des feedbacks et mettre à jour des pages de landing\n- Créer un tracker de restaurants\n- Analyser des notes de réunion\n- Préparer un rapport d'analyse concurrentielle\n## 🔧 Fonctionnalités à venir\nActuellement, ces actions doivent être déclenchées manuellement. Cependant, Notion a annoncé que la possibilité de créer des agents personnalisés fonctionnant sur programmation ou déclencheurs sera bientôt disponible. La société prévoit également de lancer une bibliothèque de modèles pour les agents, permettant aux utilisateurs de choisir des invites prêtes à l'emploi adaptées à leurs tâches.\n## 📅 Évolutions récentes de Notion\nAu cours des deux dernières années, Notion a lancé plusieurs fonctionnalités, notamment :\n- Une application de calendrier\n- Un client Gmail\n- Un preneur de notes de réunion\n- Une recherche d'entreprise pour obtenir des informations de différentes sources\nCes fonctionnalités ont fourni à la société les briques contextuelles nécessaires pour créer des automatisations. D'autres plateformes de connaissance et de productivité d'entreprise, comme Salesforce, Fireflies et Read AI, ont également lancé leurs propres agents pour extraire et mettre à jour des informations.\nTAGS: [Notion, Intelligence Artificielle, Productivité, Agents IA]"

def get_port():
    """Get the port from environment variable or use default"""
    return int(os.getenv("PORT", DEFAULT_PORT))

def get_environment():
    """Get the current environment"""
    return os.getenv("FLASK_ENV", "development")

def is_production():
    """Check if running in production"""
    return get_environment() == "production"

def is_development():
    """Check if running in development"""
    return get_environment() == "development"