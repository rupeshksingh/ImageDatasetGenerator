import os
import hashlib
import requests
from PIL import Image
from io import BytesIO
from typing import Optional
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class ImageProcessor:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(os.path.join(output_dir, "images"), exist_ok=True)
    
    def download_and_save(self, image_url: str) -> Optional[str]:
        try:
            response = requests.get(image_url, timeout=10)
            img = Image.open(BytesIO(response.content))
            
            filename = hashlib.md5(image_url.encode()).hexdigest() + ".jpg"
            local_path = os.path.join(self.output_dir, "images", filename)
            
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            img.save(local_path, "JPEG")
            
            return local_path
        except Exception as e:
            logger.error(f"Error processing image: {str(e)}")
            return None