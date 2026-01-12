import chromadb
from chromadb.config import Settings
from uuid import uuid4

from app.config import get_vector_persist_dir

class VectorStoreManager:
    def __init__(self, project_path: str = ".", collection_name="cortex", persist_dir=None):
        if persist_dir is None:
            persist_dir = get_vector_persist_dir(project_path)
            
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def add_chunks(self, chunks, embeddings):
        ids = []
        documents = []
        metadatas = []

        for chunk in chunks:
            ids.append(str(uuid4()))
            documents.append(chunk.content)
            
            # Prepare metadata and filter out None values
            metadata = chunk.metadata.copy()
            metadata["start_line"] = chunk.start_line
            metadata["end_line"] = chunk.end_line
            
            # ChromaDB doesn't allow None values in metadata
            clean_metadata = {k: v for k, v in metadata.items() if v is not None}
            metadatas.append(clean_metadata)

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def delete_by_file(self, path: str):
        self.collection.delete(where={"path": path})

