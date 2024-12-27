import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERP_API_KEY: str
    OPENAI_API_KEY: str
    OUTPUT_DIR: str = "dataset"
    MAX_IMAGES_PER_QUERY: int = 10
    MAX_CONCURRENT_DOWNLOADS: int = 5
    
    class Config:
        env_file = ".env"

settings = Settings()