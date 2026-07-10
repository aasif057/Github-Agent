from dataclasses import dataclass

from app.chunking.models import CodeChunk


@dataclass
class EmbeddingResult:
    chunk: CodeChunk
    embedding: list[float]