import hashlib


class ChunkIdGenerator:

    @staticmethod
    def generate(
        repo: str,
        file_path: str,
        symbol: str,
        chunk_type: str,
        part: int = 1,
    ) -> str:

        key = (
            f"{repo}:"
            f"{file_path}:"
            f"{chunk_type}:"
            f"{symbol}:"
            f"{part}"
        )

        return hashlib.sha256(
            key.encode("utf-8")
        ).hexdigest()