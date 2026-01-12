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
    
    # Check if we should ignore (e.g. .git, __pycache__, .venv, .cortex)
    ignore_list = [".git", "__pycache__", ".venv", ".pytest_cache", ".cortex", ".gemini"]
    if any(part.startswith(".") or part in ignore_list for part in rel_path.split(os.sep)):
        return False

    # Also ignore typical temporary/journal files
    if rel_path.endswith(("-journal", ".tmp", ".swp")):
        return False

    if not os.path.exists(abs_path):
        return False

    has_changed, current_hash = state_manager.has_changed(abs_path)
    
    if has_changed:
        print(f"Indexing: {rel_path}")
        from ingestion.loaders.filesystem import CODE_EXTENSIONS
        ext = os.path.splitext(abs_path)[1].lower()
        doc_type = "code" if ext in CODE_EXTENSIONS else "text"
        
        # Minimally load document for this file
        try:
            with open(abs_path, "r", encoding="utf-8") as f:
                content = f.read()
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
    source_abs = os.path.abspath(source)
    if source_type == "folder":
        docs = load_folder(source_abs)
    elif source_type == "github":
        docs = load_github_repo(source_abs)
    else:
        raise ValueError("Unsupported source type")

    indexer = Indexer(project_path=source_abs)
    state_manager = StateManager(project_path=source_abs)
    
    indexed_count = 0
    skipped_count = 0

    for doc in docs:
        abs_path = doc.metadata.get("abs_path")
        if index_file(abs_path, source_abs, indexer, state_manager):
            indexed_count += 1
        else:
            skipped_count += 1

    print(f"\n--- Indexing Summary ---")
    print(f"Files Indexed: {indexed_count}")
    print(f"Files Skipped: {skipped_count}")
    return indexed_count

if __name__ == "__main__":
    num_indexed = ingest_and_index(".", "folder")