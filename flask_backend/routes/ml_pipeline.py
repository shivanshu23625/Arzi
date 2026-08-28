import time
import asyncio
from flask import Blueprint, request, jsonify
from common.schemas import PipelineInput, MasterPipelineResponse
from services.input_validator.validator import InputValidatorService
from services.duplicate_detection.embedder import EmbeddingService
from services.duplicate_detection.vector_store import FAISSVectorStore, HAS_FAISS
from services.spam_classifier.model import SpamClassifierService
from services.rag_engine.retriever import PostgresVectorRetriever
from services.rag_engine.generator import LocalRAGEngine
from services.decision_engine.pipeline import UnifiedDecisionEngine
from services.confidence_engine.calibrator import CalibratedConfidenceEngine
from services.qa_layer.rules import QualityAssuranceEngine

ml_bp = Blueprint("ml_pipeline", __name__, url_prefix="/api/v1")

validator = InputValidatorService()
embedder = EmbeddingService()
vector_store = FAISSVectorStore()
spam_classifier = SpamClassifierService()
retriever = PostgresVectorRetriever(embedder)
rag_generator = LocalRAGEngine()
decision_engine = UnifiedDecisionEngine()
confidence_engine = CalibratedConfidenceEngine()
qa_engine = QualityAssuranceEngine()

def run_async(coro):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)

@ml_bp.route("/reset", methods=["POST", "DELETE"])
def reset_ml_store():
    """Reset vector store in memory for deterministic dataset testing."""
    vector_store.vectors.clear()
    vector_store.id_mapping.clear()
    if HAS_FAISS and vector_store.index:
        vector_store.index.reset()
    return jsonify({"status": "reset", "message": "Vector store reset successfully"}), 200

@ml_bp.route("/process", methods=["POST"])
def process_pipeline():
    start_time = time.perf_counter()
    data = request.get_json() or {}

    req_id = data.get("request_id", "req-000")
    raw_text = data.get("raw_text", "")

    payload = PipelineInput(request_id=req_id, raw_text=raw_text, user_id=data.get("user_id"))

    val_res = validator.validate_and_normalize(payload)
    if not val_res.valid:
        return jsonify({
            "request_id": req_id,
            "status": "REJECTED_INPUT",
            "rejection_reason": val_res.rejection_reason,
            "output": None,
            "execution_time_ms": round((time.perf_counter() - start_time) * 1000.0, 2)
        }), 400

    query_vec = embedder.encode(val_res.normalized_input)
    dup_res = vector_store.search_duplicate(query_vec)
    spam_res = spam_classifier.predict(val_res.normalized_input)

    retrieved_docs = run_async(retriever.retrieve(val_res.normalized_input))
    rag_res = run_async(rag_generator.generate_grounded_response(val_res.normalized_input, retrieved_docs))

    decision_res = decision_engine.evaluate(val_res, dup_res, spam_res, rag_res)
    conf_res = confidence_engine.compute_confidence(dup_res, spam_res, rag_res, decision_res)

    output_payload = {
        "generation": rag_res.llm_generation,
        "evidence": [d.doc_id for d in retrieved_docs]
    }
    qa_res = qa_engine.enforce_quality_gate(decision_res, conf_res, output_payload)

    # Store vector if valid and not duplicate
    if not dup_res.is_duplicate and val_res.valid and decision_res.decision == "PROCESS_EXECUTION_SUCCESS":
        vector_store.add_vector(query_vec, payload.request_id)

    execution_time = (time.perf_counter() - start_time) * 1000.0

    return jsonify({
        "request_id": payload.request_id,
        "status": decision_res.decision,
        "output": qa_res.final_output,
        "confidence": conf_res.model_dump(),
        "qa_status": qa_res.model_dump(),
        "execution_time_ms": round(execution_time, 2)
    }), 200
