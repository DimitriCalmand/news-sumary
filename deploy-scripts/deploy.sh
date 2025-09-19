#!/bin/bash

# Script de déploiement pour Raspberry Pi
# Ce script doit être exécuté sur le Raspberry Pi

set -e

# Configuration
PROJECT_DIR="$HOME/news-summary"
DOCKER_COMPOSE_FILE="docker-compose.yml"
BACKUP_DIR="$HOME/news-summary-backups"

# Couleurs pour les logs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Fonction de backup
backup_data() {
    log_info "Création du backup des données..."
    
    mkdir -p "$BACKUP_DIR"
    BACKUP_NAME="backup-$(date +%Y%m%d-%H%M%S)"
    
    if [ -d "$PROJECT_DIR/backend/data" ]; then
        cp -r "$PROJECT_DIR/backend/data" "$BACKUP_DIR/$BACKUP_NAME"
        log_info "Backup créé: $BACKUP_DIR/$BACKUP_NAME"
    else
        log_warn "Aucune donnée à sauvegarder"
    fi
}

# Fonction de vérification des prérequis
check_prerequisites() {
    log_info "Vérification des prérequis..."
    
    # Vérifier Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker n'est pas installé"
        exit 1
    fi
    
    # Vérifier Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose n'est pas installé"
        exit 1
    fi
    
    # Vérifier l'espace disque (minimum 2GB)
    AVAILABLE_SPACE=$(df / | awk 'NR==2 {print $4}')
    MIN_SPACE=2000000  # 2GB en KB
    
    if [ "$AVAILABLE_SPACE" -lt "$MIN_SPACE" ]; then
        log_error "Espace disque insuffisant. Minimum requis: 2GB"
        exit 1
    fi
    
    log_info "Prérequis validés"
}

# Fonction de nettoyage
cleanup() {
    log_info "Nettoyage des ressources..."
    
    # Supprimer les images non utilisées
    docker image prune -f
    
    # Supprimer les volumes non utilisés
    docker volume prune -f
    
    # Garder seulement les 5 derniers backups
    if [ -d "$BACKUP_DIR" ]; then
        cd "$BACKUP_DIR"
        ls -1t | tail -n +6 | xargs -r rm -rf
    fi
    
    log_info "Nettoyage terminé"
}

# Fonction de monitoring de santé
health_check() {
    log_info "Vérification de la santé des services..."
    
    # Attendre que les services démarrent
    sleep 30
    
    # Vérifier le backend
    if curl -f http://localhost:3001/api/length > /dev/null 2>&1; then
        log_info "✓ Backend accessible"
    else
        log_error "✗ Backend non accessible"
        return 1
    fi
    
    # Vérifier le frontend
    if curl -f http://localhost/health > /dev/null 2>&1; then
        log_info "✓ Frontend accessible"
    else
        log_error "✗ Frontend non accessible"
        return 1
    fi
    
    log_info "Tous les services sont opérationnels"
}

# Fonction principale de déploiement
deploy() {
    log_info "Début du déploiement..."
    
    cd "$PROJECT_DIR"
    
    # Créer un backup avant le déploiement
    backup_data
    
    # Arrêter les services existants
    log_info "Arrêt des services existants..."
    docker-compose down || true
    
    # Tirer les nouvelles images
    log_info "Téléchargement des nouvelles images..."
    docker-compose pull
    
    # Démarrer les nouveaux services
    log_info "Démarrage des nouveaux services..."
    docker-compose up -d
    
    # Vérifier la santé des services
    if health_check; then
        log_info "✅ Déploiement réussi!"
        
        # Envoyer notification de succès
        if command -v curl &> /dev/null; then
            curl -X POST -H 'Content-type: application/json' \
                --data '{"text":"🚀 Déploiement réussi sur Raspberry Pi"}' \
                "$SLACK_WEBHOOK_URL" 2>/dev/null || true
        fi
    else
        log_error "❌ Déploiement échoué - Rollback en cours..."
        
        # Rollback en cas d'échec
        docker-compose down
        
        # Restaurer le backup le plus récent si disponible
        LATEST_BACKUP=$(ls -1t "$BACKUP_DIR" 2>/dev/null | head -n1)
        if [ -n "$LATEST_BACKUP" ]; then
            log_info "Restauration du backup: $LATEST_BACKUP"
            rm -rf "$PROJECT_DIR/backend/data"
            cp -r "$BACKUP_DIR/$LATEST_BACKUP" "$PROJECT_DIR/backend/data"
        fi
        
        exit 1
    fi
}

# Fonction d'installation initiale
install() {
    log_info "Installation initiale du projet..."
    
    # Créer les répertoires nécessaires
    mkdir -p "$PROJECT_DIR/backend/data"
    mkdir -p "$BACKUP_DIR"
    
    # Créer les fichiers de configuration de base
    cat > "$PROJECT_DIR/.env" << EOF
# Configuration de production
NODE_ENV=production
FLASK_ENV=production
PORT=3001

# Monitoring
ENABLE_MONITORING=true

# Logs
LOG_LEVEL=info
EOF
    
    log_info "Installation terminée"
}

# Fonction de monitoring des logs
logs() {
    log_info "Affichage des logs..."
    cd "$PROJECT_DIR"
    docker-compose logs -f --tail=100
}

# Fonction de status
status() {
    log_info "Statut des services:"
    cd "$PROJECT_DIR"
    docker-compose ps
    
    log_info "Utilisation des ressources:"
    docker stats --no-stream
}

# Menu principal
case "$1" in
    "install")
        check_prerequisites
        install
        ;;
    "deploy")
        check_prerequisites
        deploy
        cleanup
        ;;
    "backup")
        backup_data
        ;;
    "logs")
        logs
        ;;
    "status")
        status
        ;;
    "cleanup")
        cleanup
        ;;
    "health")
        health_check
        ;;
    *)
        echo "Usage: $0 {install|deploy|backup|logs|status|cleanup|health}"
        echo ""
        echo "Commands:"
        echo "  install  - Installation initiale"
        echo "  deploy   - Déploiement complet"
        echo "  backup   - Sauvegarde des données"
        echo "  logs     - Affichage des logs"
        echo "  status   - Statut des services"
        echo "  cleanup  - Nettoyage des ressources"
        echo "  health   - Vérification de santé"
        exit 1
        ;;
esac