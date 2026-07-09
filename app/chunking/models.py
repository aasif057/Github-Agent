from dataclasses import dataclass
from typing import Optional


@dataclass
class CodeChunk:
    chunk_type: str
    name: str
    language: str
    file_path: str
    content: str
    metadata: dict
    repo: str
    chunk_id: Optional[str] = None