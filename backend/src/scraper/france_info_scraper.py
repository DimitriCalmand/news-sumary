"""
France Info scraper module for News Summary Backend
Contains France Info article scraping functionality
"""

import time
from datetime import datetime
from typing import List, Tuple

import requests
from bs4 import BeautifulSoup

from config import (DEBUG_LOGGING, FRANCE_INFO_BASE_URL,
                    FRANCE_INFO_CARD_CLASSES, FRANCE_INFO_CONTENT_CLASS,
                    FRANCE_INFO_POLITIQUE_URL, FRANCE_INFO_SOURCE,
                    get_required_tag_for_source)
from models import Article, ArticleManager


class FranceInfoScraper:
    """France Info article scraper"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def get_article_links(self) -> List[str]:
        """Récupère toutes les URLs d'articles depuis la page politique"""
        try:
            response = self.session.get(FRANCE_INFO_POLITIQUE_URL, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            urls = []

            for class_name in FRANCE_INFO_CARD_CLASSES:
                for link in soup.find_all("a", class_=class_name):
                    href = link.get("href")
                    if href:
                        if href.startswith("http"):
                            urls.append(href)
                        else:
                            urls.append(FRANCE_INFO_BASE_URL + href)

            # Remove duplicates
            urls = list(set(urls))

            if DEBUG_LOGGING:
                print(f"[FRANCE_INFO_SCRAPER] Found {len(urls)} article links")

            return urls

        except requests.exceptions.RequestException as e:
            if DEBUG_LOGGING:
                print(f"[FRANCE_INFO_SCRAPER] HTTP request error: {e}")
            return []
        except Exception as e:
            if DEBUG_LOGGING:
                print(f"[FRANCE_INFO_SCRAPER] Unexpected error in get_article_links: {e}")
            return []

    def get_article_content(self, url: str) -> Tuple[str, str]:
        """Récupère le titre et le contenu d'un article"""
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # Get title
            title = ""
            title_element = soup.find("h1")
            if title_element:
                title = title_element.get_text(strip=True)

            # Get content
            content_blocks = soup.find_all("div", class_=FRANCE_INFO_CONTENT_CLASS)
            content = "\n".join(block.get_text(strip=True, separator=" ") for block in content_blocks)

            if not content:
                # Fallback: try to get paragraphs
                paragraphs = soup.find_all('p')
                content_parts = []
                for para in paragraphs:
                    text = para.text.strip()
                    if text and len(text) > 20:
                        content_parts.append(text)
                content = "\n".join(content_parts)

            if DEBUG_LOGGING:
                print(f"[FRANCE_INFO_SCRAPER] Scraped article: {title[:50]}...")

            return title, content

        except requests.exceptions.RequestException as e:
            if DEBUG_LOGGING:
                print(f"[FRANCE_INFO_SCRAPER] HTTP request error for {url}: {e}")
            return "", f"Error fetching article content: {str(e)}"
        except Exception as e:
            if DEBUG_LOGGING:
                print(f"[FRANCE_INFO_SCRAPER] Unexpected error scraping {url}: {e}")
            return "", f"Error processing article content: {str(e)}"

    def scrape_new_articles(self) -> List[Article]:
        """Scrape new articles and return them as Article objects"""
        if DEBUG_LOGGING:
            print("[FRANCE_INFO_SCRAPER] Starting to scrape new articles...")

        # Get existing articles to avoid duplicates
        existing_articles = ArticleManager.load_articles()
        existing_titles = {a["title"] for a in existing_articles}
        existing_urls = {a["url"] for a in existing_articles}

        # Get article links
        article_links = self.get_article_links()

        new_articles = []
        for link in article_links:
            if link not in existing_urls:
                if DEBUG_LOGGING:
                    print(f"[FRANCE_INFO_SCRAPER] Scraping new article: {link}")

                title, content = self.get_article_content(link)

                if title and title not in existing_titles and content:
                    required_tag = get_required_tag_for_source(FRANCE_INFO_SOURCE)
                    article = Article(
                        title=title,
                        url=link,
                        content=content,
                        has_been_pretreat=False,
                        tags=[required_tag] if required_tag else [],  # Tag obligatoire pour France Info
                        source=FRANCE_INFO_SOURCE,
                        scraped_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    )
                    new_articles.append(article)
                    existing_titles.add(title)
                    existing_urls.add(link)

                # Add small delay between requests to be respectful
                time.sleep(1)

        if DEBUG_LOGGING:
            print(f"[FRANCE_INFO_SCRAPER] Found {len(new_articles)} new articles")

        return new_articles