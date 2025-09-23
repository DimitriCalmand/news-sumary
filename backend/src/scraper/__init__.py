"""
Scraper package for News Summary Backend
Contains all scraping functionality organized by source
"""

from .scraping_service import ScrapingService, start_scraper, stop_scraper
from .techcrunch_scraper import TechCrunchScraper
from .france_info_scraper import FranceInfoScraper

__all__ = [
    'TechCrunchScraper',
    'FranceInfoScraper',
    'ScrapingService',
    'start_scraper',
    'stop_scraper'
]