# Image Python légère
FROM python:3.11-slim

# Crée un répertoire pour l'app
WORKDIR /app

# Upgrade pip and install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

# Installe les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV API_URL="http://backend:8000/api/articles"

# Copie le code source
COPY src/ ./src

CMD ["streamlit", "run", "src/app.py", "--server.port", "8000", "--server.address", "0.0.0.0"]