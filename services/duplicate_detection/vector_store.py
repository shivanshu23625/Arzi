import faiss
import numpy as np
from typing import List, Tuple, Optional
from config.settings import get_settings
from common.schemas import DuplicateResult

settings = get_settings()

class FAISSVectorStore:
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(self.dimension)
        self.id_mapping: List[str] = []

    def add_vector(self, vec: np.ndarray, request_id: str):
        if vec.ndim == 1:
            vec = np.expand_dims(vec, axis=0)
        self.index.add(vec)
        self.id_mapping.append(request_id)

    def search_duplicate(self, vec: np.ndarray) -> DuplicateResult:
        if self.index.ntotal == 0:
            return DuplicateResult(
                is_duplicate=False,
                similarity_score=0.0,
                matched_request_id=None,
                reason="Vector index is currently empty."
            )

        if vec.ndim == 1:
            vec = np.expand_dims(vec, axis=0)

        scores, indices = self.index.search(vec, k=1)
        top_score = float(scores[0][0])
        top_idx = int(indices[0][0])

        if top_idx != -1 and top_score >= settings.SIMILARITY_THRESHOLD:
            return DuplicateResult(
                is_duplicate=True,
                similarity_score=top_score,
                matched_request_id=self.id_mapping[top_idx],
                reason=f"Matched vector index threshold with inner product score {top_score:.4f}"
            )

        return DuplicateResult(
            is_duplicate=False,
            similarity_score=top_score if top_idx != -1 else 0.0,
            matched_request_id=None,
            reason="Similarity score below semantic duplication threshold."
        )