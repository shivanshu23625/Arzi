from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class PipelineInput(BaseModel):
    request_id: str = Field(..., description="Unique UUID for tracing execution context.")
    raw_text: str = Field(..., max_length=10000, description="Raw request text payload.")
    user_id: Optional[str] = Field(None, description="Request caller identity.")

class ValidationResult(BaseModel):
    valid: bool
    normalized_input: str
    request_id: str
    rejection_reason: Optional[str] = None

class DuplicateResult(BaseModel):
    is_duplicate: bool
    similarity_score: float
    matched_request_id: Optional[str] = None
    reason: str

class SpamResult(BaseModel):
    classification: str
    spam_score: float
    authenticity_score: float
    reason: str

class DocumentChunk(BaseModel):
    doc_id: str
    content: str
    score: float

class RAGResult(BaseModel):
    retrieved_docs: List[DocumentChunk]
    llm_generation: Optional[str] = None
    sufficient_evidence: bool

class DecisionResult(BaseModel):
    decision: str
    primary_reason: str
    model_version: str

class ConfidenceResult(BaseModel):
    confidence_score: float
    confidence_level: str  # HIGH, MEDIUM, LOW
    requires_human_review: bool
    calibration_reason: str

class QAResult(BaseModel):
    passed: bool
    final_output: Optional[Dict[str, Any]] = None
    failure_reasons: List[str] = []

class MasterPipelineResponse(BaseModel):
    request_id: str
    status: str
    output: Optional[Dict[str, Any]]
    confidence: ConfidenceResult
    qa_status: QAResult
    execution_time_ms: float