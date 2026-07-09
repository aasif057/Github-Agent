from copy import deepcopy
from typing import List
from app.chunking.utils import ChunkIdGenerator
from app.chunking.models import CodeChunk


class SlidingWindowSplitter:
    """
    Splits large CodeChunks into overlapping windows.

    Example:

    0 ---------------- 4000
             400 overlap
          3600 ----------- 7600
    """

    def __init__(
        self,
        max_chars: int = 4000,
        overlap: int = 400,
    ):
        self.max_chars = max_chars
        self.overlap = overlap

    def split_chunk(
        self,
        chunk: CodeChunk
    ) -> List[CodeChunk]:

        content = chunk.content

        if len(content) <= self.max_chars:
            chunk.chunk_id = ChunkIdGenerator.generate(
                repo=chunk.repo,
                file_path=chunk.file_path,
                symbol=chunk.name,
                chunk_type=chunk.chunk_type,
                part=1,
            )

            return [chunk]
        parts = []

        start = 0

        while start < len(content):

            end = min(
                start + self.max_chars,
                len(content)
            )

            piece = content[start:end]

            new_chunk = deepcopy(chunk)

            new_chunk.content = piece

            parts.append(new_chunk)

            if end == len(content):
                break

            start = end - self.overlap

        total_parts = len(parts)

        for index, part in enumerate(parts):

            part.metadata = {
                **part.metadata,
                "part": index + 1,
                "total_parts": total_parts,
                "char_start": index * (self.max_chars - self.overlap),
                "char_end": min(
                    index * (self.max_chars - self.overlap)
                    + self.max_chars,
                    len(content)
                ),
                "split_strategy": "sliding_window",
                "max_chars": self.max_chars
            }
            part.chunk_id = ChunkIdGenerator.generate(
            repo=part.repo,
            file_path=part.file_path,
            symbol=part.name,
            chunk_type=part.chunk_type,
            part=index + 1,
        )

        return parts