from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional
from datetime import datetime

class DomainInfo(BaseModel):
    domain: str = Field(..., description="Main topic domain")
    search_queries: List[str] = Field(..., description="List of search queries for this domain")

class ListOfDomains(BaseModel):
    domains : List[DomainInfo] = Field(description="List of domains and their search queries")

class ImageData(BaseModel):
    image_url: HttpUrl
    web_url: HttpUrl
    context: str
    caption: Optional[str] = None
    domain: str
    local_path: Optional[str] = None

class DatasetMetadata(BaseModel):
    prompt: str
    timestamp: datetime
    total_images: int
    domains: List[str]

class ImageDataset(BaseModel):
    metadata: DatasetMetadata
    images: List[ImageData]