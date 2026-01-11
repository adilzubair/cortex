from ingestion.chunking.text import chunk_text
from ingestion.chunking.code import chunk_python_code
from ingestion.chunking.base import Chunk

def chunk_document(doc):
    """
    Routes a document to the appropriate chunker.
    """
    if doc.metadata.get("type") == "code":
        if doc.metadata.get("language") == "python":
            return chunk_python_code(doc.content, doc.metadata)

        # fallback for non-python code
        lines = doc.content.splitlines()
        chunks = []
        chunk_size = 50

        for i in range(0, len(lines), chunk_size):
            chunk_text_block = "\n".join(lines[i:i + chunk_size])
            chunks.append(
                Chunk(
                    content=chunk_text_block,
                    metadata=doc.metadata.copy(),
                    start_line=i + 1,
                    end_line=min(i + chunk_size, len(lines))
                )
            )
        return chunks

    # non-code documents
    return chunk_text(doc.content, doc.metadata)
