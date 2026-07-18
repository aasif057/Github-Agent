import os

from dotenv import load_dotenv

from app.embeddings.config import EmbeddingConfig
from app.embeddings.factory import EmbeddingFactory

from app.vectorstore.config import VectorStoreConfig
from app.vectorstore.factory import VectorStoreFactory

from app.retrieval.retrieval_config import RetrievalConfig
from app.retrieval.semantic_retriever import SemanticRetriever

from app.llm.config import LLMConfig
from app.llm.gemini_llm import GeminiLLM
from app.llm.prompt_builder import PromptBuilder

from app.pipeline.rag_pipeline import RAGPipeline


def create_pipeline() -> RAGPipeline:
    """
    Builds the complete GitHub Code Intelligence pipeline.
    """

    load_dotenv()

    # --------------------------------------------------
    # Embedder
    # --------------------------------------------------

    embedder = EmbeddingFactory.get(
        "sentence_transformer",
        EmbeddingConfig(
            model_name="BAAI/bge-base-en-v1.5",
            device="cpu",
        ),
    )

    # --------------------------------------------------
    # Vector Store
    # --------------------------------------------------

    vectorstore = VectorStoreFactory.get(
        "qdrant",
        VectorStoreConfig(
            collection_name="github_code",
            embedding_dimension=768,
        ),
    )

    # --------------------------------------------------
    # Retriever
    # --------------------------------------------------

    retriever = SemanticRetriever(
        embedder=embedder,
        vectorstore=vectorstore,
        config=RetrievalConfig(
            top_k=5,
        ),
    )

    # --------------------------------------------------
    # LLM
    # --------------------------------------------------

    llm = GeminiLLM(
        LLMConfig(
            provider="gemini",
            api_key=os.environ["GEMINI_API_KEY"],
        )
    )

    # --------------------------------------------------
    # Pipeline
    # --------------------------------------------------

    pipeline = RAGPipeline(
        retriever=retriever,
        prompt_builder=PromptBuilder(),
        llm=llm,
    )

    return pipeline