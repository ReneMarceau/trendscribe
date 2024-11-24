import feedparser
from typing import List, Dict, Any
import logging
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from bs4 import BeautifulSoup
from dataclasses import dataclass

console = Console()

@dataclass
class RSSPost:
    title: str
    link: str
    description: str
    published: str
    author: str

    def __getitem__(self, key):
        return getattr(self, key)

    def to_dict(self):
        return {
            'title': self.title,
            'link': self.link,
            'description': self.description,
            'published': self.published,
            'author': self.author
        }

class RSSHandler:
    def __init__(self, feed_url: str):
        self.feed_url = feed_url

    @staticmethod
    def clean_html(html: str) -> str:
        """Clean HTML using BeautifulSoup"""
        soup = BeautifulSoup(html, 'html.parser')
        return soup.get_text(separator=' ').strip()

    def fetch_posts(self) -> List[RSSPost]:
        """Fetch posts from the RSS feed."""
        try:
            feed = feedparser.parse(self.feed_url)
            if feed.bozo:
                logging.error(f"Feed parsing error: {feed.bozo_exception}")
                return []
            
            return [
                RSSPost(
                    title=self.clean_html(entry.title),
                    link=entry.link,
                    description=self.clean_html(entry.description),
                    published=entry.published,
                    author=self.clean_html(entry.get('author', 'Unknown'))
                )
                for entry in feed.entries
            ]
        except Exception as e:
            logging.error(f"Error fetching RSS feed: {e}")
            return []

    def display_post(self, post: RSSPost):
        """Display a post in a formatted way using Rich."""
        content = Text.assemble(
            Text(post.title, style="bold blue"), "\n\n",
            Text(f"By {post.author}", style="italic"), "\n",
            Text(f"Published: {post.published}", style="dim"), "\n",
            Text(f"Link: {post.link}", style="underline"), "\n\n",
            Text(post.description)
        )
        
        console.print(Panel(
            content,
            title="TechCrunch Article",
            border_style="blue",
            padding=(1, 2)
        ))
