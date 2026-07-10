from app.chunking.models import CodeChunk


def prepare_chunk_text(chunk: CodeChunk) -> str:
    """
    Converts a CodeChunk into text suitable
    for embedding.

    This format can later be customized per
    embedding model.
    """

    sections = []

    sections.append(f"Type: {chunk.chunk_type}")

    sections.append(f"Language: {chunk.language}")

    sections.append(f"Name: {chunk.name}")

    sections.append(f"File: {chunk.file_path}")

    sections.append("")

    sections.append(chunk.content)

    return "\n".join(sections)