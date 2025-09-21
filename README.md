# 📰 News Summary - Gestionnaire d'Articles Intelligent avec IA

<div align="center">

![Node.js](https://img.shields.io/badge/Node.js-43853D?style=for-the-badge&logo=node.js&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![AI](https://img.shields.io/badge/AI_Powered-FF6B6B?style=for-the-badge&logo=openai&logoColor=white)

**Une application moderne de gestion et résumé d'articles avec IA personnalisable, interface React et API Flask**

[🚀 Fonctionnalités](#-fonctionnalités) • 
[🤖 IA Intégrée](#-ia-intégrée) • 
[📋 Installation](#-installation) • 
[🛠️ Technologies](#️-technologies) • 
[🔧 Configuration](#-configuration-ia) • 
[📚 Documentation](#-documentation-api)

</div>

---

## 📖 Description

News Summary est une application web complète alimentée par l'IA permettant de gérer, organiser, résumer et discuter d'articles de presse. Elle offre une interface utilisateur moderne avec des fonctionnalités avancées de traitement par IA, chat interactif, système de configuration personnalisable, notation, commentaires, tags, et suivi du temps de lecture.

## 🌟 Fonctionnalités

### 🤖 **Intelligence Artificielle Intégrée**
- ✅ **Traitement automatique d'articles** avec résumés et reformatage IA
- ✅ **Chat intelligent** pour poser des questions sur les articles
- ✅ **Configuration IA personnalisable** via interface graphique
- ✅ **Support multi-modèles** (Mistral, DeepSeek, etc.)
- ✅ **Prompts personnalisables** pour le traitement et le chat
- ✅ **Tags automatiques** générés par l'IA

### ⚙️ **Système de Configuration Avancé**
- ✅ **Interface de paramètres** avec icône d'engrenage
- ✅ **Gestion des modèles IA** (ajout, suppression, modification)
- ✅ **Édition des prompts** en temps réel
- ✅ **Sélection du modèle par défaut** via liste déroulante
- ✅ **Sauvegarde persistante** des configurations
- ✅ **Validation automatique** des paramètres

### 📰 **Gestion d'Articles Intelligente**
- ✅ **Lecture d'articles** avec traitement IA intégré
- ✅ **Pagination intelligente** côté serveur et client
- ✅ **Recherche et filtrage** par tags et notes
- ✅ **Résumés automatiques** générés par IA
- ✅ **Support Markdown** avec highlighting de code
- ✅ **Chat contextuel** sur chaque article

### 💬 **Chat IA Contextuel**
- ✅ **Questions personnalisées** sur chaque article
- ✅ **Réponses contextualisées** basées sur le contenu
- ✅ **Historique des conversations** par article
- ✅ **Interface chat moderne** avec bulles de conversation
- ✅ **Analyse approfondie** des articles via IA

### ⭐ **Système d'Évaluation & Organisation**
- ✅ **Notation 5 étoiles** interactive
- ✅ **Feedback visuel instantané** lors du clic
- ✅ **Tags personnalisés** pour catégoriser les articles
- ✅ **Autocomplétion** basée sur les tags existants
- ✅ **Filtrage avancé** par tags et notes

### 💬 **Commentaires & Temps de Lecture**
- ✅ **Zone de commentaires** pliable/dépliable
- ✅ **Édition en temps réel** avec sauvegarde automatique
- ✅ **Timer automatique** se déclenchant à l'ouverture
- ✅ **Pause intelligente** quand la page devient inactive
- ✅ **Cumul du temps** sur plusieurs sessions

---

## 🤖 IA Intégrée

### **Modèles Supportés**
- **Mistral AI** (Small, Magistral, Ministral 3B)
- **DeepSeek V3** (Chat)
- **Support extensible** pour nouveaux modèles

### **Fonctionnalités IA**

#### **Traitement Automatique d'Articles**
```
🔄 Article brut → IA → 📝 Article formaté avec :
• Résumé clair et concis
• Formatage avec emojis et mise en forme
• Structure améliorée (titres, sections)
• Tags automatiques pertinents
• Préservation du contenu original
```

#### **Chat Intelligent**
```
💬 Questions sur l'article → IA → 🎯 Réponses contextualisées
• Analyse basée uniquement sur l'article
• Réponses précises et pertinentes
• Ton professionnel mais accessible
• Indication si l'information n'est pas disponible
```

### **Interface de Configuration**
- **Accès rapide** : Bouton engrenage dans l'en-tête
- **Gestion des modèles** : Ajout, suppression, modification des APIs
- **Édition des prompts** : Zones de texte pour personnaliser les instructions IA
- **Sélection du modèle** : Liste déroulante pour choisir le modèle par défaut
- **Sauvegarde instantanée** : Configuration persistante en JSON

---

## 🛠️ Technologies

### **Frontend Moderne**
- **React 19.1.1** - Framework UI dernière génération
- **TypeScript 5.8.3** - Typage statique complet
- **Vite 7.1.6** - Build tool ultra-rapide
- **TanStack Query** - Gestion d'état et cache intelligent
- **React Router 7.9.1** - Navigation SPA
- **Tailwind CSS 3.4.17** - Framework CSS utilitaire
- **React Markdown 10.1.0** - Rendu Markdown
- **Lucide React** - Icônes modernes

### **Backend IA-Ready**
- **Python 3.11+** - Langage serveur
- **Flask 3.1.0** - Framework web léger
- **Flask-CORS 5.0.0** - Gestion CORS
- **Requests 2.32.3** - Client HTTP pour APIs IA
- **BeautifulSoup4 4.12.3** - Parsing HTML
- **Système de configuration JSON** - Gestion des modèles IA

### **Infrastructure DevOps**
- **Docker & Docker Compose** - Containerisation
- **GitHub Actions** - CI/CD automatisé
- **Nginx** - Serveur web de production
- **Multi-architecture** - Support AMD64/ARM64

---

## 🏗️ Architecture

```
news-summary/
├── 🎨 frontend/                 # Application React TypeScript
│   ├── src/
│   │   ├── components/          # Composants React réutilisables
│   │   │   ├── ArticleDetail.tsx     # Page détail avec chat IA
│   │   │   ├── ArticleList.tsx       # Liste avec bouton paramètres
│   │   │   ├── SettingsModal.tsx     # Interface configuration IA
│   │   │   ├── ArticleChat.tsx       # Chat IA contextuel
│   │   │   ├── StarRating.tsx        # Système de notation
│   │   │   ├── TagsEditor.tsx        # Gestionnaire de tags
│   │   │   ├── CommentsEditor.tsx    # Zone de commentaires
│   │   │   ├── AutoReadingTimer.tsx  # Timer intelligent
│   │   │   ├── ArticleFilters.tsx    # Interface de filtrage
│   │   │   └── PaginationControls.tsx # Contrôles pagination
│   │   ├── lib/
│   │   │   └── api.ts           # Client API TypeScript avec endpoints IA
│   │   ├── types/
│   │   │   └── index.ts         # Types TypeScript (Settings, Models, etc.)
│   │   └── utils/
│   │       └── api.ts           # Utilitaires API existants
│   ├── 🐳 Dockerfile            # Build multi-architecture
│   └── 📦 package.json          # Dépendances Node.js
│
├── 🐍 backend/                  # API Flask avec IA
│   ├── src/
│   │   ├── settings.py          # 🆕 Gestionnaire de configuration IA
│   │   ├── ai.py                # 🔄 Traitement IA et chat contextuel
│   │   ├── models.py            # Modèles de données et ArticleManager
│   │   ├── routes.py            # 🔄 Endpoints API REST + paramètres IA
│   │   ├── cache.py             # Système de cache intelligent
│   │   └── config.py            # 🔄 Configuration simplifiée
│   ├── data/
│   │   ├── settings.json        # 🆕 Configuration IA personnalisable
│   │   ├── models.json          # Configuration modèles (legacy)
│   │   ├── articles_seen.json   # Base de données articles
│   │   └── chat_history.json    # Historique des conversations IA
│   ├── 🐳 Dockerfile            # Build optimisé Python
│   └── 📋 requirements.txt      # Dépendances Python
│
├── 🚀 .github/workflows/        # CI/CD GitHub Actions
│   └── docker-build.yml        # Build/Deploy automatique ARM64
│
├── 🐳 Docker Compose Files      # Orchestration des services
│   ├── docker-compose.yml           # Développement local
│   ├── docker-compose.prod.yml      # Production générique
│   └── docker-compose.arm64.yml     # Raspberry Pi ARM64
│
└── 🛠️ Scripts de Déploiement    # Automatisation DevOps
    ├── deploy.sh                # Script principal multi-plateforme
    ├── full-deploy.sh           # Déploiement complet automatisé
    └── setup-ssh.sh             # Configuration SSH sans mot de passe
```

---

## 🔧 Configuration IA

### **Accès aux Paramètres**
1. **Cliquer sur l'icône engrenage** dans l'en-tête de l'application
2. **Configurer les modèles IA** (nom, API, clés)
3. **Personnaliser les prompts** (traitement d'articles et chat)
4. **Sélectionner le modèle par défaut**
5. **Sauvegarder** les modifications

### **Configuration des Modèles**
```json
{
  "models": [
    {
      "name": "mistral small",
      "id": "mistral-small-latest", 
      "url": "https://api.mistral.ai/v1/chat/completions",
      "apikey": "votre-clé-api",
      "llm": "mistral"
    }
  ],
  "default_model": "mistral small"
}
```

### **Personnalisation des Prompts**

#### **Prompt de Traitement d'Articles**
- **Usage** : Résumé et reformatage automatique des articles
- **Variables** : `{tags}` pour les tags existants
- **Sortie** : Article formaté + tags automatiques

#### **Prompt de Chat**
- **Usage** : Réponses aux questions sur les articles
- **Variables** : `{article_content}`, `{article_title}`, `{article_source}`, `{user_question}`
- **Comportement** : Analyse contextuelle uniquement

---

## 📋 Installation

### 🚀 **Déploiement Rapide (Recommandé)**

```bash
# 1. Cloner le repository
git clone https://github.com/DimitriCalmand/news-summary.git
cd news-summary

# 2. Configuration SSH (une seule fois)
chmod +x setup-ssh.sh
./setup-ssh.sh

# 3. Déploiement complet automatisé
chmod +x full-deploy.sh
./full-deploy.sh
```

### 🛠️ **Installation Manuelle**

#### **Prérequis**
- Node.js 18+ et npm
- Python 3.11+ et pip
- Docker et Docker Compose
- Git
- **Clés API IA** (Mistral, DeepSeek, etc.)

#### **Backend Flask avec IA**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configuration initiale des clés IA
cp data/settings.json.example data/settings.json
# Éditer settings.json avec vos clés API

python src/main.py
```
*Serveur disponible sur `http://localhost:3001`*

#### **Frontend React**
```bash
cd frontend
npm install
npm run dev
```
*Application disponible sur `http://localhost:5173`*

#### **Avec Docker (Production)**
```bash
# Démarrage complet
docker-compose -f docker-compose.prod.yml up -d

# Ou pour Raspberry Pi ARM64
docker-compose -f docker-compose.arm64.yml up -d
```

---

## 📚 Documentation API

### **Endpoints IA**

#### **Configuration IA**
```http
GET    /api/settings              # Récupérer la configuration IA
PUT    /api/settings              # Mettre à jour la configuration
GET    /api/settings/models       # Liste des modèles disponibles
GET    /api/settings/prompts      # Récupérer les prompts actuels
```

#### **Chat IA**
```http
POST   /api/articles/{id}/chat    # Envoyer une question à l'IA
GET    /api/articles/{id}/chat    # Récupérer l'historique du chat
DELETE /api/articles/{id}/chat/clear # Vider l'historique du chat
```

#### **Traitement IA d'Articles**
```http
POST   /api/pretreat              # Déclencher le traitement IA des articles
GET    /api/unpretreat            # Articles non traités par l'IA
```

### **Endpoints Articles (Existants)**
```http
GET    /api/length                # Nombre total d'articles
POST   /api/titles                # Liste paginée des titres
GET    /api/article/{id}          # Détail d'un article
GET    /api/articles/filter       # Articles filtrés par tags/rating
PUT    /api/articles/{id}/rating  # Noter un article (1-5)
POST   /api/articles/{id}/reading-time # Ajouter temps de lecture
PUT    /api/articles/{id}/comments # Ajouter/modifier commentaires
PUT    /api/articles/{id}/tags    # Gérer les tags
GET    /api/tags                  # Liste des tags disponibles
GET    /api/health                # Status de l'API
```

### **Exemples d'Utilisation IA**

#### **Configuration d'un nouveau modèle**
```javascript
const newSettings = {
  models: [
    ...existingModels,
    {
      name: "nouveau-modele",
      id: "model-id",
      url: "https://api.provider.com/v1/chat/completions",
      apikey: "votre-clé",
      llm: "provider"
    }
  ],
  default_model: "nouveau-modele",
  prompts: {
    article_processing: "Votre prompt personnalisé...",
    chat: "Votre prompt de chat..."
  }
};

await settingsApi.updateSettings(newSettings);
```

#### **Chat avec l'IA**
```javascript
const chatResponse = await chatApi.sendMessage(articleId, {
  message: "Quels sont les points clés de cet article ?",
  model: "mistral small" // optionnel, utilise le modèle par défaut
});
```

#### **Traitement automatique d'articles**
```python
# Backend - Traitement automatique
from settings import SettingsManager
from ai import pretreat_articles

# Configuration dynamique
settings = SettingsManager.load_settings()
default_model = settings.get("default_model")

# Traitement avec le modèle configuré
pretreat_articles(model_name=default_model)
```

---

## 🎨 Interface Utilisateur

### **Nouvelles Fonctionnalités UI**

#### **Modal de Configuration IA**
- **Design moderne** avec icône d'engrenage
- **Onglets organisés** : Modèles, Prompts, Configuration
- **Formulaires dynamiques** pour l'ajout/suppression de modèles
- **Zones de texte expandables** pour l'édition des prompts
- **Sauvegarde en temps réel** avec indicateurs de statut

#### **Interface de Chat IA**
- **Chat en temps réel** avec bulles de conversation
- **Historique persistent** par article
- **Indicateurs de chargement** pendant les requêtes IA
- **Gestion d'erreurs** avec messages informatifs

#### **Boutons d'Action IA**
- **Bouton Paramètres** : Accès rapide à la configuration
- **Bouton Chat** : Ouverture du chat contextuel
- **Indicateurs de traitement** : Status des articles traités par IA

### **Design System Amélioré**
- **Framework** : Tailwind CSS avec composants IA spécialisés
- **Couleurs** : Palette étendue avec codes couleur pour l'IA
- **Icônes** : Lucide React + icônes spécifiques IA
- **Animations** : Transitions fluides pour les interactions IA

---

## 🚀 Scripts de Déploiement

### **Script Complet Automatisé**
```bash
./full-deploy.sh
```
**Fonctionnalités :**
- ✅ Build des images ARM64 optimisées avec support IA
- ✅ Push automatique vers Docker Hub
- ✅ Déploiement sur Raspberry Pi avec configuration IA
- ✅ Tests de santé automatiques (backend + IA)
- ✅ Affichage des URLs d'accès

### **Variables d'Environnement IA**
```bash
# Configuration IA (optionnel, via interface web)
AI_DEFAULT_MODEL=mistral-small
AI_CONFIG_PATH=/app/data/settings.json

# APIs externes (configurées via interface)
MISTRAL_API_KEY=votre-clé-mistral
DEEPSEEK_API_KEY=votre-clé-deepseek
```

---

## 🔒 Sécurité IA

### **Protection des Clés API**
- ✅ **Stockage sécurisé** des clés dans settings.json
- ✅ **Validation côté serveur** des configurations
- ✅ **Masquage automatique** des clés dans l'interface
- ✅ **Chiffrement** des communications avec les APIs IA

### **Validation des Prompts**
- ✅ **Sanitisation automatique** des inputs utilisateur
- ✅ **Limitation de longueur** des prompts et messages
- ✅ **Protection contre l'injection** de prompts malveillants
- ✅ **Rate limiting** pour les requêtes IA

### **Gestion des Erreurs IA**
- ✅ **Timeout automatique** pour les requêtes longues
- ✅ **Fallback** en cas d'échec d'un modèle
- ✅ **Logs sécurisés** sans exposition des clés
- ✅ **Messages d'erreur** informatifs sans détails techniques

---

## 📊 Performance & Optimisations IA

### **Optimisations Backend IA**
- ✅ **Cache des réponses IA** pour requêtes similaires
- ✅ **Connection pooling** pour les APIs externes
- ✅ **Retry automatique** avec backoff exponentiel
- ✅ **Monitoring des quotas** API

### **Optimisations Frontend**
- ✅ **Lazy loading** des composants IA
- ✅ **Debouncing** des requêtes de chat
- ✅ **Cache local** des configurations
- ✅ **Optimistic updates** pour l'UX

---

## 🛠️ Développement avec IA

### **Structure de Développement IA**
```bash
# Installation avec dépendances IA
pip install -r requirements.txt  # Inclut requests pour APIs IA
npm install                      # Inclut types pour Settings IA

# Configuration développement
cp backend/data/settings.json.example backend/data/settings.json
# Ajouter vos clés API de test

# Tests IA
python -m pytest tests/test_ai.py        # Tests unitaires IA
npm run test -- --grep "Settings"        # Tests configuration frontend
```

### **Ajout d'un Nouveau Modèle IA**
1. **Ajouter le modèle** dans `settings.json`
2. **Tester la compatibilité** avec `ai.py`
3. **Mettre à jour les types** TypeScript
4. **Ajouter les tests** appropriés

---

## 📱 Guide d'Utilisation IA

### **Configuration Initiale**
1. **Accéder aux paramètres** : Clic sur l'icône engrenage
2. **Ajouter vos clés API** : Configuration des modèles
3. **Personnaliser les prompts** : Selon vos besoins
4. **Sélectionner le modèle par défaut** : Via liste déroulante
5. **Sauvegarder** : Configuration persistante

### **Utilisation du Chat IA**
1. **Ouvrir un article** : Navigation vers la page détail
2. **Accéder au chat** : Section dédiée en bas de page
3. **Poser une question** : Saisie dans la zone de texte
4. **Recevoir la réponse** : Réponse contextualisée de l'IA
5. **Continuer la conversation** : Historique persistent

### **Traitement Automatique**
1. **Articles non traités** : Détection automatique
2. **Lancement du traitement** : Via API ou interface
3. **Résultats** : Articles reformatés avec résumés et tags
4. **Vérification** : Contrôle qualité manuel possible

---

## 🚨 Troubleshooting IA

### **Problèmes Courants**

#### **"Modèle IA non disponible"**
```bash
# Vérifier la configuration
curl -X GET http://localhost:3001/api/settings/models

# Tester la connectivité API
curl -X POST "https://api.mistral.ai/v1/chat/completions" \
  -H "Authorization: Bearer VOTRE_CLE" \
  -H "Content-Type: application/json"
```

#### **"Configuration IA non sauvegardée"**
```bash
# Vérifier les permissions
ls -la backend/data/settings.json
chmod 644 backend/data/settings.json

# Vérifier la structure JSON
python -m json.tool backend/data/settings.json
```

#### **"Chat IA ne répond pas"**
```bash
# Logs backend
docker-compose logs -f backend | grep -i "ai\|chat"

# Test manuel API
curl -X POST http://localhost:3001/api/articles/1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Test question", "model": "mistral small"}'
```

### **Debug et Monitoring**
```bash
# Logs spécifiques IA
tail -f backend/logs/ai.log

# Monitoring des requêtes IA
docker-compose exec backend python -c "
from settings import SettingsManager
print(SettingsManager.load_settings())
"

# Test complet de la configuration
curl http://localhost:3001/api/health | jq '.ai_status'
```

---

## 🤝 Contribution

### **Nouvelles Guidelines IA**
1. **Tests IA obligatoires** pour nouvelles fonctionnalités
2. **Documentation des prompts** et de leur usage
3. **Validation des APIs** avant merge
4. **Performance testing** pour les requêtes IA
5. **Sécurité audit** pour les clés et configurations

### **Standards de Code IA**
- **Type safety** strict pour Settings et Models
- **Error handling** robuste pour APIs externes
- **Async/await** pour toutes les requêtes IA
- **Loading states** pour l'UX pendant les requêtes

---

## 📄 Licence

Ce projet est sous licence **MIT**. Voir le fichier `LICENSE` pour plus de détails.

---

## 👥 Auteurs

- **Dimitri Calmand** - *Développeur Principal & Architecte IA* - [GitHub](https://github.com/DimitriCalmand)

---

## 🙏 Remerciements

- **Mistral AI** pour les modèles de langage performants
- **DeepSeek** pour l'innovation en IA open-source
- **React Team** pour l'excellent framework
- **Flask Team** pour l'API simple et efficace
- **TanStack** pour React Query
- **Tailwind CSS** pour le design system
- **Communauté Open Source** pour l'écosystème IA

---

<div align="center">

**⭐ Application moderne avec IA intégrée - Donnez une étoile si elle vous aide !**

[🐛 Reporter un Bug](https://github.com/DimitriCalmand/news-summary/issues) • 
[💡 Suggérer une Fonctionnalité IA](https://github.com/DimitriCalmand/news-summary/issues) • 
[📖 Documentation IA](https://github.com/DimitriCalmand/news-summary/wiki/AI-Integration)

**🤖 Powered by AI • 🚀 Built for the Future**

</div>
│   ├── src/
│   │   ├── components/          # Composants React réutilisables
│   │   │   ├── ArticleDetail.tsx     # Page détail d'article
│   │   │   ├── ArticleList.tsx       # Liste paginée d'articles
│   │   │   ├── StarRating.tsx        # Système de notation
│   │   │   ├── TagsEditor.tsx        # Gestionnaire de tags
│   │   │   ├── CommentsEditor.tsx    # Zone de commentaires
│   │   │   ├── AutoReadingTimer.tsx  # Timer intelligent
│   │   │   ├── ArticleFilters.tsx    # Interface de filtrage
│   │   │   └── PaginationControls.tsx # Contrôles pagination
│   │   ├── utils/
│   │   │   └── api.ts           # Client API TypeScript
│   │   ├── types/
│   │   │   └── index.ts         # Types TypeScript
│   │   └── lib/
│   │       └── utils.ts         # Utilitaires UI
│   ├── 🐳 Dockerfile            # Build multi-architecture
│   └── 📦 package.json          # Dépendances Node.js
│
├── 🐍 backend/                  # API Flask Python
│   ├── src/
│   │   ├── models.py            # Modèles de données et ArticleManager
│   │   ├── routes.py            # Endpoints API REST
│   │   ├── cache.py             # Système de cache intelligent
│   │   └── ai.py                # Résumés automatiques (IA)
│   ├── 🐳 Dockerfile            # Build optimisé Python
│   └── 📋 requirements.txt      # Dépendances Python
│
├── 🚀 .github/workflows/        # CI/CD GitHub Actions
│   └── docker-build.yml        # Build/Deploy automatique ARM64
│
├── 🐳 Docker Compose Files      # Orchestration des services
│   ├── docker-compose.yml           # Développement local
│   ├── docker-compose.prod.yml      # Production générique
│   └── docker-compose.arm64.yml     # Raspberry Pi ARM64
│
└── 🛠️ Scripts de Déploiement    # Automatisation DevOps
    ├── deploy.sh                # Script principal multi-plateforme
    ├── full-deploy.sh           # Déploiement complet automatisé
    └── setup-ssh.sh             # Configuration SSH sans mot de passe
```

---

## 📋 Installation

### 🚀 **Déploiement Rapide (Recommandé)**

```bash
# 1. Cloner le repository
git clone https://github.com/votre-username/news-summary.git
cd news-summary

# 2. Configuration SSH (une seule fois)
chmod +x setup-ssh.sh
./setup-ssh.sh

# 3. Déploiement complet automatisé
chmod +x full-deploy.sh
./full-deploy.sh
```

### 🛠️ **Installation Manuelle**

#### **Prérequis**
- Node.js 18+ et npm
- Python 3.11+ et pip
- Docker et Docker Compose
- Git

#### **Backend Flask**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python src/app.py
```
*Serveur disponible sur `http://localhost:3001`*

#### **Frontend React**
```bash
cd frontend
npm install
npm run dev
```
*Application disponible sur `http://localhost:5173`*

#### **Avec Docker (Production)**
```bash
# Démarrage complet
docker-compose -f docker-compose.prod.yml up -d

# Ou pour Raspberry Pi ARM64
docker-compose -f docker-compose.arm64.yml up -d
```

---

## 🔧 Configuration

### **Variables d'Environnement**

#### Frontend (`.env.development`)
```bash
VITE_API_URL=http://localhost:3001/api/
```

#### Backend
```bash
PORT=3001
DEBUG=true
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### **Configuration Docker Hub**
```bash
# Secrets GitHub Actions requis
DOCKERHUB_USERNAME=votre-username
DOCKERHUB_TOKEN=votre-token
RASPI_HOST=192.168.1.137
RASPI_USERNAME=pi
RASPI_SSH_KEY=votre-cle-privee
RASPI_PORT=22
```

---

## 📚 Documentation API

### **Endpoints Principaux**

#### **Articles**
```http
GET    /api/length                 # Nombre total d'articles
POST   /api/titles                 # Liste paginée des titres
GET    /api/article/{id}           # Détail d'un article
GET    /api/articles/filter        # Articles filtrés par tags/rating
```

#### **Gestion des Données**
```http
PUT    /api/articles/{id}/rating   # Noter un article (1-5)
POST   /api/articles/{id}/reading-time # Ajouter temps de lecture
PUT    /api/articles/{id}/comments # Ajouter/modifier commentaires
PUT    /api/articles/{id}/tags     # Gérer les tags
GET    /api/tags                   # Liste des tags disponibles
```

#### **Santé du Service**
```http
GET    /api/health                 # Status de l'API
```

### **Exemples d'Utilisation**

#### **Récupérer des articles avec pagination**
```javascript
// Frontend TypeScript
const { data: articles } = useQuery({
  queryKey: ['articleTitles', currentPage],
  queryFn: () => newsApi.getTitles(currentPage, 10)
});
```

#### **Noter un article**
```javascript
const rateArticle = useMutation({
  mutationFn: ({ id, rating }) => newsApi.rateArticle(id, rating),
  onSuccess: () => queryClient.invalidateQueries(['article'])
});
```

#### **Filtrer par tags**
```python
# Backend Python
@app.route('/api/articles/filter', methods=['GET'])
def filter_articles():
    tags = request.args.getlist('tags')
    min_rating = int(request.args.get('min_rating', 0))
    
    articles = ArticleManager.load_articles()
    filtered = [a for a in articles 
               if a.get('rating', 0) >= min_rating
               and any(tag in a.get('tags', []) for tag in tags)]
    
    return jsonify(filtered)
```

---

## 🚀 Scripts de Déploiement

### **Script Complet Automatisé**
```bash
./full-deploy.sh
```
**Fonctionnalités :**
- ✅ Build des images ARM64 optimisées
- ✅ Push automatique vers Docker Hub
- ✅ Déploiement sur Raspberry Pi
- ✅ Tests de santé automatiques
- ✅ Affichage des URLs d'accès

### **Script Manuel Avancé**
```bash
# Build multi-architecture
./deploy.sh multiarch

# Build ARM64 uniquement
./deploy.sh arm64

# Build local pour test
./deploy.sh build

# Push vers Docker Hub
./deploy.sh push
```

---

## 🔄 CI/CD GitHub Actions

### **Workflow Automatique**
- **Déclenchement :** Push sur `main` ou déclenchement manuel
- **Build :** Images ARM64 optimisées pour Raspberry Pi
- **Tests :** Vérification de santé des services
- **Déploiement :** Automatique sur Raspberry Pi via SSH

### **Fonctionnalités Avancées**
- ✅ **Cache intelligent** pour builds rapides
- ✅ **Timeouts optimisés** (90min total, 45min frontend)
- ✅ **Libération d'espace disque** automatique
- ✅ **Logs détaillés** pour debugging
- ✅ **Rollback automatique** en cas d'échec

---

## 🎨 Interface Utilisateur

### **Design System**
- **Framework :** Tailwind CSS avec composants personnalisés
- **Couleurs :** Palette moderne avec mode sombre/clair
- **Typographie :** Inter font pour lisibilité optimale
- **Icônes :** Lucide React pour cohérence visuelle

### **Responsive Design**
- ✅ **Mobile First** avec breakpoints adaptatifs
- ✅ **Touch-friendly** pour tablettes/mobiles
- ✅ **Desktop optimisé** avec shortcuts clavier
- ✅ **Accessibilité** WCAG 2.1 AA compliant

### **Animations & Transitions**
- ✅ **Micro-interactions** fluides
- ✅ **Loading states** avec spinners élégants
- ✅ **Transitions de page** smooth
- ✅ **Feedback visuel** immédiat

---

## 📊 Performance & Optimisations

### **Frontend**
- ✅ **Code splitting** automatique avec Vite
- ✅ **Lazy loading** des composants
- ✅ **React Query cache** intelligent
- ✅ **Bundle optimization** < 500KB gzippé

### **Backend**
- ✅ **Cache en mémoire** pour requêtes fréquentes
- ✅ **Pagination efficace** côté serveur
- ✅ **Compression gzip** automatique
- ✅ **Rate limiting** pour protection API

### **Infrastructure**
- ✅ **Docker multi-stage builds** optimisés
- ✅ **Nginx caching** pour assets statiques
- ✅ **Health checks** automatiques
- ✅ **Logs structurés** pour monitoring

---

## 🔒 Sécurité

### **Frontend**
- ✅ **Input sanitization** automatique
- ✅ **XSS protection** avec CSP headers
- ✅ **HTTPS enforcement** en production
- ✅ **Environment variables** sécurisées

### **Backend**
- ✅ **CORS configuration** stricte
- ✅ **Input validation** sur tous les endpoints
- ✅ **Error handling** sécurisé sans leaks
- ✅ **Rate limiting** anti-DDoS

### **Infrastructure**
- ✅ **SSH key authentication** uniquement
- ✅ **Docker security** best practices
- ✅ **Network isolation** entre services
- ✅ **Regular security updates** automatiques

---

## 🛠️ Développement

### **Structure de Développement**
```bash
# Installation développement
npm install          # Frontend dependencies
pip install -r requirements.txt  # Backend dependencies

# Lancement développement
npm run dev          # Frontend dev server (port 5173)
python src/app.py    # Backend dev server (port 3001)

# Tests
npm test            # Frontend tests
python -m pytest   # Backend tests

# Linting
npm run lint        # Frontend linting
flake8 src/         # Backend linting
```

### **Git Workflow**
```bash
# Feature branch
git checkout -b feature/nouvelle-fonctionnalite
git commit -m "feat: description de la fonctionnalité"
git push origin feature/nouvelle-fonctionnalite

# Pull request → main
# → Déclenchement automatique du CI/CD
```

---

## 📱 Utilisation

### **Navigation Principale**
1. **Page d'accueil** : Liste paginée des articles avec filtres
2. **Détail article** : Lecture complète avec toutes les fonctionnalités
3. **Filtrage** : Recherche par tags, notes, et combinaisons

### **Fonctionnalités Clés**
- **🌟 Noter** : Cliquer sur les étoiles (1-5)
- **🏷️ Tagger** : Ajouter des tags personnalisés avec autocomplétion
- **💬 Commenter** : Zone de commentaires personnels pliable
- **⏱️ Timer** : Suivi automatique du temps de lecture
- **🔍 Filtrer** : Combinaisons de filtres pour recherche précise

---

## 🚨 Troubleshooting

### **Problèmes Courants**

#### **"Article introuvable" lors du clic**
```bash
# Vérifier que l'ID 0 est bien géré
# Solution déjà implementée dans ArticleDetail.tsx
```

#### **Timer qui augmente trop vite**
```bash
# Vérifier la logique de delta time
# Solution implementée avec lastSavedSessionTime
```

#### **Erreur build ARM64 "esbuild linux-arm64"**
```bash
# Solution dans Dockerfile frontend
RUN npm install --include=optional
RUN npm install @esbuild/linux-arm64 --force
```

#### **Erreur réseau Docker "Pool overlaps"**
```bash
docker network prune -f
docker-compose down --remove-orphans
```

### **Logs & Debugging**
```bash
# Logs conteneurs en direct
docker-compose logs -f backend
docker-compose logs -f frontend

# Debug API locale
curl http://localhost:3001/api/health

# Debug frontend
http://localhost:5173 (ouvrir DevTools)
```

---

## 🤝 Contribution

### **Guidelines**
1. **Fork** le repository
2. **Feature branch** depuis `main`
3. **Tests** pour nouvelles fonctionnalités
4. **Pull request** avec description détaillée
5. **Code review** par l'équipe

### **Standards de Code**
- **TypeScript** strict mode activé
- **ESLint + Prettier** pour formatting
- **Conventional Commits** pour messages
- **Tests unitaires** requis pour nouveaux composants

---

## 📄 Licence

Ce projet est sous licence **MIT**. Voir le fichier `LICENSE` pour plus de détails.

---

## 👥 Auteurs

- **Dimitri** - *Développeur Principal* - [GitHub](https://github.com/dimitriepita)

---

## 🙏 Remerciements

- **React Team** pour l'excellent framework
- **Flask Team** pour l'API simple et efficace
- **TanStack** pour React Query
- **Tailwind CSS** pour le design system
- **Communauté Open Source** pour les outils utilisés

---

<div align="center">

**⭐ Si ce projet vous aide, n'hésitez pas à lui donner une étoile !**

[🐛 Reporter un Bug](https://github.com/dimitriepita/news-summary/issues) • 
[💡 Suggérer une Fonctionnalité](https://github.com/dimitriepita/news-summary/issues) • 
[📖 Documentation](https://github.com/dimitriepita/news-summary/wiki)

</div>