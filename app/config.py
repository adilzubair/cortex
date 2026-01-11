import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
    EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "ollama")
    VECTOR_DB_DIR = os.getenv("VECTOR_DB_DIR", "./data/chroma")
