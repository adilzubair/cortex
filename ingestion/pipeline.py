import os
from indexing.indexer import Indexer
from indexing.state import StateManager
from ingestion.loaders.filesystem import load_folder
from ingestion.loaders.github import load_github_repo
from ingestion.chunking import chunk_document

def index_file(abs_path: str, source_root: str, indexer: Indexer = None, state_manager: StateManager = None):
    """Indexes a single file if it has changed."""
    if indexer is None:
        indexer = Indexer(project_path=source_root)
    if state_manager is None:
        state_manager = StateManager(project_path=source_root)

    # Determine relative path for metadata
    rel_path = os.path.relpath(abs_path, source_root)
    
    # Check if we should ignore
    from core.config import IGNORED_DIRS, IGNORED_FILE_SUFFIXES, CODE_EXTENSIONS
    
    parts = rel_path.split(os.sep)
    if any(part.startswith(".") or part in IGNORED_DIRS for part in parts):
        return False

    # Also ignore typical temporary/journal files
    if rel_path.endswith(IGNORED_FILE_SUFFIXES):
        return False

    if not os.path.exists(abs_path):
        return False

    has_changed, current_hash = state_manager.has_changed(abs_path)
    
    if has_changed:
        print(f"Indexing: {rel_path}")
        ext = os.path.splitext(abs_path)[1].lower()
        doc_type = "code" if ext in CODE_EXTENSIONS else "text"
        
        # Minimally load document for this file
        try:
            from ingestion.loaders.filesystem import read_file_robust
            content = read_file_robust(abs_path)
        except Exception as e:
            print(f"Error reading {abs_path}: {e}")
            return False

        from ingestion.loaders.document import IngestedDocument
        from datetime import datetime
        doc = IngestedDocument(
            content=content,
            metadata={
                "source": "filesystem",
                "path": rel_path,
                "abs_path": abs_path,
                "type": doc_type,
                "language": CODE_EXTENSIONS.get(ext, "unknown"),
                "last_modified": datetime.fromtimestamp(os.path.getmtime(abs_path)).isoformat()
            }
        )

        indexer.delete_file_index(rel_path)
        chunks = chunk_document(doc)
        indexer.index_chunks(chunks)
        state_manager.update_state(abs_path, current_hash)
        return True
    return False

def ingest_and_index(source: str, source_type: str):
    """
    Ingest and index a codebase from a folder or GitHub repository.
    
    Args:
        source: Path to folder or GitHub URL
        source_type: Either 'folder' or 'github'
    
    Returns:
        tuple: (number of indexed files, project path)
    """
    # Determine if source is a GitHub URL
    is_github_url = source_type == "github" or source.startswith(("http://", "https://", "git@"))
    
    if is_github_url:
        # For GitHub repos, clone and get the persistent path
        docs, project_path = load_github_repo(source)
    else:
        # For local folders, use the absolute path
        project_path = os.path.abspath(source)
        docs = load_folder(project_path)

    indexer = Indexer(project_path=project_path)
    state_manager = StateManager(project_path=project_path)
    
    indexed_count = 0
    skipped_count = 0

    for doc in docs:
        abs_path = doc.metadata.get("abs_path")
        if index_file(abs_path, project_path, indexer, state_manager):
            indexed_count += 1
        else:
            skipped_count += 1

    print(f"\n--- Indexing Summary ---")
    print(f"Files Indexed: {indexed_count}")
    print(f"Files Skipped: {skipped_count}")
    return indexed_count, project_path

if __name__ == "__main__":
    num_indexed = ingest_and_index(".", "folder")