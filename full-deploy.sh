#!/bin/bash

# 🚀 Script de Build et Déploiement Complet sur Raspberry Pi
# Usage: ./full-deploy.sh

set -e

# Configuration
RASPI_HOST="192.168.1.137"
RASPI_USER="server"
RASPI_PATH="/Disk/Programmation/Intern/News-sumary"
DOCKERHUB_USERNAME="dimitriepita"
BACKEND_IMAGE="news-summary-backend"
FRONTEND_IMAGE="news-summary-frontend"

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${BLUE}==========================================${NC}"
    echo -e "${BLUE}  🚀 News Summary Full Deploy Script    ${NC}"
    echo -e "${BLUE}==========================================${NC}"
}

print_step() {
    echo -e "${BLUE}📋 Step $1: $2${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Vérifier les prérequis
check_prerequisites() {
    print_step "1" "Vérification des prérequis"
    
    # Vérifier Docker et Buildx
    if ! docker buildx version > /dev/null 2>&1; then
        print_error "Docker Buildx n'est pas disponible"
        exit 1
    fi
    
    # Vérifier la connexion SSH
    if ! ssh -o BatchMode=yes -o ConnectTimeout=5 ${RASPI_USER}@${RASPI_HOST} exit 2>/dev/null; then
        print_error "Impossible de se connecter à la Raspberry Pi via SSH"
        print_warning "Assurez-vous que la clé SSH est configurée"
        exit 1
    fi
    
    # Vérifier la connexion Docker Hub
    if ! docker info | grep -q "Username:"; then
        print_warning "Non connecté à Docker Hub, tentative de connexion..."
        docker login
    fi
    
    print_success "Tous les prérequis sont satisfaits"
}

# Configurer le builder multi-architecture
setup_builder() {
    print_step "2" "Configuration du builder multi-architecture"
    
    if ! docker buildx inspect arm64-builder > /dev/null 2>&1; then
        echo -e "${YELLOW}Création du builder 'arm64-builder'...${NC}"
        docker buildx create --name arm64-builder --driver docker-container --use
        docker buildx inspect --bootstrap
    else
        echo -e "${YELLOW}Utilisation du builder existant 'arm64-builder'...${NC}"
        docker buildx use arm64-builder
    fi
    
    print_success "Builder configuré"
}

# Build des images ARM64
build_images() {
    print_step "3" "Build des images ARM64"
    
    # Build Frontend ARM64
    echo -e "${YELLOW}Building frontend ARM64...${NC}"
    docker buildx build \
        --platform linux/arm64 \
        -t ${DOCKERHUB_USERNAME}/${FRONTEND_IMAGE}:arm64 \
        --push \
        ./frontend
    
    print_success "Frontend ARM64 built et pushed"
    
    # Build Backend ARM64  
    echo -e "${YELLOW}Building backend ARM64...${NC}"
    docker buildx build \
        --platform linux/arm64 \
        -t ${DOCKERHUB_USERNAME}/${BACKEND_IMAGE}:arm64 \
        --push \
        ./backend
    
    print_success "Backend ARM64 built et pushed"
    print_success "Toutes les images ARM64 sont disponibles sur Docker Hub"
}

# Copier le docker-compose sur la Raspberry Pi
copy_compose_file() {
    print_step "4" "Copie du docker-compose.arm64.yml sur Raspberry Pi"
    
    scp docker-compose.arm64.yml ${RASPI_USER}@${RASPI_HOST}:${RASPI_PATH}/docker-compose.arm64.yml
    
    print_success "docker-compose.arm64.yml copié sur Raspberry Pi"
}

# Déployer sur Raspberry Pi
deploy_to_raspi() {
    print_step "5" "Déploiement sur Raspberry Pi"
    
    ssh ${RASPI_USER}@${RASPI_HOST} << EOF
        set -e
        cd ${RASPI_PATH}
        
        echo "📁 Dans le répertoire: \$(pwd)"
        
        # Stopper les anciens conteneurs
        echo "🛑 Arrêt des conteneurs existants..."
        docker-compose -f docker-compose.arm64.yml down --remove-orphans || true
        docker network prune -f || true
        
        # Nettoyer les anciennes images
        echo "🧹 Nettoyage des anciennes images..."
        docker rmi ${DOCKERHUB_USERNAME}/${BACKEND_IMAGE}:arm64 || true
        docker rmi ${DOCKERHUB_USERNAME}/${FRONTEND_IMAGE}:arm64 || true
        docker image prune -f
        
        # Pull des nouvelles images
        echo "📥 Téléchargement des nouvelles images ARM64..."
        docker pull ${DOCKERHUB_USERNAME}/${BACKEND_IMAGE}:arm64
        docker pull ${DOCKERHUB_USERNAME}/${FRONTEND_IMAGE}:arm64
        
        # Créer le répertoire data et initialiser articles_seen.json
        mkdir -p data
        
        # Créer articles_seen.json s'il n'existe pas (pour la persistance)
        if [ ! -f data/articles_seen.json ]; then
            echo "📋 Création du fichier articles_seen.json..."
            echo "[]" > data/articles_seen.json
            echo "✅ articles_seen.json créé"
        else
            echo "✅ articles_seen.json déjà présent"
        fi
        
        # Créer chat_history.json s'il n'existe pas (pour les conversations IA)
        if [ ! -f data/chat_history.json ]; then
            echo "📋 Création du fichier chat_history.json..."
            echo "{}" > data/chat_history.json
            echo "✅ chat_history.json créé"
        else
            echo "✅ chat_history.json déjà présent"
        fi
        
        # Démarrer les nouveaux conteneurs
        echo "🚀 Démarrage des nouveaux conteneurs..."
        docker-compose -f docker-compose.arm64.yml up -d
        
        # Attendre le démarrage
        echo "⏱️  Attente du démarrage des services (15s)..."
        sleep 15
        
        # Vérifier le statut
        echo "📊 État des conteneurs:"
        docker-compose -f docker-compose.arm64.yml ps
        
        # Afficher les logs
        echo "📋 Logs récents du backend:"
        docker-compose -f docker-compose.arm64.yml logs --tail=5 backend
        
        echo "📋 Logs récents du frontend:"
        docker-compose -f docker-compose.arm64.yml logs --tail=5 frontend
        
        # Tests de santé
        echo "🔍 Tests de santé:"
        if curl -f -s http://localhost:3001/health > /dev/null; then
            echo "✅ Backend (port 3001) : OK"
        else
            echo "❌ Backend (port 3001) : ÉCHEC"
        fi
        
        if curl -f -s http://localhost:3000 > /dev/null; then
            echo "✅ Frontend (port 3000) : OK"
        else
            echo "❌ Frontend (port 3000) : ÉCHEC"
        fi
        
        echo "🎉 Déploiement terminé !"
EOF
    
    print_success "Déploiement sur Raspberry Pi terminé"
}

# Afficher les informations finales
show_final_info() {
    print_step "6" "Informations finales"
    
    echo -e "${GREEN}🎉 Déploiement complet terminé avec succès !${NC}"
    echo ""
    echo -e "${BLUE}📱 Accès à l'application :${NC}"
    echo -e "${GREEN}  • Frontend : http://${RASPI_HOST}:3000${NC}"
    echo -e "${GREEN}  • Backend  : http://${RASPI_HOST}:3001${NC}"
    echo -e "${GREEN}  • Health   : http://${RASPI_HOST}:3001/health${NC}"
    echo ""
    echo -e "${BLUE}🔧 Commandes utiles sur Raspberry Pi :${NC}"
    echo -e "${YELLOW}  ssh ${RASPI_USER}@${RASPI_HOST}${NC}"
    echo -e "${YELLOW}  cd ${RASPI_PATH}${NC}"
    echo -e "${YELLOW}  docker-compose -f docker-compose.arm64.yml logs -f${NC}"
    echo -e "${YELLOW}  docker-compose -f docker-compose.arm64.yml ps${NC}"
    echo ""
    echo -e "${BLUE}📊 Images déployées :${NC}"
    echo -e "${GREEN}  • ${DOCKERHUB_USERNAME}/${BACKEND_IMAGE}:arm64${NC}"
    echo -e "${GREEN}  • ${DOCKERHUB_USERNAME}/${FRONTEND_IMAGE}:arm64${NC}"
}

# Script principal
main() {
    print_header
    
    check_prerequisites
    setup_builder
    build_images
    copy_compose_file
    deploy_to_raspi
    show_final_info
}

# Exécuter le script principal
main "$@"