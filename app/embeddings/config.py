from dataclasses import dataclass


@dataclass
class EmbeddingConfig:

    model_name: str = "BAAI/bge-base-en-v1.5"

    batch_size: int = 16

    device: str = "auto"

    normalize: bool = True

    show_progress: bool = True

    cache_folder: str | None = None

    trust_remote_code: bool = False