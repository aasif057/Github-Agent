from app.github.client import get_github_client
from app.github.repo_ingestor import RepositoryIngestor

from app.embeddings.config import EmbeddingConfig
from app.embeddings.factory import EmbeddingFactory

from app.vectorstore.config import VectorStoreConfig
from app.vectorstore.factory import VectorStoreFactory

from app.chunking.chunk_factory import ChunkFactory


def main():

    # -------------------------------
    # GitHub
    # -------------------------------

    github = get_github_client()

    ingestor = RepositoryIngestor(
        github
    )

    documents = ingestor.load_code_files(
        "langchain-ai/langgraph"
    )

    print(
        f"Loaded {len(documents)} files"
    )

    # -------------------------------
    # Chunking
    # -------------------------------

    chunks = []

    for document in documents:

        chunker = ChunkFactory.get_chunker(
            document.language
        )

        if chunker is None:
            continue

        chunks.extend(
            chunker.chunk(document)
        )

    print(
        f"Generated {len(chunks)} chunks"
    )

    # -------------------------------
    # Limit for testing
    # -------------------------------

    chunks = chunks[:50]

    print(
        f"Testing with {len(chunks)} chunks"
    )

    # -------------------------------
    # Embedder
    # -------------------------------

    embedding_config = EmbeddingConfig(
        model_name="BAAI/bge-base-en-v1.5",
        device="cpu",
        batch_size=8,
    )

    embedder = EmbeddingFactory.get(
        "sentence_transformer",
        embedding_config,
    )

    vectors = embedder.embed_chunks(
        chunks
    )

    print(
        f"Generated {len(vectors)} vectors"
    )

    # -------------------------------
    # Vector Store
    # -------------------------------

    vector_config = VectorStoreConfig(
        collection_name="github_code",
        embedding_dimension=768,
        recreate_collection=True,
    )

    store = VectorStoreFactory.get(
        "qdrant",
        vector_config,
    )

    store.upsert(
        chunks,
        vectors,
    )

    print()

    print(
        "Vectors in collection:",
        store.count()
    )


if __name__ == "__main__":

    main()