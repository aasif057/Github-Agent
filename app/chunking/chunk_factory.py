from app.chunking.python_chunker import PythonChunker


class ChunkFactory:

    _chunkers = {
        "python": PythonChunker(),
    }

    @classmethod
    def get_chunker(cls, language):

        return cls._chunkers.get(language)