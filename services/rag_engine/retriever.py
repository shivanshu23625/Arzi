import asyncpg
from typing import List
from config.settings import get_settings
from common.schemas import DocumentChunk
from services.duplicate_detection.embedder import EmbeddingService

settings = get_settings()

class PostgresVectorRetriever:
    def __init__(self, embedder: EmbeddingService):
        self.embedder = embedder
        self.pool: asyncpg.Pool = None

    async def initialize(self):
        self.pool = await asyncpg.create_pool(
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            database=settings.POSTGRES_DB,
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
            min_size=2,
            max_size=settings.POSTGRES_POOL_SIZE
        )

    async def retrieve(self, query: str, top_k: int = 3) -> List[DocumentChunk]:
        if not self.pool:
            await self.initialize()

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

        return [
            DocumentChunk(
                doc_id=str(row["id"]),
                content=row["content"],
                score=float(row["similarity"])
            )
            for row in rows
        ]