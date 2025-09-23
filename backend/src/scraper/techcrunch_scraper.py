"""
TechCrunch scraper module for News Summary Backend
Contains TechCrunch article scraping functionality
"""

import time
from datetime import datetime
from typing import List

import requests
from bs4 import BeautifulSoup

from config import (DEBUG_LOGGING, PARAGRAPH_CLASS, TAG_CATEGORIES, TECHCRUNCH_SOURCE,
                    TECHCRUNCH_URL, TITLE_CLASS)
from models import Article, ArticleManager


class TechCrunchScraper:
    """TechCrunch article scraper"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def get_titles_and_links(self) -> tuple[List[str], List[str]]:
        """Scrape article titles and links from TechCrunch AI category"""
        titles = []
        links = []

        try:
            response = self.session.get(TECHCRUNCH_URL, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            title_elements = soup.find_all(class_=TITLE_CLASS)

            if not title_elements:
                if DEBUG_LOGGING:
                    print(f"[SCRAPER] No elements found with class '{TITLE_CLASS}'")
                return [], []

            for element in title_elements:
                link_element = element.find('a')
                if link_element and 'href' in link_element.attrs:
                    title_text = element.text.strip()
                    link_href = link_element['href']
                    if title_text and link_href:
                        titles.append(title_text)
                        links.append(link_href)

            if DEBUG_LOGGING:
                print(f"[SCRAPER] Found {len(titles)} articles from TechCrunch")

            return titles, links

        except requests.exceptions.RequestException as e:
            if DEBUG_LOGGING:
                print(f"[SCRAPER] HTTP request error: {e}")
            return [], []
        except Exception as e:
            if DEBUG_LOGGING:
                print(f"[SCRAPER] Unexpected error in get_titles_and_links: {e}")
            return [], []

    def get_article_content(self, url: str) -> str:
        """Scrape the content of a specific article"""
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs = soup.find_all('p', class_=PARAGRAPH_CLASS)

            if not paragraphs:
                # Fallback: try to get any paragraphs
                paragraphs = soup.find_all('p')
                if DEBUG_LOGGING:
                    print(f"[SCRAPER] No paragraphs with class '{PARAGRAPH_CLASS}' found, using fallback")

            content_parts = []
            for para in paragraphs:
                text = para.text.strip()
                if text and len(text) > 20:  # Filter out very short paragraphs
                    content_parts.append(text)

            if content_parts:
                content = "\n".join(content_parts)
                if DEBUG_LOGGING:
                    print(f"[SCRAPER] Scraped {len(content_parts)} paragraphs from {url}")
                return content
            else:
                return f"No substantial content found for this article: {url}"

        except requests.exceptions.RequestException as e:
            if DEBUG_LOGGING:
                print(f"[SCRAPER] HTTP request error for {url}: {e}")
            return f"Error fetching article content: {str(e)}"
        except Exception as e:
            if DEBUG_LOGGING:
                print(f"[SCRAPER] Unexpected error scraping {url}: {e}")
            return f"Error processing article content: {str(e)}"

    def scrape_new_articles(self) -> List[Article]:
        """Scrape new articles and return them as Article objects"""
        if DEBUG_LOGGING:
            print("[SCRAPER] Starting to scrape new articles...")

        # Get existing articles to avoid duplicates
        existing_articles = ArticleManager.load_articles()
        existing_titles = {a["title"] for a in existing_articles}
        existing_urls = {a["url"] for a in existing_articles}

        # Get titles and links from TechCrunch
        titles, links = self.get_titles_and_links()

        new_articles = []
        for title, link in zip(titles, links):
            if title not in existing_titles and link not in existing_urls:
                if DEBUG_LOGGING:
                    print(f"[SCRAPER] Scraping new article: {title}")

                content = self.get_article_content(link)
                required_tag = TAG_CATEGORIES["ia"]["main_tag"]
                article = Article(
                    title=title,
                    url=link,
                    content=content,
                    has_been_pretreat=False,
                    tags=[required_tag] if required_tag else [],  # Tag obligatoire pour TechCrunch
                    source=TECHCRUNCH_SOURCE,
                    scraped_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
                new_articles.append(article)
                existing_titles.add(title)
                existing_urls.add(link)

                # Add small delay between requests to be respectful
                time.sleep(1)

        if DEBUG_LOGGING:
            print(f"[SCRAPER] Found {len(new_articles)} new articles")

        return new_articles