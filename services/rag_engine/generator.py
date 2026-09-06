import time
import httpx
from typing import List
from config.settings import get_settings
from common.schemas import DocumentChunk, RAGResult
from common.logger import logger

settings = get_settings()

class LocalRAGEngine:
    def __init__(self):
        self.client = httpx.AsyncClient(base_url=settings.OLLAMA_BASE_URL, timeout=3.0)
        self._is_available: bool = True
        self._last_failure_time: float = 0.0
        self._retry_cooldown: float = 30.0 # Wait 30 seconds before re-probing offline Ollama

    async def generate_grounded_response(self, query: str, docs: List[DocumentChunk]) -> RAGResult:
        if not docs or all(d.score < 0.60 for d in docs):
            return RAGResult(retrieved_docs=docs, llm_generation=None, sufficient_evidence=False)

        top_doc = docs[0]
        context_str = "\n\n".join([f"[Source ID: {d.doc_id}] {d.content}" for d in docs])
        fallback_text = f"Summary: {top_doc.content} (Derived from Document {top_doc.doc_id})"

        now = time.time()
        # Fast-fail circuit breaker: If Ollama failed recently, bypass network timeout immediately
        if not self._is_available and (now - self._last_failure_time) < self._retry_cooldown:
            return RAGResult(retrieved_docs=docs, llm_generation=fallback_text, sufficient_evidence=True)

        prompt = f"Use ONLY the context below to answer.\nContext:\n{context_str}\n\nUser Request: {query}\nAnswer:"

        try:
            response = await self.client.post("/api/generate", json={"model": settings.OLLAMA_MODEL, "prompt": prompt, "stream": False})
            response.raise_for_status()
            gen_text = response.json().get("response", "").strip()
            self._is_available = True
            return RAGResult(retrieved_docs=docs, llm_generation=gen_text, sufficient_evidence=True)
        except Exception as e:
            self._is_available = False
            self._last_failure_time = now
            logger.info(f"Ollama Inference Offline/Unavailable ({e}). Engaged fast-fail circuit breaker. Using deterministic grounded context fallback.")
            return RAGResult(retrieved_docs=docs, llm_generation=fallback_text, sufficient_evidence=True)