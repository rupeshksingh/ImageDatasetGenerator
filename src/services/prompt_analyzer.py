from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from typing import List
from ..models.schemas import ListOfDomains
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class PromptAnalyzer:
    def __init__(self, openai_api_key: str):
        self.llm = ChatOpenAI(api_key=openai_api_key, model="chatgpt-4o-latest", temperature=0)
        self.parser = JsonOutputParser(pydantic_object=ListOfDomains)
        
    def analyze(self, prompt: str) -> ListOfDomains:
        template = [
        (
            "system",
            "Analyze the user prompt and identify relevant domains and their search queries. "
            "Provide specific search queries for each domain that would yield relevant images.\n"
            "{format_instructions}"
        ),
        ("human", "{query}"),
    ]
        
        try:
            chat_prompt = ChatPromptTemplate.from_messages(template).partial(format_instructions=self.parser.get_format_instructions())
            chain = chat_prompt | self.llm | self.parser
            result = chain.invoke({'query': prompt})
            return result.get('domains', [])
        except Exception as e:
            logger.error(f"Error analyzing prompt: {str(e)}")
            raise