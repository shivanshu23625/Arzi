import numpy as np
from config.settings import get_settings
from common.schemas import (
    DuplicateResult, SpamResult, RAGResult, DecisionResult, ConfidenceResult
)

settings = get_settings()

class CalibratedConfidenceEngine:
    def __init__(self):
        self.w_spam = -2.5
        self.w_rag = 3.0
        self.w_dup = -1.0
        self.intercept = 0.5

    def compute_confidence(
        self,
        dup: DuplicateResult,
        spam: SpamResult,
        rag: RAGResult,
        decision: DecisionResult
    ) -> ConfidenceResult:
        
        rag_top_score = rag.retrieved_docs[0].score if rag.retrieved_docs else 0.0
        
        z = (
            self.intercept 
            + (self.w_spam * spam.spam_score) 
            + (self.w_rag * rag_top_score)
            + (self.w_dup * (1.0 if dup.is_duplicate else 0.0))
        )
        
        calibrated_score = float(1.0 / (1.0 + np.exp(-z)))

        if calibrated_score >= settings.CONFIDENCE_HIGH_THRESHOLD:
            level = "HIGH"
            needs_review = False
        elif calibrated_score >= settings.CONFIDENCE_LOW_THRESHOLD:
            level = "MEDIUM"
            needs_review = False
        else:
            level = "LOW"
            needs_review = True

        return ConfidenceResult(
            confidence_score=round(calibrated_score, 4),
            confidence_level=level,
            requires_human_review=needs_review,
            calibration_reason=f"Platt score derived output: {calibrated_score:.4f}"
        )