import tempfile
import subprocess
import os
from .filesystem import load_folder

def load_github_repo(repo_url: str) -> list:
    with tempfile.TemporaryDirectory() as tmpdir:
        subprocess.run(
            ["git", "clone", "--depth", "1", repo_url, tmpdir],
            check=True
        )

        repo_name = os.path.basename(repo_url).replace(".git", "")
        docs = load_folder(tmpdir)

        for doc in docs:
            doc.metadata["source"] = "github"
            doc.metadata["repo"] = repo_name

        return docs
