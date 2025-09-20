# Étape 1: Build de l'application React
FROM node:20-alpine AS build

# Installe les dépendances système nécessaires pour les builds natifs
RUN apk add --no-cache python3 make g++

# Définit le répertoire de travail
WORKDIR /app

# Copie les fichiers de configuration des dépendances
COPY package.json package-lock.json* ./

# Installation optimisée des dépendances
# Installation avec dépendances optionnelles pour esbuild multi-arch
RUN npm ci --include=optional --no-audit --no-fund --silent || \
    (npm cache clean --force && npm install --include=optional --no-audit --no-fund --silent)

# Copie le code source après l'installation des dépendances (pour un meilleur cache)
COPY . .

# Vérification que les fichiers importés existent
RUN ls -la src/lib/ && \
    test -f src/lib/utils.ts && \
    echo "utils.ts found" || echo "utils.ts NOT FOUND"

# Installation explicite des binaires esbuild pour l'architecture cible
RUN case $(uname -m) in \
    aarch64|arm64) npm install --no-save @esbuild/linux-arm64 ;; \
    x86_64|amd64) npm install --no-save @esbuild/linux-x64 ;; \
    *) echo "Architecture non supportée: $(uname -m)" && exit 1 ;; \
    esac

# Build l'application pour la production avec plus de mémoire allouée
RUN NODE_OPTIONS="--max-old-space-size=4096" npm run build

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