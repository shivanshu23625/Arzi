import httpx
from typing import List, Optional
from config.settings import get_settings
from common.schemas import DocumentChunk, RAGResult

settings = get_settings()

class LocalRAGEngine:
    def __init__(self):
        self.client = httpx.AsyncClient(base_url=settings.OLLAMA_BASE_URL, timeout=30.0)

    async def generate_grounded_response(self, query: str, docs: List[DocumentChunk]) -> RAGResult:
        if not docs or all(d.score < 0.60 for d in docs):
            return RAGResult(
                retrieved_docs=docs,
                llm_generation=None,
                sufficient_evidence=False
            )

        context_str = "\n\n".join([f"[Source ID: {d.doc_id}] {d.content}" for d in docs])
        prompt = (
            f"You are a strict domain decision model. Use ONLY the context below to answer.\n"
            f"Context:\n{context_str}\n\n"
            f"User Request: {query}\n"
            f"Answer:"
        )

        try:
            response = await self.client.post(
                "/api/generate",
                json={
                    "model": settings.OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": False
                }
            )
            response.raise_for_status()
            text_output = response.json().get("response", "")
            return RAGResult(
                retrieved_docs=docs,
                llm_generation=text_output.strip(),
                sufficient_evidence=True
            )
        except Exception:
            return RAGResult(
                retrieved_docs=docs,
                llm_generation="Retrieved relevant facts successfully. Inference model offline.",
                sufficient_evidence=True
            )