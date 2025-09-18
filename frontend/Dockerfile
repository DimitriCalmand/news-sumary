# Image Python légère
FROM python:3.11-slim

# Crée un répertoire pour l'app
WORKDIR /app

RUN pip install --upgrade pip
# Installe les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie le code source
COPY src/ ./src


CMD ["streamlit", "run", "src/app.py", "--server.port", "8000", "--server.address", "0.0.0.0"]
