from typing import Optional


class MetadataBuilder:
    """
    Creates standardized metadata for every CodeChunk.

    Keeps metadata generation centralized so all
    chunkers produce the same schema.
    """

    @staticmethod
    def build(
        *,
        repo: str,
        language: str,
        file_path: str,
        chunk_type: str,
        symbol: str,
        start_line: int,
        end_line: int,
        parent_class: Optional[str] = None,
    ) -> dict:

        metadata = {
            "repo": repo,
            "language": language,
            "file_path": file_path,
            "chunk_type": chunk_type,
            "symbol": symbol,
            "start_line": start_line,
            "end_line": end_line,
        }

        if parent_class is not None:
            metadata["parent_class"] = parent_class

        return metadata