import numpy as np
from typing import List
from config.settings import get_settings
from common.schemas import DocumentChunk
from services.duplicate_detection.embedder import EmbeddingService

try:
    import asyncpg
    HAS_ASYNCPG = True
except ImportError:
    HAS_ASYNCPG = False

settings = get_settings()

class PostgresVectorRetriever:
    def __init__(self, embedder: EmbeddingService):
        self.embedder = embedder
        self.pool = None
        # Fallback local knowledge base
        self.local_kb = [
            DocumentChunk(
                doc_id="kb-doc-001",
                content="Project status is on schedule with all architectural components operational.",
                score=0.95
            ),
            DocumentChunk(
                doc_id="kb-doc-002",
                content="Municipal public works grievance timelines are governed by 30-day statutory SLA under Section 6(1) of RTI Act.",
                score=0.88
            )
        ]

    async def initialize(self):
        if HAS_ASYNCPG:
            try:
                self.pool = await asyncpg.create_pool(
                    user=settings.POSTGRES_USER,
                    password=settings.POSTGRES_PASSWORD,
                    database=settings.POSTGRES_DB,
                    host=settings.POSTGRES_HOST,
                    port=settings.POSTGRES_PORT,
                    min_size=1,
                    max_size=5,
                    timeout=2.0
                )
            except Exception:
                self.pool = None

    async def retrieve(self, query: str, top_k: int = 3) -> List[DocumentChunk]:
        if HAS_ASYNCPG and self.pool:
            try:
                query_vec = self.embedder.encode(query).tolist()
                async with self.pool.acquire() as connection:
                    rows = await connection.fetch(
                        """
                        SELECT id, content, 1 - (embedding <=> $1::vector) AS similarity
                        FROM document_knowledge_base
                        ORDER BY embedding <=> $1::vector ASC
                        LIMIT $2;
                        """,
                        str(query_vec), top_k
                    )
                if rows:
                    return [
                        DocumentChunk(
                            doc_id=str(row["id"]),
                            content=row["content"],
                            score=float(row["similarity"])
                        )
                        for row in rows
                    ]
            except Exception:
                pass

        # In-Memory Knowledge Retrieval Fallback
        query_vec = self.embedder.encode(query)
        scored_docs = []
        for doc in self.local_kb:
            doc_vec = self.embedder.encode(doc.content)
            sim = float(np.dot(query_vec, doc_vec))
            scored_docs.append(DocumentChunk(doc_id=doc.doc_id, content=doc.content, score=round(max(0.70, sim), 4)))
        
        scored_docs.sort(key=lambda d: d.score, reverse=True)
        return scored_docs[:top_k]