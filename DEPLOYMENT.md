# 🚀 Configuration du Déploiement Automatique

Ce projet utilise GitHub Actions pour automatiquement construire et déployer l'application sur votre Raspberry Pi.

## 📋 Secrets GitHub Requis

Allez dans **Settings** > **Secrets and variables** > **Actions** de votre repository GitHub et ajoutez ces secrets :

### 🐳 DockerHub
- `DOCKERHUB_USERNAME` : Votre nom d'utilisateur DockerHub
- `DOCKERHUB_TOKEN` : Token d'accès DockerHub (généré dans DockerHub > Account Settings > Security)

### 🔐 Raspberry Pi SSH
- `RASPI_HOST` : Adresse IP de votre Raspberry Pi (ex: `192.168.1.100`)
- `RASPI_USERNAME` : Nom d'utilisateur SSH (généralement `pi`)
- `RASPI_SSH_KEY` : Clé privée SSH (voir section génération ci-dessous)
- `RASPI_PORT` : Port SSH (généralement `22`)

## 🔑 Génération de la Clé SSH

Sur votre machine locale, générez une paire de clés SSH :

```bash
# Générer une nouvelle clé SSH
ssh-keygen -t rsa -b 4096 -C "github-actions@news-summary"

# Copier la clé publique sur votre Raspberry Pi
ssh-copy-id -i ~/.ssh/id_rsa.pub pi@VOTRE_IP_RASPI
```

Ensuite :
1. **Copiez le contenu de la clé privée** (`~/.ssh/id_rsa`) dans le secret `RASPI_SSH_KEY`
2. **Testez la connexion** : `ssh pi@VOTRE_IP_RASPI`

## 🛠️ Préparation du Raspberry Pi

Sur votre Raspberry Pi, installez Docker et Docker Compose :

```bash
# Installer Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker pi

# Installer Docker Compose
sudo pip3 install docker-compose

# Redémarrer pour appliquer les changements de groupe
sudo reboot
```

## 🚀 Déploiement

Le déploiement se déclenche automatiquement :
- ✅ **Sur chaque push** vers la branche `main`
- ✅ **Manuellement** via l'onglet "Actions" de GitHub

### Processus de déploiement :
1. **Build** des images Docker (ARM64 + AMD64)
2. **Push** vers DockerHub
3. **Connexion SSH** au Raspberry Pi
4. **Téléchargement** du nouveau docker-compose.prod.yml
5. **Mise à jour** des conteneurs
6. **Vérification** du bon fonctionnement

## 📊 Monitoring

Après déploiement, vous pouvez surveiller votre application :

```bash
# Sur votre Raspberry Pi
cd ~/news-summary

# Voir les logs
docker-compose -f docker-compose.prod.yml logs -f

# Vérifier l'état des services
docker-compose -f docker-compose.prod.yml ps

# Redémarrer un service
docker-compose -f docker-compose.prod.yml restart frontend
```

## 🌐 Accès

Une fois déployé, votre application sera accessible :
- **Frontend** : http://VOTRE_IP_RASPI
- **Backend API** : http://VOTRE_IP_RASPI:3001

## 🔧 Variables d'Environnement

Vous pouvez personnaliser le déploiement en créant un fichier `.env` sur votre Raspberry Pi :

```bash
# ~/news-summary/.env
DOCKERHUB_USERNAME=votre-username-dockerhub
```

## ⚠️ Dépannage

### Erreur de connexion SSH
- Vérifiez que SSH est activé sur votre Raspberry Pi
- Testez la connexion manuellement : `ssh pi@VOTRE_IP_RASPI`

### Images non trouvées
- Vérifiez que `DOCKERHUB_USERNAME` est correct
- Assurez-vous que les images sont publiques sur DockerHub

### Erreur de mémoire
- Le Raspberry Pi a des ressources limitées
- Les limites sont configurées dans `docker-compose.prod.yml`