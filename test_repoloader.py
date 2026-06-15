# test_repo_loader.py

from app.ingestion.repo_loader import RepoLoader

loader = RepoLoader()

docs = loader.load_repository(
    "https://github.com/langchain-ai/langgraph"
)

print(f"Files loaded: {len(docs)}")

print(docs[0]["file_path"])
print(docs[0]["content"][:500])