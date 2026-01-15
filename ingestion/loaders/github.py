import subprocess
import os
import shutil
from pathlib import Path
from .filesystem import load_folder
from core.config import get_global_repos_dir

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
    cortex_home = get_global_repos_dir()
    
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

def list_cloned_repos() -> list[str]:
    """
    List all repositories cloned in the global repos directory.
    
    Returns:
        list: List of repository names (folder names)
    """
    repos_dir = get_global_repos_dir()
    return [d.name for d in repos_dir.iterdir() if d.is_dir()]

def delete_cloned_repo(repo_name: str) -> bool:
    """
    Delete a cloned repository from the global repos directory.
    
    Args:
        repo_name: Name of the repository folder
        
    Returns:
        bool: True if deleted, False if not found
    """
    repos_dir = get_global_repos_dir()
    repo_path = repos_dir / repo_name
    
    if repo_path.exists() and repo_path.is_dir():
        shutil.rmtree(repo_path)
        return True
    return False
