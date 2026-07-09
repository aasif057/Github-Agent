import ast
from app.chunking.base_chunker import BaseChunker
from app.chunking.models import CodeChunk
from app.chunking.metadata import MetadataBuilder
from app.chunking.splitters import SlidingWindowSplitter


class PythonChunker(BaseChunker):

    def __init__(self):
        self.splitter = SlidingWindowSplitter()

    def chunk(self, document):

        chunks = []

        try:
            tree = ast.parse(document.content)
        except SyntaxError:
            return []

        for node in tree.body:

            # ==========================================================
            # CLASS
            # ==========================================================

            if isinstance(node, ast.ClassDef):

                class_chunk = self._build_class_chunk(
                    node,
                    document
                )

                chunks.extend(
                    self.splitter.split_chunk(
                        class_chunk
                    )
                )

                # ------------------------------------------------------
                # Methods
                # ------------------------------------------------------

                for child in node.body:

                    if not isinstance(
                        child,
                        (
                            ast.FunctionDef,
                            ast.AsyncFunctionDef,
                        )
                    ):
                        continue

                    method_content = ast.get_source_segment(
                        document.content,
                        child
                    )

                    if not method_content:
                        continue

                    metadata = MetadataBuilder.build(
                        repo=document.repo,
                        language=document.language,
                        file_path=document.file_path,
                        chunk_type="method",
                        symbol=f"{node.name}.{child.name}",
                        parent_class=node.name,
                        start_line=child.lineno,
                        end_line=getattr(
                            child,
                            "end_lineno",
                            child.lineno,
                        ),
                    )

                    method_chunk = CodeChunk(
                        chunk_type="method",
                        name=f"{node.name}.{child.name}",
                        language=document.language,
                        file_path=document.file_path,
                        content=method_content,
                        metadata=metadata,
                        repo=document.repo,
                    )

                    chunks.extend(
                        self.splitter.split_chunk(
                            method_chunk
                        )
                    )

            # ==========================================================
            # TOP LEVEL FUNCTIONS
            # ==========================================================

            elif isinstance(
                node,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            ):

                function_content = ast.get_source_segment(
                    document.content,
                    node
                )

                if not function_content:
                    continue

                metadata = MetadataBuilder.build(
                    repo=document.repo,
                    language=document.language,
                    file_path=document.file_path,
                    chunk_type="function",
                    symbol=node.name,
                    start_line=node.lineno,
                    end_line=getattr(
                        node,
                        "end_lineno",
                        node.lineno,
                    ),
                )

                function_chunk = CodeChunk(
                    chunk_type="function",
                    name=node.name,
                    language=document.language,
                    file_path=document.file_path,
                    content=function_content,
                    metadata=metadata,
                    repo=document.repo,
                )

                chunks.extend(
                    self.splitter.split_chunk(
                        function_chunk
                    )
                )

        return chunks

    # ==============================================================
    # Build class summary
    # ==============================================================

    def _build_class_chunk(
        self,
        node,
        document,
    ):

        docstring = ast.get_docstring(node)

        methods = []

        MAX_METHODS_IN_SUMMARY = 10

        for child in node.body:

            if isinstance(
                child,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            ):
                methods.append(child.name)
        public_methods = [
            m for m in methods
            if not m.startswith("_")
        ]

        private_methods = [
            m for m in methods
            if m.startswith("_")
        ]    
        base_classes = []

        for base in node.bases:

            if isinstance(base, ast.Name):
                base_classes.append(base.id)

            elif isinstance(base, ast.Attribute):
                base_classes.append(base.attr)
        decorators = []

        for dec in node.decorator_list:

            if isinstance(dec, ast.Name):
                decorators.append(dec.id)

            elif isinstance(dec, ast.Attribute):
                decorators.append(dec.attr)

        summary = []

        summary.append(
            f"Class: {node.name}"
        )
        summary.append("")
        summary.append(
            f"Public Methods: {len(public_methods)}"
        )

        summary.append(
            f"Private Methods: {len(private_methods)}"
        )

        if base_classes:
            summary.append("")
            summary.append(
                "Base Classes:"
            )

            for base in base_classes:
                summary.append(
                    f"- {base}"
                )
        if decorators:

            summary.append("")
            summary.append("Decorators:")

            for dec in decorators:
                summary.append(f"- @{dec}")

        if docstring:
            summary.append("")
            summary.append("Docstring:")
            summary.append(docstring)

        if methods:
            summary.append("")
            summary.append("Methods:")

            display_methods = methods[:MAX_METHODS_IN_SUMMARY]

            for method in display_methods:
                summary.append(f"- {method}")

            remaining = len(methods) - len(display_methods)

            if remaining > 0:
                summary.append("")
                summary.append(
                    f"... and {remaining} more methods"
                )

        metadata = MetadataBuilder.build(
            repo=document.repo,
            language=document.language,
            file_path=document.file_path,
            chunk_type="class",
            symbol=node.name,
            start_line=node.lineno,
            end_line=getattr(
                node,
                "end_lineno",
                node.lineno,
            ),
        )

        return CodeChunk(
            chunk_type="class",
            name=node.name,
            language=document.language,
            file_path=document.file_path,
            content="\n".join(summary),
            metadata=metadata,
            repo=document.repo,
        )