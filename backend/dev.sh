#!/bin/bash

# 🔥 Script de développement avec Hot Reload
# Lance le backend avec rechargement automatique

echo "🚀 Démarrage du serveur de développement avec Hot Reload..."
echo "📁 Répertoire: $(pwd)"
echo "🔄 Hot Reload: ACTIVÉ"
echo "📝 Les fichiers seront rechargés automatiquement à chaque sauvegarde"
echo "---"

# Variables d'environnement pour le développement
export FLASK_ENV=development
export FLASK_DEBUG=1

# Lancer le serveur avec hot reload
python3 src/main.py