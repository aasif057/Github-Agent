from abc import ABC, abstractmethod

import torch

from app.chunking.models import CodeChunk
from app.embeddings.config import EmbeddingConfig


class BaseEmbedder(ABC):

    def __init__(
        self,
        config: EmbeddingConfig,
    ):

        self.config = config

        if config.device == "auto":

            self.device = (
                "cuda"
                if torch.cuda.is_available()
                else "cpu"
            )

        else:

            self.device = config.device

    @abstractmethod
    def embed_chunks(
        self,
        chunks: list[CodeChunk],
    ) -> list[list[float]]:
        """
        Embed a batch of CodeChunks.

        Returns
        -------
        List[List[float]]
            One embedding vector per chunk.
        """
        pass

    def embed_chunk(
        self,
        chunk: CodeChunk,
    ) -> list[float]:
        """
        Convenience wrapper for embedding
        a single chunk.
        """

        return self.embed_chunks(
            [chunk]
        )[0]
    
    # def _prepare_text(
    #     self,
    #     chunk: CodeChunk,
    # ) -> str:
    #     """
    #     Converts a CodeChunk into
    #     embeddable text.

    #     Can be overridden by subclasses.
    #     """

    #     return chunk.content

    @abstractmethod
    def model_name(
        self,
    ) -> str:
        """
        Returns the model identifier.
        """
        pass

    @abstractmethod
    def embedding_dimension(
        self,
    ) -> int:
        """
        Returns embedding dimension.
        """
        pass