from time import perf_counter

from app.llm.base_llm import BaseLLM
from app.llm.prompt_builder import PromptBuilder
from app.pipeline.response import PipelineResponse
from app.retrieval.base_retriever import BaseRetriever


class RAGPipeline:
    """
    End-to-end Retrieval-Augmented Generation pipeline.
    """
    def __init__(
        self,
        retriever: BaseRetriever,
        prompt_builder: PromptBuilder,
        llm: BaseLLM,
    ):
        self.retriever = retriever
        self.prompt_builder = prompt_builder
        self.llm = llm
    def ask(
        self,
        question: str,
    ) -> PipelineResponse:

        pipeline_start = perf_counter()

        retrieval_start = perf_counter()
        retrieval_results = self.retriever.retrieve(question)
        retrieval_latency = (perf_counter() - retrieval_start) * 1000

        prompt = PromptBuilder.build(
            question=question,
            results=retrieval_results,
        )

        llm_response = self.llm.generate(prompt)

        total_latency = (perf_counter() - pipeline_start) * 1000
        
        return PipelineResponse(
            question=question,
            answer=llm_response.answer,
            retrieval_results=retrieval_results,
            model=llm_response.model,
            retrieval_latency_ms=retrieval_latency,
            generation_latency_ms=llm_response.latency_ms,
            total_latency_ms=total_latency,
        )