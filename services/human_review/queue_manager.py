import asyncpg
import json
from config.settings import get_settings
from common.schemas import PipelineInput, DecisionResult, ConfidenceResult

settings = get_settings()

class HumanReviewQueueManager:
    def __init__(self):
        self.pool: asyncpg.Pool = None

    async def initialize(self):
        self.pool = await asyncpg.create_pool(
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            database=settings.POSTGRES_DB,
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT
        )

    async def enqueue_for_review(
        self,
        inp: PipelineInput,
        decision: DecisionResult,
        confidence: ConfidenceResult,
        reason: str
    ):
        if not self.pool:
            await self.initialize()

        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO human_review_queue 
                (request_id, raw_input, decision, confidence_score, failure_reason, status)
                VALUES ($1, $2, $3, $4, $5, 'PENDING');
                """,
                inp.request_id,
                inp.raw_text,
                decision.decision,
                confidence.confidence_score,
                reason
            )