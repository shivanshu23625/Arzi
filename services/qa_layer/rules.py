from common.schemas import DecisionResult, ConfidenceResult, QAResult
from typing import Dict, Any

class QualityAssuranceEngine:
    def enforce_quality_gate(
        self,
        decision: DecisionResult,
        confidence: ConfidenceResult,
        payload_data: Dict[str, Any]
    ) -> QAResult:
        
        reasons = []

        if not decision.decision or not decision.model_version:
            reasons.append("Structural Failure: Missing required prediction metadata fields.")

        if confidence.requires_human_review:
            reasons.append("Uncertainty Failure: Confidence bounds require human intervention.")

        if decision.decision == "PROCESS_EXECUTION_SUCCESS" and not payload_data.get("generation"):
            reasons.append("Evidence Contradiction: Execution success flagged without backing response generation.")

        passed = len(reasons) == 0
        return QAResult(
            passed=passed,
            final_output=payload_data if passed else None,
            failure_reasons=reasons
        )