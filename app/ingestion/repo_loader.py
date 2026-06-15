from pathlib import Path
from typing import List, Dict
import git
import os


SUPPORTED_EXTENSIONS = {
    ".py",
    ".md",
    ".txt",
    ".rst",
    ".yaml",
    ".yml",
    ".json"
}

IGNORED_DIRS = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "dist",
    "build",
    ".idea",
    ".vscode"
}


class RepoLoader:
    """
    Clone and load GitHub repositories.
    """

    def __init__(self, base_dir: str = "data/repos"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def clone_or_update_repo(self, repo_url: str) -> Path:
        """
        Clone repository if not present.
        Pull latest changes if already exists.
        """

        repo_name = repo_url.rstrip("/").split("/")[-1]
        repo_path = self.base_dir / repo_name

        if repo_path.exists():
            print(f"[INFO] Repository exists. Pulling latest changes...")
            repo = git.Repo(repo_path)
            repo.remotes.origin.pull()

        else:
            print(f"[INFO] Cloning repository...")
            git.Repo.clone_from(repo_url, repo_path)

        return repo_path

    def load_files(self, repo_path: Path) -> List[Dict]:
        """
        Load supported files from repository.
        """

        documents = []

        for root, dirs, files in os.walk(repo_path):

            dirs[:] = [
                d for d in dirs
                if d not in IGNORED_DIRS
            ]

            for file in files:

                file_path = Path(root) / file

                if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                    continue

                try:
                    content = file_path.read_text(
                        encoding="utf-8"
                    )

                    documents.append(
                        {
                            "file_path": str(
                                file_path.relative_to(repo_path)
                            ),
                            "extension": file_path.suffix,
                            "content": content
                        }
                    )

                except Exception as e:
                    print(
                        f"[WARNING] Failed to read {file_path}: {e}"
                    )

        return documents

    def load_repository(
        self,
        repo_url: str
    ) -> List[Dict]:
        """
        End-to-end repository loading.
        """

        repo_path = self.clone_or_update_repo(repo_url)

        documents = self.load_files(repo_path)

        print(
            f"[INFO] Loaded {len(documents)} files"
        )

        return documents
