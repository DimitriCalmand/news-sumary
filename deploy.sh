#!/bin/bash

# 🚀 Script de déploiement News Summary
# Usage: ./deploy.sh [command]

set -e

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DOCKERHUB_USERNAME=${DOCKERHUB_USERNAME:-"dimitriepita"}
BACKEND_IMAGE="news-summary-backend"
FRONTEND_IMAGE="news-summary-frontend"

print_header() {
    echo -e "${BLUE}======================================${NC}"
    echo -e "${BLUE}  🚀 News Summary Deployment Script  ${NC}"
    echo -e "${BLUE}======================================${NC}"
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

build_images() {
    print_header
    echo -e "${BLUE}🔨 Building Docker images...${NC}"
    
    # Build backend
    echo -e "${YELLOW}Building backend...${NC}"
    docker build -t ${DOCKERHUB_USERNAME}/${BACKEND_IMAGE}:latest ./backend
    
    # Build frontend
    echo -e "${YELLOW}Building frontend...${NC}"
    docker build -t ${DOCKERHUB_USERNAME}/${FRONTEND_IMAGE}:latest ./frontend
    
    print_success "Images built successfully!"
}

build_multiarch() {
    print_header
    echo -e "${BLUE}🏗️  Building Multi-Architecture Docker images...${NC}"
    echo -e "${YELLOW}Platforms: linux/amd64, linux/arm64${NC}"
    
    # Vérifier que buildx est disponible
    if ! docker buildx version > /dev/null 2>&1; then
        print_error "Docker Buildx n'est pas disponible. Veuillez l'installer."
        exit 1
    fi
    
    # Créer ou réutiliser un builder multi-arch
    echo -e "${YELLOW}Configuration du builder multi-arch...${NC}"
    if ! docker buildx inspect multiarch > /dev/null 2>&1; then
        echo -e "${YELLOW}Création du builder 'multiarch'...${NC}"
        docker buildx create --name multiarch --driver docker-container --use
        docker buildx inspect --bootstrap
    else
        echo -e "${YELLOW}Utilisation du builder existant 'multiarch'...${NC}"
        docker buildx use multiarch
    fi
    
    # Build et push backend multi-arch
    # echo -e "${YELLOW}Building backend (multi-arch)...${NC}"
    # docker buildx build \
    #     --platform linux/amd64,linux/arm64 \
    #     -t ${DOCKERHUB_USERNAME}/${BACKEND_IMAGE}:latest \
    #     --push \
    #     ./backend
    
    # Build et push frontend multi-arch
    echo -e "${YELLOW}Building frontend (multi-arch)...${NC}"
    docker buildx build \
        --platform linux/amd64,linux/arm64 \
        -t ${DOCKERHUB_USERNAME}/${FRONTEND_IMAGE}:latest \
        --push \
        ./frontend
    
    print_success "Images multi-architecture built and pushed successfully!"
    echo -e "${GREEN}Images disponibles pour:${NC}"
    echo -e "${GREEN}  • linux/amd64 (PC/Serveurs x86_64)${NC}"
    echo -e "${GREEN}  • linux/arm64 (Raspberry Pi 4/5, Apple Silicon)${NC}"
}

build_arm64_only() {
    print_header
    echo -e "${BLUE}🏗️  Building ARM64 Only Docker images...${NC}"
    echo -e "${YELLOW}Platform: linux/arm64 (Raspberry Pi)${NC}"
    
    # Vérifier que buildx est disponible
    if ! docker buildx version > /dev/null 2>&1; then
        print_error "Docker Buildx n'est pas disponible. Veuillez l'installer."
        exit 1
    fi
    
    # Créer ou réutiliser un builder multi-arch
    echo -e "${YELLOW}Configuration du builder multi-arch...${NC}"
    if ! docker buildx inspect multiarch > /dev/null 2>&1; then
        echo -e "${YELLOW}Création du builder 'multiarch'...${NC}"
        docker buildx create --name multiarch --driver docker-container --use
        docker buildx inspect --bootstrap
    else
        echo -e "${YELLOW}Utilisation du builder existant 'multiarch'...${NC}"
        docker buildx use multiarch
    fi
    
    # Build et push frontend ARM64 uniquement
    echo -e "${YELLOW}Building frontend (ARM64 only)...${NC}"
    docker buildx build \
        --platform linux/arm64 \
        -t ${DOCKERHUB_USERNAME}/${FRONTEND_IMAGE}:arm64 \
        --push \
        ./frontend
    
    # Build et push backend ARM64 uniquement
    echo -e "${YELLOW}Building backend (ARM64 only)...${NC}"
    docker buildx build \
        --platform linux/arm64 \
        -t ${DOCKERHUB_USERNAME}/${BACKEND_IMAGE}:arm64 \
        --push \
        ./backend
    
    print_success "Images ARM64 built and pushed successfully!"
    echo -e "${GREEN}Images ARM64 disponibles avec le tag :arm64${NC}"
}

push_images() {
    echo -e "${BLUE}📤 Pushing images to DockerHub...${NC}"
    
    # Push backend
    echo -e "${YELLOW}Pushing backend...${NC}"
    docker push ${DOCKERHUB_USERNAME}/${BACKEND_IMAGE}:latest
    
    # Push frontend
    echo -e "${YELLOW}Pushing frontend...${NC}"
    docker push ${DOCKERHUB_USERNAME}/${FRONTEND_IMAGE}:latest
    
    print_success "Images pushed successfully!"
}

deploy_local() {
    echo -e "${BLUE}🏠 Deploying locally...${NC}"
    
    # Stop existing containers
    docker-compose down 2>/dev/null || true
    
    # Start new containers
    docker-compose up -d
    
    # Wait a bit
    sleep 5
    
    # Check status
    docker-compose ps
    
    print_success "Local deployment completed!"
    echo -e "${GREEN}Frontend: http://localhost${NC}"
    echo -e "${GREEN}Backend:  http://localhost:3001${NC}"
}

deploy_production() {
    echo -e "${BLUE}🍓 Deploying to production...${NC}"
    
    # Stop existing containers
    docker-compose -f docker-compose.prod.yml down 2>/dev/null || true
    
    # Pull latest images
    docker pull ${DOCKERHUB_USERNAME}/${BACKEND_IMAGE}:latest
    docker pull ${DOCKERHUB_USERNAME}/${FRONTEND_IMAGE}:latest
    
    # Start new containers
    DOCKERHUB_USERNAME=${DOCKERHUB_USERNAME} docker-compose -f docker-compose.prod.yml up -d
    
    # Wait a bit
    sleep 10
    
    # Check status
    docker-compose -f docker-compose.prod.yml ps
    
    print_success "Production deployment completed!"
}

check_status() {
    echo -e "${BLUE}📊 Checking application status...${NC}"
    
    # Check if containers are running
    if docker-compose ps | grep -q "Up"; then
        print_success "Containers are running"
        
        # Test backend health
        if curl -f -s http://localhost:3001/health > /dev/null; then
            print_success "Backend is healthy"
        else
            print_warning "Backend health check failed"
        fi
        
        # Test frontend
        if curl -f -s http://localhost > /dev/null; then
            print_success "Frontend is accessible"
        else
            print_warning "Frontend accessibility check failed"
        fi
        
        # Show logs tail
        echo -e "${BLUE}📋 Recent logs:${NC}"
        docker-compose logs --tail=10
    else
        print_error "No containers are running"
    fi
}

show_logs() {
    echo -e "${BLUE}📋 Showing application logs...${NC}"
    docker-compose logs -f
}

cleanup() {
    echo -e "${BLUE}🧹 Cleaning up...${NC}"
    
    # Stop containers
    docker-compose down 2>/dev/null || true
    docker-compose -f docker-compose.prod.yml down 2>/dev/null || true
    
    # Remove unused images
    docker image prune -f
    
    print_success "Cleanup completed!"
}

show_help() {
    print_header
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  build     - Build Docker images locally"
    echo "  multiarch - Build and push multi-architecture images (AMD64 + ARM64)"
    echo "  arm64     - Build and push ARM64 only images (Raspberry Pi)"
    echo "  push      - Push images to DockerHub"
    echo "  deploy    - Deploy locally (development)"
    echo "  prod      - Deploy production version"
    echo "  status    - Check application status"
    echo "  logs      - Show live logs"
    echo "  cleanup   - Stop containers and cleanup"
    echo "  help      - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 build && $0 push     # Build and push to DockerHub"
    echo "  $0 multiarch            # Build and push multi-arch (Raspberry Pi compatible)"
    echo "  $0 arm64                # Build ARM64 only (plus rapide pour Raspberry Pi)"
    echo "  $0 deploy               # Deploy locally"
    echo "  $0 prod                 # Deploy production"
    echo ""
}

# Main script logic
case "${1:-help}" in
    "build")
        build_images
        ;;
    "multiarch")
        build_multiarch
        ;;
    "arm64")
        build_arm64_only
        ;;
    "push")
        push_images
        ;;
    "deploy")
        deploy_local
        ;;
    "prod")
        deploy_production
        ;;
    "status")
        check_status
        ;;
    "logs")
        show_logs
        ;;
    "cleanup")
        cleanup
        ;;
    "help"|*)
        show_help
        ;;
esac