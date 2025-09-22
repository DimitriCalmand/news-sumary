import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://www.franceinfo.fr"
URL = BASE_URL + "/politique/"

def get_article_links(url):
    """Récupère toutes les URLs d'articles depuis la page politique"""
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Erreur {response.status_code} sur {url}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    classes = ["card-article-m__link", "card-article-majeure__link"]

    urls = []
    for class_name in classes:
        for link in soup.find_all("a", class_=class_name):
            href = link.get("href")
            if href:
                if href.startswith("http"):
                    urls.append(href)
                else:
                    urls.append(BASE_URL + href)
    return list(set(urls))


def get_article_content(url):
    """Récupère le texte contenu dans les balises c-body d'un article"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"Erreur {response.status_code} sur {url}")
            return ""

        soup = BeautifulSoup(response.text, "html.parser")
        content_blocks = soup.find_all("div", class_="c-body")
        
        # Concatène le texte de tous les blocs trouvés
        text = "\n".join(block.get_text(strip=True, separator=" ") for block in content_blocks)
        return text

    except requests.exceptions.RequestException as e:
        print(f"Erreur requête {e} sur {url}")
        return ""


if __name__ == "__main__":
    article_links = get_article_links(URL)
    print(f"{len(article_links)} articles trouvés.\n")

    for link in article_links:
        print(f"--- {link} ---")
        content = get_article_content(link)
        print(content[:500], "...\n")  # affiche seulement les 500 premiers caractères
        time.sleep(1)  # petite pause pour éviter de surcharger le site
