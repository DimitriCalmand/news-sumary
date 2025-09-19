# 🚀 News Summary Backend

Un backend Flask modulaire pour le scraping et la diffusion d'articles TechCrunch AI.

## 📁 Architecture Modulaire

```
backend/src/
├── __init__.py          # Package initialization
├── main.py             # Point d'entrée principal
├── config.py           # Configuration et constantes
├── models.py           # Modèles de données et gestion des articles
├── cache.py            # Système de cache en mémoire
├── scraper.py          # Fonctionnalités de scraping TechCrunch
└── routes.py           # Routes API Flask
```

## 🧩 Modules

### 📋 `config.py`
- **Rôle** : Configuration centralisée
- **Contenu** : Constantes, URLs, intervalles, paramètres Flask
- **Avantages** : Configuration centralisée, facile à modifier

### 🗃️ `models.py`
- **Rôle** : Gestion des données et articles
- **Classes** : `Article`, `ArticleManager`
- **Fonctions** : CRUD operations, persistence JSON

### ⚡ `cache.py`
- **Rôle** : Cache en mémoire pour les performances
- **Classe** : `ArticleCache`
- **Fonctions** : Cache automatique avec expiration, invalidation

### 🕷️ `scraper.py`
- **Rôle** : Scraping TechCrunch en arrière-plan
- **Classes** : `TechCrunchScraper`, `ScrapingService`
- **Fonctions** : Scraping asynchrone, gestion des erreurs

### 🛤️ `routes.py`
- **Rôle** : Endpoints API REST
- **Routes** : 
  - `GET/POST /api/articles` - Articles avec pagination
  - `POST /api/titles` - Titres paginés
  - `GET /api/article/<id>` - Article individuel
  - `GET /api/unpretreat` - Articles non prétraités
  - `POST /api/article/<id>/pretreat` - Marquer comme prétraité
  - `GET /api/length` - Nombre d'articles
  - `GET /health` - Health check

### 🎯 `main.py`
- **Rôle** : Point d'entrée et orchestration
- **Fonctions** : Initialisation Flask, démarrage des services

## 🚀 Démarrage

```bash
cd backend/src
python main.py
```

## 🧪 Testing des Modules

```python
# Test du cache
from cache import article_cache
articles = article_cache.get_articles()

# Test du scraper
from scraper import TechCrunchScraper
scraper = TechCrunchScraper()
titles, links = scraper.get_titles_and_links()

# Test des models
from models import ArticleManager
articles = ArticleManager.load_articles()
```

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/length` | GET | Nombre total d'articles |
| `/api/articles` | GET | Tous les articles |
| `/api/articles` | POST | Articles paginés |
| `/api/titles` | POST | Titres paginés |
| `/api/article/<id>` | GET | Article individuel |
| `/api/unpretreat` | GET | Articles non prétraités |
| `/api/article/<id>/pretreat` | POST | Marquer prétraité |

## 🔧 Configuration

Toute la configuration se trouve dans `config.py` :

```python
# Modifier l'intervalle de scraping
SCRAPING_INTERVAL = 1800  # 30 minutes

# Modifier la durée du cache
CACHE_DURATION = 60  # 60 secondes

# Modifier l'URL TechCrunch
TECHCRUNCH_URL = "https://techcrunch.com/category/artificial-intelligence/"
```

## ✅ Avantages de cette Architecture

1. **🧩 Modularité** : Chaque fonction dans son module
2. **🔧 Maintenabilité** : Code organisé et facile à modifier
3. **🧪 Testabilité** : Modules indépendants testables
4. **📈 Scalabilité** : Facile d'ajouter de nouvelles fonctionnalités
5. **🔍 Debugging** : Logs structurés par module
6. **📚 Documentation** : Code auto-documenté et type hints

## 🛡️ Gestion d'Erreurs

- **Scraper** : Retry automatique, fallbacks
- **Cache** : Invalidation gracieuse
- **API** : Codes d'erreur HTTP appropriés
- **Models** : Validation des données

Cette architecture modulaire rend votre backend beaucoup plus maintenable et extensible ! 🎯