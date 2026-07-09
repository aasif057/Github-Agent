from app.github.client import get_github_client
from app.github.repo_ingestor import RepositoryIngestor
from collections import Counter

github_client = get_github_client()

ingestor = RepositoryIngestor(
    github_client
)

docs = ingestor.load_code_files(
    "langchain-ai/langgraph"
)

print(f"Loaded {len(docs)} files")

print(docs[0].file_path)
print(docs[0].content[:500])

extensions = Counter()

for doc in docs:
    ext = doc.file_path.split(".")[-1]
    extensions[ext] += 1

print(extensions.most_common(20))

language_counts = {}

for doc in docs:
    language_counts[doc.language] = (
        language_counts.get(doc.language, 0) + 1
    )

print(language_counts)