import ast
import warnings
from .base import Chunk

def chunk_python_code(code: str, metadata):
    chunks = []
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", SyntaxWarning)
            tree = ast.parse(code)

        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                start_line = node.lineno
                end_line = getattr(node, "end_lineno", start_line)
                chunk_text = "\n".join(
                    code.splitlines()[start_line - 1 : end_line]
                )
                chunks.append(
                    Chunk(
                        content=chunk_text,
                        metadata=metadata.copy(),
                        start_line=start_line,
                        end_line=end_line,
                    )
                )
    except Exception:
        # fallback chunking
        lines = code.splitlines()
        chunk_size = 50
        for i in range(0, len(lines), chunk_size):
            chunks.append(
                Chunk(
                    content="\n".join(lines[i : i + chunk_size]),
                    metadata=metadata.copy(),
                    start_line=i + 1,
                    end_line=min(i + chunk_size, len(lines)),
                )
            )

    return chunks
