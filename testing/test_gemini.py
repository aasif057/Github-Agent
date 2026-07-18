
import os
from app.llm.config import LLMConfig
from app.llm.gemini_llm import GeminiLLM
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
load_dotenv()

config = LLMConfig(
    provider="gemini",
    api_key=os.environ["GEMINI_API_KEY"],
)

llm = GeminiLLM(config)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are helpful."),
    ("human", "Say hello.")
])

response = llm.generate(prompt)

print(response.answer)
print(response.model)
print(response.latency_ms)