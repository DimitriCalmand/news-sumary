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

# Copie tout le code de l'application
COPY . .

# Crée le répertoire data s'il n'existe pas
RUN mkdir -p data

# Définit les variables d'environnement
ENV PYTHONPATH=/app
ENV PORT=3001

# Expose le port sur lequel l'application écoute
EXPOSE 3001

# Commande pour lancer l'application
CMD ["python", "src/main.py"]