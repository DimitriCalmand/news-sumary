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
DOCKERHUB_USERNAME=${DOCKERHUB_USERNAME:-"dimitricalmand"}
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
    echo "  $0 deploy               # Deploy locally"
    echo "  $0 prod                 # Deploy production"
    echo ""
}

# Main script logic
case "${1:-help}" in
    "build")
        build_images
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