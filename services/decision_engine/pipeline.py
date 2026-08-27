from common.schemas import (
    ValidationResult, DuplicateResult, SpamResult, RAGResult, DecisionResult
)

class UnifiedDecisionEngine:
    def __init__(self):
        self.version = "1.0.0-fused"

    def evaluate(
        self,
        val: ValidationResult,
        dup: DuplicateResult,
        spam: SpamResult,
        rag: RAGResult
    ) -> DecisionResult:
        
        # 1. Validation Check
        if not val.valid:
            return DecisionResult(
                decision="REJECTED_INPUT",
                primary_reason=val.rejection_reason or "Input validation failure.",
                model_version=self.version
            )

        # 2. Duplicate Check
        if dup.is_duplicate:
            return DecisionResult(
                decision="SHORT_CIRCUIT_DUPLICATE",
                primary_reason=f"Matched duplicate execution context: {dup.matched_request_id}",
                model_version=self.version
            )

        # 3. Spam Check (Moved BEFORE RAG evidence check)
        if spam.classification == "SPAM":
            return DecisionResult(
                decision="REJECTED_SPAM",
                primary_reason=f"Spam score ({spam.spam_score:.2f}) exceeds policy limits.",
                model_version=self.version
            )

        # 4. RAG Evidence Check
        if not rag.sufficient_evidence:
            return DecisionResult(
                decision="INSUFFICIENT_CONTEXT",
                primary_reason="Retrieved knowledge base entries fell below evidence thresholds.",
                model_version=self.version
            )

        return DecisionResult(
            decision="PROCESS_EXECUTION_SUCCESS",
            primary_reason="All evidence metrics passed pipeline constraints.",
            model_version=self.version
        )