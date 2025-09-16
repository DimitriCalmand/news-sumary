import requests
from bs4 import BeautifulSoup
import json
import time
import os
import threading
from flask import Flask, jsonify

JSON_FILE = "./data/articles_seen.json"
app = Flask(__name__)
articles_cache = []  # Cache en mémoire pour les articles

def get_title_and_links():
    url = "https://techcrunch.com/category/artificial-intelligence/"
    classe_des_titres = "loop-card__title"
    titres = []
    liens = []
    try:
        reponse = requests.get(url)
        reponse.raise_for_status()
        soup = BeautifulSoup(reponse.text, 'html.parser')
        titres_et_liens = soup.find_all(class_=classe_des_titres)
        if titres_et_liens:
            for element in titres_et_liens:
                lien = element.find('a')
                if lien and 'href' in lien.attrs:
                    titre_texte = element.text.strip()
                    lien_href = lien['href']
                    titres.append(titre_texte)
                    liens.append(lien_href)
            return titres, liens
        else:
            return [], []
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête HTTP: {e}")
        return [], []

def get_article_content(url):
    classe_paragraphe = "wp-block-paragraph"
    res = ""
    try:
        reponse = requests.get(url)
        reponse.raise_for_status()
        soup = BeautifulSoup(reponse.text, 'html.parser')
        paragraphes = soup.find_all('p', class_=classe_paragraphe)
        if paragraphes:
            for para in paragraphes:
                res += para.text.strip() + "\n"
                res += "-" * 20 + "\n"
        else:
            res += f"Aucun paragraphe avec la classe '{classe_paragraphe}' n'a été trouvé sur cette page."
        return res
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête HTTP : {e}")
        return f"Erreur lors de la requête HTTP : {e}"

def load_seen_articles():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except Exception:
                return []
    return []

def save_seen_articles(articles):
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

def scraper_loop():
    global articles_cache
    print("Démarrage du thread de scraping...")
    while True:
        seen_articles = load_seen_articles()
        seen_titles = {a["title"] for a in seen_articles}
        titres, liens = get_title_and_links()
        new_articles = []
        for titre, lien in zip(titres, liens):
            if titre not in seen_titles:
                contenu = get_article_content(lien)
                article = {
                    "title": titre,
                    "url": lien,
                    "content": contenu
                }
                seen_articles.append(article)
                new_articles.append(article)
        
        if new_articles:
            print(f"{len(new_articles)} nouvel(s) article(s) trouvé(s) et ajouté(s) au fichier JSON.")
            save_seen_articles(seen_articles)
        else:
            print("Aucun nouvel article trouvé.")
        
        # Mettre à jour le cache en mémoire pour l'API
        articles_cache = seen_articles
        
        print("Attente de 30 minutes avant la prochaine vérification...")
        time.sleep(1800)

@app.route('/api/articles', methods=['GET'])
def get_articles():
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        articles = json.load(f)
    return jsonify(articles)

def start_scraper():
    scraper_thread = threading.Thread(target=scraper_loop, daemon=True)
    scraper_thread.start()

if __name__ == "__main__":
    start_scraper()
    articles_cache = load_seen_articles()
    app.run(host='0.0.0.0', port=8000)