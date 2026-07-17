from time import perf_counter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from app.llm.base_llm import BaseLLM
from app.llm.response import LLMResponse


class GeminiLLM(BaseLLM):
    """
    Gemini implementation of the BaseLLM interface.
    """

    def __init__(self, config):
        super().__init__(config)

        self.llm = ChatGoogleGenerativeAI(
            model=config.model_name,
            google_api_key=config.api_key,
            temperature=config.temperature,
            max_output_tokens=config.max_tokens,
            timeout=config.timeout,
        )

        self.parser = StrOutputParser()

    def generate(
        self,
        prompt: ChatPromptTemplate,
    ) -> LLMResponse:

        chain = prompt | self.llm | self.parser

        start = perf_counter()
        try:
            answer = chain.invoke({})
        except Exception as e:
            raise RuntimeError(
                f"Failed to invoke Gemini model '{self.config.model_name}'. "
                "Check that the model name is available for your API project."
            ) from e

        latency_ms = (perf_counter() - start) * 1000

        return LLMResponse(
            answer=answer,
            model=self.model_name(),
            latency_ms=latency_ms,
        )

    def model_name(self) -> str:
        return self.config.model_name