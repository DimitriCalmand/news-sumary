@echo off
REM 🔥 Script de développement Windows avec Hot Reload

echo 🚀 Démarrage du serveur de développement avec Hot Reload...
echo 📁 Répertoire: %cd%
echo 🔄 Hot Reload: ACTIVÉ
echo 📝 Les fichiers seront rechargés automatiquement à chaque sauvegarde
echo ---

REM Variables d'environnement pour le développement
set FLASK_ENV=development
set FLASK_DEBUG=1
set PORT=3001

REM Lancer le serveur avec hot reload
cd src
python main.py