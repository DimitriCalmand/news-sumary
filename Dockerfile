# Image Python légère
FROM python:3.11-slim

# Crée un répertoire pour l'app
WORKDIR /app

# Installe les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie le code source
COPY src/ ./src

# Définit la variable d'environnement Flask
ENV PORT=80
ENV DEBUG=True
ENV FLASK_APP=src/app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=$PORT

# Expose le port
EXPOSE $PORT

# Commande de lancement
CMD ["flask", "run"]
