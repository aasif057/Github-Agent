from app.embeddings.config import EmbeddingConfig


class EmbeddingFactory:

    @staticmethod
    def get(
        provider: str,
        config: EmbeddingConfig,
    ):

        provider = provider.lower()

        if provider == "sentence_transformer":

            from app.embeddings.sentence_transformer_embedder import (
                SentenceTransformerEmbedder,
            )

            return SentenceTransformerEmbedder(
                config
            )

        raise ValueError(
            f"Unsupported provider: {provider}"
        )