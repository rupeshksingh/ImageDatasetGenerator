# Image Dataset Builder 🖼️

An advanced web scraping pipeline that builds custom image datasets with AI-powered captioning and context extraction. This tool allows you to create high-quality image datasets from web content based on your specific prompts.

## 🌟 Features

- **Smart Domain Analysis**: Automatically analyzes your prompt to identify relevant domains and generate optimal search queries
- **Concurrent Web Scraping**: Efficiently scrapes images and context from multiple sources simultaneously
- **AI-Powered Captioning**: Generates relevant captions based on image context and source content
- **Context Extraction**: Extracts and preserves relevant context from source webpages
- **Beautiful Streamlit UI**: User-friendly interface for dataset creation and visualization
- **Robust Error Handling**: Comprehensive error handling and logging system
- **Type Safety**: Fully typed with Pydantic models
- **Modular Architecture**: Well-organized, maintainable codebase

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/image-dataset-builder.git
cd image-dataset-builder
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your API keys:
```env
SERP_API_KEY=your_serp_api_key
OPENAI_API_KEY=your_openai_api_key
```

## 📂 Project Structure

```
image_dataset_builder/
├── src/
│   ├── models/
│   │   └── schemas.py         # Pydantic models
│   ├── services/
│   │   ├── prompt_analyzer.py # Prompt analysis service
│   │   ├── web_searcher.py   # Web search service
│   │   ├── content_extractor.py # Content extraction
│   │   ├── image_processor.py   # Image processing
│   │   └── caption_generator.py # Caption generation
│   ├── utils/
│   │   ├── config.py         # Configuration management
│   │   └── logger.py         # Logging setup
│   └── pipeline.py           # Main pipeline
├── app.py                    # Streamlit application
├── requirements.txt          # Project dependencies
└── README.md                # This file
```

## 🚀 Usage

### Using the Streamlit UI

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser and navigate to the provided URL (typically `http://localhost:8501`)

3. Enter your API keys in the sidebar

4. Enter your prompt and click "Build Dataset"

### Using the Python API

```python
from src.utils.config import Settings
from src.pipeline import ImageDatasetPipeline

# Initialize settings
settings = Settings(
    SERP_API_KEY="your_serp_api_key",
    OPENAI_API_KEY="your_openai_api_key",
    MAX_IMAGES_PER_QUERY=10,
    MAX_CONCURRENT_DOWNLOADS=5
)

# Create pipeline
pipeline = ImageDatasetPipeline(settings)

# Build dataset
dataset = pipeline.build_dataset(
    prompt="Show me different types of renewable energy installations"
)

# Access results
print(f"Created dataset with {dataset.metadata.total_images} images")
print(f"Domains covered: {dataset.metadata.domains}")
```

## 📚 API Documentation

### ImageDatasetPipeline

The main pipeline class that orchestrates the dataset creation process.

```python
class ImageDatasetPipeline:
    def __init__(self, settings: Settings):
        """
        Initialize the pipeline with configuration settings.
        
        Args:
            settings (Settings): Configuration settings including API keys
        """
        
    def build_dataset(self, prompt: str) -> ImageDataset:
        """
        Build an image dataset from a prompt.
        
        Args:
            prompt (str): The input prompt describing desired images
            
        Returns:
            ImageDataset: The compiled dataset with metadata
        """
```

### Data Models

```python
class ImageData(BaseModel):
    image_url: HttpUrl
    web_url: HttpUrl
    context: str
    caption: Optional[str]
    domain: str
    local_path: Optional[str]

class ImageDataset(BaseModel):
    metadata: DatasetMetadata
    images: List[ImageData]
```

## ⚙️ Configuration

Configuration is managed through environment variables or a `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| SERP_API_KEY | SerpAPI key for web search | Required |
| OPENAI_API_KEY | OpenAI API key for AI features | Required |
| OUTPUT_DIR | Directory for dataset storage | "dataset" |
| MAX_IMAGES_PER_QUERY | Maximum images per search query | 10 |
| MAX_CONCURRENT_DOWNLOADS | Maximum concurrent downloads | 5 |

## 📝 License

MIT License - see LICENSE file for details

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🐛 Bug Reports & Feature Requests

Please use the [GitHub issue tracker](https://github.com/yourusername/image-dataset-builder/issues) to report bugs or submit feature requests.
