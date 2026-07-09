from collections import Counter

from app.github.client import get_github_client
from app.github.repo_ingestor import RepositoryIngestor
from app.chunking.chunk_factory import ChunkFactory


def main():

    github_client = get_github_client()

    ingestor = RepositoryIngestor(github_client)

    docs = ingestor.load_code_files(
        "langchain-ai/langgraph"
    )

    all_chunks = []

    for doc in docs:

        chunker = ChunkFactory.get_chunker(
            doc.language
        )

        if chunker is None:
            continue

        all_chunks.extend(
            chunker.chunk(doc)
        )

    print("=" * 60)

    print(f"Generated {len(all_chunks)} chunks")

    print("=" * 60)

    sample = all_chunks[0]

    print(f"Name      : {sample.name}")
    print(f"Type      : {sample.chunk_type}")
    print(f"Chunk ID  : {sample.chunk_id}")
    print(f"Language  : {sample.language}")
    print(f"File      : {sample.file_path}")
    print(f"Metadata  : {sample.metadata}")

    print("=" * 60)

    counter = Counter(
        chunk.chunk_type
        for chunk in all_chunks
    )

    print("Chunk Type Distribution")

    for chunk_type, count in counter.items():
        print(f"{chunk_type:<10}: {count}")

    print("=" * 60)

    largest = max(
        all_chunks,
        key=lambda chunk: len(chunk.content)
    )

    print("Largest Chunk")

    print(f"Name      : {largest.name}")
    print(f"Type      : {largest.chunk_type}")
    print(f"Size      : {len(largest.content)}")
    print(f"File      : {largest.file_path}")
    print(f"Chunk ID  : {largest.chunk_id}")
    print(f"Metadata  : {largest.metadata}")
    print("=" * 60)


if __name__ == "__main__":
    main()