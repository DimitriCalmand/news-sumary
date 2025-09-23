"""
Scraping service module for News Summary Backend
Contains the background scraping service and global functions
"""

import threading
import time

import ai as ai

from config import DEBUG_LOGGING, SCRAPING_INTERVAL
from models import ArticleManager

from .france_info_scraper import FranceInfoScraper
from .techcrunch_scraper import TechCrunchScraper


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