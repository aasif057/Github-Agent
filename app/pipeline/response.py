from dataclasses import dataclass

from app.retrieval.retrieval_result import RetrievalResult


@dataclass
class PipelineResponse:
    """
    Response returned by the RAG pipeline.
    """

    question: str

    answer: str

    retrieval_results: list[RetrievalResult]

    model: str

    retrieval_latency_ms: float | None = None

    generation_latency_ms: float | None = None

    total_latency_ms: float | None = None