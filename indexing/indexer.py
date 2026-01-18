from embeddings.ollama import OllamaEmbeddingModel
from vectorstore.chroma import VectorStoreManager
import os
from dotenv import load_dotenv

load_dotenv()

from core.config import EMBEDDING_MODEL, OLLAMA_BASE_URL

class Indexer:
    def __init__(self, project_path: str = ".", embedding_model=None, vector_store=None):
        self.embedding_model = embedding_model or OllamaEmbeddingModel(
            model=EMBEDDING_MODEL,
            base_url=OLLAMA_BASE_URL 
        )
        self.vector_store = vector_store or VectorStoreManager(project_path=project_path)

    def index_chunks(self, chunks):
        if not chunks:
            return
        texts = [chunk.content for chunk in chunks]
        embeddings = self.embedding_model.embed(texts)
        self.vector_store.add_chunks(chunks, embeddings)

    def delete_file_index(self, file_path: str):
        """Removes all chunks for a given file from the vector store."""
        self.vector_store.delete_by_file(file_path)