from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import base64
import httpx
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class CaptionGenerator:
    def __init__(self, openai_api_key: str):
        self.llm = ChatOpenAI(api_key=openai_api_key, model="chatgpt-4o-latest")
    
    def generate(self, image_url: str, context: str) -> str:
        image_data = base64.b64encode(httpx.get(image_url).content).decode("utf-8")
        prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Generate a relevant caption for an image based on its context. Context: {context}"),
            (
                "user",
                [
                {
                    "type": "image_url",
                    "image_url": {"url": "data:image/jpeg;base64,{image_data}"},
                },
                {
                    "type": "text",
                    "text": "Generate a concise and descriptive caption that relates the image to its context.",
                },
                ],
            ),
            ]
        )
        
        try:
            chain = prompt | self.llm
            result = chain.invoke({
                "context": context,
                "image_data": image_data
            })
            return result.content
        except Exception as e:
            logger.error(f"Error generating caption: {str(e)}")
            return ""