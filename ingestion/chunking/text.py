from .base import Chunk

def chunk_text(text, metadata, chunk_size=500, overlap=50):
    """
    Splits text into chunks of approximately chunk_size characters with overlap.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk_text = text[start:end]
        chunks.append(
            Chunk(
                content=chunk_text,
                metadata=metadata.copy()
            )
        )
        start += chunk_size - overlap
    return chunks
