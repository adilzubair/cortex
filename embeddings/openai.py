from openai import OpenAI
from .base import EmbeddingModel

class OpenAIEmbeddingModel(EmbeddingModel):
    def __init__(self, model="text-embedding-3-small"):
        self.client = OpenAI()
        self.model = model

    def embed(self, texts):
        response = self.client.embeddings.create(
            model=self.model,
            input=texts
        )
        return [item.embedding for item in response.data]
