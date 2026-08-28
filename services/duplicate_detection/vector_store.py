import numpy as np
from typing import List
from config.settings import get_settings
from common.schemas import DuplicateResult
from common.logger import logger

try:
    import faiss
    HAS_FAISS = True
except ImportError:
    HAS_FAISS = False

settings = get_settings()

class FAISSVectorStore:
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.vectors: List[np.ndarray] = []
        self.id_mapping: List[str] = []

        if HAS_FAISS:
            self.index = faiss.IndexFlatIP(self.dimension)
        else:
            self.index = None

    def add_vector(self, vec: np.ndarray, request_id: str):
        if vec.ndim == 1:
            vec_flat = vec
            vec_batch = np.expand_dims(vec, axis=0)
        else:
            vec_flat = vec[0]
            vec_batch = vec

        self.vectors.append(vec_flat)
        self.id_mapping.append(request_id)

        if HAS_FAISS and self.index is not None:
            self.index.add(vec_batch)

    def search_duplicate(self, vec: np.ndarray) -> DuplicateResult:
        if len(self.vectors) == 0:
            return DuplicateResult(is_duplicate=False, similarity_score=0.0, reason="Index empty.")

        if vec.ndim == 1:
            vec_batch = np.expand_dims(vec, axis=0)
            vec_flat = vec
        else:
            vec_batch = vec
            vec_flat = vec[0]

        # Use FAISS if present
        if HAS_FAISS and self.index is not None and self.index.ntotal > 0:
            scores, indices = self.index.search(vec_batch, k=1)
            top_score, top_idx = float(scores[0][0]), int(indices[0][0])
            if top_idx != -1 and top_score >= settings.SIMILARITY_THRESHOLD:
                return DuplicateResult(
                    is_duplicate=True, 
                    similarity_score=round(top_score, 4), 
                    matched_request_id=self.id_mapping[top_idx], 
                    reason="Matched vector threshold."
                )
            return DuplicateResult(
                is_duplicate=False, 
                similarity_score=round(top_score if top_idx != -1 else 0.0, 4), 
                reason="Below threshold."
            )

        # Pure Numpy Cosine Similarity Fallback
        matrix = np.array(self.vectors, dtype=np.float32)
        dot_products = np.dot(matrix, vec_flat)
        top_idx = int(np.argmax(dot_products))
        top_score = float(dot_products[top_idx])

        if top_score >= settings.SIMILARITY_THRESHOLD:
            return DuplicateResult(
                is_duplicate=True,
                similarity_score=round(top_score, 4),
                matched_request_id=self.id_mapping[top_idx],
                reason="Matched vector similarity threshold."
            )

        return DuplicateResult(
            is_duplicate=False,
            similarity_score=round(top_score, 4),
            reason="Below threshold."
        )