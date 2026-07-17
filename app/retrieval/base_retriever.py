from abc import ABC, abstractmethod

from app.retrieval.retrieval_result import RetrievalResult

class BaseRetriever(ABC):
    """
    Abstract interface for retrieval components.

    Implementations retrieve the most relevant chunks for a given query.
    """

    @abstractmethod
    def retrieve(
        self,
        query: str,
    ) -> list[RetrievalResult]:
        """
        Retrieve relevant chunks for the supplied query.
        """
        pass