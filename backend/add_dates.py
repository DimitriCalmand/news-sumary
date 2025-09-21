#!/usr/bin/env python3
"""
Script pour ajouter des dates aux articles existants
"""

import json
import os
import re
from datetime import datetime, timedelta


def extract_date_from_url(url):
    """Essaie d'extraire une date depuis l'URL"""
    # Pattern pour TechCrunch: /2025/09/21/article-title
    date_pattern = r'/(\d{4})/(\d{2})/(\d{2})/'
    match = re.search(date_pattern, url)
    if match:
        year, month, day = match.groups()
        try:
            return f"{year}-{month}-{day}"
        except:
            pass
    return None

def add_dates_to_articles():
    """Ajoute des dates aux articles du fichier JSON"""
    
    # Chemin vers le fichier des articles
    articles_file = os.path.join(os.path.dirname(__file__), 'data', 'articles_seen.json')
    
    if not os.path.exists(articles_file):
        print(f"Fichier {articles_file} non trouvé")
        return
    
    # Charger les articles
    with open(articles_file, 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    print(f"Traitement de {len(articles)} articles...")
    
    # Date de base (aujourd'hui moins le nombre d'articles en jours)
    base_date = datetime.now() - timedelta(days=len(articles))
    
    articles_updated = 0
    
    for i, article in enumerate(articles):
        if 'date' not in article or not article['date']:
            # Essayer d'extraire la date depuis l'URL
            extracted_date = extract_date_from_url(article.get('url', ''))
            
            if extracted_date:
                article['date'] = extracted_date
                articles_updated += 1
                print(f"Date extraite pour article {article.get('id', i)}: {extracted_date}")
            else:
                # Utiliser une date basée sur l'ordre d'arrivée
                estimated_date = (base_date + timedelta(days=i)).strftime('%Y-%m-%d')
                article['date'] = estimated_date
                articles_updated += 1
                print(f"Date estimée pour article {article.get('id', i)}: {estimated_date}")
    
    # Sauvegarder les articles mis à jour
    with open(articles_file, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ {articles_updated} articles mis à jour avec des dates")
    print(f"Fichier sauvegardé: {articles_file}")

if __name__ == "__main__":
    add_dates_to_articles()