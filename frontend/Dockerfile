# Étape 1: Build de l'application React
FROM node:20-alpine AS build

# Définit le répertoire de travail
WORKDIR /app

# Copie les fichiers de configuration des dépendances
COPY package.json package-lock.json* ./

# Nettoie le cache npm et installe les dépendances
RUN npm cache clean --force && \
    rm -rf node_modules package-lock.json && \
    npm install --no-optional --prefer-offline

# Copie le code source
COPY . .

# Build l'application pour la production
RUN npm run build

# Étape 2: Serveur Nginx pour servir l'application
FROM nginx:alpine

# Copie les fichiers buildés depuis l'étape précédente
COPY --from=build /app/dist /usr/share/nginx/html

# Copie la configuration Nginx personnalisée
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose le port 80
EXPOSE 80

# Démarre Nginx
CMD ["nginx", "-g", "daemon off;"]