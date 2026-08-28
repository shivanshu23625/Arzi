import numpy as np

try:
    from sentence_transformers import SentenceTransformer
    HAS_SENTENCE_TRANSFORMERS = True
except ImportError:
    HAS_SENTENCE_TRANSFORMERS = False

from sklearn.feature_extraction.text import HashingVectorizer

class ModelSingleton:
    _instance = None

    @classmethod
    def get_model(cls):
        if cls._instance is None:
            if HAS_SENTENCE_TRANSFORMERS:
                try:
                    cls._instance = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
                except Exception:
                    cls._instance = HashingVectorizer(n_features=384, alternate_sign=False)
            else:
                cls._instance = HashingVectorizer(n_features=384, alternate_sign=False)
        return cls._instance

class EmbeddingService:
    def __init__(self):
        self.model = ModelSingleton.get_model()

    def encode(self, text: str) -> np.ndarray:
        if HAS_SENTENCE_TRANSFORMERS and hasattr(self.model, "encode"):
            try:
                vec = self.model.encode(text, convert_to_numpy=True, normalize_embeddings=True)
                return vec.astype("float32")
            except Exception:
                pass

        # Robust Fallback Vectorizer (384-dimensional normalized vector)
        raw_vec = self.model.transform([text]).toarray()[0].astype("float32")
        norm = np.linalg.norm(raw_vec)
        if norm > 0:
            raw_vec = raw_vec / norm
        return raw_vec