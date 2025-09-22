#!/usr/bin/env python3
"""
Script pour ajouter automatiquement les tags obligatoires aux articles existants
selon leur source (TechCrunch -> 'ia', France Info -> 'politique')
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from models import ArticleManager
from config import get_required_tag_for_source, DEBUG_LOGGING

def add_required_tags_to_existing_articles():
    """Ajoute les tags obligatoires aux articles existants selon leur source"""
    print("=== Ajout des tags obligatoires aux articles existants ===")
    
    # Charger tous les articles
    articles = ArticleManager.load_articles()
    modified_count = 0
    
    for article in articles:
        article_source = article.get("source", "")
        required_tag = get_required_tag_for_source(article_source)
        
        if required_tag:
            current_tags = article.get("tags", [])
            
            # Vérifier si le tag obligatoire est déjà présent
            if required_tag not in current_tags:
                # Ajouter le tag obligatoire
                current_tags.append(required_tag)
                article["tags"] = current_tags
                modified_count += 1
                
                print(f"✅ Article '{article['title'][:50]}...' (source: {article_source})")
                print(f"   Ajouté tag: '{required_tag}' -> Tags: {current_tags}")
            else:
                print(f"⏭️ Article '{article['title'][:50]}...' (source: {article_source})")
                print(f"   Tag '{required_tag}' déjà présent -> Tags: {current_tags}")
        else:
            print(f"❓ Article '{article['title'][:50]}...' (source: {article_source})")
            print(f"   Aucun tag obligatoire défini pour cette source")
    
    # Sauvegarder les modifications
    if modified_count > 0:
        ArticleManager.save_articles(articles)
        print(f"\n🎉 {modified_count} articles modifiés et sauvegardés!")
    else:
        print(f"\n✨ Aucun article à modifier (tous ont déjà leurs tags obligatoires)")
    
    # Statistiques finales
    print(f"\n📊 Statistiques:")
    print(f"   Total articles: {len(articles)}")
    print(f"   Articles modifiés: {modified_count}")
    
    # Compter par source
    sources_count = {}
    for article in articles:
        source = article.get("source", "Unknown")
        sources_count[source] = sources_count.get(source, 0) + 1
    
    print(f"   Répartition par source:")
    for source, count in sources_count.items():
        required_tag = get_required_tag_for_source(source)
        print(f"     {source}: {count} articles (tag: {required_tag})")

if __name__ == "__main__":
    add_required_tags_to_existing_articles()