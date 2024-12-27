from serpapi import GoogleSearch
from typing import List
from ratelimit import limits, sleep_and_retry
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class WebSearcher:
    def __init__(self, api_key: str, max_images: int = 10):
        self.api_key = api_key
        self.max_images = max_images
    
    @sleep_and_retry
    @limits(calls=100, period=60)
    def search(self, query: str) -> List[dict]:
        try:
            search = GoogleSearch({
                "q": query,
                "tbm": "isch",
                "api_key": self.api_key
            })
            results = search.get_dict()
            return results.get("images_results", [])[:self.max_images]
        except Exception as e:
            logger.error(f"Error in image search: {str(e)}")
            raise
