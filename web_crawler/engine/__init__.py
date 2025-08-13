"""
Web Crawler Engine Package
Core crawling engine, background processing, and intelligent learning
"""

from .web_crawler_engine import WebCrawler, CrawlConfig, LearningBit, BackgroundCrawlerManager

__all__ = [
    "WebCrawler",
    "CrawlConfig", 
    "LearningBit",
    "BackgroundCrawlerManager"
]
