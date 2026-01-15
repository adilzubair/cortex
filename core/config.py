import os
from pathlib import Path

def get_global_repos_dir() -> Path:
    """Returns the absolute path to the global directory where GitHub repos are cloned."""
    repos_dir = Path.home() / ".cortex" / "repos"
    repos_dir.mkdir(parents=True, exist_ok=True)
    return repos_dir

def get_project_metadata_dir(project_path: str) -> str:
    """Returns the absolute path to the .cortex directory within the project."""
    return os.path.abspath(os.path.join(project_path, ".cortex"))

def get_state_db_path(project_path: str) -> str:
    """Returns the path to the SQLite state database for the project."""
    metadata_dir = get_project_metadata_dir(project_path)
    os.makedirs(os.path.join(metadata_dir, "indexing"), exist_ok=True)
    return os.path.join(metadata_dir, "indexing", "state.db")

def get_vector_persist_dir(project_path: str) -> str:
    """Returns the path to the ChromaDB directory for the project."""
    metadata_dir = get_project_metadata_dir(project_path)
    return os.path.join(metadata_dir, "chroma")
