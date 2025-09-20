# Utilise une image Python officielle comme base
FROM python:3.11-slim

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Met à jour pip d'abord
RUN pip install --upgrade pip

# Copie le fichier requirements.txt
COPY requirements.txt .

# Installe les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie le code source
COPY src/ ./src/

# Copie le répertoire data avec les fichiers de configuration
COPY data/ ./data/

# S'assure que le répertoire data existe et que models.json est accessible
RUN ls -la data/ && cat data/models.json

# Définit les variables d'environnement
ENV PYTHONPATH=/app
ENV PORT=3001

# Expose le port sur lequel l'application écoute
EXPOSE 3001

# Commande pour lancer l'application
CMD ["python", "src/main.py"]