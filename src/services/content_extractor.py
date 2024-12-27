import requests
from bs4 import BeautifulSoup
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class ContentExtractor:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def extract_context(self, url: str) -> str:
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            relevant_tags = soup.find_all(['h1', 'h2', 'p'])
            context = ' '.join(tag.get_text().strip() for tag in relevant_tags)
            
            return context[:1000]
        except Exception as e:
            logger.error(f"Error extracting context: {str(e)}")
            return ""