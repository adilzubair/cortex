import subprocess
import os
from pathlib import Path
from .filesystem import load_folder

def load_github_repo(repo_url: str) -> tuple[list, str]:
    """
    Clone a GitHub repository to persistent storage and load its files.
    
    Args:
        repo_url: GitHub repository URL (e.g., https://github.com/user/repo.git)
    
    Returns:
        tuple: (list of documents, absolute path to cloned repo)
    """
    # Extract repo name from URL
    repo_name = os.path.basename(repo_url.rstrip('/').replace('.git', ''))
    
    # Create persistent storage directory
    cortex_home = Path.home() / ".cortex" / "repos"
    cortex_home.mkdir(parents=True, exist_ok=True)
    
    clone_path = cortex_home / repo_name
    
    # Clone or update the repository
    if clone_path.exists():
        print(f"Repository '{repo_name}' already exists at {clone_path}. Pulling latest changes...")
        try:
            subprocess.run(
                ["git", "-C", str(clone_path), "pull"],
                check=True,
                capture_output=True,
                text=True
            )
        except subprocess.CalledProcessError as e:
            print(f"Warning: Could not pull latest changes: {e.stderr}")
    else:
        print(f"Cloning repository to {clone_path}...")
        subprocess.run(
            ["git", "clone", "--depth", "1", repo_url, str(clone_path)],
            check=True
        )
    
    # Load documents from the cloned repository
    docs = load_folder(str(clone_path))
    
    # Add GitHub metadata
    for doc in docs:
        doc.metadata["source"] = "github"
        doc.metadata["repo"] = repo_name
        doc.metadata["repo_url"] = repo_url
    
    return docs, str(clone_path)
