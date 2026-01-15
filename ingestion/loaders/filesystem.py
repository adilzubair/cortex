import os
from .base import IngestedDocument
from datetime import datetime

CODE_EXTENSIONS = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".java": "java",
    ".cpp": "cpp",
}

TEXT_EXTENSIONS = {
    ".md": "markdown",
    ".txt": "text"
}

def read_file_robust(path: str) -> str:
    """
    Reads a file using multiple encodings as fallback.
    """
    encodings = ["utf-8", "latin-1", "utf-16", "utf-16le", "utf-16be"]
    
    for enc in encodings:
        try:
            with open(path, "r", encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, LookupError):
            continue
            
    # Final fallback: read with utf-8 and ignore errors
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def load_folder(path: str) -> list[IngestedDocument]:
    documents = []

    for root, dirs, files in os.walk(path):
        # Skip hidden directories in-place (dirs starting with .)
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            # Skip hidden files
            if file.startswith('.'):
                continue
                
            ext = os.path.splitext(file)[1]
            full_path = os.path.join(root, file)

            if ext not in CODE_EXTENSIONS and ext not in TEXT_EXTENSIONS:
                continue

            try:
                content = read_file_robust(full_path)

                doc_type = "code" if ext in CODE_EXTENSIONS else "text"

                documents.append(
                    IngestedDocument(
                        content=content,
                        metadata={
                            "source": "filesystem",
                            "path": os.path.relpath(full_path, path),
                            "abs_path": os.path.abspath(full_path), # Add this line
                            "type": doc_type,
                            "language": CODE_EXTENSIONS.get(ext, "unknown"),
                            "last_modified": datetime.fromtimestamp(
                                os.path.getmtime(full_path)
                            ).isoformat()
                        }
                    )
                )
            except Exception as e:
                print(f"Skipped {full_path}: {e}")

    return documents
