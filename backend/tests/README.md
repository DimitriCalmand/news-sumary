# News Summary Backend Test Suite

Cette suite de tests couvre tous les endpoints de l'API backend du projet News Summary.

## Structure des tests

```
tests/
├── test_api.py              # Tests principaux des endpoints API
├── requirements-test.txt    # Dépendances pour les tests
├── run_tests.sh            # Script d'exécution des tests
├── pytest.ini             # Configuration pytest
└── README.md              # Ce fichier
```

## Endpoints testés

### Articles
- `GET /api/articles` - Récupération de tous les articles
- `POST /api/articles` - Récupération paginée des articles
- `POST /api/titles` - Récupération paginée des titres
- `GET /api/article/<id>` - Récupération d'un article spécifique
- `GET /api/length` - Nombre total d'articles

### Gestion des articles
- `PUT /api/articles/<id>/rating` - Mise à jour de la note
- `PUT /api/articles/<id>/tags` - Mise à jour des tags
- `PUT /api/articles/<id>/comments` - Mise à jour des commentaires
- `POST /api/articles/<id>/reading-time` - Mise à jour du temps de lecture

### Tags
- `GET /api/tags` - Récupération de tous les tags
- `GET /api/tags/categories` - Récupération des catégories de tags

### Chat IA
- `POST /api/articles/<id>/chat` - Chat avec l'IA
- `GET /api/articles/<id>/chat/history` - Historique du chat
- `DELETE /api/articles/<id>/chat/clear` - Suppression de l'historique

### Utilitaires
- `GET /api/health` - Vérification de santé
- `GET /api/cache/status` - Statut du cache
- `POST /api/cache/refresh` - Rafraîchissement du cache
- `GET /api/unpretreat` - Articles non traités
- `GET /api/pretreat` - Articles traités
- `GET /api/articles/filter` - Filtrage d'articles
- `GET /api/settings` - Paramètres de l'application

## Installation et exécution

### 1. Installation des dépendances de test

```bash
cd backend/tests
pip install -r requirements-test.txt
```

### 2. Exécution des tests

#### Tests rapides (recommandé pour le développement)
```bash
cd backend/tests
./run_tests.sh
```
Ces tests exécutent uniquement les tests unitaires et API (avec mocks), pas besoin de serveur backend.

#### Tests avec couverture de code
```bash
cd backend/tests
./run_tests.sh --coverage
```

#### Tests d'intégration (nécessitent un serveur)
Pour exécuter les tests d'intégration, vous devez d'abord démarrer le serveur backend :

```bash
# Terminal 1: Démarrer le serveur
cd backend
python3 main.py

# Terminal 2: Exécuter les tests d'intégration
cd backend/tests
SKIP_INTEGRATION_TESTS=false ./run_all_tests.sh --integration
```

#### Exécution d'un test spécifique
```bash
python3 -m pytest tests/test_api.py::TestArticlesEndpoints::test_get_articles_success -v
```

#### Exécution des tests d'un endpoint spécifique
```bash
python3 -m pytest tests/test_api.py::TestRatingEndpoints -v
```

#### Ignorer les tests d'intégration
Si vous voulez ignorer complètement les tests d'intégration :
```bash
export SKIP_INTEGRATION_TESTS=true
./run_all_tests.sh
```

## Types de tests

### Tests unitaires
- Tests des fonctions individuelles
- Utilisation de mocks pour isoler les composants
- Vérification des cas d'erreur et des cas normaux

### Tests d'intégration
- Tests des endpoints complets
- Vérification des interactions entre composants
- Tests des cas limites et de la validation des données

## Fonctionnalités testées

### Validation des données
- Types de données corrects
- Valeurs dans les plages autorisées
- Gestion des données manquantes

### Gestion d'erreurs
- Articles non trouvés (404)
- Données invalides (400)
- Erreurs serveur (500)

### Cache
- Invalidation du cache après modifications
- Récupération des données en cache

### Normalisation
- Normalisation automatique des tags
- Validation des ratings (1-5 étoiles)

## Exécution automatique

Les tests peuvent être intégrés dans un pipeline CI/CD :

```yaml
# Exemple pour GitHub Actions
- name: Run Backend Tests
  run: |
    cd backend/tests
    pip install -r requirements-test.txt
    ./run_tests.sh --coverage
```

## Maintenance des tests

### Ajout de nouveaux tests
1. Ajouter les méthodes de test dans la classe appropriée
2. Utiliser des noms descriptifs : `test_<action>_<condition>_<expected_result>`
3. Documenter les cas d'usage dans les docstrings

### Mise à jour après changements d'API
1. Modifier les URLs et paramètres dans les tests
2. Mettre à jour les données de test si nécessaire
3. Vérifier que tous les tests passent

## Métriques de couverture

L'objectif est de maintenir une couverture de code supérieure à 80% pour :
- Les endpoints API
- La logique métier
- La gestion d'erreurs
- La validation des données

## Debugging

### Tests qui échouent
- Vérifier les logs détaillés avec `-v`
- Utiliser `--tb=long` pour les traces complètes
- Vérifier les mocks et leurs retours

### Problèmes d'imports
- S'assurer que le PYTHONPATH inclut le répertoire `src`
- Vérifier que toutes les dépendances sont installées

## Contribution

Lors de l'ajout de nouvelles fonctionnalités :
1. Créer les tests correspondants
2. Vérifier que les tests existants passent
3. Maintenir la couverture de code
4. Documenter les nouveaux cas d'usage