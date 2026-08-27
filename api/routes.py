from fastapi import APIRouter, HTTPException, Depends
import time
from common.schemas import PipelineInput, MasterPipelineResponse
from services.input_validator.validator import InputValidatorService
from services.duplicate_detection.embedder import EmbeddingService
from services.duplicate_detection.vector_store import FAISSVectorStore
from services.spam_classifier.model import SpamClassifierService
from services.rag_engine.retriever import PostgresVectorRetriever
from services.rag_engine.generator import LocalRAGEngine
from services.decision_engine.pipeline import UnifiedDecisionEngine
from services.confidence_engine.calibrator import CalibratedConfidenceEngine
from services.qa_layer.rules import QualityAssuranceEngine
from services.human_review.queue_manager import HumanReviewQueueManager

router = APIRouter()

validator = InputValidatorService()
embedder = EmbeddingService()
vector_store = FAISSVectorStore()
spam_classifier = SpamClassifierService()
retriever = PostgresVectorRetriever(embedder)
rag_generator = LocalRAGEngine()
decision_engine = UnifiedDecisionEngine()
confidence_engine = CalibratedConfidenceEngine()
qa_engine = QualityAssuranceEngine()
review_queue = HumanReviewQueueManager()

@router.post("/process", response_model=MasterPipelineResponse)
async def process_pipeline(payload: PipelineInput):
    start_time = time.perf_counter()

    val_res = validator.validate_and_normalize(payload)
    if not val_res.valid:
        raise HTTPException(status_code=400, detail=val_res.rejection_reason)

    query_vec = embedder.encode(val_res.normalized_input)
    dup_res = vector_store.search_duplicate(query_vec)

    spam_res = spam_classifier.predict(val_res.normalized_input)

    retrieved_docs = await retriever.retrieve(val_res.normalized_input)
    rag_res = await rag_generator.generate_grounded_response(val_res.normalized_input, retrieved_docs)

    decision_res = decision_engine.evaluate(val_res, dup_res, spam_res, rag_res)

    conf_res = confidence_engine.compute_confidence(dup_res, spam_res, rag_res, decision_res)

    output_payload = {"generation": rag_res.llm_generation, "evidence": [d.doc_id for d in retrieved_docs]}
    qa_res = qa_engine.enforce_quality_gate(decision_res, conf_res, output_payload)

    if not dup_res.is_duplicate and val_res.valid:
        vector_store.add_vector(query_vec, payload.request_id)

    if not qa_res.passed:
        await review_queue.enqueue_for_review(
            payload, decision_res, conf_res, ", ".join(qa_res.failure_reasons)
        )

    execution_time = (time.perf_counter() - start_time) * 1000.0

    return MasterPipelineResponse(
        request_id=payload.request_id,
        status=decision_res.decision,
        output=qa_res.final_output,
        confidence=conf_res,
        qa_status=qa_res,
        execution_time_ms=round(execution_time, 2)
    )