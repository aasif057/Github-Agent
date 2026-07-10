from sentence_transformers import SentenceTransformer
from app.chunking.models import CodeChunk

from app.embeddings.base_embedder import BaseEmbedder
from app.embeddings.utils import prepare_chunk_text


class SentenceTransformerEmbedder(BaseEmbedder):
    # Cache for loaded models
    _loaded_models = {}

    def __init__(self, config):

        super().__init__(config)

        if config.model_name not in self._loaded_models:

            print(
                f"\nLoading embedding model:"
                f" {config.model_name}"
            )

            self._loaded_models[
                config.model_name
            ] = SentenceTransformer(
                model_name_or_path=config.model_name,
                device=self.device,
                cache_folder=config.cache_folder,
                trust_remote_code=config.trust_remote_code,
            )

            print(
                f"Loaded model on {self.device}"
            )

        else:

            print(
                f"Using cached model:"
                f" {config.model_name}"
            )

        self.model = self._loaded_models[
            config.model_name
        ]

    def embed_chunks(
        self,
        chunks: list[CodeChunk],
    ) -> list[list[float]]:

        if len(chunks) == 0:
            return []

        texts = [
            prepare_chunk_text(chunk)
            for chunk in chunks
        ]

        embeddings = self.model.encode(
            texts,
            batch_size=self.config.batch_size,
            normalize_embeddings=self.config.normalize,
            convert_to_numpy=True,
            show_progress_bar=self.config.show_progress,
        )

        return embeddings.tolist()

    def model_name(
        self,
    ) -> str:

        return self.config.model_name

    def embedding_dimension(
        self,
    ) -> int:

        return self.model.get_embedding_dimension()