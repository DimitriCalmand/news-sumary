"""
Scraper module for News Summary Backend
Contains all TechCrunch scraping functionality
"""

import threading
import time
from datetime import datetime
from typing import List, Tuple

import ai as ai
import requests
from bs4 import BeautifulSoup
from config import (DEBUG_LOGGING, PARAGRAPH_CLASS, SCRAPING_INTERVAL,
                    TECHCRUNCH_URL, TITLE_CLASS, FRANCE_INFO_BASE_URL,
                    FRANCE_INFO_POLITIQUE_URL, FRANCE_INFO_CARD_CLASSES,
                    FRANCE_INFO_CONTENT_CLASS, TECHCRUNCH_SOURCE,
                    FRANCE_INFO_SOURCE, REQUIRED_TAGS)
from models import Article, ArticleManager


class TechCrunchScraper:
    """TechCrunch article scraper"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_titles_and_links(self) -> Tuple[List[str], List[str]]:
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
                article = Article(
                    title=title,
                    url=link,
                    content=content,
                    has_been_pretreat=False,
                    tags=["IA"],  # Tag obligatoire pour TechCrunch
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
                    article = Article(
                        title=title,
                        url=link,
                        content=content,
                        has_been_pretreat=False,
                        tags=["politique"],  # Tag obligatoire pour France Info
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


class ScrapingService:
    """Service to manage continuous scraping in a background thread"""
    
    def __init__(self):
        self.techcrunch_scraper = TechCrunchScraper()
        self.france_info_scraper = FranceInfoScraper()
        self.running = False
        self.thread = None
    
    def start(self):
        """Start the background scraping service"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._scraping_loop, daemon=True)
            self.thread.start()
            if DEBUG_LOGGING:
                print("[SCRAPING_SERVICE] Background scraping service started")
    
    def stop(self):
        """Stop the background scraping service"""
        self.running = False
        if DEBUG_LOGGING:
            print("[SCRAPING_SERVICE] Background scraping service stopped")
    
    def _scraping_loop(self):
        """Main scraping loop that runs in background"""
        if DEBUG_LOGGING:
            print("[SCRAPING_SERVICE] Scraping loop started")
        
        while self.running:
            try:
                # Scrape new articles from both sources
                techcrunch_articles = self.techcrunch_scraper.scrape_new_articles()
                france_info_articles = self.france_info_scraper.scrape_new_articles()
                
                # Combine all new articles
                all_new_articles = techcrunch_articles + france_info_articles
                
                # Add them to the database
                if all_new_articles:
                    added_count = ArticleManager.add_new_articles(all_new_articles)
                    if DEBUG_LOGGING:
                        tc_count = len(techcrunch_articles)
                        fi_count = len(france_info_articles)
                        print(f"[SCRAPING_SERVICE] Added {added_count} new articles "
                              f"({tc_count} from TechCrunch, {fi_count} from France Info)")
                else:
                    if DEBUG_LOGGING:
                        print("[SCRAPING_SERVICE] No new articles found")
                
                # Wait before next iteration
                if DEBUG_LOGGING:
                    print(f"[SCRAPING_SERVICE] Waiting {SCRAPING_INTERVAL} seconds before next check...")
                ai.pretreat_articles()
                # Sleep in small chunks to allow for graceful shutdown
                for _ in range(SCRAPING_INTERVAL):
                    if not self.running:
                        break
                    time.sleep(1)

                    
            except Exception as e:
                if DEBUG_LOGGING:
                    print(f"[SCRAPING_SERVICE] Error in scraping loop: {e}")
                # Wait a bit before retrying on error
                time.sleep(60)
        
        if DEBUG_LOGGING:
            print("[SCRAPING_SERVICE] Scraping loop ended")


# Global scraping service instance
scraping_service = ScrapingService()


def start_scraper():
    """Start the background scraping service"""
    scraping_service.start()


def stop_scraper():
    """Stop the background scraping service"""
    scraping_service.stop()