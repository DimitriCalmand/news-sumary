# News Summary - Guide de Développement

## Configuration de l'environnement de développement avec hot reload

### 1. Prérequis
- Python 3.11+
- Node.js 20+
- Docker et Docker Compose (optionnel)

### 2. Installation

#### Backend (Flask)
```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

#### Frontend (React + Vite)
```bash
cd frontend
npm install
```

### 3. Développement avec hot reload

#### Option 1: Scripts de développement (Recommandé)

**Backend avec hot reload :**
```bash
cd backend
# Windows
dev.bat
# Linux/Mac
./dev.sh
```

**Frontend avec hot reload :**
```bash
cd frontend
npm run dev
```

#### Option 2: VS Code Tasks
Utilisez `Ctrl+Shift+P` → "Tasks: Run Task" et sélectionnez :
- "Hot Reload Backend Server" - Lance le backend avec rechargement automatique
- "Frontend Dev Server" - Lance le frontend avec Vite
- "Full Dev Environment" - Lance les deux simultanément

#### Option 3: Commandes manuelles

**Backend :**
```bash
cd backend
set FLASK_ENV=development && python src/main.py
```

**Frontend :**
```bash
cd frontend
npm run dev
```

### 4. Configuration du hot reload

Le hot reload fonctionne automatiquement grâce à :

#### Backend :
- `FLASK_ENV=development` active le mode debug
- `app.run(debug=True, use_reloader=True)` dans `main.py`
- Redémarre automatiquement quand vous modifiez des fichiers Python

#### Frontend :
- Vite intègre le hot reload par défaut
- Rechargement instantané lors de modifications de fichiers React/TS

#### VS Code :
- `files.autoSave: "onFocusChange"` - Sauvegarde automatique
- `editor.formatOnSave: true` - Formatage automatique
- Configuration Python et TypeScript optimisée

### 5. URLs de développement

- **Backend API :** http://localhost:5000
- **Frontend :** http://localhost:5173
- **API Health Check :** http://localhost:5000/health

### 6. Structure modulaire du backend

```
backend/src/
├── main.py          # Point d'entrée avec hot reload
├── config.py        # Configuration et variables d'environnement
├── models.py        # Classes Article et ArticleManager
├── cache.py         # Système de cache avec expiration
├── scraper.py       # Service de scraping TechCrunch
└── routes.py        # Endpoints API REST
```

### 7. Débogage

#### Backend :
- Les logs s'affichent dans le terminal avec le niveau DEBUG
- Modification d'un fichier → redémarrage automatique du serveur
- Breakpoints supportés avec l'extension Python de VS Code

#### Frontend :
- Hot Module Replacement (HMR) de Vite
- React DevTools disponibles dans le navigateur
- Console du navigateur pour les erreurs JS/TS

### 8. Production avec Docker

#### Développement local :
```bash
docker-compose up --build
```

#### Production :
```bash
docker-compose -f docker-compose.prod.yml up --build
```

### 9. Conseils pour le développement

1. **Sauvegarde automatique :** Vos fichiers se sauvegardent automatiquement quand vous changez de fenêtre
2. **Formatage automatique :** Le code se formate automatiquement à la sauvegarde
3. **Hot reload :** Aucun redémarrage manuel nécessaire pendant le développement
4. **Multi-terminal :** Utilisez VS Code intégré pour lancer backend et frontend simultanément
5. **Debugging :** Placez des breakpoints directement dans VS Code pour le backend Python

### 10. Troubleshooting

#### Le hot reload ne fonctionne pas :
- Vérifiez que `FLASK_ENV=development` est défini
- Redémarrez le serveur backend manuellement
- Vérifiez les logs pour les erreurs de syntaxe

#### Port déjà utilisé :
- Backend : Modifiez le port dans `config.py`
- Frontend : Vite choisira automatiquement un port libre

#### Erreurs de CORS :
- Vérifiez que flask-cors est installé
- Le backend est configuré pour accepter les requêtes depuis localhost:5173