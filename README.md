# 📰 News Summary - Gestionnaire d'Articles Intelligent

<div align="center">

![Node.js](https://img.shields.io/badge/Node.js-43853D?style=for-the-badge&logo=node.js&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-A22846?style=for-the-badge&logo=Raspberry%20Pi&logoColor=white)

**Une application moderne de gestion et résumé d'articles avec interface React et API Flask**

[🚀 Fonctionnalités](#-fonctionnalités) • 
[📋 Installation](#-installation) • 
[🛠️ Technologies](#️-technologies) • 
[🏗️ Architecture](#️-architecture) • 
[📚 Documentation](#-documentation-api)

</div>

---

## 📖 Description

News Summary est une application web complète permettant de gérer, organiser et analyser des articles de presse. Elle offre une interface utilisateur moderne avec des fonctionnalités avancées de notation, commentaires, tags, et suivi du temps de lecture.

## 🌟 Fonctionnalités

### 📰 **Gestion d'Articles**
- ✅ **Lecture d'articles** avec interface moderne et responsive
- ✅ **Pagination intelligente** côté serveur et client
- ✅ **Recherche et filtrage** par tags et notes
- ✅ **Résumés automatiques** des articles longs
- ✅ **Support Markdown** avec highlighting de code

### ⭐ **Système d'Évaluation**
- ✅ **Notation 5 étoiles** interactive
- ✅ **Feedback visuel instantané** lors du clic
- ✅ **Persistance automatique** des notes

### 🏷️ **Gestion des Tags**
- ✅ **Tags personnalisés** pour catégoriser les articles
- ✅ **Autocomplétion** basée sur les tags existants
- ✅ **Filtrage par tags** avec interface intuitive
- ✅ **Tags populaires** affichés en priorité

### 💬 **Commentaires Personnels**
- ✅ **Zone de commentaires** pliable/dépliable
- ✅ **Édition en temps réel** avec sauvegarde automatique
- ✅ **Interface minimaliste** et élégante

### ⏱️ **Suivi du Temps de Lecture**
- ✅ **Timer automatique** se déclenchant à l'ouverture d'un article
- ✅ **Pause intelligente** quand la page devient inactive
- ✅ **Cumul du temps** sur plusieurs sessions
- ✅ **Sauvegarde périodique** toutes les 10 secondes

### 🔍 **Filtrage Avancé**
- ✅ **Filtrage par note minimale** avec interface étoiles
- ✅ **Filtrage par tags multiples** avec sélection rapide
- ✅ **Combinaison de filtres** pour recherches précises
- ✅ **Pagination des résultats filtrés**

---

## 🛠️ Technologies

### **Frontend**
- **React 19.1.1** - Framework UI moderne
- **TypeScript 5.8.3** - Typage statique
- **Vite 7.1.6** - Build tool ultra-rapide
- **TanStack Query** - Gestion d'état et cache
- **React Router 7.9.1** - Navigation SPA
- **Tailwind CSS 3.4.17** - Framework CSS utilitaire
- **React Markdown 10.1.0** - Rendu Markdown
- **Lucide React** - Icônes modernes

### **Backend**
- **Python 3.11+** - Langage serveur
- **Flask 3.1.0** - Framework web léger
- **Flask-CORS 5.0.0** - Gestion CORS
- **Requests 2.32.3** - Client HTTP
- **BeautifulSoup4 4.12.3** - Parsing HTML

### **Infrastructure**
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