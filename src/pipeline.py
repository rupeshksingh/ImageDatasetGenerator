from concurrent.futures import ThreadPoolExecutor
import json
from datetime import datetime
from typing import Optional
from .models.schemas import ImageData, ImageDataset, DatasetMetadata
from .services.prompt_analyzer import PromptAnalyzer
from .services.web_searcher import WebSearcher
from .services.content_extractor import ContentExtractor
from .services.image_processor import ImageProcessor
from .services.caption_generator import CaptionGenerator
from .utils.logger import setup_logger
import os

logger = setup_logger(__name__)

class ImageDatasetPipeline:
    def __init__(self, settings):
        self.settings = settings
        self.prompt_analyzer = PromptAnalyzer(settings.OPENAI_API_KEY)
        self.web_searcher = WebSearcher(settings.SERP_API_KEY, settings.MAX_IMAGES_PER_QUERY)
        self.content_extractor = ContentExtractor()
        self.image_processor = ImageProcessor(settings.OUTPUT_DIR)
        self.caption_generator = CaptionGenerator(settings.OPENAI_API_KEY)
    
    def process_image(self, image_result: dict, domain: str) -> Optional[ImageData]:
        try:
            context = self.content_extractor.extract_context(image_result["link"])
            
            image_data = ImageData(
                image_url=image_result["original"],
                web_url=image_result["link"],
                context=context,
                domain=domain,
                caption=None
            )
            
            local_path = self.image_processor.download_and_save(str(image_data.image_url))
            if not local_path:
                return None
                
            image_data.local_path = local_path
            image_data.caption = self.caption_generator.generate(
                str(image_data.image_url),
                image_data.context
            )
            
            return image_data
        except Exception as e:
            logger.error(f"Error processing image: {str(e)}")
            return None
    
    def build_dataset(self, prompt: str) -> ImageDataset:
        domains = self.prompt_analyzer.analyze(prompt)
        
        all_images = []
        for domain_info in domains:
            for query in domain_info['search_queries']:
                image_results = self.web_searcher.search(query)
                
                with ThreadPoolExecutor(max_workers=self.settings.MAX_CONCURRENT_DOWNLOADS) as executor:
                    futures = [
                        executor.submit(self.process_image, img_result, domain_info['domain'])
                        for img_result in image_results
                    ]
                    
                    for future in futures:
                        if image_data := future.result():
                            all_images.append(image_data)
        
        dataset = ImageDataset(
            metadata=DatasetMetadata(
                prompt=prompt,
                timestamp=datetime.now(),
                total_images=len(all_images),
                domains=[d['domain'] for d in domains]
            ),
            images=all_images
        )
        
        self._save_metadata(dataset)
        return dataset
    
    def _save_metadata(self, dataset: ImageDataset):
        metadata_path = os.path.join(self.settings.OUTPUT_DIR, "metadata.json")
        with open(metadata_path, "w") as f:
            json.dump(dataset.model_dump(), f, default=str, indent=2)