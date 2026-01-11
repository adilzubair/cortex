from typing import List
import time

class OllamaEmbeddingModel:
    def __init__(
        self,
        model: str,
        base_url: str = "http://localhost:11434",
        timeout: int = 600,  # 10 minutes
        batch_size: int = 32,
    ):
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.batch_size = batch_size

    def embed(self, texts: List[str]) -> List[List[float]]:
        all_embeddings = []

        for i in range(0, len(texts), self.batch_size):
            batch = texts[i : i + self.batch_size]

            embeddings = self._embed_batch(batch)
            all_embeddings.extend(embeddings)

            # small delay to avoid Ollama overload
            time.sleep(0.05)

        return all_embeddings

    def _embed_batch(self, texts: List[str]) -> List[List[float]]:
        import requests

        url = f"{self.base_url}/v1/embeddings"

        response = requests.post(
            url,
            json={
                "model": self.model,
                "input": texts,
            },
            timeout=self.timeout,
        )

        response.raise_for_status()
        data = response.json()

        return [item["embedding"] for item in data["data"]]
