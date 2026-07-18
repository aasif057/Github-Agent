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

load_dotenv()

def main():

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

    # --------------------------------------------------
    # Ask
    # --------------------------------------------------

    question = "Where is generate_redirects implemented?"

    response = pipeline.ask(question)

    print("=" * 80)

    print("QUESTION")
    print(question)

    print("=" * 80)

    print("ANSWER")
    print(response.answer)

    print("=" * 80)

    print("MODEL")
    print(response.model)

    print("=" * 80)

    print("LATENCIES")

    print(
        f"Retrieval : {response.retrieval_latency_ms:.2f} ms"
    )

    print(
        f"Generation: {response.generation_latency_ms:.2f} ms"
    )

    print(
        f"Total     : {response.total_latency_ms:.2f} ms"
    )

    print("=" * 80)

    print("SOURCES")

    for i, result in enumerate(
        response.retrieval_results,
        start=1,
    ):

        print(
            f"{i}. "
            f"{result.chunk.file_path} "
            f"({result.score:.4f})"
        )


if __name__ == "__main__":
    main()