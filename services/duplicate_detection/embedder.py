from sentence_transformers import SentenceTransformer
import numpy as np

class ModelSingleton:
    _instance = None

    @classmethod
    def get_model(cls) -> SentenceTransformer:
        if cls._instance is None:
            cls._instance = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        return cls._instance

class EmbeddingService:
    def __init__(self):
        self.model = ModelSingleton.get_model()

    def encode(self, text: str) -> np.ndarray:
        vec = self.model.encode(text, convert_to_numpy=True, normalize_embeddings=True)
        return vec.astype("float32")